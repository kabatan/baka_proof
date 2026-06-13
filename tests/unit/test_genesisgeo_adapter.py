from __future__ import annotations

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from plugins.geometry_synthetic.facade import GeometrySolveRequest
from plugins.geometry_synthetic.provider import CompositeSyntheticGeometryProviderV1
from plugins.geometry_synthetic.providers.genesisgeo_adapter import (
    GenesisGeoCompatibleConstructionProposerAdapter,
    normalize_genesisgeo_candidate,
)
from scripts.run_genesisgeo_probe import build_report


def claim_spec_fixture() -> dict:
    return {
        "schema_version": "1.0.0",
        "claim_id": "geometry_claim:genesisgeo_adapter",
        "target_library": "LeanGeoSubsetV1:1.0.0",
        "objects": ["A:Point", "B:Point", "C:Point"],
        "hypotheses": ["collinear"],
        "target": {"form": "collinear", "raw": "Coll A B C"},
        "nondegeneracy_assumptions": [],
        "orientation_assumptions": [],
        "source_goal_ref": "lean-check:genesisgeo-adapter",
    }


def request_for(constraints: dict) -> GeometrySolveRequest:
    return GeometrySolveRequest(
        schema_version="1.0.0",
        request_id="geometry_request:genesisgeo_adapter",
        claim_spec_ref="sha256:claim",
        intent="prove_or_diagnose",
        trust_target="final_theorem",
        budget="medium",
        constraints=constraints,
        resource_budget_ref="sha256:resource_budget",
    )


class GenesisGeoAdapterTest(unittest.TestCase):
    def test_plan_path_genesisgeo_adapter_exports_real_adapter_and_normalizer(self) -> None:
        adapter = GenesisGeoCompatibleConstructionProposerAdapter()
        self.assertEqual(adapter.engine_family, "genesisgeo_compatible")
        with tempfile.NamedTemporaryFile() as checkpoint:
            with patch.dict(os.environ, {"GENESISGEO_MODEL_PATH": checkpoint.name}, clear=False):
                report = build_report("geometry_request:genesisgeo_normalize", claim_spec_fixture())
        if report["candidate"] is None:
            self.skipTest(f"GenesisGeo runtime diagnostic blockers: {report['blocker_reasons']}")
        candidate = normalize_genesisgeo_candidate(report["candidate"])
        self.assertEqual(candidate.schema_version, "1.0.0")
        self.assertTrue(candidate.candidate_id.startswith("aux_construction_candidate:"))
        self.assertEqual(candidate.proof_use_status, "not_allowed")

    def test_real_genesisgeo_diagnostic_or_candidate_is_not_proof_use(self) -> None:
        run = CompositeSyntheticGeometryProviderV1().run(
            request_for(
                {
                    "construction_needed": True,
                    "claim_spec": claim_spec_fixture(),
                    "use_real_genesisgeo": True,
                }
            )
        )
        self.assertEqual(run.result.proof_use_status, "not_allowed")
        self.assertIsNone(run.result.geotrace_ref)
        genesis_runs = [
            engine_run for engine_run in run.manifest.engine_runs if engine_run["engine_role"] == "construction_proposer"
        ]
        self.assertEqual(len(genesis_runs), 1)
        self.assertFalse(genesis_runs[0]["fixture_flag"])
        self.assertTrue(genesis_runs[0]["real_integration_flag"])
        genesis_reports = [
            report for report in run.resource_usage_reports if report["engine_role"] == "construction_proposer"
        ]
        self.assertEqual(genesis_reports[0]["logs_ref"], "external_genesisgeo_stdout")
        if run.result.construction_candidate_refs:
            self.assertTrue(run.result.construction_candidate_refs[0].startswith("aux_construction_candidate:"))
        else:
            self.assertTrue(any("genesisgeo_real" in ref for ref in run.result.diagnostic_refs))

    def test_genesis_output_not_proof(self) -> None:
        report = build_report("geometry_request:genesisgeo_raw_not_proof", claim_spec_fixture())
        raw = json.dumps(report, sort_keys=True)
        self.assertIn("raw_rationale", report)
        self.assertEqual(report["proof_use_status"], "not_allowed")
        self.assertNotIn('"proof_use_status": "final_theorem"', raw)


if __name__ == "__main__":
    unittest.main()
