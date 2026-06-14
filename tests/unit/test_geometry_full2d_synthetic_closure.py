from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext
from plugins.geometry_full2d.engines.synthetic_closure import run
from scripts.extract_geometry_full2d_statement import extract_statement
from scripts.smoke_full2d_engine import run_smoke


class GeometryFull2DSyntheticClosureTest(unittest.TestCase):
    def test_synthetic_closure_smoke_passes(self) -> None:
        self.assertEqual(run_smoke("synthetic_closure"), [])

    def test_collinear_reflexive_goal_normalizes_to_trace(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="synthetic_closure_unit",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim.to_dict(),
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:synthetic_closure_unit",
                request_id="synthetic_closure_unit",
                resource_usage_ref="resource_usage:synthetic_closure_unit",
            ),
        )
        self.assertEqual(output.status, "normalized_success")
        self.assertTrue(output.real_integration_flag)
        self.assertFalse(output.fixture_flag)
        self.assertTrue(output.normalized_output_ref)
        self.assertTrue(output.raw_output_hash.startswith("sha256:"))

    def test_missing_claim_spec_is_measured_failure(self) -> None:
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="synthetic_closure_missing",
                claim_spec_ref="sha256:" + "0" * 64,
                target_library="GeometryFull2DTarget:1.0.0",
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:synthetic_closure_missing",
                request_id="synthetic_closure_missing",
                resource_usage_ref="resource_usage:synthetic_closure_missing",
            ),
        )
        self.assertEqual(output.status, "measured_failure")
        self.assertTrue(output.real_integration_flag)


if __name__ == "__main__":
    unittest.main()
