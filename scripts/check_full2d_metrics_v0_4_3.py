from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.run_records import validate_actual_task_pipeline_run  # noqa: E402


OVERALL_THRESHOLD = 0.85
FAMILY_THRESHOLDS = {
    "Full2DCore500": 0.95,
    "IncidenceParallelPerp350": 0.92,
    "AngleCyclic450": 0.90,
    "Construction450": 0.85,
    "MetricRatioArea350": 0.85,
    "Transformation250": 0.75,
    "OrderCase250": 0.80,
    "Algebraic250": 0.85,
    "Inequality150": 0.75,
    "OlympiadStyle300": 0.70,
    "HardHoldout50": 0.50,
}
ADVANTAGE_THRESHOLDS = {
    "B2_minus_B1_overall": 0.25,
    "B2_minus_B5_construction": 0.15,
    "B2_minus_B6_algebraic_metric": 0.15,
    "B2_minus_B7_order_case": 0.10,
    "B2_minus_B8_olympiad": 0.05,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_metrics(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_metrics(run_dir: Path) -> dict[str, Any]:
    run_dir = _resolve(run_dir)
    errors: list[str] = []
    records = _iter_run_records(run_dir, errors)
    valid_records: list[dict[str, Any]] = []
    for source, record in records:
        record_errors = validate_actual_task_pipeline_run(record, run_dir=run_dir)
        if record_errors:
            errors.extend(f"{source}:{error}" for error in record_errors)
        else:
            valid_records.append(record)
    if not valid_records:
        errors.append("no_valid_actual_task_pipeline_runs_for_metrics")
    metrics_summary = _metrics_summary(valid_records)
    advantage_summary = _advantage_summary(valid_records)
    measured_failure_summary = _measured_failure_summary(valid_records)
    _check_thresholds(metrics_summary, advantage_summary, errors)
    output = {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "metrics_summary": metrics_summary,
        "advantage_summary": advantage_summary,
        "measured_failure_summary": measured_failure_summary,
        "errors": sorted(set(errors)),
    }
    (run_dir / "metrics_v0_4_3.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output


def _metrics_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_baseline: dict[str, dict[str, Any]] = {}
    for baseline in sorted({str(record.get("baseline_id")) for record in records}):
        baseline_records = [record for record in records if str(record.get("baseline_id")) == baseline]
        positives = [record for record in baseline_records if _target_status(record) == "in_target_positive"]
        final_success = [record for record in positives if record.get("final_status") == "final_theorem"]
        family_rates = {}
        for family in FAMILY_THRESHOLDS:
            family_records = [record for record in positives if _theorem_family(record) == family]
            family_success = [record for record in family_records if record.get("final_status") == "final_theorem"]
            family_rates[family] = _rate(len(family_success), len(family_records))
        by_baseline[baseline] = {
            "positive_count": len(positives),
            "final_theorem_count": len(final_success),
            "overall_final_theorem_rate": _rate(len(final_success), len(positives)),
            "family_rates": family_rates,
            "safe_reject_success_on_in_target_positive": sum(
                1 for record in positives if record.get("final_status") == "measured_failure" and record.get("failure_reason") == "safe_reject"
            ),
        }
    return {"derived_from": "ActualTaskPipelineRunV1", "by_baseline": by_baseline}


def _advantage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "B2_minus_B1_overall": _rate_for(records, "B2") - _rate_for(records, "B1"),
        "B2_minus_B5_construction": _rate_for(records, "B2", {"Construction450"}) - _rate_for(records, "B5", {"Construction450"}),
        "B2_minus_B6_algebraic_metric": _rate_for(records, "B2", {"Algebraic250", "MetricRatioArea350"}) - _rate_for(records, "B6", {"Algebraic250", "MetricRatioArea350"}),
        "B2_minus_B7_order_case": _rate_for(records, "B2", {"OrderCase250"}) - _rate_for(records, "B7", {"OrderCase250"}),
        "B2_minus_B8_olympiad": _rate_for(records, "B2", {"OlympiadStyle300"}) - _rate_for(records, "B8", {"OlympiadStyle300"}),
        "derived_from": "ActualTaskPipelineRunV1",
    }


def _measured_failure_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    reasons = Counter(str(record.get("failure_reason", "unspecified")) for record in records if record.get("final_status") == "measured_failure")
    return {"measured_failure_count": sum(reasons.values()), "reasons": dict(sorted(reasons.items()))}


def _check_thresholds(metrics: dict[str, Any], advantage: dict[str, Any], errors: list[str]) -> None:
    b2 = metrics.get("by_baseline", {}).get("B2")
    if not isinstance(b2, dict):
        errors.append("missing_B2_metrics")
        return
    if b2.get("overall_final_theorem_rate", 0.0) < OVERALL_THRESHOLD:
        errors.append(f"overall_final_theorem_rate_below_0_85:{b2.get('overall_final_theorem_rate', 0.0)}")
    if b2.get("safe_reject_success_on_in_target_positive", 0) != 0:
        errors.append(f"in_target_positive_safe_reject_success_nonzero:{b2.get('safe_reject_success_on_in_target_positive')}")
    family_rates = b2.get("family_rates", {})
    for family, threshold in FAMILY_THRESHOLDS.items():
        rate = family_rates.get(family, 0.0) if isinstance(family_rates, dict) else 0.0
        if rate < threshold:
            errors.append(f"{family}_rate_below_{threshold}:{rate}")
    for key, threshold in ADVANTAGE_THRESHOLDS.items():
        value = advantage.get(key, 0.0)
        if value < threshold:
            errors.append(f"{key}_below_{threshold}:{value}")


def _rate_for(records: list[dict[str, Any]], baseline: str, families: set[str] | None = None) -> float:
    selected = [
        record
        for record in records
        if record.get("baseline_id") == baseline
        and _target_status(record) == "in_target_positive"
        and (families is None or _theorem_family(record) in families)
    ]
    success = [record for record in selected if record.get("final_status") == "final_theorem"]
    return _rate(len(success), len(selected))


def _target_status(record: dict[str, Any]) -> str:
    return str(record.get("target_status", record.get("task_metadata", {}).get("target_status", "in_target_positive")))


def _theorem_family(record: dict[str, Any]) -> str:
    return str(record.get("theorem_family", record.get("task_metadata", {}).get("theorem_family", "")))


def _rate(success: int, total: int) -> float:
    return round(success / total, 6) if total else 0.0


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
