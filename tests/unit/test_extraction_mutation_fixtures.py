from __future__ import annotations

import unittest

from plugins.geometry_synthetic.extraction import GeometryExtractor, LeanGoalContext, RelationEvidence


class ExtractionMutationFixtureTest(unittest.TestCase):
    def test_local_notation_ambiguity_safe_rejects(self) -> None:
        report, claim = GeometryExtractor().extract("target unsupported_local_notation", "goal:local-notation")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "unsupported_local_notation")
        self.assertIsNone(claim)

    def test_missing_nondegeneracy_safe_rejects_construction_target(self) -> None:
        report, claim = GeometryExtractor().extract_context(
            LeanGoalContext(
                source_goal_ref="goal:missing-nondegeneracy",
                elaboration_status="passed",
                elaboration_report_ref="lean:missing-nondegeneracy",
                objects=("A:Point", "B:Point"),
                hypotheses=(),
                target_form="line_through_two_distinct_points",
                target_raw="line_from_points A B",
                nondegeneracy_assumptions=(),
            )
        )
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "missing_nondegeneracy")
        self.assertIsNone(claim)

    def test_unsupported_orientation_safe_rejects(self) -> None:
        report, claim = GeometryExtractor().extract("target unsupported_orientation_semantics", "goal:orientation")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "unsupported_orientation_semantics")
        self.assertIsNone(claim)

    def test_related_only_target_safe_rejects(self) -> None:
        report, claim = GeometryExtractor().extract_context(
            _context_for_collinearity("goal:related-only"),
            RelationEvidence("related"),
        )
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "relation_not_goal_level")
        self.assertIsNone(claim)

    def test_raw_dsl_claim_safe_rejects(self) -> None:
        report, claim = GeometryExtractor().extract("raw_dsl_claim collinear A B C", "")
        self.assertEqual(report.status, "safe_rejected")
        self.assertEqual(report.safe_reject_reason, "missing_goal_anchor")
        self.assertEqual(report.proof_use_status, "not_allowed")
        self.assertIsNone(claim)


def _context_for_collinearity(source_goal_ref: str) -> LeanGoalContext:
    return LeanGoalContext(
        source_goal_ref=source_goal_ref,
        elaboration_status="passed",
        elaboration_report_ref="lean:related-only",
        objects=("A:Point", "B:Point", "C:Point"),
        hypotheses=("collinear",),
        target_form="collinear",
        target_raw="Coll A B C",
    )


if __name__ == "__main__":
    unittest.main()
