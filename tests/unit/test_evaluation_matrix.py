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
            self.assertEqual(result["matrix_report"]["claim_ceiling"], "level2_pilot_matrix_not_level2_advantage_claim")

    def test_pilot_config_uses_b0_through_b5_without_runtime_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_level2_matrix(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), Path(tmp))
        baselines = [item["baseline"] for item in result["matrix_report"]["baselines"]]
        self.assertEqual([item["baseline_id"] for item in baselines], ["B0", "B1", "B2", "B3", "B4", "B5"])
        self.assertEqual(result["matrix_report"]["benchmark_count"], 25)
        b2 = next(item for item in baselines if item["baseline_id"] == "B2")
        b5 = next(item for item in baselines if item["baseline_id"] == "B5")
        self.assertEqual(b2["provider_config_ref"], "configs/selected_implementations/geometry_default.yaml")
        self.assertFalse(b5["construction_enabled"])
        self.assertEqual(b5["construction_disabled_scope"], "evaluation_config_only")

    def test_pilot_metrics_include_required_v03_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_level2_matrix(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), Path(tmp))
            metrics_path = Path(result["run_dir"]) / "metrics_B2.json"
            payload = __import__("json").loads(metrics_path.read_text(encoding="utf-8"))
        required = {
            "final_theorem_rate",
            "lean_compile_success_rate",
            "proof_repair_success_rate",
            "geometry_solve_request_count",
            "provider_success_rate_by_role",
            "trace_compile_success_rate",
            "construction_candidate_accepted_count",
            "side_condition_blocker_count",
            "resource_usage_by_role",
            "timeout_count",
            "diagnostic_kind_counts",
            "replay_success_rate",
        }
        self.assertTrue(required.issubset(payload["metric_values"]))
        self.assertEqual(payload["metric_values"]["benchmark_count"], 25)


if __name__ == "__main__":
    unittest.main()
