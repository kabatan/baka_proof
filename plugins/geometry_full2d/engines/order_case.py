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

ENGINE_ROLE = "order_case"
BACKEND_IDENTITY = "geometry_full2d.order_case:finite_coverage_gate:v0_4_2"


@dataclass(frozen=True)
class ProofStateDAGCaseFull2D:
    case_id: str
    assumptions: tuple[str, ...]
    obligations: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoverageGateFull2D:
    schema_version: str
    gate_id: str
    target_fact: str
    cases: tuple[ProofStateDAGCaseFull2D, ...]
    coverage_rule_ids: tuple[str, ...]
    coverage_result: str
    lean_summary: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["cases"] = [case.to_dict() for case in self.cases]
        return payload


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    gate = _build_gate(claim_spec)
    if gate is None:
        return _measured_failure(engine_input, context, "unsupported_order_case_target")
    payload = gate.to_dict()
    payload_hash = hash_ref(canonical_json(payload))
    return EngineOutputFull2D(
        schema_version="1.0.0",
        engine_role=ENGINE_ROLE,
        backend_identity=BACKEND_IDENTITY,
        real_integration_flag=True,
        fixture_flag=False,
        input_ref=engine_input.input_ref(),
        raw_output_hash=payload_hash,
        normalized_output_ref=f"CoverageGateFull2D:{payload_hash}",
        checker_or_compiler_ref=f"CoverageGateCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
    )


def _build_gate(claim_spec: dict[str, Any]) -> CoverageGateFull2D | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    if family not in {"incidence", "collinear"} or len(args) != 3:
        return None
    between_hypothesis = _has_between_hypothesis(claim_spec, args)
    if between_hypothesis:
        target_fact = f"{family}:{','.join(args)}:positive"
        assumptions = _side_conditions(claim_spec)
        case = ProofStateDAGCaseFull2D(
            case_id="case:between_implies_collinearity",
            assumptions=assumptions + (between_hypothesis,),
            obligations=(target_fact,),
            status="closed_by_between_order",
        )
        coverage_rule_ids = (
            "full2d_rule:order_between:01",
            "full2d_rule:order_between:02",
            "full2d_rule:case_split_orientation:01",
            "full2d_rule:case_split_orientation:02",
        )
        coverage_result = _check_coverage((case,), coverage_rule_ids, accepted_statuses={"closed_by_between_order"})
        if coverage_result != "passed":
            return None
        seed = canonical_json({"target": target, "case": case.to_dict(), "coverage_rule_ids": coverage_rule_ids})
        return CoverageGateFull2D(
            schema_version="1.0.0",
            gate_id=f"coverage_gate:{hash_ref(seed)[7:23]}",
            target_fact=target_fact,
            cases=(case,),
            coverage_rule_ids=coverage_rule_ids,
            coverage_result=coverage_result,
            lean_summary="the declared between relation closes the collinearity target through the order-case rule",
        )
    if not _has_repeated_point(args):
        return None
    target_fact = f"{family}:{','.join(args)}:positive"
    assumptions = _side_conditions(claim_spec)
    case = ProofStateDAGCaseFull2D(
        case_id="case:repeated_point_collinearity",
        assumptions=assumptions,
        obligations=(target_fact,),
        status="closed_by_repeated_point",
    )
    coverage_rule_ids = ("full2d_rule:case_split_orientation:01", "full2d_rule:case_split_orientation:02")
    coverage_result = _check_coverage((case,), coverage_rule_ids, accepted_statuses={"closed_by_repeated_point"})
    if coverage_result != "passed":
        return None
    seed = canonical_json({"target": target, "case": case.to_dict(), "coverage_rule_ids": coverage_rule_ids})
    return CoverageGateFull2D(
        schema_version="1.0.0",
        gate_id=f"coverage_gate:{hash_ref(seed)[7:23]}",
        target_fact=target_fact,
        cases=(case,),
        coverage_rule_ids=coverage_rule_ids,
        coverage_result=coverage_result,
        lean_summary="the repeated-point smoke target has a singleton closed case, so no additional order split is required",
    )


def _side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for key in ("nondegeneracy", "orientation", "order_cases"):
        values = buckets.get(key, ())
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


def _has_repeated_point(args: tuple[str, ...]) -> bool:
    return args[0] == args[1] or args[0] == args[2] or args[1] == args[2]


def _has_between_hypothesis(claim_spec: dict[str, Any], args: tuple[str, ...]) -> str | None:
    for hypothesis in claim_spec.get("hypotheses", ()):
        if not isinstance(hypothesis, dict):
            continue
        if "between" not in str(hypothesis.get("source_expr", "")).lower():
            continue
        if tuple(str(arg) for arg in hypothesis.get("args", ())) == args:
            return str(hypothesis.get("predicate_id", "hyp:between"))
    return None


def _check_coverage(
    cases: tuple[ProofStateDAGCaseFull2D, ...],
    rule_ids: tuple[str, ...],
    *,
    accepted_statuses: set[str],
) -> str:
    if not cases or not rule_ids:
        return "failed"
    if any(case.status not in accepted_statuses for case in cases):
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
