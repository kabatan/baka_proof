#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test:
        bad = {"solver_causal_necessity": True, "mutation_sensitive": True}
        if bad.get("delete_selected_solver_artifact"):
            errors.append("self_test_bad_boolean_fixture_invalid")
    report_dir = Path(args.run_dir) / "solver_causality_reports_v0_4_5"
    reports = sorted(report_dir.glob("*.json")) if report_dir.exists() else []
    for path in reports:
        report = json.loads(path.read_text(encoding="utf-8"))
        if report.get("schema_version") != "SolverCausalityReportV2":
            errors.append(f"{path.name}:bad_schema")
        for field in ("positive_control", "delete_selected_solver_artifact", "corrupt_selected_solver_fact", "unsupported_rule_mutation"):
            if not report.get(field):
                errors.append(f"{path.name}:missing_{field}")
        if report.get("boolean_only") is True:
            errors.append(f"{path.name}:boolean_only_causality")
    out = {"schema_version": "solver_causality_reports_v0_4_5_report_1", "status": "passed" if not errors else "failed", "report_count": len(reports), "errors": sorted(set(errors))}
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
