from __future__ import annotations

import unittest

from math_auto_research.proof_state import (
    DAGWriter,
    Derivation,
    EvidenceRef,
    GraphPatch,
    Obligation,
    ProofStateDAG,
    StateReader,
)
from math_auto_research.proof_state.dag import DAGValidationError


class ProofStateDAGTest(unittest.TestCase):
    def test_final_theorem_derivation_closes_obligation(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="p1",
                obligations=(Obligation("o:target", "sha256:target"),),
                evidence_refs=(
                    EvidenceRef(
                        "e:final",
                        "sha256:artifact",
                        "used_in_final_proof",
                        "application/json",
                        "sha256:content",
                    ),
                ),
                derivations=(
                    Derivation(
                        "d:final",
                        "o:target",
                        "final_verify_gate",
                        ("e:final",),
                        proof_use_status="final_theorem",
                        final_verify_ref="final_verify:ok",
                        protected_theorem_hash_unchanged=True,
                        final_verify_report=_final_report("final_verify:ok", "o:target"),
                    ),
                ),
            )
        )
        self.assertTrue(StateReader(dag).is_closed("o:target"))
        self.assertIn("o:target", StateReader(dag).snapshot().obligation_ids)

    def test_forged_final_verify_ref_is_rejected(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p1",
                    obligations=(Obligation("o:target", "sha256:target"),),
                    evidence_refs=(
                        EvidenceRef("e:final", "sha256:artifact", "used_in_final_proof", "application/json", "sha256:c"),
                    ),
                    derivations=(
                        Derivation(
                            "d:final",
                            "o:target",
                            "final_verify_gate",
                            ("e:final",),
                            proof_use_status="final_theorem",
                            final_verify_ref="sha256:forged",
                            protected_theorem_hash_unchanged=True,
                        ),
                    ),
                )
            )

    def test_raw_or_diagnostic_derivation_cannot_close(self) -> None:
        dag = ProofStateDAG()
        DAGWriter(dag).commit(
            GraphPatch(
                patch_id="p1",
                obligations=(Obligation("o:target", "sha256:target"),),
                evidence_refs=(
                    EvidenceRef(
                        "e:diagnostic",
                        "sha256:artifact",
                        "diagnostic_only",
                        "text/plain",
                        "sha256:content",
                    ),
                ),
                derivations=(
                    Derivation(
                        "d:diagnostic",
                        "o:target",
                        "provider_result",
                        ("e:diagnostic",),
                        proof_use_status="not_allowed",
                    ),
                ),
            )
        )
        self.assertFalse(StateReader(dag).is_closed("o:target"))

    def test_side_conditions_must_be_closed(self) -> None:
        dag = ProofStateDAG()
        DAGWriter(dag).commit(
            GraphPatch(
                patch_id="p1",
                obligations=(
                    Obligation("o:target", "sha256:target"),
                    Obligation("o:side", "sha256:side"),
                ),
                evidence_refs=(
                    EvidenceRef(
                        "e:final",
                        "sha256:artifact",
                        "used_in_final_proof",
                        "application/json",
                        "sha256:content",
                    ),
                ),
                derivations=(
                    Derivation(
                        "d:target",
                        "o:target",
                        "final_verify_gate",
                        ("e:final",),
                        required_side_condition_ids=("o:side",),
                        proof_use_status="final_theorem",
                        final_verify_ref="final_verify:side",
                        protected_theorem_hash_unchanged=True,
                        final_verify_report=_final_report("final_verify:side", "o:target"),
                    ),
                ),
            )
        )
        self.assertFalse(StateReader(dag).is_closed("o:target"))

    def test_graph_patch_validates_references_and_cycles(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="p1",
                obligations=(
                    Obligation("o:a", "sha256:a"),
                    Obligation("o:b", "sha256:b"),
                ),
                evidence_refs=(
                    EvidenceRef("e:1", "sha256:artifact", "used_in_final_proof", "application/json", "sha256:c"),
                ),
            )
        )
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p2",
                    derivations=(
                        Derivation(
                            "d:a",
                            "o:a",
                            "final_verify_gate",
                            ("e:1",),
                            required_side_condition_ids=("o:b",),
                            proof_use_status="final_theorem",
                            final_verify_ref="final_verify:a",
                            protected_theorem_hash_unchanged=True,
                            final_verify_report=_final_report("final_verify:a", "o:a"),
                        ),
                        Derivation(
                            "d:b",
                            "o:b",
                            "final_verify_gate",
                            ("e:1",),
                            required_side_condition_ids=("o:a",),
                            proof_use_status="final_theorem",
                            final_verify_ref="final_verify:b",
                            protected_theorem_hash_unchanged=True,
                            final_verify_report=_final_report("final_verify:b", "o:b"),
                        ),
                    ),
                )
            )

    def test_invalidation_reopens_obligation_summary(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        writer.commit(
            GraphPatch(
                patch_id="p1",
                obligations=(Obligation("o:target", "sha256:target"),),
                evidence_refs=(
                    EvidenceRef("e:1", "sha256:artifact", "used_in_final_proof", "application/json", "sha256:c"),
                ),
                derivations=(
                    Derivation(
                        "d:target",
                        "o:target",
                        "final_verify_gate",
                        ("e:1",),
                        proof_use_status="final_theorem",
                        final_verify_ref="final_verify:target",
                        protected_theorem_hash_unchanged=True,
                        final_verify_report=_final_report("final_verify:target", "o:target"),
                    ),
                ),
            )
        )
        writer.commit(GraphPatch(patch_id="p2", invalidate_obligation_ids=("o:target",)))
        summary = StateReader(dag).summary()
        self.assertEqual(summary["closed_obligation_ids"], [])
        self.assertEqual(summary["open_obligation_ids"], ["o:target"])

    def test_final_theorem_rejects_raw_log_evidence(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p1",
                    obligations=(Obligation("o:target", "sha256:target"),),
                    evidence_refs=(
                        EvidenceRef(
                            "e:raw",
                            "sha256:raw",
                            "used_in_final_proof",
                            "text/plain",
                            "sha256:raw",
                            artifact_kind="raw_log",
                        ),
                    ),
                    derivations=(
                        Derivation(
                            "d:final",
                            "o:target",
                            "final_verify_gate",
                            ("e:raw",),
                            proof_use_status="final_theorem",
                            final_verify_ref="final_verify:target",
                            protected_theorem_hash_unchanged=True,
                            final_verify_report=_final_report("final_verify:target", "o:target"),
                        ),
                    ),
                )
            )

    def test_unknown_rule_id_is_rejected(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p1",
                    obligations=(Obligation("o:target", "sha256:target"),),
                    evidence_refs=(
                        EvidenceRef("e:1", "sha256:artifact", "diagnostic_only", "text/plain", "sha256:c"),
                    ),
                    derivations=(
                        Derivation(
                            "d:unknown",
                            "o:target",
                            "unadmitted_rule",
                            ("e:1",),
                            proof_use_status="not_allowed",
                        ),
                    ),
                )
            )

    def test_evidence_status_must_match_rule(self) -> None:
        dag = ProofStateDAG()
        writer = DAGWriter(dag)
        with self.assertRaises(DAGValidationError):
            writer.commit(
                GraphPatch(
                    patch_id="p1",
                    obligations=(Obligation("o:target", "sha256:target"),),
                    evidence_refs=(
                        EvidenceRef("e:1", "sha256:artifact", "used_in_final_proof", "text/plain", "sha256:c"),
                    ),
                    derivations=(
                        Derivation(
                            "d:bad-evidence",
                            "o:target",
                            "provider_result",
                            ("e:1",),
                            proof_use_status="not_allowed",
                        ),
                    ),
                )
            )

    def test_base_owned_payload_mutation_flag_is_rejected(self) -> None:
        dag = ProofStateDAG()
        with self.assertRaises(DAGValidationError):
            DAGWriter(dag).commit(
                GraphPatch(
                    patch_id="p1",
                    metadata={"mutates_base_owned_payload": True},
                )
            )


def _final_report(report_id: str, target_obligation_id: str) -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "report_id": report_id,
        "target_obligation_id": target_obligation_id,
        "theorem_statement_hash": "sha256:target",
        "protected_theorem_hash_unchanged": True,
        "lean_status": "passed",
        "forbidden_axiom_status": "clean",
        "sorry_status": "clean",
        "proof_use_status": "final_theorem",
    }


if __name__ == "__main__":
    unittest.main()
