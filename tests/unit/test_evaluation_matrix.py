from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.evaluation import run_level2_matrix


class EvaluationMatrixTest(unittest.TestCase):
    def test_level2_matrix_writes_b0_through_b5_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_level2_matrix(Path("configs/benchmark_runs/geometry_level2_smoke.yaml"), Path(tmp))
            run_dir = Path(result["run_dir"])
            for baseline_id in ("B0", "B1", "B2", "B3", "B4", "B5"):
                self.assertTrue((run_dir / f"metrics_{baseline_id}.json").exists(), baseline_id)
            self.assertTrue((run_dir / "level2_matrix_report.json").exists())
            self.assertEqual(result["reproducibility_report"]["run_id"], "geometry_level2_smoke")
            self.assertEqual(result["matrix_report"]["benchmark_pool"], ["sample_target_fixture"])

    def test_matrix_distinguishes_geometry_enabled_from_no_geometry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_level2_matrix(Path("configs/benchmark_runs/geometry_level2_smoke.yaml"), Path(tmp))
            comparison = result["matrix_report"]["comparison"]
            self.assertEqual(comparison["geometry_enabled_minus_controller_no_geometry_final_count"], 1)
            self.assertEqual(result["matrix_report"]["claim_ceiling"], "fixture_level_matrix_not_level2_advantage_claim")


if __name__ == "__main__":
    unittest.main()
