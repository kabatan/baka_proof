from __future__ import annotations

import unittest

from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider
from tests.unit.test_tonggeometry_adapter import claim_spec_fixture, request_for


class HeavySearchNoOrphansRegressionTest(unittest.TestCase):
    def test_plan_filter_heavy_search_no_orphans(self) -> None:
        run = CompositeSyntheticGeometryProvider().run(
            request_for(
                "heavy",
                {
                    "construction_needed": False,
                    "explicit_escalation": True,
                    "heavy_search_requested": True,
                    "claim_spec": claim_spec_fixture(),
                    "heavy_search_timeout_sec": 0.001,
                    "heavy_search_hard_timeout_sec": 1.0,
                    "heavy_search_sleep_sec": 5.0,
                },
            )
        )
        report = run.resource_usage_reports[-1]
        self.assertEqual(report["engine_role"], "heavy_search")
        self.assertEqual(report["admission_status"], "timeout")
        self.assertEqual(report["exit_status"], "killed")
        self.assertTrue(report["orphan_check_passed"])
        self.assertGreaterEqual(report["heartbeat_count"], 1)
