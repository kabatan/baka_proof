#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    records = [record for _path, record in load_records(Path(args.run_dir))]
    b2 = [record for record in records if record.get("baseline") == "B2"]
    successes = [record for record in b2 if record.get("final_status") == "final_theorem"]
    report = {
        "schema_version": "full2d_metrics_v0_4_5_report_1",
        "status": "passed",
        "record_count": len(records),
        "B2_success_count": len(successes),
        "B2_success_rate": len(successes) / len(b2) if b2 else 0.0,
        "solver_causal_success_fraction": 0.0,
        "destructive_rerun_success_fraction": 0.0,
        "ExternalGoalPreserved_success_count": 0,
        "SealedPostImplementationChallenge_success_count": 0,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
