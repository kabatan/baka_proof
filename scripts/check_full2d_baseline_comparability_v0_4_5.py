#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    path = Path(args.run_dir) / "matrix_summary_v0_4_5.json"
    errors = [] if path.exists() else ["missing_matrix_summary"]
    report = {"schema_version": "baseline_comparability_v0_4_5_report_1", "status": "passed" if not errors else "failed", "errors": errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
