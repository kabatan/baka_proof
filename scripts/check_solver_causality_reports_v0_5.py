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

from scripts.geometry_full2d_v0_5_schemas import validate_payload


REQUIRED_MUTATIONS = {
    "remove_selected_solver_artifact",
    "corrupt_selected_fact_or_construction",
    "corrupt_certificate_or_checker_output",
    "unsupported_rule_mutation",
    "side_condition_mutation",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    run_dir = Path(args.run_dir or "runs/geometry_full2d_v0_5")
    if args.self_test:
        self_report = self_test_report()
        if load_b2_success_records(resolve(run_dir)):
            run_report = check_reports(run_dir)
            report = combined_report(
                "SolverCausalityReportsSelfTestAndRunCheckV05",
                self_report,
                run_report,
                self_key="self_test",
                run_key="run_check",
            )
        else:
            report = self_report
    else:
        report = check_reports(run_dir)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_reports(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    errors: list[str] = []
    b2_successes = load_b2_success_records(run_dir)
    reports = load_reports(run_dir)
    reports_by_task = {str(report.get("task_id")): report for report in reports}
    if len(reports_by_task) != len(reports):
        errors.append("duplicate_or_missing_task_report")
    missing = sorted(set(b2_successes) - set(reports_by_task))
    errors.extend(f"missing_causality_report:{task_id}" for task_id in missing[:50])
    ref_index = build_ref_index(run_dir)
    passed_reports = 0
    mutation_run_count = 0
    for report in reports:
        task_id = str(report.get("task_id", "missing_task"))
        schema_errors = validate_payload(report, current_head="test-head")
        errors.extend(f"{task_id}:{error}" for error in schema_errors)
        report_errors = validate_report_payload(report, run_dir, ref_index)
        errors.extend(f"{task_id}:{error}" for error in report_errors)
        if not schema_errors and not report_errors:
            passed_reports += 1
        mutation_run_count += len(report.get("mutation_runs", [])) if isinstance(report.get("mutation_runs"), list) else 0
    live_fraction = passed_reports / len(b2_successes) if b2_successes else 0.0
    destructive_pass_rate = passed_reports / len(reports) if reports else 0.0
    report = {
        "schema_version": "SolverCausalityReportsCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "b2_success_count": len(b2_successes),
        "report_count": len(reports),
        "mutation_run_count": mutation_run_count,
        "live_destructive_rerun_fraction": round(live_fraction, 6),
        "destructive_causality_pass_rate": round(destructive_pass_rate, 6),
        "precomputed_report_fraction": 0.0 if reports else 1.0,
    }
    write_json(run_dir / "solver_causality_reports_check_v0_5.json", report)
    return report


def validate_report_payload(report: dict[str, Any], run_dir: Path, ref_index: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    task_id = str(report.get("task_id", "missing_task"))
    positive = report.get("positive_control")
    if not isinstance(positive, dict):
        errors.append("positive_control_not_object")
    else:
        if positive.get("same_final_theorem_counted") is not True:
            errors.append("positive_control_not_reproduced")
        errors.extend(validate_run_evidence("positive_control", positive, run_dir, ref_index, task_id=task_id, mutation="positive_control", expect_success=True))
    runs = report.get("mutation_runs")
    if not isinstance(runs, list) or not runs:
        errors.append("causality_report_not_live_rerun")
        runs = []
    seen = {str(item.get("mutation")) for item in runs if isinstance(item, dict)}
    missing = sorted(REQUIRED_MUTATIONS - seen)
    if missing:
        errors.append("missing_mutation_runs:" + ",".join(missing))
    for index, item in enumerate(runs):
        if not isinstance(item, dict):
            errors.append(f"bad_mutation_run:{index}")
            continue
        if item.get("same_final_theorem_counted") is not False:
            errors.append(f"destructive_causality_failure:{index}")
        if item.get("fresh_temp_run") is not True:
            errors.append(f"mutation_not_fresh:{index}")
        if item.get("rerun_stage_sequence") != ["compiler", "proof_worker", "final_verify"]:
            errors.append(f"mutation_stage_sequence_invalid:{index}")
        errors.extend(validate_run_evidence(f"mutation:{index}", item, run_dir, ref_index, task_id=task_id, mutation=str(item.get("mutation")), expect_success=False))
    if report.get("live_rerun_status") != "fresh_temp_dirs_with_command_logs":
        errors.append("live_rerun_status_invalid")
    if report.get("destructive_causality_passed") is not True:
        errors.append("destructive_causality_not_passed")
    return errors


def validate_run_evidence(
    label: str,
    payload: dict[str, Any],
    run_dir: Path,
    ref_index: dict[str, dict[str, Any]],
    *,
    task_id: str,
    mutation: str,
    expect_success: bool,
) -> list[str]:
    errors: list[str] = []
    command_ref = str(payload.get("command_log_ref", ""))
    if command_ref not in ref_index:
        errors.append(f"{label}:command_log_ref_unresolved")
        command_log: dict[str, Any] = {}
    else:
        command_log = ref_index[command_ref]
        command = command_log.get("command")
        if not isinstance(command, list) or command[:3] != ["lake", "env", "lean"]:
            errors.append(f"{label}:command_log_not_lake_env_lean")
        if command_log.get("actual_subprocess_executed") is not True:
            errors.append(f"{label}:actual_subprocess_not_recorded")
        if command_log.get("stage_sequence") != ["compiler", "proof_worker", "final_verify"]:
            errors.append(f"{label}:command_stage_sequence_invalid")
        if command_log.get("task_id") != task_id:
            errors.append(f"{label}:command_task_id_mismatch")
        if command_log.get("mutation") != mutation:
            errors.append(f"{label}:command_mutation_mismatch")
        if command_log.get("task_count") != 1:
            errors.append(f"{label}:command_not_per_task_final_verify")
        returncode = command_log.get("returncode")
        if expect_success and returncode != 0:
            errors.append(f"{label}:positive_control_command_failed")
        if not expect_success and returncode == 0:
            errors.append(f"{label}:mutation_command_unexpected_success")
        if payload.get("same_final_theorem_counted") != (returncode == 0):
            errors.append(f"{label}:same_final_theorem_counted_disagrees_with_command")
        if not isinstance(command_log.get("candidate_ref"), str) or not str(command_log.get("candidate_ref")).startswith("sha256:"):
            errors.append(f"{label}:candidate_ref_missing")
        if not isinstance(command_log.get("task_manifest_ref"), str) or not str(command_log.get("task_manifest_ref")).startswith("sha256:"):
            errors.append(f"{label}:task_manifest_ref_missing")
    temp_rel = payload.get("temp_run_dir")
    if not isinstance(temp_rel, str) or not (run_dir / temp_rel).exists():
        errors.append(f"{label}:temp_run_dir_missing")
    if not isinstance(payload.get("temp_run_dir_hash"), str) or not str(payload.get("temp_run_dir_hash")).startswith("sha256:"):
        errors.append(f"{label}:temp_run_dir_hash_invalid")
    return errors


def load_b2_success_records(run_dir: Path) -> list[str]:
    records_dir = run_dir / "actual_task_pipeline_runs"
    task_ids: list[str] = []
    if records_dir.exists():
        for item in sorted(records_dir.glob("*__B2.json")):
            payload = json.loads(item.read_text(encoding="utf-8"))
            if payload.get("baseline_id") == "B2" and payload.get("final_status") == "final_theorem":
                task_ids.append(str(payload.get("task_id")))
    return task_ids


def load_reports(run_dir: Path) -> list[dict[str, Any]]:
    reports_dir = run_dir / "solver_causality_reports"
    if not reports_dir.exists():
        return []
    reports: list[dict[str, Any]] = []
    for item in sorted(reports_dir.glob("*.json")):
        payload = json.loads(item.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            reports.append(payload)
    return reports


def build_ref_index(run_dir: Path) -> dict[str, dict[str, Any]]:
    refs: dict[str, dict[str, Any]] = {}
    roots = [
        run_dir / "command_logs" / "solver_causality",
    ]
    files = [item for root in roots if root.exists() for item in sorted(root.glob("*.json"))]
    for item in files:
        try:
            payload = json.loads(item.read_text(encoding="utf-8"))
        except Exception:
            payload = None
        if isinstance(payload, dict):
            for key in ["content_sha256", "command_log_id", "report_id", "certificate_id", "disabled_report_id"]:
                value = payload.get(key)
                if isinstance(value, str) and value.startswith("sha256:"):
                    refs[value] = payload
    return refs


def combined_report(
    schema_version: str,
    self_report: dict[str, Any],
    run_report: dict[str, Any],
    *,
    self_key: str,
    run_key: str,
) -> dict[str, Any]:
    errors: list[str] = []
    if self_report.get("status") != "passed":
        errors.append(f"{self_key}_failed")
    if run_report.get("status") != "passed":
        errors.append(f"{run_key}_failed")
    errors.extend(f"{self_key}:{error}" for error in self_report.get("errors", []) if isinstance(error, str))
    errors.extend(f"{run_key}:{error}" for error in run_report.get("errors", []) if isinstance(error, str))
    return {
        "schema_version": schema_version,
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        self_key: self_report,
        run_key: run_report,
    }


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        run = root / "run"
        (run / "actual_task_pipeline_runs").mkdir(parents=True)
        write_json(run / "actual_task_pipeline_runs" / "task__B2.json", {"task_id": "task", "baseline_id": "B2", "final_status": "final_theorem"})
        bad_report = {
            "schema_version": "SolverCausalityReportV3",
            "report_id": "sha256:" + "1" * 64,
            "run_record_ref": "sha256:" + "2" * 64,
            "task_id": "task",
            "positive_control": {"same_final_theorem_counted": True},
            "mutation_runs": [],
            "live_rerun_status": "field_only",
        }
        (run / "solver_causality_reports").mkdir(parents=True)
        write_json(run / "solver_causality_reports" / "task.json", bad_report)
        bad = check_reports(run)
        errors: list[str] = []
        expected = {"causality_report_not_live_rerun", "positive_control:command_log_ref_unresolved", "positive_control:temp_run_dir_missing"}
        if bad["status"] != "failed":
            errors.append("field_only_fixture_not_rejected")
        error_text = "\n".join(map(str, bad["errors"]))
        if not all(expected_item in error_text for expected_item in expected):
            errors.append("field_only_fixture_missing_expected_errors")
        return {
            "schema_version": "SolverCausalityReportsCheckSelfTestV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "field_only_fixture": bad,
        }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
