from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LeanErrorSummary:
    status: str
    stderr_tail: str
    stdout_tail: str
