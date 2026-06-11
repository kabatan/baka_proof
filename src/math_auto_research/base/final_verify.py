from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from math_auto_research.base.lean_port import LeanPort


FORBIDDEN_DECLARATIONS = ("axiom", "unsafe", "admit")


@dataclass(frozen=True)
class GoalAnchor:
    theorem_name: str
    theorem_statement_hash: str


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


class ProofRegionGuard:
    start_pattern = re.compile(r"--\s*PROOF-REGION-START:[A-Za-z0-9_.:-]+")
    end_pattern = re.compile(r"--\s*PROOF-REGION-END:[A-Za-z0-9_.:-]+")

    def outside_regions(self, text: str) -> str:
        kept: list[str] = []
        in_region = False
        for line in text.splitlines():
            if self.start_pattern.match(line.strip()):
                in_region = True
                continue
            if self.end_pattern.match(line.strip()):
                in_region = False
                continue
            if not in_region:
                kept.append(line)
        return "\n".join(kept)

    def permits(self, original: str, candidate: str) -> bool:
        return self.outside_regions(original) == self.outside_regions(candidate)


class FinalVerifyGate:
    def __init__(self, lean_port: LeanPort | None = None, region_guard: ProofRegionGuard | None = None) -> None:
        self.lean_port = lean_port or LeanPort()
        self.region_guard = region_guard or ProofRegionGuard()

    def goal_anchor(self, lean_text: str, theorem_name: str) -> GoalAnchor:
        statement = extract_theorem_statement(lean_text, theorem_name)
        return GoalAnchor(theorem_name=theorem_name, theorem_statement_hash=hash_text(statement))

    def verify_file(
        self,
        original_text: str,
        candidate_path: Path,
        theorem_name: str,
        target_obligation_id: str,
    ) -> FinalVerifyReport:
        candidate_text = candidate_path.read_text(encoding="utf-8")
        original_anchor = self.goal_anchor(original_text, theorem_name)
        candidate_anchor = self.goal_anchor(candidate_text, theorem_name)
        theorem_hash_unchanged = original_anchor.theorem_statement_hash == candidate_anchor.theorem_statement_hash
        region_ok = self.region_guard.permits(original_text, candidate_text)
        lean_result = self.lean_port.check_file(candidate_path)
        sorry_status = "failed" if contains_sorry(candidate_text) else "clean"
        forbidden_status = "failed" if contains_forbidden_declaration(candidate_text) else "clean"
        passed = (
            theorem_hash_unchanged
            and region_ok
            and lean_result.status == "passed"
            and sorry_status == "clean"
            and forbidden_status == "clean"
        )
        return FinalVerifyReport(
            schema_version="1.0.0",
            report_id=f"final_verify:{hash_text(str(candidate_path))[:16]}",
            target_obligation_id=target_obligation_id,
            theorem_statement_hash=original_anchor.theorem_statement_hash,
            protected_theorem_hash_unchanged=theorem_hash_unchanged and region_ok,
            lean_status=lean_result.status if region_ok else "failed",
            forbidden_axiom_status=forbidden_status,
            sorry_status=sorry_status,
            proof_use_status="final_theorem" if passed else "not_allowed",
            lean_artifact_ref=str(candidate_path),
            proof_artifact_ref=str(candidate_path),
        )


def extract_theorem_statement(lean_text: str, theorem_name: str) -> str:
    pattern = re.compile(rf"\btheorem\s+{re.escape(theorem_name)}\b(?P<body>.*?)(?::=|:=\s*by)", re.DOTALL)
    match = pattern.search(lean_text)
    if match is None:
        raise ValueError(f"theorem not found: {theorem_name}")
    return f"theorem {theorem_name}{match.group('body').strip()}"


def hash_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def contains_sorry(text: str) -> bool:
    return re.search(r"\bsorry\b", text) is not None


def contains_forbidden_declaration(text: str) -> bool:
    return any(re.search(rf"\b{term}\b", text) is not None for term in FORBIDDEN_DECLARATIONS)
