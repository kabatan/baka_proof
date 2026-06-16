from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES, canonical_json
from plugins.geometry_full2d.run_records import content_addressed_typed_ref


COMPILER_BY_ROLE: dict[str, str] = {
    "synthetic_closure": "TraceCompilerFull2D",
    "construction_search": "ConstructionCompilerFull2D",
    "algebraic_geometry": "AlgebraicCompilerFull2D",
    "metric_angle": "MetricAngleCompilerFull2D",
    "transformation": "TransformationCompilerFull2D",
    "order_case": "OrderCaseCompilerFull2D",
    "inequality": "InequalityCompilerFull2D",
    "lean_proof_search": "LeanProofSearchCompilerFull2D",
    "portfolio_coordinator": "PortfolioCompilerFull2D",
}

RULES_BY_ROLE: dict[str, tuple[str, ...]] = {
    "synthetic_closure": ("full2d_rule:incidence_collinearity:02",),
    "construction_search": ("full2d_rule:construction_line:01",),
    "algebraic_geometry": ("full2d_rule:algebraic_coordinate:01",),
    "metric_angle": ("full2d_rule:directed_angle_mod_pi:01", "full2d_rule:angle_chase:01"),
    "transformation": ("full2d_rule:transformation_reflection:01",),
    "order_case": ("full2d_rule:case_split_orientation:01",),
    "inequality": ("full2d_rule:inequality_length:01",),
    "lean_proof_search": ("full2d_rule:incidence_collinearity:02",),
    "portfolio_coordinator": ("full2d_rule:incidence_collinearity:02",),
}

FORBIDDEN_PROOF_TOKENS = re.compile(r"\b(sorry|axiom|admit|unsafe)\b")


@dataclass(frozen=True)
class CompilerResultFull2D:
    schema_version: str
    compiler_result_ref: str
    result_id: str
    compiler_id: str
    task_id: str
    claim_spec_ref: str
    provider_run_manifest_ref: str
    consumed_engine_output_refs: tuple[str, ...]
    input_engine_output_refs: tuple[str, ...]
    consumed_normalized_output_refs: tuple[str, ...]
    proof_derivation_ref: str
    proof_derivation_input_refs: tuple[str, ...]
    proof_derivation_witnesses: tuple[dict[str, Any], ...]
    consumed_rule_ids: tuple[str, ...]
    used_rule_ids: tuple[str, ...]
    used_rule_refs: tuple[str, ...]
    generated_obligations: tuple[str, ...]
    side_condition_report_ref: str
    lean_patch_candidate_ref: str | None
    status: Literal["compiled_patch", "measured_failure"]
    proof_use_status: Literal["not_allowed"] = "not_allowed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LeanPatchCandidateFull2D:
    schema_version: str
    patch_id: str
    target_theorem_name: str
    target_statement_hash: str
    allowed_edit_region: dict[str, str]
    proof_region_replacement_ref: str
    proof_region_replacement_text: str
    source_compiler_result_refs: tuple[str, ...]
    compiler_result_refs: tuple[str, ...]
    source_engine_output_refs: tuple[str, ...]
    source_rule_ids: tuple[str, ...]
    used_rule_ids: tuple[str, ...]
    used_rule_refs: tuple[str, ...]
    provider_run_manifest_ref: str
    claim_spec_ref: str
    solver_dependency_refs: tuple[str, ...]
    proof_derivation_ref: str
    proof_derivation_input_refs: tuple[str, ...]
    proof_derivation_witnesses: tuple[dict[str, Any], ...]
    raw_provider_output_used_as_proof: bool
    status: Literal["lean_patch_candidate"] = "lean_patch_candidate"
    proof_use_status: Literal["lean_patch_candidate"] = "lean_patch_candidate"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Full2DCompilerRun:
    compiler_results: tuple[CompilerResultFull2D, ...]
    lean_patch_candidate: LeanPatchCandidateFull2D
    compiler_result_refs: tuple[str, ...]
    lean_patch_candidate_ref: str
    artifact_paths: dict[str, str]


def compile_full2d_engine_outputs(
    *,
    task_id: str,
    claim_spec: dict[str, Any],
    claim_spec_ref: str,
    provider_run_manifest_ref: str,
    engine_outputs: dict[str, dict[str, Any]],
    artifact_root: Path | None = None,
    artifact_paths: dict[str, str] | None = None,
) -> Full2DCompilerRun:
    if not engine_outputs:
        raise ValueError("compiler_requires_engine_output_artifacts")
    artifact_paths = artifact_paths if artifact_paths is not None else {}
    usable = {
        ref: payload
        for ref, payload in engine_outputs.items()
        if payload.get("status") == "normalized_success" and payload.get("normalized_output_ref")
    }
    if not usable:
        raise ValueError("compiler_found_no_normalized_engine_outputs")
    proof_text, selected_rule_ids = _proof_text_from_claim_and_rules(claim_spec, usable)
    proof_text = _with_solver_intermediate_if_substantive(
        claim_spec=claim_spec,
        proof_text=proof_text,
        selected_rule_ids=selected_rule_ids,
    )
    proof_derivation_witnesses = _semantic_witnesses_for_rules(usable, selected_rule_ids)
    proof_derivation_input_refs = tuple(str(witness["normalized_output_ref"]) for witness in proof_derivation_witnesses)
    if not proof_derivation_input_refs:
        raise ValueError("compiler_found_no_normalized_semantic_derivation_inputs")
    patch_proof_derivation_ref = _proof_derivation_ref(
        claim_spec_ref=claim_spec_ref,
        proof_text=proof_text,
        selected_rule_ids=selected_rule_ids,
        proof_derivation_input_refs=proof_derivation_input_refs,
        proof_derivation_witnesses=proof_derivation_witnesses,
    )
    side_condition_report_ref = _side_condition_report_ref(claim_spec)
    compiler_results: list[CompilerResultFull2D] = []
    compiler_refs: list[str] = []
    for engine_ref, engine_payload in sorted(usable.items()):
        role = str(engine_payload.get("engine_role", ""))
        if role not in ENGINE_ROLES:
            continue
        normalized_payload = engine_payload.get("normalized_output_payload")
        if not isinstance(normalized_payload, dict) or not _semantic_rule_ids(normalized_payload):
            continue
        role_rules = tuple(dict.fromkeys(RULES_BY_ROLE[role] + _selected_rules_for_role(role, selected_rule_ids)))
        result_derivation_witnesses = (_engine_derivation_witness(engine_ref, engine_payload),)
        result_derivation_inputs = (str(engine_payload["normalized_output_ref"]),)
        result_derivation_ref = _proof_derivation_ref(
            claim_spec_ref=claim_spec_ref,
            proof_text=proof_text,
            selected_rule_ids=role_rules,
            proof_derivation_input_refs=result_derivation_inputs,
            proof_derivation_witnesses=result_derivation_witnesses,
        )
        payload = {
            "schema_version": "1.0.0",
            "compiler_id": COMPILER_BY_ROLE[role],
            "task_id": task_id,
            "claim_spec_ref": claim_spec_ref,
            "provider_run_manifest_ref": provider_run_manifest_ref,
            "consumed_engine_output_refs": [engine_ref],
            "input_engine_output_refs": [engine_ref],
            "consumed_normalized_output_refs": [str(engine_payload["normalized_output_ref"])],
            "proof_derivation_ref": result_derivation_ref,
            "proof_derivation_input_refs": list(result_derivation_inputs),
            "proof_derivation_witnesses": list(result_derivation_witnesses),
            "consumed_rule_ids": list(role_rules),
            "used_rule_ids": list(role_rules),
            "used_rule_refs": list(role_rules),
            "generated_obligations": _generated_obligations(claim_spec, role),
            "side_condition_report_ref": side_condition_report_ref,
            "lean_patch_candidate_ref": None,
            "status": "compiled_patch",
            "proof_use_status": "not_allowed",
        }
        result_ref = content_addressed_typed_ref("CompilerResultFull2D", payload)
        result = CompilerResultFull2D(
            compiler_result_ref=result_ref,
            result_id=result_ref,
            **_tupled_compiler_payload(payload),
        )
        errors = validate_compiler_result_full2d(result.to_dict(), available_engine_output_refs=set(engine_outputs))
        if errors:
            raise ValueError(";".join(errors))
        compiler_results.append(result)
        compiler_refs.append(result_ref)
        if artifact_root is not None:
            _write_typed_json(
                artifact_root,
                f"compiler_result_{role}",
                "CompilerResultFull2D",
                "result_id",
                payload,
                artifact_paths,
            )

    if not compiler_results:
        raise ValueError("compiler_no_role_outputs_admitted")
    patch_payload_without_id = _patch_payload_without_id(
        claim_spec=claim_spec,
        claim_spec_ref=claim_spec_ref,
        provider_run_manifest_ref=provider_run_manifest_ref,
        proof_text=proof_text,
        compiler_refs=tuple(compiler_refs),
        engine_refs=tuple(sorted(usable)),
        rule_ids=tuple(dict.fromkeys(selected_rule_ids + tuple(rule for result in compiler_results for rule in result.consumed_rule_ids))),
        proof_derivation_ref=patch_proof_derivation_ref,
        proof_derivation_input_refs=proof_derivation_input_refs,
        proof_derivation_witnesses=proof_derivation_witnesses,
    )
    patch_ref = content_addressed_typed_ref("LeanPatchCandidateFull2D", patch_payload_without_id)
    patch = LeanPatchCandidateFull2D(patch_id=patch_ref, **_tupled_patch_payload(patch_payload_without_id))
    patch_errors = validate_lean_patch_candidate_full2d(
        patch.to_dict(),
        available_compiler_result_refs=set(compiler_refs),
        available_engine_output_refs=set(engine_outputs),
    )
    if patch_errors:
        raise ValueError(";".join(patch_errors))
    if artifact_root is not None:
        _write_sha_text(artifact_root, "proof_region_replacement", proof_text, artifact_paths)
        _write_typed_json(
            artifact_root,
            "lean_patch_candidate",
            "LeanPatchCandidateFull2D",
            "patch_id",
            patch_payload_without_id,
            artifact_paths,
        )
    return Full2DCompilerRun(
        compiler_results=tuple(compiler_results),
        lean_patch_candidate=patch,
        compiler_result_refs=tuple(compiler_refs),
        lean_patch_candidate_ref=patch_ref,
        artifact_paths=artifact_paths,
    )


def validate_compiler_result_full2d(
    payload: dict[str, Any],
    *,
    available_engine_output_refs: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "compiler_result_ref",
        "result_id",
        "compiler_id",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "consumed_engine_output_refs",
        "consumed_normalized_output_refs",
        "proof_derivation_ref",
        "proof_derivation_input_refs",
        "proof_derivation_witnesses",
        "consumed_rule_ids",
        "generated_obligations",
        "side_condition_report_ref",
        "lean_patch_candidate_ref",
        "status",
        "proof_use_status",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"compiler_missing_fields:{','.join(missing)}"]
    if payload["schema_version"] != "1.0.0":
        errors.append("compiler_schema_version_mismatch")
    expected = content_addressed_typed_ref("CompilerResultFull2D", _without_identity(payload))
    if payload["compiler_result_ref"] != expected or payload["result_id"] != expected:
        errors.append("compiler_result_ref_content_mismatch")
    consumed = _as_str_tuple(payload.get("consumed_engine_output_refs"))
    if not consumed:
        errors.append("compiler_missing_consumed_engine_output_refs")
    elif available_engine_output_refs is not None and not set(consumed).issubset(available_engine_output_refs):
        errors.append("compiler_consumed_unknown_engine_output_ref")
    rule_ids = _as_str_tuple(payload.get("consumed_rule_ids"))
    normalized_refs = _as_str_tuple(payload.get("consumed_normalized_output_refs"))
    direct_lean_mode = payload.get("compile_mode") == "proof_worker_only_direct_lean"
    measured_failure_mode = payload.get("status") == "measured_failure"
    if not normalized_refs and not direct_lean_mode and not measured_failure_mode:
        errors.append("compiler_missing_consumed_normalized_output_refs")
    derivation_inputs = _as_str_tuple(payload.get("proof_derivation_input_refs"))
    derivation_witnesses = _as_witness_tuple(payload.get("proof_derivation_witnesses"))
    if not derivation_inputs:
        errors.append("compiler_missing_proof_derivation_input_refs")
    if not derivation_witnesses:
        errors.append("compiler_missing_proof_derivation_witnesses")
    elif not direct_lean_mode and not measured_failure_mode and not set(derivation_inputs).issubset(set(normalized_refs)):
        errors.append("compiler_derivation_inputs_not_normalized_refs")
    elif measured_failure_mode and not set(derivation_inputs).issubset(set(consumed)):
        errors.append("compiler_measured_failure_derivation_inputs_not_engine_refs")
    errors.extend(_validate_derivation_witnesses(
        derivation_witnesses,
        consumed_engine_refs=consumed,
        normalized_refs=normalized_refs,
        derivation_inputs=derivation_inputs,
        mode="direct" if direct_lean_mode else "measured_failure" if measured_failure_mode else "normalized_success",
    ))
    if not str(payload.get("proof_derivation_ref", "")).startswith("sha256:"):
        errors.append("compiler_missing_proof_derivation_ref")
    if not rule_ids:
        errors.append("compiler_missing_consumed_rule_ids")
    elif any(not rule.startswith("full2d_rule:") for rule in rule_ids):
        errors.append("compiler_consumed_rule_id_prefix_mismatch")
    if payload["compiler_id"] not in set(COMPILER_BY_ROLE.values()):
        errors.append("compiler_id_unknown")
    if payload["proof_use_status"] != "not_allowed":
        errors.append("compiler_proof_use_status_violation")
    if payload["status"] not in {"compiled_patch", "measured_failure"}:
        errors.append("compiler_status_invalid")
    if _has_benchmark_label_source(payload):
        errors.append("compiler_benchmark_label_source_detected")
    return sorted(set(errors))


def validate_lean_patch_candidate_full2d(
    payload: dict[str, Any],
    *,
    available_compiler_result_refs: set[str] | None = None,
    available_engine_output_refs: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "patch_id",
        "target_theorem_name",
        "target_statement_hash",
        "allowed_edit_region",
        "proof_region_replacement_ref",
        "proof_region_replacement_text",
        "source_compiler_result_refs",
        "source_engine_output_refs",
        "source_rule_ids",
        "proof_derivation_ref",
        "proof_derivation_input_refs",
        "proof_derivation_witnesses",
        "raw_provider_output_used_as_proof",
        "proof_use_status",
    }
    missing = sorted(required - set(payload))
    if missing:
        return [f"patch_missing_fields:{','.join(missing)}"]
    if payload["schema_version"] != "1.0.0":
        errors.append("patch_schema_version_mismatch")
    expected = content_addressed_typed_ref("LeanPatchCandidateFull2D", _without_identity(payload))
    if payload["patch_id"] != expected:
        errors.append("patch_id_content_mismatch")
    compiler_refs = _as_str_tuple(payload.get("source_compiler_result_refs"))
    if not compiler_refs:
        errors.append("patch_missing_source_compiler_result_refs")
    elif available_compiler_result_refs is not None and not set(compiler_refs).issubset(available_compiler_result_refs):
        errors.append("patch_unknown_source_compiler_result_ref")
    engine_refs = _as_str_tuple(payload.get("source_engine_output_refs"))
    if not engine_refs:
        errors.append("patch_missing_source_engine_output_refs")
    elif available_engine_output_refs is not None and not set(engine_refs).issubset(available_engine_output_refs):
        errors.append("patch_unknown_source_engine_output_ref")
    rule_ids = _as_str_tuple(payload.get("source_rule_ids"))
    if not rule_ids:
        errors.append("patch_missing_source_rule_ids")
    elif any(not rule.startswith("full2d_rule:") for rule in rule_ids):
        errors.append("patch_rule_id_prefix_mismatch")
    if payload["raw_provider_output_used_as_proof"] is not False:
        errors.append("patch_raw_provider_output_used_as_proof")
    derivation_inputs = _as_str_tuple(payload.get("proof_derivation_input_refs"))
    derivation_witnesses = _as_witness_tuple(payload.get("proof_derivation_witnesses"))
    if not derivation_inputs:
        errors.append("patch_missing_proof_derivation_input_refs")
    if not derivation_witnesses:
        errors.append("patch_missing_proof_derivation_witnesses")
    errors.extend(_validate_derivation_witnesses(
        derivation_witnesses,
        consumed_engine_refs=engine_refs,
        normalized_refs=tuple(str(item.get("normalized_output_ref")) for item in derivation_witnesses if isinstance(item.get("normalized_output_ref"), str)),
        derivation_inputs=derivation_inputs,
        mode="direct" if payload.get("compile_mode") == "proof_worker_only_direct_lean" else "measured_failure" if payload.get("failure_reason") else "normalized_success",
    ))
    if not str(payload.get("proof_derivation_ref", "")).startswith("sha256:"):
        errors.append("patch_missing_proof_derivation_ref")
    proof_text = str(payload.get("proof_region_replacement_text", ""))
    if FORBIDDEN_PROOF_TOKENS.search(proof_text):
        errors.append("patch_contains_forbidden_proof_token")
    if _has_benchmark_label_source(payload):
        errors.append("patch_benchmark_label_source_detected")
    region = payload.get("allowed_edit_region")
    if not isinstance(region, dict) or region.get("policy") != "MARP proof region only":
        errors.append("patch_allowed_region_policy_mismatch")
    if payload["proof_use_status"] != "lean_patch_candidate":
        errors.append("patch_proof_use_status_mismatch")
    return sorted(set(errors))


def _patch_payload_without_id(
    *,
    claim_spec: dict[str, Any],
    claim_spec_ref: str,
    provider_run_manifest_ref: str,
    proof_text: str,
    compiler_refs: tuple[str, ...],
    engine_refs: tuple[str, ...],
    rule_ids: tuple[str, ...],
    proof_derivation_ref: str,
    proof_derivation_input_refs: tuple[str, ...],
    proof_derivation_witnesses: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    theorem_name = str(claim_spec["theorem_name"])
    replacement_ref = _sha_text(proof_text)
    return {
        "schema_version": "1.0.0",
        "target_theorem_name": theorem_name,
        "target_statement_hash": str(claim_spec["source_statement_hash"]),
        "allowed_edit_region": {
            "policy": "MARP proof region only",
            "region_id": f"proof_region:{theorem_name}",
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "proof_region_replacement_ref": replacement_ref,
        "proof_region_replacement_text": proof_text,
        "source_compiler_result_refs": list(compiler_refs),
        "compiler_result_refs": list(compiler_refs),
        "source_engine_output_refs": list(engine_refs),
        "source_rule_ids": list(rule_ids),
        "used_rule_ids": list(rule_ids),
        "used_rule_refs": list(rule_ids),
        "provider_run_manifest_ref": provider_run_manifest_ref,
        "claim_spec_ref": claim_spec_ref,
        "solver_dependency_refs": [provider_run_manifest_ref, *engine_refs, *compiler_refs],
        "proof_derivation_ref": proof_derivation_ref,
        "proof_derivation_input_refs": list(proof_derivation_input_refs),
        "proof_derivation_witnesses": list(proof_derivation_witnesses),
        "raw_provider_output_used_as_proof": False,
        "status": "lean_patch_candidate",
        "proof_use_status": "lean_patch_candidate",
    }


def _proof_text_from_claim_and_rules(
    claim_spec: dict[str, Any],
    engine_outputs: dict[str, dict[str, Any]],
) -> tuple[str, tuple[str, ...]]:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        raise ValueError("claim_target_not_object")
    args = tuple(str(arg) for arg in target.get("args", []))
    family = str(target.get("family", ""))
    source_expr = _source_expr(target)
    names = _object_names(claim_spec)
    roles = _available_roles(engine_outputs)
    semantic_rules = _available_semantic_rules(engine_outputs)

    if family in {"incidence", "collinear"} and len(args) == 3:
        midpoint_hyp = _hypothesis_for(claim_spec, "midpoint", args)
        if midpoint_hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "construction_search", "full2d_rule:midpoint_segment:01")
            a, m, b = (_object_ref_to_name(ref, names) for ref in args)
            return (
                f"  exact midpoint_collinear {a} {m} {b} {_hypothesis_name(midpoint_hyp)}",
                (
                    "full2d_rule:construction_line:01",
                    "full2d_rule:construction_line:02",
                    "full2d_rule:midpoint_segment:01",
                    "full2d_rule:midpoint_segment:02",
                ),
            )

        between_hyp = _hypothesis_for(claim_spec, "between", args)
        if between_hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "order_case", "full2d_rule:order_between:01")
            a, b, c = (_object_ref_to_name(ref, names) for ref in args)
            return (
                f"  exact between_collinear {a} {b} {c} {_hypothesis_name(between_hyp)}",
                (
                    "full2d_rule:case_split_orientation:01",
                    "full2d_rule:case_split_orientation:02",
                    "full2d_rule:order_between:01",
                    "full2d_rule:order_between:02",
                ),
            )

        if args[0] == args[1]:
            _require_semantic_rule(roles, semantic_rules, "lean_proof_search", "full2d_rule:incidence_collinearity:02")
            left = _object_ref_to_name(args[0], names)
            right = _object_ref_to_name(args[2], names)
            return (
                f"  exact collinear_refl_left {left} {right}",
                (
                    "full2d_rule:incidence_collinearity:01",
                    "full2d_rule:incidence_collinearity:02",
                    "full2d_rule:incidence_collinearity:03",
                ),
            )

    if family == "construction" and "constructed_circle_point" in source_expr and len(args) == 3:
        hyp = _hypothesis_for_args(claim_spec, "circle_with_center_through_point", args)
        if hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "construction_search", "full2d_rule:construction_circle:01")
            o, p, c = (_object_ref_to_name(ref, names) for ref in args)
            return (
                f"  exact circle_construction_on_circle {o} {p} {c} {_hypothesis_name(hyp)}",
                ("full2d_rule:construction_circle:01", "full2d_rule:construction_circle:02"),
            )

    if family == "construction" and "constructed_line_circle_point" in source_expr and len(args) == 3:
        hyp = _hypothesis_for_args(claim_spec, "line_circle_intersection", args)
        if hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "construction_search", "full2d_rule:construction_intersection:01")
            p, l, c = (_object_ref_to_name(ref, names) for ref in args)
            return (
                f"  exact line_circle_intersection_on_line {p} {l} {c} {_hypothesis_name(hyp)}",
                ("full2d_rule:construction_intersection:01", "full2d_rule:construction_intersection:02"),
            )

    if family == "construction" and "constructed_center_point" in source_expr and len(args) == 2:
        hyp = _hypothesis_for_args(claim_spec, "constructed_center_point", args)
        if hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "construction_search", "full2d_rule:construction_center:01")
            o, c = (_object_ref_to_name(ref, names) for ref in args)
            return (
                f"  exact constructed_center_identity {o} {c} {_hypothesis_name(hyp)}",
                ("full2d_rule:construction_center:01", "full2d_rule:construction_center:02"),
            )

    if family == "angle" and "directed_angle_eq_mod_pi" in source_expr and len(args) == 6 and args[:3] == args[3:]:
        _require_semantic_rule(roles, semantic_rules, "metric_angle", "full2d_rule:directed_angle_mod_pi:01")
        a, b, c = (_object_ref_to_name(ref, names) for ref in args[:3])
        return (
            f"  exact directed_angle_eq_refl {a} {b} {c}",
            (
                "full2d_rule:directed_angle_mod_pi:01",
                "full2d_rule:directed_angle_mod_pi:03",
                "full2d_rule:angle_chase:01",
                "full2d_rule:angle_chase:03",
            ),
        )

    if family == "angle" and "directed_angle_eq_mod_pi" in source_expr and len(args) == 6:
        reverse_hyp = _hypothesis_for_args(claim_spec, "directed_angle_eq_mod_pi", args[3:] + args[:3])
        if reverse_hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "metric_angle", "full2d_rule:directed_angle_mod_pi:02")
            d, e, f, a, b, c = (_object_ref_to_name(ref, names) for ref in args[3:] + args[:3])
            return (
                f"  exact directed_angle_eq_symm {d} {e} {f} {a} {b} {c} {_hypothesis_name(reverse_hyp)}",
                (
                    "full2d_rule:directed_angle_mod_pi:02",
                    "full2d_rule:directed_angle_mod_pi:03",
                    "full2d_rule:angle_chase:02",
                    "full2d_rule:angle_chase:03",
                ),
            )

    if family == "metric" and "equal_length" in source_expr and len(args) == 4 and args[:2] == args[2:]:
        _require_semantic_rule(roles, semantic_rules, "algebraic_geometry", "full2d_rule:metric_equal_length:03")
        a, b = (_object_ref_to_name(ref, names) for ref in args[:2])
        return (
            f"  exact equal_length_refl {a} {b}",
            (
                "full2d_rule:algebraic_coordinate:01",
                "full2d_rule:algebraic_coordinate:03",
                "full2d_rule:metric_equal_length:01",
                "full2d_rule:metric_equal_length:03",
            ),
        )

    if family == "metric" and "equal_length" in source_expr and len(args) == 4:
        reverse_hyp = _hypothesis_for_args(claim_spec, "equal_length", args[2:] + args[:2])
        if reverse_hyp is not None:
            _require_semantic_rule(roles, semantic_rules, "algebraic_geometry", "full2d_rule:metric_equal_length:02")
            a, b, c, d = (_object_ref_to_name(ref, names) for ref in args[2:] + args[:2])
            return (
                f"  exact equal_length_symm {a} {b} {c} {d} {_hypothesis_name(reverse_hyp)}",
                (
                    "full2d_rule:algebraic_coordinate:02",
                    "full2d_rule:algebraic_coordinate:03",
                    "full2d_rule:metric_equal_length:01",
                    "full2d_rule:metric_equal_length:02",
                    "full2d_rule:metric_equal_length:03",
                ),
            )

    if family == "inequality" and "length_le" in source_expr and len(args) == 4 and args[:2] == args[2:]:
        _require_semantic_rule(roles, semantic_rules, "inequality", "full2d_rule:inequality_length:01")
        a, b = (_object_ref_to_name(ref, names) for ref in args[:2])
        return (
            f"  exact length_le_refl {a} {b}",
            ("full2d_rule:inequality_length:01", "full2d_rule:inequality_length:03"),
        )

    if family == "inequality" and "length_le" in source_expr and len(args) == 4:
        trans_hyps = _length_le_trans_hypotheses(claim_spec, args)
        if trans_hyps is not None:
            first_hyp, second_hyp, middle = trans_hyps
            _require_semantic_rule(roles, semantic_rules, "inequality", "full2d_rule:inequality_length:02")
            a, b = (_object_ref_to_name(ref, names) for ref in args[:2])
            c, d = (_object_ref_to_name(ref, names) for ref in middle)
            e, f = (_object_ref_to_name(ref, names) for ref in args[2:])
            return (
                f"  exact length_le_trans {a} {b} {c} {d} {e} {f} {_hypothesis_name(first_hyp)} {_hypothesis_name(second_hyp)}",
                (
                    "full2d_rule:inequality_length:02",
                    "full2d_rule:inequality_length:03",
                    "full2d_rule:inequality_power:01",
                    "full2d_rule:inequality_power:02",
                ),
            )

    if family == "transformation" and "reflection_image" in source_expr and len(args) == 1:
        _require_semantic_rule(roles, semantic_rules, "transformation", "full2d_rule:transformation_reflection:01")
        r = _object_ref_to_name(args[0], names)
        return (
            f"  exact reflection_has_evidence {r}",
            ("full2d_rule:transformation_reflection:01",),
        )

    if family == "transformation" and "rotation_preserves_collinear" in source_expr and len(args) == 6:
        equality_hyps = tuple(_equality_hypothesis(claim_spec, args[index], args[index + 3]) for index in range(3))
        if all(item is not None for item in equality_hyps):
            _require_semantic_rule(roles, semantic_rules, "transformation", "full2d_rule:transformation_rotation:01")
            a, b, c, a1, b1, c1 = (_object_ref_to_name(ref, names) for ref in args)
            ha, hb, hc = (_hypothesis_name(item) for item in equality_hyps if item is not None)
            return (
                f"  exact rotation_preserves_collinear_of_eq {a} {b} {c} {a1} {b1} {c1} {ha} {hb} {hc}",
                ("full2d_rule:transformation_rotation:01", "full2d_rule:transformation_rotation:02"),
            )

    raise ValueError("no_compiler_rule_for_target")


def _with_solver_intermediate_if_substantive(
    *,
    claim_spec: dict[str, Any],
    proof_text: str,
    selected_rule_ids: tuple[str, ...],
) -> str:
    """Expose non-direct solver-backed derivations as an explicit Lean intermediate fact."""
    if not re.fullmatch(r"\s*exact\s+.+\s*", proof_text, flags=re.DOTALL):
        return proof_text
    if _is_direct_facade_collinearity_claim(claim_spec, proof_text, selected_rule_ids):
        return proof_text
    target_expr = _target_source_expr_for_have(claim_spec)
    if not target_expr:
        return proof_text
    exact_body = proof_text.strip()
    return "\n".join(
        (
            f"  have h_solver_intermediate : {target_expr} := by",
            f"    {exact_body}",
            "  exact h_solver_intermediate",
        )
    )


def _is_direct_facade_collinearity_claim(
    claim_spec: dict[str, Any],
    proof_text: str,
    selected_rule_ids: tuple[str, ...],
) -> bool:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return False
    args = tuple(str(arg) for arg in target.get("args", []))
    family = str(target.get("family", ""))
    return (
        family in {"incidence", "collinear"}
        and len(args) == 3
        and args[0] == args[1]
        and "collinear_refl_left" in proof_text
        and set(selected_rule_ids).issubset(
            {
                "full2d_rule:incidence_collinearity:01",
                "full2d_rule:incidence_collinearity:02",
                "full2d_rule:incidence_collinearity:03",
            }
        )
    )


def _target_source_expr_for_have(claim_spec: dict[str, Any]) -> str:
    target = claim_spec.get("target", {})
    if not isinstance(target, dict):
        return ""
    source_expr = str(target.get("source_expr", "")).strip()
    return source_expr


def _available_roles(engine_outputs: dict[str, dict[str, Any]]) -> set[str]:
    return {
        str(payload.get("engine_role"))
        for payload in engine_outputs.values()
        if payload.get("status") == "normalized_success" and payload.get("normalized_output_ref")
    }


def _available_semantic_rules(engine_outputs: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    rules_by_role: dict[str, set[str]] = {}
    for payload in engine_outputs.values():
        if payload.get("status") != "normalized_success" or not payload.get("normalized_output_ref"):
            continue
        role = str(payload.get("engine_role", ""))
        normalized_payload = payload.get("normalized_output_payload")
        if not isinstance(normalized_payload, dict):
            continue
        rules_by_role.setdefault(role, set()).update(_semantic_rule_ids(normalized_payload))
    return rules_by_role


def _semantic_rule_ids(payload: dict[str, Any]) -> set[str]:
    rules: set[str] = set()
    for key in (
        "used_rule_ids",
        "used_rule_refs",
        "admissible_rule_refs",
        "rule_ids",
        "source_rule_ids",
        "coverage_rule_ids",
        "source_rule_id",
        "selected_rule_refs",
    ):
        value = payload.get(key)
        if isinstance(value, str):
            rules.add(value)
        elif isinstance(value, (list, tuple)):
            rules.update(str(item) for item in value)
    for key in ("steps", "cases", "certificates"):
        value = payload.get(key)
        if not isinstance(value, (list, tuple)):
            continue
        for item in value:
            if isinstance(item, dict):
                rules.update(_semantic_rule_ids(item))
    return {rule for rule in rules if rule.startswith("full2d_rule:")}


def _semantic_witnesses_for_rules(
    engine_outputs: dict[str, dict[str, Any]],
    selected_rule_ids: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    role_by_family = {
        "incidence_collinearity": "lean_proof_search",
        "midpoint_segment": "construction_search",
        "construction_line": "construction_search",
        "construction_circle": "construction_search",
        "construction_intersection": "construction_search",
        "construction_center": "construction_search",
        "order_between": "order_case",
        "case_split_orientation": "order_case",
        "directed_angle_mod_pi": "metric_angle",
        "angle_chase": "metric_angle",
        "algebraic_coordinate": "algebraic_geometry",
        "metric_equal_length": "algebraic_geometry",
        "inequality_length": "inequality",
        "inequality_power": "inequality",
        "transformation_reflection": "transformation",
        "transformation_rotation": "transformation",
    }
    required_roles: set[str] = set()
    for rule_id in selected_rule_ids:
        parts = rule_id.split(":")
        if len(parts) >= 3 and parts[1] in role_by_family:
            required_roles.add(role_by_family[parts[1]])
    refs: list[str] = []
    witnesses: list[dict[str, Any]] = []
    witnessed_roles: set[str] = set()
    for engine_ref, payload in sorted(engine_outputs.items()):
        role = str(payload.get("engine_role", ""))
        normalized = payload.get("normalized_output_ref")
        if role not in required_roles:
            continue
        if not _normalized_ref_matches_role(role, normalized):
            continue
        witnessed_roles.add(role)
        witnesses.append(_engine_derivation_witness(engine_ref, payload))
    missing_roles = sorted(required_roles - witnessed_roles)
    if missing_roles:
        raise ValueError(f"compiler_missing_normalized_semantic_witnesses:{','.join(missing_roles)}")
    return tuple(witnesses)


def _engine_derivation_witness(engine_ref: str, payload: dict[str, Any]) -> dict[str, Any]:
    normalized = str(payload.get("normalized_output_ref", ""))
    normalized_payload = payload.get("normalized_output_payload")
    normalized_payload_hash = _sha_text(canonical_json(normalized_payload)) if isinstance(normalized_payload, dict) else ""
    return {
        "engine_output_ref": engine_ref,
        "engine_role": str(payload.get("engine_role", "")),
        "normalized_output_ref": normalized,
        "normalized_artifact_kind": normalized.split(":sha256:", 1)[0] if ":sha256:" in normalized else "",
        "normalized_payload_hash": normalized_payload_hash,
        "semantic_rule_ids": sorted(_semantic_rule_ids(normalized_payload)) if isinstance(normalized_payload, dict) else [],
        "raw_output_hash": str(payload.get("raw_output_hash", "")),
        "checker_or_compiler_ref": str(payload.get("checker_or_compiler_ref", "")),
        "backend_identity": str(payload.get("backend_identity", "")),
    }


def _normalized_ref_matches_role(role: str, normalized: Any) -> bool:
    if not isinstance(normalized, str):
        return False
    expected_prefix = {
        "synthetic_closure": "Full2DTraceV1:",
        "construction_search": "AuxiliaryConstructionFull2D:",
        "algebraic_geometry": "AlgebraicCertificateFull2D:",
        "metric_angle": "MetricAngleTraceFull2D:",
        "transformation": "TransformationTraceFull2D:",
        "order_case": "CoverageGateFull2D:",
        "inequality": "InequalityCertificateFull2D:",
        "lean_proof_search": "LeanProofSearchTraceFull2D:",
        "portfolio_coordinator": "PortfolioDecisionFull2D:",
    }.get(role)
    return bool(expected_prefix and normalized.startswith(expected_prefix) and ":sha256:" in normalized)


def _proof_derivation_ref(
    *,
    claim_spec_ref: str,
    proof_text: str,
    selected_rule_ids: tuple[str, ...],
    proof_derivation_input_refs: tuple[str, ...],
    proof_derivation_witnesses: tuple[dict[str, Any], ...],
) -> str:
    return _sha_text(
        canonical_json(
            {
                "claim_spec_ref": claim_spec_ref,
                "proof_region_replacement_ref": _sha_text(proof_text),
                "proof_derivation_input_refs": list(proof_derivation_input_refs),
                "proof_derivation_witnesses": list(proof_derivation_witnesses),
                "selected_rule_ids": list(selected_rule_ids),
                "derivation_contract": "compiler_output_from_normalized_engine_artifacts_v1",
            }
        )
    )


def _selected_rules_for_role(role: str, selected_rule_ids: tuple[str, ...]) -> tuple[str, ...]:
    family_to_role = {
        "incidence_collinearity": "lean_proof_search",
        "midpoint_segment": "construction_search",
        "construction_line": "construction_search",
        "construction_circle": "construction_search",
        "construction_intersection": "construction_search",
        "construction_center": "construction_search",
        "order_between": "order_case",
        "case_split_orientation": "order_case",
        "directed_angle_mod_pi": "metric_angle",
        "angle_chase": "metric_angle",
        "algebraic_coordinate": "algebraic_geometry",
        "metric_equal_length": "algebraic_geometry",
        "inequality_length": "inequality",
        "inequality_power": "inequality",
        "transformation_reflection": "transformation",
        "transformation_rotation": "transformation",
    }
    matched: list[str] = []
    for rule_id in selected_rule_ids:
        parts = rule_id.split(":")
        if len(parts) < 3:
            continue
        if family_to_role.get(parts[1]) == role:
            matched.append(rule_id)
    return tuple(dict.fromkeys(matched))


def _require_role(roles: set[str], role: str) -> None:
    if role not in roles:
        raise ValueError(f"{role}_engine_output_required_for_patch")


def _require_semantic_rule(
    roles: set[str],
    semantic_rules: dict[str, set[str]],
    role: str,
    rule_id: str,
) -> None:
    _require_role(roles, role)
    if rule_id not in semantic_rules.get(role, set()):
        raise ValueError(f"{role}_normalized_payload_missing_semantic_rule:{rule_id}")


def _source_expr(item: dict[str, Any]) -> str:
    return str(item.get("source_expr", "")).lower()


def _hypothesis_for(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        if token not in _source_expr(item):
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == args:
            return item
    return None


def _hypothesis_for_args(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        if token not in _source_expr(item):
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == args:
            return item
    return None


def _length_le_trans_hypotheses(
    claim_spec: dict[str, Any],
    target_args: tuple[str, ...],
) -> tuple[dict[str, Any], dict[str, Any], tuple[str, str]] | None:
    length_hyps = [
        item
        for item in claim_spec.get("hypotheses", ())
        if isinstance(item, dict)
        and "length_le" in _source_expr(item)
        and len(tuple(item.get("args", ()))) == 4
    ]
    for first in length_hyps:
        first_args = tuple(str(arg) for arg in first.get("args", ()))
        if first_args[:2] != target_args[:2]:
            continue
        for second in length_hyps:
            second_args = tuple(str(arg) for arg in second.get("args", ()))
            if first_args[2:] == second_args[:2] and second_args[2:] == target_args[2:]:
                return first, second, first_args[2:]
    return None


def _equality_hypothesis(claim_spec: dict[str, Any], left: str, right: str) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        source_expr = str(item.get("source_expr", ""))
        if "=" not in source_expr or "!=" in source_expr or "≠" in source_expr:
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == (left, right):
            return item
    return None


def _hypothesis_name(hypothesis: dict[str, Any]) -> str:
    predicate_id = str(hypothesis.get("predicate_id", "hyp:h"))
    return predicate_id.rsplit(":", 1)[-1]


def _object_ref_to_name(ref: str, names: dict[str, str]) -> str:
    return names.get(ref, _last_ref_part(ref))


def _generated_obligations(claim_spec: dict[str, Any], role: str) -> list[str]:
    side_conditions = claim_spec.get("side_conditions", {})
    values: list[str] = []
    if isinstance(side_conditions, dict):
        for bucket in side_conditions.values():
            if isinstance(bucket, (list, tuple)):
                values.extend(f"obligation:{item}" for item in bucket)
    if role == "construction_search" and not values:
        values.append("obligation:construction_domain")
    return values


def _side_condition_report_ref(claim_spec: dict[str, Any]) -> str:
    payload = {
        "schema_version": "1.0.0",
        "theorem_name": claim_spec.get("theorem_name"),
        "side_conditions": claim_spec.get("side_conditions", {}),
    }
    return _sha_text(canonical_json(payload))


def _object_names(claim_spec: dict[str, Any]) -> dict[str, str]:
    names: dict[str, str] = {}
    for item in claim_spec.get("objects", ()):
        if isinstance(item, dict) and item.get("object_id") and item.get("canonical_name"):
            names[str(item["object_id"])] = str(item["canonical_name"])
    return names


def _last_ref_part(value: str) -> str:
    return value.rsplit(":", 1)[-1]


def _tupled_compiler_payload(payload: dict[str, Any]) -> dict[str, Any]:
    data = dict(payload)
    for key in (
        "consumed_engine_output_refs",
        "input_engine_output_refs",
        "consumed_normalized_output_refs",
        "proof_derivation_input_refs",
        "consumed_rule_ids",
        "used_rule_ids",
        "used_rule_refs",
        "generated_obligations",
    ):
        data[key] = tuple(str(item) for item in data.get(key, ()))
    data["proof_derivation_witnesses"] = _as_witness_tuple(data.get("proof_derivation_witnesses"))
    return data


def _tupled_patch_payload(payload: dict[str, Any]) -> dict[str, Any]:
    data = dict(payload)
    for key in (
        "source_compiler_result_refs",
        "compiler_result_refs",
        "source_engine_output_refs",
        "source_rule_ids",
        "used_rule_ids",
        "used_rule_refs",
        "solver_dependency_refs",
        "proof_derivation_input_refs",
    ):
        data[key] = tuple(str(item) for item in data.get(key, ()))
    data["proof_derivation_witnesses"] = _as_witness_tuple(data.get("proof_derivation_witnesses"))
    data["allowed_edit_region"] = dict(data["allowed_edit_region"])
    return data


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return ()


def _as_witness_tuple(value: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    witnesses: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, dict):
            witnesses.append({str(key): item[key] for key in item})
    return tuple(witnesses)


def _validate_derivation_witnesses(
    witnesses: tuple[dict[str, Any], ...],
    *,
    consumed_engine_refs: tuple[str, ...],
    normalized_refs: tuple[str, ...],
    derivation_inputs: tuple[str, ...],
    mode: str,
) -> list[str]:
    errors: list[str] = []
    consumed_set = set(consumed_engine_refs)
    normalized_set = set(normalized_refs)
    input_set = set(derivation_inputs)
    for witness in witnesses:
        if mode == "direct":
            if witness.get("derivation_status") != "direct_lean_baseline" or not witness.get("claim_spec_ref"):
                errors.append("derivation_witness_direct_mode_invalid")
            continue
        engine_ref = witness.get("engine_output_ref")
        if not isinstance(engine_ref, str) or engine_ref not in consumed_set:
            errors.append("derivation_witness_engine_ref_not_consumed")
        if mode == "measured_failure":
            if witness.get("derivation_status") != "measured_failure":
                errors.append("derivation_witness_measured_failure_status_missing")
            continue
        role = str(witness.get("engine_role", ""))
        normalized = witness.get("normalized_output_ref")
        raw_hash = witness.get("raw_output_hash")
        checker = witness.get("checker_or_compiler_ref")
        payload_hash = witness.get("normalized_payload_hash")
        semantic_rules = witness.get("semantic_rule_ids")
        if role not in ENGINE_ROLES:
            errors.append("derivation_witness_unknown_engine_role")
        if not _normalized_ref_matches_role(role, normalized):
            errors.append(f"derivation_witness_normalized_ref_mismatch:{role}")
        elif str(normalized) not in normalized_set or str(normalized) not in input_set:
            errors.append("derivation_witness_normalized_ref_not_consumed")
        if not isinstance(raw_hash, str) or not raw_hash.startswith("sha256:"):
            errors.append("derivation_witness_missing_raw_output_hash")
        if not isinstance(payload_hash, str) or not payload_hash.startswith("sha256:"):
            errors.append("derivation_witness_missing_normalized_payload_hash")
        if not isinstance(semantic_rules, list) or not any(str(rule).startswith("full2d_rule:") for rule in semantic_rules):
            errors.append("derivation_witness_missing_semantic_rule_ids")
        if not isinstance(checker, str) or not checker:
            errors.append("derivation_witness_missing_checker_ref")
    return sorted(set(errors))


def _has_benchmark_label_source(payload: dict[str, Any]) -> bool:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return any(token in encoded for token in ("benchmark_label", "legacy_template_key", "family_label_dispatch"))


def _write_typed_json(
    root: Path,
    name: str,
    prefix: str,
    id_field: str,
    payload_without_identity: dict[str, Any],
    artifact_paths: dict[str, str],
) -> tuple[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    ref = content_addressed_typed_ref(prefix, payload_without_identity)
    payload = {id_field: ref, "content_sha256": _sha_from_typed_ref(ref), **payload_without_identity}
    if prefix == "CompilerResultFull2D":
        payload.setdefault("compiler_result_ref", ref)
    path = root / f"{name}.{_sha_from_typed_ref(ref)[7:23]}.json"
    path.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    artifact_paths[ref] = str(path)
    return ref, path


def _write_sha_text(root: Path, name: str, text: str, artifact_paths: dict[str, str]) -> str:
    root.mkdir(parents=True, exist_ok=True)
    ref = _sha_text(text)
    path = root / f"{name}.{ref[7:23]}.lean.txt"
    path.write_text(text, encoding="utf-8")
    artifact_paths[ref] = str(path)
    return ref


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    identity_fields = {
        "compiler_result_ref",
        "result_id",
        "patch_id",
        "content_sha256",
        "payload_sha256",
        "artifact_sha256",
    }
    return {key: value for key, value in payload.items() if key not in identity_fields}


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _sha_from_typed_ref(ref: str) -> str:
    return "sha256:" + ref.rsplit("sha256:", 1)[1]
