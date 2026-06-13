from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from math_auto_research.workflow.replay import generate_reproducibility_report
from plugins.geometry_synthetic.evaluation import run_level2_matrix
from plugins.geometry_synthetic.run_trace import build_fixture_run


class ReplayIntegrationTest(unittest.TestCase):
    def test_replay_restores_level2_matrix_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run_level2_matrix(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), Path(tmp))
            report = generate_reproducibility_report(Path(result["run_dir"]))
            self.assertEqual(report.replay_status, "restored")
            self.assertIn("level2_run_matrix", report.restored_components)
            self.assertIn("evaluation_funnel", report.restored_components)
            self.assertEqual(report.missing_components, ())

    def test_replay_reports_partial_when_artifact_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "fixture_run"
            build_fixture_run(run_dir)
            (run_dir / "provider_run_manifest.json").unlink()
            report = generate_reproducibility_report(run_dir)
            self.assertEqual(report.replay_status, "partial")
            self.assertIn("provider_run_manifest.json", report.missing_components)
            self.assertNotIn("final_verification_state", report.restored_components)

    def test_generate_repro_report_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "fixture_run"
            build_fixture_run(run_dir)
            completed = subprocess.run(
                [sys.executable, "scripts/generate_repro_report.py", "--run-dir", str(run_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue((run_dir / "reproducibility_report.json").exists())
            self.assertIn('"replay_status": "restored"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
