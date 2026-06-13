from __future__ import annotations

import unittest

from math_auto_research.proof_state import DAGWriter, EvidenceRef, GraphPatch, Obligation, ProofStateDAG


class DagRawLogNotNodeTest(unittest.TestCase):
    def test_raw_log_is_only_an_evidence_ref_payload_pointer(self) -> None:
        dag = ProofStateDAG()
        DAGWriter(dag).commit(
            GraphPatch(
                patch_id="p1",
                obligations=(Obligation("o:target", "sha256:target"),),
                evidence_refs=(
                    EvidenceRef(
                        evidence_id="e:raw-log",
                        artifact_ref="sha256:raw-log",
                        evidence_status="diagnostic_only",
                        media_type="text/plain",
                        content_hash="sha256:raw-log",
                        artifact_kind="raw_log",
                    ),
                ),
            )
        )
        self.assertEqual(set(dag.obligations), {"o:target"})
        self.assertEqual(set(dag.evidence_refs), {"e:raw-log"})
        self.assertEqual(dag.derivations, {})
        self.assertFalse(hasattr(next(iter(dag.evidence_refs.values())), "raw_content"))


if __name__ == "__main__":
    unittest.main()
