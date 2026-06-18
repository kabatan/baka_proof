#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_metrics(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_metrics(run_dir: Path) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    records = load_records(run_dir)
    b2 = [record for record in records if record.get("baseline_id") == "B2"]
    counted = len({str(record.get("task_id")) for record in b2})
    b2_success = [record for record in b2 if record.get("final_status") == "final_theorem"]
    causality_reports = load_causality_reports(run_dir)
    causal_tasks = {
        str(report.get("task_id"))
        for report in causality_reports
        if report.get("destructive_causality_passed") is True and report.get("live_rerun_status") == "fresh_temp_dirs_with_command_logs"
    }
    errors: list[str] = []
    if counted == 0:
        errors.append("empty_metrics_no_b2_records")
    baselines_present = sorted({str(record.get("baseline_id")) for record in records})
    missing_baselines = sorted(set(REQUIRED_BASELINES) - set(baselines_present))
    if missing_baselines:
        errors.append("b2_only_or_missing_baselines:" + ",".join(missing_baselines))
    b2_rate = len(b2_success) / counted if counted else 0.0
    causal_rate = len([record for record in b2_success if str(record.get("task_id")) in causal_tasks]) / counted if counted else 0.0
    destructive_pass_rate = len(causal_tasks) / len(b2_success) if b2_success else 0.0
    non_target_fraction = fraction(b2_success, "has_non_target_intermediate")
    construction_fraction = fraction(b2_success, "has_construction_case_certificate")
    direct_facade_fraction = fraction(b2_success, "direct_or_wrapped_facade_success")
    by_baseline = baseline_success_rates(records)
    advantage = {
        "B2_minus_B1_overall": round(by_baseline.get("B2", 0.0) - by_baseline.get("B1", 0.0), 6),
        "B2_minus_B5_construction_subset": round(by_baseline.get("B2", 0.0) - by_baseline.get("B5", 0.0), 6),
        "B2_minus_B6_algebraic_metric_subset": round(by_baseline.get("B2", 0.0) - by_baseline.get("B6", 0.0), 6),
        "B2_minus_B7_order_case_subset": round(by_baseline.get("B2", 0.0) - by_baseline.get("B7", 0.0), 6),
    }
    threshold_checks = {
        "B2_final_theorem_rate": b2_rate >= 0.70,
        "B2_solver_causal_rate": causal_rate >= 0.70,
        "destructive_causality_pass_rate": destructive_pass_rate == 1.0,
        "non_target_intermediate_fraction": non_target_fraction >= 0.50,
        "construction_case_certificate_success_fraction": construction_fraction >= 0.40,
        "direct_or_wrapped_facade_fraction": direct_facade_fraction <= 0.10,
        "B2_minus_B1_overall": advantage["B2_minus_B1_overall"] >= 0.15,
        "B2_minus_B5_construction_subset": advantage["B2_minus_B5_construction_subset"] >= 0.10,
        "B2_minus_B6_algebraic_metric_subset": advantage["B2_minus_B6_algebraic_metric_subset"] >= 0.10,
        "B2_minus_B7_order_case_subset": advantage["B2_minus_B7_order_case_subset"] >= 0.05,
    }
    errors.extend(f"threshold_failed:{name}" for name, passed in threshold_checks.items() if not passed)
    if any(field in json.dumps(records) for field in ["theorem_family", "target_shape_id", "expected_outcome", "label_derived_metric"]):
        errors.append("label_or_shape_derived_metric_field_present")
    measured_failures = [record for record in records if record.get("final_status") == "measured_failure"]
    report = {
        "schema_version": "Full2DMetricsCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "counted_b2_records": counted,
        "B2_final_theorem_count": len(b2_success),
        "B2_final_theorem_rate": round(b2_rate, 6),
        "B2_solver_causal_rate": round(causal_rate, 6),
        "destructive_causality_pass_rate": round(destructive_pass_rate, 6),
        "non_target_intermediate_success_fraction": round(non_target_fraction, 6),
        "construction_case_certificate_success_fraction": round(construction_fraction, 6),
        "direct_wrapped_facade_fraction": round(direct_facade_fraction, 6),
        "baseline_success_rates": by_baseline,
        "baseline_advantage": advantage,
        "measured_failure_count": len(measured_failures),
        "measured_failure_by_baseline": measured_failure_counts(records),
        "threshold_checks": threshold_checks,
        "freshness_hash_binding": {
            "record_git_heads": sorted({str(record.get("git_head")) for record in records}),
            "record_run_dir_hashes": sorted({str(record.get("release_run_dir_hash")) for record in records})[:5],
        },
    }
    write_json(run_dir / "full2d_metrics_report_v0_5.json", report)
    return report


def fraction(records: list[dict[str, Any]], key: str) -> float:
    if not records:
        return 0.0
    return len([record for record in records if record.get(key) is True]) / len(records)


def baseline_success_rates(records: list[dict[str, Any]]) -> dict[str, float]:
    rates: dict[str, float] = {}
    for baseline in REQUIRED_BASELINES:
        rows = [record for record in records if record.get("baseline_id") == baseline]
        rates[baseline] = round(len([record for record in rows if record.get("final_status") == "final_theorem"]) / len(rows), 6) if rows else 0.0
    return rates


def measured_failure_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {baseline: 0 for baseline in REQUIRED_BASELINES}
    for record in records:
        baseline = str(record.get("baseline_id"))
        if baseline in counts and record.get("final_status") == "measured_failure":
            counts[baseline] += 1
    return counts


def load_records(run_dir: Path) -> list[dict[str, Any]]:
    records_dir = run_dir / "actual_task_pipeline_runs"
    records: list[dict[str, Any]] = []
    if records_dir.exists():
        for item in sorted(records_dir.glob("*.json")):
            payload = json.loads(item.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                records.append(payload)
    return records


def load_causality_reports(run_dir: Path) -> list[dict[str, Any]]:
    reports_dir = run_dir / "solver_causality_reports"
    reports: list[dict[str, Any]] = []
    if reports_dir.exists():
        for item in sorted(reports_dir.glob("*.json")):
            payload = json.loads(item.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                reports.append(payload)
    return reports


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
