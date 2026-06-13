from __future__ import annotations


GOAL_LEVEL_RELATIONS = {"exact", "sufficient"}


def relation_allows_goal_level_proof_use(relation: str, direction_available: str | None = None) -> bool:
    if relation == "exact":
        return True
    if relation == "sufficient":
        return direction_available not in {None, "", "none"}
    return False


__all__ = ["GOAL_LEVEL_RELATIONS", "relation_allows_goal_level_proof_use"]
