from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext
from plugins.geometry_full2d.engines.construction_search import run
from scripts.extract_geometry_full2d_statement import extract_statement
from scripts.smoke_full2d_engine import run_smoke


class GeometryFull2DConstructionSearchTest(unittest.TestCase):
    def test_construction_search_smoke_passes(self) -> None:
        self.assertEqual(run_smoke("construction_search"), [])

    def test_non_degenerate_point_pair_produces_auxiliary_line(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="construction_search_unit",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim.to_dict(),
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:construction_search_unit",
                request_id="construction_search_unit",
                resource_usage_ref="resource_usage:construction_search_unit",
            ),
        )
        self.assertEqual(output.status, "normalized_success")
        self.assertTrue(output.real_integration_flag)
        self.assertFalse(output.fixture_flag)
        self.assertTrue(str(output.normalized_output_ref).startswith("AuxiliaryConstructionFull2D:sha256:"))

    def test_missing_side_condition_is_measured_failure(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        claim_dict = claim.to_dict()
        claim_dict["side_conditions"]["nondegeneracy"] = ()
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="construction_search_missing_side",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim_dict,
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:construction_search_missing_side",
                request_id="construction_search_missing_side",
                resource_usage_ref="resource_usage:construction_search_missing_side",
            ),
        )
        self.assertEqual(output.status, "measured_failure")


if __name__ == "__main__":
    unittest.main()
