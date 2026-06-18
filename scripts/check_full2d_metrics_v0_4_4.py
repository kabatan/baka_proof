#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import FAMILY_FLOORS, load_manifest, positive_tasks, resolve  # noqa: E402
from scripts.full2d_v0_4_4_run_checks import artifact, load_records  # noqa: E402


FAMILY_RATE_FLOORS = {
    "Full2DCore500": 0.95,
    "IncidenceParallelPerp350": 0.92,
    "AngleCyclic450": 0.90,
    "Construction450": 0.85,
    "MetricRatioArea350": 0.85,
    "Transformation250": 0.80,
    "OrderCase250": 0.75,
    "Algebraic250": 0.75,
    "Inequality150": 0.70,
    "OlympiadStyle300": 0.65,
    "HardHoldout50": 0.50,
}

ALGEBRAIC_METRIC_FAMILIES = {
    "AngleCyclic450",
    "MetricRatioArea350",
    "Algebraic250",
    "Inequality150",
    "OlympiadStyle300",
    "HardHoldout50",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_4_4.yaml")
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = check_metrics(resolve(Path(args.config)), resolve(Path(args.run_dir)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_metrics(config_path: Path, run_dir: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifest = load_manifest(resolve(Path(str(config["benchmark_corpus_root"]))))
    tasks = positive_tasks(manifest)
    task_by_id = {str(task["task_id"]): task for task in tasks}
    records = [record for _path, record in load_records(run_dir) if str(record.get("task_id")) in task_by_id]
    errors: list[str] = []
    b2_records = [record for record in records if record.get("baseline_id") == "B2"]
    b2_successes = [record for record in b2_records if record.get("final_status") == "final_theorem"]
    overall_rate = _rate(len(b2_successes), len(tasks))
    if overall_rate < 0.85:
        errors.append(f"B2_overall_rate_below_floor:{overall_rate:.6f}")

    family_summary: dict[str, dict[str, Any]] = {}
    for family, expected_count in FAMILY_FLOORS.items():
        family_records = [record for record in b2_records if record.get("theorem_family") == family]
        successes = [record for record in family_records if record.get("final_status") == "final_theorem"]
        rate = _rate(len(successes), len(family_records))
        floor = FAMILY_RATE_FLOORS[family]
        family_summary[family] = {
            "record_count": len(family_records),
            "expected_count": expected_count,
            "final_theorem": len(successes),
            "success_rate": rate,
            "required_rate": floor,
            "passed": len(family_records) == expected_count and rate >= floor,
        }
        if len(family_records) != expected_count:
            errors.append(f"{family}:record_count:{len(family_records)}:expected:{expected_count}")
        if rate < floor:
            errors.append(f"{family}:success_rate_below_floor:{rate:.6f}:{floor:.2f}")

    advantage_summary = {
        "B2_minus_B1_overall": _advantage(records, "B2", "B1", set(FAMILY_FLOORS)),
        "B2_minus_B5_construction_subset": _advantage(records, "B2", "B5", {"Construction450"}),
        "B2_minus_B6_algebraic_metric_subset": _advantage(records, "B2", "B6", ALGEBRAIC_METRIC_FAMILIES),
        "B2_minus_B7_order_case_subset": _advantage(records, "B2", "B7", {"OrderCase250"}),
        "B8": {"status": "not_applicable_model_provider_not_used"},
    }
    floors = {
        "B2_minus_B1_overall": 0.25,
        "B2_minus_B5_construction_subset": 0.15,
        "B2_minus_B6_algebraic_metric_subset": 0.15,
        "B2_minus_B7_order_case_subset": 0.10,
    }
    for key, floor in floors.items():
        value = float(advantage_summary[key]["advantage"])
        if value < floor:
            errors.append(f"{key}_below_floor:{value:.6f}:{floor:.2f}")

    causality_success = 0
    for record in b2_successes:
        causality = artifact(run_dir, record, str(record.get("solver_causality_report_ref")))
        if causality and causality.get("solver_causal_necessity") is True:
            causality_success += 1
    causality_fraction = _rate(causality_success, len(b2_successes))
    if causality_fraction != 1.0:
        errors.append(f"solver_causal_success_fraction_not_1:{causality_fraction:.6f}")

    category_counts = Counter(str(task_by_id[str(record["task_id"])].get("category")) for record in b2_successes)
    if category_counts["ExternalGoalPreserved"] < 500:
        errors.append(f"ExternalGoalPreserved_success_count_below_floor:{category_counts['ExternalGoalPreserved']}")
    if category_counts["SealedSolverChallenge"] < 700:
        errors.append(f"SealedSolverChallenge_success_count_below_floor:{category_counts['SealedSolverChallenge']}")

    report = {
        "schema_version": "full2d_metrics_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "b2_overall": {
            "positive_task_count": len(tasks),
            "final_theorem": len(b2_successes),
            "success_rate": overall_rate,
            "required_rate": 0.85,
        },
        "family_floor_summary": family_summary,
        "advantage_summary": advantage_summary,
        "solver_causal_success_fraction": causality_fraction,
        "category_success_summary": dict(category_counts),
        "errors": sorted(set(errors)),
    }
    return report


def _advantage(records: list[dict[str, Any]], baseline_a: str, baseline_b: str, families: set[str]) -> dict[str, Any]:
    a = [record for record in records if record.get("baseline_id") == baseline_a and record.get("theorem_family") in families]
    b = [record for record in records if record.get("baseline_id") == baseline_b and record.get("theorem_family") in families]
    a_rate = _rate(sum(1 for record in a if record.get("final_status") == "final_theorem"), len(a))
    b_rate = _rate(sum(1 for record in b if record.get("final_status") == "final_theorem"), len(b))
    return {
        "baseline_a": baseline_a,
        "baseline_b": baseline_b,
        "families": sorted(families),
        "a_count": len(a),
        "b_count": len(b),
        "a_success_rate": a_rate,
        "b_success_rate": b_rate,
        "advantage": a_rate - b_rate,
    }


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


if __name__ == "__main__":
    raise SystemExit(main())
