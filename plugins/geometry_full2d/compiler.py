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
    side_condition_report_ref = _side_condition_report_ref(claim_spec)
    compiler_results: list[CompilerResultFull2D] = []
    compiler_refs: list[str] = []
    for engine_ref, engine_payload in sorted(usable.items()):
        role = str(engine_payload.get("engine_role", ""))
        if role not in ENGINE_ROLES:
            continue
        role_rules = RULES_BY_ROLE[role]
        payload = {
            "schema_version": "1.0.0",
            "compiler_id": COMPILER_BY_ROLE[role],
            "task_id": task_id,
            "claim_spec_ref": claim_spec_ref,
            "provider_run_manifest_ref": provider_run_manifest_ref,
            "consumed_engine_output_refs": [engine_ref],
            "input_engine_output_refs": [engine_ref],
            "consumed_normalized_output_refs": [str(engine_payload["normalized_output_ref"])],
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
    args = [str(arg) for arg in target.get("args", [])]
    if str(target.get("family")) not in {"incidence", "collinear"} or len(args) != 3 or args[0] != args[1]:
        raise ValueError("no_compiler_rule_for_target")
    if not any(payload.get("engine_role") == "lean_proof_search" for payload in engine_outputs.values()):
        raise ValueError("lean_proof_search_engine_output_required_for_patch")
    names = _object_names(claim_spec)
    left = names.get(args[0], _last_ref_part(args[0]))
    right = names.get(args[2], _last_ref_part(args[2]))
    return (f"  exact collinear_refl_left {left} {right}", ("full2d_rule:incidence_collinearity:02",))


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
        "consumed_rule_ids",
        "used_rule_ids",
        "used_rule_refs",
        "generated_obligations",
    ):
        data[key] = tuple(str(item) for item in data.get(key, ()))
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
    ):
        data[key] = tuple(str(item) for item in data.get(key, ()))
    data["allowed_edit_region"] = dict(data["allowed_edit_region"])
    return data


def _as_str_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return ()


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
