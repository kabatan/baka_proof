#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_compiler import (
    EXACT_COMPILE_INPUTS,
    compile_derivation,
    compiler_code_hash,
)
from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_proof_worker import (
    apply_lean_patch_candidate_v0_6,
    build_solver_backed_certificate_v0_6,
    file_sha256,
    final_verify_gate_v0_6,
    proof_worker_code_hash,
    run_lake_env_lean,
)
from scripts.geometry_full2d_v0_6_schemas import current_git_head, sha256_text


ACTUAL_TASK_RUN_DIRS = ("actual_task_pipeline_runs_v0_6", "actual_task_pipeline_runs")
CAUSALITY_REPORT_DIR = "solver_causality_live_runs_v0_6"
CAUSALITY_TEMP_DIR = "solver_causality_live_temp_v0_6"
COMMAND_LOG_DIR = Path("command_logs") / "solver_causality_live_v0_6"
CAUSALITY_BATCH_DIR = "solver_causality_live_final_verify_batches_v0_6"
COMPILER_RESULT_DIR = "compiler_results_v0_6"
LEAN_PATCH_DIR = "lean_patch_candidates_v0_6"
PROOF_WORKER_RESULT_DIR = "proof_worker_results_v0_6"
FINAL_VERIFY_REPORT_DIR = "final_verify_reports_v0_6"
SOLVER_BACKED_CERTIFICATE_DIR = "solver_backed_certificates_v0_6"

MUTATION_KINDS = [
    "positive_control",
    "remove_selected_artifact",
    "corrupt_non_target_intermediate",
    "corrupt_construction_or_certificate",
    "unsupported_rule_mutation",
    "side_condition_mutation",
    "remove_checker_transcript",
]

ID_KEYS = {
    "report_id",
    "claim_id",
    "provider_manifest_id",
    "engine_output_id",
    "check_id",
    "derivation_id",
    "match_report_id",
    "compiler_result_id",
    "patch_id",
    "worker_result_id",
    "verify_report_id",
    "certificate_id",
    "anchor_ref",
    "snapshot_ref",
}


class CausalityInputError(RuntimeError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    parser.add_argument("--all-b2-successes", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", required=False)
    args = parser.parse_args()

    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "wp11_self_test_run"
            build_self_test_run(run_dir)
            report = run_solver_causality_live(run_dir, all_b2_successes=True)
    else:
        if not args.run_dir:
            parser.error("--run-dir is required unless --self-test is used")
        report = run_solver_causality_live(Path(args.run_dir), all_b2_successes=args.all_b2_successes)

    if args.output:
        write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("status") == "passed" else 1


def run_solver_causality_live(run_dir: Path, *, all_b2_successes: bool) -> dict[str, Any]:
    run_dir = resolve_path(run_dir)
    errors: list[str] = []
    if not all_b2_successes:
        errors.append("all_b2_successes_flag_required")

    records = load_b2_success_records(run_dir)
    ref_index = build_ref_index(run_dir)
    report_dir = run_dir / CAUSALITY_REPORT_DIR
    temp_root = run_dir / CAUSALITY_TEMP_DIR
    command_root = run_dir / COMMAND_LOG_DIR
    batch_root = run_dir / CAUSALITY_BATCH_DIR
    for path in (temp_root, report_dir, command_root, batch_root):
        if path.exists():
            shutil.rmtree(path)
    temp_root.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    command_root.mkdir(parents=True, exist_ok=True)
    batch_root.mkdir(parents=True, exist_ok=True)

    task_states: list[dict[str, Any]] = []
    case_states: list[dict[str, Any]] = []
    for record_path, record, record_ref in records:
        state = prepare_b2_success_record(
            run_dir=run_dir,
            ref_index=ref_index,
            record_path=record_path,
            record=record,
            source_actual_run_ref=record_ref,
        )
        task_states.append(state)
        case_states.extend(state.get("case_states", []))

    run_causality_final_verify_batches(run_dir, case_states)

    reports: list[dict[str, Any]] = []
    task_results: list[dict[str, Any]] = []
    for state in task_states:
        result = finalize_b2_success_record(run_dir=run_dir, state=state)
        task_results.append(result)
        reports.append(result["report"])
        errors.extend(f"{state.get('task_id', state.get('source_actual_run_ref'))}:{error}" for error in result.get("errors", []))

    summary = {
        "schema_version": "RunSolverCausalityLiveV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "all_b2_successes": all_b2_successes,
        "b2_success_count": len(records),
        "causality_report_count": len(reports),
        "mutation_case_count": sum(len(report.get("mutation_cases", [])) for report in reports),
        "not_applicable_no_b2_successes": len(records) == 0,
        "report_paths": [
            (run_dir / CAUSALITY_REPORT_DIR / f"{safe_path_part(str(result.get('task_id')))}.json").relative_to(run_dir).as_posix()
            for result in task_results
        ],
        "task_results": sorted(task_results, key=lambda item: str(item.get("task_id")))[:50],
        "git_head": current_git_head(),
    }
    write_json(run_dir / "solver_causality_live_summary_v0_6.json", summary)
    return summary


def prepare_b2_success_record(
    *,
    run_dir: Path,
    ref_index: dict[str, tuple[Path, dict[str, Any]]],
    record_path: Path,
    record: dict[str, Any],
    source_actual_run_ref: str,
) -> dict[str, Any]:
    task_id = str(record.get("task_id") or record_path.stem)
    errors: list[str] = []
    case_states: list[dict[str, Any]] = []
    try:
        inputs = reconstruct_inputs(run_dir, ref_index, record)
    except CausalityInputError as exc:
        inputs = None
        errors.append(str(exc))

    if inputs is not None:
        for mutation_kind in MUTATION_KINDS:
            case = prepare_mutation_case(
                run_dir=run_dir,
                source_actual_run_ref=source_actual_run_ref,
                task_id=task_id,
                baseline_id=str(record.get("baseline_id", "B2")),
                mutation_kind=mutation_kind,
                inputs=inputs,
            )
            case_states.append(case)
            errors.extend(f"{mutation_kind}:{error}" for error in case.get("prepare_errors", []))

    return {
        "task_id": task_id,
        "record_path": record_path,
        "record_path_rel": record_path.relative_to(run_dir).as_posix(),
        "baseline_id": str(record.get("baseline_id", "B2")),
        "source_actual_run_ref": source_actual_run_ref,
        "case_states": case_states,
        "errors": sorted(set(errors)),
    }


def finalize_b2_success_record(*, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    task_id = str(state.get("task_id"))
    errors: list[str] = list(state.get("errors", []))
    mutation_cases: list[dict[str, Any]] = []
    case_temp_refs: list[str] = []
    for case in state.get("case_states", []):
        mutation_kind = str(case.get("mutation_kind"))
        verify = case.get("final_verify_report")
        verify_path = case.get("final_verify_report_path")
        final_verify_status = str(verify.get("status", "not_run")) if isinstance(verify, dict) else "not_run"
        counted_same_final_theorem = final_verify_status == "passed"
        if mutation_kind == "positive_control":
            if not counted_same_final_theorem:
                errors.append(f"{mutation_kind}:positive_control_did_not_reproduce_final_theorem")
        else:
            if counted_same_final_theorem:
                errors.append(f"{mutation_kind}:mutation_produced_same_counted_final_theorem")

        command_log, command_log_ref = build_command_log(
            run_dir=run_dir,
            temp_dir=Path(str(case.get("temp_dir"))),
            task_id=task_id,
            baseline_id=str(state.get("baseline_id", "B2")),
            source_actual_run_ref=str(state.get("source_actual_run_ref")),
            mutation_kind=mutation_kind,
            input_artifact_set_hash=str(case.get("input_artifact_set_hash")),
            output_patch_hash=str(case.get("output_patch_hash")),
            compiler_status=str(case.get("compiler_status")),
            compiler_error=case.get("compiler_error"),
            proof_worker_result=case.get("worker") if isinstance(case.get("worker"), dict) else {},
            final_verify_report=verify if isinstance(verify, dict) else None,
            final_verify_report_path=verify_path if isinstance(verify_path, Path) else None,
        )
        command_log_path = run_dir / COMMAND_LOG_DIR / f"{safe_path_part(task_id)}__{safe_path_part(mutation_kind)}.json"
        write_json(command_log_path, command_log)
        mutation_cases.append(
            {
                "mutation_kind": mutation_kind,
                "command_log_ref": command_log_ref,
                "input_artifact_set_hash": case.get("input_artifact_set_hash"),
                "output_patch_hash": case.get("output_patch_hash"),
                "final_verify_status": final_verify_status,
                "counted_same_final_theorem": counted_same_final_theorem,
            }
        )
        case_temp_refs.append(str(case.get("temp_run_dir_ref")))
        errors.extend(f"{mutation_kind}:{error}" for error in case.get("verify_errors", []))

    unsigned = {
        "schema_version": "SolverCausalityLiveRunV1",
        "source_actual_run_ref": state.get("source_actual_run_ref"),
        "temp_run_dir_ref": sha256_text(canonical_json(case_temp_refs)),
        "mutation_cases": mutation_cases,
        "status": "passed" if not errors else "failed",
        "git_head": current_git_head(),
    }
    report = {"report_id": sha256_text(canonical_json(unsigned)), **unsigned}
    report_path = run_dir / CAUSALITY_REPORT_DIR / f"{safe_path_part(task_id)}.json"
    write_json(report_path, report)
    return {
        "task_id": task_id,
        "record_path": state.get("record_path_rel"),
        "source_actual_run_ref": state.get("source_actual_run_ref"),
        "status": report["status"],
        "errors": sorted(set(errors)),
        "report": report,
        "report_ref": file_sha256(report_path),
        "mutation_case_count": len(mutation_cases),
    }


def reconstruct_inputs(
    run_dir: Path,
    ref_index: dict[str, tuple[Path, dict[str, Any]]],
    record: dict[str, Any],
) -> dict[str, Any]:
    selected_path, selected_derivation = resolve_ref(ref_index, str(record.get("selected_solver_derivation_ref")), "selected_solver_derivation_ref")
    compiler_refs = record.get("compiler_result_refs")
    if not isinstance(compiler_refs, list) or not compiler_refs:
        raise CausalityInputError("missing_compiler_result_refs")
    compiler_path, compiler_result = resolve_ref(ref_index, str(compiler_refs[0]), "compiler_result_refs[0]")
    anchor_path, theorem_anchor = resolve_ref(ref_index, str(compiler_result.get("theorem_anchor_ref")), "compiler_result.theorem_anchor_ref")
    registry_path, rule_registry_snapshot = resolve_ref(ref_index, str(compiler_result.get("rule_registry_snapshot_ref")), "compiler_result.rule_registry_snapshot_ref")
    side_reports: list[dict[str, Any]] = []
    side_paths: list[Path] = []
    for index, side_ref in enumerate(compiler_result.get("side_condition_report_refs", [])):
        path, payload = resolve_ref(ref_index, str(side_ref), f"side_condition_report_refs[{index}]")
        side_paths.append(path)
        side_reports.append(payload)
    source_path = resolve_source_path(theorem_anchor)
    if not source_path.exists():
        raise CausalityInputError(f"source_theorem_file_missing:{source_path}")
    return {
        "selected_path": selected_path,
        "selected_derivation": selected_derivation,
        "compiler_path": compiler_path,
        "compiler_result": compiler_result,
        "anchor_path": anchor_path,
        "theorem_anchor": theorem_anchor,
        "registry_path": registry_path,
        "rule_registry_snapshot": rule_registry_snapshot,
        "side_paths": side_paths,
        "side_condition_reports": side_reports,
        "source_path": source_path,
    }


def prepare_mutation_case(
    *,
    run_dir: Path,
    source_actual_run_ref: str,
    task_id: str,
    baseline_id: str,
    mutation_kind: str,
    inputs: dict[str, Any],
) -> dict[str, Any]:
    temp_dir = run_dir / CAUSALITY_TEMP_DIR / safe_path_part(task_id) / safe_path_part(mutation_kind)
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    source_path = Path(inputs["source_path"])
    theorem_anchor = dict(inputs["theorem_anchor"])
    selected_derivation = mutate_selected_derivation(dict_deepcopy(inputs["selected_derivation"]), mutation_kind)
    rule_registry_snapshot = mutate_rule_registry_snapshot(dict_deepcopy(inputs["rule_registry_snapshot"]), mutation_kind)
    side_reports = [dict_deepcopy(report) for report in inputs["side_condition_reports"]]
    side_reports = mutate_side_condition_reports(side_reports, mutation_kind)

    write_json(temp_dir / "inputs" / "theorem_anchor.json", theorem_anchor)
    write_json(temp_dir / "inputs" / "selected_solver_derivation.json", selected_derivation)
    write_json(temp_dir / "inputs" / "rule_registry_snapshot.json", rule_registry_snapshot)
    for index, report in enumerate(side_reports):
        write_json(temp_dir / "inputs" / "side_condition_reports" / f"{index:02d}.json", report)

    input_artifact_set_hash = hash_case_inputs(source_path, theorem_anchor, selected_derivation, rule_registry_snapshot, side_reports)
    compiler_status = "not_run"
    compiler_error: str | None = None
    try:
        patch_candidate, compiler_result, compiler_ref, patch_ref = compile_case(
            temp_dir=temp_dir,
            theorem_anchor=theorem_anchor,
            selected_derivation=selected_derivation,
            rule_registry_snapshot=rule_registry_snapshot,
            side_reports=side_reports,
        )
        compiler_status = "passed"
    except Exception as exc:
        compiler_error = str(exc)
        compiler_status = "failed"
        compiler_result = build_compiler_failure_result(theorem_anchor, selected_derivation, rule_registry_snapshot, side_reports, compiler_error)
        compiler_path = temp_dir / COMPILER_RESULT_DIR / "compiler_failure.json"
        write_json(compiler_path, compiler_result)
        compiler_ref = sha256_text(canonical_json(compiler_result))
        patch_candidate = build_failure_patch(theorem_anchor, compiler_ref, compiler_error)
        patch_path = temp_dir / LEAN_PATCH_DIR / "fallback_failure_patch.json"
        write_json(patch_path, patch_candidate)
        patch_ref = file_sha256(patch_path)

    output_patch_hash = patch_ref
    worker = apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=theorem_anchor,
        patch_candidate=patch_candidate,
        output_dir=temp_dir,
        run_id=mutation_kind,
    )
    worker_path = temp_dir / PROOF_WORKER_RESULT_DIR / "proof_worker_result.json"
    write_json(worker_path, worker)
    candidate_path = Path(str(worker.get("generated_candidate_path") or ""))
    if not candidate_path.exists():
        errors.append("proof_worker_did_not_generate_candidate")

    return {
        "task_id": task_id,
        "baseline_id": baseline_id,
        "source_actual_run_ref": source_actual_run_ref,
        "mutation_kind": mutation_kind,
        "temp_dir": temp_dir,
        "source_path": source_path,
        "theorem_anchor": theorem_anchor,
        "worker": worker,
        "worker_path": worker_path,
        "candidate_path": candidate_path if candidate_path.exists() else None,
        "input_artifact_set_hash": input_artifact_set_hash,
        "output_patch_hash": output_patch_hash,
        "compiler_status": compiler_status,
        "compiler_error": compiler_error,
        "temp_run_dir_ref": sha256_text(canonical_json({"temp_dir": str(temp_dir), "input_hash": input_artifact_set_hash, "patch_hash": output_patch_hash})),
        "prepare_errors": sorted(set(errors)),
        "verify_errors": [],
    }


def causality_final_verify_batch_size() -> int:
    return max(1, int(os.environ.get("FULL2D_CAUSALITY_FINAL_VERIFY_BATCH_SIZE", "40")))


def causality_final_verify_batch_workers() -> int:
    return max(1, int(os.environ.get("FULL2D_CAUSALITY_FINAL_VERIFY_BATCH_WORKERS", "4")))


def run_causality_final_verify_batches(run_dir: Path, case_states: list[dict[str, Any]]) -> None:
    candidate_states = [case for case in case_states if isinstance(case.get("candidate_path"), Path)]
    batch_size = causality_final_verify_batch_size()
    batch_workers = causality_final_verify_batch_workers()
    batches: list[tuple[int, str, list[dict[str, Any]]]] = []
    batch_index = 0
    for mutation_kind in MUTATION_KINDS:
        rows = [case for case in candidate_states if case.get("mutation_kind") == mutation_kind]
        for index in range(0, len(rows), batch_size):
            batches.append((batch_index, mutation_kind, rows[index : index + batch_size]))
            batch_index += 1
    if not batches:
        return
    batch_rows_by_index = {batch_index: rows for batch_index, _mutation_kind, rows in batches}
    with ThreadPoolExecutor(max_workers=batch_workers) as executor:
        futures = {
            executor.submit(run_one_causality_final_verify_batch, run_dir, batch_index, mutation_kind, rows): batch_index
            for batch_index, mutation_kind, rows in batches
        }
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:  # pragma: no cover - release evidence defensive path.
                batch_index = futures[future]
                for case in batch_rows_by_index.get(batch_index, []):
                    if case.get("final_verify_report") is None:
                        case.setdefault("verify_errors", []).append(f"final_verify_batch_{batch_index}_exception:{exc}")


def run_one_causality_final_verify_batch(run_dir: Path, batch_index: int, mutation_kind: str, case_states: list[dict[str, Any]]) -> None:
    if not case_states:
        return
    batch_path = write_causality_final_verify_batch_source(run_dir, batch_index, mutation_kind, case_states)
    batch_ref = file_sha256(batch_path)
    lean = run_lake_env_lean(batch_path, timeout_sec=max(180, len(case_states) * 30))
    if mutation_kind == "positive_control" and lean.get("returncode") != 0:
        for case in case_states:
            verify_case_state(run_dir, case, lean_result=None, batch_path=None, batch_ref=None)
        return
    for case in case_states:
        verify_case_state(run_dir, case, lean_result=lean, batch_path=batch_path, batch_ref=batch_ref)


def write_causality_final_verify_batch_source(
    run_dir: Path,
    batch_index: int,
    mutation_kind: str,
    case_states: list[dict[str, Any]],
) -> Path:
    batch_dir = run_dir / CAUSALITY_BATCH_DIR
    batch_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "import MathAutoResearch.GeometryFull2D.RuleLemmas",
        "",
        "namespace MathAutoResearch.GeometryFull2D",
        "",
    ]
    for case in case_states:
        candidate_path = case.get("candidate_path")
        if not isinstance(candidate_path, Path):
            continue
        lines.append(f"-- causality_mutation_kind:{mutation_kind}")
        lines.append(f"-- causality_task_id:{safe_path_part(str(case.get('task_id')))}")
        lines.append(f"-- final_verify_batch_member:{candidate_path.as_posix()}")
        lines.append(f"-- final_verify_candidate_ref:{file_sha256(candidate_path)}")
        lines.append(candidate_theorem_body_for_batch(candidate_path))
        lines.append("")
    lines.append("end MathAutoResearch.GeometryFull2D")
    path = batch_dir / f"{batch_index:04d}__{safe_path_part(mutation_kind)}.lean"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def candidate_theorem_body_for_batch(candidate_path: Path) -> str:
    rows: list[str] = []
    for line in candidate_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            continue
        if stripped == "namespace MathAutoResearch.GeometryFull2D":
            continue
        if stripped == "end MathAutoResearch.GeometryFull2D":
            continue
        rows.append(line)
    return "\n".join(rows).strip() + "\n"


def verify_case_state(
    run_dir: Path,
    case: dict[str, Any],
    *,
    lean_result: dict[str, Any] | None,
    batch_path: Path | None,
    batch_ref: str | None,
) -> None:
    candidate_path = case.get("candidate_path")
    if not isinstance(candidate_path, Path):
        case.setdefault("verify_errors", []).append("final_verify_candidate_missing")
        return
    verify = final_verify_gate_v0_6(
        source_path=Path(str(case["source_path"])),
        candidate_path=candidate_path,
        theorem_anchor=case["theorem_anchor"],
        proof_worker_result=case["worker"],
        output_dir=Path(str(case["temp_dir"])),
        lean_result=lean_result,
        batch_source_path=batch_path,
        batch_source_ref=batch_ref,
    )
    verify_path = Path(str(case["temp_dir"])) / FINAL_VERIFY_REPORT_DIR / "final_verify_report.json"
    write_json(verify_path, verify)
    case["final_verify_report"] = verify
    case["final_verify_report_path"] = verify_path


def compile_case(
    *,
    temp_dir: Path,
    theorem_anchor: dict[str, Any],
    selected_derivation: dict[str, Any],
    rule_registry_snapshot: dict[str, Any],
    side_reports: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    enforce_checker_transcripts(selected_derivation)
    patch = compile_derivation(theorem_anchor, selected_derivation, rule_registry_snapshot, side_reports)
    patch_path = temp_dir / LEAN_PATCH_DIR / "lean_patch_candidate.json"
    write_json(patch_path, patch)
    preliminary_patch_ref = file_sha256(patch_path)
    compiler_unsigned = {
        "schema_version": "CompilerResultFull2D",
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "selected_derivation_ref": sha256_text(canonical_json(selected_derivation)),
        "rule_registry_snapshot_ref": sha256_text(canonical_json(rule_registry_snapshot)),
        "side_condition_report_refs": [sha256_text(canonical_json(report)) for report in side_reports],
        "lean_patch_candidate_ref": preliminary_patch_ref,
        "compiler_code_hash": compiler_code_hash(),
        "compile_inputs": EXACT_COMPILE_INPUTS,
        "compile_api_signature": "compile_derivation(theorem_anchor, selected_derivation, rule_registry_snapshot, side_condition_reports)",
        "proof_strategy_source": "selected_derivation_steps_and_rule_registry_only",
        "used_rule_ids_hash": sha256_text(canonical_json(patch.get("proof_plan", {}).get("used_rule_ids", []))),
        "patch_text_hash": patch.get("patch_text_hash"),
        "git_head": current_git_head(),
    }
    compiler_result = {"compiler_result_id": sha256_text(canonical_json(compiler_unsigned)), **compiler_unsigned}
    compiler_path = temp_dir / COMPILER_RESULT_DIR / "compiler_result.json"
    write_json(compiler_path, compiler_result)
    compiler_ref = file_sha256(compiler_path)
    patch["compiler_result_ref"] = compiler_ref
    patch["patch_id"] = sha256_text(
        canonical_json(
            {
                "compiler_result_ref": compiler_ref,
                "patch_text_hash": patch.get("patch_text_hash"),
                "proof_plan": patch.get("proof_plan"),
            }
        )
    )
    write_json(patch_path, patch)
    patch_ref = file_sha256(patch_path)
    return patch, compiler_result, compiler_ref, patch_ref


def enforce_checker_transcripts(selected_derivation: dict[str, Any]) -> None:
    steps = selected_derivation.get("selected_steps")
    if not isinstance(steps, list) or not steps:
        raise CausalityInputError("selected_derivation_has_no_steps")
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            raise CausalityInputError(f"selected_step_not_object:{index}")
        checker_ref = str(step.get("checker_ref", ""))
        if not checker_ref.startswith("sha256:"):
            raise CausalityInputError(f"selected_step_checker_transcript_missing:{index}")


def mutate_selected_derivation(selected: dict[str, Any], mutation_kind: str) -> dict[str, Any]:
    steps = selected.get("selected_steps")
    if not isinstance(steps, list):
        steps = []
    if mutation_kind == "remove_selected_artifact":
        selected["selected_steps"] = []
        selected["has_non_target_intermediate"] = False
    elif mutation_kind == "corrupt_non_target_intermediate":
        for step in steps:
            if not isinstance(step, dict) or step.get("is_final_target") is True:
                continue
            step["artifact_ref"] = sha256_text("corrupt_non_target_intermediate")
            step["conclusion"] = "corrupted_non_target_intermediate"
            premise_sources = step.get("premise_sources")
            if isinstance(premise_sources, list) and premise_sources:
                first = premise_sources[0]
                if isinstance(first, dict):
                    first["source_expr"] = "False"
                    first["source_expr_hash"] = sha256_text("False")
                    first["mutation_reason"] = "corrupt_non_target_intermediate_forces_lean_dependency_failure"
                    break
    elif mutation_kind == "corrupt_construction_or_certificate":
        selected["has_checked_side_condition_or_certificate"] = False
        for step in steps:
            if isinstance(step, dict):
                step["checked_side_conditions"] = []
                step["artifact_kind"] = "corrupted_certificate"
    elif mutation_kind == "unsupported_rule_mutation":
        for step in steps:
            if isinstance(step, dict):
                step["rule_id"] = "full2d_rule:unsupported_mutation:00"
    elif mutation_kind == "remove_checker_transcript":
        for step in steps:
            if isinstance(step, dict):
                step["checker_ref"] = "removed_checker_transcript"
    return selected


def mutate_rule_registry_snapshot(registry: dict[str, Any], mutation_kind: str) -> dict[str, Any]:
    if mutation_kind == "unsupported_rule_mutation":
        registry["unsupported_rule_mutation_applied"] = True
    return registry


def mutate_side_condition_reports(reports: list[dict[str, Any]], mutation_kind: str) -> list[dict[str, Any]]:
    if mutation_kind == "side_condition_mutation":
        if reports:
            reports[0]["status"] = "failed"
            reports[0]["mutation_reason"] = "side_condition_mutation"
        else:
            reports.append(
                {
                    "schema_version": "SideConditionReportV1",
                    "report_id": sha256_text("side_condition_mutation_missing_report"),
                    "status": "failed",
                    "git_head": current_git_head(),
                }
            )
    return reports


def build_compiler_failure_result(
    theorem_anchor: dict[str, Any],
    selected_derivation: dict[str, Any],
    rule_registry_snapshot: dict[str, Any],
    side_reports: list[dict[str, Any]],
    error: str,
) -> dict[str, Any]:
    body = {
        "schema_version": "CompilerFailureRerunV06",
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "selected_derivation_ref": sha256_text(canonical_json(selected_derivation)),
        "rule_registry_snapshot_ref": sha256_text(canonical_json(rule_registry_snapshot)),
        "side_condition_report_refs": [sha256_text(canonical_json(report)) for report in side_reports],
        "compiler_code_hash": compiler_code_hash(),
        "compile_inputs": EXACT_COMPILE_INPUTS,
        "failure_reason": error,
        "git_head": current_git_head(),
    }
    return {"compiler_failure_id": sha256_text(canonical_json(body)), **body}


def build_failure_patch(theorem_anchor: dict[str, Any], compiler_result_ref: str, reason: str) -> dict[str, Any]:
    patch_text = "  exact solverCausalityMutationFailed\n"
    body = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": compiler_result_ref,
        "patch_text_hash": sha256_text(patch_text),
        "patch_region": "MARP",
        "inside_marp_region": True,
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "patch_replacement_text": patch_text,
        "proof_plan_hash": sha256_text(canonical_json({"compiler_failure_reason": reason})),
        "proof_plan": {"compiler_failure_reason": reason},
        "patch_generation_source": "compiler_failure_fallback_for_live_causality_rerun",
        "mutates_theorem_statement": False,
        "git_head": current_git_head(),
    }
    return {"patch_id": sha256_text(canonical_json(body)), **body}


def build_command_log(
    *,
    run_dir: Path,
    temp_dir: Path,
    task_id: str,
    baseline_id: str,
    source_actual_run_ref: str,
    mutation_kind: str,
    input_artifact_set_hash: str,
    output_patch_hash: str,
    compiler_status: str,
    compiler_error: str | None,
    proof_worker_result: dict[str, Any],
    final_verify_report: dict[str, Any] | None,
    final_verify_report_path: Path | None,
) -> tuple[dict[str, Any], str]:
    final_verify_status = str(final_verify_report.get("status")) if isinstance(final_verify_report, dict) else "not_run"
    command = final_verify_report.get("lake_env_lean_command") if isinstance(final_verify_report, dict) else ["lake", "env", "lean", "<not-run>"]
    returncode = final_verify_report.get("lake_env_lean_returncode") if isinstance(final_verify_report, dict) else None
    body = {
        "schema_version": "SolverCausalityLiveCommandLogV06",
        "task_id": task_id,
        "baseline_id": baseline_id,
        "source_actual_run_ref": source_actual_run_ref,
        "mutation_kind": mutation_kind,
        "temp_run_dir": temp_dir.relative_to(run_dir).as_posix() if is_relative_to(temp_dir, run_dir) else str(temp_dir),
        "temp_run_dir_hash": directory_hash(temp_dir),
        "stage_sequence": ["compiler", "proof_worker", "final_verify"],
        "compiler_status": compiler_status,
        "compiler_error": compiler_error,
        "proof_worker_status": proof_worker_result.get("status"),
        "proof_worker_result_ref": sha256_text(canonical_json(proof_worker_result)),
        "final_verify_status": final_verify_status,
        "final_verify_report_ref": file_sha256(final_verify_report_path) if final_verify_report_path is not None and final_verify_report_path.exists() else None,
        "final_verify_report_path": final_verify_report_path.relative_to(run_dir).as_posix()
        if final_verify_report_path is not None and is_relative_to(final_verify_report_path, run_dir)
        else (str(final_verify_report_path) if final_verify_report_path is not None else None),
        "command": command,
        "returncode": returncode,
        "actual_subprocess_executed": isinstance(final_verify_report, dict),
        "input_artifact_set_hash": input_artifact_set_hash,
        "output_patch_hash": output_patch_hash,
        "candidate_ref": final_verify_report.get("patched_candidate_ref") if isinstance(final_verify_report, dict) else None,
        "proof_worker_code_hash": proof_worker_code_hash(),
        "git_head": current_git_head(),
    }
    command_log_ref = sha256_text(canonical_json(body))
    return {"command_log_id": command_log_ref, **body}, command_log_ref


def hash_case_inputs(
    source_path: Path,
    theorem_anchor: dict[str, Any],
    selected_derivation: dict[str, Any],
    rule_registry_snapshot: dict[str, Any],
    side_reports: list[dict[str, Any]],
) -> str:
    return sha256_text(
        canonical_json(
            {
                "source_file_ref": file_sha256(source_path),
                "theorem_anchor": theorem_anchor,
                "selected_derivation": selected_derivation,
                "rule_registry_snapshot": rule_registry_snapshot,
                "side_condition_reports": side_reports,
            }
        )
    )


def directory_hash(path: Path) -> str:
    rows: list[tuple[str, str]] = []
    if path.exists():
        for item in sorted(child for child in path.rglob("*") if child.is_file()):
            rows.append((item.relative_to(path).as_posix(), file_sha256(item)))
    return sha256_text(canonical_json(rows))


def load_b2_success_records(run_dir: Path) -> list[tuple[Path, dict[str, Any], str]]:
    rows: list[tuple[Path, dict[str, Any], str]] = []
    seen: set[Path] = set()
    for directory in ACTUAL_TASK_RUN_DIRS:
        root = run_dir / directory
        if not root.exists():
            continue
        for path in sorted(root.glob("*.json")):
            if path in seen:
                continue
            seen.add(path)
            payload = read_json(path)
            if not isinstance(payload, dict):
                continue
            if payload.get("schema_version") != "ActualTaskPipelineRunV4":
                continue
            if payload.get("baseline_id") == "B2" and payload.get("final_status") == "final_theorem":
                rows.append((path, payload, file_sha256(path)))
    return rows


def build_ref_index(run_dir: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    index: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(run_dir.rglob("*.json")):
        if CAUSALITY_TEMP_DIR in path.parts or CAUSALITY_REPORT_DIR in path.parts:
            continue
        try:
            payload = read_json(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        index[file_sha256(path)] = (path, payload)
        index[sha256_text(canonical_json(payload))] = (path, payload)
        for key in ID_KEYS:
            value = payload.get(key)
            if isinstance(value, str) and value.startswith("sha256:"):
                index[value] = (path, payload)
    return index


def resolve_ref(index: dict[str, tuple[Path, dict[str, Any]]], ref: str, label: str) -> tuple[Path, dict[str, Any]]:
    if ref in index:
        return index[ref]
    raise CausalityInputError(f"unresolved_content_ref:{label}:{ref}")


def resolve_source_path(theorem_anchor: dict[str, Any]) -> Path:
    source = Path(str(theorem_anchor.get("source_file_path", "")))
    return source if source.is_absolute() else ROOT / source


def build_self_test_run(run_dir: Path) -> None:
    run_dir = resolve_path(run_dir)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    source_path = run_dir / "self_test_source.lean"
    theorem_name = "wp11_self_test_line_circle"
    source_path.write_text(
        "\n".join(
            [
                "import MathAutoResearch.GeometryFull2D.RuleLemmas",
                "",
                "namespace MathAutoResearch.GeometryFull2D",
                "",
                f"theorem {theorem_name} (P : Point) (L : Line) (C : Circle) (h00 : line_circle_intersection P L C) : on_line P L := by",
                f"-- MARP_PROOF_REGION_START:{theorem_name}",
                "  sorry",
                f"-- MARP_PROOF_REGION_END:{theorem_name}",
                "",
                "end MathAutoResearch.GeometryFull2D",
                "",
            ]
        ),
        encoding="utf-8",
    )
    anchor = {
        "schema_version": "TheoremAnchorV1",
        "theorem_name": theorem_name,
        "source_file_ref": file_sha256(source_path),
        "source_file_path": str(source_path),
        "proof_region": {
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "statement_hash": sha256_text(f"theorem {theorem_name} (P : Point) (L : Line) (C : Circle) (h00 : line_circle_intersection P L C) : on_line P L"),
        "binder_map": {"P": "point:P", "L": "line:L", "C": "circle:C", "h00": "hyp:h00"},
        "proof_region_identity": sha256_text(f"proof-region:{theorem_name}"),
        "binder_map_identity": sha256_text("{}"),
        "anchor_use_policy": "locate_and_patch_only",
        "git_head": current_git_head(),
    }
    anchor["anchor_ref"] = sha256_text(canonical_json(anchor))
    write_json(run_dir / "theorem_anchors_v0_6" / "self_test.json", anchor)

    claim_ref = sha256_text("wp11_self_test_claim")
    checker_ref = sha256_text("wp11_self_test_checker")
    artifact_ref = sha256_text("wp11_self_test_non_target_artifact")
    selected = {
        "schema_version": "SelectedSolverDerivationV3",
        "claim_spec_ref": claim_ref,
        "selected_steps": [
            {
                "step_id": "wp11-self-test-step",
                "artifact_ref": artifact_ref,
                "artifact_kind": "construction",
                "checker_ref": checker_ref,
                "rule_id": "full2d_rule:construction_intersection:07",
                "premises": ["hypothesis:h00"],
                "conclusion": "self_test_non_target_intermediate",
                "is_final_target": False,
                "engine_output_ref": sha256_text("wp11_self_test_engine"),
                "engine_role": "construction",
                "checked_side_conditions": ["self_test_side_condition"],
                "non_target_source": "checked_solver_artifact",
            },
            {
                "step_id": "wp11-self-test-final-step",
                "artifact_ref": sha256_text("wp11_self_test_final_application"),
                "artifact_kind": "fact",
                "checker_ref": sha256_text("wp11_self_test_final_checker"),
                "rule_id": "full2d_rule:construction_intersection:07",
                "premises": ["hypothesis:h00"],
                "conclusion": sha256_text("wp11_self_test_target"),
                "is_final_target": True,
                "engine_output_ref": None,
                "engine_role": "derivation_target_closure",
                "checked_side_conditions": [{"kind": "claim_hypothesis_target_alignment", "expr_hash": sha256_text("wp11_self_test_alignment")}],
                "rule_application": {
                    "rule_id": "full2d_rule:construction_intersection:07",
                    "object_args": ["P", "L", "C"],
                    "premise_bindings": ["h00"],
                    "application_source": "claim_hypothesis_target_alignment_v0_6",
                },
            },
        ],
        "final_step_ref": sha256_text("wp11_self_test_target"),
        "has_non_target_intermediate": True,
        "has_checked_side_condition_or_certificate": True,
        "target_hash_commitment": sha256_text("wp11_self_test_target"),
        "entailment_witness_ref": sha256_text("wp11_self_test_entailment"),
        "entailment_witness_input_hash": sha256_text("wp11_self_test_entailment_input"),
        "source_stage": "selected_solver_derivation_from_independently_checked_solver_artifacts",
        "git_head": current_git_head(),
    }
    write_json(run_dir / "selected_solver_derivations_v0_6" / "self_test.json", selected)
    selected_ref = file_sha256(run_dir / "selected_solver_derivations_v0_6" / "self_test.json")

    registry = {
        "schema_version": "RuleRegistrySnapshotV1",
        "snapshot_ref": sha256_text("wp11_self_test_registry"),
        "source_registry_hash": sha256_text("wp11_self_test_registry_source"),
        "source_registry_ref": sha256_text("wp11_self_test_registry_file"),
        "rules": [
            {
                "rule_id": "full2d_rule:construction_intersection:07",
                "lean_lemma": "MathAutoResearch.GeometryFull2D.line_circle_meet_on_line",
                "lean_lemma_type_hash": sha256_text("wp11_self_test_rule_type"),
                "counted_release_rule": True,
            }
        ],
        "rule_contract_hashes": {
            "full2d_rule:construction_intersection:07": sha256_text("wp11_self_test_rule_contract")
        },
        "git_head": current_git_head(),
    }
    write_json(run_dir / "rule_registry_snapshots_v0_6" / "rule_registry_snapshot_v0_6.json", registry)
    registry_ref = file_sha256(run_dir / "rule_registry_snapshots_v0_6" / "rule_registry_snapshot_v0_6.json")

    side = {
        "schema_version": "SideConditionReportV1",
        "step_id": "wp11-self-test-step",
        "artifact_ref": artifact_ref,
        "status": "passed",
        "side_condition_count": 1,
        "side_condition_hash": sha256_text("wp11_self_test_side_condition"),
        "git_head": current_git_head(),
    }
    side["report_id"] = sha256_text(canonical_json(side))
    write_json(run_dir / "side_condition_reports_v0_6" / "self_test.json", side)
    side_ref = file_sha256(run_dir / "side_condition_reports_v0_6" / "self_test.json")

    patch, compiler, compiler_ref, patch_ref = compile_case(
        temp_dir=run_dir,
        theorem_anchor=anchor,
        selected_derivation=selected,
        rule_registry_snapshot=registry,
        side_reports=[side],
    )
    worker = apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=anchor,
        patch_candidate=patch,
        output_dir=run_dir,
        run_id="self_test_original",
    )
    worker_path = run_dir / PROOF_WORKER_RESULT_DIR / "self_test_original.json"
    write_json(worker_path, worker)
    verify = final_verify_gate_v0_6(
        source_path=source_path,
        candidate_path=Path(str(worker["generated_candidate_path"])),
        theorem_anchor=anchor,
        proof_worker_result=worker,
        output_dir=run_dir,
    )
    verify_path = run_dir / FINAL_VERIFY_REPORT_DIR / "self_test_original.json"
    write_json(verify_path, verify)
    certificate = build_solver_backed_certificate_v0_6(
        actual_task_run_ref=sha256_text("wp11_self_test_actual_task_pending"),
        claim_spec_ref=claim_ref,
        engine_output_refs=[sha256_text("wp11_self_test_engine")],
        selected_derivation_ref=selected_ref,
        compiler_result_ref=compiler_ref,
        proof_worker_result_ref=file_sha256(worker_path),
        final_verify_report_ref=file_sha256(verify_path),
        solver_causality_live_run_ref=sha256_text("wp11_self_test_causality_pending"),
    )
    certificate_path = run_dir / SOLVER_BACKED_CERTIFICATE_DIR / "self_test_original.json"
    write_json(certificate_path, certificate)
    record = {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": "wp11-self-test-run",
        "task_id": "wp11_self_test",
        "baseline_id": "B2",
        "git_head": current_git_head(),
        "git_status_hash": sha256_text("wp11_self_test_git_status"),
        "selected_implementation_hash": sha256_text("wp11_self_test_impl"),
        "corpus_manifest_hash": sha256_text("wp11_self_test_corpus"),
        "config_hash": sha256_text("wp11_self_test_config"),
        "checker_hash_set_ref": sha256_text("wp11_self_test_checker_hash_set"),
        "release_run_dir_hash": sha256_text(str(run_dir)),
        "stage_timestamps": {
            "extraction_started_at": "2026-06-20T00:00:00Z",
            "provider_started_at": "2026-06-20T00:00:01Z",
            "provider_finished_at": "2026-06-20T00:00:02Z",
            "compiler_started_at": "2026-06-20T00:00:03Z",
            "final_verify_finished_at": "2026-06-20T00:00:04Z",
        },
        "source_theorem_ref": file_sha256(source_path),
        "extraction_report_ref": sha256_text("wp11_self_test_extraction"),
        "claim_spec_ref": claim_ref,
        "provider_run_manifest_ref": sha256_text("wp11_self_test_provider"),
        "engine_output_refs": [sha256_text("wp11_self_test_engine")],
        "independent_solver_artifact_check_refs": [checker_ref],
        "selected_solver_derivation_ref": selected_ref,
        "derivation_target_match_ref": sha256_text("wp11_self_test_target_match"),
        "compiler_result_refs": [compiler_ref],
        "lean_patch_candidate_ref": patch_ref,
        "proof_worker_result_ref": file_sha256(worker_path),
        "final_verify_report_ref": file_sha256(verify_path),
        "solver_backed_certificate_ref": file_sha256(certificate_path),
        "stage_failure_report_ref": None,
        "final_status": "final_theorem",
    }
    write_json(run_dir / "actual_task_pipeline_runs_v0_6" / "wp11_self_test__B2.json", record)


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def safe_path_part(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value)


def dict_deepcopy(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload))


if __name__ == "__main__":
    raise SystemExit(main())
