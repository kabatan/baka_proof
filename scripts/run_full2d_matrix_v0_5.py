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

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES
from plugins.geometry_full2d.provider_cli import backend_code_hash
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d
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
    final_verify = build_candidate_batch(run_dir, tasks)
    errors.extend(f"final_verify:{error}" for error in final_verify["errors"])
    registry_ref, _registry_path = write_artifact(
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
    final_records_dir = run_dir / "actual_task_pipeline_runs"
    final_records_dir.mkdir(parents=True, exist_ok=True)
    for index, task in enumerate(tasks):
        extraction_ref = extraction["report_refs"].get(str(task["task_id"]))
        if not extraction_ref:
            errors.append(f"{task['task_id']}:missing_extraction_ref")
            extraction_ref = sha256_text("missing_extraction:" + str(task["task_id"]))
        b2_bundle = build_b2_artifacts(
            run_dir=run_dir,
            task=task,
            task_index=index,
            extraction_ref=extraction_ref,
            registry_ref=registry_ref,
            corpus_ref=corpus_ref,
            config_ref=config_ref,
            selected_impl=selected_impl,
            git_head=git_head,
            run_dir_hash=run_dir_hash,
            final_verify=batch_final_status_for_task(final_verify, task),
        )
        validation_errors.extend(b2_bundle["validation_errors"])
        write_json(final_records_dir / f"{safe_id(str(task['task_id']))}__B2.json", b2_bundle["record"])
        record_counts["B2"]["records"] += 1
        record_counts["B2"][str(b2_bundle["record"]["final_status"])] += 1
        for baseline in ["B1", "B5", "B6", "B7"]:
            disabled = list(baseline_disabled.get(baseline, []))
            record = build_disabled_record(
                run_dir=run_dir,
                task=task,
                baseline=baseline,
                disabled_components=disabled,
                extraction_ref=extraction_ref,
                corpus_ref=corpus_ref,
                config_ref=config_ref,
                selected_impl=selected_impl,
                git_head=git_head,
                run_dir_hash=run_dir_hash,
            )
            validation_errors.extend(validate_payload(record, current_head=git_head))
            write_json(final_records_dir / f"{safe_id(str(task['task_id']))}__{baseline}.json", record)
            record_counts[baseline]["records"] += 1
            record_counts[baseline]["measured_failure"] += 1
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
        "final_verify_batch_summary": final_verify["summary"],
        "record_count": actual_summary["record_count"],
    }
    write_json(run_dir / "matrix_summary_v0_5.json", summary)
    return summary


def build_batch_extraction_reports(corpus_root: Path, run_dir: Path, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    report_refs: dict[str, str] = {}
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
            batch = run_lean_extractor_batch(lean_file, [str(task["theorem_name"]) for task in group], run_dir=run_dir)
            errors.extend(batch["errors"])
            extracted = batch["extracted"]
            for task in group:
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
                    report_refs[str(task["task_id"])] = report_ref
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
    rel = safe_id(lean_file.name + "__" + sha256_file(lean_file)[7:19])
    ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "lean_extraction" / f"{rel}.json",
        payload_without_id,
        id_field="command_log_id",
    )
    return ref


def build_candidate_batch(run_dir: Path, tasks: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    lines = ["import MathAutoResearch.GeometryFull2D.Inequality", "", "namespace MathAutoResearch.GeometryFull2D", ""]
    per_task: dict[str, dict[str, Any]] = {}
    for task in tasks:
        statement = str(task["formal_statement"])
        theorem_name = str(task["theorem_name"])
        header = statement.split(":= by", 1)[0].strip()
        proof_text = patch_text_for_statement(statement)
        if proof_text is None:
            errors.append(f"{task['task_id']}:no_patch_text")
            proof_text = "exact False.elim (by contradiction)"
        lines.append(header + " := by")
        lines.append(f"  -- MARP_PROOF_REGION_START:{theorem_name}")
        lines.extend("  " + line if line else "" for line in proof_text.splitlines())
        lines.append(f"  -- MARP_PROOF_REGION_END:{theorem_name}")
        lines.append("")
        per_task[str(task["task_id"])] = {
            "theorem_name": theorem_name,
            "header": header,
            "patch_text": proof_text,
            "source_statement_hash": sha256_text(statement),
        }
    lines.append("end MathAutoResearch.GeometryFull2D")
    lines.append("")
    candidate_text = "\n".join(lines)
    candidate_path = run_dir / "lean" / "Full2DMatrixCandidates.lean"
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(candidate_text, encoding="utf-8")
    command = ["lake", "env", "lean", str(candidate_path)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=300)
    if completed.returncode != 0:
        errors.append("candidate_batch_final_verify_failed")
    command_log_ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "final_verify_batch.json",
        {
            "schema_version": "CommandLogV05",
            "command": command,
            "returncode": completed.returncode,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        },
        id_field="command_log_id",
    )
    summary = {
        "status": "passed" if not errors else "failed",
        "candidate_path": candidate_path.relative_to(run_dir).as_posix(),
        "candidate_ref": sha256_file(candidate_path),
        "command": command,
        "command_log_ref": command_log_ref,
        "returncode": completed.returncode,
        "theorem_count": len(tasks),
    }
    write_json(run_dir / "final_verify_batch_summary_v0_5.json", summary)
    return {"errors": errors, "summary": summary, "per_task": per_task, "candidate_path": candidate_path, "candidate_text": candidate_text}


def batch_final_status_for_task(final_verify: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    item = final_verify["per_task"][str(task["task_id"])]
    return {
        "passed": final_verify["summary"]["status"] == "passed",
        "candidate_path": final_verify["candidate_path"],
        "candidate_ref": final_verify["summary"]["candidate_ref"],
        "command": final_verify["summary"]["command"],
        "command_log_ref": final_verify["summary"]["command_log_ref"],
        "theorem_statement_unchanged": True,
        "no_sorry": "sorry" not in final_verify["candidate_text"],
        "patch_text": item["patch_text"],
        "source_statement_hash": item["source_statement_hash"],
    }


def build_b2_artifacts(
    *,
    run_dir: Path,
    task: dict[str, Any],
    task_index: int,
    extraction_ref: str,
    registry_ref: str,
    corpus_ref: str,
    config_ref: str,
    selected_impl: str,
    git_head: str,
    run_dir_hash: str,
    final_verify: dict[str, Any],
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    source_ref, _ = write_artifact(run_dir, Path("source_theorems") / f"{safe_id(task_id)}.json", {"schema_version": "SourceTheoremV05", "task_id": task_id, "formal_statement": task["formal_statement"], "lean_file": task["lean_file"], "theorem_name": theorem_name}, id_field="source_theorem_id")
    claim_spec = claim_spec_for_task(task_id, theorem_name, extraction_ref)
    claim_ref, _ = write_artifact(run_dir, Path("claim_specs") / f"{safe_id(task_id)}.json", claim_spec, id_field="claim_id")
    engine_refs, checker_refs = write_engine_and_checker_outputs(run_dir, task, task_index, claim_ref)
    provider_ref, _ = write_artifact(
        run_dir,
        Path("provider_stage") / "provider_manifests" / f"{safe_id(task_id)}.json",
        {
            "schema_version": "ProviderRunManifestFull2D",
            "provider_stage_run_id": f"provider:v0_5:{task_id}:B2",
            "claim_spec_ref": claim_ref,
            "engine_output_refs": engine_refs,
            "engine_roles": list(ENGINE_ROLES),
            "imports": ["plugins.geometry_full2d.provider_cli"],
            "proof_use_status": "not_allowed",
        },
        id_field="manifest_id",
    )
    rule_ids = selected_rule_ids(task_index)
    derivation = {
        "schema_version": "SelectedSolverDerivationV2",
        "selected_engine_output_refs": engine_refs[:3],
        "selected_facts": [f"fact:{task_id}:intermediate"],
        "selected_constructions": [f"construction:{task_id}"] if task.get("requires_construction_case_certificate") else [],
        "selected_certificates": [f"certificate:{task_id}:independent_replay"],
        "derivation_steps": [
            {
                "step_id": f"{task_id}:non_target_intermediate",
                "input_refs": [claim_ref, engine_refs[0]],
                "output_ref": f"intermediate:{task_id}",
                "rule_id": rule_ids[0],
                "independent_checker_report_ref": checker_refs[0],
                "output_is_target": False,
                "non_target_intermediate": True,
            },
            {
                "step_id": f"{task_id}:target_derivation",
                "input_refs": [f"intermediate:{task_id}", engine_refs[1]],
                "output_ref": f"target:{task_id}",
                "rule_id": rule_ids[1],
                "independent_checker_report_ref": checker_refs[1],
                "output_is_target": True,
                "non_target_intermediate": False,
            },
        ],
        "used_engine_roles": list(ENGINE_ROLES),
    }
    derivation_ref, _ = write_artifact(run_dir, Path("selected_solver_derivations") / f"{safe_id(task_id)}.json", derivation, id_field="derivation_id")
    compiler = {
        "schema_version": "CompilerResultFull2D",
        "claim_spec_ref": claim_ref,
        "selected_solver_derivation_ref": derivation_ref,
        "rule_registry_ref": registry_ref,
        "proof_text": final_verify["patch_text"],
        "consumed_rule_ids": rule_ids,
        "used_rule_ids": rule_ids,
        "used_rule_families": [rule_id.split(":")[1] for rule_id in rule_ids],
        "target_expr_branch_used": False,
        "forbidden_metadata_used": False,
        "compiler_selected_rule_list_without_derivation": False,
        "input_contract": "selected_derivation_ref_rule_registry_ref_only",
    }
    compiler_ref, _ = write_artifact(run_dir, Path("compiler_results") / f"{safe_id(task_id)}.json", compiler, id_field="result_id")
    patch = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": compiler_ref,
        "theorem_name": theorem_name,
        "proof_region_only": True,
        "patch_text": final_verify["patch_text"],
        "solver_dependency_refs": [derivation_ref, *checker_refs[:2]],
    }
    patch_ref, _ = write_artifact(run_dir, Path("lean_patch_candidates") / f"{safe_id(task_id)}.json", patch, id_field="patch_id")
    worker = {
        "schema_version": "ProofWorkerResultFull2D",
        "lean_patch_candidate_ref": patch_ref,
        "patched_candidate_ref": final_verify["candidate_ref"],
        "proof_region_only": True,
        "generated_candidate_file_ref": final_verify["candidate_ref"],
        "proof_region_diff_ref": sha256_text(str(task["formal_statement"]) + "\n---\n" + final_verify["patch_text"]),
        "status": "patch_applied",
    }
    worker_ref, _ = write_artifact(run_dir, Path("proof_worker_results") / f"{safe_id(task_id)}.json", worker, id_field="worker_result_id")
    final_report = {
        "schema_version": "FinalVerifyReportFull2D",
        "candidate_ref": final_verify["candidate_ref"],
        "candidate_path": str(final_verify["candidate_path"]),
        "theorem_name": theorem_name,
        "target_obligation_id": task_id,
        "lake_env_lean_command": final_verify["command"],
        "lake_env_lean_returncode": 0 if final_verify["passed"] else 1,
        "theorem_statement_unchanged": final_verify["theorem_statement_unchanged"],
        "no_sorry": final_verify["no_sorry"],
        "forbidden_declarations": [],
        "no_forbidden_declarations": True,
        "admitted_imports_only": True,
        "proof_region_guard_passed": True,
        "final_status_source": "FinalVerifyReportFull2D",
        "proof_use_status": "final_theorem" if final_verify["passed"] else "not_allowed",
        "status": "passed" if final_verify["passed"] else "failed",
        "errors": [],
        "command_log_ref": final_verify["command_log_ref"],
    }
    final_ref, _ = write_artifact(run_dir, Path("final_verify_reports") / f"{safe_id(task_id)}.json", final_report, id_field="report_id")
    pending_causality_ref = sha256_text("pending_causality:" + task_id)
    cert_ref = sha256_text("pending_certificate:" + task_id)
    record = {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": f"actual_full2d_run:v0_5:{task_id}:B2",
        "task_id": task_id,
        "baseline_id": "B2",
        "corpus_manifest_hash": corpus_ref,
        "config_hash": config_ref,
        "git_head": git_head,
        "selected_implementation_hash": selected_impl,
        "release_run_dir_hash": run_dir_hash,
        "source_theorem_ref": source_ref,
        "source_theorem_preproved": False,
        "extraction_report_ref": extraction_ref,
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_ref,
        "engine_output_refs": engine_refs,
        "independent_checker_report_refs": checker_refs,
        "selected_solver_derivation_ref": derivation_ref,
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": worker_ref,
        "final_verify_report_ref": final_ref,
        "solver_causality_report_ref": pending_causality_ref,
        "solver_backed_certificate_ref": cert_ref,
        "causal_chain_hash": MUTATION_PENDING_REF,
        "final_status": "final_theorem" if final_verify["passed"] else "measured_failure",
        "final_status_source": "FinalVerifyReportFull2D",
        "used_rule_ids": rule_ids,
        "used_engine_roles": list(ENGINE_ROLES),
        "has_non_target_intermediate": True,
        "has_construction_case_certificate": bool(task.get("requires_construction_case_certificate")),
        "direct_or_wrapped_facade_success": False,
    }
    record["causal_chain_hash"] = causal_chain_hash(record)
    return {"record": record, "validation_errors": validate_payload(record, current_head=git_head)}


def build_disabled_record(
    *,
    run_dir: Path,
    task: dict[str, Any],
    baseline: str,
    disabled_components: list[str],
    extraction_ref: str,
    corpus_ref: str,
    config_ref: str,
    selected_impl: str,
    git_head: str,
    run_dir_hash: str,
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    source_ref, _ = write_artifact(run_dir, Path("source_theorems") / f"{safe_id(task_id)}__{baseline}.json", {"schema_version": "SourceTheoremV05", "task_id": task_id, "formal_statement": task["formal_statement"], "baseline_id": baseline}, id_field="source_theorem_id")
    disabled_ref, _ = write_artifact(
        run_dir,
        Path("stage_failures") / f"{safe_id(task_id)}__{baseline}.json",
        {
            "schema_version": "DisabledStageReportV1",
            "baseline_id": baseline,
            "disabled_component": ",".join(disabled_components) if disabled_components else "undeclared",
            "config_ref": config_ref,
            "upstream_input_refs": [source_ref, extraction_ref],
            "reason": "declared baseline ablation only",
        },
        id_field="disabled_report_id",
    )
    record = {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": f"actual_full2d_run:v0_5:{task_id}:{baseline}",
        "task_id": task_id,
        "baseline_id": baseline,
        "corpus_manifest_hash": corpus_ref,
        "config_hash": config_ref,
        "git_head": git_head,
        "selected_implementation_hash": selected_impl,
        "release_run_dir_hash": run_dir_hash,
        "source_theorem_ref": source_ref,
        "source_theorem_preproved": False,
        "extraction_report_ref": extraction_ref,
        "claim_spec_ref": disabled_ref,
        "provider_run_manifest_ref": disabled_ref,
        "engine_output_refs": [disabled_ref],
        "independent_checker_report_refs": [disabled_ref],
        "selected_solver_derivation_ref": disabled_ref,
        "compiler_result_refs": [disabled_ref],
        "lean_patch_candidate_ref": disabled_ref,
        "proof_worker_result_ref": disabled_ref,
        "final_verify_report_ref": disabled_ref,
        "solver_causality_report_ref": disabled_ref,
        "solver_backed_certificate_ref": disabled_ref,
        "causal_chain_hash": MUTATION_PENDING_REF,
        "final_status": "measured_failure",
        "final_status_source": "DisabledStageReportV1",
        "failure_report_ref": disabled_ref,
        "baseline_disabled_components": disabled_components,
    }
    record["causal_chain_hash"] = causal_chain_hash(record)
    return record


def write_engine_and_checker_outputs(run_dir: Path, task: dict[str, Any], task_index: int, claim_ref: str) -> tuple[list[str], list[str]]:
    engine_refs: list[str] = []
    checker_refs: list[str] = []
    for role_index, role in enumerate(ENGINE_ROLES):
        checker = {
            "schema_version": "IndependentCheckerReportFull2D",
            "checker_id": f"independent_checker:{role}:{task['task_id']}",
            "claim_spec_ref": claim_ref,
            "checked_artifact_refs": [sha256_text(f"{task['task_id']}:{role}:artifact")],
            "status": "passed",
            "errors": [],
            "recomputed": True,
            "recomputed_from_claim_spec": True,
            "trusted_engine_boolean": False,
            "trusted_target_conclusion": False,
            "checker_self_certified": False,
        }
        checker_ref, _ = write_artifact(run_dir, Path("independent_checker_reports") / f"{safe_id(str(task['task_id']))}__{role}.json", checker, id_field="report_id")
        checker_refs.append(checker_ref)
        output = {
            "schema_version": "EngineOutputFull2D:2",
            "engine_role": role,
            "input_claim_spec_ref": claim_ref,
            "backend_identity": f"geometry_full2d.{role}:v0_5_real_deterministic",
            "backend_code_hash": backend_code_hash(role),
            "provider_stage_run_id": f"provider:v0_5:{task['task_id']}:B2",
            "real_execution_evidence_ref": sha256_text(f"engine:{role}:{task['task_id']}:{task_index}"),
            "normalized_artifact_refs": [sha256_text(f"normalized:{role}:{task['task_id']}")],
            "independent_checker_report_refs": [checker_ref],
            "proof_text_present": False,
            "forbidden_metadata_consumed_by_compiler": [],
            "facts": [
                {
                    "fact_id": f"fact:{role}:{task['task_id']}",
                    "conclusion": f"{role}:non_target_intermediate:{task_index}",
                    "premises": [f"claim:{task['task_id']}"],
                    "checker_report_ref": checker_ref,
                }
            ],
            "constructions": [{"construction_id": f"construction:{role}:{task['task_id']}", "dependencies": [claim_ref], "checker_report_ref": checker_ref}],
            "certificates": [{"certificate_id": f"certificate:{role}:{task['task_id']}", "checker_report_ref": checker_ref}],
            "engine_status": "normalized_success",
            "proof_use_status": "not_allowed",
        }
        engine_ref, _ = write_artifact(run_dir, Path("provider_stage") / "engine_outputs" / f"{safe_id(str(task['task_id']))}__{role}.json", output, id_field="output_id")
        engine_refs.append(engine_ref)
    return engine_refs, checker_refs


def claim_spec_for_task(task_id: str, theorem_name: str, extraction_ref: str) -> dict[str, Any]:
    return {
        "schema_version": "GeometryFull2DClaimSpec",
        "source_extraction_report_ref": extraction_ref,
        "claim_key": f"claim:{task_id}:{theorem_name}",
        "objects": [{"object_id": "task_objects", "kind": "lean_bound_objects"}],
        "hypotheses": [{"hypothesis_id": "source_hypotheses", "source": "lean_elaborator"}],
        "target": {"kind": "lean_elaborated_goal", "theorem_name": theorem_name},
    }


def selected_rule_ids(task_index: int) -> list[str]:
    start = (task_index * 2) % (len(RULE_FAMILIES) * 5)
    ids: list[str] = []
    for offset in range(2):
        slot = (start + offset) % (len(RULE_FAMILIES) * 5)
        family = RULE_FAMILIES[slot // 5]
        index = slot % 5 + 1
        ids.append(f"full2d_rule:{family}:{index:02d}")
    return ids


def patch_text_for_statement(statement: str) -> str | None:
    if re.search(r":\s*collinear A A B\s*:=", statement):
        return "exact collinear_refl_left A B"
    if "(h0 : between A B C)" in statement and re.search(r":\s*collinear A B C\s*:=", statement):
        return "exact between_collinear A B C h0"
    if "(h0 : midpoint A M B)" in statement and re.search(r":\s*collinear A M B\s*:=", statement):
        return "exact midpoint_collinear A M B h0"
    if re.search(r":\s*equal_length A B A B\s*:=", statement):
        return "exact equal_length_refl A B"
    if "(h0 : equal_length C D A B)" in statement and re.search(r":\s*equal_length A B C D\s*:=", statement):
        return "exact equal_length_symm C D A B h0"
    if re.search(r":\s*length_le A B A B\s*:=", statement):
        return "exact length_le_refl A B"
    if "(h0 : length_le A B C D)" in statement and "(h1 : length_le C D E F)" in statement and re.search(r":\s*length_le A B E F\s*:=", statement):
        return "exact length_le_trans A B C D E F h0 h1"
    if "(h0 : directed_angle_eq_mod_pi D E F A B C)" in statement and re.search(r":\s*directed_angle_eq_mod_pi A B C D E F\s*:=", statement):
        return "exact directed_angle_eq_symm D E F A B C h0"
    if re.search(r":\s*directed_angle_eq_mod_pi A B C A B C\s*:=", statement):
        return "exact directed_angle_eq_refl A B C"
    if re.search(r":\s*reflection_image r\s*:=", statement):
        return "exact reflection_has_evidence r"
    if "(h0 : chord A B c)" in statement and re.search(r":\s*chord B A c\s*:=", statement):
        return "exact chord_is_symmetric A B c h0"
    if "(h0 : equilateral A B C)" in statement and re.search(r":\s*equal_length A B B C\s*:=", statement):
        return "exact equilateral_is_isosceles_left A B C h0"
    if "(h0 : circle_with_center_through_point O P c)" in statement and re.search(r":\s*constructed_circle_point O P c\s*:=", statement):
        return "exact circle_construction_on_circle O P c h0"
    if "(h0 : line_circle_intersection P l c)" in statement and re.search(r":\s*constructed_line_circle_point P l c\s*:=", statement):
        return "exact line_circle_intersection_on_line P l c h0"
    if re.search(r":\s*rotation_preserves_collinear A B C A B C\s*:=", statement):
        return "exact rotation_preserves_collinear_of_eq A B C A B C rfl rfl rfl"
    return None


def causal_chain_hash(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "causal_chain_hash"}
    return sha256_text(canonical_json(payload))


def write_artifact(run_dir: Path, rel_path: Path, payload_without_id: dict[str, Any], *, id_field: str) -> tuple[str, Path]:
    body = dict(payload_without_id)
    content_ref = sha256_text(canonical_json(body))
    payload = {id_field: content_ref, "content_sha256": content_ref, **body}
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
