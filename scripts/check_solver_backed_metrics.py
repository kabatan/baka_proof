from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


THRESHOLDS = {
    "B2": {
        "solver_backed_final_theorem_count": 8,
        "geotrace_solver_backed_final_theorem_count": 5,
        "construction_solver_backed_final_theorem_count": 2,
    },
    "B4": {
        "solver_backed_final_theorem_count": 5,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    observed: dict[str, dict[str, Any]] = {}
    for baseline_id, thresholds in THRESHOLDS.items():
        metrics_path = run_dir / f"metrics_{baseline_id}.json"
        if not metrics_path.exists():
            errors.append(f"{baseline_id}:missing_metrics")
            continue
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        values = metrics.get("metric_values", {})
        observed[baseline_id] = {key: values.get(key) for key in thresholds}
        for key, minimum in thresholds.items():
            value = values.get(key)
            if not isinstance(value, int) or value < minimum:
                errors.append(f"{baseline_id}:{key}:expected_at_least_{minimum}:observed_{value}")
    payload = {"status": "failed" if errors else "passed", "observed": observed, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
