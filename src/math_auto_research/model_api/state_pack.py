from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ResearchStatePack:
    schema_version: str
    state_id: str
    proof_state_summary_ref: str
    selected_implementations_ref: str
    artifact_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkerStatePack:
    schema_version: str
    state_id: str
    work_order_id: str
    proof_region_ref: str
    artifact_refs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
