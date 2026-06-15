from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records import validate_actual_task_pipeline_run  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_matrix_evidence(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_matrix_evidence(run_dir: Path) -> dict[str, Any]:
    run_dir = _resolve(run_dir)
    errors: list[str] = []
    matrix_summary = _read_json(run_dir / "matrix_summary.json", errors)
    baseline_report = _read_json(run_dir / "baseline_comparability_report.json", errors)
    records = _iter_run_records(run_dir, errors)
    record_reports = []
    for source, record in records:
        record_errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
        record_reports.append({"source": source, "status": "passed" if not record_errors else "failed", "errors": record_errors})
        errors.extend(record_errors)
    if matrix_summary is None:
        errors.append("missing_matrix_summary")
    else:
        if matrix_summary.get("sidecar_overlay_used") is not False:
            errors.append("matrix_sidecar_overlay_used")
        summary_count = (
            matrix_summary.get("actual_task_pipeline_run_summary", {}).get("record_count")
            if isinstance(matrix_summary.get("actual_task_pipeline_run_summary"), dict)
            else None
        )
        if summary_count != len(records):
            errors.append(f"matrix_record_count_mismatch:{summary_count}!={len(records)}")
        if matrix_summary.get("status") != "passed":
            errors.append("matrix_summary_status_not_passed")
    if baseline_report is None:
        errors.append("missing_baseline_comparability_report")
    if not records:
        errors.append("no_actual_task_pipeline_runs_for_matrix")
    final_count = sum(1 for _source, record in records if record.get("final_status") == "final_theorem")
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "matrix_evidence_summary": {
            "record_count": len(records),
            "final_theorem_record_count": final_count,
            "matrix_summary_present": matrix_summary is not None,
            "baseline_comparability_report_present": baseline_report is not None,
        },
        "record_reports": record_reports,
        "errors": sorted(set(errors)),
    }


def _iter_run_records(run_dir: Path, errors: list[str]) -> list[tuple[str, dict[str, Any]]]:
    records: list[tuple[str, dict[str, Any]]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, errors)
            if isinstance(payload, dict):
                records.append((path.relative_to(run_dir).as_posix(), payload))
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for index, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"actual_task_pipeline_runs.jsonl:{index}:json_decode_error:{exc}")
                continue
            if isinstance(payload, dict):
                records.append((f"actual_task_pipeline_runs.jsonl:{index}", payload))
    return records


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
