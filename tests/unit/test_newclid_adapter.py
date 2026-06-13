from __future__ import annotations

import shutil
import unittest

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProviderV1
from plugins.geometry_synthetic.providers.newclid_adapter import (
    NewclidCompatibleSymbolicClosureAdapter,
    convert_claim_spec_to_newclid_fixture,
    convert_claim_spec_to_newclid_jgex,
)


def claim_spec_fixture() -> dict:
    return {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:newclid_adapter",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:newclid-adapter",
    }


def request_for(constraints: dict) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_request:newclid_adapter",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget="small",
        constraints=constraints,
        resource_budget_ref="sha256:resource_budget",
    )


class NewclidAdapterTest(unittest.TestCase):
    def test_plan_path_newclid_adapter_exports_real_adapter_and_conversion(self) -> None:
        adapter = NewclidCompatibleSymbolicClosureAdapter()
        self.assertEqual(adapter.engine_family, "newclid_compatible")
        fixture_input = convert_claim_spec_to_newclid_fixture(claim_spec_fixture())
        self.assertEqual(fixture_input["target"], "collinear")
        real_input = convert_claim_spec_to_newclid_jgex(claim_spec_fixture())
        self.assertEqual(real_input["status"], "supported")
        self.assertIn("coll", real_input["jgex_problem"])

    def test_unsupported_claim_returns_blocker_diagnostic(self) -> None:
        unsupported = claim_spec_fixture()
        unsupported["target"] = {"form": "parallel", "raw": "Parallel l m"}
        run = CompositeSyntheticGeometryProviderV1().run(
            request_for(
                {
                    "construction_needed": False,
                    "claim_spec": unsupported,
                    "use_real_newclid": True,
                }
            )
        )
        self.assertEqual(run.result.status, "unsupported")
        self.assertIsNone(run.result.geotrace_ref)
        self.assertIn("newclid_translation_unsupported", run.result.diagnostic_refs[0])
        self.assertFalse(run.manifest.fixture_flag)
        self.assertTrue(run.manifest.real_integration_flag)
        self.assertEqual(run.resource_usage_reports[0]["admission_status"], "admitted")

    @unittest.skipUnless(shutil.which("newclid") and shutil.which("yuclid"), "Newclid/Yuclid CLI unavailable")
    def test_real_newclid_output_normalizes_to_geotrace_manifest_and_resource_report(self) -> None:
        run = CompositeSyntheticGeometryProviderV1().run(
            request_for(
                {
                    "construction_needed": False,
                    "claim_spec": claim_spec_fixture(),
                    "use_real_newclid": True,
                }
            )
        )
        self.assertEqual(run.result.status, "partial")
        self.assertEqual(run.result.proof_use_status, "not_allowed")
        self.assertTrue(run.result.geotrace_ref.startswith("geotrace:"))
        self.assertFalse(run.manifest.fixture_flag)
        self.assertTrue(run.manifest.real_integration_flag)
        self.assertEqual(run.manifest.unsupported_rule_count, 0)
        self.assertEqual(len(run.manifest.engine_runs), 1)
        engine_run = run.manifest.engine_runs[0]
        self.assertEqual(engine_run["engine_role"], "symbolic_closure")
        self.assertEqual(engine_run["engine_family"], "newclid_compatible")
        self.assertIn("newclid==", engine_run["engine_version"])
        self.assertFalse(engine_run["fixture_flag"])
        self.assertTrue(engine_run["real_integration_flag"])
        self.assertEqual(len(run.resource_usage_reports), 1)
        self.assertEqual(run.resource_usage_reports[0]["logs_ref"], "external_newclid_stdout")


if __name__ == "__main__":
    unittest.main()
