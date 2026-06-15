from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from plugins.geometry_full2d.run_records import content_addressed_typed_ref


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
TYPED_SHA_RE = re.compile(r"^[A-Za-z0-9_:.+-]+:sha256:[0-9a-f]{64}$")


class SolverBackedProofCertificateFull2D:
    def __init__(self, **payload: Any) -> None:
        normalized = _normalize_payload(payload)
        errors = validate_solver_backed_certificate_full2d(normalized)
        if errors:
            raise ValueError(";".join(errors))
        self._payload = normalized
        for key, value in normalized.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **payload: Any) -> "SolverBackedProofCertificateFull2D":
        base = _normalize_payload({**payload, "schema_version": payload.get("schema_version", "1.0.0")})
        body = _without_identity(base)
        certificate_id = content_addressed_typed_ref("SolverBackedProofCertificateFull2D", body)
        base["certificate_id"] = certificate_id
        return cls(**base)

    def to_dict(self) -> dict[str, Any]:
        return dict(self._payload)


def validate_solver_backed_certificate_full2d(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    normalized = _normalize_payload(payload)
    required = {
        "schema_version",
        "certificate_id",
        "task_id",
        "source_statement_hash",
        "extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "engine_output_refs",
        "compiler_result_refs",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
        "proof_region_diff_ref",
        "checked_candidate_file_ref",
        "theorem_hash_unchanged",
        "no_sorry",
        "no_forbidden_axioms",
        "raw_solver_output_used_as_proof",
        "proof_use_status",
        "status",
    }
    missing = sorted(key for key in required if key not in normalized)
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if normalized["schema_version"] != "1.0.0":
        errors.append("schema_version_mismatch")
    certificate_id = str(normalized["certificate_id"])
    if not certificate_id.startswith("SolverBackedProofCertificateFull2D:"):
        errors.append("certificate_id_prefix_mismatch")
    elif _is_typed_sha(certificate_id):
        expected = content_addressed_typed_ref("SolverBackedProofCertificateFull2D", _without_identity(normalized))
        if certificate_id != expected:
            errors.append("certificate_id_content_mismatch")
    else:
        errors.append("certificate_id_not_typed_sha_ref")
    if normalized.get("target_library") not in {None, "GeometryFull2DTarget:1.0.0"}:
        errors.append("target_library_mismatch")
    for key in ("source_statement_hash", "proof_region_diff_ref", "checked_candidate_file_ref"):
        if not _is_sha256(normalized[key]):
            errors.append(f"{key}_not_sha256")
    prefix_requirements = {
        "extraction_report_ref": ("GeometryFull2DExtraction:",),
        "claim_spec_ref": ("GeometryFull2DClaimSpec:",),
        "provider_run_manifest_ref": ("ProviderRunManifestFull2D:",),
        "lean_patch_candidate_ref": ("LeanPatchCandidateFull2D:",),
        "proof_worker_result_ref": ("ProofWorkerResultFull2D:", "worker_result:"),
        "final_verify_report_ref": ("FinalVerifyGateFull2D:", "final_verify:"),
    }
    for key, prefixes in prefix_requirements.items():
        if not isinstance(normalized[key], str) or not normalized[key].startswith(prefixes):
            errors.append(f"{key}_prefix_mismatch")
    engine_refs = _as_tuple(normalized.get("engine_output_refs"))
    if not engine_refs:
        errors.append("engine_output_refs_missing")
    elif any(not _matches_engine_ref(ref) for ref in engine_refs):
        errors.append("engine_output_refs_prefix_mismatch")
    compiler_refs = _as_tuple(normalized.get("compiler_result_refs"))
    if not compiler_refs:
        errors.append("compiler_result_refs_missing")
    elif any(not ref.startswith("CompilerResultFull2D:") for ref in compiler_refs):
        errors.append("compiler_result_refs_prefix_mismatch")
    final_verify_status = normalized.get("final_verify_status", "passed")
    if final_verify_status != "passed":
        errors.append("final_verify_status_not_passed")
    if normalized.get("solver_dependency_status", "passed") != "passed":
        errors.append("solver_dependency_status_not_passed")
    if normalized["proof_use_status"] != "solver_backed_final_theorem":
        errors.append("proof_use_status_not_solver_backed_final_theorem")
    if normalized["status"] != "passed":
        errors.append("certificate_status_not_passed")
    for key in ("theorem_hash_unchanged", "no_sorry", "no_forbidden_axioms"):
        if normalized[key] is not True:
            errors.append(f"{key}_not_true")
    if normalized["raw_solver_output_used_as_proof"] is not False:
        errors.append("raw_solver_output_used_as_proof")
    if normalized.get("raw_provider_output_used_as_proof") is True:
        errors.append("raw_provider_output_used_as_proof")
    for rule in _as_tuple(normalized.get("used_rule_refs", ())):
        if not rule.startswith("full2d_rule:"):
            errors.append("used_rule_ref_prefix_mismatch")
    return sorted(set(errors))


def solver_backed_certificate_full2d_from_dict(payload: dict[str, Any]) -> SolverBackedProofCertificateFull2D:
    return SolverBackedProofCertificateFull2D(**payload)


def _normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    normalized.setdefault("schema_version", "1.0.0")
    if "proof_worker_result_ref" not in normalized and "worker_result_ref" in normalized:
        normalized["proof_worker_result_ref"] = normalized["worker_result_ref"]
    if "worker_result_ref" not in normalized and "proof_worker_result_ref" in normalized:
        normalized["worker_result_ref"] = normalized["proof_worker_result_ref"]
    if "final_verify_report_ref" not in normalized and "final_verify_ref" in normalized:
        normalized["final_verify_report_ref"] = normalized["final_verify_ref"]
    if "final_verify_ref" not in normalized and "final_verify_report_ref" in normalized:
        normalized["final_verify_ref"] = normalized["final_verify_report_ref"]
    if "compiler_result_refs" not in normalized and "compiler_result_ref" in normalized:
        normalized["compiler_result_refs"] = [normalized["compiler_result_ref"]]
    if "compiler_result_ref" not in normalized and _as_tuple(normalized.get("compiler_result_refs")):
        normalized["compiler_result_ref"] = _as_tuple(normalized["compiler_result_refs"])[0]
    if "engine_output_refs" not in normalized and "normalized_solver_artifact_ref" in normalized:
        normalized["engine_output_refs"] = [normalized["normalized_solver_artifact_ref"]]
    if "normalized_solver_artifact_ref" not in normalized and _as_tuple(normalized.get("engine_output_refs")):
        normalized["normalized_solver_artifact_ref"] = _as_tuple(normalized["engine_output_refs"])[0]
    if "claim_spec_ref" not in normalized and normalized.get("task_id") and normalized.get("source_statement_hash"):
        seed = {"task_id": normalized["task_id"], "source_statement_hash": normalized["source_statement_hash"]}
        normalized["claim_spec_ref"] = f"GeometryFull2DClaimSpec:{_sha256_json(seed)}"
    if "final_verify_status" not in normalized and normalized.get("status") == "passed":
        normalized["final_verify_status"] = "passed"
    if "solver_dependency_status" not in normalized and normalized.get("status") == "passed":
        normalized["solver_dependency_status"] = "passed"
    if "raw_provider_output_used_as_proof" not in normalized:
        normalized["raw_provider_output_used_as_proof"] = normalized.get("raw_solver_output_used_as_proof", False)
    for key in ("engine_output_refs", "compiler_result_refs", "used_rule_refs", "used_rule_ids"):
        if key in normalized:
            normalized[key] = list(_as_tuple(normalized[key]))
    return normalized


def _without_identity(payload: dict[str, Any]) -> dict[str, Any]:
    identity = {"certificate_id", "content_sha256", "payload_sha256", "artifact_sha256"}
    return {key: value for key, value in _normalize_payload(payload).items() if key not in identity}


def _matches_engine_ref(ref: str) -> bool:
    prefixes = (
        "EngineOutputFull2D:",
        "Full2DTraceV1:",
        "AuxiliaryConstructionFull2D:",
        "SyntheticClosureTraceFull2D:",
        "ConstructionTraceFull2D:",
        "AlgebraicCertificateFull2D:",
        "MetricAngleTraceFull2D:",
        "TransformationTraceFull2D:",
        "OrderCaseReportFull2D:",
        "CoverageGateFull2D:",
        "InequalityCertificateFull2D:",
        "LeanPatchCandidateFull2D:",
        "PortfolioDecisionFull2D:",
        "geotrace:",
        "aux_construction_candidate:",
    )
    return isinstance(ref, str) and ref.startswith(prefixes)


def _as_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return ()


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _is_typed_sha(value: Any) -> bool:
    return isinstance(value, str) and TYPED_SHA_RE.fullmatch(value) is not None


def _sha256_json(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(data.encode('utf-8')).hexdigest()}"
