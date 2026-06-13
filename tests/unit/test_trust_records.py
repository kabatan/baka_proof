from __future__ import annotations

import unittest

from pydantic import ValidationError

from math_auto_research.base.diagnostics import TrustReport


class TrustRecordsTest(unittest.TestCase):
    def test_trust_report_keeps_non_final_artifacts_out_of_proof_use(self) -> None:
        report = TrustReport(
            result_level="raw_candidate",
            proof_use_status="not_allowed",
            reason="raw_provider_output",
        )
        self.assertEqual(report.model_dump(mode="json")["proof_use_status"], "not_allowed")

    def test_final_theorem_requires_lean_theorem_result_level(self) -> None:
        with self.assertRaises(ValidationError):
            TrustReport(
                result_level="lean_patch_candidate",
                proof_use_status="final_theorem",
                reason="not_final_verified",
            )

    def test_final_theorem_status_can_only_be_represented_with_lean_theorem(self) -> None:
        report = TrustReport(
            result_level="lean_theorem",
            proof_use_status="final_theorem",
            reason="final_verify_gate_passed",
            final_verify_ref="sha256:final",
        )
        self.assertEqual(report.proof_use_status, "final_theorem")


if __name__ == "__main__":
    unittest.main()
