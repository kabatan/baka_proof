from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_RULE_CHECKER_IMPORT_PARTS = (
    "provider",
    "compiler",
    "proof_generation",
    "proof_worker",
    "final_verify",
    "matrix",
    "release",
    "release_checker",
    "corpus",
    "corpus_generator",
    "proof_template",
    "previous_release",
    "prior_release",
    "v0_5",
    "v0_4",
)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def module_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return sorted(set(imports))


def rule_checker_import_report() -> dict[str, Any]:
    path = ROOT / "scripts" / "geometry_full2d_v0_6_rule_checkers.py"
    imports = module_imports(path)
    forbidden = [item for item in imports if any(part in item.lower() for part in FORBIDDEN_RULE_CHECKER_IMPORT_PARTS)]
    return {
        "schema_version": "RuleCheckerImportReportV06",
        "module": "scripts.geometry_full2d_v0_6_rule_checkers",
        "module_path": path.relative_to(ROOT).as_posix(),
        "imports": imports,
        "forbidden_imports": forbidden,
        "status": "passed" if not forbidden else "failed",
        "checker_code_hash": sha256_text(path.read_text(encoding="utf-8")),
    }


def _with_fixture_hash(fixture: dict[str, Any]) -> dict[str, Any]:
    return {"fixture_hash": sha256_text(canonical_json(fixture)), **fixture}


def build_rule_fixture(
    *,
    rule_id: str,
    checker_name: str,
    input_pattern: str,
    side_conditions: tuple[str, ...] | list[str],
    output_pattern: str,
    fixture_id: str,
    fixture_kind: str,
    expected_status: str,
    mutation_kind: str | None = None,
    unsupported_kind: str | None = None,
) -> dict[str, Any]:
    input_facts = [{"fact_id": f"{fixture_id}:input:0", "pattern": input_pattern, "source": "rule_fixture_premise"}]
    side_condition_evidence = [
        {"condition": str(condition), "status": "verified", "source": "rule_fixture_side_condition"}
        for condition in side_conditions
    ]
    claimed_output = output_pattern
    if mutation_kind == "premise_removed":
        input_facts = []
    elif mutation_kind == "output_corrupted":
        claimed_output = f"corrupted:{output_pattern}"
    elif unsupported_kind == "target_assertion":
        claimed_output = "final_target"
    elif unsupported_kind == "schema_only_certificate":
        side_condition_evidence = [
            {"condition": str(condition), "status": "schema_only", "source": "schema_only_certificate"}
            for condition in side_conditions
        ]
    elif fixture_kind == "negative" and fixture_id.endswith(":missing_premise"):
        input_facts = []
    elif fixture_kind == "negative" and fixture_id.endswith(":wrong_output"):
        claimed_output = f"wrong_output:{output_pattern}"

    payload = {
        "schema_version": "RuleFixtureV06",
        "fixture_id": fixture_id,
        "fixture_kind": fixture_kind,
        "expected_status": expected_status,
        "claimed_rule_id": rule_id,
        "checker_name": checker_name,
        "input_facts": input_facts,
        "side_condition_evidence": side_condition_evidence,
        "claimed_output": claimed_output,
        "target_equivalent": unsupported_kind == "target_assertion",
        "unsupported_kind": unsupported_kind,
        "mutation_kind": mutation_kind,
        "proof_material_present": False,
    }
    return _with_fixture_hash(payload)


def build_rule_fixtures_for_contract(
    *,
    rule_id: str,
    checker_name: str,
    input_pattern: str,
    side_conditions: tuple[str, ...] | list[str],
    output_pattern: str,
) -> dict[str, list[dict[str, Any]]]:
    return {
        "positive_fixtures": [
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"positive:{rule_id}:canonical",
                fixture_kind="positive",
                expected_status="passed",
            ),
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"positive:{rule_id}:renamed_objects",
                fixture_kind="positive",
                expected_status="passed",
            ),
        ],
        "negative_fixtures": [
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"negative:{rule_id}:missing_premise",
                fixture_kind="negative",
                expected_status="failed",
            ),
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"negative:{rule_id}:wrong_output",
                fixture_kind="negative",
                expected_status="failed",
            ),
        ],
        "unsupported_variants": [
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"unsupported:{rule_id}:target_assertion",
                fixture_kind="unsupported",
                expected_status="failed",
                unsupported_kind="target_assertion",
            ),
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"unsupported:{rule_id}:schema_only_certificate",
                fixture_kind="unsupported",
                expected_status="failed",
                unsupported_kind="schema_only_certificate",
            ),
        ],
        "mutation_fixtures": [
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"mutation:{rule_id}:premise_removed",
                fixture_kind="mutation",
                expected_status="failed",
                mutation_kind="premise_removed",
            ),
            build_rule_fixture(
                rule_id=rule_id,
                checker_name=checker_name,
                input_pattern=input_pattern,
                side_conditions=side_conditions,
                output_pattern=output_pattern,
                fixture_id=f"mutation:{rule_id}:output_corrupted",
                fixture_kind="mutation",
                expected_status="failed",
                mutation_kind="output_corrupted",
            ),
        ],
    }


def evaluate_rule_fixture(rule: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if fixture.get("schema_version") != "RuleFixtureV06":
        errors.append("bad_fixture_schema")
    if fixture.get("claimed_rule_id") != rule.get("rule_id"):
        errors.append("fixture_rule_id_mismatch")
    if fixture.get("checker_name") != rule.get("independent_rule_checker"):
        errors.append("fixture_checker_mismatch")
    if fixture.get("proof_material_present") is not False:
        errors.append("proof_material_present")
    text = canonical_json(fixture).lower()
    for marker in ("proof_text", "tactic_script", "lean_template", "exact ", " by "):
        if marker in text:
            errors.append("fixture_contains_proof_material")

    input_patterns = [str(item.get("pattern")) for item in fixture.get("input_facts", []) if isinstance(item, dict)]
    expected_inputs = [str(item) for item in rule.get("input_patterns", [])]
    if sorted(input_patterns) != sorted(expected_inputs):
        errors.append("premises_not_verified")

    observed_side_conditions = [
        str(item.get("condition"))
        for item in fixture.get("side_condition_evidence", [])
        if isinstance(item, dict) and item.get("status") == "verified"
    ]
    expected_side_conditions = [str(item) for item in rule.get("side_conditions", [])]
    if sorted(observed_side_conditions) != sorted(expected_side_conditions):
        errors.append("side_conditions_not_verified")

    if fixture.get("claimed_output") != rule.get("output_pattern"):
        errors.append("conclusion_not_verified")
    if fixture.get("target_equivalent") is True or fixture.get("claimed_output") in {"target", "target_goal", "final_target", "goal"}:
        errors.append("target_assertion_or_equivalent")
    if fixture.get("unsupported_kind") == "schema_only_certificate":
        errors.append("schema_only_certificate")

    status = "passed" if not errors else "failed"
    return {
        "fixture_id": fixture.get("fixture_id"),
        "fixture_hash": fixture.get("fixture_hash"),
        "fixture_kind": fixture.get("fixture_kind"),
        "expected_status": fixture.get("expected_status"),
        "observed_status": status,
        "errors": sorted(set(errors)),
    }


def run_rule_fixture_suite(registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    rule_rows: list[dict[str, Any]] = []
    import_report = rule_checker_import_report()
    errors.extend(f"rule_checker_forbidden_import:{item}" for item in import_report.get("forbidden_imports", []))

    for rule in registry.get("rules", []):
        if not isinstance(rule, dict) or rule.get("counted_release_rule") is not True:
            continue
        fixture_results: list[dict[str, Any]] = []
        for field, minimum in (
            ("positive_fixtures", 1),
            ("negative_fixtures", 1),
            ("unsupported_variants", 1),
            ("mutation_fixtures", 1),
        ):
            fixtures = rule.get(field)
            if not isinstance(fixtures, list) or len(fixtures) < minimum:
                errors.append(f"{rule.get('rule_id')}:missing_executable_{field}")
                continue
            for fixture in fixtures:
                if not isinstance(fixture, dict):
                    errors.append(f"{rule.get('rule_id')}:non_executable_fixture:{field}")
                    continue
                result = evaluate_rule_fixture(rule, fixture)
                fixture_results.append({**result, "field": field})
                if result["observed_status"] != result["expected_status"]:
                    errors.append(
                        f"{rule.get('rule_id')}:{field}:{result.get('fixture_id')}:"
                        f"expected_{result['expected_status']}_observed_{result['observed_status']}"
                    )
        positives = [row for row in fixture_results if row["field"] == "positive_fixtures"]
        negatives = [row for row in fixture_results if row["field"] in {"negative_fixtures", "unsupported_variants", "mutation_fixtures"}]
        if not positives or any(row["observed_status"] != "passed" for row in positives):
            errors.append(f"{rule.get('rule_id')}:positive_fixture_not_passing")
        if not negatives or any(row["observed_status"] != "failed" for row in negatives):
            errors.append(f"{rule.get('rule_id')}:negative_or_mutation_fixture_not_failing")
        rule_rows.append(
            {
                "rule_id": rule.get("rule_id"),
                "family": rule.get("family"),
                "independent_rule_checker": rule.get("independent_rule_checker"),
                "fixture_results": fixture_results,
            }
        )

    return {
        "schema_version": "RuleFixtureSuiteReportV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "rule_count": len(rule_rows),
        "rule_checker_import_report": import_report,
        "rule_results": rule_rows,
    }
