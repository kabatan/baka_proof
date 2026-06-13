from __future__ import annotations

import unittest
from pathlib import Path

from plugins.geometry_synthetic.target_library_status import build_target_library_status


class TargetLibraryStatusTest(unittest.TestCase):
    def test_manifest_selects_exactly_leangeo_subset(self) -> None:
        report = build_target_library_status(Path("configs/target_libraries/leangeo_subset_v1.yaml"))
        self.assertEqual(report["target_library_id"], "LeanGeoSubsetV1:1.0.0")
        self.assertIn(report["install_status"], {"available", "blocked"})
        self.assertNotIn("Mathlib", report["target_library_id"])


if __name__ == "__main__":
    unittest.main()
