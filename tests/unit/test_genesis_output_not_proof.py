from __future__ import annotations

import json
import unittest

from scripts.run_genesisgeo_probe import build_report


class GenesisOutputNotProofRegressionTest(unittest.TestCase):
    def test_genesis_output_not_proof(self) -> None:
        report = build_report(
            "geometry_request:genesis_output_not_proof",
            {
                "schema_version": "1.0.0",
                "claim_id": "geometry_claim:genesis_output_not_proof",
                "target_library": "LeanGeoSubsetV1:1.0.0",
                "objects": ["A:Point", "B:Point", "C:Point"],
                "hypotheses": ["collinear"],
                "target": {"form": "collinear", "raw": "Coll A B C"},
                "nondegeneracy_assumptions": [],
                "orientation_assumptions": [],
                "source_goal_ref": "lean-check:genesis-output-not-proof",
            },
        )
        raw = json.dumps(report, sort_keys=True)
        self.assertEqual(report["proof_use_status"], "not_allowed")
        self.assertIn("raw_rationale", report)
        self.assertNotIn('"proof_use_status": "final_theorem"', raw)


if __name__ == "__main__":
    unittest.main()
