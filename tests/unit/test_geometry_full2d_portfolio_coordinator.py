from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext
from plugins.geometry_full2d.engines.portfolio_coordinator import build_portfolio_decision, run, validate_portfolio_decision
from scripts.check_portfolio_reason_codes import check_portfolio_reason_codes
from scripts.extract_geometry_full2d_statement import extract_statement
from scripts.smoke_full2d_engine import run_smoke


class GeometryFull2DPortfolioCoordinatorTest(unittest.TestCase):
    def test_portfolio_coordinator_smoke_passes(self) -> None:
        self.assertEqual(run_smoke("portfolio_coordinator"), [])

    def test_reason_code_checker_passes(self) -> None:
        self.assertEqual(check_portfolio_reason_codes(), [])

    def test_incidence_claim_uses_deterministic_policy(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        decision = build_portfolio_decision(claim.to_dict())
        self.assertEqual(validate_portfolio_decision(decision), [])
        self.assertEqual(decision.selected_engine_order[0], "synthetic_closure")
        self.assertIn("lean_proof_search", decision.selected_engine_order)
        self.assertIn("policy:no_llm_semantics", decision.reason_codes)
        self.assertFalse(decision.llm_semantics_used)

    def test_smoke_claim_produces_portfolio_decision_output(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="portfolio_coordinator_unit",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim.to_dict(),
            ),
            ResourceBudget(),
            RunContext(
                run_id="provider_run:portfolio_coordinator_unit",
                request_id="portfolio_coordinator_unit",
                resource_usage_ref="resource_usage:portfolio_coordinator_unit",
            ),
        )
        self.assertEqual(output.status, "normalized_success")
        self.assertTrue(output.real_integration_flag)
        self.assertFalse(output.fixture_flag)
        self.assertTrue(str(output.normalized_output_ref).startswith("PortfolioDecisionFull2D:sha256:"))


if __name__ == "__main__":
    unittest.main()
