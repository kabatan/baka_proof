from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.schema_validation import validate_artifact
from plugins.geometry_synthetic.construction.auxiliary_construction_candidate_v1 import (
    AuxiliaryConstructionCandidateV1,
    candidate_from_dict,
)


class AuxiliaryConstructionCandidateTest(unittest.TestCase):
    def test_base_spec_fields_are_emitted_and_schema_validates(self) -> None:
        candidate = AuxiliaryConstructionCandidateV1(
            schema_version="1.0.0",
            candidate_id="aux_construction_candidate:fixture",
            construction_kind="line_through_two_distinct_points",
            source_provenance="provider_run:fixture",
            introduced_objects=("l_aux:Line",),
            dependencies=("A:Point", "B:Point"),
            intended_use="search_hint_for_symbolic_retry",
            side_conditions=("A != B",),
        )
        payload = candidate.to_dict()
        self.assertEqual(payload["construction_id"], "aux_construction_candidate:fixture")
        self.assertIn("source_provider_result", payload)
        self.assertEqual(payload["dependencies"], {"objects": ("A:Point", "B:Point")})
        self.assertIn("required_side_conditions", payload)
        self.assertIn("lean_introduction_plan", payload)
        self.assertEqual(payload["proof_use_status"], "not_allowed_until_final_verify")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "auxiliary_construction_candidate_v1.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(validate_artifact(path).schema_id, "geometry.auxiliary_construction_candidate_v1.v1")

    def test_candidate_from_base_payload_preserves_structured_side_conditions(self) -> None:
        candidate = candidate_from_dict(
            {
                "schema_version": "1.0.0",
                "construction_id": "aux_construction_candidate:base",
                "source_provider_result": "sha256:provider",
                "construction_kind": "midpoint",
                "introduced_objects": ["M:Point"],
                "dependencies": {"points": ["A", "B"]},
                "required_side_conditions": {
                    "nondegeneracy": ["A != B"],
                    "incidence": [],
                    "existence": [],
                    "uniqueness_if_needed": [],
                    "orientation": [],
                    "diagram_cases": [],
                },
                "lean_introduction_plan": {
                    "theorem_template_id": "lean_template:midpoint:v1",
                    "generated_obligations": ["obligation:A != B"],
                },
                "proof_use_status": "not_allowed_until_final_verify",
            }
        )
        self.assertEqual(candidate.candidate_id, "aux_construction_candidate:base")
        self.assertEqual(candidate.dependencies, ("A", "B"))
        self.assertEqual(candidate.side_conditions, ("A != B",))
        self.assertEqual(candidate.proof_use_status, "not_allowed_until_final_verify")


if __name__ == "__main__":
    unittest.main()
