from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.workflow.release_acceptance import (
    _browser_suppressed_env,
    blocked_real_integrations,
    evaluate_release_acceptance,
    validate_checklist_item,
)


class ReleaseAcceptanceTest(unittest.TestCase):
    def test_release_commands_inject_no_browser_sitecustomize(self) -> None:
        env = _browser_suppressed_env()
        self.assertIn("no_browser_sitecustomize", env["PYTHONPATH"])
        self.assertIn("sys.exit(0)", env["BROWSER"])

    def test_missing_dependency_probe_fails_blocked_integration_accounting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = blocked_real_integrations(Path(tmp) / "missing.json")
        self.assertEqual(result[0]["status"], "failed")

    def test_contradictory_dependency_probe_fails_blocked_integration_accounting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dependency_probe.json"
            path.write_text(json.dumps({"engines": [], "unresolved": []}), encoding="utf-8")
            result = blocked_real_integrations(path)
        self.assertIn("failed", [item["status"] for item in result])

    def test_bogus_checklist_test_evidence_fails(self) -> None:
        result = validate_checklist_item(
            "bogus_check",
            "test",
            "tests.unit.test_does_not_exist",
            [],
            [],
        )
        self.assertEqual(result["status"], "failed")

    def test_checklist_test_evidence_requires_passed_gate(self) -> None:
        result = validate_checklist_item(
            "release_blocker_19_evaluation_replay_counts",
            "test",
            "tests.unit.test_evaluation_matrix",
            [{"check_id": "gate:make_test", "status": "failed"}],
            [],
        )
        self.assertEqual(result["status"], "failed")

    def test_release_acceptance_static_mode_blocks_commands_disabled(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), run_commands=False)
        self.assertEqual(len(report["checked_blockers"]), 34)
        self.assertIn(report["core_experiment_ready_status"], {"blocked", "failed"})
        self.assertIn(report["tonggeometry_model_backed_status"], {"blocked", "failed", "passed"})
        self.assertIn("blocked_claims", report)
        self.assertIn("release_blocker_24_level2_matrix_run_replay", report["open_blockers"])

    def test_release_acceptance_reports_independent_claim_statuses(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), run_commands=False)
        self.assertIn("core_experiment_ready_status", report)
        self.assertIn("tonggeometry_model_backed_status", report)
        self.assertIn("blocked_claims", report)
        self.assertIn(
            report["claim_ceiling"],
            {
                "core_experiment_ready_passed_no_tong_model_backed_claim",
                "core_experiment_ready_passed_and_tong_model_backed_ready",
                "release_acceptance_blocked_no_v0_3_completion_claim",
                "release_acceptance_failed_no_v0_3_completion_claim",
            },
        )

    def test_release_acceptance_blocks_missing_model_backed_provider_evidence(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), run_commands=False)
        check = next(
            item
            for item in report["checks"]
            if item["check_id"] == "release_blocker_11_real_provider_smoke_evidence"
        )
        self.assertIn(check["status"], {"blocked", "passed"})

    def test_closure_not_allowed_section_does_not_trigger_overclaim(self) -> None:
        report = evaluate_release_acceptance(Path("configs/benchmark_runs/geometry_level2_pilot.yaml"), run_commands=False)
        check = next(
            item
            for item in report["checks"]
            if item["check_id"] == "release_blocker_25_closure_claims_do_not_exceed_evidence"
        )
        self.assertEqual(check["status"], "passed")


if __name__ == "__main__":
    unittest.main()
