from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.run_trace import build_fixture_run


class RunTraceTest(unittest.TestCase):
    def test_fixture_run_records_required_trace_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "fixture_run"
            report = build_fixture_run(run_dir)
            self.assertEqual(report.replay_status, "restored")
            for name in (
                "provider_run_manifest.json",
                "resource_usage_report_0.json",
                "controller_strategy_log.json",
                "research_contribution_records.json",
                "metrics_report.json",
                "evaluation_funnel.json",
                "reproducibility_report.json",
            ):
                self.assertTrue((run_dir / name).exists(), name)

    def test_contribution_records_distinguish_search_final_and_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "fixture_run"
            build_fixture_run(run_dir)
            payload = (run_dir / "research_contribution_records.json").read_text(encoding="utf-8")
            self.assertIn("used_in_search", payload)
            self.assertIn("used_in_final_proof", payload)
            self.assertIn("diagnostic_only", payload)

    def test_generate_repro_report_script_restores_fixture(self) -> None:
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
            self.assertIn('"replay_status": "restored"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
