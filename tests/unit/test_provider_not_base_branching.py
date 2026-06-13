from __future__ import annotations

import unittest
from pathlib import Path


class ProviderNotBaseBranchingRegressionTest(unittest.TestCase):
    def test_base_source_does_not_branch_on_geometry_engine_names(self) -> None:
        base_files = list(Path("src/math_auto_research/base").rglob("*.py"))
        text = "\n".join(path.read_text(encoding="utf-8") for path in base_files)
        self.assertNotIn("Newclid", text)
        self.assertNotIn("GenesisGeo", text)
        self.assertNotIn("TongGeometry", text)


if __name__ == "__main__":
    unittest.main()
