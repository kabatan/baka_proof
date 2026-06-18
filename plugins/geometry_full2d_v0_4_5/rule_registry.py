from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleContract:
    rule_id: str
    input_fact_patterns: tuple[str, ...]
    output_fact_pattern: str
    side_conditions_required: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    lean_template_id: str
    unsupported_variants: tuple[str, ...]


RULES: dict[str, RuleContract] = {
    "full2d.collinear.identity": RuleContract(
        rule_id="full2d.collinear.identity",
        input_fact_patterns=("collinear ?a ?b ?c",),
        output_fact_pattern="collinear ?a ?b ?c",
        side_conditions_required=(),
        generated_obligations=(),
        lean_template_id="GeometryFull2D.rule_collinear_identity",
        unsupported_variants=(),
    ),
    "full2d.metric.symmetry": RuleContract(
        rule_id="full2d.metric.symmetry",
        input_fact_patterns=("equal_length ?a ?b ?c ?d",),
        output_fact_pattern="equal_length ?c ?d ?a ?b",
        side_conditions_required=(),
        generated_obligations=(),
        lean_template_id="GeometryFull2D.rule_equal_length_symm",
        unsupported_variants=(),
    ),
    "full2d.order.between_collinear": RuleContract(
        rule_id="full2d.order.between_collinear",
        input_fact_patterns=("between ?a ?b ?c",),
        output_fact_pattern="collinear ?a ?b ?c",
        side_conditions_required=(),
        generated_obligations=(),
        lean_template_id="GeometryFull2D.rule_between_collinear",
        unsupported_variants=(),
    ),
}


def lookup(rule_id: str) -> RuleContract:
    return RULES[rule_id]
