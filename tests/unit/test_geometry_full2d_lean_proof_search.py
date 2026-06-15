from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec
from plugins.geometry_full2d.engine_contracts import EngineInputFull2D, ResourceBudget, RunContext
from plugins.geometry_full2d.engines.lean_proof_search import run
from scripts.extract_geometry_full2d_statement import extract_statement
from scripts.smoke_full2d_engine import run_smoke


class GeometryFull2DLeanProofSearchTest(unittest.TestCase):
    def test_lean_proof_search_smoke_passes(self) -> None:
        self.assertEqual(run_smoke("lean_proof_search"), [])

    def test_smoke_claim_produces_semantic_trace(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="lean_proof_search_unit",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim.to_dict(),
            ),
            ResourceBudget(timeout_sec=30.0),
            RunContext(
                run_id="provider_run:lean_proof_search_unit",
                request_id="lean_proof_search_unit",
                resource_usage_ref="resource_usage:lean_proof_search_unit",
            ),
        )
        self.assertEqual(output.status, "normalized_success")
        self.assertTrue(output.real_integration_flag)
        self.assertFalse(output.fixture_flag)
        self.assertTrue(str(output.normalized_output_ref).startswith("LeanProofSearchTraceFull2D:sha256:"))

    def test_unsupported_theorem_is_measured_failure(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        claim = build_claim_spec(payload).claim_spec
        assert claim is not None
        claim_dict = claim.to_dict()
        claim_dict["target"] = {**claim_dict["target"], "args": ["point:A", "point:B", "point:A"]}
        output = run(
            EngineInputFull2D(
                schema_version="1.0.0",
                request_id="lean_proof_search_unsupported",
                claim_spec_ref=claim.claim_spec_hash,
                target_library=claim.target_library,
                claim_spec=claim_dict,
            ),
            ResourceBudget(timeout_sec=30.0),
            RunContext(
                run_id="provider_run:lean_proof_search_unsupported",
                request_id="lean_proof_search_unsupported",
                resource_usage_ref="resource_usage:lean_proof_search_unsupported",
            ),
        )
        self.assertEqual(output.status, "measured_failure")


if __name__ == "__main__":
    unittest.main()
