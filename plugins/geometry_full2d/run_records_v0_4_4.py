from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TYPED_SHA_RE = re.compile(r"^[A-Za-z0-9_:.+-]+:sha256:[0-9a-f]{64}$")

SCHEMA_VERSION = "ActualTaskPipelineRunV2"

REQUIRED_FIELDS = (
    "schema_version",
    "run_id",
    "task_id",
    "baseline_id",
    "corpus_manifest_hash",
    "config_hash",
    "repo_tree_hash",
    "selected_implementation_hash",
    "source_theorem_ref",
    "source_theorem_path",
    "source_theorem_preproved",
    "lean_extraction_report_ref",
    "claim_spec_ref",
    "provider_run_manifest_ref",
    "engine_output_refs",
    "compiler_result_refs",
    "lean_patch_candidate_ref",
    "proof_worker_result_ref",
    "generated_candidate_file_ref",
    "final_verify_report_ref",
    "solver_causality_report_ref",
    "solver_backed_certificate_ref",
    "causal_chain_hash",
    "final_status",
    "artifact_paths",
)

JSON_ID_FIELDS = (
    "report_id",
    "claim_id",
    "manifest_id",
    "output_id",
    "result_id",
    "patch_id",
    "worker_result_id",
    "certificate_id",
)

IDENTITY_FIELDS = frozenset(
    {
        *JSON_ID_FIELDS,
        "content_sha256",
        "payload_sha256",
        "artifact_sha256",
        "causal_chain_hash",
    }
)


def validate_actual_task_pipeline_run_v2(payload: dict[str, Any], *, run_dir: Path | None = None) -> list[str]:
    errors = validate_structure(payload)
    if errors:
        return errors
    artifact_paths = {str(key): str(value) for key, value in payload["artifact_paths"].items()}
    refs = ordered_artifact_refs(payload)

    source_path = _resolve_path(str(payload["source_theorem_path"]), run_dir)
    if not source_path.exists():
        errors.append(f"{payload['run_id']}:missing_source_theorem_file:{source_path}")
    elif _sha_file(source_path) != payload["source_theorem_ref"]:
        errors.append(f"{payload['run_id']}:source_theorem_ref_hash_mismatch")

    loaded: dict[str, dict[str, Any]] = {}
    for ref in refs:
        path_value = artifact_paths.get(ref)
        if path_value is None:
            errors.append(f"{payload['run_id']}:missing_artifact_path:{ref}")
            continue
        path = _resolve_path(path_value, run_dir)
        if not path.exists():
            errors.append(f"{payload['run_id']}:missing_artifact_file:{ref}:{path}")
            continue
        errors.extend(_validate_artifact_ref(ref, path, str(payload["run_id"])))
        if _is_typed_ref(ref):
            try:
                artifact = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"{payload['run_id']}:artifact_json_error:{ref}:{exc}")
                continue
            if not isinstance(artifact, dict):
                errors.append(f"{payload['run_id']}:artifact_not_object:{ref}")
                continue
            loaded[ref] = artifact
            if ref not in [artifact.get(field) for field in JSON_ID_FIELDS]:
                errors.append(f"{payload['run_id']}:artifact_identity_mismatch:{ref}")

    errors.extend(_binding_errors(payload, loaded))
    expected_chain = compute_causal_chain_hash_v2(payload)
    if payload.get("causal_chain_hash") != expected_chain:
        errors.append(f"{payload['run_id']}:causal_chain_hash_mismatch")
    if payload.get("legacy_schema_version") or payload.get("schema_version") == "1.0.0":
        errors.append(f"{payload['run_id']}:old_run_record_schema_detected")
    return sorted(set(errors))


def validate_structure(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["run_record_not_object"]
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version_not_ActualTaskPipelineRunV2")
    if not isinstance(payload.get("run_id"), str) or ":v0_4_4:" not in payload["run_id"]:
        errors.append("run_id_not_v0_4_4")
    for key in (
        "corpus_manifest_hash",
        "config_hash",
        "repo_tree_hash",
        "selected_implementation_hash",
        "source_theorem_ref",
        "generated_candidate_file_ref",
        "causal_chain_hash",
    ):
        if not _is_sha(payload.get(key)):
            errors.append(f"{key}_not_sha256")
    for key in (
        "lean_extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
        "solver_causality_report_ref",
        "solver_backed_certificate_ref",
    ):
        if not _is_typed_ref(payload.get(key)):
            errors.append(f"{key}_not_typed_sha_ref")
    for key in ("engine_output_refs", "compiler_result_refs"):
        value = payload.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"{key}_missing_or_empty")
        elif any(not _is_typed_ref(item) for item in value):
            errors.append(f"{key}_contains_invalid_ref")
    if payload.get("source_theorem_preproved") not in {True, False}:
        errors.append("source_theorem_preproved_not_boolean")
    if payload.get("final_status") not in {"final_theorem", "measured_failure"}:
        errors.append("final_status_invalid")
    if not isinstance(payload.get("artifact_paths"), dict):
        errors.append("artifact_paths_not_object")
    return sorted(set(errors))


def ordered_artifact_refs(payload: dict[str, Any]) -> list[str]:
    return [
        str(payload["lean_extraction_report_ref"]),
        str(payload["claim_spec_ref"]),
        str(payload["provider_run_manifest_ref"]),
        *[str(ref) for ref in payload["engine_output_refs"]],
        *[str(ref) for ref in payload["compiler_result_refs"]],
        str(payload["lean_patch_candidate_ref"]),
        str(payload["proof_worker_result_ref"]),
        str(payload["generated_candidate_file_ref"]),
        str(payload["final_verify_report_ref"]),
        str(payload["solver_causality_report_ref"]),
        str(payload["solver_backed_certificate_ref"]),
    ]


def compute_causal_chain_hash_v2(payload: dict[str, Any]) -> str:
    chain = {
        "schema": "ActualTaskPipelineRunV2.causal_chain_hash",
        "corpus_manifest_hash": payload["corpus_manifest_hash"],
        "config_hash": payload["config_hash"],
        "repo_tree_hash": payload["repo_tree_hash"],
        "selected_implementation_hash": payload["selected_implementation_hash"],
        "refs": ordered_artifact_refs(payload),
    }
    return _sha_text(_canonical_json(chain))


def typed_ref(prefix: str, payload_without_identity: dict[str, Any]) -> str:
    return f"{prefix}:{_payload_hash(payload_without_identity)}"


def _binding_errors(record: dict[str, Any], loaded: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    run_id = str(record["run_id"])
    extraction = loaded.get(str(record["lean_extraction_report_ref"]))
    claim = loaded.get(str(record["claim_spec_ref"]))
    provider = loaded.get(str(record["provider_run_manifest_ref"]))
    causality = loaded.get(str(record["solver_causality_report_ref"]))
    final_verify = loaded.get(str(record["final_verify_report_ref"]))
    certificate = loaded.get(str(record["solver_backed_certificate_ref"]))

    if extraction:
        if extraction.get("task_id") != record["task_id"]:
            errors.append(f"{run_id}:extraction_task_id_mismatch")
        if extraction.get("semantic_extraction_authority") != "lean_elaborator":
            errors.append(f"{run_id}:extraction_not_lean_elaborator")
        if extraction.get("python_semantic_extraction_used") is not False:
            errors.append(f"{run_id}:extraction_python_semantics_used")
    if claim:
        if claim.get("task_id") != record["task_id"]:
            errors.append(f"{run_id}:claim_task_id_mismatch")
        if claim.get("created_from") != "GeometryFull2DExtractionReportV2":
            errors.append(f"{run_id}:claim_not_extraction_derived")
        if claim.get("manifest_label_input_used") is not False:
            errors.append(f"{run_id}:claim_manifest_label_input_used")
    if provider:
        if provider.get("claim_spec_ref") != record["claim_spec_ref"]:
            errors.append(f"{run_id}:provider_claim_ref_mismatch")
        if provider.get("schema_version") != "ProviderRunManifestV2":
            errors.append(f"{run_id}:provider_not_v2")
    if causality:
        if causality.get("schema_version") != "SolverCausalityReportV1":
            errors.append(f"{run_id}:causality_schema_mismatch")
        if causality.get("claim_spec_ref") != record["claim_spec_ref"]:
            errors.append(f"{run_id}:causality_claim_ref_mismatch")
        if causality.get("provider_run_manifest_ref") != record["provider_run_manifest_ref"]:
            errors.append(f"{run_id}:causality_provider_ref_mismatch")
        if causality.get("compiler_result_refs") != record["compiler_result_refs"]:
            errors.append(f"{run_id}:causality_compiler_refs_mismatch")
        if record["final_status"] == "final_theorem" and causality.get("solver_causal_necessity") is not True:
            errors.append(f"{run_id}:final_success_without_solver_causal_necessity")
    if final_verify:
        if final_verify.get("solver_causality_report_ref") != record["solver_causality_report_ref"]:
            errors.append(f"{run_id}:final_verify_causality_ref_mismatch")
        if record["final_status"] == "final_theorem" and final_verify.get("status") != "passed":
            errors.append(f"{run_id}:final_verify_not_passed")
    if certificate:
        for key in (
            "lean_extraction_report_ref",
            "claim_spec_ref",
            "provider_run_manifest_ref",
            "solver_causality_report_ref",
            "final_verify_report_ref",
        ):
            if certificate.get(key) != record[key]:
                errors.append(f"{run_id}:certificate_{key}_mismatch")
    return errors


def _validate_artifact_ref(ref: str, path: Path, label: str) -> list[str]:
    if _is_sha(ref):
        return [] if _sha_file(path) == ref else [f"{label}:artifact_sha256_mismatch:{ref}"]
    if not _is_typed_ref(ref):
        return [f"{label}:artifact_ref_invalid:{ref}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{label}:typed_artifact_json_error:{ref}:{exc}"]
    if not isinstance(payload, dict):
        return [f"{label}:typed_artifact_not_object:{ref}"]
    expected = ref.rsplit(":", 2)[-2] + ":" + ref.rsplit(":", 1)[-1]
    candidates = {
        str(payload.get("content_sha256")),
        str(payload.get("payload_sha256")),
        str(payload.get("artifact_sha256")),
        _payload_hash(payload),
    }
    return [] if expected in candidates else [f"{label}:typed_artifact_hash_mismatch:{ref}"]


def _resolve_path(value: str, run_dir: Path | None) -> Path:
    path = Path(value)
    if path.is_absolute() or run_dir is None:
        return path
    return run_dir / path


def _payload_hash(payload: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in payload.items() if key not in IDENTITY_FIELDS}
    return _sha_text(_canonical_json(unsigned))


def _is_sha(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _is_typed_ref(value: Any) -> bool:
    return isinstance(value, str) and TYPED_SHA_RE.fullmatch(value) is not None


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
