from __future__ import annotations

import unittest
from pathlib import Path

from math_auto_research.workflow.release_acceptance import evaluate_release_acceptance


class ReleaseAcceptanceSolverBackedTests(unittest.TestCase):
    def test_solver_backed_release_fields_and_blockers_are_present(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml"), run_commands=False)

        self.assertIn("solver_backed_proof_repair_status", report)
        self.assertIn("solver_backed_summary", report)
        self.assertEqual(set(str(index) for index in range(35, 48)) - set(report["checked_blockers"]), set())

    def test_solver_backed_blockers_gate_solver_claim(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml"), run_commands=False)

        self.assertIn("V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY", report["blocked_claims"])
        self.assertIn(
            report["claim_ceiling"],
            {
                "v0_3a_harness_ready_but_solver_backed_proof_repair_blocked",
                "release_acceptance_blocked_no_v0_3_completion_claim",
                "release_acceptance_failed_no_v0_3_completion_claim",
            },
        )


if __name__ == "__main__":
    unittest.main()
