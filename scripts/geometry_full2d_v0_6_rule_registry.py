from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_6_rule_checkers import build_rule_fixtures_for_contract, run_rule_fixture_suite


ROOT = Path(__file__).resolve().parents[1]
RULE_LEMMA_FILE = ROOT / "lean" / "MathAutoResearch" / "GeometryFull2D" / "RuleLemmas.lean"
RULE_LEMMA_IMPORT = "MathAutoResearch.GeometryFull2D.RuleLemmas"


COUNTED_RULE_SPECS: tuple[tuple[str, str, str, tuple[str, ...], str], ...] = (
    ("construction_circle", "circle_center_witness_center", "circle_center_witness", ("circle_center_exists",), "center_on_constructed_circle"),
    ("construction_circle", "circle_center_witness_point_on_circle", "circle_center_witness", ("circle_center_exists",), "constructed_point_on_circle"),
    ("construction_circle", "circle_three_points_first_on_circle", "circle_three_noncollinear", ("three_point_circle_exists",), "first_point_on_circle"),
    ("construction_circle", "circle_three_points_second_on_circle", "circle_three_noncollinear", ("three_point_circle_exists",), "second_point_on_circle"),
    ("construction_circle", "circle_three_points_third_on_circle", "circle_three_noncollinear", ("three_point_circle_exists",), "third_point_on_circle"),
    ("triangle_structure", "circle_three_points_triangle", "circle_three_noncollinear", ("three_point_circle_exists",), "triangle_predicate"),
    ("construction_intersection", "line_circle_meet_on_line", "line_circle_intersection", ("intersection_exists",), "intersection_point_on_line"),
    ("construction_intersection", "line_circle_meet_on_circle", "line_circle_intersection", ("intersection_exists",), "intersection_point_on_circle"),
    ("construction_intersection", "circle_circle_meet_on_first", "circle_circle_intersection", ("intersection_exists",), "intersection_point_on_first_circle"),
    ("construction_intersection", "circle_circle_meet_on_second", "circle_circle_intersection", ("intersection_exists",), "intersection_point_on_second_circle"),
    ("circle_cyclicity", "chord_first_on_circle", "chord", ("chord_witness",), "chord_first_endpoint_on_circle"),
    ("circle_cyclicity", "chord_second_on_circle", "chord", ("chord_witness",), "chord_second_endpoint_on_circle"),
    ("circle_cyclicity", "chord_endpoints_distinct", "chord", ("chord_witness",), "chord_distinct_endpoints"),
    ("circle_tangent", "tangent_chord_tangent_part", "tangent_chord_angle", ("tangent_chord_witness",), "tangent_at_chord_point"),
    ("circle_tangent", "tangent_chord_circle_part", "tangent_chord_angle", ("tangent_chord_witness",), "chord_reference_point_on_circle"),
    ("triangle_metric", "equilateral_first_equal_length", "equilateral", ("triangle_non_degenerate",), "first_equal_side_pair"),
    ("triangle_metric", "equilateral_second_equal_length", "equilateral", ("triangle_non_degenerate",), "second_equal_side_pair"),
    ("triangle_structure", "equilateral_triangle_pred", "equilateral", ("triangle_non_degenerate",), "triangle_from_equilateral"),
    ("triangle_altitude", "altitude_foot_part", "altitude", ("altitude_line_witness",), "foot_of_altitude"),
    ("triangle_altitude", "altitude_first_endpoint_on_line", "altitude", ("altitude_line_witness",), "first_base_endpoint_on_line"),
    ("triangle_altitude", "altitude_second_endpoint_on_line", "altitude", ("altitude_line_witness",), "second_base_endpoint_on_line"),
    ("angle_bisector", "angle_bisector_line_on_line", "angle_bisector_line", ("angle_bisector_line_witness",), "bisector_point_on_line"),
    ("angle_bisector", "angle_bisector_line_angle_part", "angle_bisector_line", ("angle_bisector_line_witness",), "angle_bisector_predicate"),
    ("metric_length_sum", "length_sum_comm_inputs", "length_sum", ("length_sum_certificate",), "commuted_length_sum"),
    ("ratio_algebra", "ratio_product_comm_inputs", "ratio_product", ("ratio_product_certificate",), "commuted_ratio_product"),
    ("directed_angle_mod_pi", "directed_angle_mod_pi_chain", "directed_angle_eq_mod_pi_pair", ("directed_angle_chain_certificate",), "directed_angle_mod_pi_transitive"),
    ("directed_angle_mod_2pi", "directed_angle_mod_2pi_chain", "directed_angle_eq_mod_2pi_pair", ("directed_angle_chain_certificate",), "directed_angle_mod_2pi_transitive"),
    ("metric_equal_length", "equal_length_chain_rule", "equal_length_pair", ("metric_chain_certificate",), "equal_length_transitive"),
    ("area_relation", "area_eq_chain_rule", "area_eq_pair", ("area_chain_certificate",), "area_eq_transitive"),
    ("midpoint_segment", "midpoint_collinear_rule", "midpoint", ("midpoint_construction_checked",), "midpoint_implies_collinear"),
    ("order_between", "between_collinear_rule", "between", ("between_order_checked",), "between_implies_collinear"),
    ("transformation_reflection", "reflection_evidence_rule", "reflection_witness", ("reflection_object_checked",), "reflection_image_evidence"),
    ("transformation_homothety", "homothety_evidence_rule", "homothety_witness", ("homothety_object_checked",), "homothety_image_evidence"),
    ("transformation_inversion", "inversion_evidence_rule", "inversion_witness", ("inversion_object_checked",), "inversion_image_evidence"),
    ("spiral_similarity", "spiral_similarity_evidence_rule", "spiral_similarity_witness", ("spiral_similarity_object_checked",), "spiral_similarity_center_evidence"),
    ("transformation_rotation", "rotation_preserves_collinear_rule", "rotation_collinearity_transport", ("rotation_point_equalities",), "rotated_collinearity"),
)

HELPER_RULE_SPECS: tuple[tuple[str, str, str], ...] = (
    ("full2d_helper:reflexive_ratio_le", "inequality_length", "ratio_le_refl_rule"),
    ("full2d_helper:area_le_refl", "area_relation", "area_le_refl_rule"),
    ("full2d_helper:angle_le_refl", "angle_bisector", "angle_le_refl_rule"),
)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def normalize_type_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def extract_theorem_type_map(source: str) -> dict[str, str]:
    pattern = re.compile(r"\btheorem\s+([A-Za-z0-9_']+)\s+(.*?):=\s+by", re.DOTALL)
    results: dict[str, str] = {}
    for match in pattern.finditer(source):
        name = match.group(1)
        signature = normalize_type_text(match.group(2))
        if ":" not in signature:
            continue
        type_text = normalize_type_text(signature[signature.find(":") + 1 :])
        results[name] = type_text
    return results


def lemma_type_hashes() -> dict[str, str]:
    source = RULE_LEMMA_FILE.read_text(encoding="utf-8")
    return {name: sha256_text(type_text) for name, type_text in extract_theorem_type_map(source).items()}


def run_lean_rule_lemma_check() -> dict[str, Any]:
    proc = subprocess.run(["lake", "env", "lean", str(RULE_LEMMA_FILE)], cwd=ROOT, text=True, capture_output=True)
    return {
        "schema_version": "RuleLemmaLeanElaborationReportV06",
        "command": ["lake", "env", "lean", str(RULE_LEMMA_FILE.relative_to(ROOT))],
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "status": "passed" if proc.returncode == 0 else "failed",
    }


def build_rule_registry_v0_6() -> dict[str, Any]:
    type_hashes = lemma_type_hashes()
    rules: list[dict[str, Any]] = []
    for index, (family, lemma, input_pattern, side_conditions, output_pattern) in enumerate(COUNTED_RULE_SPECS, start=1):
        rule_id = f"full2d_rule:{family}:{index:02d}"
        checker_name = f"{family}_rule_checker_v0_6"
        fixtures = build_rule_fixtures_for_contract(
            rule_id=rule_id,
            checker_name=checker_name,
            input_pattern=input_pattern,
            side_conditions=side_conditions,
            output_pattern=output_pattern,
        )
        rule = {
            "schema_version": "RuleContractV2",
            "rule_id": rule_id,
            "family": family,
            "input_patterns": [input_pattern],
            "output_pattern": output_pattern,
            "side_conditions": list(side_conditions),
            "lean_lemma": f"MathAutoResearch.GeometryFull2D.{lemma}",
            "lean_lemma_type_hash": type_hashes.get(lemma, ""),
            "independent_rule_checker": checker_name,
            "positive_fixtures": fixtures["positive_fixtures"],
            "negative_fixtures": fixtures["negative_fixtures"],
            "unsupported_variants": fixtures["unsupported_variants"],
            "counted_release_rule": True,
            "direct_identity_rule": False,
            "direct_facade_rule": False,
            "alias_of": None,
            "mutation_sensitive": True,
            "mutation_fixtures": fixtures["mutation_fixtures"],
            "release_usage_requirement": {
                "used_in_b2_final_theorem": "required_by_wp13_wp14_actual_records",
                "consumed_by_compiler": "required_by_wp09_wp13_actual_records",
                "present_in_certificate": "required_by_wp10_wp13_actual_records",
            },
        }
        rules.append(rule)
    for helper_id, family, lemma in HELPER_RULE_SPECS:
        rules.append(
            {
                "schema_version": "RuleContractV2",
                "rule_id": helper_id,
                "family": family,
                "input_patterns": ["helper_input"],
                "output_pattern": "helper_output",
                "side_conditions": [],
                "lean_lemma": f"MathAutoResearch.GeometryFull2D.{lemma}",
                "lean_lemma_type_hash": type_hashes.get(lemma, ""),
                "independent_rule_checker": "helper_rule_checker_v0_6",
                "positive_fixtures": ["positive:helper"],
                "negative_fixtures": ["negative:helper"],
                "unsupported_variants": ["unsupported:helper_counted"],
                "counted_release_rule": False,
                "direct_identity_rule": True,
                "direct_facade_rule": False,
                "alias_of": None,
                "mutation_sensitive": False,
                "mutation_fixtures": [],
                "release_usage_requirement": {},
            }
        )
    unsigned = {
        "schema_version": "RuleRegistryFull2DV06",
        "registry_id": "RuleRegistryFull2D:v0_6:semantic_contracts",
        "lean_module": RULE_LEMMA_IMPORT,
        "lean_file": RULE_LEMMA_FILE.relative_to(ROOT).as_posix(),
        "rules": rules,
        "git_head": current_git_head(),
    }
    return {"registry_hash": sha256_text(canonical_json(unsigned)), **unsigned}


def counted_rules(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [rule for rule in registry.get("rules", []) if isinstance(rule, dict) and rule.get("counted_release_rule") is True]


def validate_rule_registry_v0_6(registry: dict[str, Any], *, release: bool = False) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != "RuleRegistryFull2DV06":
        errors.append("bad_registry_schema")
    rules = registry.get("rules")
    if not isinstance(rules, list):
        return ["rules_not_list"]
    ids = [str(rule.get("rule_id")) for rule in rules if isinstance(rule, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_rule_ids")
    counted = counted_rules(registry)
    if release and len(counted) < 35:
        errors.append(f"counted_rule_count_below_35:{len(counted)}")
    families = {str(rule.get("family")) for rule in counted}
    if release and len(families) < 15:
        errors.append(f"counted_rule_family_count_below_15:{len(families)}")
    type_hashes = lemma_type_hashes()
    lemma_names = set(type_hashes)
    semantic_keys: set[tuple[str, str, tuple[str, ...]]] = set()
    required = {
        "rule_id",
        "family",
        "input_patterns",
        "output_pattern",
        "side_conditions",
        "lean_lemma",
        "lean_lemma_type_hash",
        "independent_rule_checker",
        "positive_fixtures",
        "negative_fixtures",
        "unsupported_variants",
        "counted_release_rule",
    }
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"bad_rule:{index}")
            continue
        missing = sorted(required - set(rule))
        errors.extend(f"missing_rule_field:{rule.get('rule_id', index)}:{field}" for field in missing)
        lemma_full = str(rule.get("lean_lemma", ""))
        lemma = lemma_full.rsplit(".", 1)[-1]
        if lemma not in lemma_names:
            errors.append(f"lean_lemma_missing:{rule.get('rule_id')}:{lemma_full}")
        elif rule.get("lean_lemma_type_hash") != type_hashes[lemma]:
            errors.append(f"lean_lemma_type_hash_mismatch:{rule.get('rule_id')}")
        for key in ["input_patterns", "positive_fixtures", "negative_fixtures", "unsupported_variants"]:
            value = rule.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"empty_rule_list_field:{rule.get('rule_id')}:{key}")
            elif rule.get("counted_release_rule") is True and key in {"positive_fixtures", "negative_fixtures", "unsupported_variants"}:
                if not all(isinstance(item, dict) for item in value):
                    errors.append(f"non_executable_rule_fixture:{rule.get('rule_id')}:{key}")
        if rule.get("counted_release_rule") is not True:
            continue
        inputs = rule.get("input_patterns", [])
        output = str(rule.get("output_pattern", ""))
        semantic_key = (str(rule.get("family")), output, tuple(str(item) for item in inputs))
        if semantic_key in semantic_keys:
            errors.append(f"alias_inflation_duplicate_semantics:{rule.get('rule_id')}")
        semantic_keys.add(semantic_key)
        if rule.get("alias_of"):
            errors.append(f"counted_alias_rule:{rule.get('rule_id')}")
        if rule.get("direct_identity_rule") is True or rule.get("direct_facade_rule") is True:
            errors.append(f"counted_identity_or_facade_rule:{rule.get('rule_id')}")
        if output in {str(item) for item in inputs}:
            errors.append(f"counted_identity_rule:{rule.get('rule_id')}")
        if output.lower() in {"target", "target_goal", "final_target", "goal"}:
            errors.append(f"counted_naked_target_rule:{rule.get('rule_id')}")
        if rule.get("mutation_sensitive") is not True:
            errors.append(f"counted_rule_not_mutation_sensitive:{rule.get('rule_id')}")
        mutation = rule.get("mutation_fixtures")
        if not isinstance(mutation, list) or not mutation:
            errors.append(f"counted_rule_missing_mutation_fixtures:{rule.get('rule_id')}")
        elif not all(isinstance(item, dict) for item in mutation):
            errors.append(f"non_executable_rule_fixture:{rule.get('rule_id')}:mutation_fixtures")
        usage = rule.get("release_usage_requirement")
        if not isinstance(usage, dict) or set(usage) != {"used_in_b2_final_theorem", "consumed_by_compiler", "present_in_certificate"}:
            errors.append(f"counted_rule_missing_release_usage_requirements:{rule.get('rule_id')}")
    fixture_report = run_rule_fixture_suite(registry)
    errors.extend(f"rule_fixture_suite:{error}" for error in fixture_report.get("errors", []))
    return sorted(set(errors))
