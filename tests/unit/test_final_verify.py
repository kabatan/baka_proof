from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.base.final_verify import FinalVerifyGate, ProofRegionGuard, contains_sorry


LEAN_TEMPLATE = """theorem sample_target : True := by
-- PROOF-REGION-START:sample_target
  trivial
-- PROOF-REGION-END:sample_target
"""


class FinalVerifyGateTest(unittest.TestCase):
    def test_final_verify_accepts_clean_lean_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(LEAN_TEMPLATE, encoding="utf-8")
            report = FinalVerifyGate().verify_file(LEAN_TEMPLATE, path, "sample_target", "o:sample")
            self.assertEqual(report.lean_status, "passed")
            self.assertTrue(report.protected_theorem_hash_unchanged)
            self.assertEqual(report.sorry_status, "clean")
            self.assertEqual(report.proof_use_status, "final_theorem")

    def test_changed_theorem_statement_is_rejected(self) -> None:
        changed = LEAN_TEMPLATE.replace(": True", ": False")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(changed, encoding="utf-8")
            report = FinalVerifyGate().verify_file(LEAN_TEMPLATE, path, "sample_target", "o:sample")
            self.assertFalse(report.protected_theorem_hash_unchanged)
            self.assertEqual(report.proof_use_status, "not_allowed")

    def test_proof_region_guard_rejects_outside_edits(self) -> None:
        candidate = LEAN_TEMPLATE + "\ntheorem extra : True := by trivial\n"
        self.assertFalse(ProofRegionGuard().permits(LEAN_TEMPLATE, candidate))

    def test_sorry_is_detected(self) -> None:
        self.assertTrue(contains_sorry("theorem bad : True := by\n  sorry\n"))

    def test_unadmitted_import_is_rejected(self) -> None:
        candidate = "import Other.Target\n" + LEAN_TEMPLATE
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(candidate, encoding="utf-8")
            report = FinalVerifyGate().verify_file(LEAN_TEMPLATE, path, "sample_target", "o:sample")
            self.assertEqual(report.proof_use_status, "not_allowed")

    def test_toy_target_is_rejected(self) -> None:
        candidate = LEAN_TEMPLATE + "\n-- ToyGeometry\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(candidate, encoding="utf-8")
            report = FinalVerifyGate().verify_file(LEAN_TEMPLATE, path, "sample_target", "o:sample")
            self.assertEqual(report.proof_use_status, "not_allowed")

    def test_incomplete_proof_use_provenance_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(LEAN_TEMPLATE, encoding="utf-8")
            report = FinalVerifyGate().verify_file(
                LEAN_TEMPLATE,
                path,
                "sample_target",
                "o:sample",
                proof_use_provenance={"goal_anchor_ref": "sha256:goal"},
            )
            self.assertEqual(report.proof_use_status, "not_allowed")


if __name__ == "__main__":
    unittest.main()
