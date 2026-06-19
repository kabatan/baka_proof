#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.compiler_v0_5 import run_compiler_cli
from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES
from math_auto_research.lean_integration.goal_anchor import extract_theorem_statement, hash_text
from plugins.geometry_full2d.proof_worker_v0_5 import (
    apply_lean_patch_candidate_full2d_v0_5,
    final_verify_gate_full2d_v0_5,
    forbidden_declarations,
    imports_are_admitted,
    outside_target_region,
    toy_target_tokens,
    validate_proof_use_provenance,
)
from plugins.geometry_full2d.provider_cli import run_provider_cli
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d
from plugins.geometry_full2d.solver_derivation import select_solver_derivation
from scripts.geometry_full2d_v0_5_independent_checkers import run_independent_solver_checkers
from scripts.extract_geometry_full2d_theorem import (
    _canonicalize_lean_structured_output,
    _direct_lean_env,
    _ensure_extraction_olean,
    _ensure_local_lean_artifacts,
    _extract_theorem_source,
    _file_sha256,
    _lean,
    _lean_extraction_cache_key,
    _lean_source_with_extraction_import,
    _parse_all_lean_extraction_json,
    _qualified_theorem_name,
    _sha256_text,
    _theorem_header_for_cache,
)
from scripts.geometry_full2d_v0_5_extraction import EXTRACTION_REPORT_DIR, INDEX_NAME, manifest_hash, normalize_extraction_report
from scripts.geometry_full2d_v0_5_schemas import validate_payload


REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7"]
MUTATION_PENDING_REF = "sha256:" + "0" * 64
RULE_FAMILIES = [
    "incidence_collinearity",
    "line_parallelism",
    "line_perpendicularity",
    "circle_cyclicity",
    "circle_tangent",
    "radical_axis",
    "midpoint_segment",
    "angle_chase",
    "directed_angle_mod_pi",
    "metric_equal_length",
    "ratio_similarity",
    "area_relation",
    "triangle_centers",
    "triangle_congruence",
    "triangle_similarity",
    "construction_line",
    "construction_circle",
    "construction_intersection",
    "construction_center",
    "transformation_reflection",
    "transformation_rotation",
    "transformation_homothety",
    "transformation_inversion",
    "spiral_similarity",
    "order_between",
    "order_same_side",
    "case_split_orientation",
    "algebraic_coordinate",
    "inequality_length",
    "inequality_power",
]
EXTRACTION_BATCH_SIZE = 100
BATCH_FINAL_VERIFY_CHUNK_SIZE = 200


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--execute-all-baselines", action="store_true")
    parser.add_argument("--fresh-run", action="store_true")
    args = parser.parse_args()
    report = run_matrix(
        config_path=Path(args.config),
        run_dir=Path(args.run_dir),
        execute_all_baselines=args.execute_all_baselines,
        fresh_run=args.fresh_run,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_matrix(
    *,
    config_path: Path,
    run_dir: Path,
    execute_all_baselines: bool,
    fresh_run: bool,
) -> dict[str, Any]:
    started = time.time()
    config_path = resolve(config_path)
    run_dir = resolve(run_dir)
    config = read_json(config_path)
    corpus_root = resolve(Path(str(config.get("benchmark_corpus_root", "benchmarks/geometry_full2d_v0_5"))))
    if fresh_run and run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    required_baselines = [str(item) for item in config.get("required_baselines", REQUIRED_BASELINES)]
    if required_baselines != REQUIRED_BASELINES:
        errors.append("required_baselines_not_v0_5_set")
    if not execute_all_baselines:
        errors.append("execute_all_baselines_flag_required")
    manifest = read_json(corpus_root / "corpus_manifest.json")
    tasks = [task for task in manifest.get("tasks", []) if isinstance(task, dict) and task.get("counted_positive") is True]
    if len(tasks) < 1200:
        errors.append("counted_task_count_below_release_floor")
    extraction = build_batch_extraction_reports(corpus_root, run_dir, tasks)
    errors.extend(f"extraction:{error}" for error in extraction["errors"])
    registry_ref, registry_path = write_artifact(
        run_dir,
        Path("rule_registry") / "rule_registry_full2d.json",
        build_rule_registry_full2d().to_dict(),
        id_field="registry_content_id",
    )
    config_ref = sha256_file(config_path)
    corpus_ref = sha256_file(corpus_root / "corpus_manifest.json")
    selected_impl = selected_implementation_hash()
    git_head = current_git_head()
    run_dir_hash = sha256_text(str(run_dir.resolve()) + ":" + corpus_ref + ":" + config_ref)
    baseline_disabled = config.get("baseline_disabled_components", {})
    record_counts: dict[str, dict[str, int]] = {baseline: {"records": 0, "final_theorem": 0, "measured_failure": 0} for baseline in required_baselines}
    validation_errors: list[str] = []
    upstreams_by_baseline: dict[str, dict[str, dict[str, Any]]] = {baseline: {} for baseline in required_baselines}
    for index, task in enumerate(tasks):
        task_id = str(task["task_id"])
        extraction_ref = extraction["report_refs"].get(task_id)
        extraction_report = extraction["reports"].get(task_id)
        if not extraction_ref or not isinstance(extraction_report, dict):
            errors.append(f"{task_id}:missing_extraction_for_upstream_pipeline")
            continue
        upstream = build_upstream_artifacts(
            run_dir=run_dir,
            task=task,
            task_index=index,
            baseline="B2",
            disabled_components=[],
            extraction_ref=extraction_ref,
            extraction_report=extraction_report,
            registry_ref=registry_ref,
            registry_path=registry_path,
        )
        validation_errors.extend(upstream["validation_errors"])
        errors.extend(f"{task_id}:B2:upstream:{error}" for error in upstream["errors"])
        upstreams_by_baseline["B2"][task_id] = upstream
        for baseline in ["B1", "B5", "B6", "B7"]:
            disabled = list(baseline_disabled.get(baseline, []))
            baseline_upstream = build_upstream_artifacts(
                run_dir=run_dir,
                task=task,
                task_index=index,
                baseline=baseline,
                disabled_components=disabled,
                extraction_ref=extraction_ref,
                extraction_report=extraction_report,
                registry_ref=registry_ref,
                registry_path=registry_path,
            )
            validation_errors.extend(baseline_upstream["validation_errors"])
            upstreams_by_baseline[baseline][task_id] = baseline_upstream
    final_records_dir = run_dir / "actual_task_pipeline_runs"
    final_records_dir.mkdir(parents=True, exist_ok=True)
    prepared_runs: list[dict[str, Any]] = []
    for index, task in enumerate(tasks):
        task_id = str(task["task_id"])
        extraction_ref = extraction["report_refs"].get(str(task["task_id"]))
        if not extraction_ref:
            errors.append(f"{task['task_id']}:missing_extraction_ref")
            extraction_ref = sha256_text("missing_extraction:" + str(task["task_id"]))
        for baseline in ["B2", "B1", "B5", "B6", "B7"]:
            disabled = list(baseline_disabled.get(baseline, []))
            upstream = upstreams_by_baseline[baseline].get(task_id)
            if upstream is None:
                errors.append(f"{task_id}:{baseline}:missing_upstream_bundle")
                upstream = missing_b2_upstream_bundle(task_id, extraction_ref)
            prepared = prepare_proof_worker_run(
                run_dir=run_dir,
                corpus_root=corpus_root,
                task=task,
                baseline=baseline,
                upstream=upstream,
                git_head=git_head,
                selected_impl=selected_impl,
            )
            validation_errors.extend(prepared.get("validation_errors", []))
            if baseline == "B2" or not disabled:
                errors.extend(f"{task_id}:{baseline}:proof_worker:{error}" for error in prepared.get("errors", []))
            prepared_runs.append({"task": task, "baseline": baseline, "upstream": upstream, "disabled_components": disabled, "prepared": prepared})
    finalized = finalize_batch_final_verify_runs(
        run_dir=run_dir,
        prepared_runs=prepared_runs,
        git_head=git_head,
        selected_impl=selected_impl,
    )
    validation_errors.extend(finalized["validation_errors"])
    errors.extend(finalized["errors"])
    for item in prepared_runs:
        task = item["task"]
        baseline = str(item["baseline"])
        proof_run = finalized["proof_runs"].get((str(task["task_id"]), baseline))
        if proof_run is None:
            failure_ref = write_stage_failure(
                run_dir=run_dir,
                task_id=str(task["task_id"]),
                baseline=baseline,
                stage="final_verify",
                input_refs=[str(item["upstream"].get("claim_ref", "")), str(item["upstream"].get("patch_ref", ""))],
                command_log_payload={
                    "schema_version": "CommandLogV05",
                    "stage": "final_verify",
                    "stage_sequence": ["proof_worker", "final_verify"],
                    "actual_python_function_executed": False,
                    "actual_subprocess_executed": False,
                    "returncode": 1,
                    "errors": ["batch_final_verify_result_missing"],
                },
                failure_kind="real_execution_failure",
                failure_reason="batch FinalVerify did not produce a task result",
                git_head=git_head,
                selected_impl=selected_impl,
                disabled_components=list(item.get("disabled_components", [])),
            )
            proof_run = proof_failure_result(str(task["task_id"]), baseline, failure_ref, "StageFailureReportV1", errors=["batch_final_verify_result_missing"])
        bundle = materialize_record(
            run_dir=run_dir,
            task=task,
            baseline=baseline,
            corpus_ref=corpus_ref,
            config_ref=config_ref,
            selected_impl=selected_impl,
            git_head=git_head,
            run_dir_hash=run_dir_hash,
            upstream=item["upstream"],
            proof_run=proof_run,
            disabled_components=list(item.get("disabled_components", [])) if baseline != "B2" else None,
        )
        validation_errors.extend(bundle["validation_errors"])
        record = bundle["record"]
        write_json(final_records_dir / f"{safe_id(str(task['task_id']))}__{baseline}.json", record)
        record_counts[baseline]["records"] += 1
        record_counts[baseline][str(record["final_status"])] += 1
    errors.extend(f"record_validation:{error}" for error in sorted(set(validation_errors))[:50])
    actual_summary = {
        "status": "passed" if not errors else "failed",
        "counted_task_count": len(tasks),
        "required_baselines": required_baselines,
        "required_record_count": len(tasks) * len(required_baselines),
        "record_count": sum(item["records"] for item in record_counts.values()),
        "by_baseline": record_counts,
        "derived_from_actual_task_pipeline_runs": True,
        "final_status_source_policy": "FinalVerifyReportFull2D_or_content_addressed_stage_failure",
    }
    b8 = config.get("conditional_b8", {})
    b8_report = {
        "resolution": b8.get("resolution"),
        "reason": b8.get("reason"),
        "conditional_b8_resolution_valid": b8.get("resolution") == "B8_NOT_APPLICABLE" and bool(b8.get("reason")),
        "b2_metrics_independent_of_b8": True,
    }
    summary = {
        "schema_version": "Full2DMatrixRunV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "config": config_path.relative_to(ROOT).as_posix(),
        "run_dir": run_dir.relative_to(ROOT).as_posix() if is_relative_to(run_dir, ROOT) else str(run_dir),
        "execute_all_baselines": execute_all_baselines,
        "fresh_run": fresh_run,
        "duration_seconds": round(time.time() - started, 3),
        "actual_pipeline_run_summary": actual_summary,
        "conditional_b8": b8_report,
        "extraction_summary": extraction["summary"],
        "task_level_final_verify_summary": {
            "mode": "per_task_proof_worker_batch_final_verify_gate",
            "proof_worker_result_count": len(list((run_dir / "proof_worker_results").glob("*.json"))) if (run_dir / "proof_worker_results").exists() else 0,
            "final_verify_report_count": len(list((run_dir / "final_verify_reports").glob("*.json"))) if (run_dir / "final_verify_reports").exists() else 0,
            "batch_command_count": finalized["batch_command_count"],
            "batch_chunk_size": BATCH_FINAL_VERIFY_CHUNK_SIZE,
        },
        "record_count": actual_summary["record_count"],
    }
    write_json(run_dir / "matrix_summary_v0_5.json", summary)
    return summary


def build_batch_extraction_reports(corpus_root: Path, run_dir: Path, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    report_refs: dict[str, str] = {}
    reports: dict[str, dict[str, Any]] = {}
    groups: dict[Path, list[dict[str, Any]]] = {}
    for task in tasks:
        lean_file = corpus_root / str(task.get("lean_file", ""))
        groups.setdefault(lean_file, []).append(task)
    output_dir = run_dir / EXTRACTION_REPORT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    for lean_file, group in groups.items():
        if not lean_file.exists():
            errors.append(f"lean_file_missing:{lean_file}")
        else:
            for group_chunk in chunks(group, EXTRACTION_BATCH_SIZE):
                batch = run_lean_extractor_batch(lean_file, [str(task["theorem_name"]) for task in group_chunk], run_dir=run_dir)
                errors.extend(batch["errors"])
                extracted = batch["extracted"]
                for task in group_chunk:
                    theorem_name = str(task["theorem_name"])
                    raw_structured = extracted.get(theorem_name)
                    if raw_structured is None:
                        errors.append(f"{task['task_id']}:missing_lean_extractor_output")
                    else:
                        theorem_source = _extract_theorem_source(lean_file.read_text(encoding="utf-8"), theorem_name)
                        source_statement_hash = _sha256_text(theorem_source)
                        canonical = _canonicalize_lean_structured_output(raw_structured, lean_file, theorem_name, source_statement_hash)
                        raw = {
                            "theorem_name": theorem_name,
                            "source_file_ref": _file_sha256(lean_file),
                            "source_statement_hash": source_statement_hash,
                            "elaborated_expr_hash": sha256_text(canonical_json(raw_structured)),
                            "target_classification": canonical["target_classification"],
                            "canonical_statement": canonical["canonical_statement"],
                            "source_theorem_preproved": False,
                            "extraction_method": "lean_elaborator_structured_theorem",
                            "semantic_extraction_authority": "lean_elaborator",
                            "python_semantic_extraction_used": False,
                            "regex_used_for_semantics": False,
                            "regex_used_for_source_location": True,
                            "lean_command": batch["command"],
                            "lean_semantic_extractor_ref": sha256_text(canonical_json(raw_structured)),
                            "lean_semantic_extractor_cache_key": _lean_extraction_cache_key(
                                theorem_name,
                                _sha256_text(_theorem_header_for_cache(theorem_source)),
                            ),
                            "lean_semantic_extractor_cache_status": "batch_fresh",
                            "lean_stdout_hash": sha256_text(batch["stdout"]),
                            "lean_stderr_hash": sha256_text(batch["stderr"]),
                        }
                        report = normalize_extraction_report(raw, task, lean_file)
                        report_ref = str(report["content_sha256"])
                        task_id = str(task["task_id"])
                        report_refs[task_id] = report_ref
                        reports[task_id] = report
                        write_json(output_dir / f"{safe_id(str(task['task_id']))}.json", report)
    index = {
        "schema_version": "GeometryFull2DExtractionCorpusIndexV05",
        "corpus_manifest_hash": manifest_hash(corpus_root),
        "run_dir": str(run_dir),
        "required_task_count": len(tasks),
        "report_count": len(report_refs),
        "report_paths": sorted(path.relative_to(run_dir).as_posix() for path in output_dir.glob("*.json")),
    }
    write_json(run_dir / INDEX_NAME, index)
    if len(report_refs) != len(tasks):
        errors.append(f"extraction_report_count_mismatch:{len(report_refs)}!={len(tasks)}")
    return {
        "errors": sorted(set(errors)),
        "report_refs": report_refs,
        "reports": reports,
        "summary": {
            "status": "passed" if not errors else "failed",
            "required_task_count": len(tasks),
            "report_count": len(report_refs),
            "batch_lean_file_count": len(groups),
            "batch_command_log_refs": [
                str(ref) for ref in sorted(
                    batch_ref
                    for path in (run_dir / "command_logs" / "lean_extraction").glob("*.json")
                    for batch_ref in [read_json(path).get("command_log_id")]
                    if batch_ref
                )
            ] if (run_dir / "command_logs" / "lean_extraction").exists() else [],
        },
    }


def run_lean_extractor_batch(lean_file: Path, theorem_names: list[str], *, run_dir: Path | None = None) -> dict[str, Any]:
    _ensure_local_lean_artifacts()
    _ensure_extraction_olean()
    source = lean_file.read_text(encoding="utf-8")
    directives = "\n".join(f"#full2d_extract {_qualified_theorem_name(name)}" for name in theorem_names)
    extractor_source = (
        _lean_source_with_extraction_import(source).rstrip()
        + "\n\nopen MathAutoResearch.GeometryFull2D\n"
        + "open MathAutoResearch.GeometryFull2D.Extraction\n"
        + directives
        + "\n"
    )
    command = [_lean(), "--stdin", "--json"]
    command_log: dict[str, Any]
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            input=extractor_source,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=_direct_lean_env(),
            timeout=300,
        )
        command_log = {
            "schema_version": "CommandLogV05",
            "command": command,
            "lean_file": str(lean_file),
            "theorem_count": len(theorem_names),
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        command_log = {
            "schema_version": "CommandLogV05",
            "command": command,
            "lean_file": str(lean_file),
            "theorem_count": len(theorem_names),
            "returncode": 124,
            "stdout_tail": str(exc.stdout or "")[-4000:],
            "stderr_tail": str(exc.stderr or "lean batch extraction timed out")[-4000:],
        }
        command_log_ref = write_command_log(run_dir, lean_file, command_log) if run_dir is not None else None
        return {
            "command": command,
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "lean batch extraction timed out",
            "errors": ["lean_batch_extraction_timeout"],
            "extracted": {},
            "command_log_ref": command_log_ref,
        }
    parsed = _parse_all_lean_extraction_json(completed.stdout)
    extracted = {str(item.get("theorem_name")): item for item in parsed if isinstance(item, dict)}
    errors: list[str] = []
    if completed.returncode != 0:
        errors.append("lean_batch_extraction_failed")
    missing = sorted(set(theorem_names) - set(extracted))
    if missing:
        errors.append("lean_batch_extraction_missing:" + ",".join(missing[:20]))
    command_log_ref = write_command_log(run_dir, lean_file, command_log) if run_dir is not None else None
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "errors": errors,
        "extracted": extracted,
        "command_log_ref": command_log_ref,
    }


def write_command_log(run_dir: Path | None, lean_file: Path, payload_without_id: dict[str, Any]) -> str | None:
    if run_dir is None:
        return None
    rel = safe_id(lean_file.name + "__" + sha256_file(lean_file)[7:19] + "__" + sha256_text(canonical_json(payload_without_id))[7:15])
    ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "lean_extraction" / f"{rel}.json",
        payload_without_id,
        id_field="command_log_id",
    )
    return ref


def chunks(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def build_upstream_artifacts(
    *,
    run_dir: Path,
    task: dict[str, Any],
    task_index: int,
    baseline: str,
    disabled_components: list[str],
    extraction_ref: str,
    extraction_report: dict[str, Any],
    registry_ref: str,
    registry_path: Path,
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    errors: list[str] = []
    source_ref, _ = write_artifact(
        run_dir,
        Path("source_theorems") / f"{safe_id(task_id)}.json",
        {
            "schema_version": "SourceTheoremV05",
            "task_id": task_id,
            "formal_statement": task["formal_statement"],
            "lean_file": task["lean_file"],
            "theorem_name": theorem_name,
        },
        id_field="source_theorem_id",
    )
    claim_spec = claim_spec_for_task(task_id, theorem_name, extraction_ref, extraction_report)
    _claim_body_ref, claim_path = write_artifact(run_dir, Path("claim_specs") / f"{safe_id(task_id)}.json", claim_spec, id_field="claim_id")
    claim_ref = sha256_file(claim_path)
    provider = run_provider_and_checkers(run_dir, task_id, claim_path, claim_ref, baseline=baseline, disabled_components=disabled_components)
    errors.extend(provider["fatal_errors"])
    engine_refs = provider["engine_refs"]
    checker_refs = provider["checker_refs"]
    provider_ref, _ = write_artifact(
        run_dir,
        Path("provider_stage") / "provider_manifests" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "ProviderRunManifestFull2D",
            "provider_stage_run_id": f"provider:v0_5:{task_id}:{baseline}",
            "claim_spec_ref": claim_ref,
            "engine_output_refs": engine_refs,
            "engine_roles": list(ENGINE_ROLES),
            "baseline_id": baseline,
            "disabled_components": disabled_components,
            "disabled_engine_roles": provider["disabled_engine_roles"],
            "provider_cli_summary_ref": provider["provider_summary_ref"],
            "independent_checker_summary_ref": provider["checker_summary_ref"],
            "provider_process_boundary": "plugins.geometry_full2d.provider_cli.run_provider_cli",
            "proof_use_status": "not_allowed",
        },
        id_field="manifest_id",
    )
    derivation, derivation_errors = select_solver_derivation(
        claim_spec=claim_spec,
        engine_refs_by_role=provider["engine_refs_by_role"],
        checker_refs_by_role=provider["checker_refs_by_role"],
        normalized_artifacts_by_role=provider["normalized_artifacts_by_role"],
        normalized_artifact_refs_by_role=provider["normalized_artifact_refs_by_role"],
    )
    errors.extend(f"selected_derivation:{error}" for error in derivation_errors)
    if derivation is None:
        derivation = {
            "schema_version": "SelectedSolverDerivationV2",
            "selected_engine_output_refs": [],
            "selected_facts": [],
            "selected_constructions": [],
            "selected_certificates": [],
            "derivation_steps": [],
            "used_engine_roles": [],
            "selection_errors": derivation_errors,
        }
    rule_ids = [
        str(step.get("rule_id"))
        for step in derivation.get("derivation_steps", [])
        if isinstance(step, dict) and str(step.get("rule_id", "")).startswith("full2d_rule:")
    ]
    derivation_ref, derivation_path = write_artifact(run_dir, Path("selected_solver_derivations") / f"{safe_id(task_id)}__{safe_id(baseline)}.json", derivation, id_field="derivation_id")
    compiler_stage = run_compiler_cli(
        claim_spec_json=claim_path,
        selected_derivation_json=derivation_path,
        rule_registry_json=registry_path,
        output_dir=run_dir / "compiler_task_runs" / safe_id(baseline) / safe_id(task_id),
        claim_spec_ref=claim_ref,
        selected_derivation_ref=derivation_ref,
        rule_registry_ref=registry_ref,
        side_condition_checker_refs=tuple(checker_refs[:2]),
    )
    errors.extend(f"compiler_cli:{error}" for error in compiler_stage.get("errors", []))
    compiler_result_path = run_dir / "compiler_task_runs" / safe_id(baseline) / safe_id(task_id) / "compiler_stage" / "compiler_result.json"
    compiler_payload = read_json(compiler_result_path) if compiler_stage.get("status") == "passed" and compiler_result_path.exists() else {}
    patch_text = str(compiler_payload.get("proof_text", ""))
    if not patch_text:
        errors.append("compiler_no_patch_text_from_selected_derivation")
    compiler_ref, _ = write_artifact(
        run_dir,
        Path("compiler_results") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        strip_identity(compiler_payload)
        if compiler_payload
        else {
            "schema_version": "StageFailureReportV1",
            "stage": "compiler",
            "input_refs": [claim_ref, derivation_ref, registry_ref],
            "command_log_ref": sha256_text(canonical_json(compiler_stage)),
            "failure_kind": "unsupported_after_disabled_component" if disabled_components else "validation_rejected",
            "failure_reason": ";".join(map(str, compiler_stage.get("errors", []))) or "compiler_cli_failed",
            "baseline_id": baseline,
            "disabled_components": disabled_components,
        },
        id_field="result_id",
    )
    patch = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": compiler_ref,
        "theorem_name": theorem_name,
        "proof_region_only": True,
        "allowed_edit_region": {
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "patch_text": indent_proof_region(patch_text),
        "solver_dependency_refs": [derivation_ref, *checker_refs[:2]],
    }
    patch_ref, patch_path = write_artifact(run_dir, Path("lean_patch_candidates") / f"{safe_id(task_id)}__{safe_id(baseline)}.json", patch, id_field="patch_id")
    return {
        "errors": sorted(set(errors)),
        "validation_errors": [],
        "baseline": baseline,
        "disabled_components": disabled_components,
        "source_ref": source_ref,
        "extraction_ref": extraction_ref,
        "claim_ref": claim_ref,
        "claim_path": str(claim_path),
        "provider_ref": provider_ref,
        "engine_refs": engine_refs,
        "checker_refs": checker_refs,
        "derivation_ref": derivation_ref,
        "compiler_ref": compiler_ref,
        "patch_ref": patch_ref,
        "patch_path": str(patch_path),
        "patch_text": indent_proof_region(patch_text),
        "rule_ids": rule_ids,
        "has_non_target_intermediate": any(
            isinstance(step, dict) and step.get("non_target_intermediate") is True
            for step in derivation.get("derivation_steps", [])
        ),
        "has_construction_case_certificate": bool(derivation.get("selected_constructions") or derivation.get("selected_certificates")),
        "used_engine_roles": sorted(str(role) for role in derivation.get("used_engine_roles", [])),
        "direct_or_wrapped_facade_success": bool(derivation.get("direct_or_wrapped_facade_success")),
        "provider_nonfatal_errors": provider["nonfatal_errors"],
    }


def prepare_proof_worker_run(
    *,
    run_dir: Path,
    corpus_root: Path,
    task: dict[str, Any],
    baseline: str,
    upstream: dict[str, Any],
    git_head: str,
    selected_impl: str,
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    disabled_components = list(upstream.get("disabled_components", []))
    input_refs = [
        str(upstream.get("claim_ref", "")),
        str(upstream.get("derivation_ref", "")),
        str(upstream.get("compiler_ref", "")),
        str(upstream.get("patch_ref", "")),
    ]
    if not str(upstream.get("patch_text", "")).strip():
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="compiler",
            input_refs=input_refs,
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "compiler",
                "stage_sequence": ["claimspec", "provider", "independent_checker", "selected_derivation", "compiler"],
                "actual_python_function_executed": True,
                "returncode": 1,
                "errors": upstream.get("errors", []),
            },
            failure_kind="unsupported_after_disabled_component" if disabled_components else "validation_rejected",
            failure_reason="compiler did not produce a Lean patch from checked selected solver derivation",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        return {"status": "failed", "proof_run": proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=["compiler_no_patch_text_from_selected_derivation"]), "errors": ["compiler_no_patch_text_from_selected_derivation"], "validation_errors": []}

    patch_path = Path(str(upstream.get("patch_path", "")))
    if not patch_path.exists():
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="proof_worker",
            input_refs=input_refs,
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "proof_worker",
                "stage_sequence": ["proof_worker"],
                "actual_python_function_executed": False,
                "returncode": 1,
                "errors": ["patch_artifact_path_missing"],
            },
            failure_kind="validation_rejected",
            failure_reason="LeanPatchCandidateFull2D artifact was missing before ProofWorker execution",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        return {"status": "failed", "proof_run": proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=["patch_artifact_path_missing"]), "errors": ["patch_artifact_path_missing"], "validation_errors": []}

    source_path = write_task_source_lean(run_dir, corpus_root, task, baseline)
    proof_root = run_dir / "proof_worker_task_runs" / safe_id(baseline) / safe_id(task_id)
    patch_payload = read_json(patch_path)
    worker = apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch_payload,
        output_dir=proof_root,
        run_id=f"actual_full2d_run:v0_5:{task_id}:{baseline}",
        task_id=task_id,
    )
    worker_ref, _ = write_artifact(
        run_dir,
        Path("proof_worker_results") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        strip_identity(worker),
        id_field="worker_result_id",
    )
    validation_errors = [f"proof_worker:{error}" for error in validate_payload(read_json(run_dir / "proof_worker_results" / f"{safe_id(task_id)}__{safe_id(baseline)}.json"), current_head=git_head)]
    if worker.get("status") != "patch_applied":
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="proof_worker",
            input_refs=[*input_refs, worker_ref],
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "proof_worker",
                "stage_sequence": ["proof_worker"],
                "actual_python_function_executed": True,
                "returncode": 1,
                "errors": worker.get("errors", []),
                "worker_result_ref": worker_ref,
            },
            failure_kind="validation_rejected",
            failure_reason="ProofWorker rejected the Lean patch candidate",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        result = proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=[f"proof_worker:{error}" for error in worker.get("errors", [])])
        result["proof_worker_result_ref"] = worker_ref
        result["validation_errors"] = validation_errors
        return {"status": "failed", "proof_run": result, "errors": result["errors"], "validation_errors": validation_errors}
    return {
        "status": "prepared",
        "errors": [],
        "validation_errors": validation_errors,
        "source_path": str(source_path),
        "candidate_path": str(worker.get("generated_candidate_path", "")),
        "worker_ref": worker_ref,
        "worker": worker,
    }


def finalize_batch_final_verify_runs(
    *,
    run_dir: Path,
    prepared_runs: list[dict[str, Any]],
    git_head: str,
    selected_impl: str,
) -> dict[str, Any]:
    proof_runs: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[str] = []
    validation_errors: list[str] = []
    ready = [item for item in prepared_runs if item.get("prepared", {}).get("status") == "prepared"]
    for item in prepared_runs:
        prepared = item.get("prepared", {})
        if prepared.get("status") != "prepared" and isinstance(prepared.get("proof_run"), dict):
            proof_runs[(str(item["task"]["task_id"]), str(item["baseline"]))] = prepared["proof_run"]
    batch_command_count = 0
    for baseline in ["B2", "B1", "B5", "B6", "B7"]:
        baseline_items = [item for item in ready if str(item["baseline"]) == baseline]
        for chunk_index, chunk_items in enumerate(chunks(baseline_items, BATCH_FINAL_VERIFY_CHUNK_SIZE)):
            if not chunk_items:
                continue
            batch = run_batch_lean_verify(run_dir, baseline, chunk_index, chunk_items)
            batch_command_count += 1
            for item in chunk_items:
                task = item["task"]
                task_id = str(task["task_id"])
                prepared = item["prepared"]
                upstream = item["upstream"]
                disabled_components = list(item.get("disabled_components", []))
                result = build_batch_final_verify_result(
                    run_dir=run_dir,
                    task=task,
                    baseline=baseline,
                    upstream=upstream,
                    prepared=prepared,
                    batch=batch,
                    git_head=git_head,
                    selected_impl=selected_impl,
                    disabled_components=disabled_components,
                )
                validation_errors.extend(result.get("validation_errors", []))
                errors.extend(f"{task_id}:{baseline}:batch_final_verify:{error}" for error in result.get("errors", []))
                proof_runs[(task_id, baseline)] = result["proof_run"]
    return {"proof_runs": proof_runs, "errors": errors, "validation_errors": validation_errors, "batch_command_count": batch_command_count}


def run_batch_lean_verify(run_dir: Path, baseline: str, chunk_index: int, items: list[dict[str, Any]]) -> dict[str, Any]:
    batch_dir = run_dir / "batch_final_verify" / safe_id(baseline)
    batch_dir.mkdir(parents=True, exist_ok=True)
    batch_path = batch_dir / f"chunk_{chunk_index:04d}.lean"
    text = build_batch_candidate_text(items)
    batch_path.write_text(text, encoding="utf-8")
    command = ["lake", "env", "lean", str(batch_path)]
    started = time.time()
    try:
        completed = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600, check=False)
        return {
            "batch_path": str(batch_path),
            "batch_ref": sha256_file(batch_path),
            "command": command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
            "duration_seconds": round(time.time() - started, 3),
            "task_count": len(items),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "batch_path": str(batch_path),
            "batch_ref": sha256_file(batch_path),
            "command": command,
            "returncode": 124,
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "batch lake env lean timed out",
            "duration_seconds": round(time.time() - started, 3),
            "task_count": len(items),
        }


def build_batch_candidate_text(items: list[dict[str, Any]]) -> str:
    lines = ["import MathAutoResearch.GeometryFull2D.Inequality", "", "namespace MathAutoResearch.GeometryFull2D", ""]
    for item in items:
        candidate_text = Path(str(item["prepared"]["candidate_path"])).read_text(encoding="utf-8")
        lines.extend(extract_candidate_body(candidate_text))
        lines.append("")
    lines.extend(["end MathAutoResearch.GeometryFull2D", ""])
    return "\n".join(lines)


def extract_candidate_body(candidate_text: str) -> list[str]:
    output: list[str] = []
    for line in candidate_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            continue
        if stripped == "namespace MathAutoResearch.GeometryFull2D":
            continue
        if stripped == "end MathAutoResearch.GeometryFull2D":
            continue
        output.append(line)
    return output


def build_batch_final_verify_result(
    *,
    run_dir: Path,
    task: dict[str, Any],
    baseline: str,
    upstream: dict[str, Any],
    prepared: dict[str, Any],
    batch: dict[str, Any],
    git_head: str,
    selected_impl: str,
    disabled_components: list[str],
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    source_path = Path(str(prepared["source_path"]))
    candidate_path = Path(str(prepared["candidate_path"]))
    source_text = source_path.read_text(encoding="utf-8")
    candidate_text = candidate_path.read_text(encoding="utf-8")
    theorem_statement_unchanged = False
    theorem_statement_hash = ""
    try:
        theorem_statement_hash = hash_text(extract_theorem_statement(source_text, theorem_name))
        theorem_statement_unchanged = theorem_statement_hash == hash_text(extract_theorem_statement(candidate_text, theorem_name))
    except Exception:
        theorem_statement_hash = ""
    no_sorry = re.search(r"\bsorry\b", candidate_text) is None
    forbidden = forbidden_declarations(candidate_text)
    toy_tokens = toy_target_tokens(candidate_text)
    admitted_imports_only, bad_imports = imports_are_admitted(candidate_text, ("MathAutoResearch", "Mathlib", "LeanGeo", "Lean"))
    proof_region_guard_passed = outside_target_region(source_text, theorem_name) == outside_target_region(candidate_text, theorem_name)
    provenance = {
        "claim_spec_ref": upstream["claim_ref"],
        "compiler_result_ref": upstream["compiler_ref"],
        "lean_patch_candidate_ref": upstream["patch_ref"],
        "proof_worker_result_ref": prepared["worker_ref"],
        "proof_region_diff_ref": prepared["worker"].get("proof_region_diff_ref"),
        "generated_candidate_file_ref": prepared["worker"].get("generated_candidate_file_ref"),
    }
    provenance_errors = validate_proof_use_provenance(provenance)
    final_errors: list[str] = []
    if not theorem_statement_unchanged:
        final_errors.append("theorem_statement_changed")
    if not proof_region_guard_passed:
        final_errors.append("candidate_modified_outside_marp_region")
    if not no_sorry:
        final_errors.append("sorry_present")
    if forbidden:
        final_errors.append("forbidden_declarations")
    if toy_tokens:
        final_errors.append("toy_target_definitions")
    if not admitted_imports_only:
        final_errors.append("non_admitted_imports")
    if batch["returncode"] != 0:
        final_errors.append("batch_lake_env_lean_failed")
    final_errors.extend(provenance_errors)
    command_log_ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "final_verify" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "CommandLogV05",
            "stage": "final_verify",
            "stage_sequence": ["final_verify"],
            "actual_python_function_executed": True,
            "actual_subprocess_executed": True,
            "command": batch["command"],
            "returncode": batch["returncode"],
            "stdout_tail": batch["stdout_tail"],
            "stderr_tail": batch["stderr_tail"],
            "batch_final_verify": True,
            "batch_candidate_path": batch["batch_path"],
            "batch_candidate_ref": batch["batch_ref"],
            "task_count": batch["task_count"],
            "task_id": task_id,
            "candidate_ref": sha256_file(candidate_path),
        },
        id_field="command_log_id",
    )
    final_body = {
        "schema_version": "FinalVerifyReportFull2D",
        "target_obligation_id": task_id,
        "candidate_ref": sha256_file(candidate_path),
        "candidate_path": str(candidate_path),
        "compiled_batch_candidate_ref": batch["batch_ref"],
        "compiled_batch_candidate_path": batch["batch_path"],
        "source_path": str(source_path),
        "lake_env_lean_command": batch["command"],
        "lake_env_lean_returncode": batch["returncode"],
        "lake_env_lean_stdout_tail": batch["stdout_tail"],
        "lake_env_lean_stderr_tail": batch["stderr_tail"],
        "theorem_name": theorem_name,
        "theorem_statement_hash": theorem_statement_hash,
        "theorem_statement_unchanged": theorem_statement_unchanged,
        "proof_region_guard_passed": proof_region_guard_passed,
        "no_sorry": no_sorry,
        "forbidden_declarations": forbidden,
        "no_forbidden_declarations": not forbidden,
        "toy_target_definitions": toy_tokens,
        "no_toy_target_definitions": not toy_tokens,
        "admitted_import_prefixes": ["MathAutoResearch", "Mathlib", "LeanGeo", "Lean"],
        "non_admitted_imports": bad_imports,
        "admitted_imports_only": admitted_imports_only,
        "proof_use_provenance_status": "passed" if not provenance_errors else "failed",
        "proof_use_provenance_errors": provenance_errors,
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_use_status": "final_theorem" if not final_errors else "not_allowed",
        "status": "passed" if not final_errors else "failed",
        "errors": sorted(set(final_errors)),
    }
    final_ref, _ = write_artifact(
        run_dir,
        Path("final_verify_reports") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        final_body,
        id_field="report_id",
    )
    validation_errors = [
        f"final_verify:{error}"
        for error in validate_payload(read_json(run_dir / "final_verify_reports" / f"{safe_id(task_id)}__{safe_id(baseline)}.json"), current_head=git_head)
    ]
    if final_errors:
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="final_verify",
            input_refs=[str(upstream.get("claim_ref", "")), str(upstream.get("derivation_ref", "")), str(upstream.get("compiler_ref", "")), prepared["worker_ref"], final_ref],
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "final_verify",
                "stage_sequence": ["final_verify"],
                "actual_python_function_executed": True,
                "actual_subprocess_executed": True,
                "command": batch["command"],
                "returncode": batch["returncode"],
                "errors": final_errors,
                "final_verify_report_ref": final_ref,
                "batch_final_verify": True,
            },
            failure_kind="real_execution_failure",
            failure_reason="Batch FinalVerifyGate rejected the ProofWorker candidate",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        proof_run = proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=[f"final_verify:{error}" for error in final_errors])
        proof_run.update(
            {
                "proof_worker_result_ref": prepared["worker_ref"],
                "final_verify_report_ref": final_ref,
                "candidate_ref": sha256_file(candidate_path),
                "candidate_path": str(candidate_path),
                "command": batch["command"],
                "command_log_ref": command_log_ref,
                "validation_errors": validation_errors,
            }
        )
        return {"proof_run": proof_run, "errors": proof_run["errors"], "validation_errors": validation_errors}
    certificate_ref, _ = write_artifact(
        run_dir,
        Path("solver_backed_certificates") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "SolverBackedCertificateV05",
            "task_id": task_id,
            "baseline_id": baseline,
            "claim_spec_ref": upstream["claim_ref"],
            "selected_solver_derivation_ref": upstream["derivation_ref"],
            "compiler_result_ref": upstream["compiler_ref"],
            "lean_patch_candidate_ref": upstream["patch_ref"],
            "proof_worker_result_ref": prepared["worker_ref"],
            "final_verify_report_ref": final_ref,
            "used_rule_ids": upstream.get("rule_ids", []),
            "used_engine_roles": upstream.get("used_engine_roles", []),
            "batch_final_verify_command_log_ref": command_log_ref,
            "status": "solver_causal_candidate_pending_mutation",
        },
        id_field="certificate_id",
    )
    proof_run = {
        "errors": [],
        "validation_errors": validation_errors,
        "final_status": "final_theorem",
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_worker_result_ref": prepared["worker_ref"],
        "final_verify_report_ref": final_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "failure_report_ref": None,
        "candidate_ref": sha256_file(candidate_path),
        "candidate_path": str(candidate_path),
        "command": batch["command"],
        "command_log_ref": command_log_ref,
        "theorem_statement_unchanged": True,
        "no_sorry": True,
        "patch_text": upstream.get("patch_text", ""),
    }
    return {"proof_run": proof_run, "errors": [], "validation_errors": validation_errors}


def run_proof_worker_and_final_verify(
    *,
    run_dir: Path,
    corpus_root: Path,
    task: dict[str, Any],
    baseline: str,
    upstream: dict[str, Any],
    git_head: str,
    selected_impl: str,
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    disabled_components = list(upstream.get("disabled_components", []))
    input_refs = [
        str(upstream.get("claim_ref", "")),
        str(upstream.get("derivation_ref", "")),
        str(upstream.get("compiler_ref", "")),
        str(upstream.get("patch_ref", "")),
    ]
    if not str(upstream.get("patch_text", "")).strip():
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="compiler",
            input_refs=input_refs,
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "compiler",
                "stage_sequence": ["claimspec", "provider", "independent_checker", "selected_derivation", "compiler"],
                "actual_python_function_executed": True,
                "returncode": 1,
                "errors": upstream.get("errors", []),
            },
            failure_kind="unsupported_after_disabled_component" if disabled_components else "validation_rejected",
            failure_reason="compiler did not produce a Lean patch from checked selected solver derivation",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        return proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=["compiler_no_patch_text_from_selected_derivation"])

    patch_path = Path(str(upstream.get("patch_path", "")))
    if not patch_path.exists():
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="proof_worker",
            input_refs=input_refs,
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "proof_worker",
                "stage_sequence": ["proof_worker"],
                "actual_python_function_executed": False,
                "returncode": 1,
                "errors": ["patch_artifact_path_missing"],
            },
            failure_kind="validation_rejected",
            failure_reason="LeanPatchCandidateFull2D artifact was missing before ProofWorker execution",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        return proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=["patch_artifact_path_missing"])

    source_path = write_task_source_lean(run_dir, corpus_root, task, baseline)
    proof_root = run_dir / "proof_worker_task_runs" / safe_id(baseline) / safe_id(task_id)
    patch_payload = read_json(patch_path)
    worker = apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch_payload,
        output_dir=proof_root,
        run_id=f"actual_full2d_run:v0_5:{task_id}:{baseline}",
        task_id=task_id,
    )
    worker_ref, _ = write_artifact(
        run_dir,
        Path("proof_worker_results") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        strip_identity(worker),
        id_field="worker_result_id",
    )
    validation_errors = [f"proof_worker:{error}" for error in validate_payload(read_json(run_dir / "proof_worker_results" / f"{safe_id(task_id)}__{safe_id(baseline)}.json"), current_head=git_head)]
    if worker.get("status") != "patch_applied":
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="proof_worker",
            input_refs=[*input_refs, worker_ref],
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "proof_worker",
                "stage_sequence": ["proof_worker"],
                "actual_python_function_executed": True,
                "returncode": 1,
                "errors": worker.get("errors", []),
                "worker_result_ref": worker_ref,
            },
            failure_kind="validation_rejected",
            failure_reason="ProofWorker rejected the Lean patch candidate",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        result = proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=[f"proof_worker:{error}" for error in worker.get("errors", [])])
        result["proof_worker_result_ref"] = worker_ref
        result["validation_errors"] = validation_errors
        return result

    candidate_path = Path(str(worker.get("generated_candidate_path", "")))
    provenance = {
        "claim_spec_ref": upstream["claim_ref"],
        "compiler_result_ref": upstream["compiler_ref"],
        "lean_patch_candidate_ref": upstream["patch_ref"],
        "proof_worker_result_ref": worker_ref,
        "proof_region_diff_ref": worker.get("proof_region_diff_ref"),
        "generated_candidate_file_ref": worker.get("generated_candidate_file_ref"),
    }
    final = final_verify_gate_full2d_v0_5(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        target_obligation_id=task_id,
        proof_use_provenance=provenance,
        output_dir=proof_root,
    )
    command_log_ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "final_verify" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "CommandLogV05",
            "stage": "final_verify",
            "stage_sequence": ["final_verify"],
            "actual_python_function_executed": True,
            "actual_subprocess_executed": True,
            "command": final.get("lake_env_lean_command", []),
            "returncode": final.get("lake_env_lean_returncode"),
            "stdout_tail": final.get("lake_env_lean_stdout_tail", ""),
            "stderr_tail": final.get("lake_env_lean_stderr_tail", ""),
        },
        id_field="command_log_id",
    )
    final_ref, _ = write_artifact(
        run_dir,
        Path("final_verify_reports") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        strip_identity(final),
        id_field="report_id",
    )
    validation_errors.extend(
        f"final_verify:{error}"
        for error in validate_payload(read_json(run_dir / "final_verify_reports" / f"{safe_id(task_id)}__{safe_id(baseline)}.json"), current_head=git_head)
    )
    if final.get("status") != "passed":
        failure_ref = write_stage_failure(
            run_dir=run_dir,
            task_id=task_id,
            baseline=baseline,
            stage="final_verify",
            input_refs=[*input_refs, worker_ref, final_ref],
            command_log_payload={
                "schema_version": "CommandLogV05",
                "stage": "final_verify",
                "stage_sequence": ["final_verify"],
                "actual_python_function_executed": True,
                "actual_subprocess_executed": True,
                "command": final.get("lake_env_lean_command", []),
                "returncode": final.get("lake_env_lean_returncode"),
                "errors": final.get("errors", []),
                "final_verify_report_ref": final_ref,
            },
            failure_kind="real_execution_failure",
            failure_reason="FinalVerifyGate rejected the ProofWorker candidate",
            git_head=git_head,
            selected_impl=selected_impl,
            disabled_components=disabled_components,
        )
        result = proof_failure_result(task_id, baseline, failure_ref, "StageFailureReportV1", errors=[f"final_verify:{error}" for error in final.get("errors", [])])
        result.update(
            {
                "proof_worker_result_ref": worker_ref,
                "final_verify_report_ref": final_ref,
                "candidate_ref": final.get("candidate_ref", failure_ref),
                "candidate_path": str(candidate_path),
                "command": final.get("lake_env_lean_command", []),
                "command_log_ref": command_log_ref,
                "validation_errors": validation_errors,
            }
        )
        return result

    certificate_ref, _ = write_artifact(
        run_dir,
        Path("solver_backed_certificates") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "SolverBackedCertificateV05",
            "task_id": task_id,
            "baseline_id": baseline,
            "claim_spec_ref": upstream["claim_ref"],
            "selected_solver_derivation_ref": upstream["derivation_ref"],
            "compiler_result_ref": upstream["compiler_ref"],
            "lean_patch_candidate_ref": upstream["patch_ref"],
            "proof_worker_result_ref": worker_ref,
            "final_verify_report_ref": final_ref,
            "used_rule_ids": upstream.get("rule_ids", []),
            "used_engine_roles": upstream.get("used_engine_roles", []),
            "status": "solver_causal_candidate_pending_mutation",
        },
        id_field="certificate_id",
    )
    return {
        "errors": [],
        "validation_errors": validation_errors,
        "final_status": "final_theorem",
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_worker_result_ref": worker_ref,
        "final_verify_report_ref": final_ref,
        "solver_backed_certificate_ref": certificate_ref,
        "failure_report_ref": None,
        "candidate_ref": final.get("candidate_ref", ""),
        "candidate_path": str(candidate_path),
        "command": final.get("lake_env_lean_command", []),
        "command_log_ref": command_log_ref,
        "theorem_statement_unchanged": final.get("theorem_statement_unchanged") is True,
        "no_sorry": final.get("no_sorry") is True,
        "patch_text": upstream.get("patch_text", ""),
    }


def proof_failure_result(task_id: str, baseline: str, failure_ref: str, source: str, *, errors: list[str]) -> dict[str, Any]:
    del task_id, baseline
    return {
        "errors": errors,
        "validation_errors": [],
        "final_status": "measured_failure",
        "final_status_source": source,
        "proof_worker_result_ref": failure_ref,
        "final_verify_report_ref": failure_ref,
        "solver_backed_certificate_ref": failure_ref,
        "failure_report_ref": failure_ref,
        "candidate_ref": failure_ref,
        "candidate_path": "",
        "command": [],
        "command_log_ref": failure_ref,
        "theorem_statement_unchanged": False,
        "no_sorry": False,
        "patch_text": "",
    }


def write_task_source_lean(run_dir: Path, corpus_root: Path, task: dict[str, Any], baseline: str) -> Path:
    del corpus_root
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    statement = str(task["formal_statement"])
    header = statement.split(":= by", 1)[0].strip()
    text = "\n".join(
        [
            "import MathAutoResearch.GeometryFull2D.Inequality",
            "",
            "namespace MathAutoResearch.GeometryFull2D",
            "",
            header + " := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            "  sorry",
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
            "end MathAutoResearch.GeometryFull2D",
            "",
        ]
    )
    path = run_dir / "source_lean_tasks" / safe_id(baseline) / f"{safe_id(task_id)}.lean"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_stage_failure(
    *,
    run_dir: Path,
    task_id: str,
    baseline: str,
    stage: str,
    input_refs: list[str],
    command_log_payload: dict[str, Any],
    failure_kind: str,
    failure_reason: str,
    git_head: str,
    selected_impl: str,
    disabled_components: list[str],
) -> str:
    command_ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "stage_failures" / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(stage)}.json",
        command_log_payload,
        id_field="command_log_id",
    )
    failure_ref, _ = write_artifact(
        run_dir,
        Path("stage_failures") / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(stage)}.json",
        {
            "schema_version": "StageFailureReportV1",
            "stage": stage,
            "baseline_id": baseline,
            "disabled_components": disabled_components,
            "input_refs": [ref for ref in input_refs if valid_ref(ref)],
            "command_log_ref": command_ref,
            "failure_kind": failure_kind,
            "failure_reason": failure_reason,
            "git_head": git_head,
            "selected_implementation_hash": selected_impl,
        },
        id_field="failure_report_id",
    )
    return failure_ref


def materialize_record(
    *,
    run_dir: Path,
    task: dict[str, Any],
    baseline: str,
    corpus_ref: str,
    config_ref: str,
    selected_impl: str,
    git_head: str,
    run_dir_hash: str,
    upstream: dict[str, Any],
    proof_run: dict[str, Any],
    disabled_components: list[str] | None = None,
) -> dict[str, Any]:
    del run_dir
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    pending_causality_ref = sha256_text("pending_causality:" + task_id)
    cert_ref = str(proof_run.get("solver_backed_certificate_ref") or proof_run.get("failure_report_ref") or sha256_text("missing_certificate:" + task_id))
    failure_ref = str(proof_run.get("failure_report_ref") or "")
    patch_available = bool(str(upstream.get("patch_text", "")).strip())
    checker_refs = list(upstream.get("checker_refs") or ([failure_ref] if valid_ref(failure_ref) else []))
    selected_derivation_ref = str(upstream["derivation_ref"]) if patch_available else failure_ref
    compiler_refs = [str(upstream["compiler_ref"])] if patch_available else ([failure_ref] if valid_ref(failure_ref) else [str(upstream["compiler_ref"])])
    patch_ref = str(upstream["patch_ref"]) if patch_available else failure_ref
    record = {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": f"actual_full2d_run:v0_5:{task_id}:{baseline}",
        "task_id": task_id,
        "theorem_name": theorem_name,
        "baseline_id": baseline,
        "corpus_manifest_hash": corpus_ref,
        "config_hash": config_ref,
        "git_head": git_head,
        "selected_implementation_hash": selected_impl,
        "release_run_dir_hash": run_dir_hash,
        "source_theorem_ref": upstream["source_ref"],
        "source_theorem_preproved": False,
        "extraction_report_ref": upstream["extraction_ref"],
        "claim_spec_ref": upstream["claim_ref"],
        "provider_run_manifest_ref": upstream["provider_ref"],
        "engine_output_refs": upstream["engine_refs"],
        "independent_checker_report_refs": checker_refs,
        "selected_solver_derivation_ref": selected_derivation_ref,
        "compiler_result_refs": compiler_refs,
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": proof_run["proof_worker_result_ref"],
        "final_verify_report_ref": proof_run["final_verify_report_ref"],
        "solver_causality_report_ref": pending_causality_ref,
        "solver_backed_certificate_ref": cert_ref,
        "causal_chain_hash": MUTATION_PENDING_REF,
        "final_status": proof_run["final_status"],
        "final_status_source": proof_run["final_status_source"],
        "used_rule_ids": upstream["rule_ids"],
        "used_engine_roles": upstream.get("used_engine_roles") or [],
        "has_non_target_intermediate": upstream["has_non_target_intermediate"],
        "has_construction_case_certificate": upstream["has_construction_case_certificate"],
        "direct_or_wrapped_facade_success": bool(upstream.get("direct_or_wrapped_facade_success")),
    }
    if disabled_components:
        record["baseline_disabled_components"] = disabled_components
    if proof_run.get("failure_report_ref"):
        record["failure_report_ref"] = proof_run["failure_report_ref"]
    record["causal_chain_hash"] = causal_chain_hash(record)
    return {"record": record, "validation_errors": validate_payload(record, current_head=git_head)}


def missing_b2_upstream_bundle(task_id: str, extraction_ref: str) -> dict[str, Any]:
    missing = sha256_text("missing_b2_upstream:" + task_id)
    return {
        "errors": ["missing_upstream_bundle"],
        "validation_errors": [],
        "baseline": "unknown",
        "disabled_components": [],
        "source_ref": missing,
        "extraction_ref": extraction_ref,
        "claim_ref": missing,
        "claim_path": "",
        "provider_ref": missing,
        "engine_refs": [missing],
        "checker_refs": [missing],
        "derivation_ref": missing,
        "compiler_ref": missing,
        "patch_ref": missing,
        "patch_path": "",
        "patch_text": "",
        "rule_ids": [],
        "has_non_target_intermediate": False,
        "has_construction_case_certificate": False,
        "used_engine_roles": [],
        "direct_or_wrapped_facade_success": False,
    }


def run_provider_and_checkers(
    run_dir: Path,
    task_id: str,
    claim_path: Path,
    claim_ref: str,
    *,
    baseline: str,
    disabled_components: list[str],
) -> dict[str, Any]:
    disabled_roles = tuple(role for role in disabled_components if role in ENGINE_ROLES)
    disabled_component = "geometry_solver_provider" if "geometry_solver_provider" in disabled_components else (disabled_components[0] if disabled_components else "none")
    task_root = run_dir / "provider_task_runs" / safe_id(baseline) / safe_id(task_id)
    if task_root.exists():
        shutil.rmtree(task_root)
    provider_summary = run_provider_cli(
        claim_path,
        task_root,
        f"provider:v0_5:{task_id}:{baseline}",
        claim_spec_ref=claim_ref,
        task_id=task_id,
        baseline_id=baseline,
        disabled_component=disabled_component,
        disabled_engine_roles=disabled_roles,
    )
    checker_summary = run_independent_solver_checkers(task_root, claim_spec_json=claim_path, write_reports=True)
    provider_errors = [f"provider_cli:{error}" for error in provider_summary.get("errors", [])]
    checker_errors = [f"independent_checker:{error}" for error in checker_summary.get("errors", [])]
    fatal_errors: list[str] = []
    for error in provider_errors:
        if disabled_components and error == "provider_cli:engine_output_count_mismatch":
            continue
        fatal_errors.append(error)
    checker_refs_by_role: dict[str, str] = {}
    for ref, rel_path in checker_summary.get("report_paths", {}).items():
        payload = read_json(task_root / rel_path)
        role = str(payload.get("engine_role"))
        if payload.get("status") == "passed":
            checker_refs_by_role[role] = str(ref)
        write_json(run_dir / "independent_checker_reports" / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(role)}.json", payload)
    engine_refs: list[str] = []
    engine_refs_by_role: dict[str, str] = {}
    normalized_artifact_refs_by_role: dict[str, str] = {}
    normalized_artifacts_by_role: dict[str, dict[str, Any]] = {}
    selected_facts: list[str] = []
    artifact_paths = provider_summary.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        artifact_paths = {}
    engine_dir = task_root / "provider_stage" / "engine_outputs"
    for path in sorted(engine_dir.glob("*.json")) if engine_dir.exists() else []:
        payload = read_json(path)
        role = str(payload.get("engine_role"))
        body = strip_identity(payload)
        if role in checker_refs_by_role and body.get("engine_status") == "normalized_success":
            body["independent_checker_report_refs"] = [checker_refs_by_role[role]]
            for fact in body.get("facts", []):
                if isinstance(fact, dict):
                    fact["checker_report_ref"] = checker_refs_by_role[role]
                    selected_facts.append(str(fact.get("fact_id")))
            for construction in body.get("constructions", []):
                if isinstance(construction, dict):
                    construction["checker_report_ref"] = checker_refs_by_role[role]
            for certificate in body.get("certificates", []):
                if isinstance(certificate, dict):
                    certificate["checker_report_ref"] = checker_refs_by_role[role]
        ref, _ = write_artifact(
            run_dir,
            Path("provider_stage") / "engine_outputs" / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(role)}.json",
            body,
            id_field="output_id",
        )
        engine_refs.append(ref)
        engine_refs_by_role[role] = ref
        normalized_refs = [str(item) for item in payload.get("normalized_artifact_refs", []) if isinstance(item, str)]
        if normalized_refs:
            normalized_ref = normalized_refs[0]
            normalized_artifact_refs_by_role[role] = normalized_ref
            rel_path = artifact_paths.get(normalized_ref)
            if isinstance(rel_path, str):
                artifact_path = task_root / rel_path
                if artifact_path.exists():
                    normalized_artifacts_by_role[role] = strip_identity(read_json(artifact_path))
                else:
                    fatal_errors.append(f"normalized_artifact_path_missing:{role}")
            else:
                fatal_errors.append(f"normalized_artifact_ref_unresolved:{role}")
    provider_summary_ref, _ = write_artifact(
        run_dir,
        Path("provider_stage") / "provider_summaries" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        strip_identity(provider_summary),
        id_field="summary_id",
    )
    checker_summary_ref, _ = write_artifact(
        run_dir,
        Path("independent_checker_reports") / f"{safe_id(task_id)}__{safe_id(baseline)}__summary.json",
        strip_identity(checker_summary),
        id_field="summary_id",
    )
    return {
        "fatal_errors": sorted(set(fatal_errors)),
        "nonfatal_errors": sorted(set(provider_errors + checker_errors)),
        "engine_refs": engine_refs,
        "engine_refs_by_role": engine_refs_by_role,
        "checker_refs": [checker_refs_by_role[role] for role in sorted(checker_refs_by_role)],
        "checker_refs_by_role": checker_refs_by_role,
        "selected_facts": sorted(set(selected_facts)),
        "normalized_artifact_refs_by_role": normalized_artifact_refs_by_role,
        "normalized_artifacts_by_role": normalized_artifacts_by_role,
        "provider_summary_ref": provider_summary_ref,
        "checker_summary_ref": checker_summary_ref,
        "disabled_engine_roles": list(disabled_roles),
    }


def claim_spec_for_task(task_id: str, theorem_name: str, extraction_ref: str, extraction_report: dict[str, Any]) -> dict[str, Any]:
    canonical = extraction_report.get("canonical_statement") if isinstance(extraction_report.get("canonical_statement"), dict) else {}
    return {
        "schema_version": "GeometryFull2DClaimSpec",
        "source_extraction_report_ref": extraction_ref,
        "source_statement_hash": extraction_report.get("source_statement_hash"),
        "claim_key": f"claim:{task_id}:{theorem_name}",
        "theorem_name": theorem_name,
        "objects": canonical.get("objects", []),
        "hypotheses": canonical.get("hypotheses", []),
        "target": canonical.get("target", {"kind": "lean_elaborated_goal", "theorem_name": theorem_name}),
        "side_conditions": canonical.get("side_conditions", {}),
        "relation_to_goal": canonical.get("relation_to_goal", {}),
    }


def strip_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in payload.items()
        if key
        not in {
            "artifact_sha256",
            "certificate_id",
            "claim_id",
            "content_sha256",
            "derivation_id",
            "manifest_id",
            "output_id",
            "patch_id",
            "payload_sha256",
            "registry_content_id",
            "registry_id",
            "report_id",
            "result_id",
            "source_theorem_id",
            "summary_id",
            "worker_result_id",
        }
    }


def valid_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def indent_proof_region(proof_text: str) -> str:
    if not proof_text.strip():
        return ""
    lines = proof_text.splitlines()
    return "\n".join("" if not line.strip() else "  " + line for line in lines)


def causal_chain_hash(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "causal_chain_hash"}
    return sha256_text(canonical_json(payload))


def write_artifact(run_dir: Path, rel_path: Path, payload_without_id: dict[str, Any], *, id_field: str) -> tuple[str, Path]:
    body = strip_identity(dict(payload_without_id))
    content_ref = sha256_text(canonical_json(body))
    payload = {**body, id_field: content_ref, "content_sha256": content_ref}
    path = run_dir / rel_path
    write_json(path, payload)
    return content_ref, path


def selected_implementation_hash() -> str:
    freeze = ROOT / "benchmarks" / "geometry_full2d_v0_5" / "freeze_manifest.json"
    if freeze.exists():
        try:
            payload = read_json(freeze)
            value = payload.get("selected_implementation_hash")
            if isinstance(value, str) and value.startswith("sha256:"):
                return value
        except Exception:
            pass
    return sha256_text("selected_implementation_hash_unavailable:" + current_git_head())


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
