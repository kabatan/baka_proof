from __future__ import annotations

import json
import unittest

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProvider, CompositeSyntheticGeometryProviderV1
from plugins.geometry_synthetic.providers.tonggeometry_adapter import (
    TongGeometryCompatibleHeavySearchAdapter,
    normalize_tonggeometry_output,
)
from scripts.run_tonggeometry_probe import build_report


def claim_spec_fixture() -> dict:
    return {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:tonggeometry_adapter",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:tonggeometry-adapter",
    }


def request_for(budget: str, constraints: dict) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id=f"geometry_request:tonggeometry_adapter:{budget}",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget=budget,
        constraints=constraints,
        resource_budget_ref="sha256:resource_budget",
    )


class TongGeometryAdapterTest(unittest.TestCase):
    def test_plan_path_tonggeometry_adapter_exports_real_adapter_and_normalizer(self) -> None:
        adapter = TongGeometryCompatibleHeavySearchAdapter()
        self.assertEqual(adapter.engine_family, "tonggeometry_compatible")
        self.assertIsNone(normalize_tonggeometry_output({"search_result_ref": None}))
        self.assertEqual(
            normalize_tonggeometry_output({"search_result_ref": "geotrace:request:heavy_search:tong"}),
            "geotrace:request:heavy_search:tong",
        )

    def test_heavy_search_budget_gate(self) -> None:
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
        self.assertEqual(heavy.resource_usage_reports[-1]["engine_role"], "heavy_search")
        self.assertEqual(heavy.resource_usage_reports[-1]["role"], "heavy_search")
        self.assertFalse(heavy.manifest.engine_runs[-1]["fixture_flag"])
        self.assertTrue(heavy.manifest.engine_runs[-1]["real_integration_flag"])
        self.assertEqual(heavy.result.proof_use_status, "not_allowed")

    def test_heavy_search_no_orphans(self) -> None:
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
        self.assertEqual(run.result.proof_use_status, "not_allowed")

    def test_tonggeometry_raw_output_not_proof(self) -> None:
        report = build_report("geometry_request:tong_raw_not_proof", claim_spec_fixture())
        raw = json.dumps(report, sort_keys=True)
        self.assertIn("raw_search_output", report)
        self.assertEqual(report["proof_use_status"], "not_allowed")
        self.assertNotIn('"proof_use_status": "final_theorem"', raw)


if __name__ == "__main__":
    unittest.main()
