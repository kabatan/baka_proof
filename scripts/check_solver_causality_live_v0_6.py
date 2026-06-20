#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_proof_worker import file_sha256
from scripts.geometry_full2d_v0_6_red_cases import detect_variant
from scripts.geometry_full2d_v0_6_schemas import current_git_head, sha256_text, validate_payload
from scripts.run_solver_causality_live_v0_6 import (
    ACTUAL_TASK_RUN_DIRS,
    CAUSALITY_REPORT_DIR,
    COMMAND_LOG_DIR,
    MUTATION_KINDS,
    build_self_test_run,
    run_solver_causality_live,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--output", required=False)
    args = parser.parse_args()

    sections: dict[str, Any] = {}
    errors: list[str] = []
    if args.self_test:
        sections["self_test"] = self_test_report()
        if sections["self_test"]["status"] != "passed":
            errors.extend(f"self_test:{error}" for error in sections["self_test"].get("errors", []))
    if args.run_dir:
        sections["run_check"] = check_solver_causality_live(Path(args.run_dir))
        if sections["run_check"]["status"] != "passed":
            errors.extend(f"run_check:{error}" for error in sections["run_check"].get("errors", []))
    if args.red_cases:
        sections["red_cases"] = red_case_report()
        if sections["red_cases"]["status"] != "passed":
            errors.extend(f"red_cases:{error}" for error in sections["red_cases"].get("errors", []))
    if not sections:
        parser.error("at least one of --run-dir, --self-test, or --red-cases is required")

    report = {
        "schema_version": "CheckSolverCausalityLiveV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "sections": sections,
        "git_head": current_git_head(),
    }
    if args.output:
        write_json(Path(args.output), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_solver_causality_live(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve_path(run_dir)
    errors: list[str] = []
    b2_records = load_b2_success_record_refs(run_dir)
    reports = load_reports(run_dir)
    command_logs = build_command_log_index(run_dir)
    reports_by_source: dict[str, dict[str, Any]] = {}
    for report_path, report in reports:
        source_ref = str(report.get("source_actual_run_ref", ""))
        if source_ref in reports_by_source:
            errors.append(f"duplicate_causality_report:{source_ref}")
        reports_by_source[source_ref] = report
        errors.extend(f"{report_path.name}:{error}" for error in validate_report(report_path, report, run_dir, b2_records, command_logs))

    missing = sorted(set(b2_records) - set(reports_by_source))
    errors.extend(f"missing_live_causality_report:{ref}" for ref in missing)
    unexpected = sorted(set(reports_by_source) - set(b2_records))
    errors.extend(f"causality_report_without_b2_success:{ref}" for ref in unexpected)
    report = {
        "schema_version": "SolverCausalityLiveRunCheckV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "b2_success_count": len(b2_records),
        "causality_report_count": len(reports),
        "not_applicable_no_b2_successes": len(b2_records) == 0,
        "coverage_fraction": round(len(reports_by_source) / len(b2_records), 6) if b2_records else None,
        "git_head": current_git_head(),
    }
    write_json(run_dir / "solver_causality_live_check_v0_6.json", report)
    return report


def validate_report(
    report_path: Path,
    report: dict[str, Any],
    run_dir: Path,
    b2_records: dict[str, Path],
    command_logs: dict[str, dict[str, Any]],
) -> list[str]:
    errors = validate_payload(report)
    if report.get("status") != "passed":
        errors.append("causality_report_status_not_passed")
    source_ref = str(report.get("source_actual_run_ref", ""))
    if source_ref not in b2_records:
        errors.append("source_actual_run_ref_not_b2_success")
    seen_kinds: set[str] = set()
    seen_temp_dirs: set[str] = set()
    mutation_cases = report.get("mutation_cases")
    if not isinstance(mutation_cases, list):
        return errors + ["mutation_cases_not_list"]
    for index, case in enumerate(mutation_cases):
        if not isinstance(case, dict):
            errors.append(f"mutation_case_not_object:{index}")
            continue
        kind = str(case.get("mutation_kind"))
        seen_kinds.add(kind)
        command_ref = str(case.get("command_log_ref", ""))
        command_log = command_logs.get(command_ref)
        if command_log is None:
            errors.append(f"{kind}:command_log_ref_unresolved")
            continue
        errors.extend(validate_command_log(kind, case, command_log, run_dir, source_ref, seen_temp_dirs))
    missing_kinds = set(MUTATION_KINDS) - seen_kinds
    if missing_kinds:
        errors.append("missing_mutation_kinds:" + ",".join(sorted(missing_kinds)))
    return sorted(set(errors))


def validate_command_log(
    kind: str,
    case: dict[str, Any],
    command_log: dict[str, Any],
    run_dir: Path,
    source_ref: str,
    seen_temp_dirs: set[str],
) -> list[str]:
    errors: list[str] = []
    if command_log.get("source_actual_run_ref") != source_ref:
        errors.append(f"{kind}:command_source_actual_run_ref_mismatch")
    if command_log.get("mutation_kind") != kind:
        errors.append(f"{kind}:command_mutation_kind_mismatch")
    if command_log.get("stage_sequence") != ["compiler", "proof_worker", "final_verify"]:
        errors.append(f"{kind}:stage_sequence_not_compiler_proof_worker_final_verify")
    command = command_log.get("command")
    if not isinstance(command, list) or command[:3] != ["lake", "env", "lean"]:
        errors.append(f"{kind}:final_verify_command_not_lake_env_lean")
    if command_log.get("actual_subprocess_executed") is not True:
        errors.append(f"{kind}:actual_final_verify_subprocess_not_executed")
    if command_log.get("input_artifact_set_hash") != case.get("input_artifact_set_hash"):
        errors.append(f"{kind}:input_artifact_set_hash_mismatch")
    if command_log.get("output_patch_hash") != case.get("output_patch_hash"):
        errors.append(f"{kind}:output_patch_hash_mismatch")
    if command_log.get("final_verify_status") != case.get("final_verify_status"):
        errors.append(f"{kind}:final_verify_status_mismatch")
    verify_rel = command_log.get("final_verify_report_path")
    verify_ref = command_log.get("final_verify_report_ref")
    if not isinstance(verify_rel, str) or not isinstance(verify_ref, str):
        errors.append(f"{kind}:final_verify_report_path_or_ref_missing")
    else:
        verify_path = run_dir / verify_rel
        if not verify_path.exists():
            errors.append(f"{kind}:final_verify_report_file_missing")
        elif file_sha256(verify_path) != verify_ref:
            errors.append(f"{kind}:final_verify_report_ref_mismatch")
    temp_rel = command_log.get("temp_run_dir")
    if not isinstance(temp_rel, str):
        errors.append(f"{kind}:temp_run_dir_missing")
    else:
        if temp_rel in seen_temp_dirs:
            errors.append(f"{kind}:temp_run_dir_reused")
        seen_temp_dirs.add(temp_rel)
        temp_path = run_dir / temp_rel
        if not temp_path.exists():
            errors.append(f"{kind}:temp_run_dir_not_found")
        if "solver_causality_live_temp_v0_6" not in temp_path.parts:
            errors.append(f"{kind}:temp_run_dir_not_isolated_causality_dir")
    if kind == "positive_control":
        if case.get("final_verify_status") != "passed":
            errors.append("positive_control_final_verify_not_passed")
        if command_log.get("returncode") != 0:
            errors.append("positive_control_lake_env_lean_failed")
        if case.get("counted_same_final_theorem") is not True:
            errors.append("positive_control_did_not_reproduce_final_theorem")
    else:
        if case.get("counted_same_final_theorem") is not False:
            errors.append(f"{kind}:mutation_counted_same_final_theorem")
        if case.get("final_verify_status") == "passed" or command_log.get("returncode") == 0:
            errors.append(f"{kind}:mutation_final_verify_unexpectedly_passed")
    return errors


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "wp11_self_test_run"
        build_self_test_run(run_dir)
        run_report = run_solver_causality_live(run_dir, all_b2_successes=True)
        check_report = check_solver_causality_live(run_dir)
        errors: list[str] = []
        if run_report.get("status") != "passed":
            errors.append("self_test_runner_failed")
        if check_report.get("status") != "passed":
            errors.append("self_test_check_failed")
        if check_report.get("b2_success_count") != 1:
            errors.append("self_test_b2_success_count_not_one")
        if check_report.get("causality_report_count") != 1:
            errors.append("self_test_causality_report_count_not_one")
        return {
            "schema_version": "SolverCausalityLiveSelfTestV06",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "runner": run_report,
            "checker": check_report,
        }


def red_case_report() -> dict[str, Any]:
    cases = {
        "field_only_causality": red_case_field_only,
        "missing_command_log": red_case_missing_command_log,
        "mutation_same_final_theorem": red_case_mutation_same_final,
        "positive_control_not_passed": red_case_positive_not_passed,
        "checker_generated_success_artifact": red_case_checker_generated_success,
    }
    results: dict[str, Any] = {}
    errors: list[str] = []
    for name, builder in cases.items():
        result = builder()
        results[name] = result
        if result.get("status") != "passed":
            errors.append(f"{name}_not_rejected")
    rc006_blockers, rc006_errors = detect_variant(
        {
            "kind": "static-code",
            "code": "causality_report_only = True\nfailed_as_expected = True\nfield_only_causality\nno_live_rerun_logs\nmutation_same_final_theorem\n",
        }
    )
    rc006 = {"detected_K": sorted(rc006_blockers), "errors": rc006_errors}
    if not {"K-018", "K-019"}.issubset(rc006_blockers) or rc006_errors:
        errors.append("rc006_manifest_not_rejected")
    return {
        "schema_version": "SolverCausalityLiveRedCasesV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "case_results": results,
        "rc006_manifest": rc006,
        "git_head": current_git_head(),
    }


def red_case_field_only() -> dict[str, Any]:
    return expect_bad_report(
        {
            "schema_version": "SolverCausalityLiveRunV1",
            "report_id": ref("field_only_report"),
            "source_actual_run_ref": ref("actual"),
            "temp_run_dir_ref": ref("temp"),
            "mutation_cases": [],
            "status": "passed",
            "report_only_causality": True,
            "git_head": current_git_head(),
        },
        expected=["causality_report_not_live_rerun", "schema_only_or_forbidden_marker:report_only_causality"],
    )


def red_case_missing_command_log() -> dict[str, Any]:
    report = valid_report_skeleton()
    return expect_check_failure(report, expected=["command_log_ref_unresolved"])


def red_case_mutation_same_final() -> dict[str, Any]:
    report = valid_report_skeleton()
    for case in report["mutation_cases"]:
        if case["mutation_kind"] == "remove_selected_artifact":
            case["counted_same_final_theorem"] = True
            case["final_verify_status"] = "passed"
    return expect_bad_report(report, expected=["mutation_did_not_break_same_final_theorem"])


def red_case_positive_not_passed() -> dict[str, Any]:
    report = valid_report_skeleton()
    report["mutation_cases"][0]["final_verify_status"] = "failed"
    report["mutation_cases"][0]["counted_same_final_theorem"] = False
    return expect_bad_report(report, expected=["positive_control_final_verify_not_passed"])


def red_case_checker_generated_success() -> dict[str, Any]:
    report = valid_report_skeleton()
    report["checker_generated_success_artifacts"] = True
    return expect_bad_report(report, expected=["schema_only_or_forbidden_marker:checker_generated_success_artifacts"])


def expect_bad_report(report: dict[str, Any], *, expected: list[str]) -> dict[str, Any]:
    errors = validate_payload(report)
    text = "\n".join(errors)
    missing = [item for item in expected if item not in text]
    return {
        "status": "passed" if errors and not missing else "failed",
        "validator_errors": errors,
        "missing_expected_errors": missing,
    }


def expect_check_failure(report: dict[str, Any], *, expected: list[str]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / "bad_run"
        run_dir.mkdir()
        actual_ref = write_minimal_actual_record(run_dir)
        report["source_actual_run_ref"] = actual_ref
        write_json(run_dir / CAUSALITY_REPORT_DIR / "bad.json", report)
        check = check_solver_causality_live(run_dir)
        text = "\n".join(check.get("errors", []))
        missing = [item for item in expected if item not in text]
        return {
            "status": "passed" if check.get("status") == "failed" and not missing else "failed",
            "check": check,
            "missing_expected_errors": missing,
        }


def valid_report_skeleton() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for kind in MUTATION_KINDS:
        cases.append(
            {
                "mutation_kind": kind,
                "command_log_ref": ref(f"command:{kind}"),
                "input_artifact_set_hash": ref(f"input:{kind}"),
                "output_patch_hash": ref(f"patch:{kind}"),
                "final_verify_status": "passed" if kind == "positive_control" else "failed",
                "counted_same_final_theorem": kind == "positive_control",
            }
        )
    body = {
        "schema_version": "SolverCausalityLiveRunV1",
        "source_actual_run_ref": ref("actual"),
        "temp_run_dir_ref": ref("temp"),
        "mutation_cases": cases,
        "status": "passed",
        "git_head": current_git_head(),
    }
    return {"report_id": sha256_text(canonical_json(body)), **body}


def load_b2_success_record_refs(run_dir: Path) -> dict[str, Path]:
    rows: dict[str, Path] = {}
    for directory in ACTUAL_TASK_RUN_DIRS:
        root = run_dir / directory
        if not root.exists():
            continue
        for path in sorted(root.glob("*.json")):
            try:
                payload = read_json(path)
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            if payload.get("schema_version") != "ActualTaskPipelineRunV4":
                continue
            if payload.get("baseline_id") == "B2" and payload.get("final_status") == "final_theorem":
                rows[file_sha256(path)] = path
    return rows


def load_reports(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    report_dir = run_dir / CAUSALITY_REPORT_DIR
    if not report_dir.exists():
        return []
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(report_dir.glob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        if isinstance(payload, dict):
            rows.append((path, payload))
    return rows


def build_command_log_index(run_dir: Path) -> dict[str, dict[str, Any]]:
    root = run_dir / COMMAND_LOG_DIR
    rows: dict[str, dict[str, Any]] = {}
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        rows[file_sha256(path)] = payload
        command_id = payload.get("command_log_id")
        if isinstance(command_id, str) and command_id.startswith("sha256:"):
            rows[command_id] = payload
    return rows


def write_minimal_actual_record(run_dir: Path) -> str:
    record = {
        "schema_version": "ActualTaskPipelineRunV4",
        "run_id": "red-case-run",
        "task_id": "red_case_task",
        "baseline_id": "B2",
        "git_head": current_git_head(),
        "git_status_hash": ref("git_status"),
        "selected_implementation_hash": ref("implementation"),
        "corpus_manifest_hash": ref("corpus"),
        "config_hash": ref("config"),
        "checker_hash_set_ref": ref("checker"),
        "release_run_dir_hash": ref("run_dir"),
        "stage_timestamps": {
            "extraction_started_at": "2026-06-20T00:00:00Z",
            "provider_started_at": "2026-06-20T00:00:01Z",
            "provider_finished_at": "2026-06-20T00:00:02Z",
            "compiler_started_at": "2026-06-20T00:00:03Z",
            "final_verify_finished_at": "2026-06-20T00:00:04Z",
        },
        "source_theorem_ref": ref("source"),
        "extraction_report_ref": ref("extraction"),
        "claim_spec_ref": ref("claim"),
        "provider_run_manifest_ref": ref("provider"),
        "engine_output_refs": [ref("engine")],
        "independent_solver_artifact_check_refs": [ref("check")],
        "selected_solver_derivation_ref": ref("selected"),
        "derivation_target_match_ref": ref("match"),
        "compiler_result_refs": [ref("compiler")],
        "lean_patch_candidate_ref": ref("patch"),
        "proof_worker_result_ref": ref("worker"),
        "final_verify_report_ref": ref("verify"),
        "solver_backed_certificate_ref": ref("certificate"),
        "stage_failure_report_ref": None,
        "final_status": "final_theorem",
    }
    path = run_dir / "actual_task_pipeline_runs_v0_6" / "red_case_task__B2.json"
    write_json(path, record)
    return file_sha256(path)


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def ref(seed: str) -> str:
    return sha256_text(seed)


if __name__ == "__main__":
    raise SystemExit(main())
