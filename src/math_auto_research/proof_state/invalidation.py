from __future__ import annotations

from math_auto_research.proof_state.records import GraphPatch


PROOF_CRITICAL_HASH_KEYS = {
    "schema_hash",
    "selected_implementations_hash",
    "target_library_manifest_hash",
    "geometry_extraction_contract_hash",
    "geometry_claim_spec_hash",
    "solver_policy_hash",
    "execution_plan_hash",
    "provider_adapter_hash",
    "rule_registry_hash",
    "construction_mapping_hash",
    "trust_boundary_hash",
    "protected_theorem_statement_hash",
    "lean_dependency_hash",
}


def invalidation_patch(patch_id: str, obligation_ids: list[str] | tuple[str, ...]) -> GraphPatch:
    return GraphPatch(patch_id=patch_id, invalidate_obligation_ids=tuple(obligation_ids))


def proof_critical_hash_changed(before: dict[str, str], after: dict[str, str]) -> bool:
    return any(before.get(key) != after.get(key) for key in PROOF_CRITICAL_HASH_KEYS)


__all__ = ["PROOF_CRITICAL_HASH_KEYS", "invalidation_patch", "proof_critical_hash_changed"]
