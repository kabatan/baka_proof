#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import artifact, load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    errors: list[str] = []
    concrete_rules: set[str] = set()
    family_counts: Counter[str] = Counter()
    checked_successes = 0
    inflated_records: list[str] = []
    for path, record in load_records(run_dir):
        if record.get("baseline_id") != "B2" or record.get("final_status") != "final_theorem":
            continue
        checked_successes += 1
        causality = artifact(run_dir, record, str(record.get("solver_causality_report_ref")))
        compiler = artifact(run_dir, record, str(record.get("compiler_result_refs", [""])[0]))
        if causality is None or compiler is None:
            errors.append(f"{path.name}:missing_causality_or_compiler")
            continue
        causal_rules = [str(rule) for rule in causality.get("used_rule_ids", [])]
        compiler_rules = [str(rule) for rule in compiler.get("used_rule_ids", [])]
        if sorted(causal_rules) != sorted(compiler_rules):
            errors.append(f"{path.name}:rule_binding_mismatch")
            continue
        if len(set(causal_rules)) != len(causal_rules) or len(causal_rules) > 12:
            inflated_records.append(path.name)
        for rule in causal_rules:
            if not rule.startswith("full2d_rule:"):
                errors.append(f"{path.name}:invalid_rule_id:{rule}")
                continue
            concrete_rules.add(rule)
            family_counts[_rule_family(rule)] += 1
    if checked_successes == 0:
        errors.append("no_B2_counted_successes")
    if len(concrete_rules) < 35:
        errors.append(f"used_concrete_rules_below_floor:{len(concrete_rules)}")
    if len(family_counts) < 15:
        errors.append(f"used_rule_families_below_floor:{len(family_counts)}")
    if inflated_records:
        errors.append(f"inflated_or_duplicate_rule_lists:{len(inflated_records)}")
    report = {
        "schema_version": "full2d_used_rule_coverage_v0_4_4_report_1",
        "status": "passed" if not errors else "failed",
        "checked_b2_successes": checked_successes,
        "used_concrete_rules": len(concrete_rules),
        "required_concrete_rules": 35,
        "used_rule_families": len(family_counts),
        "required_rule_families": 15,
        "rule_family_counts": dict(sorted(family_counts.items())),
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _rule_family(rule_id: str) -> str:
    parts = rule_id.split(":")
    return parts[1] if len(parts) >= 3 else rule_id


if __name__ == "__main__":
    raise SystemExit(main())
