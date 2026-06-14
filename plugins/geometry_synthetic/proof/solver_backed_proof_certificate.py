from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class SolverBackedProofCertificate:
    schema_version: str
    certificate_id: str
    task_run_id: str
    benchmark_entry_id: str
    baseline_id: str
    source_problem_ref: str
    generated_candidate_file_ref: str
    theorem_name: str
    protected_statement_hash: str
    extraction_report_ref: str
    goal_anchor_ref: str
    provider_run_manifest_ref: str
    normalized_solver_artifact: dict[str, str]
    compiler_result_ref: str
    lean_patch_candidate_ref: str
    worker_result_ref: str
    final_verify_report_ref: str
    proof_region_diff_hash: str
    solver_dependency_status: str
    theorem_hash_unchanged: bool
    no_sorry: bool
    no_forbidden_axioms: bool
    final_verify_status: str
    status: str
    failure_reason: str | None

    def __post_init__(self) -> None:
        if self.schema_version != "1.0.0":
            raise ValueError("SolverBackedProofCertificate.schema_version must be 1.0.0")
        if self.baseline_id not in {"B2", "B4", "other"}:
            raise ValueError("baseline_id must be B2, B4, or other")
        _require_sha256("source_problem_ref", self.source_problem_ref)
        _require_sha256("generated_candidate_file_ref", self.generated_candidate_file_ref)
        _require_sha256("protected_statement_hash", self.protected_statement_hash)
        _require_sha256("proof_region_diff_hash", self.proof_region_diff_hash)
        _require_prefix("extraction_report_ref", self.extraction_report_ref, ("geometry_extraction_report:", "geometry_extraction:"))
        _require_prefix("goal_anchor_ref", self.goal_anchor_ref, ("goal_anchor:", "goal:"))
        _require_prefix("provider_run_manifest_ref", self.provider_run_manifest_ref, ("provider_run_manifest:",))
        _validate_solver_artifact(self.normalized_solver_artifact)
        _require_prefix("compiler_result_ref", self.compiler_result_ref, ("trace_compilation:", "construction_compilation:"))
        _require_prefix("lean_patch_candidate_ref", self.lean_patch_candidate_ref, ("lean_patch:",))
        _require_prefix("worker_result_ref", self.worker_result_ref, ("worker_result:",))
        _require_prefix("final_verify_report_ref", self.final_verify_report_ref, ("final_verify:",))
        if self.solver_dependency_status not in {"passed", "failed"}:
            raise ValueError("solver_dependency_status must be passed or failed")
        if self.final_verify_status != "final_theorem":
            raise ValueError("final_verify_status must be final_theorem")
        if self.status not in {"passed", "failed"}:
            raise ValueError("status must be passed or failed")
        if self.status == "passed":
            if self.failure_reason is not None:
                raise ValueError("passed certificates must not include failure_reason")
            if not (
                self.solver_dependency_status == "passed"
                and self.theorem_hash_unchanged
                and self.no_sorry
                and self.no_forbidden_axioms
            ):
                raise ValueError("passed certificates require passed dependencies and clean final verification")
        expected = expected_certificate_id(self.to_unsigned_dict())
        if self.certificate_id != expected:
            raise ValueError(f"certificate_id must be deterministic: expected {expected}")

    @classmethod
    def create(cls, **kwargs: Any) -> "SolverBackedProofCertificate":
        payload = dict(kwargs)
        payload.setdefault("schema_version", "1.0.0")
        payload["certificate_id"] = expected_certificate_id(_unsigned_payload(payload))
        return cls(**payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SolverBackedProofCertificate":
        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(payload) - allowed)
        if unknown:
            raise ValueError(f"unknown SolverBackedProofCertificate fields: {unknown}")
        missing = sorted(allowed - set(payload))
        if missing:
            raise ValueError(f"missing SolverBackedProofCertificate fields: {missing}")
        return cls(
            schema_version=str(payload["schema_version"]),
            certificate_id=str(payload["certificate_id"]),
            task_run_id=str(payload["task_run_id"]),
            benchmark_entry_id=str(payload["benchmark_entry_id"]),
            baseline_id=str(payload["baseline_id"]),
            source_problem_ref=str(payload["source_problem_ref"]),
            generated_candidate_file_ref=str(payload["generated_candidate_file_ref"]),
            theorem_name=str(payload["theorem_name"]),
            protected_statement_hash=str(payload["protected_statement_hash"]),
            extraction_report_ref=str(payload["extraction_report_ref"]),
            goal_anchor_ref=str(payload["goal_anchor_ref"]),
            provider_run_manifest_ref=str(payload["provider_run_manifest_ref"]),
            normalized_solver_artifact=dict(payload["normalized_solver_artifact"]),
            compiler_result_ref=str(payload["compiler_result_ref"]),
            lean_patch_candidate_ref=str(payload["lean_patch_candidate_ref"]),
            worker_result_ref=str(payload["worker_result_ref"]),
            final_verify_report_ref=str(payload["final_verify_report_ref"]),
            proof_region_diff_hash=str(payload["proof_region_diff_hash"]),
            solver_dependency_status=str(payload["solver_dependency_status"]),
            theorem_hash_unchanged=bool(payload["theorem_hash_unchanged"]),
            no_sorry=bool(payload["no_sorry"]),
            no_forbidden_axioms=bool(payload["no_forbidden_axioms"]),
            final_verify_status=str(payload["final_verify_status"]),
            status=str(payload["status"]),
            failure_reason=payload.get("failure_reason"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_unsigned_dict(self) -> dict[str, Any]:
        return _unsigned_payload(self.to_dict())


def solver_backed_proof_certificate_from_dict(payload: dict[str, Any]) -> SolverBackedProofCertificate:
    return SolverBackedProofCertificate.from_dict(payload)


def expected_certificate_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(_unsigned_payload(payload), sort_keys=True, separators=(",", ":"))
    return f"solver_backed_proof:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"


def _unsigned_payload(payload: dict[str, Any]) -> dict[str, Any]:
    unsigned = dict(payload)
    unsigned.pop("certificate_id", None)
    return unsigned


def _require_sha256(field_name: str, value: str) -> None:
    if not SHA256_RE.match(value):
        raise ValueError(f"{field_name} must be sha256:<64 hex>")


def _require_prefix(field_name: str, value: str, prefixes: tuple[str, ...]) -> None:
    if not value.startswith(prefixes):
        raise ValueError(f"{field_name} must start with one of {prefixes}")


def _validate_solver_artifact(value: dict[str, str]) -> None:
    if set(value) != {"kind", "ref", "source_engine_role"}:
        raise ValueError("normalized_solver_artifact must contain kind, ref, source_engine_role")
    kind = value["kind"]
    if kind not in {"geotrace", "auxiliary_construction", "hybrid"}:
        raise ValueError("normalized_solver_artifact.kind is unsupported")
    expected_prefixes = {
        "geotrace": ("geotrace:",),
        "auxiliary_construction": ("aux_construction_candidate:",),
        "hybrid": ("geotrace:", "aux_construction_candidate:"),
    }[kind]
    _require_prefix("normalized_solver_artifact.ref", value["ref"], expected_prefixes)
    if value["source_engine_role"] not in {"symbolic_closure", "construction_proposer", "hybrid"}:
        raise ValueError("normalized_solver_artifact.source_engine_role is unsupported")
