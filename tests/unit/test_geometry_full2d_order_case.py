from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext
from plugins.geometry_full2d.engines.order_case import run
from scripts.extract_geometry_full2d_statement import extract_statement
from scripts.smoke_full2d_engine import run_smoke


class GeometryFull2DOrderCaseTest(unittest.TestCase):
    def test_order_case_smoke_passes(self) -> None:
        self.assertEqual(run_smoke("order_case"), [])

    def test_repeated_point_collinearity_produces_coverage_gate(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="order_case_unit",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim.to_dict(),
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:order_case_unit",
                request_id="order_case_unit",
                resource_usage_ref="resource_usage:order_case_unit",
            ),
        )
        self.assertEqual(output.status, "normalized_success")
        self.assertTrue(output.real_integration_flag)
        self.assertFalse(output.fixture_flag)
        self.assertTrue(str(output.normalized_output_ref).startswith("CoverageGateFull2D:sha256:"))

    def test_unsupported_target_is_measured_failure(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        claim_dict = claim.to_dict()
        claim_dict["target"] = {
            "args": ["pt:A", "pt:B"],
            "canonical_expr_hash": "sha256:canon-goal-distinct",
            "family": "metric",
            "predicate_or_shape_id": "goal:distance",
            "source_expr_hash": "sha256:goal-distance",
        }
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="order_case_unsupported",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim_dict,
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:order_case_unsupported",
                request_id="order_case_unsupported",
                resource_usage_ref="resource_usage:order_case_unsupported",
            ),
        )
        self.assertEqual(output.status, "measured_failure")


if __name__ == "__main__":
    unittest.main()
