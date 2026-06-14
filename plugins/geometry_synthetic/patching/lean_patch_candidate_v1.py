from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any


SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PATCH_KINDS = {"replace_proof_region", "add_helper_lemma_and_replace_proof_region"}
PROOF_ORIGINS = {"trace_compiler", "construction_compiler", "hybrid"}
CREATORS = {"TraceCompiler", "ConstructionCompiler"}


@dataclass(frozen=True)
class LeanPatchCandidateV1:
    schema_version: str
    patch_id: str
    source_task_run_id: str
    target_theorem_name: str
    target_file_path: str
    target_protected_statement_hash: str
    patch_kind: str
    allowed_edit_region: dict[str, str]
    required_imports: tuple[str, ...]
    helper_lemmas: tuple[dict[str, str], ...]
    proof_region_replacement: dict[str, str]
    solver_dependency_refs: tuple[str, ...]
    proof_template_id: str
    proof_origin: str
    raw_provider_output_used_as_proof: bool
    created_by: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.schema_version != "1.0.0":
            raise ValueError("LeanPatchCandidateV1.schema_version must be 1.0.0")
        if self.patch_kind not in PATCH_KINDS:
            raise ValueError(f"unsupported patch_kind: {self.patch_kind}")
        if self.proof_origin not in PROOF_ORIGINS:
            raise ValueError(f"unsupported proof_origin: {self.proof_origin}")
        if self.created_by not in CREATORS:
            raise ValueError(f"unsupported created_by: {self.created_by}")
        if self.raw_provider_output_used_as_proof:
            raise ValueError("raw provider output cannot be used as proof_region_replacement")
        _require_sha256("target_protected_statement_hash", self.target_protected_statement_hash)
        _validate_allowed_edit_region(self.allowed_edit_region)
        _validate_proof_region_replacement(self.proof_region_replacement)
        _validate_solver_dependencies(self.solver_dependency_refs)
        expected = expected_patch_id(
            self.target_protected_statement_hash,
            self.proof_region_replacement["text_hash"],
            self.solver_dependency_refs,
        )
        if self.patch_id != expected:
            raise ValueError(f"patch_id must be deterministic: expected {expected}")

    @classmethod
    def create(
        cls,
        *,
        source_task_run_id: str,
        target_theorem_name: str,
        target_file_path: str,
        target_protected_statement_hash: str,
        patch_kind: str,
        allowed_edit_region: dict[str, str],
        proof_region_text: str,
        solver_dependency_refs: tuple[str, ...],
        proof_template_id: str,
        proof_origin: str,
        created_by: str,
        required_imports: tuple[str, ...] = (),
        helper_lemmas: tuple[dict[str, str], ...] = (),
        raw_provider_output_used_as_proof: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> "LeanPatchCandidateV1":
        text_hash = sha256_ref(proof_region_text)
        replacement = {"text_ref": text_hash, "text_hash": text_hash}
        patch_id = expected_patch_id(target_protected_statement_hash, text_hash, solver_dependency_refs)
        return cls(
            schema_version="1.0.0",
            patch_id=patch_id,
            source_task_run_id=source_task_run_id,
            target_theorem_name=target_theorem_name,
            target_file_path=target_file_path,
            target_protected_statement_hash=target_protected_statement_hash,
            patch_kind=patch_kind,
            allowed_edit_region=allowed_edit_region,
            required_imports=required_imports,
            helper_lemmas=helper_lemmas,
            proof_region_replacement=replacement,
            solver_dependency_refs=solver_dependency_refs,
            proof_template_id=proof_template_id,
            proof_origin=proof_origin,
            raw_provider_output_used_as_proof=raw_provider_output_used_as_proof,
            created_by=created_by,
            metadata=metadata or {},
        )

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LeanPatchCandidateV1":
        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(payload) - allowed)
        if unknown:
            raise ValueError(f"unknown LeanPatchCandidateV1 fields: {unknown}")
        missing = sorted(allowed - {"metadata"} - set(payload))
        if missing:
            raise ValueError(f"missing LeanPatchCandidateV1 fields: {missing}")
        return cls(
            schema_version=str(payload["schema_version"]),
            patch_id=str(payload["patch_id"]),
            source_task_run_id=str(payload["source_task_run_id"]),
            target_theorem_name=str(payload["target_theorem_name"]),
            target_file_path=str(payload["target_file_path"]),
            target_protected_statement_hash=str(payload["target_protected_statement_hash"]),
            patch_kind=str(payload["patch_kind"]),
            allowed_edit_region=dict(payload["allowed_edit_region"]),
            required_imports=tuple(payload.get("required_imports", ())),
            helper_lemmas=tuple(dict(item) for item in payload.get("helper_lemmas", ())),
            proof_region_replacement=dict(payload["proof_region_replacement"]),
            solver_dependency_refs=tuple(payload["solver_dependency_refs"]),
            proof_template_id=str(payload["proof_template_id"]),
            proof_origin=str(payload["proof_origin"]),
            raw_provider_output_used_as_proof=bool(payload["raw_provider_output_used_as_proof"]),
            created_by=str(payload["created_by"]),
            metadata=dict(payload.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def lean_patch_candidate_from_dict(payload: dict[str, Any]) -> LeanPatchCandidateV1:
    return LeanPatchCandidateV1.from_dict(payload)


def expected_patch_id(
    target_protected_statement_hash: str,
    proof_region_replacement_hash: str,
    solver_dependency_refs: tuple[str, ...],
) -> str:
    canonical = json.dumps(
        {
            "proof_region_replacement_hash": proof_region_replacement_hash,
            "solver_dependency_refs": tuple(solver_dependency_refs),
            "target_protected_statement_hash": target_protected_statement_hash,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"lean_patch:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()}"


def sha256_ref(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _require_sha256(field_name: str, value: str) -> None:
    if not SHA256_RE.match(value):
        raise ValueError(f"{field_name} must be sha256:<64 hex>")


def _validate_allowed_edit_region(value: dict[str, str]) -> None:
    required = {"region_id", "start_marker", "end_marker"}
    if set(value) != required:
        raise ValueError("allowed_edit_region must contain exactly region_id, start_marker, end_marker")
    if not all(str(value[key]) for key in required):
        raise ValueError("allowed_edit_region values must be non-empty strings")


def _validate_proof_region_replacement(value: dict[str, str]) -> None:
    if set(value) != {"text_ref", "text_hash"}:
        raise ValueError("proof_region_replacement must contain exactly text_ref and text_hash")
    _require_sha256("proof_region_replacement.text_ref", value["text_ref"])
    _require_sha256("proof_region_replacement.text_hash", value["text_hash"])
    if value["text_ref"] != value["text_hash"]:
        raise ValueError("proof_region_replacement.text_ref must be content-addressed by text_hash")


def _validate_solver_dependencies(refs: tuple[str, ...]) -> None:
    if not refs:
        raise ValueError("solver_dependency_refs must not be empty")
    if not any(ref.startswith("provider_run_manifest:") for ref in refs):
        raise ValueError("solver_dependency_refs must include provider_run_manifest:<hash>")
    if not any(ref.startswith(("geotrace:", "aux_construction_candidate:")) for ref in refs):
        raise ValueError("solver_dependency_refs must include a normalized solver artifact")
    if not any(ref.startswith(("trace_compilation:", "construction_compilation:")) for ref in refs):
        raise ValueError("solver_dependency_refs must include a compiler result artifact")
