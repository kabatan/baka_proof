from __future__ import annotations

import unittest

from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProviderV1
from tests.unit.test_tonggeometry_adapter import claim_spec_fixture, request_for


class HeavySearchBudgetGateRegressionTest(unittest.TestCase):
    def test_plan_filter_heavy_search_budget_gate(self) -> None:
        constraints = {
            "construction_needed": False,
            "explicit_escalation": True,
            "heavy_search_requested": True,
            "claim_spec": claim_spec_fixture(),
            "use_real_tonggeometry": True,
        }
        medium = CompositeSyntheticGeometryProviderV1().run(request_for("medium", constraints))
        self.assertNotIn("heavy_search", [run["engine_role"] for run in medium.manifest.engine_runs])

        heavy = CompositeSyntheticGeometryProviderV1().run(request_for("heavy", constraints))
        self.assertEqual(heavy.manifest.engine_runs[-1]["engine_role"], "heavy_search")
        self.assertFalse(heavy.manifest.engine_runs[-1]["fixture_flag"])
        self.assertTrue(heavy.manifest.engine_runs[-1]["real_integration_flag"])
