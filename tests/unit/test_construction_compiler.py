from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.construction import AuxiliaryConstructionCandidateV1, ConstructionCompiler
from plugins.geometry_synthetic.construction.construction_compiler import ConstructionCompiler as PlanPathConstructionCompiler


def candidate_fixture(kind: str = "line_through_two_distinct_points") -> AuxiliaryConstructionCandidateV1:
    return AuxiliaryConstructionCandidateV1(
        schema_version="1.0.0",
        candidate_id="aux_construction_candidate:fixture",
        construction_kind=kind,
        source_provenance="provider_run:fixture",
        introduced_objects=("l_aux:Line",),
        dependencies=("A", "B"),
        intended_use="search_hint_for_symbolic_retry",
        side_conditions=("A != B",),
    )


class ConstructionCompilerTest(unittest.TestCase):
    def test_plan_path_construction_compiler_exports_compiler(self) -> None:
        self.assertIs(PlanPathConstructionCompiler, ConstructionCompiler)

    def test_candidate_and_compilation_schemas_validate(self) -> None:
        candidate = candidate_fixture()
        result = ConstructionCompiler().compile(candidate)
        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.proof_use_status, "lean_patch_candidate")
        self.assertEqual(result.generated_obligations, ("obligation:A != B",))
        with tempfile.TemporaryDirectory() as tmp:
            candidate_path = Path(tmp) / "auxiliary_construction_candidate_v1.json"
            result_path = Path(tmp) / "construction_compilation_result.json"
            candidate_path.write_text(json.dumps(candidate.to_dict()), encoding="utf-8")
            result_path.write_text(json.dumps(result.to_dict()), encoding="utf-8")
            self.assertEqual(validate_artifact(candidate_path).schema_id, "geometry.auxiliary_construction_candidate_v1.v1")
            self.assertEqual(validate_artifact(result_path).schema_id, "geometry.construction_compilation_result.v1")

    def test_unsupported_construction_kind_is_blocked(self) -> None:
        candidate = candidate_fixture("free_point")
        result = ConstructionCompiler().compile(candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("unsupported_construction_kind:free_point", result.blockers)
        self.assertIsNone(result.lean_patch)

    def test_missing_side_conditions_are_blocked(self) -> None:
        candidate = AuxiliaryConstructionCandidateV1(
            "1.0.0",
            "aux_construction_candidate:missing-side",
            "line_through_two_distinct_points",
            "provider_run:fixture",
            ("l_aux:Line",),
            ("A", "B"),
            "search_hint_for_symbolic_retry",
            (),
        )
        result = ConstructionCompiler().compile(candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_side_conditions", result.blockers)
        self.assertIn("missing_nondegeneracy_side_conditions", result.blockers)

    def test_missing_dependency_refs_are_blocked(self) -> None:
        candidate = AuxiliaryConstructionCandidateV1(
            "1.0.0",
            "aux_construction_candidate:missing-deps",
            "line_through_two_distinct_points",
            "provider_run:fixture",
            ("l_aux:Line",),
            (),
            "search_hint_for_symbolic_retry",
            ("A != B",),
        )
        result = ConstructionCompiler().compile(candidate)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_dependency_refs", result.blockers)


if __name__ == "__main__":
    unittest.main()
