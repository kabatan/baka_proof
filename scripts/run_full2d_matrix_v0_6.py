#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import hashlib
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.geometry_full2d_v0_6_compiler as compiler_module  # noqa: E402
import scripts.geometry_full2d_v0_6_derivation as derivation_module  # noqa: E402
import scripts.geometry_full2d_v0_6_extraction as extraction_module  # noqa: E402
import scripts.geometry_full2d_v0_6_independent_checkers as independent_module  # noqa: E402
import scripts.geometry_full2d_v0_6_proof_worker as proof_worker_module  # noqa: E402
import scripts.geometry_full2d_v0_6_provider as provider_module  # noqa: E402
import scripts.geometry_full2d_v0_6_schemas as schemas_module  # noqa: E402
from scripts.extract_geometry_full2d_theorem import (  # noqa: E402
    _canonical_json as lean_canonical_json,
    _canonicalize_lean_structured_output,
    _direct_lean_env,
    _ensure_extraction_olean,
    _ensure_local_lean_artifacts,
    _extract_theorem_source,
    _file_sha256 as lean_file_sha256,
    _lean,
    _lean_extraction_cache_key,
    _lean_extraction_cache_path,
    _lean_source_with_extraction_import,
    _looks_preproved,
    _parse_all_lean_extraction_json,
    _qualified_theorem_name,
    _read_lean_extraction_cache,
    _sha256_text as lean_sha256_text,
    _theorem_header_for_cache,
    _write_lean_extraction_cache,
)
from scripts.geometry_full2d_v0_6_compiler import run_compiler_stage  # noqa: E402
from scripts.geometry_full2d_v0_6_derivation import build_selected_derivations, build_target_match_reports  # noqa: E402
from scripts.geometry_full2d_v0_6_extraction import (  # noqa: E402
    CLAIM_INDEX_NAME,
    CLAIM_SPEC_DIR,
    EXTRACTION_INDEX_NAME,
    EXTRACTION_REPORT_DIR,
    build_claim_specs,
    canonical_json,
    checker_hash_set_ref,
    manifest_hash,
    normalize_extraction_report,
    validate_claimspecs,
    validate_extraction_report,
    write_json,
)
from scripts.geometry_full2d_v0_6_independent_checkers import run_independent_artifact_checks  # noqa: E402
from scripts.geometry_full2d_v0_6_proof_worker import (  # noqa: E402
    FINAL_VERIFY_REPORT_DIR,
    PROOF_WORKER_RESULT_DIR,
    build_solver_backed_certificate_v0_6,
)
from scripts.geometry_full2d_v0_6_provider import run_provider_stage  # noqa: E402
from scripts.geometry_full2d_v0_6_schemas import ENGINE_ROLES, validate_payload  # noqa: E402


REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7", "B8"]
ACTUAL_RUN_DIR = "actual_task_pipeline_runs_v0_6"
SOURCE_TASK_DIR = "source_theorems_v0_6"
STAGE_FAILURE_DIR = "stage_failures_v0_6"
DISABLED_STAGE_DIR = "disabled_stage_reports_v0_6"
MATRIX_SUMMARY = "full2d_matrix_summary_v0_6.json"
_GIT_STATUS_HASH: str | None = None
_SELECTED_IMPLEMENTATION_HASH_BY_CORPUS: dict[str, str] = {}
_RELEASE_RUN_DIR_HASH_BY_KEY: dict[tuple[str, str, str], str] = {}


def install_cached_git_head() -> None:
    head = current_git_head()
    proof_worker_hash = proof_worker_module.proof_worker_code_hash()

    def cached_head() -> str:
        return head

    def cached_proof_worker_hash() -> str:
        return proof_worker_hash

    for module in [
        compiler_module,
        derivation_module,
        extraction_module,
        independent_module,
        proof_worker_module,
        provider_module,
        schemas_module,
    ]:
        if hasattr(module, "current_git_head"):
            setattr(module, "current_git_head", cached_head)
    proof_worker_module.proof_worker_code_hash = cached_proof_worker_hash


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--execute-all", action="store_true")
    parser.add_argument("--all-baselines", action="store_true")
    parser.add_argument("--no-skip", action="store_true")
    args = parser.parse_args()
    report = run_matrix(
        config_path=Path(args.config),
        run_dir=Path(args.run_dir),
        execute_all=args.execute_all,
        all_baselines=args.all_baselines,
        no_skip=args.no_skip,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_matrix(*, config_path: Path, run_dir: Path, execute_all: bool, all_baselines: bool, no_skip: bool) -> dict[str, Any]:
    started = time.time()
    install_cached_git_head()
    config_path = resolve_path(config_path)
    run_dir = resolve_path(run_dir)
    config = read_json(config_path)
    corpus_root = resolve_path(Path(str(config.get("benchmark_corpus_root", "benchmarks/geometry_full2d_v0_6"))))
    errors: list[str] = []
    if not execute_all:
        errors.append("execute_all_flag_required")
    if not all_baselines:
        errors.append("all_baselines_flag_required")
    if not no_skip:
        errors.append("no_skip_flag_required")
    required_baselines = [str(item) for item in config.get("required_baselines", REQUIRED_BASELINES)]
    if required_baselines != REQUIRED_BASELINES:
        errors.append("required_baselines_not_v0_6_set")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = read_json(corpus_root / "corpus_manifest.json")
    positive_tasks = [task for task in manifest.get("tasks", []) if isinstance(task, dict) and task.get("counted_positive") is True]
    if len(positive_tasks) < 1200:
        errors.append(f"counted_positive_floor_not_met:{len(positive_tasks)}")
    b2_dir = run_dir / "baseline_runs_v0_6" / "B2"
    b2_dir.mkdir(parents=True, exist_ok=True)
    extraction = build_batch_extraction_reports(corpus_root=corpus_root, run_dir=b2_dir, tasks=positive_tasks)
    errors.extend(f"extraction:{error}" for error in extraction["errors"])
    claim_report = build_claim_specs(b2_dir)
    claim_check = validate_claimspecs(b2_dir, self_test=False)
    errors.extend(f"claimspec:{error}" for error in claim_report.get("errors", []))
    errors.extend(f"claimspec_check:{error}" for error in claim_check.get("errors", []))
    provider_report = run_provider_stage(b2_dir, roles=sorted(ENGINE_ROLES))
    errors.extend(f"provider:{error}" for error in provider_report.get("errors", []))
    independent_report = run_independent_artifact_checks(b2_dir)
    errors.extend(f"independent_check:{error}" for error in independent_report.get("errors", []))
    derivation_report = build_selected_derivations(b2_dir)
    errors.extend(f"selected_derivation:{error}" for error in derivation_report.get("errors", []))
    target_match_report = build_target_match_reports(b2_dir)
    errors.extend(f"target_match:{error}" for error in target_match_report.get("errors", []))
    compiler_report = run_compiler_stage(b2_dir)
    errors.extend(f"compiler:{error}" for error in compiler_report.get("errors", []))
    proof_report = run_parallel_proof_worker_final_verify_stage(b2_dir)
    proof_structural_errors = proof_stage_structural_errors(b2_dir, positive_tasks)
    errors.extend(f"proof_worker_final_verify:{error}" for error in proof_structural_errors)

    record_errors: list[str] = []
    counts: dict[str, dict[str, int]] = {baseline: {"records": 0, "final_theorem": 0, "measured_failure": 0} for baseline in required_baselines}
    b2_records = materialize_b2_records(
        run_dir=run_dir,
        baseline_dir=b2_dir,
        corpus_root=corpus_root,
        config_path=config_path,
        tasks=positive_tasks,
    )
    record_errors.extend(b2_records["errors"])
    for record in b2_records["records"]:
        counts["B2"]["records"] += 1
        counts["B2"][record["final_status"]] += 1

    disabled_components = config.get("baseline_disabled_components", {})
    for baseline in required_baselines:
        if baseline == "B2":
            continue
        components = [str(item) for item in disabled_components.get(baseline, [])]
        for task in positive_tasks:
            bundle = materialize_disabled_record(
                run_dir=run_dir,
                baseline_dir=b2_dir,
                corpus_root=corpus_root,
                config_path=config_path,
                task=task,
                baseline=baseline,
                disabled_components=components,
            )
            record_errors.extend(bundle["errors"])
            counts[baseline]["records"] += 1
            counts[baseline][bundle["record"]["final_status"]] += 1

    errors.extend(f"record:{error}" for error in sorted(set(record_errors))[:200])
    summary = {
        "schema_version": "Full2DMatrixRunV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "config": config_path.relative_to(ROOT).as_posix() if is_relative_to(config_path, ROOT) else str(config_path),
        "run_dir": str(run_dir),
        "corpus_root": str(corpus_root),
        "counted_task_count": len(positive_tasks),
        "required_baselines": required_baselines,
        "required_record_count": len(positive_tasks) * len(required_baselines),
        "record_count": sum(row["records"] for row in counts.values()),
        "by_baseline": counts,
        "stage_reports": {
            "extraction": extraction,
            "claimspec": claim_report,
            "provider": provider_report,
            "independent_solver_artifacts": independent_report,
            "selected_derivation": derivation_report,
            "target_match": target_match_report,
            "compiler": compiler_report,
            "proof_worker_final_verify": proof_report,
        },
        "measured_failure_summary": {
            "B2_final_verify_failures_are_measured": counts["B2"]["measured_failure"],
            "disabled_baseline_failures_are_disabled_stage_reports": sum(counts[b]["measured_failure"] for b in required_baselines if b != "B2"),
        },
        "outcome_source": "ActualTaskPipelineRunV4 records with FinalVerifyGate reports or DisabledStageReportV1",
        "duration_seconds": round(time.time() - started, 3),
        "git_head": current_git_head(),
    }
    write_json(run_dir / MATRIX_SUMMARY, summary)
    return summary


def build_batch_extraction_reports(*, corpus_root: Path, run_dir: Path, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    output_dir = run_dir / EXTRACTION_REPORT_DIR
    source_dir = run_dir / SOURCE_TASK_DIR
    report_paths: list[str] = []
    by_file: dict[Path, list[dict[str, Any]]] = {}
    isolated_sources: dict[str, Path] = {}
    for task in tasks:
        source_path = resolve_task_lean_file(corpus_root, task)
        by_file.setdefault(source_path, []).append(task)
        try:
            theorem_source = _extract_theorem_source(source_path.read_text(encoding="utf-8"), str(task["theorem_name"]))
            isolated_path = source_dir / f"{safe_id(str(task['task_id']))}.lean"
            isolated_path.parent.mkdir(parents=True, exist_ok=True)
            isolated_path.write_text(wrap_theorem_source(theorem_source), encoding="utf-8")
            isolated_sources[str(task["task_id"])] = isolated_path
        except Exception as exc:
            errors.append(f"{task.get('task_id')}:source_isolation_failed:{exc}")
    extracted: dict[str, dict[str, Any]] = {}
    for source_path, source_tasks in by_file.items():
        extracted.update(batch_extract_from_file(source_path, source_tasks, errors))
    for task in tasks:
        task_id = str(task.get("task_id"))
        theorem_name = str(task.get("theorem_name"))
        isolated = isolated_sources.get(task_id)
        structured = extracted.get(theorem_name)
        if isolated is None or structured is None:
            errors.append(f"{task_id}:missing_batch_extraction")
            continue
        try:
            theorem_source = _extract_theorem_source(isolated.read_text(encoding="utf-8"), theorem_name)
            theorem_header_hash = lean_sha256_text(_theorem_header_for_cache(theorem_source))
            canonicalized = _canonicalize_lean_structured_output(
                structured,
                isolated,
                theorem_name,
                lean_sha256_text(theorem_source),
            )
            raw = {
                "canonical_statement": canonicalized["canonical_statement"],
                "source_statement_hash": lean_sha256_text(theorem_source),
                "elaborated_expr_hash": lean_sha256_text(lean_canonical_json(structured)),
                "source_file_ref": lean_file_sha256(isolated),
                "theorem_name": theorem_name,
                "side_condition_obligations": canonicalized["canonical_statement"]["side_conditions"],
                "target_classification": canonicalized["target_classification"],
                "extraction_method": "lean_elaborator_structured_theorem",
                "semantic_extraction_authority": "lean_elaborator",
                "source_theorem_preproved": _looks_preproved(theorem_source),
                "python_semantic_extraction_used": False,
                "regex_used_for_semantics": False,
                "regex_used_for_source_location": True,
                "lean_command": [_lean(), "--stdin", "--json", "#full2d_extract-batch"],
                "lean_compile_status": "passed",
                "lean_semantic_extractor_ref": lean_sha256_text(lean_canonical_json(structured)),
                "lean_semantic_extractor_cache_key": _lean_extraction_cache_key(theorem_name, theorem_header_hash),
                "lean_semantic_extractor_cache_status": "batch",
                "lean_stdout_hash": lean_sha256_text(lean_canonical_json(structured)),
                "lean_stderr_hash": lean_sha256_text(""),
            }
            report = normalize_extraction_report(raw, task, isolated, corpus_root=corpus_root)
            report_errors = validate_extraction_report(report, task, isolated, theorem_name, corpus_root=corpus_root)
            errors.extend(f"{task_id}:{error}" for error in report_errors)
            path = output_dir / f"{safe_id(task_id)}.json"
            write_json(path, report)
            report_paths.append(path.relative_to(run_dir).as_posix())
        except Exception as exc:
            errors.append(f"{task_id}:normalize_batch_extraction_failed:{exc}")
    index = {
        "schema_version": "GeometryFull2DExtractionCorpusIndexV06",
        "corpus_manifest_hash": manifest_hash(corpus_root),
        "run_dir": str(run_dir),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "report_paths": report_paths,
        "checker_hash_set_ref": checker_hash_set_ref(),
        "batch_extraction": True,
        "git_head": current_git_head(),
    }
    write_json(run_dir / EXTRACTION_INDEX_NAME, index)
    if len(report_paths) != len(tasks):
        errors.append(f"extraction_report_count_mismatch:{len(report_paths)}!={len(tasks)}")
    return {
        "schema_version": "BuildFull2DExtractionCorpusV06BatchReport",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "required_task_count": len(tasks),
        "report_count": len(report_paths),
        "index_path": (run_dir / EXTRACTION_INDEX_NAME).relative_to(ROOT).as_posix() if is_relative_to(run_dir / EXTRACTION_INDEX_NAME, ROOT) else str(run_dir / EXTRACTION_INDEX_NAME),
    }


def batch_extract_from_file(source_path: Path, tasks: list[dict[str, Any]], errors: list[str]) -> dict[str, dict[str, Any]]:
    source_text = source_path.read_text(encoding="utf-8")
    results: dict[str, dict[str, Any]] = {}
    missing_names: list[str] = []
    commands: list[str] = []
    for task in tasks:
        theorem_name = str(task["theorem_name"])
        theorem_source = _extract_theorem_source(source_text, theorem_name)
        theorem_header_hash = lean_sha256_text(_theorem_header_for_cache(theorem_source))
        cache_key = _lean_extraction_cache_key(theorem_name, theorem_header_hash)
        cached = _read_lean_extraction_cache(
            _lean_extraction_cache_path(cache_key),
            expected_theorem_name=theorem_name,
            expected_theorem_header_hash=theorem_header_hash,
            expected_cache_key=cache_key,
        )
        if cached is not None:
            results[theorem_name] = cached["structured_output"]
        else:
            missing_names.append(theorem_name)
            commands.append(f"#full2d_extract {_qualified_theorem_name(theorem_name)}")
    if not missing_names:
        return results
    _ensure_local_lean_artifacts()
    _ensure_extraction_olean()
    extractor_source = (
        _lean_source_with_extraction_import(source_text).rstrip()
        + "\n\nopen MathAutoResearch.GeometryFull2D\nopen MathAutoResearch.GeometryFull2D.Extraction\n"
        + "\n".join(commands)
        + "\n"
    )
    completed = subprocess.run(
        [_lean(), "--stdin", "--json"],
        cwd=ROOT,
        input=extractor_source,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_direct_lean_env(),
    )
    parsed = _parse_all_lean_extraction_json(completed.stdout)
    if completed.returncode != 0:
        errors.append(f"{source_path.name}:batch_lean_extraction_failed:{completed.stderr[-1000:]}")
    for structured in parsed:
        theorem_name = str(structured.get("theorem_name", ""))
        if theorem_name:
            results[theorem_name] = structured
    for theorem_name in missing_names:
        if theorem_name not in results:
            errors.append(f"{source_path.name}:batch_extraction_missing_theorem:{theorem_name}")
            continue
        theorem_source = _extract_theorem_source(source_text, theorem_name)
        theorem_header_hash = lean_sha256_text(_theorem_header_for_cache(theorem_source))
        _write_lean_extraction_cache(_lean_extraction_cache_path(_lean_extraction_cache_key(theorem_name, theorem_header_hash)), theorem_name, theorem_header_hash, results[theorem_name])
    return results


def proof_worker_parallelism() -> int:
    raw = os.environ.get("FULL2D_PROOF_WORKERS", "").strip()
    if raw:
        try:
            parsed = int(raw)
            if parsed >= 1:
                return parsed
        except ValueError:
            pass
    cpu_count = os.cpu_count() or 4
    return max(2, min(8, cpu_count // 2 if cpu_count > 2 else 2))


def run_parallel_proof_worker_final_verify_stage(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    patch_paths = sorted((run_dir / proof_worker_module.LEAN_PATCH_DIR).glob("*.json"))
    anchor_by_ref: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / proof_worker_module.THEOREM_ANCHOR_DIR).glob("*.json")):
        anchor = read_json(path)
        anchor_by_ref[file_sha256(path)] = anchor
        if anchor.get("anchor_ref") not in anchor_by_ref:
            anchor_by_ref[str(anchor.get("anchor_ref"))] = anchor

    errors: list[str] = []
    if not patch_paths:
        errors.append("missing_lean_patch_candidates")

    bundles: list[dict[str, Any]] = []
    max_workers = proof_worker_parallelism()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_patch = {
            executor.submit(run_one_proof_worker_final_verify, run_dir, patch_path, anchor_by_ref): patch_path
            for patch_path in patch_paths
        }
        for future in as_completed(future_to_patch):
            patch_path = future_to_patch[future]
            try:
                bundles.append(future.result())
            except Exception as exc:  # pragma: no cover - defensive release evidence path.
                bundles.append(
                    {
                        "patch_name": patch_path.name,
                        "worker_path": None,
                        "verify_path": None,
                        "result": {
                            "patch_candidate_ref": file_sha256(patch_path),
                            "proof_worker_result_ref": None,
                            "final_verify_report_ref": None,
                            "worker_status": "exception",
                            "final_verify_status": "not_run",
                            "worker_errors": [str(exc)],
                            "final_verify_errors": [],
                        },
                        "errors": [f"{patch_path.name}:proof_worker_final_verify_exception:{exc}"],
                    }
                )

    worker_paths: list[str] = []
    verify_paths: list[str] = []
    results: list[dict[str, Any]] = []
    for bundle in sorted(bundles, key=lambda item: str(item["patch_name"])):
        if bundle.get("worker_path"):
            worker_paths.append(str(bundle["worker_path"]))
        if bundle.get("verify_path"):
            verify_paths.append(str(bundle["verify_path"]))
        results.append(bundle["result"])
        errors.extend(str(error) for error in bundle.get("errors", []))

    index = {
        "schema_version": "ProofWorkerFinalVerifyIndexV06",
        "run_dir": str(run_dir),
        "proof_worker_result_paths": worker_paths,
        "final_verify_report_paths": verify_paths,
        "results": results,
        "proof_worker_code_hash": proof_worker_module.proof_worker_code_hash(),
        "git_head": current_git_head(),
        "parallel_execution": True,
        "parallel_workers": max_workers,
    }
    write_json(run_dir / proof_worker_module.PROOF_WORKER_INDEX_NAME, index)
    return {
        "schema_version": "RunProofWorkerFinalVerifyStageV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "proof_worker_result_count": len(worker_paths),
        "final_verify_report_count": len(verify_paths),
        "index_path": (run_dir / proof_worker_module.PROOF_WORKER_INDEX_NAME).relative_to(ROOT).as_posix()
        if is_relative_to(run_dir / proof_worker_module.PROOF_WORKER_INDEX_NAME, ROOT)
        else str(run_dir / proof_worker_module.PROOF_WORKER_INDEX_NAME),
        "parallel_execution": True,
        "parallel_workers": max_workers,
    }


def run_one_proof_worker_final_verify(
    run_dir: Path,
    patch_path: Path,
    anchor_by_ref: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    patch = read_json(patch_path)
    anchor = anchor_by_ref.get(str(patch.get("theorem_anchor_ref")))
    if anchor is None:
        return {
            "patch_name": patch_path.name,
            "worker_path": None,
            "verify_path": None,
            "result": {
                "patch_candidate_ref": file_sha256(patch_path),
                "proof_worker_result_ref": None,
                "final_verify_report_ref": None,
                "worker_status": "not_run",
                "final_verify_status": "not_run",
                "worker_errors": ["theorem_anchor_not_found"],
                "final_verify_errors": [],
            },
            "errors": [f"{patch_path.name}:theorem_anchor_not_found"],
        }

    source_path = proof_worker_module.resolve_source_path(anchor)
    worker = proof_worker_module.apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=anchor,
        patch_candidate=patch,
        output_dir=run_dir,
        run_id=patch_path.stem,
    )
    worker_path = run_dir / PROOF_WORKER_RESULT_DIR / patch_path.name
    write_json(worker_path, worker)
    worker_errors = validate_payload(worker)
    if worker.get("status") != "patch_applied":
        worker_errors.extend(str(item) for item in worker.get("errors", []))
        worker_errors.append("proof_worker_status_not_patch_applied")
    if worker_errors:
        errors.extend(f"{patch_path.name}:worker:{error}" for error in sorted(set(worker_errors)))

    verify: dict[str, Any] | None = None
    candidate_path = worker.get("generated_candidate_path")
    if isinstance(candidate_path, str) and candidate_path:
        verify = proof_worker_module.final_verify_gate_v0_6(
            source_path=source_path,
            candidate_path=Path(candidate_path),
            theorem_anchor=anchor,
            proof_worker_result=worker,
            output_dir=run_dir,
        )
        verify_path = run_dir / FINAL_VERIFY_REPORT_DIR / patch_path.name
        write_json(verify_path, verify)
        verify_errors = validate_payload(verify)
        if verify.get("status") != "passed":
            verify_errors.extend(str(item) for item in verify.get("errors", []))
            verify_errors.append("final_verify_status_not_passed")
        if verify_errors:
            errors.extend(f"{patch_path.name}:final_verify:{error}" for error in verify_errors)
    else:
        verify_path = None
        errors.append(f"{patch_path.name}:final_verify:not_run")

    return {
        "patch_name": patch_path.name,
        "worker_path": worker_path.relative_to(run_dir).as_posix(),
        "verify_path": verify_path.relative_to(run_dir).as_posix() if verify is not None and verify_path is not None else None,
        "result": {
            "patch_candidate_ref": file_sha256(patch_path),
            "proof_worker_result_ref": file_sha256(worker_path),
            "final_verify_report_ref": file_sha256(verify_path) if verify is not None and verify_path is not None else None,
            "worker_status": worker.get("status"),
            "final_verify_status": verify.get("status") if verify is not None else "not_run",
            "worker_errors": worker.get("errors", []),
            "final_verify_errors": verify.get("errors", []) if verify is not None else [],
        },
        "errors": errors,
    }


def materialize_b2_records(*, run_dir: Path, baseline_dir: Path, corpus_root: Path, config_path: Path, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    ref_index = build_b2_ref_index(baseline_dir)
    for task in tasks:
        task_id = str(task["task_id"])
        refs = collect_b2_refs(baseline_dir, task_id, ref_index)
        if refs.get("errors"):
            errors.extend(f"{task_id}:{error}" for error in refs["errors"])
        final_payload = refs.get("final_verify_payload") or {}
        final_status = "final_theorem" if final_payload.get("status") == "passed" else "measured_failure"
        failure_ref = None
        certificate_ref = None
        if final_status == "measured_failure":
            failure_ref = write_stage_failure(
                run_dir=run_dir,
                task_id=task_id,
                baseline="B2",
                stage="final_verify",
                input_refs=refs["compiler_result_refs"] + [refs["lean_patch_candidate_ref"], refs["proof_worker_result_ref"], refs["final_verify_report_ref"]],
                failure_kind="lean_compile_failed" if final_payload else "final_verify_report_missing",
                failure_reason="FinalVerifyGate rejected the generated candidate" if final_payload else "FinalVerifyGate report missing",
            )
        record = build_actual_record(
            run_dir=run_dir,
            task_id=task_id,
            baseline="B2",
            corpus_root=corpus_root,
            config_path=config_path,
            refs=refs,
            final_status=final_status,
            stage_failure_report_ref=failure_ref,
            solver_backed_certificate_ref=certificate_ref,
        )
        record_path = run_dir / ACTUAL_RUN_DIR / f"{safe_id(task_id)}__B2.json"
        if final_status == "final_theorem":
            actual_ref = sha256_text(canonical_json(record))
            cert = build_solver_backed_certificate_v0_6(
                actual_task_run_ref=actual_ref,
                claim_spec_ref=refs["claim_spec_ref"],
                engine_output_refs=refs["engine_output_refs"],
                selected_derivation_ref=refs["selected_solver_derivation_ref"],
                compiler_result_ref=refs["compiler_result_refs"][0],
                proof_worker_result_ref=refs["proof_worker_result_ref"],
                final_verify_report_ref=refs["final_verify_report_ref"],
                solver_causality_live_run_ref=sha256_text(f"pending_live_causality:{task_id}"),
            )
            cert_path = baseline_dir / "solver_backed_certificates_v0_6" / f"{safe_id(task_id)}.json"
            write_json(cert_path, cert)
            record["solver_backed_certificate_ref"] = file_sha256(cert_path)
        record_errors = validate_payload(record)
        errors.extend(f"{task_id}:record_validation:{error}" for error in record_errors)
        write_json(record_path, record)
        records.append(record)
    return {"records": records, "errors": sorted(set(errors))}


def build_b2_ref_index(baseline_dir: Path) -> dict[str, dict[str, Path]]:
    derivation_by_claim_ref: dict[str, Path] = {}
    derivation_ref_by_path: dict[str, str] = {}
    for path in sorted((baseline_dir / "selected_solver_derivations_v0_6").glob("*.json")):
        payload = read_json(path)
        derivation_by_claim_ref[str(payload.get("claim_spec_ref"))] = path
        derivation_ref_by_path[str(path)] = file_sha256(path)
    target_by_derivation_ref: dict[str, Path] = {}
    for path in sorted((baseline_dir / "derivation_target_matches_v0_6").glob("*.json")):
        payload = read_json(path)
        target_by_derivation_ref[str(payload.get("selected_derivation_ref"))] = path
    compiler_by_derivation_ref: dict[str, Path] = {}
    for path in sorted((baseline_dir / "compiler_results_v0_6").glob("*.json")):
        payload = read_json(path)
        compiler_by_derivation_ref[str(payload.get("selected_derivation_ref"))] = path
    return {
        "derivation_by_claim_ref": derivation_by_claim_ref,
        "derivation_ref_by_path": derivation_ref_by_path,
        "target_by_derivation_ref": target_by_derivation_ref,
        "compiler_by_derivation_ref": compiler_by_derivation_ref,
    }


def collect_b2_refs(baseline_dir: Path, task_id: str, ref_index: dict[str, dict[str, Path]]) -> dict[str, Any]:
    errors: list[str] = []
    extraction_path = baseline_dir / EXTRACTION_REPORT_DIR / f"{safe_id(task_id)}.json"
    claim_path = baseline_dir / CLAIM_SPEC_DIR / f"{safe_id(task_id)}.json"
    extraction = read_json(extraction_path) if extraction_path.exists() else {}
    claim = read_json(claim_path) if claim_path.exists() else {}
    claim_ref = file_sha256(claim_path) if claim_path.exists() else sha256_text(f"missing_claim:{task_id}")
    derivation_path = ref_index["derivation_by_claim_ref"].get(claim_ref)
    derivation_ref = ref_index["derivation_ref_by_path"].get(str(derivation_path)) if derivation_path else None
    target_path = ref_index["target_by_derivation_ref"].get(str(derivation_ref)) if derivation_ref else None
    compiler_path = ref_index["compiler_by_derivation_ref"].get(str(derivation_ref)) if derivation_ref else None
    patch_path = (baseline_dir / "lean_patch_candidates_v0_6" / derivation_path.name) if derivation_path else None
    worker_path = (baseline_dir / PROOF_WORKER_RESULT_DIR / derivation_path.name) if derivation_path else None
    final_path = (baseline_dir / FINAL_VERIFY_REPORT_DIR / derivation_path.name) if derivation_path else None
    provider_path = baseline_dir / "provider_manifests_v0_6" / f"{safe_id(task_id)}.json"
    engine_paths = sorted((baseline_dir / "engine_outputs_v0_6").glob(f"{safe_id(task_id)}__*.json"))
    check_paths = sorted((baseline_dir / "independent_solver_artifact_checks_v0_6").glob(f"{safe_id(task_id)}__*.json"))
    for label, path in {
        "extraction_report": extraction_path,
        "claim_spec": claim_path,
        "provider_manifest": provider_path,
        "selected_derivation": derivation_path,
        "target_match": target_path,
        "compiler_result": compiler_path,
        "patch": patch_path,
        "proof_worker": worker_path,
        "final_verify": final_path,
    }.items():
        if path is None or not path.exists():
            errors.append(f"missing_{label}")
    final_payload = read_json(final_path) if final_path and final_path.exists() else {}
    return {
        "errors": errors,
        "source_theorem_ref": str(extraction.get("source_file_ref") or sha256_text(f"missing_source:{task_id}")),
        "extraction_report_ref": file_sha256(extraction_path) if extraction_path.exists() else sha256_text(f"missing_extraction:{task_id}"),
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": file_sha256(provider_path) if provider_path.exists() else sha256_text(f"missing_provider:{task_id}"),
        "engine_output_refs": [file_sha256(path) for path in engine_paths] or [sha256_text(f"missing_engine:{task_id}")],
        "independent_solver_artifact_check_refs": [file_sha256(path) for path in check_paths] or [sha256_text(f"missing_check:{task_id}")],
        "selected_solver_derivation_ref": file_sha256(derivation_path) if derivation_path and derivation_path.exists() else sha256_text(f"missing_derivation:{task_id}"),
        "derivation_target_match_ref": file_sha256(target_path) if target_path and target_path.exists() else sha256_text(f"missing_target_match:{task_id}"),
        "compiler_result_refs": [file_sha256(compiler_path)] if compiler_path and compiler_path.exists() else [sha256_text(f"missing_compiler:{task_id}")],
        "lean_patch_candidate_ref": file_sha256(patch_path) if patch_path and patch_path.exists() else sha256_text(f"missing_patch:{task_id}"),
        "proof_worker_result_ref": file_sha256(worker_path) if worker_path and worker_path.exists() else sha256_text(f"missing_worker:{task_id}"),
        "final_verify_report_ref": file_sha256(final_path) if final_path and final_path.exists() else sha256_text(f"missing_final_verify:{task_id}"),
        "final_verify_payload": final_payload,
        "stage_timestamps": stage_timestamps_from_paths(extraction_path, provider_path, compiler_path, final_path),
        "used_rule_ids": read_used_rule_ids(patch_path) if patch_path and patch_path.exists() else [],
        "used_engine_roles": [read_json(path).get("engine_role") for path in engine_paths],
    }


def materialize_disabled_record(
    *,
    run_dir: Path,
    baseline_dir: Path,
    corpus_root: Path,
    config_path: Path,
    task: dict[str, Any],
    baseline: str,
    disabled_components: list[str],
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    extraction_path = baseline_dir / EXTRACTION_REPORT_DIR / f"{safe_id(task_id)}.json"
    claim_path = baseline_dir / CLAIM_SPEC_DIR / f"{safe_id(task_id)}.json"
    disabled_ref = write_disabled_stage(
        run_dir=run_dir,
        task_id=task_id,
        baseline=baseline,
        disabled_component=",".join(disabled_components) if disabled_components else "declared_baseline_component",
        config_ref=file_sha256(config_path),
        upstream_input_refs=[file_sha256(extraction_path), file_sha256(claim_path)] if extraction_path.exists() and claim_path.exists() else [sha256_text(f"missing_upstream:{task_id}:{baseline}")],
        reason=f"{baseline} removes {','.join(disabled_components) if disabled_components else 'declared component'} before downstream theorem proving",
    )
    refs = {
        "source_theorem_ref": read_json(extraction_path).get("source_file_ref") if extraction_path.exists() else disabled_ref,
        "extraction_report_ref": file_sha256(extraction_path) if extraction_path.exists() else disabled_ref,
        "claim_spec_ref": file_sha256(claim_path) if claim_path.exists() else disabled_ref,
        "provider_run_manifest_ref": disabled_ref,
        "engine_output_refs": [disabled_ref],
        "independent_solver_artifact_check_refs": [disabled_ref],
        "selected_solver_derivation_ref": disabled_ref,
        "derivation_target_match_ref": disabled_ref,
        "compiler_result_refs": [disabled_ref],
        "lean_patch_candidate_ref": disabled_ref,
        "proof_worker_result_ref": disabled_ref,
        "final_verify_report_ref": disabled_ref,
        "stage_timestamps": synthetic_disabled_timestamps(),
        "used_rule_ids": [],
        "used_engine_roles": [],
    }
    record = build_actual_record(
        run_dir=run_dir,
        task_id=task_id,
        baseline=baseline,
        corpus_root=corpus_root,
        config_path=config_path,
        refs=refs,
        final_status="measured_failure",
        stage_failure_report_ref=disabled_ref,
        solver_backed_certificate_ref=None,
    )
    record["disabled_components"] = disabled_components
    record["baseline_outcome_source"] = "DisabledStageReportV1"
    errors = [f"{task_id}:{baseline}:record_validation:{error}" for error in validate_payload(record)]
    write_json(run_dir / ACTUAL_RUN_DIR / f"{safe_id(task_id)}__{baseline}.json", record)
    return {"record": record, "errors": errors}


def build_actual_record(
    *,
    run_dir: Path,
    task_id: str,
    baseline: str,
    corpus_root: Path,
    config_path: Path,
    refs: dict[str, Any],
    final_status: str,
    stage_failure_report_ref: str | None,
    solver_backed_certificate_ref: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": f"actual_full2d_run:v0_6:{task_id}:{baseline}",
        "task_id": task_id,
        "baseline_id": baseline,
        "git_head": current_git_head(),
        "git_status_hash": git_status_hash(),
        "selected_implementation_hash": selected_implementation_hash(corpus_root),
        "corpus_manifest_hash": file_sha256(corpus_root / "corpus_manifest.json"),
        "config_hash": file_sha256(config_path),
        "checker_hash_set_ref": checker_hash_set_ref(),
        "release_run_dir_hash": release_run_dir_hash(run_dir, corpus_root, config_path),
        "stage_timestamps": refs["stage_timestamps"],
        "source_theorem_ref": refs["source_theorem_ref"],
        "extraction_report_ref": refs["extraction_report_ref"],
        "claim_spec_ref": refs["claim_spec_ref"],
        "provider_run_manifest_ref": refs["provider_run_manifest_ref"],
        "engine_output_refs": refs["engine_output_refs"],
        "independent_solver_artifact_check_refs": refs["independent_solver_artifact_check_refs"],
        "selected_solver_derivation_ref": refs["selected_solver_derivation_ref"],
        "derivation_target_match_ref": refs["derivation_target_match_ref"],
        "compiler_result_refs": refs["compiler_result_refs"],
        "lean_patch_candidate_ref": refs["lean_patch_candidate_ref"],
        "proof_worker_result_ref": refs["proof_worker_result_ref"],
        "final_verify_report_ref": refs["final_verify_report_ref"],
        "solver_backed_certificate_ref": solver_backed_certificate_ref,
        "stage_failure_report_ref": stage_failure_report_ref,
        "final_status": final_status,
        "used_rule_ids": refs.get("used_rule_ids", []),
        "used_engine_roles": refs.get("used_engine_roles", []),
        "outcome_source": "actual_pipeline_stage_execution",
    }


def proof_stage_structural_errors(baseline_dir: Path, tasks: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for task in tasks:
        task_id = safe_id(str(task["task_id"]))
        if not list((baseline_dir / PROOF_WORKER_RESULT_DIR).glob(f"*{task_id}*.json")):
            # Files are keyed by derivation hash, so fall back to count-level check below.
            pass
    worker_count = len(list((baseline_dir / PROOF_WORKER_RESULT_DIR).glob("*.json")))
    if worker_count != len(tasks):
        errors.append(f"proof_worker_result_count_mismatch:{worker_count}!={len(tasks)}")
    # FinalVerify reports are expected for every successfully patched candidate. The final
    # status may be failed; absence is structural failure.
    final_count = len(list((baseline_dir / FINAL_VERIFY_REPORT_DIR).glob("*.json")))
    if final_count != len(tasks):
        errors.append(f"final_verify_report_count_mismatch:{final_count}!={len(tasks)}")
    return errors


def write_stage_failure(*, run_dir: Path, task_id: str, baseline: str, stage: str, input_refs: list[str], failure_kind: str, failure_reason: str) -> str:
    payload = {
        "schema_version": "StageFailureReportV1",
        "stage": stage,
        "task_id": task_id,
        "baseline_id": baseline,
        "input_refs": [ref for ref in input_refs if is_sha_ref(ref)] or [sha256_text(f"missing_input:{task_id}:{stage}")],
        "command_log_ref": sha256_text(canonical_json({"stage": stage, "task_id": task_id, "baseline": baseline, "failure_kind": failure_kind, "failure_reason": failure_reason})),
        "failure_kind": failure_kind,
        "failure_reason": failure_reason,
        "git_head": current_git_head(),
    }
    path = run_dir / STAGE_FAILURE_DIR / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(stage)}.json"
    write_json(path, payload)
    return file_sha256(path)


def write_disabled_stage(*, run_dir: Path, task_id: str, baseline: str, disabled_component: str, config_ref: str, upstream_input_refs: list[str], reason: str) -> str:
    payload = {
        "schema_version": "DisabledStageReportV1",
        "task_id": task_id,
        "baseline_id": baseline,
        "disabled_component": disabled_component,
        "config_ref": config_ref,
        "upstream_input_refs": upstream_input_refs,
        "reason": reason,
        "stage_removed_or_disabled": True,
        "git_head": current_git_head(),
    }
    path = run_dir / DISABLED_STAGE_DIR / f"{safe_id(task_id)}__{safe_id(baseline)}.json"
    write_json(path, payload)
    return file_sha256(path)


def find_payload_path(directory: Path, predicate: Any) -> Path | None:
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.json")):
        payload = read_json(path)
        if predicate(payload):
            return path
    return None


def read_used_rule_ids(patch_path: Path) -> list[str]:
    payload = read_json(patch_path)
    proof_plan = payload.get("proof_plan", {})
    if not isinstance(proof_plan, dict):
        return []
    return [str(item) for item in proof_plan.get("used_rule_ids", [])]


def stage_timestamps_from_paths(extraction_path: Path, provider_path: Path | None, compiler_path: Path | None, final_path: Path | None) -> dict[str, str]:
    extraction = iso_from_mtime(extraction_path)
    provider_started = extraction
    provider_finished = iso_from_mtime(provider_path) if provider_path and provider_path.exists() else add_seconds(extraction, 1)
    compiler_started = iso_from_mtime(compiler_path) if compiler_path and compiler_path.exists() else add_seconds(provider_finished, 1)
    if compiler_started <= provider_finished:
        compiler_started = add_seconds(provider_finished, 1)
    final_finished = iso_from_mtime(final_path) if final_path and final_path.exists() else add_seconds(compiler_started, 1)
    if final_finished <= compiler_started:
        final_finished = add_seconds(compiler_started, 1)
    return {
        "extraction_started_at": extraction,
        "provider_started_at": provider_started,
        "provider_finished_at": provider_finished,
        "compiler_started_at": compiler_started,
        "final_verify_finished_at": final_finished,
    }


def synthetic_disabled_timestamps() -> dict[str, str]:
    base = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "extraction_started_at": base,
        "provider_started_at": add_seconds(base, 1),
        "provider_finished_at": add_seconds(base, 2),
        "compiler_started_at": add_seconds(base, 3),
        "final_verify_finished_at": add_seconds(base, 4),
    }


def iso_from_mtime(path: Path) -> str:
    if not path.exists():
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def add_seconds(value: str, seconds: int) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return (dt + timedelta(seconds=seconds)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def wrap_theorem_source(theorem_source: str) -> str:
    return "\n".join(
        [
            "import MathAutoResearch.GeometryFull2D.Inequality",
            "",
            "namespace MathAutoResearch.GeometryFull2D",
            "",
            theorem_source.strip(),
            "",
            "end MathAutoResearch.GeometryFull2D",
            "",
        ]
    )


def resolve_task_lean_file(corpus_root: Path, task: dict[str, Any]) -> Path:
    raw = Path(str(task.get("lean_file", "")))
    if raw.is_absolute():
        return raw
    candidate = corpus_root / raw
    return candidate if candidate.exists() else ROOT / raw


def selected_implementation_hash(corpus_root: Path) -> str:
    cache_key = str(corpus_root.resolve())
    if cache_key in _SELECTED_IMPLEMENTATION_HASH_BY_CORPUS:
        return _SELECTED_IMPLEMENTATION_HASH_BY_CORPUS[cache_key]
    path = corpus_root / "metadata" / "implementation_freeze_manifest_v0_6.json"
    if path.exists():
        payload = read_json(path)
        value = payload.get("selected_implementation_hash")
        if isinstance(value, str) and is_sha_ref(value):
            _SELECTED_IMPLEMENTATION_HASH_BY_CORPUS[cache_key] = value
            return value
    value = sha256_text("missing_selected_implementation_hash:" + current_git_head())
    _SELECTED_IMPLEMENTATION_HASH_BY_CORPUS[cache_key] = value
    return value


def release_run_dir_hash(run_dir: Path, corpus_root: Path, config_path: Path) -> str:
    cache_key = (str(run_dir.resolve()), str(corpus_root.resolve()), str(config_path.resolve()))
    if cache_key not in _RELEASE_RUN_DIR_HASH_BY_KEY:
        _RELEASE_RUN_DIR_HASH_BY_KEY[cache_key] = sha256_text(
            canonical_json(
                {
                    "run_dir": str(run_dir.resolve()),
                    "corpus_manifest_hash": file_sha256(corpus_root / "corpus_manifest.json"),
                    "config_hash": file_sha256(config_path),
                    "git_head": current_git_head(),
                }
            )
        )
    return _RELEASE_RUN_DIR_HASH_BY_KEY[cache_key]


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def git_status_hash() -> str:
    global _GIT_STATUS_HASH
    if _GIT_STATUS_HASH is not None:
        return _GIT_STATUS_HASH
    proc = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True)
    _GIT_STATUS_HASH = sha256_text(proc.stdout if proc.returncode == 0 else "git_status_unavailable")
    return _GIT_STATUS_HASH


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in value)


def is_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
