from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class SolverBackedProofCertificateFull2D:
    schema_version: str
    certificate_id: str
    task_id: str
    theorem_name: str
    target_library: str
    source_statement_hash: str
    extraction_report_ref: str
    provider_run_manifest_ref: str
    normalized_solver_artifact_ref: str
    compiler_result_ref: str
    lean_patch_candidate_ref: str
    worker_result_ref: str
    final_verify_ref: str
    proof_region_diff_ref: str
    checked_candidate_file_ref: str
    final_verify_status: str
    solver_dependency_status: str
    theorem_hash_unchanged: bool
    no_sorry: bool
    no_forbidden_axioms: bool
    raw_solver_output_used_as_proof: bool
    proof_use_status: str
    status: str

    @classmethod
    def create(cls, **payload: Any) -> "SolverBackedProofCertificateFull2D":
        base = dict(payload)
        base.setdefault("schema_version", "1.0.0")
        body = {key: value for key, value in base.items() if key != "certificate_id"}
        certificate_id = f"SolverBackedProofCertificateFull2D:{_sha256_json(body)[7:]}"
        base["certificate_id"] = certificate_id
        cert = cls(**base)
        errors = validate_solver_backed_certificate_full2d(cert.to_dict())
        if errors:
            raise ValueError(";".join(errors))
        return cert

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_solver_backed_certificate_full2d(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "certificate_id",
        "task_id",
        "theorem_name",
        "target_library",
        "source_statement_hash",
        "extraction_report_ref",
        "provider_run_manifest_ref",
        "normalized_solver_artifact_ref",
        "compiler_result_ref",
        "lean_patch_candidate_ref",
        "worker_result_ref",
        "final_verify_ref",
        "proof_region_diff_ref",
        "checked_candidate_file_ref",
        "final_verify_status",
        "solver_dependency_status",
        "theorem_hash_unchanged",
        "no_sorry",
        "no_forbidden_axioms",
        "raw_solver_output_used_as_proof",
        "proof_use_status",
        "status",
    }
    missing = sorted(key for key in required if key not in payload)
    if missing:
        return [f"missing_fields:{','.join(missing)}"]
    if payload["schema_version"] != "1.0.0":
        errors.append("schema_version_mismatch")
    if not str(payload["certificate_id"]).startswith("SolverBackedProofCertificateFull2D:"):
        errors.append("certificate_id_prefix_mismatch")
    if payload["target_library"] != "GeometryFull2DTarget:1.0.0":
        errors.append("target_library_mismatch")
    for key in ("source_statement_hash", "proof_region_diff_ref", "checked_candidate_file_ref"):
        if not _is_sha256(payload[key]):
            errors.append(f"{key}_not_sha256")
    prefix_requirements = {
        "extraction_report_ref": ("GeometryFull2DExtraction:",),
        "provider_run_manifest_ref": ("ProviderRunManifestFull2D:",),
        "normalized_solver_artifact_ref": (
            "SyntheticClosureTraceFull2D:",
            "ConstructionTraceFull2D:",
            "AlgebraicCertificateFull2D:",
            "MetricAngleTraceFull2D:",
            "TransformationTraceFull2D:",
            "CoverageGateFull2D:",
            "InequalityCertificateFull2D:",
            "PortfolioDecisionFull2D:",
        ),
        "compiler_result_ref": ("CompilerResultFull2D:",),
        "lean_patch_candidate_ref": ("LeanPatchCandidateFull2D:",),
        "worker_result_ref": ("ProofWorkerResultFull2D:",),
        "final_verify_ref": ("FinalVerifyGateFull2D:", "final_verify:"),
    }
    for key, prefixes in prefix_requirements.items():
        if not isinstance(payload[key], str) or not payload[key].startswith(prefixes):
            errors.append(f"{key}_prefix_mismatch")
    if payload["final_verify_status"] != "passed":
        errors.append("final_verify_status_not_passed")
    if payload["solver_dependency_status"] != "passed":
        errors.append("solver_dependency_status_not_passed")
    if payload["proof_use_status"] != "solver_backed_final_theorem":
        errors.append("proof_use_status_not_solver_backed_final_theorem")
    if payload["status"] != "passed":
        errors.append("certificate_status_not_passed")
    for key in ("theorem_hash_unchanged", "no_sorry", "no_forbidden_axioms"):
        if payload[key] is not True:
            errors.append(f"{key}_not_true")
    if payload["raw_solver_output_used_as_proof"] is not False:
        errors.append("raw_solver_output_used_as_proof")
    return sorted(set(errors))


def solver_backed_certificate_full2d_from_dict(payload: dict[str, Any]) -> SolverBackedProofCertificateFull2D:
    errors = validate_solver_backed_certificate_full2d(payload)
    if errors:
        raise ValueError(";".join(errors))
    return SolverBackedProofCertificateFull2D(**payload)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _sha256_json(payload: dict[str, Any]) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256:{hashlib.sha256(data.encode('utf-8')).hexdigest()}"
