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
        self.assertIn("started_at", report)
        self.assertIn("ended_at", report)

    def test_probe_local_resources(self) -> None:
        profile = probe_local_resources()
        self.assertEqual(profile["schema_version"], "1.0.0")
        self.assertGreaterEqual(profile["cpu_logical_cores"], 1)
        self.assertIn("heavy_search", profile["provider_engine_availability"])

    def test_heavy_search_is_exclusive_but_lean_is_not_starved(self) -> None:
        governor = ResourceGovernor()
        heavy = ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="heavy")
        second_heavy = ResourceRequest(component="provider_engine", engine_role="heavy_search", budget="heavy")
        lean = ResourceRequest(component="final_verify", engine_role="lean", budget="tiny")

        with governor.admit(heavy):
            with self.assertRaises(ResourceRejected):
                with governor.admit(second_heavy):
                    pass
            with governor.admit(lean) as admitted:
                self.assertEqual(admitted.engine_role, "lean")


if __name__ == "__main__":
    unittest.main()
