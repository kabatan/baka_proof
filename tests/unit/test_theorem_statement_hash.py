from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from math_auto_research.lean_integration.final_verify_gate import FinalVerifyGate


LEAN_TEMPLATE = """theorem sample_target : True := by
-- PROOF-REGION-START:sample_target
  trivial
-- PROOF-REGION-END:sample_target
"""


class TheoremStatementHashRegressionTest(unittest.TestCase):
    def test_changed_statement_is_not_final_theorem(self) -> None:
        changed = LEAN_TEMPLATE.replace(": True", ": False")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "Sample.lean"
            path.write_text(changed, encoding="utf-8")
            report = FinalVerifyGate().verify_file(LEAN_TEMPLATE, path, "sample_target", "o:sample")
            self.assertFalse(report.protected_theorem_hash_unchanged)
            self.assertEqual(report.proof_use_status, "not_allowed")


if __name__ == "__main__":
    unittest.main()
