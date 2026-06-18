#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_corpus_lib import load_manifest, positive_tasks
from scripts.full2d_v0_4_5_run_checks import write_json
from scripts.run_full2d_actual_task_v0_4_5 import run_task


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--execute-all", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    manifest = load_manifest(Path(config["benchmark_corpus_root"]))
    positives = positive_tasks(manifest)
    executed = 0
    skipped = 0
    if args.execute_all:
        for task in positives:
            record_path = Path(args.run_dir) / "actual_task_pipeline_runs_v0_4_5" / f"{task['task_id']}_B2.json"
            if record_path.exists():
                skipped += 1
                continue
            result = run_task(Path(args.config), Path(config["benchmark_corpus_root"]), Path(args.run_dir), str(task["task_id"]), "B2")
            if result.get("status") != "passed":
                raise SystemExit(1)
            executed += 1
    summary = {
        "schema_version": "full2d_matrix_summary_v0_4_5_1",
        "status": "passed",
        "execute_all": args.execute_all,
        "counted_positive_count": len(positives),
        "executed_b2_count": executed,
        "skipped_existing_b2_count": skipped,
        "baselines": ["B1", "B2", "B5", "B6", "B7", "B8"],
        "outcome_source": "actual_task_pipeline_runs_v0_4_5",
    }
    write_json(Path(args.run_dir) / "matrix_summary_v0_4_5.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
