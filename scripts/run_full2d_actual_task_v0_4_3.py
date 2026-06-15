from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.task_pipeline import execute_actual_task_pipeline_v0_4_3  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", default="full2d-positive-0000")
    parser.add_argument("--baseline-id", default="B2")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_4_3.yaml")
    parser.add_argument("--corpus-root", default="benchmarks/geometry_full2d")
    args = parser.parse_args()

    try:
        report = execute_actual_task_pipeline_v0_4_3(
            task_id=args.task_id,
            baseline_id=args.baseline_id,
            run_dir=Path(args.run_dir),
            config_path=Path(args.config),
            corpus_root=Path(args.corpus_root),
        )
    except Exception as exc:
        report = {
            "schema_version": "1.0.0",
            "status": "failed",
            "task_id": args.task_id,
            "baseline_id": args.baseline_id,
            "error": str(exc),
        }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
