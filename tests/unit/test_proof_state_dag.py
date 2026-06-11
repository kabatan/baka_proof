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
                        final_verify_ref="sha256:final_verify",
                        protected_theorem_hash_unchanged=True,
                    ),
                ),
            )
        )
        self.assertTrue(StateReader(dag).is_closed("o:target"))

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
                        proof_use_status="diagnostic_only",
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
                        final_verify_ref="sha256:final_verify",
                        protected_theorem_hash_unchanged=True,
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
                            final_verify_ref="sha256:final_a",
                            protected_theorem_hash_unchanged=True,
                        ),
                        Derivation(
                            "d:b",
                            "o:b",
                            "final_verify_gate",
                            ("e:1",),
                            required_side_condition_ids=("o:a",),
                            proof_use_status="final_theorem",
                            final_verify_ref="sha256:final_b",
                            protected_theorem_hash_unchanged=True,
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
                        final_verify_ref="sha256:final",
                        protected_theorem_hash_unchanged=True,
                    ),
                ),
            )
        )
        writer.commit(GraphPatch(patch_id="p2", invalidate_obligation_ids=("o:target",)))
        summary = StateReader(dag).summary()
        self.assertEqual(summary["closed_obligation_ids"], [])
        self.assertEqual(summary["open_obligation_ids"], ["o:target"])


if __name__ == "__main__":
    unittest.main()
