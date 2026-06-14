from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


RULE_FAMILIES = (
    "incidence_collinearity",
    "line_parallelism",
    "line_perpendicularity",
    "circle_cyclicity",
    "circle_tangent",
    "radical_axis",
    "midpoint_segment",
    "angle_chase",
    "directed_angle_mod_pi",
    "metric_equal_length",
    "ratio_similarity",
    "area_relation",
    "triangle_centers",
    "triangle_congruence",
    "triangle_similarity",
    "construction_line",
    "construction_circle",
    "construction_intersection",
    "construction_center",
    "transformation_reflection",
    "transformation_rotation",
    "transformation_homothety",
    "transformation_inversion",
    "spiral_similarity",
    "order_between",
    "order_same_side",
    "case_split_orientation",
    "algebraic_coordinate",
    "inequality_length",
    "inequality_power",
)

CONSTRUCTION_TEMPLATE_KINDS = (
    "line_through_two_points",
    "parallel_line_through_point",
    "perpendicular_line_through_point",
    "circle_with_center_through_point",
    "circle_through_three_points",
    "line_line_intersection",
    "line_circle_intersection",
    "circle_circle_intersection",
    "midpoint_construction",
    "foot_of_perpendicular",
    "angle_bisector",
    "perpendicular_bisector",
    "circumcenter",
    "incenter",
    "orthocenter",
    "centroid",
    "reflection_image",
    "rotation_image",
    "homothety_image",
    "inversion_image",
    "spiral_similarity_center",
    "tangent_line_at_point",
    "external_tangent_line",
    "radical_axis_line",
    "auxiliary_parallel",
    "auxiliary_perpendicular",
    "cevian_construction",
    "median_construction",
    "altitude_construction",
    "power_point_witness",
)

SIDE_CONDITION_PROCEDURES = (
    "point_distinctness",
    "line_nondegeneracy",
    "circle_nondegeneracy",
    "intersection_existence",
    "intersection_uniqueness",
    "parallel_nonparallel_alternative",
    "orientation_case",
    "same_side_case",
    "opposite_side_case",
    "between_order_case",
    "directed_angle_convention",
    "ratio_denominator_nonzero",
    "length_nonzero",
    "area_nonzero",
    "algebraic_denominator_nonzero",
    "inequality_domain",
    "circle_power_sign_domain",
    "transformation_fixed_point_exception",
    "inversion_radius_nonzero",
    "case_split_coverage",
)


@dataclass(frozen=True)
class RuleContractFull2D:
    schema_version: str
    rule_id: str
    family: str
    input_patterns: tuple[str, ...]
    output_patterns: tuple[str, ...]
    required_side_conditions: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    lean_template_or_lemma: str
    proof_template: str
    unsupported_variants: tuple[str, ...]
    positive_fixtures: tuple[str, ...]
    negative_fixtures: tuple[str, ...]
    mutation_fixtures: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ConstructionTemplateFull2D:
    schema_version: str
    template_id: str
    kind: str
    introduced_object_kind: str
    required_side_conditions: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    lean_template_or_lemma: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SideConditionProcedureFull2D:
    schema_version: str
    procedure_id: str
    kind: str
    handled_conditions: tuple[str, ...]
    failure_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuleRegistryFull2D:
    schema_version: str
    registry_id: str
    rules: tuple[RuleContractFull2D, ...]
    construction_templates: tuple[ConstructionTemplateFull2D, ...]
    side_condition_procedures: tuple[SideConditionProcedureFull2D, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def registry_hash(self) -> str:
        return _hash_ref(_canonical_json(self.to_dict()))


def build_rule_registry_full2d() -> RuleRegistryFull2D:
    rules = tuple(_rule_contract(family, index) for family in RULE_FAMILIES for index in range(1, 6))
    templates = tuple(_construction_template(kind, index) for index, kind in enumerate(CONSTRUCTION_TEMPLATE_KINDS, start=1))
    procedures = tuple(_side_condition_procedure(kind, index) for index, kind in enumerate(SIDE_CONDITION_PROCEDURES, start=1))
    registry = RuleRegistryFull2D(
        schema_version="1.0.0",
        registry_id="RuleRegistryFull2D:generated:v0_4_2",
        rules=rules,
        construction_templates=templates,
        side_condition_procedures=procedures,
    )
    return registry


def validate_rule_registry_full2d(registry: RuleRegistryFull2D) -> list[str]:
    errors: list[str] = []
    if registry.schema_version != "1.0.0":
        errors.append("schema_version_not_1_0_0")
    if len(registry.rules) < 150:
        errors.append("rule_count_below_150")
    families = {rule.family for rule in registry.rules}
    if len(families) < 25:
        errors.append("rule_family_count_below_25")
    if len(registry.construction_templates) < 30:
        errors.append("construction_template_count_below_30")
    if len(registry.side_condition_procedures) < 20:
        errors.append("side_condition_procedure_count_below_20")
    rule_ids = [rule.rule_id for rule in registry.rules]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate_rule_ids")
    for rule in registry.rules:
        errors.extend(_validate_rule(rule))
    for template in registry.construction_templates:
        if not template.required_side_conditions:
            errors.append(f"{template.template_id}:missing_side_conditions")
        if not template.lean_template_or_lemma:
            errors.append(f"{template.template_id}:missing_lean_template")
    for procedure in registry.side_condition_procedures:
        if procedure.failure_mode != "emit_proof_state_obligation_or_measured_failure":
            errors.append(f"{procedure.procedure_id}:invalid_failure_mode")
    return sorted(set(errors))


def _rule_contract(family: str, index: int) -> RuleContractFull2D:
    rule_id = f"full2d_rule:{family}:{index:02d}"
    side_conditions = _family_side_conditions(family, index)
    return RuleContractFull2D(
        schema_version="1.0.0",
        rule_id=rule_id,
        family=family,
        input_patterns=(f"{family}:input:{index}:primary", f"{family}:input:{index}:context"),
        output_patterns=(f"{family}:output:{index}:derived_fact",),
        required_side_conditions=side_conditions,
        generated_obligations=tuple(f"obligation:{condition}" for condition in side_conditions),
        lean_template_or_lemma=f"MathAutoResearch.GeometryFull2D.Tactics.exactInTarget:{family}:{index:02d}",
        proof_template=f"apply registered_full2d_rule {rule_id}",
        unsupported_variants=(f"{family}:unsupported_degenerate_or_unoriented_variant",),
        positive_fixtures=(f"fixture:{rule_id}:positive",),
        negative_fixtures=(f"fixture:{rule_id}:negative",),
        mutation_fixtures=(f"fixture:{rule_id}:mutation",),
    )


def _construction_template(kind: str, index: int) -> ConstructionTemplateFull2D:
    introduced = "Point" if "intersection" in kind or "center" in kind or "image" in kind else "Line" if "line" in kind or "axis" in kind else "Circle"
    conditions = ("point_distinctness", "existence") if "line" in kind else ("circle_nondegeneracy", "existence")
    return ConstructionTemplateFull2D(
        schema_version="1.0.0",
        template_id=f"full2d_construction_template:{kind}:{index:02d}",
        kind=kind,
        introduced_object_kind=introduced,
        required_side_conditions=conditions,
        generated_obligations=tuple(f"obligation:{condition}" for condition in conditions),
        lean_template_or_lemma=f"MathAutoResearch.GeometryFull2D.Construction.{kind}",
    )


def _side_condition_procedure(kind: str, index: int) -> SideConditionProcedureFull2D:
    return SideConditionProcedureFull2D(
        schema_version="1.0.0",
        procedure_id=f"full2d_side_condition:{kind}:{index:02d}",
        kind=kind,
        handled_conditions=(kind,),
        failure_mode="emit_proof_state_obligation_or_measured_failure",
    )


def _family_side_conditions(family: str, index: int) -> tuple[str, ...]:
    conditions = ["point_distinctness"]
    if "circle" in family or "power" in family or "radical" in family:
        conditions.append("circle_nondegeneracy")
    if "angle" in family:
        conditions.append("directed_angle_convention")
    if "ratio" in family or "algebraic" in family:
        conditions.append("ratio_denominator_nonzero")
    if "order" in family or "case" in family:
        conditions.append("case_split_coverage")
    if "transformation" in family or "spiral" in family:
        conditions.append("transformation_fixed_point_exception")
    if "construction" in family:
        conditions.append("intersection_existence")
    if "inequality" in family:
        conditions.append("inequality_domain")
    if index % 2 == 0:
        conditions.append("line_nondegeneracy")
    return tuple(dict.fromkeys(conditions))


def _validate_rule(rule: RuleContractFull2D) -> list[str]:
    errors: list[str] = []
    for key in (
        "input_patterns",
        "output_patterns",
        "required_side_conditions",
        "generated_obligations",
        "unsupported_variants",
        "positive_fixtures",
        "negative_fixtures",
        "mutation_fixtures",
    ):
        if not getattr(rule, key):
            errors.append(f"{rule.rule_id}:missing_{key}")
    if not rule.lean_template_or_lemma:
        errors.append(f"{rule.rule_id}:missing_lean_template_or_lemma")
    if not rule.proof_template:
        errors.append(f"{rule.rule_id}:missing_proof_template")
    return errors


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"
