from __future__ import annotations

from math_auto_research.proof_state.dag import StateReader


class ClosureEngine:
    def __init__(self, reader: StateReader) -> None:
        self.reader = reader

    def is_obligation_closed(self, obligation_id: str) -> bool:
        return self.reader.is_closed(obligation_id)


__all__ = ["ClosureEngine"]
