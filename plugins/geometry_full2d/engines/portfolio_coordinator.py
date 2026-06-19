from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from plugins.geometry_full2d.engine_contracts import (
    ENGINE_ROLES,
    EngineInputFull2D,
    EngineOutputFull2D,
    ResourceBudget,
    RunContext,
    canonical_json,
    hash_ref,
    independent_checker_ref,
)

ENGINE_ROLE = "portfolio_coordinator"
BACKEND_IDENTITY = "geometry_full2d.portfolio_coordinator:deterministic_policy:v0_5"
POLICY_VERSION = "GeometryFull2DPortfolioPolicy:1.0.0"


@dataclass(frozen=True)
class PortfolioDecisionFull2D:
    schema_version: str
    decision_id: str
    policy_version: str
    target_family: str
    selected_engine_order: tuple[str, ...]
    parallel_groups: tuple[tuple[str, ...], ...]
    reason_codes: tuple[str, ...]
    selection_features: dict[str, str]
    llm_semantics_used: bool
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    decision = build_portfolio_decision(claim_spec)
    payload = decision.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"PortfolioDecisionFull2D:{payload_hash}",
        checker_or_compiler_ref=f"PortfolioPolicyCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
        normalized_output_payload=payload,
    )


def build_portfolio_decision(claim_spec: dict[str, Any]) -> PortfolioDecisionFull2D:
    target = claim_spec.get("target", {})
    target_family = str(target.get("family", "unknown")) if isinstance(target, dict) else "unknown"
    features = _selection_features(claim_spec, target_family)
    selected_order, reasons, parallel_groups = _policy(features)
    seed = canonical_json({"features": features, "selected_order": selected_order, "reasons": reasons})
    return PortfolioDecisionFull2D(
        schema_version="1.0.0",
        decision_id=f"portfolio_decision:{hash_ref(seed)[7:23]}",
        policy_version=POLICY_VERSION,
        target_family=target_family,
        selected_engine_order=selected_order,
        parallel_groups=parallel_groups,
        reason_codes=reasons,
        selection_features=features,
        llm_semantics_used=False,
    )


def validate_portfolio_decision(decision: PortfolioDecisionFull2D) -> list[str]:
    errors: list[str] = []
    if decision.policy_version != POLICY_VERSION:
        errors.append("policy_version_mismatch")
    if decision.llm_semantics_used:
        errors.append("llm_semantics_used")
    if not decision.reason_codes:
        errors.append("missing_reason_codes")
    if not decision.selected_engine_order:
        errors.append("missing_engine_order")
    unknown = [role for role in decision.selected_engine_order if role not in ENGINE_ROLES]
    if unknown:
        errors.append(f"unknown_engine_roles:{','.join(unknown)}")
    if decision.selected_engine_order[-1] != "portfolio_coordinator":
        errors.append("portfolio_coordinator_not_terminal")
    return errors


def _selection_features(claim_spec: dict[str, Any], target_family: str) -> dict[str, str]:
    side_conditions = claim_spec.get("side_conditions", {})
    side_count = 0
    if isinstance(side_conditions, dict):
        side_count = sum(len(values) for values in side_conditions.values() if isinstance(values, (list, tuple)))
    object_count = len(claim_spec.get("objects", ())) if isinstance(claim_spec.get("objects", ()), (list, tuple)) else 0
    return {
        "target_family": target_family,
        "side_condition_count": str(side_count),
        "object_count": str(object_count),
        "has_claim_spec": "true",
    }


def _policy(features: dict[str, str]) -> tuple[tuple[str, ...], tuple[str, ...], tuple[tuple[str, ...], ...]]:
    family = features["target_family"]
    if family in {"incidence", "collinear"}:
        order = (
            "synthetic_closure",
            "construction_search",
            "metric_angle",
            "algebraic_geometry",
            "transformation",
            "order_case",
            "inequality",
            "lean_proof_search",
            "portfolio_coordinator",
        )
        reasons = (
            "target_family:incidence_prefers_synthetic_first",
            "side_conditions:domain_engines_after_primary_trace",
            "proof_candidate:last_after_normalized_artifacts",
            "policy:no_llm_semantics",
        )
        parallel = (("metric_angle", "algebraic_geometry"), ("transformation", "order_case", "inequality"))
        return order, reasons, parallel
    order = ENGINE_ROLES
    reasons = ("target_family:generic_full_order", "policy:no_llm_semantics")
    return order, reasons, (("synthetic_closure", "algebraic_geometry"),)


def semantic_rule_ids(claim_spec: dict[str, Any], primary_family: str) -> list[str]:
    text = " ".join(
        [str((claim_spec.get("target") or {}).get("source_expr", ""))]
        + [str(h.get("source_expr", "")) for h in claim_spec.get("hypotheses", []) if isinstance(h, dict)]
    )
    families = [primary_family]
    token_map = {
        "collinear": "incidence_collinearity",
        "between": "order_between",
        "midpoint": "midpoint_segment",
        "equal_length": "metric_equal_length",
        "length_le": "inequality_length",
        "directed_angle": "directed_angle_mod_pi",
        "circle": "construction_circle",
        "chord": "circle_cyclicity",
        "reflection": "transformation_reflection",
        "rotation": "transformation_rotation",
        "line_circle_intersection": "construction_intersection",
        "equilateral": "triangle_congruence",
    }
    for token, family in token_map.items():
        if token in text:
            families.append(family)
    out: list[str] = []
    seed = canonical_json(claim_spec)
    for family in dict.fromkeys(families):
        index = int(hash_ref(family + seed)[7:15], 16) % 5 + 1
        out.append(f"full2d_rule:{family}:{index:02d}")
    while len(out) < 2:
        out.append("full2d_rule:incidence_collinearity:01")
    return out[:4]


def find_hypothesis(hypotheses: list[dict[str, Any]], token: str, args: list[str]) -> dict[str, Any] | None:
    wanted = canonical_args(args)
    for hypothesis in hypotheses:
        if token in str(hypothesis.get("source_expr", "")) and canonical_args(hypothesis.get("args", [])) == wanted:
            return hypothesis
    return None


def find_hypothesis_by_source(hypotheses: list[dict[str, Any]], token: str) -> dict[str, Any] | None:
    for hypothesis in hypotheses:
        if token in str(hypothesis.get("source_expr", "")):
            return hypothesis
    return None


def find_length_le_chain(hypotheses: list[dict[str, Any]], target_args: list[str]) -> tuple[str, str, tuple[str, str]] | None:
    normalized_target_args = list(canonical_args(target_args))
    length_hyps = [
        (hypothesis_name(item), canonical_args(item.get("args", [])))
        for item in hypotheses
        if "length_le" in str(item.get("source_expr", ""))
    ]
    for first_name, first_args in length_hyps:
        if len(first_args) != 4 or list(first_args[:2]) != normalized_target_args[:2]:
            continue
        for second_name, second_args in length_hyps:
            if len(second_args) == 4 and first_args[2:] == second_args[:2] and list(second_args[2:]) == normalized_target_args[2:]:
                return first_name, second_name, (first_args[2], first_args[3])
    return None


def target_fact(claim_spec: dict[str, Any]) -> str:
    target = claim_spec.get("target", {}) if isinstance(claim_spec.get("target"), dict) else {}
    return f"{target.get('family')}:{','.join(str(item) for item in target.get('args', []))}:positive"


def hypothesis_name(hypothesis: dict[str, Any]) -> str:
    return str(hypothesis.get("predicate_id", "h0")).split(":")[-1]


def canonical_args(values: Any) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        return tuple()
    return tuple(canonical_arg(value) for value in values)


def canonical_arg(value: Any) -> str:
    text = str(value)
    return text.split(":", 1)[1] if ":" in text else text


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
        checker_or_compiler_ref=independent_checker_ref(ENGINE_ROLE),
        resource_usage_ref=context.resource_usage_ref,
        status="measured_failure",
    )

