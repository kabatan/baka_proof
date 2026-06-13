from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ActionPlan:
    schema_version: str
    plan_id: str
    task_kinds: tuple[str, ...]
    constraints: dict[str, Any]
    escalation_policy: str
    artifact_refs: tuple[str, ...]
    proof_use_note: str
    model_invocation_record: dict[str, Any] | None = None
    controller_output: dict[str, Any] | None = None
    proof_use_status: str = "not_allowed"
    final_verify_ref: None = field(default=None)

    def __post_init__(self) -> None:
        if self.proof_use_status == "final_theorem" or self.final_verify_ref is not None:
            raise ValueError("ActionPlan cannot close obligations or claim final theorem")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
