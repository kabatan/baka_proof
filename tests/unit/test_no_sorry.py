from __future__ import annotations

import unittest

from math_auto_research.lean_integration.final_verify_gate import contains_sorry


class NoSorryRegressionTest(unittest.TestCase):
    def test_sorry_token_is_detected(self) -> None:
        self.assertTrue(contains_sorry("theorem bad : True := by\n  sorry\n"))


if __name__ == "__main__":
    unittest.main()
