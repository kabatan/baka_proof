from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class StandardGeometryLoopContract:
    schema_version: str = "1.0.0"
    workflow_id: str = "standard_geometry_loop:contract:v1"
    required_stages: tuple[str, ...] = (
        "lean_port",
        "goal_anchor",
        "extraction",
        "solve_request",
        "compiler",
        "worker",
        "final_verify_gate",
        "dag_update",
        "run_logger",
    )
    final_closure_stage: str = "final_verify_gate"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


__all__ = ["StandardGeometryLoopContract"]
