from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class WorkOrder:
    schema_version: str
    work_order_id: str
    task_kind: str
    target_obligation_id: str
    constraints: dict[str, Any]
    artifact_refs: tuple[str, ...]
    proof_use_note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
