from __future__ import annotations

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
        sorry_status = "failed" if contains_sorry(candidate_text) else "clean"
        forbidden_status = "failed" if contains_forbidden_declaration(candidate_text) else "clean"
        admitted_imports_ok = imports_are_admitted(candidate_text, admitted_import_prefixes)
        toy_target_ok = not contains_local_toy_target(candidate_text)
        provenance_ok = proof_use_provenance_valid(proof_use_provenance)
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
        )


def contains_sorry(text: str) -> bool:
    import re

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


def proof_use_provenance_valid(provenance: dict[str, Any] | None) -> bool:
    if provenance is None:
        return False
    required = {
        "geometry_extraction_report_ref",
        "goal_anchor_ref",
        "protected_statement_hash",
        "target_library_manifest_hash",
    }
    return required.issubset(provenance)
