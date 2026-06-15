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

ENGINE_ROLE = "synthetic_closure"
BACKEND_IDENTITY = "geometry_full2d.synthetic_closure:local_rule_closure:v0_4_2"


@dataclass(frozen=True)
class Full2DTraceStep:
    step_id: str
    rule_id: str
    input_facts: tuple[str, ...]
    output_fact: str
    discharged_side_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Full2DTraceV1:
    schema_version: str
    trace_id: str
    engine_role: str
    target_fact: str
    steps: tuple[Full2DTraceStep, ...]
    used_rule_ids: tuple[str, ...]
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    target = claim_spec.get("target", {})
    target_fact = _fact_key(target)
    hypotheses = tuple(_predicate_fact_key(item) for item in claim_spec.get("hypotheses", []))
    side_conditions = tuple(
        condition
        for bucket in claim_spec.get("side_conditions", {}).values()
        if isinstance(bucket, (list, tuple))
        for condition in bucket
    )
    trace = _derive_trace(target, target_fact, hypotheses, side_conditions)
    if trace is None:
        return _measured_failure(engine_input, context, "no_synthetic_closure_found")
    trace_payload = trace.to_dict()
    trace_hash = hash_ref(canonical_json(trace_payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=trace_hash,
        normalized_output_ref=f"Full2DTraceV1:{trace_hash}",
        checker_or_compiler_ref=f"RuleRegistryFull2D:{build_rule_registry_full2d().registry_hash()}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
    )


def _derive_trace(
    target: dict[str, Any],
    target_fact: str,
    hypotheses: tuple[str, ...],
    side_conditions: tuple[str, ...],
) -> Full2DTraceV1 | None:
    if target_fact in hypotheses:
        steps = tuple(
            Full2DTraceStep(
                step_id=f"synthetic_closure:known_fact:{index}",
                rule_id=rule,
                input_facts=(target_fact,),
                output_fact=target_fact,
                discharged_side_conditions=side_conditions,
            )
            for index, rule in enumerate(("full2d_rule:incidence_collinearity:01", "full2d_rule:incidence_collinearity:03"), start=1)
        )
        return _trace(target_fact, steps)
    if _is_collinear_reflexive_target(target):
        steps = tuple(
            Full2DTraceStep(
                step_id=f"synthetic_closure:collinear_reflexive:{index}",
                rule_id=rule,
                input_facts=(),
                output_fact=target_fact,
                discharged_side_conditions=side_conditions,
            )
            for index, rule in enumerate(
                (
                    "full2d_rule:incidence_collinearity:01",
                    "full2d_rule:incidence_collinearity:02",
                    "full2d_rule:incidence_collinearity:03",
                ),
                start=1,
            )
        )
        return _trace(target_fact, steps)
    return None


def _trace(target_fact: str, steps: tuple[Full2DTraceStep, ...]) -> Full2DTraceV1:
    used = tuple(step.rule_id for step in steps)
    trace_id = f"full2d_trace:{hash_ref(canonical_json([step.to_dict() for step in steps]))[7:23]}"
    return Full2DTraceV1(
        schema_version="1.0.0",
        trace_id=trace_id,
        engine_role=ENGINE_ROLE,
        target_fact=target_fact,
        steps=steps,
        used_rule_ids=used,
    )


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


def _is_collinear_reflexive_target(target: dict[str, Any]) -> bool:
    family = str(target.get("family", ""))
    args = list(target.get("args", []))
    return family in {"incidence", "collinear"} and len(args) == 3 and (args[0] == args[1] or args[1] == args[2])


def _predicate_fact_key(predicate: dict[str, Any]) -> str:
    return f"{predicate.get('family')}:{','.join(map(str, predicate.get('args', [])))}:{predicate.get('polarity', 'positive')}"


def _fact_key(target: dict[str, Any]) -> str:
    return f"{target.get('family')}:{','.join(map(str, target.get('args', [])))}:positive"
