#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=False)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = {
        "schema_version": "SolverCausalityReportsCheckV05",
        "status": "failed",
        "errors": ["wp12_solver_causality_reports_pending"],
        "run_dir": args.run_dir,
        "self_test": args.self_test,
        "live_destructive_rerun_fraction": 0.0,
        "precomputed_report_fraction": 1.0,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
