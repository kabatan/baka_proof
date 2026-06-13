from __future__ import annotations

import sys
import unittest

from math_auto_research.base.resources.local_resource_profile import probe_local_resources
from math_auto_research.base.resources.process_runner import run_guarded_process
from math_auto_research.base.resources.resource_budget import ResourceRejected, ResourceRequest
from math_auto_research.base.resources.resource_governor import ResourceGovernor


class ResourceGovernorTest(unittest.TestCase):
    def test_rejects_heavy_search_under_medium_budget(self) -> None:
        governor = ResourceGovernor()
        request = ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="medium")
        with self.assertRaises(ResourceRejected):
            with governor.admit(request):
                pass

    def test_runs_guarded_process(self) -> None:
        governor = ResourceGovernor()
        request = ResourceRequest(component="checker", engine_role="none", budget="tiny", timeout_sec=10)
        report = run_guarded_process([sys.executable, "-c", "print('ok')"], request, governor)
        self.assertEqual(report["role"], "checker")
        self.assertEqual(report["admission_status"], "admitted")
        self.assertEqual(report["exit_status"], "completed")
        self.assertEqual(report["timeout_status"], "none")
        self.assertGreaterEqual(report["heartbeat_count"], 1)
        self.assertIn("started_at", report)
        self.assertIn("ended_at", report)

    def test_guarded_process_reports_failure(self) -> None:
        governor = ResourceGovernor()
        request = ResourceRequest(component="checker", engine_role="none", budget="tiny", timeout_sec=10)
        report = run_guarded_process([sys.executable, "-c", "import sys; sys.exit(7)"], request, governor)
        self.assertEqual(report["exit_status"], "failed")
        self.assertEqual(report["timeout_status"], "none")

    def test_guarded_process_timeout_kills_process_group(self) -> None:
        governor = ResourceGovernor()
        request = ResourceRequest(component="checker", engine_role="none", budget="tiny", timeout_sec=0.05)
        report = run_guarded_process([sys.executable, "-c", "import time; time.sleep(5)"], request, governor)
        self.assertEqual(report["exit_status"], "killed")
        self.assertIn(report["timeout_status"], {"soft_terminated_no_orphan", "hard_killed"})
        self.assertTrue(report["orphan_check_passed"])
        self.assertGreaterEqual(report["heartbeat_count"], 1)

    def test_probe_local_resources(self) -> None:
        profile = probe_local_resources()
        self.assertEqual(profile["schema_version"], "1.0.0")
        self.assertGreaterEqual(profile["cpu_logical_cores"], 1)
        self.assertIn("heavy_search", profile["provider_engine_availability"])

    def test_heavy_search_is_exclusive_but_lean_is_not_starved(self) -> None:
        governor = ResourceGovernor()
        heavy = ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="heavy")
        second_heavy = ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="heavy")
        lean = ResourceRequest(component="final_verify", engine_role="final_verify", budget="tiny")

        with governor.admit(heavy):
            with self.assertRaises(ResourceRejected):
                with governor.admit(second_heavy):
                    pass
            with governor.admit(lean) as admitted:
                self.assertEqual(admitted.engine_role, "final_verify")

    def test_scheduler_prioritizes_lean_ahead_of_queued_heavy_search(self) -> None:
        governor = ResourceGovernor()
        queued = [
            ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="heavy"),
            ResourceRequest(component="lean_build", engine_role="lean_build", budget="tiny"),
            ResourceRequest(component="final_verify", engine_role="final_verify", budget="tiny"),
            ResourceRequest(component="provider_engine", engine_role="construction_proposer", budget="medium"),
            ResourceRequest(component="worker", engine_role="proof_worker", budget="medium"),
            ResourceRequest(component="closure", engine_role="symbolic_closure", budget="medium"),
        ]
        ordered = governor.priority_order(queued)
        self.assertEqual(
            [request.engine_role for request in ordered],
            ["final_verify", "lean_build", "proof_worker", "symbolic_closure", "construction_proposer", "heavy_search"],
        )


if __name__ == "__main__":
    unittest.main()
