from __future__ import annotations

import unittest

from plugins.geometry_synthetic.bridge import TrustGuard


class RawProviderNotProofRegressionTest(unittest.TestCase):
    def test_raw_provider_not_proof(self) -> None:
        decision = TrustGuard().classify(evidence_kind="raw_provider_output", requested_result_level="final_theorem")
        self.assertEqual(decision.proof_use_status, "not_allowed")
        self.assertFalse(decision.allowed_for_goal_closure)
        self.assertEqual(decision.reason, "raw_output_not_proof")


if __name__ == "__main__":
    unittest.main()
