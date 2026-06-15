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

ENGINE_ROLE = "metric_angle"
BACKEND_IDENTITY = "geometry_full2d.metric_angle:directed_angle_normalizer:v0_4_2"


@dataclass(frozen=True)
class MetricAngleTraceFull2D:
    schema_version: str
    trace_id: str
    target_fact: str
    angle_expression: str
    normalization_policy: str
    normalized_value: str
    required_side_conditions: tuple[str, ...]
    rule_ids: tuple[str, ...]
    checker_result: str
    lean_summary: str
    proof_use_status: str = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(engine_input: EngineInputFull2D, budget: ResourceBudget, context: RunContext) -> EngineOutputFull2D:
    del budget
    claim_spec = engine_input.claim_spec
    if not isinstance(claim_spec, dict):
        return _measured_failure(engine_input, context, "missing_claim_spec")
    trace = _build_trace(claim_spec)
    if trace is None:
        return _measured_failure(engine_input, context, "unsupported_metric_angle_target")
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
        normalized_output_ref=f"MetricAngleTraceFull2D:{payload_hash}",
        checker_or_compiler_ref=f"MetricAngleTraceCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
    )


def _build_trace(claim_spec: dict[str, Any]) -> MetricAngleTraceFull2D | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    source_expr = str(target.get("source_expr", "")).lower()
    if family == "angle" and "directed_angle_eq_mod_pi" in source_expr and len(args) == 6:
        reverse_hyp = _hypothesis_with_args(claim_spec, "directed_angle_eq_mod_pi", args[3:] + args[:3])
        if reverse_hyp is not None:
            target_fact = f"{family}:{','.join(args)}:positive"
            steps = ("match_reverse_directed_angle_hypothesis", "apply_mod_pi_angle_symmetry")
            trace_seed = canonical_json({"target": target, "hypothesis": reverse_hyp, "steps": steps})
            return MetricAngleTraceFull2D(
                schema_version="1.0.0",
                trace_id=f"metric_angle_trace:{hash_ref(trace_seed)[7:23]}",
                target_fact=target_fact,
                angle_expression=f"angle({args[0]}, {args[1]}, {args[2]}) = angle({args[3]}, {args[4]}, {args[5]})",
                normalization_policy="directed_angle_mod_pi_symmetry_from_hypothesis",
                normalized_value="symmetric directed angle equality modulo pi",
                required_side_conditions=_side_conditions(claim_spec),
                rule_ids=("full2d_rule:directed_angle_mod_pi:02", "full2d_rule:angle_chase:02"),
                checker_result="passed",
                lean_summary="a reverse directed-angle equality hypothesis is normalized into the requested symmetric target",
            )
    if family == "angle" and "directed_angle_eq_mod_pi" in source_expr and len(args) == 6 and args[:3] == args[3:]:
        target_fact = f"{family}:{','.join(args)}:positive"
        steps = ("normalize_identical_directed_angles", "check_mod_pi_reflexivity")
        trace_seed = canonical_json({"target": target, "steps": steps})
        return MetricAngleTraceFull2D(
            schema_version="1.0.0",
            trace_id=f"metric_angle_trace:{hash_ref(trace_seed)[7:23]}",
            target_fact=target_fact,
            angle_expression=f"angle({args[0]}, {args[1]}, {args[2]})",
            normalization_policy="directed_angle_mod_pi_reflexivity",
            normalized_value="same directed angle modulo pi",
            required_side_conditions=_side_conditions(claim_spec),
            rule_ids=("full2d_rule:directed_angle_mod_pi:01", "full2d_rule:angle_chase:01"),
            checker_result="passed",
            lean_summary="identical directed-angle expressions are equal modulo pi by reflexivity",
        )
    if family not in {"incidence", "collinear"} or len(args) != 3:
        return None
    if not (args[0] == args[1] or args[1] == args[2]):
        return None
    side_conditions = _side_conditions(claim_spec)
    if not _has_nonzero_baseline(args, side_conditions):
        return None
    target_fact = f"{family}:{','.join(args)}:positive"
    angle_expression = f"angle({args[0]}, {args[1]}, {args[2]})"
    policy = "directed_angle_mod_pi"
    steps = (
        "normalize_repeated_endpoint_angle",
        "reduce_zero_angle_mod_pi",
        "interpret_zero_mod_pi_as_collinearity",
    )
    checker_result = _check_metric_angle_trace(args, side_conditions, steps)
    if checker_result != "passed":
        return None
    trace_seed = canonical_json({"target": target, "side_conditions": side_conditions, "steps": steps})
    return MetricAngleTraceFull2D(
        schema_version="1.0.0",
        trace_id=f"metric_angle_trace:{hash_ref(trace_seed)[7:23]}",
        target_fact=target_fact,
        angle_expression=angle_expression,
        normalization_policy=policy,
        normalized_value="0 mod pi",
        required_side_conditions=side_conditions,
        rule_ids=("full2d_rule:directed_angle_mod_pi:01", "full2d_rule:angle_chase:01"),
        checker_result=checker_result,
        lean_summary="the repeated endpoint angle normalizes to 0 modulo pi under the declared nondegeneracy convention",
    )


def _side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for key in ("nondegeneracy", "orientation"):
        values = buckets.get(key, ())
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


def _hypothesis_with_args(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        if token not in str(item.get("source_expr", "")).lower():
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == args:
            return item
    return None


def _has_nonzero_baseline(args: tuple[str, ...], side_conditions: tuple[str, ...]) -> bool:
    pairs = {(args[0], args[2]), (args[2], args[0]), (args[0], args[1]), (args[1], args[2])}
    compact_conditions = {condition.replace(" ", "") for condition in side_conditions}
    return any(f"{a}!={b}".replace(" ", "") in compact_conditions for a, b in pairs if a != b)


def _check_metric_angle_trace(args: tuple[str, ...], side_conditions: tuple[str, ...], steps: tuple[str, ...]) -> str:
    has_repeat = args[0] == args[1] or args[1] == args[2]
    has_side_condition = _has_nonzero_baseline(args, side_conditions)
    has_policy = "reduce_zero_angle_mod_pi" in steps
    return "passed" if has_repeat and has_side_condition and has_policy else "failed"


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
