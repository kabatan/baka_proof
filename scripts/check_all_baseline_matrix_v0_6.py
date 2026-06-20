#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7", "B8"]
ACTUAL_RUN_DIR = "actual_task_pipeline_runs_v0_6"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--red-cases", action="store_true")
    args = parser.parse_args()
    sections: dict[str, Any] = {"matrix_check": check_matrix(Path(args.run_dir))}
    errors = [f"matrix_check:{error}" for error in sections["matrix_check"].get("errors", [])]
    if args.red_cases:
        sections["red_cases"] = red_case_report()
        errors.extend(f"red_cases:{error}" for error in sections["red_cases"].get("errors", []))
    report = {
        "schema_version": "CheckAllBaselineMatrixV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "sections": sections,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_matrix(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    summary_path = run_dir / "full2d_matrix_summary_v0_6.json"
    if not summary_path.exists():
        return failed(["missing_matrix_summary"], run_dir)
    summary = read_json(summary_path)
    records = load_records(run_dir)
    if summary.get("schema_version") != "Full2DMatrixRunV06":
        errors.append("bad_matrix_summary_schema")
    if summary.get("outcome_source") != "ActualTaskPipelineRunV4 records with FinalVerifyGate reports or DisabledStageReportV1":
        errors.append("matrix_outcome_not_from_actual_records")
    counted_task_count = int(summary.get("counted_task_count", 0))
    required_record_count = counted_task_count * len(REQUIRED_BASELINES)
    if len(records) != required_record_count:
        errors.append(f"record_count_mismatch:{len(records)}!={required_record_count}")
    by_task: dict[str, set[str]] = {}
    by_baseline = {baseline: 0 for baseline in REQUIRED_BASELINES}
    ref_index = build_ref_index(run_dir)
    for path, record in records:
        task_id = str(record.get("task_id", ""))
        baseline = str(record.get("baseline_id", ""))
        by_task.setdefault(task_id, set()).add(baseline)
        if baseline in by_baseline:
            by_baseline[baseline] += 1
        else:
            errors.append(f"{path.name}:unknown_baseline:{baseline}")
        errors.extend(f"{path.name}:{error}" for error in validate_record(record, ref_index))
    for task_id, baselines in by_task.items():
        missing = sorted(set(REQUIRED_BASELINES) - baselines)
        if missing:
            errors.append(f"{task_id}:missing_baselines:{','.join(missing)}")
    for baseline, count in by_baseline.items():
        if count != counted_task_count:
            errors.append(f"baseline_record_count_mismatch:{baseline}:{count}!={counted_task_count}")
    return {
        "schema_version": "AllBaselineMatrixV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "record_count": len(records),
        "counted_task_count": counted_task_count,
        "required_baselines": REQUIRED_BASELINES,
        "by_baseline": by_baseline,
    }


def validate_record(record: dict[str, Any], ref_index: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    required = [
        "schema_version",
        "task_id",
        "baseline_id",
        "source_theorem_ref",
        "extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "engine_output_refs",
        "independent_solver_artifact_check_refs",
        "selected_solver_derivation_ref",
        "derivation_target_match_ref",
        "compiler_result_refs",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
        "final_status",
        "stage_failure_report_ref",
    ]
    for key in required:
        if key not in record:
            errors.append(f"missing:{key}")
    if record.get("schema_version") != "ActualTaskPipelineRunV4":
        errors.append("bad_record_schema")
    baseline = str(record.get("baseline_id", ""))
    final_status = record.get("final_status")
    if final_status not in {"final_theorem", "measured_failure"}:
        errors.append("bad_final_status")
    if final_status == "measured_failure" and not is_sha_ref(record.get("stage_failure_report_ref")):
        errors.append("measured_failure_missing_stage_failure_report_ref")
    if final_status == "final_theorem" and not is_sha_ref(record.get("solver_backed_certificate_ref")):
        errors.append("final_theorem_missing_certificate")
    if "label" in str(record.get("outcome_source", "")).lower() or record.get("baseline_outcome_source") == "label":
        errors.append("family_or_label_coded_outcome")
    if baseline == "B2":
        final_ref = str(record.get("final_verify_report_ref", ""))
        final_payload = ref_index.get(final_ref)
        if not final_payload or final_payload.get("schema_version") != "FinalVerifyReportFull2D":
            errors.append("b2_missing_final_verify_report_payload")
        if not record.get("engine_output_refs") or not record.get("independent_solver_artifact_check_refs"):
            errors.append("b2_missing_actual_solver_artifact_refs")
    else:
        failure_ref = str(record.get("stage_failure_report_ref", ""))
        failure_payload = ref_index.get(failure_ref)
        if not failure_payload or failure_payload.get("schema_version") != "DisabledStageReportV1":
            errors.append("disabled_baseline_missing_disabled_stage_report")
        elif failure_payload.get("stage_removed_or_disabled") is not True:
            errors.append("disabled_stage_not_removed_or_disabled")
    return errors


def load_records(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    root = run_dir / ACTUAL_RUN_DIR
    if not root.exists():
        return []
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.glob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        if isinstance(payload, dict):
            rows.append((path, payload))
    return rows


def build_ref_index(run_dir: Path) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(run_dir.rglob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        index[file_sha256(path)] = payload
        for key in ("verify_report_id", "worker_result_id", "failure_report_id", "certificate_id", "report_id"):
            value = payload.get(key)
            if is_sha_ref(value):
                index[str(value)] = payload
    return index


def red_case_report() -> dict[str, Any]:
    cases = {
        "b2_only_matrix": red_case_b2_only_matrix(),
        "label_coded_failure": red_case_label_coded_failure(),
    }
    errors = [name for name, result in cases.items() if result.get("status") != "passed"]
    return {
        "schema_version": "AllBaselineMatrixRedCasesV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "case_results": cases,
    }


def red_case_b2_only_matrix() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_json(root / "full2d_matrix_summary_v0_6.json", {"schema_version": "Full2DMatrixRunV06", "counted_task_count": 1, "outcome_source": "ActualTaskPipelineRunV4 records with FinalVerifyGate reports or DisabledStageReportV1"})
        write_json(root / ACTUAL_RUN_DIR / "task__B2.json", {"schema_version": "ActualTaskPipelineRunV4", "task_id": "task", "baseline_id": "B2", "final_status": "measured_failure", "stage_failure_report_ref": sha256_text("failure")})
        result = check_matrix(root)
        return expect_failure(result, "record_count_mismatch")


def red_case_label_coded_failure() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_json(root / "full2d_matrix_summary_v0_6.json", {"schema_version": "Full2DMatrixRunV06", "counted_task_count": 1, "outcome_source": "ActualTaskPipelineRunV4 records with FinalVerifyGate reports or DisabledStageReportV1"})
        for baseline in REQUIRED_BASELINES:
            write_json(root / ACTUAL_RUN_DIR / f"task__{baseline}.json", {"schema_version": "ActualTaskPipelineRunV4", "task_id": "task", "baseline_id": baseline, "final_status": "measured_failure", "stage_failure_report_ref": sha256_text("failure"), "outcome_source": "label_coded"})
        result = check_matrix(root)
        return expect_failure(result, "family_or_label_coded_outcome")


def expect_failure(report: dict[str, Any], expected: str) -> dict[str, Any]:
    text = "\n".join(str(error) for error in report.get("errors", []))
    return {"status": "passed" if expected in text and report.get("status") == "failed" else "failed", "errors": report.get("errors", [])}


def failed(errors: list[str], run_dir: Path) -> dict[str, Any]:
    return {"schema_version": "AllBaselineMatrixV06", "status": "failed", "errors": errors, "run_dir": str(run_dir)}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(text: str) -> str:
    import hashlib

    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


if __name__ == "__main__":
    raise SystemExit(main())
