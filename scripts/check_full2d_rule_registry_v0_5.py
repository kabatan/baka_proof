#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d, validate_rule_registry_full2d
from scripts.geometry_full2d_v0_5_schemas import validate_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = self_test_report() if args.self_test else check_rule_registry_v0_5()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_rule_registry_v0_5() -> dict[str, Any]:
    registry = build_rule_registry_full2d()
    payload = registry.to_dict()
    errors = validate_rule_registry_payload(payload)
    errors.extend(validate_rule_registry_full2d(registry))
    return {
        "schema_version": "RuleRegistryFull2DCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "registry_hash": registry.registry_hash(),
        "rule_count": len(registry.rules),
        "counted_rule_count": sum(1 for rule in registry.rules if rule.counted),
        "counted_rule_family_count": len({rule.rule_family for rule in registry.rules if rule.counted}),
        "helper_rule_count": sum(1 for rule in registry.rules if not rule.counted),
    }


def validate_rule_registry_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_payload(payload, current_head="test-head")
    rules = payload.get("rules")
    if not isinstance(rules, list):
        return sorted(set(errors + ["rules_not_list"]))
    counted = [rule for rule in rules if isinstance(rule, dict) and rule.get("counted") is True]
    if len(counted) < 150:
        errors.append(f"counted_rule_count_below_150:{len(counted)}")
    families = {str(rule.get("rule_family")) for rule in counted}
    if len(families) < 25:
        errors.append(f"counted_rule_family_count_below_25:{len(families)}")
    ids = [str(rule.get("rule_id")) for rule in rules if isinstance(rule, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_rule_ids")
    required = {
        "rule_id",
        "rule_family",
        "input_patterns",
        "output_pattern",
        "required_side_conditions",
        "generated_obligations",
        "lean_template_id",
        "independent_checker",
        "positive_fixtures",
        "negative_fixtures",
        "mutation_fixtures",
        "direct_identity_rule",
        "direct_facade_rule",
        "counted",
    }
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"bad_rule:{index}")
            continue
        missing = sorted(required - set(rule))
        errors.extend(f"missing_rule_field:{index}:{key}" for key in missing)
        if rule.get("counted") is not True:
            continue
        inputs = set(str(item) for item in rule.get("input_patterns", []) if isinstance(rule.get("input_patterns"), list))
        output = str(rule.get("output_pattern", ""))
        if rule.get("direct_identity_rule") is True or rule.get("direct_facade_rule") is True:
            errors.append(f"counted_identity_or_facade_rule:{rule.get('rule_id')}")
        if output in inputs:
            errors.append(f"counted_rule_output_equals_input:{rule.get('rule_id')}")
        if output in {"TARGET", "TARGET_GOAL", "target_goal"}:
            errors.append(f"naked_target_rule_counted_success:{rule.get('rule_id')}")
        for key in ["input_patterns", "required_side_conditions", "generated_obligations", "positive_fixtures", "negative_fixtures", "mutation_fixtures"]:
            value = rule.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"counted_rule_missing_{key}:{rule.get('rule_id')}")
        if not rule.get("lean_template_id"):
            errors.append(f"counted_rule_missing_lean_template_id:{rule.get('rule_id')}")
        if not rule.get("independent_checker"):
            errors.append(f"counted_rule_missing_independent_checker:{rule.get('rule_id')}")
    return sorted(set(errors))


def self_test_report() -> dict[str, Any]:
    positive = check_rule_registry_v0_5()
    registry = build_rule_registry_full2d().to_dict()
    identity_payload = copy.deepcopy(registry)
    identity_payload["rules"][0]["direct_identity_rule"] = True
    identity_payload["rules"][0]["output_pattern"] = identity_payload["rules"][0]["input_patterns"][0]
    identity_errors = validate_rule_registry_payload(identity_payload)
    naked_payload = copy.deepcopy(registry)
    naked_payload["rules"][1]["direct_facade_rule"] = True
    naked_payload["rules"][1]["output_pattern"] = "target_goal"
    naked_errors = validate_rule_registry_payload(naked_payload)
    fixture_payload = copy.deepcopy(registry)
    fixture_payload["rules"][2]["mutation_fixtures"] = []
    fixture_errors = validate_rule_registry_payload(fixture_payload)
    errors: list[str] = []
    if positive["status"] != "passed":
        errors.append("positive_rule_registry_failed")
    if not any(error.startswith("counted_identity_or_facade_rule") or error == "identity_rule_counted_success" for error in identity_errors):
        errors.append("identity_rule_registry_not_rejected")
    if not any(error.startswith("naked_target_rule_counted_success") for error in naked_errors):
        errors.append("naked_target_rule_registry_not_rejected")
    if not any("mutation_fixtures" in error for error in fixture_errors):
        errors.append("missing_mutation_fixture_not_rejected")
    return {
        "schema_version": "RuleRegistryFull2DSelfTestV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "positive": positive,
        "negative_errors": {
            "identity_rule_registry": identity_errors,
            "naked_target_rule_registry": naked_errors,
            "missing_mutation_fixture": fixture_errors,
        },
    }


if __name__ == "__main__":
    raise SystemExit(main())
