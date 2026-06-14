from __future__ import annotations

import unittest

from plugins.geometry_full2d.claim_spec import build_claim_spec, compute_context_hash
from scripts.check_full2d_claimspec import check_full2d_claimspec
from scripts.extract_geometry_full2d_statement import extract_statement


class GeometryFull2DClaimSpecTest(unittest.TestCase):
    def test_claimspec_checker_passes(self) -> None:
        self.assertEqual(check_full2d_claimspec(), [])

    def test_smoke_payload_builds_stable_claimspec(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        result = build_claim_spec(payload)
        self.assertEqual(result.status, "accepted")
        self.assertIsNotNone(result.claim_spec)
        claim = result.claim_spec
        assert claim is not None
        self.assertEqual(claim.context_hash, compute_context_hash(payload))
        self.assertTrue(claim.claim_spec_hash.startswith("sha256:"))
        self.assertEqual(claim.relation_to_goal["kind"], "exact_goal")
        self.assertEqual(claim.proof_use_status, "not_allowed")

    def test_target_outside_and_malformed_are_not_claims(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        outside_payload = {**payload, "target": {**payload["target"], "family": "unsupported_3d"}}
        outside = build_claim_spec(outside_payload)
        self.assertEqual(outside.status, "target_outside")
        self.assertIsNone(outside.claim_spec)
        self.assertIsNotNone(outside.target_outside_report)

        malformed_payload = dict(payload)
        malformed_payload.pop("lean_context_hash")
        malformed = build_claim_spec(malformed_payload)
        self.assertEqual(malformed.status, "malformed")
        self.assertIsNone(malformed.claim_spec)
        self.assertIsNotNone(malformed.malformed_report)


if __name__ == "__main__":
    unittest.main()
