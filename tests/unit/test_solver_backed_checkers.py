from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SolverBackedCheckerTests(unittest.TestCase):
    def test_metrics_checker_accepts_thresholds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            _write_json(
                run_dir / "metrics_B2.json",
                {
                    "metric_values": {
                        "solver_backed_final_theorem_count": 8,
                        "geotrace_solver_backed_final_theorem_count": 5,
                        "construction_solver_backed_final_theorem_count": 2,
                    }
                },
            )
            _write_json(run_dir / "metrics_B4.json", {"metric_values": {"solver_backed_final_theorem_count": 5}})
            completed = _run_script("scripts/check_solver_backed_metrics.py", "--run-dir", str(run_dir))
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_artifact_and_original_checkers_accept_counted_repair(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            artifact_check = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            original_check = _run_script("scripts/check_no_original_proof_counted_as_solver_backed.py", "--run-dir", str(run_dir))
            self.assertEqual(artifact_check.returncode, 0, artifact_check.stdout + artifact_check.stderr)
            self.assertEqual(original_check.returncode, 0, original_check.stdout + original_check.stderr)

    def test_no_fixture_checker_rejects_fixture_success_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=True)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_no_fixture_solver_backed_release.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("fixture", completed.stdout)


def _make_counted_task(run_dir: Path, *, fixture: bool) -> dict:
    source = run_dir / "Source.lean"
    generated = run_dir / "Generated.lean"
    source.write_text(
        "\n".join(
            [
                "theorem task : True := by",
                "  -- MARP_PROOF_REGION_START:task",
                "  sorry",
                "  -- MARP_PROOF_REGION_END:task",
                "",
            ]
        ),
        encoding="utf-8",
    )
    generated.write_text(
        "\n".join(
            [
                "theorem task : True := by",
                "  -- MARP_PROOF_REGION_START:task",
                "  exact True.intro",
                "  -- MARP_PROOF_REGION_END:task",
                "",
            ]
        ),
        encoding="utf-8",
    )
    provider = {
        "fixture_flag": fixture,
        "real_integration_flag": not fixture,
        "engine_runs": [
            {
                "fixture_flag": fixture,
                "real_integration_flag": not fixture,
                "adapter_version": "newclid-compatible-fixture:0.1" if fixture else "newclid-real:1.0",
                "engine_version": "newclid-compatible-fixture:0.1" if fixture else "newclid-real:1.0",
            }
        ],
    }
    artifacts = {
        "source_problem_ref.json": run_dir / "source_problem_ref.json",
        "generated_candidate_file_ref.json": run_dir / "generated_candidate_file_ref.json",
        "lean_patch_candidate.json": run_dir / "lean_patch_candidate.json",
        "worker_result.json": run_dir / "worker_result.json",
        "final_verify_report.json": run_dir / "final_verify_report.json",
        "solver_backed_proof_certificate.json": run_dir / "solver_backed_proof_certificate.json",
        "provider_run_manifest.json": run_dir / "provider_run_manifest.json",
        "artifact_index.json": run_dir / "artifact_index.json",
    }
    certificate_id = "solver_backed_proof_certificate:test"
    _write_json(artifacts["source_problem_ref.json"], {"source_problem_path": str(source)})
    _write_json(artifacts["generated_candidate_file_ref.json"], {"generated_candidate_path": str(generated)})
    _write_json(artifacts["lean_patch_candidate.json"], {"patch_id": "lean_patch:test"})
    _write_json(artifacts["worker_result.json"], {"patch_applied": True, "worker_output": {"generated_candidate_path": str(generated)}})
    _write_json(
        artifacts["final_verify_report.json"],
        {"proof_use_status": "final_theorem", "solver_backed_proof_status": "passed"},
    )
    _write_json(artifacts["solver_backed_proof_certificate.json"], {"certificate_id": certificate_id})
    _write_json(artifacts["provider_run_manifest.json"], provider)
    artifact_index = {name: str(path) for name, path in artifacts.items()}
    _write_json(artifacts["artifact_index.json"], artifact_index)
    return {
        "baseline_id": "B2",
        "task_entry_id": "task",
        "theorem_file_path": str(source),
        "theorem_name": "task",
        "artifact_index": artifact_index,
        "proof_use_status": "final_theorem",
        "solver_backed_final_theorem": True,
        "solver_backed_proof_certificate_ref": certificate_id,
        "proof_repair_patch_applied": True,
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def _run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


if __name__ == "__main__":
    unittest.main()
