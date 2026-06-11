from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ObligationStatus = Literal["open", "blocked", "closed", "invalidated"]
ProofUseStatus = Literal[
    "not_allowed",
    "diagnostic_only",
    "search_only",
    "lean_patch_candidate",
    "final_theorem",
]
EvidenceStatus = Literal[
    "used_in_search",
    "used_in_final_proof",
    "diagnostic_only",
    "abandoned",
    "refuted_key_branch",
]


@dataclass(frozen=True)
class Obligation:
    obligation_id: str
    statement_hash: str
    status: ObligationStatus = "open"
    parent_obligation_ids: tuple[str, ...] = ()
    blocker_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRef:
    evidence_id: str
    artifact_ref: str
    evidence_status: EvidenceStatus
    media_type: str
    content_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Derivation:
    derivation_id: str
    conclusion_obligation_id: str
    rule_id: str
    evidence_refs: tuple[str, ...]
    required_side_condition_ids: tuple[str, ...] = ()
    proof_use_status: ProofUseStatus = "not_allowed"
    final_verify_ref: str | None = None
    protected_theorem_hash_unchanged: bool = False
    final_verify_report: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GraphPatch:
    patch_id: str
    schema_id: str = "proof_state.graph_patch.v1"
    obligations: tuple[Obligation, ...] = ()
    evidence_refs: tuple[EvidenceRef, ...] = ()
    derivations: tuple[Derivation, ...] = ()
    invalidate_obligation_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
