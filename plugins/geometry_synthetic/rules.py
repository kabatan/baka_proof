from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class GeoTraceStep:
    step_id: str
    rule_id: str
    premises: tuple[str, ...]
    conclusion: str
    side_condition_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeoTraceV1:
    schema_version: str
    trace_id: str
    claim_spec_ref: str
    steps: tuple[GeoTraceStep, ...]
    rule_refs: tuple[str, ...]
    side_condition_refs: tuple[str, ...]
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload


@dataclass(frozen=True)
class GeometryRuleContract:
    schema_version: str
    rule_id: str
    rule_family: str
    lean_lemma_or_template: str
    premise_pattern: tuple[str, ...]
    conclusion_pattern: str
    required_side_conditions: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    unsupported_variants: tuple[str, ...]
    fixtures: dict[str, tuple[str, ...]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuleRegistryV1:
    schema_version: str
    registry_id: str
    target_library: str
    rules: tuple[GeometryRuleContract, ...]
    supported_rule_families: tuple[str, ...]
    release_blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["rules"] = [rule.to_dict() for rule in self.rules]
        return payload


@dataclass(frozen=True)
class SideConditionReport:
    schema_version: str
    report_id: str
    condition_id: str
    status: str
    generated_obligation_ids: tuple[str, ...]
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_rule_registry() -> RuleRegistryV1:
    rules = (
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:collinearity_identity:v1",
            rule_family="collinearity_propagation",
            lean_lemma_or_template="LeanGeo.Abbre.Coll",
            premise_pattern=("Coll A B C",),
            conclusion_pattern="Coll A B C",
            required_side_conditions=("points_declared:A:B:C",),
            generated_obligations=(),
            unsupported_variants=("set_collinearity", "coordinate_collinearity"),
            fixtures={
                "positive": ("Coll A B C -> Coll A B C",),
                "negative": ("arbitrary_mathlib_expression",),
                "ambiguous": ("Collinear? A B C",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:midpoint_collinearity_basic:v1",
            rule_family="midpoint_basic_consequences",
            lean_lemma_or_template="LeanGeo.Abbre.MidPoint",
            premise_pattern=("MidPoint A P B",),
            conclusion_pattern="Coll A P B",
            required_side_conditions=("points_declared:A:P:B", "endpoints_distinct:A:B"),
            generated_obligations=("endpoints_distinct:A:B",),
            unsupported_variants=("segment_object_midpoint",),
            fixtures={
                "positive": ("MidPoint A P B -> Coll A P B",),
                "negative": ("MidPoint segment_object",),
                "ambiguous": ("midpoint without endpoint distinctness",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:parallel_transfer_basic:v1",
            rule_family="parallel_perpendicular_transfer",
            lean_lemma_or_template="LeanGeo.Abbre.parallel_transfer_fixture",
            premise_pattern=("parallel L M", "perpendicular L N"),
            conclusion_pattern="perpendicular M N",
            required_side_conditions=("lines_declared:L:M:N", "nondegenerate_lines:L:M:N"),
            generated_obligations=("nondegenerate_lines:L:M:N",),
            unsupported_variants=("directed_parallel_orientation",),
            fixtures={
                "positive": ("parallel L M and perpendicular L N -> perpendicular M N",),
                "negative": ("directed parallel orientation",),
                "ambiguous": ("parallel transfer without line declarations",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:concyclic_equal_angle_basic:v1",
            rule_family="concyclicity_basic_consequences",
            lean_lemma_or_template="LeanGeo.Abbre.Cyclic",
            premise_pattern=("Cyclic A B C D",),
            conclusion_pattern="equal_angle_supported_pattern",
            required_side_conditions=("points_declared:A:B:C:D",),
            generated_obligations=(),
            unsupported_variants=("oriented_arc_angle",),
            fixtures={
                "positive": ("Cyclic A B C D -> registered equal angle",),
                "negative": ("oriented arc angle",),
                "ambiguous": ("cyclic without declared points",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:midpoint_equal_length_basic:v1",
            rule_family="equal_length_transfer",
            lean_lemma_or_template="LeanGeo.Abbre.MidPoint",
            premise_pattern=("MidPoint A P B",),
            conclusion_pattern="equal_length",
            required_side_conditions=("points_declared:A:P:B", "endpoints_distinct:A:B"),
            generated_obligations=("endpoints_distinct:A:B",),
            unsupported_variants=("norm_expression",),
            fixtures={
                "positive": ("MidPoint A P B -> |A-P| = |P-B|",),
                "negative": ("arbitrary norm expression",),
                "ambiguous": ("equal length without midpoint orientation",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:parallel_angle_transfer_basic:v1",
            rule_family="angle_transfer",
            lean_lemma_or_template="LeanGeo.Abbre.angle_transfer_fixture",
            premise_pattern=("parallel L M", "registered_angle_pattern"),
            conclusion_pattern="equal_angle_supported_pattern",
            required_side_conditions=("registered_angle_pattern", "lines_declared:L:M"),
            generated_obligations=("registered_angle_pattern",),
            unsupported_variants=("arbitrary_oriented_angle",),
            fixtures={
                "positive": ("parallel L M with registered pattern -> equal angle",),
                "negative": ("arbitrary oriented angle",),
                "ambiguous": ("angle transfer without registered pattern",),
            },
        ),
        GeometryRuleContract(
            schema_version="1.0.0",
            rule_id="rule:line_construction_introduction:v1",
            rule_family="construction_introduction",
            lean_lemma_or_template="LeanGeo.Abbre.line_from_points",
            premise_pattern=("line_through_two_distinct_points",),
            conclusion_pattern="Line",
            required_side_conditions=("points_declared:A:B", "points_distinct:A:B"),
            generated_obligations=("points_distinct:A:B",),
            unsupported_variants=("arbitrary_free_point",),
            fixtures={
                "positive": ("distinct A B -> line_from_points A B",),
                "negative": ("arbitrary free point",),
                "ambiguous": ("line construction without distinct points",),
            },
        ),
    )
    return RuleRegistryV1(
        schema_version="1.0.0",
        registry_id="RuleRegistryV1:LeanGeoSubsetV1:1.0.0",
        target_library="LeanGeoSubsetV1:1.0.0",
        rules=rules,
        supported_rule_families=tuple(rule.rule_family for rule in rules),
        release_blockers=(),
    )


def validate_rule_registry(registry: RuleRegistryV1) -> list[str]:
    errors: list[str] = []
    if registry.target_library != "LeanGeoSubsetV1:1.0.0":
        errors.append("target_library_not_LeanGeoSubsetV1")
    seen: set[str] = set()
    for rule in registry.rules:
        if rule.rule_id in seen:
            errors.append(f"duplicate_rule_id:{rule.rule_id}")
        seen.add(rule.rule_id)
        if not rule.required_side_conditions:
            errors.append(f"missing_side_conditions:{rule.rule_id}")
        for fixture_kind in ("positive", "negative", "ambiguous"):
            if not rule.fixtures.get(fixture_kind):
                errors.append(f"missing_{fixture_kind}_fixtures:{rule.rule_id}")
        if not rule.lean_lemma_or_template:
            errors.append(f"missing_lean_template:{rule.rule_id}")
    return errors


def evaluate_side_conditions(rule: GeometryRuleContract, available: set[str]) -> tuple[SideConditionReport, ...]:
    reports: list[SideConditionReport] = []
    for condition in rule.required_side_conditions:
        if condition in available:
            reports.append(
                SideConditionReport("1.0.0", f"side_condition:{condition}", condition, "discharged", (), ())
            )
        else:
            reports.append(
                SideConditionReport(
                    "1.0.0",
                    f"side_condition:{condition}",
                    condition,
                    "generated_obligation",
                    (f"obligation:{condition}",),
                    (),
                )
            )
    return tuple(reports)
