#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d_v0_4_5.rule_registry import RULES
from scripts.full2d_v0_4_5_run_checks import artifacts_for, load_records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    if args.self_test and "missing.rule" in RULES:
        errors.append("self_test_registry_fixture_invalid")
    records = load_records(Path(args.run_dir))
    for path, record in records:
        for compiler in artifacts_for(Path(args.run_dir), record, "compiler_result_refs"):
            selected = compiler.get("selected_solver_derivation", {})
            if selected.get("schema_version") != "SelectedSolverDerivationV1":
                errors.append(f"{path.name}:bad_selected_derivation_schema")
            for step in selected.get("solver_steps", []):
                if step.get("rule_id") not in RULES:
                    errors.append(f"{path.name}:selected_derivation_unknown_rule:{step.get('rule_id')}")
                if not step.get("certificate_ref") or not step.get("independent_checker_ref"):
                    errors.append(f"{path.name}:selected_step_missing_certificate_or_checker")
    report = {"schema_version": "selected_solver_derivation_v0_4_5_report_1", "status": "passed" if not errors else "failed", "record_count": len(records), "errors": sorted(set(errors))}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
