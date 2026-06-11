from __future__ import annotations

from dataclasses import dataclass


VALID_BUDGETS = {"tiny", "small", "medium", "heavy", "extreme"}


@dataclass(frozen=True)
class ResourceRequest:
    component: str
    engine_role: str = "none"
    budget: str = "small"
    timeout_sec: float = 30.0

    def validate(self) -> None:
        if self.budget not in VALID_BUDGETS:
            raise ValueError(f"unsupported budget: {self.budget}")
        if self.engine_role == "heavy_search" and self.budget not in {"heavy", "extreme"}:
            raise ResourceRejected("heavy_search requires heavy or extreme budget")


class ResourceRejected(RuntimeError):
    pass
