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
    errors: list[str] = []
    if not path.exists():
        errors.append("missing_matrix_summary")
    else:
        summary = json.loads(path.read_text(encoding="utf-8"))
        if summary.get("outcome_source") != "actual_task_pipeline_runs_v0_4_5":
            errors.append("matrix_not_derived_from_actual_runs")
    report = {"schema_version": "matrix_evidence_v0_4_5_report_1", "status": "passed" if not errors else "failed", "errors": errors}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
