#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifact, load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test:
        bad = {"solver_causal_necessity": False}
        if bad["solver_causal_necessity"] is not False:
            errors.append("self_test_bad_causality_fixture_invalid")
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    records = load_records(run_dir)
    for path, record in records:
        causality = artifact(run_dir, record, str(record.get("solver_causality_report_ref")))
        if causality is None:
            errors.append(f"{path.name}:missing_causality_report")
            continue
        if record.get("final_status") == "final_theorem":
            if causality.get("solver_causal_necessity") is not True:
                errors.append(f"{path.name}:solver_causal_necessity_not_true")
            if causality.get("mutation_sensitive") is not True:
                errors.append(f"{path.name}:mutation_sensitive_not_true")
        else:
            if causality.get("solver_causal_necessity") is not False:
                errors.append(f"{path.name}:measured_failure_causality_not_false")
            if not causality.get("failure_reason"):
                errors.append(f"{path.name}:measured_failure_missing_reason")
        if causality.get("compiler_result_refs") != record.get("compiler_result_refs"):
            errors.append(f"{path.name}:causality_compiler_refs_mismatch")
        if not causality.get("used_rule_ids"):
            errors.append(f"{path.name}:causality_missing_used_rule_ids")
    report = {"schema_version": "solver_causality_reports_v0_4_4_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
