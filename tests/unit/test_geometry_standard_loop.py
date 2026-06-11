from __future__ import annotations

import unittest

from plugins.geometry_synthetic.standard_loop import StandardGeometryProofLoop


class GeometryStandardLoopTest(unittest.TestCase):
    def test_standard_loop_closes_target_only_after_final_verify(self) -> None:
        result = StandardGeometryProofLoop().run_fixture()
        self.assertIn("obligation:sample_target", result.dag_summary["closed_obligation_ids"])
        self.assertEqual(result.final_verify_report["proof_use_status"], "final_theorem")
        self.assertEqual(result.provider_result["status"], "partial")
        self.assertTrue(result.provider_result["geotrace_ref"].startswith("geotrace:"))
        self.assertEqual(result.stage_statuses["dag_final_patch"], "committed")
        self.assertTrue(result.worker_result["final_verify_ref"].startswith("final_verify:"))

    def test_unsupported_trace_returns_blocker_and_keeps_obligation_open(self) -> None:
        result = StandardGeometryProofLoop().run_fixture(trace_rule_id="rule:unsupported_fixture:v1")
        self.assertEqual(result.stage_statuses["trace_compilation"], "blocked")
        self.assertIn("obligation:sample_target", result.dag_summary["open_obligation_ids"])
        self.assertIn("unsupported_rule:rule:unsupported_fixture:v1", result.blockers)
        self.assertIsNone(result.final_verify_report)

    def test_worker_success_claim_without_final_verify_does_not_close(self) -> None:
        result = StandardGeometryProofLoop().run_fixture(run_final_verify=False, worker_status="success_claimed")
        self.assertEqual(result.stage_statuses["final_verify"], "not_run")
        self.assertIn("raw_output_not_proof", result.blockers)
        self.assertIn("obligation:sample_target", result.dag_summary["open_obligation_ids"])

    def test_controller_feedback_is_structured(self) -> None:
        result = StandardGeometryProofLoop().run_fixture()
        feedback = result.feedback_to_controller
        self.assertEqual(feedback["schema_version"], "1.0.0")
        self.assertEqual(feedback["status"], "closed")
        self.assertIn("stage_statuses", feedback)
        self.assertIn("proof_use_note", feedback)


if __name__ == "__main__":
    unittest.main()
