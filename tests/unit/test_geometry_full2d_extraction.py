from __future__ import annotations

import unittest

from scripts.check_structured_extraction_v0_4_2 import check_structured_extraction, validate_payload
from scripts.extract_geometry_full2d_statement import extract_statement


class GeometryFull2DExtractionTest(unittest.TestCase):
    def test_lean_side_extraction_smoke_validates(self) -> None:
        self.assertEqual(check_structured_extraction(), [])

    def test_payload_contains_hashes_and_exact_goal(self) -> None:
        payload = extract_statement("lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
        self.assertEqual(validate_payload(payload), [])
        self.assertEqual(payload["relation_to_goal"]["kind"], "exact_goal")
        self.assertTrue(payload["objects"][0]["source_expr_hash"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
