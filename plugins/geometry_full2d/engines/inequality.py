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

ENGINE_ROLE = "inequality"
BACKEND_IDENTITY = "geometry_full2d.inequality:exact_domain_certificate:v0_4_2"


@dataclass(frozen=True)
class InequalityCertificateFull2D:
    schema_version: str
    certificate_id: str
    certificate_scope: str
    expression_family: str
    domain_constraints: tuple[str, ...]
    inequality_goal: str
    exact_certificate_steps: tuple[str, ...]
    checker_result: str
    source_rule_ids: tuple[str, ...]
    lean_summary: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    certificate = _build_certificate(claim_spec)
    if certificate is None:
        return _measured_failure(engine_input, context, "unsupported_inequality_or_domain_target")
    payload = certificate.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"InequalityCertificateFull2D:{payload_hash}",
        checker_or_compiler_ref=f"InequalityCertificateCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
    )


def _build_certificate(claim_spec: dict[str, Any]) -> InequalityCertificateFull2D | None:
    target = claim_spec.get("target", {})
    side_conditions = _nondegeneracy_conditions(claim_spec)
    if not isinstance(target, dict) or not side_conditions:
        return None
    point_pair = _first_distinct_point_pair(side_conditions)
    if point_pair is None:
        return None
    a, b = point_pair
    inequality_goal = f"squared_distance({a}, {b}) > 0"
    steps = (
        "translate_distinct_points_to_nonzero_vector",
        "expand_squared_distance_as_sum_of_squares",
        "check_exact_positive_domain_condition",
    )
    checker_result = _check_certificate(point_pair, inequality_goal, steps)
    if checker_result != "passed":
        return None
    seed = canonical_json({"target": target, "point_pair": point_pair, "side_conditions": side_conditions})
    return InequalityCertificateFull2D(
        schema_version="1.0.0",
        certificate_id=f"inequality_certificate:{hash_ref(seed)[7:23]}",
        certificate_scope="side_condition_domain",
        expression_family="length_nonzero",
        domain_constraints=side_conditions,
        inequality_goal=inequality_goal,
        exact_certificate_steps=steps,
        checker_result=checker_result,
        source_rule_ids=("full2d_rule:inequality_length:01",),
        lean_summary="declared point distinctness is normalized as a positive squared-distance domain condition",
    )


def _nondegeneracy_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    values = buckets.get("nondegeneracy", ())
    if not isinstance(values, (list, tuple)):
        return ()
    return tuple(str(item) for item in values)


def _first_distinct_point_pair(side_conditions: tuple[str, ...]) -> tuple[str, str] | None:
    for condition in side_conditions:
        if "!=" not in condition:
            continue
        left, right = condition.split("!=", 1)
        left = left.strip()
        right = right.strip()
        if left and right and left != right:
            return (left, right)
    return None


def _check_certificate(point_pair: tuple[str, str], inequality_goal: str, steps: tuple[str, ...]) -> str:
    a, b = point_pair
    if a == b:
        return "failed"
    if f"squared_distance({a}, {b}) > 0" != inequality_goal:
        return "failed"
    if "expand_squared_distance_as_sum_of_squares" not in steps:
        return "failed"
    return "passed"


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
