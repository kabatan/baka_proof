#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_5_run_checks import artifacts_for, load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test:
        bad = {"facts": [{"conclusion": "collinear A B C"}]}
        if bad["facts"][0].get("independent_checker_ref"):
            errors.append("self_test_bad_fact_fixture_invalid")
    records = load_records(Path(args.run_dir))
    for path, record in records:
        for engine in artifacts_for(Path(args.run_dir), record, "engine_output_refs"):
            for fact in engine.get("facts", []):
                if not fact.get("independent_checker_ref") or not fact.get("certificate_ref"):
                    errors.append(f"{path.name}:solver_fact_missing_checker_or_certificate")
    report = {"schema_version": "solver_fact_independent_checkers_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
