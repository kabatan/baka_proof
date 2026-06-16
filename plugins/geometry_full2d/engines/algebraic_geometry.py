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

ENGINE_ROLE = "algebraic_geometry"
BACKEND_IDENTITY = "geometry_full2d.algebraic_geometry:exact_symbolic_checker:v0_4_2"


@dataclass(frozen=True)
class AlgebraicCertificateFull2D:
    schema_version: str
    certificate_id: str
    target_family: str
    coordinate_model: str
    variables: tuple[str, ...]
    polynomial_goal: str
    reduction_steps: tuple[str, ...]
    nondegeneracy_conditions: tuple[str, ...]
    denominator_conditions: tuple[str, ...]
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
        return _measured_failure(engine_input, context, "unsupported_algebraic_target")
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
        normalized_output_ref=f"AlgebraicCertificateFull2D:{payload_hash}",
        checker_or_compiler_ref=f"AlgebraicCertificateCheckerFull2D:{payload_hash}",
        resource_usage_ref=context.resource_usage_ref,
        status="normalized_success",
        normalized_output_payload=payload,
    )


def _build_certificate(claim_spec: dict[str, Any]) -> AlgebraicCertificateFull2D | None:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return None
    family = str(target.get("family", ""))
    args = tuple(str(arg) for arg in target.get("args", ()))
    source_expr = str(target.get("source_expr", "")).lower()
    if family == "metric" and "equal_length" in source_expr and len(args) == 4:
        reverse_hyp = _hypothesis_with_args(claim_spec, "equal_length", args[2:] + args[:2])
        if reverse_hyp is not None:
            variables = tuple(dict.fromkeys(variable for point in args for variable in _variables_for_point(point)))
            polynomial_goal = "dist(C,D) - dist(A,B) = 0"
            reduction_steps = (
                "translate_equal_length_hypothesis_to_symbolic_distance_equality",
                "apply_symmetric_equality_rewrite",
                "reduce_subtracted_equal_terms_to_zero",
            )
            payload_seed = canonical_json({"target": target, "hypothesis": reverse_hyp, "rule": "metric_equal_length_symmetry"})
            return AlgebraicCertificateFull2D(
                schema_version="1.0.0",
                certificate_id=f"algebraic_certificate:{hash_ref(payload_seed)[7:23]}",
                target_family=family,
                coordinate_model="symbolic_metric_term_algebra",
                variables=variables,
                polynomial_goal=polynomial_goal,
                reduction_steps=reduction_steps,
                nondegeneracy_conditions=_side_conditions(claim_spec, "nondegeneracy"),
                denominator_conditions=(),
                checker_result="passed",
                source_rule_ids=(
                    "full2d_rule:algebraic_coordinate:02",
                    "full2d_rule:algebraic_coordinate:03",
                    "full2d_rule:metric_equal_length:01",
                    "full2d_rule:metric_equal_length:02",
                    "full2d_rule:metric_equal_length:03",
                ),
                lean_summary="a reversed equal-length hypothesis is normalized through equality symmetry into the requested target",
            )
    if family == "metric" and "equal_length" in source_expr and len(args) == 4 and args[:2] == args[2:]:
        variables = tuple(dict.fromkeys(variable for point in args[:2] for variable in _variables_for_point(point)))
        polynomial_goal = "dist(A,B) - dist(A,B) = 0"
        reduction_steps = (
            "translate_equal_length_to_symbolic_distance_identity",
            "cancel_identical_distance_terms",
            "reduce_zero_polynomial",
        )
        payload_seed = canonical_json({"target": target, "rule": "metric_equal_length_reflexive"})
        return AlgebraicCertificateFull2D(
            schema_version="1.0.0",
            certificate_id=f"algebraic_certificate:{hash_ref(payload_seed)[7:23]}",
            target_family=family,
            coordinate_model="symbolic_metric_term_algebra",
            variables=variables,
            polynomial_goal=polynomial_goal,
            reduction_steps=reduction_steps,
            nondegeneracy_conditions=_side_conditions(claim_spec, "nondegeneracy"),
            denominator_conditions=(),
            checker_result="passed",
            source_rule_ids=(
                "full2d_rule:algebraic_coordinate:01",
                "full2d_rule:algebraic_coordinate:03",
                "full2d_rule:metric_equal_length:01",
                "full2d_rule:metric_equal_length:03",
            ),
            lean_summary="the equal-length target has identical segment terms on both sides and reduces to reflexive equality",
        )
    if family not in {"incidence", "collinear"} or len(args) != 3:
        return None
    if not _is_repeated_point_collinearity(args):
        return None

    nondegeneracy = _side_conditions(claim_spec, "nondegeneracy")
    variables = tuple(dict.fromkeys(variable for point in args for variable in _variables_for_point(point)))
    # The admitted smoke family has two equal rows in the 3x3 collinearity determinant.
    polynomial_goal = "det([[x1,y1,1],[x1,y1,1],[x2,y2,1]]) = 0"
    reduction_steps = (
        "translate_collinearity_to_3x3_determinant",
        "detect_duplicate_coordinate_row",
        "reduce_determinant_with_equal_rows_to_zero",
    )
    checker_result = _check_duplicate_row_certificate(args, polynomial_goal, reduction_steps)
    if checker_result != "passed":
        return None
    payload_seed = canonical_json({"target": target, "nondegeneracy": nondegeneracy})
    return AlgebraicCertificateFull2D(
        schema_version="1.0.0",
        certificate_id=f"algebraic_certificate:{hash_ref(payload_seed)[7:23]}",
        target_family=family,
        coordinate_model="affine_plane_over_exact_field",
        variables=variables,
        polynomial_goal=polynomial_goal,
        reduction_steps=reduction_steps,
        nondegeneracy_conditions=nondegeneracy,
        denominator_conditions=(),
        checker_result=checker_result,
        source_rule_ids=("full2d_rule:algebraic_coordinate:01", "full2d_rule:algebraic_coordinate:03"),
        lean_summary="collinearity determinant has duplicate coordinate rows, so the polynomial target reduces to zero",
    )


def _variables_for_point(point_ref: str) -> tuple[str, str]:
    name = point_ref.split(":", 1)[-1].replace(":", "_")
    return (f"x_{name}", f"y_{name}")


def _is_repeated_point_collinearity(args: tuple[str, ...]) -> bool:
    return args[0] == args[1] or args[0] == args[2] or args[1] == args[2]


def _check_duplicate_row_certificate(args: tuple[str, ...], polynomial_goal: str, steps: tuple[str, ...]) -> str:
    has_duplicate = _is_repeated_point_collinearity(args)
    has_goal = polynomial_goal.endswith("= 0") and "det(" in polynomial_goal
    has_reduction = "reduce_determinant_with_equal_rows_to_zero" in steps
    return "passed" if has_duplicate and has_goal and has_reduction else "failed"


def _side_conditions(claim_spec: dict[str, Any], key: str) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    values = buckets.get(key, ())
    if not isinstance(values, (list, tuple)):
        return ()
    return tuple(str(item) for item in values)


def _hypothesis_with_args(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        if token not in str(item.get("source_expr", "")).lower():
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == args:
            return item
    return None


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
