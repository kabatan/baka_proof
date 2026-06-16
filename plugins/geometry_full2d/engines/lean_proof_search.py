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

ENGINE_ROLE = "lean_proof_search"
BACKEND_IDENTITY = "geometry_full2d.lean_proof_search:semantic_rule_trace:v0_4_3"


@dataclass(frozen=True)
class LeanProofSearchTraceFull2D:
    schema_version: str
    trace_id: str
    target_fact: str
    source_statement_hash: str
    search_strategy_id: str
    admissible_rule_refs: tuple[str, ...]
    used_rule_refs: tuple[str, ...]
    used_side_condition_refs: tuple[str, ...]
    semantic_check_status: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    del budget
    trace = _build_trace(claim_spec)
    if trace is None:
        return _measured_failure(engine_input, context, "no_semantic_rule_trace")
    payload = trace.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"LeanProofSearchTraceFull2D:{payload_hash}",
        checker_or_compiler_ref=f"RuleRegistryFull2D:{build_rule_registry_full2d().registry_hash()}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
        normalized_output_payload=payload,
    )


def _build_trace(claim_spec: dict[str, Any]) -> LeanProofSearchTraceFull2D | None:
    target = claim_spec.get("target", {})
    if not _is_repeated_collinearity_target(target):
        return None
    side_conditions = _side_conditions(claim_spec)
    target_fact = f"{target.get('family')}:{','.join(map(str, target.get('args', [])))}:positive"
    seed = canonical_json({"target": target, "side_conditions": side_conditions, "rules": ("full2d_rule:incidence_collinearity:02",)})
    return LeanProofSearchTraceFull2D(
        schema_version="1.0.0",
        trace_id=f"lean_rule_trace:{hash_ref(seed)[7:23]}",
        target_fact=target_fact,
        source_statement_hash=str(claim_spec.get("source_statement_hash", "")),
        search_strategy_id="full2d_rule_search:incidence_repeated_collinearity",
        admissible_rule_refs=("full2d_rule:incidence_collinearity:02",),
        used_rule_refs=("full2d_rule:incidence_collinearity:02",),
        used_side_condition_refs=side_conditions,
        semantic_check_status="passed",
    )


def _is_repeated_collinearity_target(target: Any) -> bool:
    if not isinstance(target, dict):
        return False
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    return family in {"incidence", "collinear"} and len(args) == 3 and args[0] == args[1]


def _side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for values in buckets.values():
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


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
