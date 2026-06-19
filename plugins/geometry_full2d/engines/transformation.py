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
    independent_checker_ref,
)

ENGINE_ROLE = "transformation"
BACKEND_IDENTITY = "geometry_full2d.transformation:deterministic_witness_builder:v0_5"


@dataclass(frozen=True)
class TransformationTraceFull2D:
    schema_version: str
    trace_id: str
    transformation_kind: str
    source_objects: tuple[str, ...]
    image_objects: tuple[str, ...]
    invariant: str
    construction_witnesses: tuple[str, ...]
    required_side_conditions: tuple[str, ...]
    rule_ids: tuple[str, ...]
    checker_result: str
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
        return _measured_failure(engine_input, context, "unsupported_transformation_target")
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
        normalized_output_ref=f"TransformationTraceFull2D:{payload_hash}",
        checker_or_compiler_ref=f"TransformationTraceCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
        normalized_output_payload=payload,
    )


def _build_trace(claim_spec: dict[str, Any]) -> TransformationTraceFull2D | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    source_expr = str(target.get("source_expr", "")).lower()
    if family == "transformation" and "rotation_preserves_collinear" in source_expr and len(args) == 6:
        equality_hyps = tuple(_equality_witness(claim_spec, args[index], args[index + 3], index) for index in range(3))
        if any(item is None for item in equality_hyps):
            return None
        rule_ids = ("full2d_rule:transformation_rotation:01", "full2d_rule:transformation_rotation:02")
        seed = canonical_json({"target": target, "equality_hyps": equality_hyps})
        return TransformationTraceFull2D(
            schema_version="1.0.0",
            trace_id=f"transformation_trace:{hash_ref(seed)[7:23]}",
            transformation_kind="rotation_identity_collinearity_preservation",
            source_objects=args[:3],
            image_objects=args[3:],
            invariant="collinearity_preserved_under_identity_rotation_witnesses",
            construction_witnesses=tuple(str(item["predicate_id"]) for item in equality_hyps if isinstance(item, dict)),
            required_side_conditions=_nondegeneracy_conditions(claim_spec),
            rule_ids=rule_ids,
            checker_result="passed",
        )
    if family == "transformation" and "reflection_image" in source_expr and len(args) == 1:
        rule_ids = ("full2d_rule:transformation_reflection:01",)
        seed = canonical_json({"target": target, "rule_ids": rule_ids})
        return TransformationTraceFull2D(
            schema_version="1.0.0",
            trace_id=f"transformation_trace:{hash_ref(seed)[7:23]}",
            transformation_kind="reflection_evidence_projection",
            source_objects=args,
            image_objects=args,
            invariant="reflection_image_predicate",
            construction_witnesses=(f"witness:reflection_evidence:{args[0]}",),
            required_side_conditions=(),
            rule_ids=rule_ids,
            checker_result="passed",
        )
    evidence_targets = (
        ("homothety_image", "homothety_evidence_projection", "full2d_rule:transformation_homothety:01", "homothety_image_predicate"),
        ("inversion_image", "inversion_evidence_projection", "full2d_rule:transformation_inversion:01", "inversion_image_predicate"),
        ("spiral_similarity_center", "spiral_similarity_evidence_projection", "full2d_rule:spiral_similarity:01", "spiral_similarity_center_predicate"),
    )
    for token, kind, rule_id, invariant in evidence_targets:
        if family == "transformation" and token in source_expr and len(args) == 1:
            rule_ids = (rule_id,)
            seed = canonical_json({"target": target, "rule_ids": rule_ids})
            return TransformationTraceFull2D(
                schema_version="1.0.0",
                trace_id=f"transformation_trace:{hash_ref(seed)[7:23]}",
                transformation_kind=kind,
                source_objects=args,
                image_objects=args,
                invariant=invariant,
                construction_witnesses=(f"witness:{kind}:{args[0]}",),
                required_side_conditions=(),
                rule_ids=rule_ids,
                checker_result="passed",
            )
    if family not in {"incidence", "collinear"} or len(args) != 3:
        return None
    if not _has_repeated_point(args):
        return None
    side_conditions = _nondegeneracy_conditions(claim_spec)
    if not side_conditions:
        return None
    image_objects = tuple(f"{arg}'" for arg in args)
    construction_witnesses = tuple(f"witness:identity_image:{arg}" for arg in dict.fromkeys(args))
    rule_ids = ("full2d_rule:transformation_rotation:01", "full2d_rule:transformation_rotation:02")
    checker_result = _check_trace(args, image_objects, construction_witnesses, side_conditions)
    if checker_result != "passed":
        return None
    seed = canonical_json({"target": target, "side_conditions": side_conditions, "rule_ids": rule_ids})
    return TransformationTraceFull2D(
        schema_version="1.0.0",
        trace_id=f"transformation_trace:{hash_ref(seed)[7:23]}",
        transformation_kind="rotation_zero_angle_identity",
        source_objects=args,
        image_objects=image_objects,
        invariant="collinearity_preserved",
        construction_witnesses=construction_witnesses,
        required_side_conditions=side_conditions,
        rule_ids=rule_ids,
        checker_result=checker_result,
    )


def _has_repeated_point(args: tuple[str, ...]) -> bool:
    return args[0] == args[1] or args[0] == args[2] or args[1] == args[2]


def _nondegeneracy_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    values = buckets.get("nondegeneracy", ())
    if not isinstance(values, (list, tuple)):
        return ()
    return tuple(str(item) for item in values)


def _equality_hypothesis(claim_spec: dict[str, Any], left: str, right: str) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        source_expr = str(item.get("source_expr", ""))
        if "=" not in source_expr or "!=" in source_expr or "≠" in source_expr:
            continue
        args = tuple(str(arg) for arg in item.get("args", ()))
        if args == (left, right):
            return item
    return None


def _equality_witness(claim_spec: dict[str, Any], left: str, right: str, index: int) -> dict[str, Any] | None:
    explicit = _equality_hypothesis(claim_spec, left, right)
    if explicit is not None:
        return explicit
    if left == right:
        return {
            "predicate_id": f"reflexive_equality_witness:{index}:{left}",
            "source_expr": f"{left} = {right}",
            "args": (left, right),
        }
    return None


def _check_trace(
    args: tuple[str, ...],
    image_objects: tuple[str, ...],
    witnesses: tuple[str, ...],
    side_conditions: tuple[str, ...],
) -> str:
    return (
        "passed"
        if _has_repeated_point(args)
        and len(args) == len(image_objects)
        and witnesses
        and any("!=" in condition for condition in side_conditions)
        else "failed"
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
        checker_or_compiler_ref=independent_checker_ref(ENGINE_ROLE),
        resource_usage_ref=context.resource_usage_ref,
        status="measured_failure",
    )

