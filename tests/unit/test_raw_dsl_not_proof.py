from __future__ import annotations

import unittest

from tests.unit.test_geometry_bridge import GeometryBridgeGate, _accepted_extraction, _claim_spec, _target_goal


class RawDslNotProofRegressionTest(unittest.TestCase):
    def test_raw_dsl_not_proof(self) -> None:
        report = GeometryBridgeGate().evaluate(
            target_goal=_target_goal(),
            extraction_report=_accepted_extraction("exact"),
            claim_spec=_claim_spec(),
            source_result_ref="provider:raw",
            generated_patch_target="sample_target",
            source_origin="raw_dsl",
            trace_compilation_status="lean_patch_candidate",
        )
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIn("raw_dsl_origin", report.blockers)


if __name__ == "__main__":
    unittest.main()
