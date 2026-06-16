from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TYPED_SHA_RE = re.compile(r"^[A-Za-z0-9_:.+-]+:sha256:[0-9a-f]{64}$")

ACTUAL_TASK_PIPELINE_RUN_SCHEMA_VERSION = "1.0.0"
ACTUAL_TASK_PIPELINE_REQUIRED_FIELDS: tuple[str, ...] = (
    "schema_version",
    "run_id",
    "task_id",
    "baseline_id",
    "frozen_corpus_manifest_hash",
    "config_hash",
    "selected_implementations_hash",
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
    "solver_backed_certificate_ref",
    "causal_chain_hash",
    "final_status",
    "artifact_paths",
)

JSON_ID_FIELDS: tuple[str, ...] = (
    "report_id",
    "claim_id",
    "manifest_id",
    "output_id",
    "result_id",
    "patch_id",
    "worker_result_id",
    "certificate_id",
)

HASH_ID_FIELDS: frozenset[str] = frozenset(
    {
        *JSON_ID_FIELDS,
        "content_sha256",
        "payload_sha256",
        "artifact_sha256",
        "causal_chain_hash",
    }
)


@dataclass(frozen=True)
class ActualTaskPipelineRunV1:
    schema_version: str
    run_id: str
    task_id: str
    baseline_id: str
    frozen_corpus_manifest_hash: str
    config_hash: str
    selected_implementations_hash: str
    source_theorem_ref: str
    source_theorem_path: str
    source_theorem_preproved: bool
    lean_extraction_report_ref: str
    claim_spec_ref: str
    provider_run_manifest_ref: str
    engine_output_refs: tuple[str, ...]
    compiler_result_refs: tuple[str, ...]
    lean_patch_candidate_ref: str
    proof_worker_result_ref: str
    generated_candidate_file_ref: str
    final_verify_report_ref: str
    solver_backed_certificate_ref: str
    causal_chain_hash: str
    final_status: str
    artifact_paths: dict[str, str]
    failure_reason: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ActualTaskPipelineRunV1":
        errors = validate_actual_task_pipeline_run_structure(payload)
        if errors:
            raise ValueError(";".join(errors))
        admitted = {field.name for field in fields(cls)}
        data = {key: value for key, value in payload.items() if key in admitted}
        data["engine_output_refs"] = tuple(str(ref) for ref in data["engine_output_refs"])
        data["compiler_result_refs"] = tuple(str(ref) for ref in data["compiler_result_refs"])
        data["artifact_paths"] = {str(key): str(value) for key, value in data["artifact_paths"].items()}
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["engine_output_refs"] = list(self.engine_output_refs)
        payload["compiler_result_refs"] = list(self.compiler_result_refs)
        return payload


def validate_actual_task_pipeline_run_structure(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["run_record_not_object"]
    missing = [field for field in ACTUAL_TASK_PIPELINE_REQUIRED_FIELDS if field not in payload]
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if payload.get("schema_version") != ACTUAL_TASK_PIPELINE_RUN_SCHEMA_VERSION:
        errors.append("schema_version_mismatch")
    if not isinstance(payload.get("run_id"), str) or not payload["run_id"].startswith("actual_full2d_run:"):
        errors.append("run_id_prefix_mismatch")
    for key in ("task_id", "baseline_id", "source_theorem_path", "final_status"):
        if not isinstance(payload.get(key), str) or not payload[key]:
            errors.append(f"{key}_missing_or_not_string")
    for key in ("frozen_corpus_manifest_hash", "config_hash", "selected_implementations_hash", "source_theorem_ref", "generated_candidate_file_ref", "causal_chain_hash"):
        if not _is_sha256(payload.get(key)):
            errors.append(f"{key}_not_sha256")
    typed_ref_keys = (
        "lean_extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
        "solver_backed_certificate_ref",
    )
    for key in typed_ref_keys:
        if not _is_typed_sha_ref(payload.get(key)):
            errors.append(f"{key}_not_typed_sha_ref")
    if payload.get("source_theorem_preproved") not in {True, False}:
        errors.append("source_theorem_preproved_not_boolean")
    if payload.get("final_status") not in {"final_theorem", "measured_failure"}:
        errors.append("final_status_invalid")
    for key in ("engine_output_refs", "compiler_result_refs"):
        refs = payload.get(key)
        if not isinstance(refs, list) or not refs:
            errors.append(f"{key}_missing_or_empty")
        elif any(not _is_typed_sha_ref(ref) for ref in refs):
            errors.append(f"{key}_contains_invalid_ref")
    if not isinstance(payload.get("artifact_paths"), dict):
        errors.append("artifact_paths_not_object")
    return sorted(set(errors))


def validate_actual_task_pipeline_run(
    payload: dict[str, Any],
    *,
    run_dir: Path | None = None,
    require_causal_chain_recompute: bool = True,
) -> list[str]:
    errors = validate_actual_task_pipeline_run_structure(payload)
    if errors:
        return errors

    record = ActualTaskPipelineRunV1.from_dict(payload)
    label = record.run_id
    loaded: dict[str, dict[str, Any]] = {}
    referenced_refs = _ordered_artifact_refs(record)

    source_path = _resolve_path(record.source_theorem_path, run_dir)
    if not source_path.exists():
        errors.append(f"{label}:missing_source_theorem_file:{source_path}")
    elif _hash_bytes(source_path.read_bytes()) != record.source_theorem_ref:
        errors.append(f"{label}:source_theorem_ref_hash_mismatch")

    for ref in referenced_refs:
        path = _path_for_ref(record, ref, run_dir)
        if path is None:
            errors.append(f"{label}:missing_artifact_path:{ref}")
            continue
        if not path.exists():
            errors.append(f"{label}:missing_artifact_file:{ref}:{path}")
            continue
        errors.extend(_validate_artifact_content_ref(ref, path, label))
        if not _is_sha256(ref):
            payload_for_ref = _read_json(path, errors, label, ref)
            if payload_for_ref is not None:
                loaded[ref] = payload_for_ref
                _validate_artifact_identity(ref, payload_for_ref, errors, label)

    if record.final_status == "final_theorem" and record.source_theorem_preproved:
        errors.append(f"{label}:source_theorem_already_preproved")

    _validate_extraction_binding(record, loaded.get(record.lean_extraction_report_ref), source_path, errors)
    _validate_provider_binding(record, loaded.get(record.provider_run_manifest_ref), errors)
    _validate_engine_output_bindings(record, loaded, errors)
    _validate_compiler_binding(record, loaded, errors)
    _validate_patch_binding(record, loaded.get(record.lean_patch_candidate_ref), errors)
    _validate_worker_binding(record, loaded.get(record.proof_worker_result_ref), errors)
    _validate_final_verify_binding(record, loaded.get(record.final_verify_report_ref), errors)
    _validate_certificate_binding(record, loaded.get(record.solver_backed_certificate_ref), errors)

    if require_causal_chain_recompute:
        expected_chain_hash = compute_causal_chain_hash(record.to_dict())
        if record.causal_chain_hash != expected_chain_hash:
            errors.append(f"{label}:causal_chain_hash_mismatch")
    return sorted(set(errors))


def compute_causal_chain_hash(payload: dict[str, Any]) -> str:
    refs = [
        str(payload["source_theorem_ref"]),
        str(payload["lean_extraction_report_ref"]),
        str(payload["claim_spec_ref"]),
        str(payload["provider_run_manifest_ref"]),
        *[str(ref) for ref in payload["engine_output_refs"]],
        *[str(ref) for ref in payload["compiler_result_refs"]],
        str(payload["lean_patch_candidate_ref"]),
        str(payload["proof_worker_result_ref"]),
        str(payload["final_verify_report_ref"]),
        str(payload["solver_backed_certificate_ref"]),
    ]
    return _hash_text(_canonical_json({"chain": refs, "schema": "ActualTaskPipelineRunV1.causal_chain_hash"}))


def content_addressed_typed_ref(prefix: str, payload_without_identity: dict[str, Any]) -> str:
    return f"{prefix}:{_payload_content_hash(payload_without_identity)}"


def _ordered_artifact_refs(record: ActualTaskPipelineRunV1) -> list[str]:
    return [
        record.lean_extraction_report_ref,
        record.claim_spec_ref,
        record.provider_run_manifest_ref,
        *record.engine_output_refs,
        *record.compiler_result_refs,
        record.lean_patch_candidate_ref,
        record.proof_worker_result_ref,
        record.generated_candidate_file_ref,
        record.final_verify_report_ref,
        record.solver_backed_certificate_ref,
    ]


def _validate_extraction_binding(
    record: ActualTaskPipelineRunV1,
    extraction: dict[str, Any] | None,
    source_path: Path,
    errors: list[str],
) -> None:
    if extraction is None:
        return
    label = record.run_id
    if extraction.get("source_theorem_ref") != record.source_theorem_ref:
        errors.append(f"{label}:extraction_source_theorem_ref_mismatch")
    extraction_path = extraction.get("source_theorem_path")
    if not isinstance(extraction_path, str) or not extraction_path:
        errors.append(f"{label}:extraction_missing_source_theorem_path")
    elif _normalize_path(_resolve_path(extraction_path, source_path.parent)) != _normalize_path(source_path):
        errors.append(f"{label}:extraction_source_theorem_path_mismatch")
    if extraction.get("source_theorem_preproved") is True:
        errors.append(f"{label}:extraction_source_theorem_already_preproved")
    if extraction.get("extraction_method") != "lean_elaborator_structured_theorem":
        errors.append(f"{label}:extraction_method_not_lean_elaborator_structured")
    if extraction.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append(f"{label}:extraction_semantic_authority_not_lean")
    if extraction.get("python_semantic_extraction_used") is not False:
        errors.append(f"{label}:extraction_python_semantic_used")


def _validate_provider_binding(
    record: ActualTaskPipelineRunV1,
    provider: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if provider is None:
        return
    label = record.run_id
    if provider.get("task_id") != record.task_id:
        errors.append(f"{label}:provider_task_id_mismatch")
    if provider.get("baseline_id") != record.baseline_id:
        errors.append(f"{label}:provider_baseline_id_mismatch")
    if provider.get("claim_spec_ref") != record.claim_spec_ref:
        errors.append(f"{label}:provider_claim_spec_ref_mismatch")
    provider_engine_refs = _as_ref_set(provider, "engine_output_refs", "engine_record_refs")
    missing = sorted(set(record.engine_output_refs) - provider_engine_refs)
    if missing:
        errors.append(f"{label}:provider_missing_engine_output_refs:{','.join(missing)}")


def _validate_engine_output_bindings(
    record: ActualTaskPipelineRunV1,
    loaded: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    label = record.run_id
    for engine_ref in record.engine_output_refs:
        engine = loaded.get(engine_ref)
        if engine is None:
            continue
        if engine.get("status") == "normalized_success":
            if not isinstance(engine.get("normalized_output_payload"), dict):
                errors.append(f"{label}:engine_normalized_success_missing_payload:{engine_ref}")
            if not isinstance(engine.get("normalized_output_ref"), str):
                errors.append(f"{label}:engine_normalized_success_missing_ref:{engine_ref}")
        if engine.get("proof_use_status") != "not_allowed":
            errors.append(f"{label}:engine_proof_use_status_not_allowed:{engine_ref}")


def _validate_compiler_binding(
    record: ActualTaskPipelineRunV1,
    loaded: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    label = record.run_id
    engine_refs = set(record.engine_output_refs)
    for compiler_ref in record.compiler_result_refs:
        compiler = loaded.get(compiler_ref)
        if compiler is None:
            continue
        consumed = _as_ref_set(compiler, "input_engine_output_refs", "engine_output_refs", "normalized_solver_artifact_refs")
        if not consumed.intersection(engine_refs):
            errors.append(f"{label}:compiler_did_not_consume_engine_output:{compiler_ref}")
        provider_ref = compiler.get("provider_run_manifest_ref")
        if provider_ref != record.provider_run_manifest_ref:
            errors.append(f"{label}:compiler_provider_manifest_ref_mismatch:{compiler_ref}")
        claim_ref = compiler.get("claim_spec_ref")
        if claim_ref != record.claim_spec_ref:
            errors.append(f"{label}:compiler_claim_spec_ref_mismatch:{compiler_ref}")


def _validate_patch_binding(
    record: ActualTaskPipelineRunV1,
    patch: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if patch is None:
        return
    label = record.run_id
    patch_compiler_refs = _as_ref_set(patch, "compiler_result_refs", "source_compiler_result_refs")
    single_compiler_ref = patch.get("source_compiler_result_ref")
    if isinstance(single_compiler_ref, str):
        patch_compiler_refs.add(single_compiler_ref)
    if not patch_compiler_refs.intersection(record.compiler_result_refs):
        errors.append(f"{label}:patch_missing_compiler_result_ref")
    if patch.get("provider_run_manifest_ref") != record.provider_run_manifest_ref:
        errors.append(f"{label}:patch_provider_manifest_ref_mismatch")


def _validate_worker_binding(
    record: ActualTaskPipelineRunV1,
    worker: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if worker is None:
        return
    label = record.run_id
    if worker.get("lean_patch_candidate_ref") != record.lean_patch_candidate_ref:
        errors.append(f"{label}:worker_patch_ref_mismatch")
    if worker.get("generated_candidate_file_ref") != record.generated_candidate_file_ref:
        errors.append(f"{label}:worker_generated_candidate_ref_mismatch")
    if record.final_status == "final_theorem" and worker.get("patch_applied") is not True:
        errors.append(f"{label}:worker_patch_not_applied")


def _validate_final_verify_binding(
    record: ActualTaskPipelineRunV1,
    final_verify: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if final_verify is None:
        return
    label = record.run_id
    if final_verify.get("checked_candidate_file_ref") != record.generated_candidate_file_ref:
        errors.append(f"{label}:final_verify_candidate_ref_mismatch")
    if record.final_status == "final_theorem":
        status_values = {
            final_verify.get("status"),
            final_verify.get("proof_use_status"),
            final_verify.get("final_status"),
            final_verify.get("final_verify_status"),
        }
        if not ({"passed", "final_theorem"} & {str(value) for value in status_values if value is not None}):
            errors.append(f"{label}:final_verify_not_passed")


def _validate_certificate_binding(
    record: ActualTaskPipelineRunV1,
    certificate: dict[str, Any] | None,
    errors: list[str],
) -> None:
    if certificate is None:
        return
    label = record.run_id
    scalar_bindings = {
        "lean_extraction_report_ref": record.lean_extraction_report_ref,
        "claim_spec_ref": record.claim_spec_ref,
        "provider_run_manifest_ref": record.provider_run_manifest_ref,
        "lean_patch_candidate_ref": record.lean_patch_candidate_ref,
        "proof_worker_result_ref": record.proof_worker_result_ref,
        "generated_candidate_file_ref": record.generated_candidate_file_ref,
        "final_verify_report_ref": record.final_verify_report_ref,
        "source_theorem_ref": record.source_theorem_ref,
    }
    aliases = {
        "proof_worker_result_ref": ("worker_result_ref",),
        "final_verify_report_ref": ("final_verify_ref",),
        "source_theorem_ref": ("source_statement_hash",),
    }
    for key, expected in scalar_bindings.items():
        values = [certificate.get(key), *[certificate.get(alias) for alias in aliases.get(key, ())]]
        if expected not in values:
            errors.append(f"{label}:certificate_{key}_mismatch")
    if set(certificate.get("engine_output_refs", ())) != set(record.engine_output_refs):
        errors.append(f"{label}:certificate_engine_output_refs_mismatch")
    if set(certificate.get("compiler_result_refs", ())) != set(record.compiler_result_refs):
        errors.append(f"{label}:certificate_compiler_result_refs_mismatch")
    if record.final_status == "final_theorem":
        if certificate.get("status") not in {"passed", "final_theorem"}:
            errors.append(f"{label}:certificate_status_not_passed")
        if certificate.get("final_status") not in {None, "final_theorem"}:
            errors.append(f"{label}:certificate_final_status_mismatch")


def _validate_artifact_identity(ref: str, payload: dict[str, Any], errors: list[str], label: str) -> None:
    values = [payload.get(field) for field in JSON_ID_FIELDS]
    if ref not in values:
        errors.append(f"{label}:artifact_identity_mismatch:{ref}")


def _validate_artifact_content_ref(ref: str, path: Path, label: str) -> list[str]:
    errors: list[str] = []
    if _is_sha256(ref):
        if _hash_bytes(path.read_bytes()) != ref:
            errors.append(f"{label}:artifact_sha256_mismatch:{ref}:{path}")
        return errors
    if not _is_typed_sha_ref(ref):
        errors.append(f"{label}:artifact_ref_not_sha256_addressed:{ref}")
        return errors
    expected = ref.rsplit(":", 2)[-2] + ":" + ref.rsplit(":", 1)[-1]
    if _hash_bytes(path.read_bytes()) == expected:
        return errors
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}:typed_artifact_not_json:{ref}:{exc}")
        return errors
    candidates = {
        str(payload.get("content_sha256")),
        str(payload.get("payload_sha256")),
        str(payload.get("artifact_sha256")),
        _payload_content_hash(payload),
    }
    if expected not in candidates:
        errors.append(f"{label}:typed_artifact_hash_mismatch:{ref}:{path}")
    return errors


def _path_for_ref(record: ActualTaskPipelineRunV1, ref: str, run_dir: Path | None) -> Path | None:
    if ref == record.source_theorem_ref:
        return _resolve_path(record.source_theorem_path, run_dir)
    artifact_path = record.artifact_paths.get(ref)
    if artifact_path is None:
        return None
    return _resolve_path(artifact_path, run_dir)


def _resolve_path(path_value: str, base_dir: Path | None) -> Path:
    path = Path(path_value)
    if path.is_absolute() or base_dir is None:
        return path
    return base_dir / path


def _read_json(path: Path, errors: list[str], label: str, ref: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}:artifact_json_read_error:{ref}:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label}:artifact_json_not_object:{ref}")
        return None
    return payload


def _payload_content_hash(payload: dict[str, Any]) -> str:
    payload_without_identity = {key: value for key, value in payload.items() if key not in HASH_ID_FIELDS}
    return _hash_text(_canonical_json(payload_without_identity))


def _as_ref_set(payload: dict[str, Any], *keys: str) -> set[str]:
    refs: set[str] = set()
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str):
            refs.add(value)
        elif isinstance(value, list):
            refs.update(str(item) for item in value)
        elif isinstance(value, tuple):
            refs.update(str(item) for item in value)
    return refs


def _normalize_path(path: Path) -> str:
    try:
        return str(path.resolve()).replace("\\", "/").lower()
    except OSError:
        return str(path).replace("\\", "/").lower()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _is_typed_sha_ref(value: Any) -> bool:
    return isinstance(value, str) and TYPED_SHA_RE.fullmatch(value) is not None


def _hash_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def _hash_text(text: str) -> str:
    return _hash_bytes(text.encode("utf-8"))


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
