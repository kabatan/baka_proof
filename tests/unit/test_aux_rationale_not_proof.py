from __future__ import annotations

import unittest

from scripts.run_genesisgeo_probe import build_report


class AuxiliaryRationaleNotProofRegressionTest(unittest.TestCase):
    def test_aux_rationale_not_proof(self) -> None:
        report = build_report(
            "geometry_request:aux_rationale_not_proof",
            {
                "objects": ["A:Point", "B:Point", "C:Point"],
                "target": {"form": "collinear", "raw": "Coll A B C"},
            },
        )
        self.assertEqual(report["proof_use_status"], "not_allowed")
        self.assertIn("raw_rationale", report)
        candidate = report.get("candidate")
        if candidate is not None:
            self.assertEqual(candidate["proof_use_status"], "not_allowed_until_final_verify")


if __name__ == "__main__":
    unittest.main()
