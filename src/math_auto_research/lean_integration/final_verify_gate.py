from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.lean_integration.goal_anchor import extract_theorem_statement, goal_anchor_for_text, hash_text
from math_auto_research.lean_integration.lean_port import LeanPort
from math_auto_research.lean_integration.proof_region_guard import ProofRegionGuard


FORBIDDEN_DECLARATIONS = ("axiom", "unsafe", "admit")


@dataclass(frozen=True)
class FinalVerifyReport:
    schema_version: str
    report_id: str
    target_obligation_id: str
    theorem_statement_hash: str
    protected_theorem_hash_unchanged: bool
    lean_status: str
    forbidden_axiom_status: str
    sorry_status: str
    proof_use_status: str
    lean_artifact_ref: str | None = None
    proof_artifact_ref: str | None = None
    proof_use_provenance_status: str = "failed"
    solver_backed_proof_status: str = "not_applicable"
    protected_statement_hash_source: str = "original_file"
    checked_candidate_file_ref: str | None = None
    proof_region_guard_status: str = "failed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class FinalVerifyGate:
    def __init__(self, lean_port: LeanPort | None = None, region_guard: ProofRegionGuard | None = None) -> None:
        self.lean_port = lean_port or LeanPort()
        self.region_guard = region_guard or ProofRegionGuard()

    def goal_anchor(self, lean_text: str, theorem_name: str, file_path: Path | None = None):
        return goal_anchor_for_text(lean_text, theorem_name, file_path or Path("<memory>"))

    def verify_file(
        self,
        original_text: str,
        candidate_path: Path,
        theorem_name: str,
        target_obligation_id: str,
        proof_use_provenance: dict[str, Any] | None = None,
        admitted_import_prefixes: tuple[str, ...] = ("MathAutoResearch", "Mathlib", "LeanGeo"),
    ) -> FinalVerifyReport:
        candidate_text = candidate_path.read_text(encoding="utf-8")
        original_statement = extract_theorem_statement(original_text, theorem_name)
        candidate_statement = extract_theorem_statement(candidate_text, theorem_name)
        original_hash = hash_text(original_statement)
        theorem_hash_unchanged = original_hash == hash_text(candidate_statement)
        region_ok = self.region_guard.permits(original_text, candidate_text)
        lean_result = self.lean_port.compile_file(candidate_path)
        sorry_status = "failed" if contains_sorry(candidate_text, theorem_name) else "clean"
        forbidden_status = "failed" if contains_forbidden_declaration(candidate_text) else "clean"
        admitted_imports_ok = imports_are_admitted(candidate_text, admitted_import_prefixes)
        toy_target_ok = not contains_local_toy_target(candidate_text)
        provenance_ok = proof_use_provenance_valid(proof_use_provenance)
        solver_backed_mode = bool(proof_use_provenance and proof_use_provenance.get("solver_backed_mode"))
        passed = (
            theorem_hash_unchanged
            and region_ok
            and lean_result.status == "passed"
            and sorry_status == "clean"
            and forbidden_status == "clean"
            and admitted_imports_ok
            and toy_target_ok
            and provenance_ok
        )
        return FinalVerifyReport(
            schema_version="1.0.0",
            report_id=f"final_verify:{hash_text(str(candidate_path))[:16]}",
            target_obligation_id=target_obligation_id,
            theorem_statement_hash=original_hash,
            protected_theorem_hash_unchanged=theorem_hash_unchanged and region_ok,
            lean_status=lean_result.status if region_ok else "failed",
            forbidden_axiom_status=forbidden_status if admitted_imports_ok and toy_target_ok and provenance_ok else "failed",
            sorry_status=sorry_status,
            proof_use_status="final_theorem" if passed else "not_allowed",
            lean_artifact_ref=str(candidate_path),
            proof_artifact_ref=str(candidate_path),
            proof_use_provenance_status="passed" if provenance_ok else "failed",
            solver_backed_proof_status=(
                "passed" if solver_backed_mode and passed else "failed" if solver_backed_mode else "not_applicable"
            ),
            protected_statement_hash_source="source_problem" if solver_backed_mode else "original_file",
            checked_candidate_file_ref=f"sha256:{hashlib.sha256(candidate_text.encode('utf-8')).hexdigest()}",
            proof_region_guard_status="passed" if region_ok else "failed",
        )


def contains_sorry(text: str, theorem_name: str | None = None) -> bool:
    if theorem_name:
        target_region = _target_proof_region_text(text, theorem_name)
        if target_region is not None:
            return re.search(r"\bsorry\b", target_region) is not None
    return re.search(r"\bsorry\b", text) is not None


def contains_forbidden_declaration(text: str) -> bool:
    import re

    return any(re.search(rf"\b{term}\b", text) is not None for term in FORBIDDEN_DECLARATIONS)


def imports_are_admitted(text: str, admitted_prefixes: tuple[str, ...]) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("import "):
            continue
        module = stripped.split(None, 1)[1].strip()
        if not any(module == prefix or module.startswith(prefix + ".") for prefix in admitted_prefixes):
            return False
    return True


def contains_local_toy_target(text: str) -> bool:
    forbidden = ("ToyGeometry", "LocalToyGeometry", "toy_geometry")
    return any(token in text for token in forbidden)


def _target_proof_region_text(text: str, theorem_name: str) -> str | None:
    short_name = theorem_name.rsplit(".", 1)[-1]
    start = f"-- MARP_PROOF_REGION_START:{short_name}"
    end = f"-- MARP_PROOF_REGION_END:{short_name}"
    if start not in text or end not in text:
        return None
    return text.split(start, 1)[1].split(end, 1)[0]


def proof_use_provenance_valid(provenance: dict[str, Any] | None) -> bool:
    if provenance is None:
        return False
    required = {
        "geometry_extraction_report_ref",
        "goal_anchor_ref",
        "protected_statement_hash",
        "target_library_manifest_hash",
    }
    if not required.issubset(provenance):
        return False
    if not provenance.get("solver_backed_mode"):
        return True
    solver_backed_required = {
        "provider_run_manifest_ref",
        "normalized_solver_artifact_ref",
        "compiler_result_ref",
        "lean_patch_candidate_ref",
        "worker_result_ref",
        "proof_region_diff_hash",
        "generated_candidate_file_ref",
    }
    if not solver_backed_required.issubset(provenance):
        return False
    return (
        _matches_ref(provenance["provider_run_manifest_ref"], ("provider_run_manifest:",))
        and _matches_ref(provenance["normalized_solver_artifact_ref"], ("geotrace:", "aux_construction_candidate:"))
        and _matches_ref(provenance["compiler_result_ref"], ("trace_compilation:", "construction_compilation:"))
        and _matches_ref(provenance["lean_patch_candidate_ref"], ("lean_patch:",))
        and _matches_ref(provenance["worker_result_ref"], ("worker_result:",))
        and _matches_sha256(provenance["proof_region_diff_hash"])
        and _matches_sha256(provenance["generated_candidate_file_ref"])
    )


def _matches_ref(value: Any, prefixes: tuple[str, ...]) -> bool:
    return isinstance(value, str) and value.startswith(prefixes)


def _matches_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is not None
