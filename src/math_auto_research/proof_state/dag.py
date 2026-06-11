from __future__ import annotations

from dataclasses import replace
from typing import Any

from math_auto_research.proof_state.records import Derivation, EvidenceRef, GraphPatch, Obligation


class DAGValidationError(ValueError):
    pass


class ProofStateDAG:
    def __init__(self) -> None:
        self.obligations: dict[str, Obligation] = {}
        self.evidence_refs: dict[str, EvidenceRef] = {}
        self.derivations: dict[str, Derivation] = {}


class DAGWriter:
    def __init__(self, dag: ProofStateDAG) -> None:
        self.dag = dag

    def commit(self, patch: GraphPatch) -> None:
        self._validate_schema(patch)
        self._validate_unique_patch_ids(patch)
        next_obligations = dict(self.dag.obligations)
        next_evidence = dict(self.dag.evidence_refs)
        next_derivations = dict(self.dag.derivations)

        for obligation in patch.obligations:
            if obligation.obligation_id in next_obligations:
                raise DAGValidationError(f"duplicate obligation: {obligation.obligation_id}")
            next_obligations[obligation.obligation_id] = obligation

        for evidence in patch.evidence_refs:
            if evidence.evidence_id in next_evidence:
                raise DAGValidationError(f"duplicate evidence: {evidence.evidence_id}")
            next_evidence[evidence.evidence_id] = evidence

        for derivation in patch.derivations:
            if derivation.derivation_id in next_derivations:
                raise DAGValidationError(f"duplicate derivation: {derivation.derivation_id}")
            self._validate_derivation_refs(derivation, next_obligations, next_evidence)
            next_derivations[derivation.derivation_id] = derivation

        for obligation_id in patch.invalidate_obligation_ids:
            if obligation_id not in next_obligations:
                raise DAGValidationError(f"unknown invalidation obligation: {obligation_id}")
            next_obligations[obligation_id] = replace(next_obligations[obligation_id], status="invalidated")

        self._validate_acyclic(next_derivations)
        self.dag.obligations = next_obligations
        self.dag.evidence_refs = next_evidence
        self.dag.derivations = next_derivations

    def _validate_schema(self, patch: GraphPatch) -> None:
        if patch.schema_id != "proof_state.graph_patch.v1":
            raise DAGValidationError(f"unsupported graph patch schema: {patch.schema_id}")

    def _validate_unique_patch_ids(self, patch: GraphPatch) -> None:
        self._assert_unique("obligation", [item.obligation_id for item in patch.obligations])
        self._assert_unique("evidence", [item.evidence_id for item in patch.evidence_refs])
        self._assert_unique("derivation", [item.derivation_id for item in patch.derivations])

    def _assert_unique(self, label: str, values: list[str]) -> None:
        if len(values) != len(set(values)):
            raise DAGValidationError(f"duplicate {label} id in patch")

    def _validate_derivation_refs(
        self,
        derivation: Derivation,
        obligations: dict[str, Obligation],
        evidence_refs: dict[str, EvidenceRef],
    ) -> None:
        if derivation.conclusion_obligation_id not in obligations:
            raise DAGValidationError(f"unknown conclusion: {derivation.conclusion_obligation_id}")
        for obligation_id in derivation.required_side_condition_ids:
            if obligation_id not in obligations:
                raise DAGValidationError(f"unknown side condition: {obligation_id}")
        for evidence_id in derivation.evidence_refs:
            if evidence_id not in evidence_refs:
                raise DAGValidationError(f"unknown evidence: {evidence_id}")
        if derivation.proof_use_status == "final_theorem":
            self._validate_final_verify_report(derivation)

    def _validate_final_verify_report(self, derivation: Derivation) -> None:
        report = derivation.final_verify_report
        if not derivation.final_verify_ref:
            raise DAGValidationError("final_theorem derivation requires final_verify_ref")
        if not isinstance(report, dict):
            raise DAGValidationError("final_theorem derivation requires final_verify_report")
        if report.get("report_id") != derivation.final_verify_ref:
            raise DAGValidationError("final_verify_ref must match FinalVerifyReport.report_id")
        if report.get("target_obligation_id") != derivation.conclusion_obligation_id:
            raise DAGValidationError("FinalVerifyReport target obligation mismatch")
        if report.get("proof_use_status") != "final_theorem":
            raise DAGValidationError("FinalVerifyReport proof_use_status is not final_theorem")
        if report.get("lean_status") != "passed":
            raise DAGValidationError("FinalVerifyReport lean_status is not passed")
        if report.get("sorry_status") != "clean":
            raise DAGValidationError("FinalVerifyReport sorry_status is not clean")
        if report.get("forbidden_axiom_status") != "clean":
            raise DAGValidationError("FinalVerifyReport forbidden_axiom_status is not clean")
        if not report.get("protected_theorem_hash_unchanged"):
            raise DAGValidationError("FinalVerifyReport theorem hash changed")
        if not derivation.protected_theorem_hash_unchanged:
            raise DAGValidationError("final_theorem derivation requires unchanged theorem hash")

    def _validate_acyclic(self, derivations: dict[str, Derivation]) -> None:
        edges: dict[str, set[str]] = {}
        for derivation in derivations.values():
            edges.setdefault(derivation.conclusion_obligation_id, set()).update(
                derivation.required_side_condition_ids
            )

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(obligation_id: str) -> None:
            if obligation_id in visiting:
                raise DAGValidationError(f"cycle detected at obligation: {obligation_id}")
            if obligation_id in visited:
                return
            visiting.add(obligation_id)
            for dependency_id in edges.get(obligation_id, set()):
                visit(dependency_id)
            visiting.remove(obligation_id)
            visited.add(obligation_id)

        for obligation_id in edges:
            visit(obligation_id)


class StateReader:
    def __init__(self, dag: ProofStateDAG) -> None:
        self.dag = dag

    def is_closed(self, obligation_id: str) -> bool:
        obligation = self.dag.obligations.get(obligation_id)
        if obligation is None or obligation.status == "invalidated":
            return False
        for derivation in self._derivations_for(obligation_id):
            if self._derivation_closes(derivation, set()):
                return True
        return False

    def summary(self) -> dict[str, Any]:
        closed = [oid for oid in self.dag.obligations if self.is_closed(oid)]
        return {
            "obligation_count": len(self.dag.obligations),
            "derivation_count": len(self.dag.derivations),
            "evidence_ref_count": len(self.dag.evidence_refs),
            "closed_obligation_ids": sorted(closed),
            "open_obligation_ids": sorted(set(self.dag.obligations) - set(closed)),
        }

    def _derivations_for(self, obligation_id: str) -> list[Derivation]:
        return [
            derivation
            for derivation in self.dag.derivations.values()
            if derivation.conclusion_obligation_id == obligation_id
        ]

    def _derivation_closes(self, derivation: Derivation, path: set[str]) -> bool:
        if derivation.proof_use_status != "final_theorem":
            return False
        if not _final_verify_report_valid(derivation):
            return False
        conclusion = derivation.conclusion_obligation_id
        if conclusion in path:
            return False
        next_path = set(path)
        next_path.add(conclusion)
        for side_condition_id in derivation.required_side_condition_ids:
            if not self._obligation_closed_by_any(side_condition_id, next_path):
                return False
        return True

    def _obligation_closed_by_any(self, obligation_id: str, path: set[str]) -> bool:
        obligation = self.dag.obligations.get(obligation_id)
        if obligation is None or obligation.status == "invalidated":
            return False
        return any(self._derivation_closes(derivation, path) for derivation in self._derivations_for(obligation_id))


def _final_verify_report_valid(derivation: Derivation) -> bool:
    report = derivation.final_verify_report
    return (
        bool(derivation.final_verify_ref)
        and derivation.protected_theorem_hash_unchanged
        and isinstance(report, dict)
        and report.get("report_id") == derivation.final_verify_ref
        and report.get("target_obligation_id") == derivation.conclusion_obligation_id
        and report.get("proof_use_status") == "final_theorem"
        and report.get("lean_status") == "passed"
        and report.get("sorry_status") == "clean"
        and report.get("forbidden_axiom_status") == "clean"
        and bool(report.get("protected_theorem_hash_unchanged"))
    )
