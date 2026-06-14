from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.proof.solver_backed_proof_certificate import expected_certificate_id


ROOT = Path(__file__).resolve().parents[2]


class SolverBackedCheckerTests(unittest.TestCase):
    def test_metrics_checker_accepts_thresholds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            corpus_entries = []
            per_task_index = {}
            categories = ["solver_backed_geotrace_final"] * 6 + ["solver_backed_construction_final"] * 3 + ["solver_backed_hybrid_or_side_condition_final"]
            for baseline_id in ("B2", "B4"):
                for index, category in enumerate(categories, start=1):
                    task_id = f"task:{index:02d}"
                    task_dir = run_dir / baseline_id / f"task_{index:02d}"
                    task_dir.mkdir(parents=True)
                    task_result = _make_counted_task(
                        task_dir,
                        fixture=False,
                        baseline_id=baseline_id,
                        task_entry_id=task_id,
                        dependency_kind="auxiliary_construction" if category == "solver_backed_construction_final" else "geotrace",
                    )
                    _write_json(task_dir / "task_result.json", task_result)
                    per_task_index[f"{baseline_id}:{task_id}"] = str(task_dir / "task_result.json")
                    if baseline_id == "B2":
                        corpus_entries.append({"entry_id": task_id, "task_category": category})
            corpus_path = run_dir / "corpus.jsonl"
            corpus_path.write_text("\n".join(json.dumps(entry, sort_keys=True) for entry in corpus_entries), encoding="utf-8")
            _write_json(run_dir / "level2_matrix_report.json", {"benchmark_corpus_path": str(corpus_path)})
            _write_json(run_dir / "per_task_artifact_index.json", per_task_index)
            _write_json(
                run_dir / "metrics_B2.json",
                {
                    "metric_values": {
                        "solver_backed_final_theorem_count": 10,
                        "geotrace_solver_backed_final_theorem_count": 6,
                        "construction_solver_backed_final_theorem_count": 3,
                    }
                },
            )
            _write_json(run_dir / "metrics_B4.json", {"metric_values": {"solver_backed_final_theorem_count": 10}})
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

    def test_artifact_checker_rejects_empty_source_problem_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            _write_json(run_dir / "source_problem_ref.json", {})
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("missing_or_invalid_source_problem_ref", completed.stdout)

    def test_artifact_checker_rejects_fixture_provider_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            provider_manifest = json.loads((run_dir / "provider_run_manifest.json").read_text(encoding="utf-8"))
            provider_manifest["fixture_flag"] = True
            provider_manifest["engine_runs"][0]["fixture_flag"] = True
            _write_json(run_dir / "provider_run_manifest.json", provider_manifest)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("provider_manifest_fixture_flag", completed.stdout)

    def test_artifact_checker_rejects_missing_patch_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            patch = json.loads((run_dir / "lean_patch_candidate.json").read_text(encoding="utf-8"))
            patch.pop("patch_id")
            _write_json(run_dir / "lean_patch_candidate.json", patch)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("missing_or_invalid_patch_id", completed.stdout)

    def test_artifact_checker_rejects_missing_generated_candidate_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            _write_json(run_dir / "generated_candidate_file_ref.json", {"generated_candidate_file_ref": task_result["generated_candidate_file_ref"]})
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("missing_generated_candidate_path", completed.stdout)

    def test_artifact_checker_rejects_stale_generated_candidate_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            (run_dir / "Generated.lean").write_text(
                "\n".join(
                    [
                        "theorem task : True := by",
                        "  -- MARP_PROOF_REGION_START:task",
                        "  trivial",
                        "  -- MARP_PROOF_REGION_END:task",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("generated_candidate_ref_hash_mismatch", completed.stdout)

    def test_artifact_checker_rejects_final_verify_candidate_ref_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            final_report = json.loads((run_dir / "final_verify_report.json").read_text(encoding="utf-8"))
            final_report["checked_candidate_file_ref"] = "sha256:" + ("9" * 64)
            _write_json(run_dir / "final_verify_report.json", final_report)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("final_verify_generated_candidate_ref_mismatch", completed.stdout)

    def test_artifact_checker_rejects_stale_worker_and_task_generated_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            stale_ref = "sha256:" + ("9" * 64)
            worker = json.loads((run_dir / "worker_result.json").read_text(encoding="utf-8"))
            worker["generated_candidate_file_ref"] = stale_ref
            task_result["generated_candidate_file_ref"] = stale_ref
            _write_json(run_dir / "worker_result.json", worker)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("task_generated_candidate_ref_mismatch", completed.stdout)
            self.assertIn("worker_generated_candidate_ref_mismatch", completed.stdout)

    def test_artifact_checker_rejects_missing_geotrace_raw_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            geotrace = json.loads((run_dir / "geotrace.json").read_text(encoding="utf-8"))
            geotrace["steps"][0].pop("source_raw_ref")
            _write_json(run_dir / "geotrace.json", geotrace)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("geotrace_step_missing_raw_ref", completed.stdout)

    def test_artifact_checker_rejects_missing_certificate_required_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            certificate = json.loads((run_dir / "solver_backed_proof_certificate.json").read_text(encoding="utf-8"))
            certificate.pop("lean_patch_candidate_ref")
            _write_json(run_dir / "solver_backed_proof_certificate.json", certificate)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid_solver_backed_certificate", completed.stdout)

    def test_artifact_checker_rejects_missing_patch_dependency_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            patch = json.loads((run_dir / "lean_patch_candidate.json").read_text(encoding="utf-8"))
            patch["solver_dependency_refs"] = ["provider_run_manifest:test"]
            _write_json(run_dir / "lean_patch_candidate.json", patch)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("patch_missing_dependency_ref", completed.stdout)

    def test_artifact_checker_rejects_missing_compiler_result_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            trace = json.loads((run_dir / "trace_compilation_result.json").read_text(encoding="utf-8"))
            trace.pop("result_id")
            _write_json(run_dir / "trace_compilation_result.json", trace)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("trace_compiler_ref_missing_from_patch", completed.stdout)

    def test_artifact_checker_rejects_certificate_compiler_result_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            trace = json.loads((run_dir / "trace_compilation_result.json").read_text(encoding="utf-8"))
            trace["result_id"] = "trace_compilation:other"
            _write_json(run_dir / "trace_compilation_result.json", trace)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("certificate_trace_compiler_ref_mismatch", completed.stdout)

    def test_artifact_checker_rejects_provider_result_missing_solver_ref(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=False)
            provider_result = json.loads((run_dir / "provider_result.json").read_text(encoding="utf-8"))
            provider_result["geotrace_ref"] = None
            _write_json(run_dir / "provider_result.json", provider_result)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_solver_backed_artifacts.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("solver_ref_missing_from_provider_result", completed.stdout)

    def test_no_fixture_checker_rejects_fixture_success_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            task_result = _make_counted_task(run_dir, fixture=True)
            _write_json(run_dir / "per_task_artifact_index.json", {"B2:task": str(run_dir / "task_result.json")})
            _write_json(run_dir / "task_result.json", task_result)
            completed = _run_script("scripts/check_no_fixture_solver_backed_release.py", "--run-dir", str(run_dir))
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("fixture", completed.stdout)


def _make_counted_task(
    run_dir: Path,
    *,
    fixture: bool,
    baseline_id: str = "B2",
    task_entry_id: str = "task",
    dependency_kind: str = "geotrace",
) -> dict:
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
        "manifest_id": "provider_run_manifest:test",
        "fixture_flag": fixture,
        "real_integration_flag": not fixture,
        "engine_runs": [
            {
                "engine_role": "construction_proposer" if dependency_kind == "auxiliary_construction" else "symbolic_closure",
                "normalized_output_ref": "aux_construction_candidate:task" if dependency_kind == "auxiliary_construction" else "geotrace:task",
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
        "provider_result.json": run_dir / "provider_result.json",
        "extraction_report.json": run_dir / "extraction_report.json",
        "artifact_index.json": run_dir / "artifact_index.json",
    }
    if dependency_kind == "auxiliary_construction":
        artifacts["construction_candidate.json"] = run_dir / "construction_candidate.json"
        artifacts["construction_compilation_result.json"] = run_dir / "construction_compilation_result.json"
        solver_ref = "aux_construction_candidate:task"
        compiler_ref = "construction_compilation:task"
    else:
        artifacts["geotrace.json"] = run_dir / "geotrace.json"
        artifacts["trace_compilation_result.json"] = run_dir / "trace_compilation_result.json"
        solver_ref = "geotrace:task"
        compiler_ref = "trace_compilation:task"
    certificate_id = "solver_backed_proof_certificate:test"
    source_text = source.read_text(encoding="utf-8")
    generated_text = generated.read_text(encoding="utf-8")
    source_ref = "sha256:" + hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    generated_ref = "sha256:" + hashlib.sha256(generated.read_bytes()).hexdigest()
    patch_id = "lean_patch:" + ("2" * 64)
    worker_result_id = "worker_result:test"
    final_verify_report_id = "final_verify:test"
    protected_statement_hash = "sha256:" + ("3" * 64)
    raw_ref = "sha256:" + hashlib.sha256(b"provider raw trace").hexdigest()
    _write_json(
        artifacts["source_problem_ref.json"],
        {
            "source_problem_ref": source_ref,
            "source_problem_path": str(source),
            "theorem_file_path": str(source),
        },
    )
    _write_json(
        artifacts["generated_candidate_file_ref.json"],
        {"generated_candidate_file_ref": generated_ref, "generated_candidate_path": str(generated)},
    )
    _write_json(
        artifacts["lean_patch_candidate.json"],
        {
            "patch_id": patch_id,
            "proof_template_id": "trace.coll_self_left.v1" if dependency_kind == "geotrace" else "construction.exists_existing_line_witness.v1",
            "solver_dependency_refs": ["provider_run_manifest:test", solver_ref, compiler_ref],
        },
    )
    diff_hash = "sha256:" + ("1" * 64)
    _write_json(
        artifacts["worker_result.json"],
        {
            "patch_applied": True,
            "generated_candidate_file_ref": generated_ref,
            "proof_region_diff_hash": diff_hash,
            "worker_output": {"generated_candidate_path": str(generated)},
            "worker_result_id": worker_result_id,
        },
    )
    _write_json(
        artifacts["final_verify_report.json"],
        {
            "proof_use_status": "final_theorem",
            "solver_backed_proof_status": "passed",
            "report_id": final_verify_report_id,
            "theorem_statement_hash": protected_statement_hash,
            "checked_candidate_file_ref": generated_ref,
        },
    )
    certificate_payload = {
        "schema_version": "1.0.0",
        "task_run_id": f"task_run:{baseline_id}:{task_entry_id}",
        "benchmark_entry_id": task_entry_id,
        "baseline_id": baseline_id,
        "source_problem_ref": source_ref,
        "generated_candidate_file_ref": generated_ref,
        "theorem_name": "task",
        "protected_statement_hash": protected_statement_hash,
        "extraction_report_ref": "geometry_extraction:test",
        "goal_anchor_ref": "goal_anchor:test",
        "provider_run_manifest_ref": "provider_run_manifest:test",
        "normalized_solver_artifact": {
            "source_engine_role": "construction_proposer" if dependency_kind == "auxiliary_construction" else "symbolic_closure",
            "kind": "auxiliary_construction" if dependency_kind == "auxiliary_construction" else "geotrace",
            "ref": solver_ref,
        },
        "compiler_result_ref": compiler_ref,
        "lean_patch_candidate_ref": patch_id,
        "worker_result_ref": worker_result_id,
        "final_verify_report_ref": final_verify_report_id,
        "proof_region_diff_hash": diff_hash,
        "solver_dependency_status": "passed",
        "theorem_hash_unchanged": True,
        "no_sorry": True,
        "no_forbidden_axioms": True,
        "final_verify_status": "final_theorem",
        "status": "passed",
        "failure_reason": None,
    }
    certificate_payload["certificate_id"] = expected_certificate_id(certificate_payload)
    _write_json(
        artifacts["solver_backed_proof_certificate.json"],
        certificate_payload,
    )
    certificate_id = certificate_payload["certificate_id"]
    _write_json(artifacts["provider_run_manifest.json"], provider)
    _write_json(
        artifacts["provider_result.json"],
        {
            "geotrace_ref": solver_ref if dependency_kind == "geotrace" else None,
            "construction_candidate_refs": [solver_ref] if dependency_kind == "auxiliary_construction" else [],
        },
    )
    _write_json(artifacts["extraction_report.json"], {"status": "accepted"})
    if dependency_kind == "auxiliary_construction":
        _write_json(artifacts["construction_candidate.json"], {"candidate_id": solver_ref})
        _write_json(
            artifacts["construction_compilation_result.json"],
            {"status": "compiled", "candidate_id": solver_ref, "result_id": compiler_ref},
        )
    else:
        _write_json(
            artifacts["geotrace.json"],
            {
                "trace_id": solver_ref,
                "source_provider_result": "provider_run_manifest:test",
                "steps": [{"step_id": "step:1", "source_raw_ref": raw_ref}],
            },
        )
        _write_json(
            artifacts["trace_compilation_result.json"],
            {"status": "compiled", "trace_id": solver_ref, "result_id": compiler_ref, "lean_patch_candidate_ref": "compiler_patch:test"},
        )
    artifact_index = {name: str(path) for name, path in artifacts.items()}
    _write_json(artifacts["artifact_index.json"], artifact_index)
    return {
        "baseline_id": baseline_id,
        "task_entry_id": task_entry_id,
        "theorem_file_path": str(source),
        "theorem_name": "task",
        "artifact_index": artifact_index,
        "proof_use_status": "final_theorem",
        "solver_backed_final_theorem": True,
        "solver_backed_proof_certificate_ref": certificate_id,
        "proof_repair_patch_applied": True,
        "proof_region_diff_hash": diff_hash,
        "generated_candidate_file_ref": generated_ref,
        "solver_dependency_kind": dependency_kind,
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
