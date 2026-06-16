from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_full2d.engine_contracts import (
    EngineInputFull2D,
    EngineOutputFull2D,
    ResourceBudget,
    RunContext,
    canonical_json,
    hash_ref,
)
from plugins.geometry_full2d.rule_registry import build_rule_registry_full2d

ENGINE_ROLE = "construction_search"
BACKEND_IDENTITY = "geometry_full2d.construction_search:deterministic_auxiliary_search:v0_4_2"


@dataclass(frozen=True)
class AuxiliaryConstructionFull2D:
    schema_version: str
    construction_id: str
    construction_kind: str
    introduced_objects: tuple[str, ...]
    dependencies: tuple[str, ...]
    required_side_conditions: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    source_rule_id: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    construction = _construct_auxiliary_line(claim_spec)
    if construction is None:
        return _measured_failure(engine_input, context, "no_applicable_construction")
    payload = construction.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"AuxiliaryConstructionFull2D:{payload_hash}",
        checker_or_compiler_ref=f"RuleRegistryFull2D:{build_rule_registry_full2d().registry_hash()}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
        normalized_output_payload=payload,
    )


def _construct_auxiliary_line(claim_spec: dict[str, Any]) -> AuxiliaryConstructionFull2D | None:
    projected = _projection_target_hypothesis(claim_spec)
    if projected is not None:
        args, side_conditions, construction_kind, source_rule_id = projected
        construction_id = f"aux_construction:{hash_ref(':'.join((construction_kind, *args)))[7:23]}"
        return AuxiliaryConstructionFull2D(
            schema_version="1.0.0",
            construction_id=construction_id,
            construction_kind=construction_kind,
            introduced_objects=(),
            dependencies=args,
            required_side_conditions=side_conditions,
            generated_obligations=tuple(f"obligation:{condition}" for condition in side_conditions),
            source_rule_id=source_rule_id,
        )
    midpoint = _midpoint_target_hypothesis(claim_spec)
    if midpoint is not None:
        args, side_conditions = midpoint
        construction_id = f"aux_construction:{hash_ref(':'.join(args))[7:23]}"
        return AuxiliaryConstructionFull2D(
            schema_version="1.0.0",
            construction_id=construction_id,
            construction_kind="midpoint_collinearity_witness",
            introduced_objects=(),
            dependencies=args,
            required_side_conditions=side_conditions,
            generated_obligations=tuple(f"obligation:{condition}" for condition in side_conditions),
            source_rule_id="full2d_rule:midpoint_segment:01",
        )
    points = [
        str(item["object_id"])
        for item in claim_spec.get("objects", [])
        if isinstance(item, dict) and item.get("kind") == "Point" and item.get("object_id")
    ]
    if len(points) < 2:
        return None
    a, b = points[:2]
    side_conditions = _side_conditions_for_pair(claim_spec, a, b)
    if not side_conditions:
        return None
    construction_id = f"aux_construction:{hash_ref(a + ':' + b)[7:23]}"
    return AuxiliaryConstructionFull2D(
        schema_version="1.0.0",
        construction_id=construction_id,
        construction_kind="line_through_two_points",
        introduced_objects=(f"line:{a.split(':', 1)[-1]}{b.split(':', 1)[-1]}:Line",),
        dependencies=(a, b),
        required_side_conditions=side_conditions,
        generated_obligations=tuple(f"obligation:{condition}" for condition in side_conditions),
        source_rule_id="full2d_rule:construction_line:01",
    )


def _side_conditions_for_pair(claim_spec: dict[str, Any], a: str, b: str) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    declared = []
    if isinstance(buckets, dict):
        for item in buckets.get("nondegeneracy", []):
            declared.append(_compact_condition(str(item)))
    compact = _compact_condition(f"{a} != {b}")
    reversed_compact = _compact_condition(f"{b} != {a}")
    if compact in declared or reversed_compact in declared:
        return (f"{a} != {b}",)
    return ()


def _midpoint_target_hypothesis(claim_spec: dict[str, Any]) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    if str(target.get("family")) not in {"incidence", "collinear"}:
        return None
    target_args = tuple(str(arg) for arg in target.get("args", ()))
    if len(target_args) != 3:
        return None
    for hypothesis in claim_spec.get("hypotheses", ()):
        if not isinstance(hypothesis, dict):
            continue
        if "midpoint" not in str(hypothesis.get("source_expr", "")).lower():
            continue
        if tuple(str(arg) for arg in hypothesis.get("args", ())) == target_args:
            return target_args, _side_conditions(claim_spec)
    return None


def _projection_target_hypothesis(
    claim_spec: dict[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...], str, str] | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    if str(target.get("family")) != "construction":
        return None
    source_expr = str(target.get("source_expr", "")).lower()
    target_args = tuple(str(arg) for arg in target.get("args", ()))
    patterns = (
        (
            "constructed_circle_point",
            "circle_with_center_through_point",
            "circle_construction_projection",
            "full2d_rule:construction_circle:01",
        ),
        (
            "constructed_line_circle_point",
            "line_circle_intersection",
            "line_circle_intersection_projection",
            "full2d_rule:construction_intersection:01",
        ),
        (
            "constructed_center_point",
            "constructed_center_point",
            "center_construction_projection",
            "full2d_rule:construction_center:01",
        ),
    )
    for target_token, hypothesis_token, construction_kind, source_rule_id in patterns:
        if target_token not in source_expr:
            continue
        for hypothesis in claim_spec.get("hypotheses", ()):
            if not isinstance(hypothesis, dict):
                continue
            if hypothesis_token not in str(hypothesis.get("source_expr", "")).lower():
                continue
            if tuple(str(arg) for arg in hypothesis.get("args", ())) == target_args:
                return target_args, _side_conditions(claim_spec), construction_kind, source_rule_id
    return None


def _side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for values in buckets.values():
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


def _compact_condition(value: str) -> str:
    return value.replace(" ", "").replace("pt:", "")


def _measured_failure(engine_input: EngineInputFull2D, context: RunContext, reason: str) -> EngineOutputFull2D:
    payload = {
        "engine_role": ENGINE_ROLE,
        "request_id": engine_input.request_id,
        "reason": reason,
        "proof_use_status": "not_allowed",
    }
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=hash_ref(canonical_json(payload)),
        normalized_output_ref=None,
        checker_or_compiler_ref=f"RuleRegistryFull2D:{build_rule_registry_full2d().registry_hash()}",
        resource_usage_ref=context.resource_usage_ref,
        status="measured_failure",
    )
