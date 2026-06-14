from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_full2d_proof_artifacts import check_proof_artifacts  # noqa: E402

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    errors = check_metrics(Path(args.run_dir))
    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


def check_metrics(run_dir: Path) -> list[str]:
    summary_path = run_dir / "matrix_summary.json"
    results_path = run_dir / "task_results.jsonl"
    if not summary_path.exists():
        return [f"missing_matrix_summary:{summary_path.as_posix()}"]
    if not results_path.exists():
        return [f"missing_task_results:{results_path.as_posix()}"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    results = [json.loads(line) for line in results_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors: list[str] = []
    if not summary.get("release_frozen"):
        errors.append("I-000_matrix_run_not_release_frozen")
    overall_rate = float(summary.get("overall_final_theorem_rate", 0.0))
    if overall_rate < 0.85:
        errors.append(f"I-overall-rate-below-threshold:{overall_rate:.4f}<0.8500")
    for family, threshold in FAMILY_THRESHOLDS.items():
        rate = float(summary.get("family_rates", {}).get(family, {}).get("rate", 0.0))
        if rate < threshold:
            errors.append(f"I-family-rate-below-threshold:{family}:{rate:.4f}<{threshold:.4f}")
    for item in results:
        if item.get("target_status") == "in_target_positive" and item.get("safe_reject_counted_as_success"):
            errors.append(f"K-003_safe_reject_counted_positive:{item.get('task_id')}")
            break
        if item.get("fixture_flag"):
            errors.append(f"K-003_fixture_result_counted:{item.get('task_id')}")
            break
    final_count = sum(1 for item in results if item.get("final_theorem"))
    if final_count:
        errors.extend(f"K-002_proof_artifact_validation:{error}" for error in check_proof_artifacts(run_dir))
    return sorted(set(errors))


if __name__ == "__main__":
    raise SystemExit(main())
