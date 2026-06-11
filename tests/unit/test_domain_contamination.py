from __future__ import annotations

import unittest
from pathlib import Path


class DomainContaminationTest(unittest.TestCase):
    def test_proof_state_core_has_no_geometry_specific_terms(self) -> None:
        root = Path("src/math_auto_research/proof_state")
        forbidden_terms = [
            "Geometry",
            "GeoTrace",
            "LeanGeo",
            "Newclid",
            "GenesisGeo",
            "TongGeometry",
            "geometry_synthetic",
        ]
        contaminated: list[str] = []
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for term in forbidden_terms:
                if term in text:
                    contaminated.append(f"{path}:{term}")
        self.assertEqual(contaminated, [])


if __name__ == "__main__":
    unittest.main()
