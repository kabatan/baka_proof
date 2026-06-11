from __future__ import annotations

import unittest

from plugins.geometry_synthetic.extraction import GeometryExtractor


class GeometryExtractionTest(unittest.TestCase):
    def test_accepts_supported_goal_as_claim_spec(self) -> None:
        report, claim = GeometryExtractor().extract("target collinear A B C with distinct A B", "goal:1")
        self.assertEqual(report.status, "accepted")
        self.assertEqual(report.relation, "exact")
        self.assertEqual(report.result_level, "extracted_claim")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNotNone(claim)
        assert claim is not None
        self.assertEqual(claim.target_library, "LeanGeoSubsetV1:1.0.0")
        self.assertIn("explicit_distinctness", claim.nondegeneracy_assumptions)

    def test_safe_rejects_unsupported_goal(self) -> None:
        report, claim = GeometryExtractor().extract("target arbitrary_mathlib_expression", "goal:2")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "none")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)

    def test_raw_dsl_without_goal_anchor_does_not_get_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract("raw dsl collinear A B C", "")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.goal_anchor_ref, "")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)

    def test_sufficient_relation_requires_matching_direction(self) -> None:
        accepted, claim = GeometryExtractor().extract(
            "target collinear A B C relation:sufficient direction_needed:forward direction_available:forward",
            "goal:3",
        )
        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(accepted.relation, "sufficient")
        self.assertIsNotNone(claim)

        rejected, rejected_claim = GeometryExtractor().extract(
            "target collinear A B C relation:sufficient direction_needed:forward direction_available:reverse",
            "goal:4",
        )
        self.assertEqual(rejected.status, "safe_rejected")
        self.assertEqual(rejected.safe_reject_reason, "direction_mismatch")
        self.assertIsNone(rejected_claim)

    def test_related_relation_cannot_create_goal_level_claim(self) -> None:
        report, claim = GeometryExtractor().extract("target collinear A B C relation:related", "goal:5")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.relation, "related")
        self.assertIsNone(claim)


if __name__ == "__main__":
    unittest.main()
