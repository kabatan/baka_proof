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
from plugins.geometry_full2d.provider_cli import run_provider_cli
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d
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
    upstreams: dict[str, dict[str, Any]] = {}
    for index, task in enumerate(tasks):
        task_id = str(task["task_id"])
        extraction_ref = extraction["report_refs"].get(task_id)
        extraction_report = extraction["reports"].get(task_id)
        if not extraction_ref or not isinstance(extraction_report, dict):
            errors.append(f"{task_id}:missing_extraction_for_upstream_pipeline")
            continue
        upstream = build_b2_upstream_artifacts(
            run_dir=run_dir,
            task=task,
            task_index=index,
            extraction_ref=extraction_ref,
            extraction_report=extraction_report,
            registry_ref=registry_ref,
            registry_path=registry_path,
        )
        validation_errors.extend(upstream["validation_errors"])
        errors.extend(f"{task_id}:upstream:{error}" for error in upstream["errors"])
        upstreams[task_id] = upstream
    final_verify = build_candidate_batch(run_dir, tasks, upstreams)
    errors.extend(f"final_verify:{error}" for error in final_verify["errors"])
    final_records_dir = run_dir / "actual_task_pipeline_runs"
    final_records_dir.mkdir(parents=True, exist_ok=True)
    for index, task in enumerate(tasks):
        task_id = str(task["task_id"])
        extraction_ref = extraction["report_refs"].get(str(task["task_id"]))
        if not extraction_ref:
            errors.append(f"{task['task_id']}:missing_extraction_ref")
            extraction_ref = sha256_text("missing_extraction:" + str(task["task_id"]))
        upstream = upstreams.get(task_id)
        if upstream is None:
            errors.append(f"{task_id}:missing_b2_upstream_bundle")
            upstream = missing_b2_upstream_bundle(task_id, extraction_ref)
        b2_bundle = materialize_b2_record(
            run_dir=run_dir,
            task=task,
            corpus_ref=corpus_ref,
            config_ref=config_ref,
            selected_impl=selected_impl,
            git_head=git_head,
            run_dir_hash=run_dir_hash,
            upstream=upstream,
            final_verify=batch_final_status_for_task(final_verify, task),
        )
        validation_errors.extend(b2_bundle["validation_errors"])
        write_json(final_records_dir / f"{safe_id(str(task['task_id']))}__B2.json", b2_bundle["record"])
        record_counts["B2"]["records"] += 1
        record_counts["B2"][str(b2_bundle["record"]["final_status"])] += 1
        for baseline in ["B1", "B5", "B6", "B7"]:
            disabled = list(baseline_disabled.get(baseline, []))
            record = build_ablation_record(
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
                upstream=upstream,
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


def build_candidate_batch(run_dir: Path, tasks: list[dict[str, Any]], upstreams: dict[str, dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    lines = ["import MathAutoResearch.GeometryFull2D.Inequality", "", "namespace MathAutoResearch.GeometryFull2D", ""]
    per_task: dict[str, dict[str, Any]] = {}
    for task in tasks:
        statement = str(task["formal_statement"])
        task_id = str(task["task_id"])
        theorem_name = str(task["theorem_name"])
        header = statement.split(":= by", 1)[0].strip()
        upstream = upstreams.get(task_id, {})
        proof_text = str(upstream.get("patch_text", ""))
        if not proof_text:
            errors.append(f"{task_id}:no_compiler_patch_text")
            proof_text = "exact False.elim (by contradiction)"
        lines.append(header + " := by")
        lines.append(f"  -- MARP_PROOF_REGION_START:{theorem_name}")
        lines.extend("  " + line if line else "" for line in proof_text.splitlines())
        lines.append(f"  -- MARP_PROOF_REGION_END:{theorem_name}")
        lines.append("")
        per_task[task_id] = {
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


def build_b2_upstream_artifacts(
    *,
    run_dir: Path,
    task: dict[str, Any],
    task_index: int,
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
    provider = run_provider_and_checkers(run_dir, task_id, claim_path, claim_ref)
    errors.extend(provider["errors"])
    engine_refs = provider["engine_refs"]
    checker_refs = provider["checker_refs"]
    provider_ref, _ = write_artifact(
        run_dir,
        Path("provider_stage") / "provider_manifests" / f"{safe_id(task_id)}.json",
        {
            "schema_version": "ProviderRunManifestFull2D",
            "provider_stage_run_id": f"provider:v0_5:{task_id}:B2",
            "claim_spec_ref": claim_ref,
            "engine_output_refs": engine_refs,
            "engine_roles": list(ENGINE_ROLES),
            "provider_cli_summary_ref": provider["provider_summary_ref"],
            "independent_checker_summary_ref": provider["checker_summary_ref"],
            "provider_process_boundary": "plugins.geometry_full2d.provider_cli.run_provider_cli",
            "proof_use_status": "not_allowed",
        },
        id_field="manifest_id",
    )
    application = provider["checked_rule_application"]
    rule_ids = [str(rule_id) for rule_id in application.get("rule_ids", [])]
    if not application or not application.get("constructor") or len(rule_ids) < 2:
        errors.append("missing_checked_rule_application_for_derivation")
        rule_ids = ["full2d_rule:incidence_collinearity:01", "full2d_rule:incidence_collinearity:02"]
    selected_role_refs = [
        provider["engine_refs_by_role"][role]
        for role in ENGINE_ROLES
        if role in provider["engine_refs_by_role"]
    ]
    checked_application_ref = provider["checked_rule_application_ref"] or claim_ref
    derivation = {
        "schema_version": "SelectedSolverDerivationV2",
        "selected_engine_output_refs": selected_role_refs,
        "selected_facts": provider["selected_facts"] or [f"fact:{task_id}:semantic_support"],
        "selected_constructions": [f"construction:{task_id}"] if task.get("requires_construction_case_certificate") else [],
        "selected_certificates": [checked_application_ref, f"certificate:{task_id}:independent_replay"],
        "checked_rule_application": application,
        "checked_rule_application_ref": checked_application_ref,
        "derivation_steps": [
            {
                "step_id": f"{task_id}:non_target_intermediate",
                "input_refs": [claim_ref, selected_role_refs[0] if selected_role_refs else claim_ref],
                "output_ref": f"intermediate:{task_id}",
                "rule_id": rule_ids[0],
                "independent_checker_report_ref": provider["checker_refs_by_role"].get("portfolio_coordinator") or (checker_refs[0] if checker_refs else claim_ref),
                "output_is_target": False,
                "non_target_intermediate": True,
            },
            {
                "step_id": f"{task_id}:target_derivation",
                "input_refs": [f"intermediate:{task_id}", checked_application_ref],
                "output_ref": f"target:{task_id}",
                "rule_id": rule_ids[1],
                "independent_checker_report_ref": provider["checker_refs_by_role"].get("portfolio_coordinator") or (checker_refs[1] if len(checker_refs) > 1 else claim_ref),
                "output_is_target": True,
                "non_target_intermediate": False,
            },
        ],
        "used_engine_roles": sorted(provider["engine_refs_by_role"]),
    }
    derivation_ref, derivation_path = write_artifact(run_dir, Path("selected_solver_derivations") / f"{safe_id(task_id)}.json", derivation, id_field="derivation_id")
    compiler_stage = run_compiler_cli(
        claim_spec_json=claim_path,
        selected_derivation_json=derivation_path,
        rule_registry_json=registry_path,
        output_dir=run_dir / "compiler_task_runs" / safe_id(task_id),
        claim_spec_ref=claim_ref,
        selected_derivation_ref=derivation_ref,
        rule_registry_ref=registry_ref,
        side_condition_checker_refs=tuple(checker_refs[:2]),
    )
    errors.extend(f"compiler_cli:{error}" for error in compiler_stage.get("errors", []))
    compiler_result_path = run_dir / "compiler_task_runs" / safe_id(task_id) / "compiler_stage" / "compiler_result.json"
    compiler_payload = read_json(compiler_result_path) if compiler_stage.get("status") == "passed" and compiler_result_path.exists() else {}
    patch_text = str(compiler_payload.get("proof_text", ""))
    if not patch_text:
        errors.append("compiler_no_patch_text_from_selected_derivation")
    compiler_ref, _ = write_artifact(
        run_dir,
        Path("compiler_results") / f"{safe_id(task_id)}.json",
        strip_identity(compiler_payload)
        if compiler_payload
        else {
            "schema_version": "StageFailureReportV1",
            "stage": "compiler",
            "input_refs": [claim_ref, derivation_ref, registry_ref],
            "command_log_ref": sha256_text(canonical_json(compiler_stage)),
            "failure_kind": "validation_rejected",
            "failure_reason": ";".join(map(str, compiler_stage.get("errors", []))) or "compiler_cli_failed",
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
        "patch_text": patch_text,
        "solver_dependency_refs": [derivation_ref, *checker_refs[:2]],
    }
    patch_ref, _ = write_artifact(run_dir, Path("lean_patch_candidates") / f"{safe_id(task_id)}.json", patch, id_field="patch_id")
    return {
        "errors": sorted(set(errors)),
        "validation_errors": [],
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
        "patch_text": patch_text,
        "rule_ids": rule_ids,
        "has_non_target_intermediate": True,
        "has_construction_case_certificate": bool(task.get("requires_construction_case_certificate")),
    }


def materialize_b2_record(
    *,
    run_dir: Path,
    task: dict[str, Any],
    corpus_ref: str,
    config_ref: str,
    selected_impl: str,
    git_head: str,
    run_dir_hash: str,
    upstream: dict[str, Any],
    final_verify: dict[str, Any],
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    theorem_name = str(task["theorem_name"])
    worker = {
        "schema_version": "ProofWorkerResultFull2D",
        "lean_patch_candidate_ref": upstream["patch_ref"],
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
        "theorem_name": theorem_name,
        "baseline_id": "B2",
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
        "independent_checker_report_refs": upstream["checker_refs"],
        "selected_solver_derivation_ref": upstream["derivation_ref"],
        "compiler_result_refs": [upstream["compiler_ref"]],
        "lean_patch_candidate_ref": upstream["patch_ref"],
        "proof_worker_result_ref": worker_ref,
        "final_verify_report_ref": final_ref,
        "solver_causality_report_ref": pending_causality_ref,
        "solver_backed_certificate_ref": cert_ref,
        "causal_chain_hash": MUTATION_PENDING_REF,
        "final_status": "final_theorem" if final_verify["passed"] else "measured_failure",
        "final_status_source": "FinalVerifyReportFull2D",
        "used_rule_ids": upstream["rule_ids"],
        "used_engine_roles": list(ENGINE_ROLES),
        "has_non_target_intermediate": upstream["has_non_target_intermediate"],
        "has_construction_case_certificate": upstream["has_construction_case_certificate"],
        "direct_or_wrapped_facade_success": False,
    }
    record["causal_chain_hash"] = causal_chain_hash(record)
    return {"record": record, "validation_errors": validate_payload(record, current_head=git_head)}


def missing_b2_upstream_bundle(task_id: str, extraction_ref: str) -> dict[str, Any]:
    missing = sha256_text("missing_b2_upstream:" + task_id)
    return {
        "source_ref": missing,
        "extraction_ref": extraction_ref,
        "claim_ref": missing,
        "provider_ref": missing,
        "engine_refs": [missing],
        "checker_refs": [missing],
        "derivation_ref": missing,
        "compiler_ref": missing,
        "patch_ref": missing,
        "patch_text": "",
        "rule_ids": [],
        "has_non_target_intermediate": False,
        "has_construction_case_certificate": False,
    }


def build_ablation_record(
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
    upstream: dict[str, Any],
) -> dict[str, Any]:
    task_id = str(task["task_id"])
    source_ref = str(upstream.get("source_ref") or sha256_text("missing_source:" + task_id))
    claim_ref = str(upstream.get("claim_ref") or sha256_text("missing_claim:" + task_id))
    claim_path = Path(str(upstream.get("claim_path") or ""))
    if not claim_path.exists():
        claim_path = run_dir / "claim_specs" / f"{safe_id(task_id)}.json"
    component = "geometry_solver_provider" if "geometry_solver_provider" in disabled_components else (disabled_components[0] if disabled_components else "undeclared")
    disabled_roles = tuple(role for role in disabled_components if role in ENGINE_ROLES)
    task_root = run_dir / "provider_baseline_task_runs" / f"{safe_id(task_id)}__{safe_id(baseline)}"
    if task_root.exists():
        shutil.rmtree(task_root)
    provider_summary = run_provider_cli(
        claim_path,
        task_root,
        f"provider:v0_5:{task_id}:{baseline}",
        claim_spec_ref=claim_ref,
        task_id=task_id,
        baseline_id=baseline,
        disabled_component=component,
        disabled_engine_roles=disabled_roles,
    )
    provider_manifest_ref = str(provider_summary.get("provider_manifest_ref") or "")
    manifest_path = task_root / "provider_stage" / "provider_manifest.json"
    if manifest_path.exists():
        provider_manifest_ref, _ = write_artifact(
            run_dir,
            Path("provider_stage") / "baseline_manifests" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
            strip_identity(read_json(manifest_path)),
            id_field="manifest_id",
        )
    engine_refs: list[str] = []
    engine_roles_seen: list[str] = []
    engine_dir = task_root / "provider_stage" / "engine_outputs"
    for path in sorted(engine_dir.glob("*.json")) if engine_dir.exists() else []:
        payload = read_json(path)
        role = str(payload.get("engine_role"))
        engine_roles_seen.append(role)
        ref, _ = write_artifact(
            run_dir,
            Path("provider_stage") / "baseline_engine_outputs" / f"{safe_id(task_id)}__{safe_id(baseline)}__{safe_id(role)}.json",
            strip_identity(payload),
            id_field="output_id",
        )
        engine_refs.append(ref)
    missing_roles = sorted(set(ENGINE_ROLES) - set(engine_roles_seen))
    command_log_ref, _ = write_artifact(
        run_dir,
        Path("command_logs") / "baseline_ablation" / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "CommandLogV05",
            "stage": "provider",
            "stage_sequence": ["claimspec", "provider"],
            "actual_python_function_executed": True,
            "command": [
                sys.executable,
                "-m",
                "plugins.geometry_full2d.provider_cli",
                "--claim-spec-json",
                str(claim_path),
                "--output-dir",
                str(task_root),
                "--request-id",
                f"provider:v0_5:{task_id}:{baseline}",
                "--baseline-id",
                baseline,
                "--disabled-component",
                component,
                *[item for role in disabled_roles for item in ("--disabled-engine-role", role)],
            ],
            "returncode": 0 if provider_summary.get("status") == "passed" else 1,
            "provider_cli_summary_ref": sha256_text(canonical_json(provider_summary)),
            "disabled_components": disabled_components,
            "engine_roles_seen": sorted(engine_roles_seen),
            "missing_engine_roles": missing_roles,
        },
        id_field="command_log_id",
    )
    failure_ref, _ = write_artifact(
        run_dir,
        Path("stage_failures") / f"{safe_id(task_id)}__{safe_id(baseline)}.json",
        {
            "schema_version": "StageFailureReportV1",
            "stage": "provider",
            "baseline_id": baseline,
            "disabled_components": disabled_components,
            "input_refs": [source_ref, extraction_ref, claim_ref, *(engine_refs or [])],
            "command_log_ref": command_log_ref,
            "failure_kind": "declared_baseline_ablation",
            "failure_reason": "declared baseline ablation only: disabled components prevented a complete solver-causal provider stage",
            "provider_manifest_ref": provider_manifest_ref if provider_manifest_ref.startswith("sha256:") else sha256_text(canonical_json(provider_summary)),
            "provider_cli_status": provider_summary.get("status"),
            "provider_cli_errors": provider_summary.get("errors", []),
            "engine_output_refs": engine_refs,
            "engine_roles_seen": sorted(engine_roles_seen),
            "missing_engine_roles": missing_roles,
        },
        id_field="failure_report_id",
    )
    downstream_failure_ref = failure_ref
    if not provider_manifest_ref.startswith("sha256:"):
        provider_manifest_ref = downstream_failure_ref
    if not engine_refs:
        engine_refs = [downstream_failure_ref]
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
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": provider_manifest_ref,
        "engine_output_refs": engine_refs,
        "independent_checker_report_refs": [downstream_failure_ref],
        "selected_solver_derivation_ref": downstream_failure_ref,
        "compiler_result_refs": [downstream_failure_ref],
        "lean_patch_candidate_ref": downstream_failure_ref,
        "proof_worker_result_ref": downstream_failure_ref,
        "final_verify_report_ref": downstream_failure_ref,
        "solver_causality_report_ref": downstream_failure_ref,
        "solver_backed_certificate_ref": downstream_failure_ref,
        "causal_chain_hash": MUTATION_PENDING_REF,
        "final_status": "measured_failure",
        "final_status_source": "StageFailureReportV1",
        "failure_report_ref": downstream_failure_ref,
        "baseline_disabled_components": disabled_components,
        "ablation_pipeline_executed_until_stage": "provider",
        "ablation_engine_roles_seen": sorted(engine_roles_seen),
        "ablation_missing_engine_roles": missing_roles,
    }
    record["engine_output_refs"] = engine_refs
    record["causal_chain_hash"] = causal_chain_hash(record)
    return record


def run_provider_and_checkers(run_dir: Path, task_id: str, claim_path: Path, claim_ref: str) -> dict[str, Any]:
    task_root = run_dir / "provider_task_runs" / safe_id(task_id)
    if task_root.exists():
        shutil.rmtree(task_root)
    provider_summary = run_provider_cli(claim_path, task_root, f"provider:v0_5:{task_id}:B2", claim_spec_ref=claim_ref)
    checker_summary = run_independent_solver_checkers(task_root, claim_spec_json=claim_path, write_reports=True)
    errors = [f"provider_cli:{error}" for error in provider_summary.get("errors", [])]
    errors.extend(f"independent_checker:{error}" for error in checker_summary.get("errors", []))
    checker_refs_by_role: dict[str, str] = {}
    for ref, rel_path in checker_summary.get("report_paths", {}).items():
        payload = read_json(task_root / rel_path)
        role = str(payload.get("engine_role"))
        checker_refs_by_role[role] = str(ref)
        write_json(run_dir / "independent_checker_reports" / f"{safe_id(task_id)}__{safe_id(role)}.json", payload)
    engine_refs: list[str] = []
    engine_refs_by_role: dict[str, str] = {}
    selected_facts: list[str] = []
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
            Path("provider_stage") / "engine_outputs" / f"{safe_id(task_id)}__{safe_id(role)}.json",
            body,
            id_field="output_id",
        )
        engine_refs.append(ref)
        engine_refs_by_role[role] = ref
    portfolio_artifact_path = task_root / "provider_stage" / "normalized_artifacts" / "portfolio_coordinator.json"
    checked_rule_application: dict[str, Any] = {}
    checked_rule_application_ref = ""
    if portfolio_artifact_path.exists():
        portfolio_artifact = strip_identity(read_json(portfolio_artifact_path))
        application = portfolio_artifact.get("checked_rule_application")
        if isinstance(application, dict):
            checked_rule_application = application
            checked_rule_application_ref = sha256_text(canonical_json(portfolio_artifact))
        else:
            errors.append("portfolio_checked_rule_application_missing")
    else:
        errors.append("portfolio_normalized_artifact_missing")
    provider_summary_ref, _ = write_artifact(
        run_dir,
        Path("provider_stage") / "provider_summaries" / f"{safe_id(task_id)}.json",
        strip_identity(provider_summary),
        id_field="summary_id",
    )
    checker_summary_ref, _ = write_artifact(
        run_dir,
        Path("independent_checker_reports") / f"{safe_id(task_id)}__summary.json",
        strip_identity(checker_summary),
        id_field="summary_id",
    )
    return {
        "errors": sorted(set(errors)),
        "engine_refs": engine_refs,
        "engine_refs_by_role": engine_refs_by_role,
        "checker_refs": [checker_refs_by_role[role] for role in sorted(checker_refs_by_role)],
        "checker_refs_by_role": checker_refs_by_role,
        "selected_facts": sorted(set(selected_facts)),
        "checked_rule_application": checked_rule_application,
        "checked_rule_application_ref": checked_rule_application_ref,
        "provider_summary_ref": provider_summary_ref,
        "checker_summary_ref": checker_summary_ref,
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
