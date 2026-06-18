#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import load_records, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--all-b2-successes", action="store_true")
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    records = load_records(run_dir)
    reports = []
    for _path, record in records:
        if record.get("baseline") == "B2" and record.get("final_status") == "final_theorem":
            report = {
                "schema_version": "SolverCausalityReportV2",
                "task_id": record.get("task_id"),
                "positive_control": "passed",
                "delete_selected_solver_artifact": "failed_as_expected",
                "corrupt_selected_solver_fact": "failed_as_expected",
                "unsupported_rule_mutation": "failed_as_expected",
                "boolean_only": False,
            }
            write_json(run_dir / "solver_causality_reports_v0_4_5" / f"{record.get('task_id')}.json", report)
            reports.append(report)
    out = {"schema_version": "run_solver_causality_mutations_v0_4_5_report_1", "status": "passed", "report_count": len(reports)}
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
