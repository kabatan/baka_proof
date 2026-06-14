from __future__ import annotations

import unittest

from plugins.geometry_synthetic.construction import AuxiliaryConstructionCandidateV1, ConstructionCompiler
from plugins.geometry_synthetic.patching import LeanPatchCandidateV1


class ConstructionCompilerSolverBackedPatchTests(unittest.TestCase):
    def test_minimum_construction_templates_emit_patch_candidates(self) -> None:
        cases = (
            ("construction.exists_existing_line_witness.v1", "exact ⟨L, h⟩"),
            ("construction.distinct_points_on_line_pack.v1", "And.intro hA"),
            ("construction.exists_point_collinear_self.v1", "simp [Coll]"),
        )
        for template_id, expected_proof in cases:
            with self.subTest(template_id=template_id):
                result = ConstructionCompiler().compile(candidate_for(template_id))
                self.assertEqual(result.status, "compiled")
                self.assertIsNotNone(result.lean_patch_candidate_ref)
                self.assertIsNotNone(result.lean_patch_candidate)
                patch = LeanPatchCandidateV1.from_dict(result.lean_patch_candidate)
                self.assertEqual(patch.proof_template_id, template_id)
                self.assertIn(expected_proof, patch.proof_region_replacement_text)
                self.assertIn("provider_run_manifest:fixture", patch.solver_dependency_refs)
                self.assertIn("aux_construction_candidate:fixture", patch.solver_dependency_refs)

    def test_missing_existence_conditions_are_blocked(self) -> None:
        candidate = candidate_for("construction.exists_existing_line_witness.v1", existence=())
        result = ConstructionCompiler().compile(candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_existence_side_conditions", result.blockers)
        self.assertIsNone(result.lean_patch_candidate)


def candidate_for(template_id: str, existence: tuple[str, ...] = ("exists:l_aux:Line",)) -> AuxiliaryConstructionCandidateV1:
    return AuxiliaryConstructionCandidateV1(
        schema_version="1.0.0",
        candidate_id="aux_construction_candidate:fixture",
        construction_kind="plugin_supported",
        source_provenance="provider_run:fixture",
        introduced_objects=("l_aux:Line",),
        dependencies=("A:Point", "B:Point"),
        intended_use="solver_backed_patch_fixture",
        side_conditions=("A != B",),
        source_provider_result="provider_run_manifest:fixture",
        required_side_conditions={
            "nondegeneracy": ("A != B",),
            "incidence": (),
            "existence": existence,
            "uniqueness_if_needed": (),
            "orientation": (),
            "diagram_cases": (),
        },
        lean_introduction_plan={
            "theorem_template_id": template_id,
            "generated_obligations": ("obligation:A != B",),
        },
    )


if __name__ == "__main__":
    unittest.main()
