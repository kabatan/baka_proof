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
        bad = {"used_rule_ids": [], "selected_solver_derivation_ref": ""}
        if bad["used_rule_ids"] or bad["selected_solver_derivation_ref"]:
            errors.append("self_test_bad_compiler_fixture_invalid")
    records = load_records(Path(args.run_dir))
    for path, record in records:
        for compiler in artifacts_for(Path(args.run_dir), record, "compiler_result_refs"):
            if not compiler.get("used_rule_ids"):
                errors.append(f"{path.name}:compiler_missing_used_rule_ids")
            if not compiler.get("selected_solver_derivation"):
                errors.append(f"{path.name}:compiler_missing_selected_solver_derivation")
    report = {"schema_version": "compiler_evidence_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
