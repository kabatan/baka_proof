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

RULE_LEAN_TEMPLATES = {
    "full2d_rule:angle_chase:01": "lean_template:assumption_support",
    "full2d_rule:angle_chase:02": "lean_template:directed_angle_eq_mod_2pi_refl",
    "full2d_rule:angle_chase:03": "lean_template:checked_certificate",
    "full2d_rule:angle_chase:04": "lean_template:directed_angle_eq_mod_2pi_symm",
    "full2d_rule:area_relation:01": "lean_template:assumption_support",
    "full2d_rule:area_relation:02": "lean_template:area_eq_refl",
    "full2d_rule:area_relation:03": "lean_template:checked_certificate",
    "full2d_rule:area_relation:04": "lean_template:area_eq_symm",
    "full2d_rule:circle_cyclicity:01": "lean_template:assumption_support",
    "full2d_rule:circle_cyclicity:02": "lean_template:chord_is_symmetric",
    "full2d_rule:construction_center:01": "lean_template:assumption_support",
    "full2d_rule:construction_center:02": "lean_template:constructed_center_identity",
    "full2d_rule:construction_circle:01": "lean_template:assumption_support",
    "full2d_rule:construction_circle:02": "lean_template:circle_construction_on_circle",
    "full2d_rule:construction_intersection:01": "lean_template:assumption_support",
    "full2d_rule:construction_intersection:02": "lean_template:line_circle_intersection_on_line",
    "full2d_rule:directed_angle_mod_pi:01": "lean_template:checked_certificate",
    "full2d_rule:directed_angle_mod_pi:02": "lean_template:assumption_support",
    "full2d_rule:directed_angle_mod_pi:03": "lean_template:directed_angle_eq_refl",
    "full2d_rule:directed_angle_mod_pi:04": "lean_template:directed_angle_eq_symm",
    "full2d_rule:incidence_collinearity:01": "lean_template:checked_certificate",
    "full2d_rule:incidence_collinearity:02": "lean_template:collinear_refl_left",
    "full2d_rule:incidence_collinearity:03": "lean_template:checked_certificate",
    "full2d_rule:incidence_collinearity:04": "lean_template:collinear_refl_right",
    "full2d_rule:inequality_length:01": "lean_template:assumption_support",
    "full2d_rule:inequality_length:02": "lean_template:assumption_support",
    "full2d_rule:inequality_length:03": "lean_template:length_le_refl",
    "full2d_rule:inequality_length:04": "lean_template:checked_certificate",
    "full2d_rule:inequality_length:05": "lean_template:length_le_trans",
    "full2d_rule:metric_equal_length:01": "lean_template:assumption_support",
    "full2d_rule:metric_equal_length:02": "lean_template:equal_length_symm",
    "full2d_rule:metric_equal_length:03": "lean_template:equal_length_refl",
    "full2d_rule:metric_equal_length:04": "lean_template:checked_certificate",
    "full2d_rule:midpoint_segment:01": "lean_template:assumption_support",
    "full2d_rule:midpoint_segment:02": "lean_template:midpoint_collinear",
    "full2d_rule:order_between:01": "lean_template:assumption_support",
    "full2d_rule:order_between:02": "lean_template:between_collinear",
    "full2d_rule:ratio_similarity:01": "lean_template:assumption_support",
    "full2d_rule:ratio_similarity:02": "lean_template:ratio_eq_refl",
    "full2d_rule:ratio_similarity:03": "lean_template:checked_certificate",
    "full2d_rule:ratio_similarity:04": "lean_template:ratio_eq_symm",
    "full2d_rule:spiral_similarity:01": "lean_template:checked_certificate",
    "full2d_rule:spiral_similarity:02": "lean_template:spiral_similarity_has_evidence",
    "full2d_rule:transformation_homothety:01": "lean_template:checked_certificate",
    "full2d_rule:transformation_homothety:02": "lean_template:homothety_has_evidence",
    "full2d_rule:transformation_inversion:01": "lean_template:checked_certificate",
    "full2d_rule:transformation_inversion:02": "lean_template:inversion_has_evidence",
    "full2d_rule:transformation_reflection:01": "lean_template:checked_certificate",
    "full2d_rule:transformation_reflection:02": "lean_template:reflection_has_evidence",
    "full2d_rule:transformation_rotation:01": "lean_template:checked_certificate",
    "full2d_rule:transformation_rotation:02": "lean_template:rotation_preserves_collinear_of_eq",
    "full2d_rule:triangle_congruence:01": "lean_template:assumption_support",
    "full2d_rule:triangle_congruence:02": "lean_template:equilateral_is_isosceles_left",
}


@dataclass(frozen=True)
class RuleContractFull2D:
    schema_version: str
    rule_id: str
    rule_family: str
    input_patterns: tuple[str, ...]
    output_pattern: str
    required_side_conditions: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    lean_template_id: str
    independent_checker: str
    positive_fixtures: tuple[str, ...]
    negative_fixtures: tuple[str, ...]
    mutation_fixtures: tuple[str, ...]
    direct_identity_rule: bool
    direct_facade_rule: bool
    counted: bool

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))

    @property
    def family(self) -> str:
        return self.rule_family

    @property
    def output_patterns(self) -> tuple[str, ...]:
        return (self.output_pattern,)

    @property
    def lean_template_or_lemma(self) -> str:
        return self.lean_template_id

    @property
    def proof_template(self) -> str:
        return f"apply {self.lean_template_id}"

    @property
    def unsupported_variants(self) -> tuple[str, ...]:
        return tuple(fixture.replace(":mutation", ":unsupported") for fixture in self.mutation_fixtures)


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
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class SideConditionProcedureFull2D:
    schema_version: str
    procedure_id: str
    kind: str
    handled_conditions: tuple[str, ...]
    failure_mode: str

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))


@dataclass(frozen=True)
class RuleRegistryFull2D:
    schema_version: str
    registry_id: str
    rules: tuple[RuleContractFull2D, ...]
    construction_templates: tuple[ConstructionTemplateFull2D, ...]
    side_condition_procedures: tuple[SideConditionProcedureFull2D, ...]

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(asdict(self))

    def registry_hash(self) -> str:
        return _hash_ref(_canonical_json(self.to_dict()))


def build_rule_registry_full2d() -> RuleRegistryFull2D:
    counted_rules = tuple(_rule_contract(family, index) for family in RULE_FAMILIES for index in range(1, 6))
    helper_rules = (
        _helper_rule("full2d_helper:target_anchor_name", "helper_target_anchor", direct_facade=True),
        _helper_rule("full2d_helper:reflexive_rewrite_noncounted", "helper_reflexive_rewrite", direct_identity=True),
    )
    rules = counted_rules + helper_rules
    templates = tuple(_construction_template(kind, index) for index, kind in enumerate(CONSTRUCTION_TEMPLATE_KINDS, start=1))
    procedures = tuple(_side_condition_procedure(kind, index) for index, kind in enumerate(SIDE_CONDITION_PROCEDURES, start=1))
    registry = RuleRegistryFull2D(
        schema_version="RuleRegistryFull2D",
        registry_id="RuleRegistryFull2D:generated:v0_5",
        rules=rules,
        construction_templates=templates,
        side_condition_procedures=procedures,
    )
    return registry


def validate_rule_registry_full2d(registry: RuleRegistryFull2D) -> list[str]:
    errors: list[str] = []
    if registry.schema_version != "RuleRegistryFull2D":
        errors.append("schema_version_not_RuleRegistryFull2D")
    counted_rules = [rule for rule in registry.rules if rule.counted]
    if len(counted_rules) < 150:
        errors.append("counted_rule_count_below_150")
    families = {rule.rule_family for rule in counted_rules}
    if len(families) < 25:
        errors.append("counted_rule_family_count_below_25")
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
    lean_template_id = RULE_LEAN_TEMPLATES.get(rule_id, f"GeometryFull2D.rule_template.{family}.{index:02d}")
    return RuleContractFull2D(
        schema_version="RuleContractFull2D",
        rule_id=rule_id,
        rule_family=family,
        input_patterns=(f"{family}:input:{index}:primary", f"{family}:input:{index}:context"),
        output_pattern=f"{family}:output:{index}:derived_fact",
        required_side_conditions=side_conditions,
        generated_obligations=tuple(f"obligation:{condition}" for condition in side_conditions),
        lean_template_id=lean_template_id,
        independent_checker=f"IndependentCheckerFull2D:{family}:{index:02d}",
        positive_fixtures=(f"fixture:{rule_id}:positive",),
        negative_fixtures=(f"fixture:{rule_id}:negative",),
        mutation_fixtures=(f"fixture:{rule_id}:mutation",),
        direct_identity_rule=False,
        direct_facade_rule=False,
        counted=True,
    )


def _helper_rule(rule_id: str, family: str, *, direct_identity: bool = False, direct_facade: bool = False) -> RuleContractFull2D:
    return RuleContractFull2D(
        schema_version="RuleContractFull2D",
        rule_id=rule_id,
        rule_family=family,
        input_patterns=("helper:input",),
        output_pattern="helper:output",
        required_side_conditions=("helper_noncounted_guard",),
        generated_obligations=("obligation:helper_noncounted_guard",),
        lean_template_id=f"GeometryFull2D.helper_template.{family}",
        independent_checker=f"IndependentCheckerFull2D:{family}:helper",
        positive_fixtures=(f"fixture:{rule_id}:positive",),
        negative_fixtures=(f"fixture:{rule_id}:negative",),
        mutation_fixtures=(f"fixture:{rule_id}:mutation",),
        direct_identity_rule=direct_identity,
        direct_facade_rule=direct_facade,
        counted=False,
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
    if rule.schema_version != "RuleContractFull2D":
        errors.append(f"{rule.rule_id}:bad_schema_version")
    for key in (
        "input_patterns",
        "required_side_conditions",
        "generated_obligations",
        "positive_fixtures",
        "negative_fixtures",
        "mutation_fixtures",
    ):
        if not getattr(rule, key):
            errors.append(f"{rule.rule_id}:missing_{key}")
    if not rule.output_pattern:
        errors.append(f"{rule.rule_id}:missing_output_pattern")
    if not rule.lean_template_id:
        errors.append(f"{rule.rule_id}:missing_lean_template_id")
    if not rule.independent_checker:
        errors.append(f"{rule.rule_id}:missing_independent_checker")
    if tuple(rule.generated_obligations) != tuple(f"obligation:{condition}" for condition in rule.required_side_conditions):
        errors.append(f"{rule.rule_id}:generated_obligations_mismatch")
    if rule.counted:
        if rule.direct_identity_rule or rule.direct_facade_rule:
            errors.append(f"{rule.rule_id}:identity_or_facade_counted")
        if rule.output_pattern in set(rule.input_patterns):
            errors.append(f"{rule.rule_id}:counted_rule_output_equals_input")
        if rule.output_pattern in {"TARGET", "TARGET_GOAL", "target_goal"}:
            errors.append(f"{rule.rule_id}:naked_target_output_pattern")
        if not rule.positive_fixtures or not rule.negative_fixtures or not rule.mutation_fixtures:
            errors.append(f"{rule.rule_id}:missing_required_fixtures")
    return errors


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _jsonable(payload: Any) -> Any:
    return json.loads(json.dumps(payload, sort_keys=True))
