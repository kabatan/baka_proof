from __future__ import annotations

import unittest

from plugins.geometry_synthetic.patching import LeanPatchCandidateV1
from plugins.geometry_synthetic.rules import GeoTraceStep, GeoTraceV1
from plugins.geometry_synthetic.trace_compiler import TraceCompiler


class TraceCompilerSolverBackedPatchTests(unittest.TestCase):
    def test_minimum_trace_templates_emit_patch_candidates(self) -> None:
        cases = (
            ("Coll A A B", "trace.coll_self_left.v1", "simp [Coll]"),
            ("Coll A B B", "trace.coll_self_right.v1", "simp [Coll]"),
            ("P ∨ Q", "trace.collinear_or_left.v1", "Or.inl"),
            ("P ∧ Q", "trace.collinear_and_intro.v1", "And.intro"),
        )
        for conclusion, template_id, expected_proof in cases:
            with self.subTest(conclusion=conclusion):
                result = TraceCompiler().compile(trace_for(conclusion))
                self.assertEqual(result.status, "compiled")
                self.assertEqual(result.proof_use_status, "lean_patch_candidate")
                self.assertIsNotNone(result.lean_patch_candidate_ref)
                self.assertIsNotNone(result.lean_patch_candidate)
                patch = LeanPatchCandidateV1.from_dict(result.lean_patch_candidate)
                self.assertEqual(patch.proof_template_id, template_id)
                self.assertIn(expected_proof, patch.proof_region_replacement_text)
                self.assertIn("provider_run_manifest:fixture", patch.solver_dependency_refs)
                self.assertIn("geotrace:fixture", patch.solver_dependency_refs)

    def test_unsupported_trace_template_is_blocked(self) -> None:
        result = TraceCompiler().compile(trace_for("Perp A B C"))
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_trace_to_lean_template", result.blockers)
        self.assertIsNone(result.lean_patch_candidate_ref)
        self.assertIsNone(result.lean_patch_candidate)

    def test_missing_side_condition_never_emits_patch_success(self) -> None:
        trace = GeoTraceV1(
            schema_version="1.0.0",
            trace_id="geotrace:missing-side",
            claim_spec_ref="geometry_claim:fixture",
            steps=(
                GeoTraceStep(
                    step_id="step:1",
                    rule_id="rule:collinearity_identity:v1",
                    premises=("Coll A A B",),
                    conclusion="Coll A A B",
                    side_condition_refs=(),
                ),
            ),
            rule_refs=("rule:collinearity_identity:v1",),
            side_condition_refs=(),
            source_provider_result="provider_run_manifest:fixture",
        )
        result = TraceCompiler().compile(trace)
        self.assertEqual(result.status, "blocked")
        self.assertIsNone(result.lean_patch_candidate_ref)
        self.assertIsNone(result.lean_patch_candidate)


def trace_for(conclusion: str) -> GeoTraceV1:
    return GeoTraceV1(
        schema_version="1.0.0",
        trace_id="geotrace:fixture",
        claim_spec_ref="geometry_claim:fixture",
        steps=(
            GeoTraceStep(
                step_id="step:1",
                rule_id="rule:collinearity_identity:v1",
                premises=(conclusion,),
                conclusion=conclusion,
                side_condition_refs=("points_declared:A:B:C",),
            ),
        ),
        rule_refs=("rule:collinearity_identity:v1",),
        side_condition_refs=("points_declared:A:B:C",),
        source_provider_result="provider_run_manifest:fixture",
    )


if __name__ == "__main__":
    unittest.main()
