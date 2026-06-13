from __future__ import annotations

import unittest

from math_auto_research.base.trust import TrustGuard


class TrustGuardTest(unittest.TestCase):
    def test_raw_provider_output_is_not_proof(self) -> None:
        report = TrustGuard().reject_raw_source("provider_output")
        self.assertEqual(report.result_level, "raw_candidate")
        self.assertEqual(report.proof_use_status, "not_allowed")

    def test_patch_candidate_is_not_final_theorem(self) -> None:
        report = TrustGuard().lean_patch_candidate("compiled_patch_pending_final_verify")
        self.assertEqual(report.result_level, "lean_patch_candidate")
        self.assertEqual(report.proof_use_status, "claim_level_only")

    def test_final_theorem_requires_final_verify_ref(self) -> None:
        report = TrustGuard().final_theorem("final_verify:ok")
        self.assertEqual(report.result_level, "lean_theorem")
        self.assertEqual(report.proof_use_status, "final_theorem")
        self.assertEqual(report.final_verify_ref, "final_verify:ok")


if __name__ == "__main__":
    unittest.main()
