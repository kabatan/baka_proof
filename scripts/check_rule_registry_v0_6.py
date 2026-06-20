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

from scripts.geometry_full2d_v0_6_extraction import write_json
from scripts.geometry_full2d_v0_6_red_cases import evaluate_fixture, load_manifest
from scripts.geometry_full2d_v0_6_rule_checkers import run_rule_fixture_suite
from scripts.geometry_full2d_v0_6_rule_registry import (
    build_rule_registry_v0_6,
    counted_rules,
    run_lean_rule_lemma_check,
    validate_rule_registry_v0_6,
)


def red_case_report(registry: dict[str, Any]) -> dict[str, Any]:
    manifest = load_manifest()
    wanted = {"RC-003": "K-012", "RC-013": "K-029"}
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") in wanted:
            row = evaluate_fixture(fixture)
            rows.append(row)
            expected = wanted[str(fixture.get("red_case_id"))]
            if expected not in row.get("detected_K", []):
                errors.append(f"{fixture.get('red_case_id')}:{expected}_not_detected")
            if not row.get("positive_control_passed"):
                errors.append(f"{fixture.get('red_case_id')}:positive_control_failed")

    counted = counted_rules(registry)
    local_negative_results: dict[str, list[str]] = {}
    identity_only = copy.deepcopy(registry)
    identity_only["rules"] = [
        {
            **copy.deepcopy(counted[0]),
            "rule_id": "full2d_rule:identity_only:01",
            "family": "identity_only",
            "input_patterns": ["same_pattern"],
            "output_pattern": "same_pattern",
            "direct_identity_rule": True,
            "direct_facade_rule": False,
        }
        for _ in range(35)
    ]
    for index, rule in enumerate(identity_only["rules"], start=1):
        rule["rule_id"] = f"full2d_rule:identity_only:{index:02d}"
    local_negative_results["identity_only_registry"] = validate_rule_registry_v0_6(identity_only, release=True)

    alias_inflation = copy.deepcopy(registry)
    first = copy.deepcopy(counted[0])
    alias_inflation["rules"] = []
    for index in range(35):
        rule = copy.deepcopy(first)
        rule["rule_id"] = f"full2d_rule:alias_inflation:{index + 1:02d}"
        if index > 0:
            rule["alias_of"] = "full2d_rule:alias_inflation:01"
        alias_inflation["rules"].append(rule)
    local_negative_results["alias_inflation_registry"] = validate_rule_registry_v0_6(alias_inflation, release=True)

    missing_lemma = copy.deepcopy(registry)
    missing_lemma["rules"][0]["lean_lemma"] = "MathAutoResearch.GeometryFull2D.not_a_real_lemma"
    local_negative_results["missing_lean_lemma"] = validate_rule_registry_v0_6(missing_lemma, release=True)

    missing_fixtures = copy.deepcopy(registry)
    missing_fixtures["rules"][0]["negative_fixtures"] = []
    missing_fixtures["rules"][0]["unsupported_variants"] = []
    local_negative_results["missing_negative_fixtures"] = validate_rule_registry_v0_6(missing_fixtures, release=True)

    missing_mutation = copy.deepcopy(registry)
    missing_mutation["rules"][0]["mutation_sensitive"] = False
    missing_mutation["rules"][0]["mutation_fixtures"] = []
    local_negative_results["missing_mutation_sensitivity"] = validate_rule_registry_v0_6(missing_mutation, release=True)

    expected_markers = {
        "identity_only_registry": ("counted_identity_or_facade_rule", "counted_identity_rule"),
        "alias_inflation_registry": ("counted_alias_rule", "alias_inflation_duplicate_semantics", "counted_rule_family_count_below_15"),
        "missing_lean_lemma": ("lean_lemma_missing",),
        "missing_negative_fixtures": ("empty_rule_list_field",),
        "missing_mutation_sensitivity": ("counted_rule_not_mutation_sensitive", "counted_rule_missing_mutation_fixtures"),
    }
    for name, markers in expected_markers.items():
        result = local_negative_results[name]
        if not any(any(marker in error for marker in markers) for error in result):
            errors.append(f"local_negative_unrejected:{name}")

    return {
        "schema_version": "RuleRegistryV06RedCaseReport",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "manifest_cases": rows,
        "local_negative_results": local_negative_results,
    }


def check_rule_registry_v0_6(*, release: bool, red_cases: bool) -> dict[str, Any]:
    registry = build_rule_registry_v0_6()
    errors = validate_rule_registry_v0_6(registry, release=release)
    fixture_report = run_rule_fixture_suite(registry)
    if fixture_report["status"] != "passed":
        errors.extend(f"rule_fixture_suite:{error}" for error in fixture_report.get("errors", []))
    lean_report = run_lean_rule_lemma_check()
    if lean_report["status"] != "passed":
        errors.append("lean_rule_lemma_file_not_elaborated")
    red_report = red_case_report(registry) if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    counted = counted_rules(registry)
    return {
        "schema_version": "CheckRuleRegistryV06Report",
        "checker_name": "check_rule_registry_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "release_mode": release,
        "registry_hash": registry.get("registry_hash"),
        "rule_count": len(registry.get("rules", [])),
        "counted_rule_count": len(counted),
        "counted_rule_family_count": len({str(rule.get("family")) for rule in counted}),
        "helper_rule_count": len(registry.get("rules", [])) - len(counted),
        "lean_report": lean_report,
        "rule_fixture_suite": fixture_report,
        "red_cases": red_report,
        "registry": registry,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 semantic rule registry.")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--registry-output", type=Path)
    args = parser.parse_args()
    if not args.release:
        print("error: --release is required for WP07 acceptance", file=sys.stderr)
        return 2
    report = check_rule_registry_v0_6(release=args.release, red_cases=args.red_cases)
    if args.registry_output:
        target = args.registry_output if args.registry_output.is_absolute() else ROOT / args.registry_output
        write_json(target, report["registry"])
    if args.output:
        target = args.output if args.output.is_absolute() else ROOT / args.output
        serializable = {key: value for key, value in report.items() if key != "registry"}
        write_json(target, serializable)
    print(json.dumps({key: value for key, value in report.items() if key != "registry"}, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
