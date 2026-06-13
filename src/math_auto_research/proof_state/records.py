from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import ConfigDict, Field

from math_auto_research.base.schemas import SchemaRecord


ObligationStatus = Literal["open", "blocked", "closed", "invalidated"]
ProofUseStatus = Literal[
    "not_allowed",
    "search_only",
    "claim_level_only",
    "goal_level_allowed",
    "final_theorem",
]
EvidenceStatus = Literal[
    "used_in_search",
    "used_in_final_proof",
    "diagnostic_only",
    "abandoned",
    "refuted_key_branch",
]


class _ProofStateRecord(SchemaRecord):
    model_config = ConfigDict(extra="forbid", frozen=True)

    positional_fields: ClassVar[tuple[str, ...]] = ()

    def __init__(self, *args: Any, **data: Any) -> None:
        if args:
            if len(args) > len(self.positional_fields):
                raise TypeError(f"too many positional arguments for {type(self).__name__}")
            for name, value in zip(self.positional_fields, args, strict=False):
                if name in data:
                    raise TypeError(f"{type(self).__name__} got multiple values for {name}")
                data[name] = value
        super().__init__(**data)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class Obligation(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.obligation.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/obligation.schema.json"
    positional_fields: ClassVar[tuple[str, ...]] = ("obligation_id", "statement_hash", "status")

    obligation_id: str
    statement_hash: str
    status: ObligationStatus = "open"
    parent_obligation_ids: tuple[str, ...] = ()
    blocker_refs: tuple[str, ...] = ()


class EvidenceRef(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.evidence_ref.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/evidence_ref.schema.json"
    positional_fields: ClassVar[tuple[str, ...]] = (
        "evidence_id",
        "artifact_ref",
        "evidence_status",
        "media_type",
        "content_hash",
    )

    evidence_id: str
    artifact_ref: str
    evidence_status: EvidenceStatus
    media_type: str
    content_hash: str
    artifact_kind: str = "proof_artifact"


class Derivation(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.derivation.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/derivation.schema.json"
    positional_fields: ClassVar[tuple[str, ...]] = (
        "derivation_id",
        "conclusion_obligation_id",
        "rule_id",
        "evidence_refs",
    )

    derivation_id: str
    conclusion_obligation_id: str
    rule_id: str
    evidence_refs: tuple[str, ...]
    required_side_condition_ids: tuple[str, ...] = ()
    proof_use_status: ProofUseStatus = "not_allowed"
    final_verify_ref: str | None = None
    protected_theorem_hash_unchanged: bool = False
    final_verify_report: dict[str, Any] | None = None


class GraphPatch(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.graph_patch.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/graph_patch.schema.json"
    positional_fields: ClassVar[tuple[str, ...]] = ("patch_id",)

    patch_id: str
    schema_id: str = "proof_state.graph_patch.v1"
    obligations: tuple[Obligation, ...] = ()
    evidence_refs: tuple[EvidenceRef, ...] = ()
    derivations: tuple[Derivation, ...] = ()
    invalidate_obligation_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphPatchCommitResult(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.graph_patch_commit_result.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/graph_patch_commit_result.schema.json"

    patch_id: str
    status: Literal["committed", "rejected"]
    committed_obligation_ids: tuple[str, ...] = ()
    committed_derivation_ids: tuple[str, ...] = ()
    committed_evidence_ids: tuple[str, ...] = ()


class DAGSnapshot(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.dag_snapshot.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/dag_snapshot.schema.json"

    obligation_ids: tuple[str, ...]
    derivation_ids: tuple[str, ...]
    evidence_ref_ids: tuple[str, ...]


class StateReaderSummary(_ProofStateRecord):
    schema_id: ClassVar[str] = "proof_state.state_reader_summary.v1"
    schema_path: ClassVar[Any] = "schemas/proof_state/state_reader_summary.schema.json"

    obligation_count: int
    derivation_count: int
    evidence_ref_count: int
    closed_obligation_ids: tuple[str, ...] = ()
    open_obligation_ids: tuple[str, ...] = ()
