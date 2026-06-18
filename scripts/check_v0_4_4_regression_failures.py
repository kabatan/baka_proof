#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_run_checks import forbidden_label_keys_present, text_contains_proof_text  # noqa: E402


REQUIRED_FAILURE_FIXTURES = {
    "projection_counted_positive",
    "compiler_succeeds_without_engine_artifact",
    "compiler_succeeds_after_engine_fact_mutation",
    "engine_proof_text_leakage",
    "engine_output_from_task_id_hash",
    "renamed_v0_4_3_release_path",
    "stale_checker_matrix_or_release_output",
    "open_debt_ledger_ignored",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_4_4")
    args = parser.parse_args()
    errors: list[str] = []
    fixture_results = _run_fixture_detectors()
    for name in REQUIRED_FAILURE_FIXTURES:
        result = fixture_results.get(name)
        if not result or result.get("detected") is not True:
            errors.append(f"fixture_not_detected:{name}")

    command_results = []
    for command in [
        [sys.executable, "scripts/check_actual_task_pipeline_runs_v0_4_4.py", "--run-dir", args.run_dir, "--self-test"],
        [sys.executable, "scripts/check_full2d_engine_no_proof_text_v0_4_4.py", "--run-dir", args.run_dir, "--self-test"],
        [sys.executable, "scripts/check_full2d_compiler_input_isolation_v0_4_4.py", "--run-dir", args.run_dir, "--self-test"],
        [sys.executable, "scripts/check_full2d_engine_challenge_suite_v0_4_4.py", "--all-engines"],
        [sys.executable, "scripts/check_no_projection_release_path_v0_4_4.py"],
    ]:
        result = _run_command(command)
        command_results.append(result)
        if result["returncode"] != 0:
            errors.append(f"command_failed:{' '.join(command)}")

    report = {
        "schema_version": "v0_4_4_regression_failures_report_1",
        "status": "passed" if not errors else "failed",
        "fixture_results": fixture_results,
        "command_results": command_results,
        "errors": sorted(set(errors)),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def _run_fixture_detectors() -> dict[str, dict[str, Any]]:
    fake_engine_ref = "EngineOutputFull2D:sha256:" + "1" * 64
    fake_compiler_ref = "CompilerResultFull2D:sha256:" + "2" * 64
    fixtures = {
        "projection_counted_positive": {
            "detected": _is_projection_counted({"category": "ProjectionNonCounted", "target_status": "in_target_positive", "counted_for_release": True}),
        },
        "compiler_succeeds_without_engine_artifact": {
            "detected": _compiler_has_missing_engine(
                {"consumed_engine_output_refs": [fake_engine_ref], "status": "compiled_patch"},
                existing_engine_refs=set(),
            ),
        },
        "compiler_succeeds_after_engine_fact_mutation": {
            "detected": _mutation_not_sensitive({"solver_causal_necessity": True, "mutation_sensitive": False, "compiler_result_refs": [fake_compiler_ref]}),
        },
        "engine_proof_text_leakage": {
            "detected": text_contains_proof_text({"normalized_output_payload": " exact forbidden_proof"}),
        },
        "engine_output_from_task_id_hash": {
            "detected": _engine_output_from_task_id({"task_id": "v044-positive-0001", "normalized_output_ref": "sha256:v044-positive-0001"}),
        },
        "renamed_v0_4_3_release_path": {
            "detected": _contains_old_release_signature("from scripts.run_full2d_matrix_v0_4_3 import main\n"),
        },
        "stale_checker_matrix_or_release_output": {
            "detected": _is_stale_matrix({"schema_version": "Full2DMatrixSummaryV043", "status": "passed"}),
        },
        "open_debt_ledger_ignored": {
            "detected": _open_debt_ignored({"debt_ledger_summary": {"open_entries": ["ReleaseBlocker:missing evidence"]}, "closure_allowed": True}),
        },
        "compiler_forbidden_label_fixture": {
            "detected": "template_id" in forbidden_label_keys_present({"template_id": "easy-template"}),
        },
    }
    return fixtures


def _is_projection_counted(task: dict[str, Any]) -> bool:
    return task.get("category") == "ProjectionNonCounted" and (task.get("counted_for_release") is True or task.get("target_status") == "in_target_positive")


def _compiler_has_missing_engine(compiler: dict[str, Any], *, existing_engine_refs: set[str]) -> bool:
    consumed = {str(ref) for ref in compiler.get("consumed_engine_output_refs", [])}
    return compiler.get("status") == "compiled_patch" and bool(consumed - existing_engine_refs)


def _mutation_not_sensitive(causality: dict[str, Any]) -> bool:
    return causality.get("solver_causal_necessity") is True and causality.get("mutation_sensitive") is not True


def _engine_output_from_task_id(engine: dict[str, Any]) -> bool:
    value = str(engine.get("normalized_output_ref", ""))
    task_id = str(engine.get("task_id", ""))
    return bool(task_id) and task_id in value


def _contains_old_release_signature(text: str) -> bool:
    return "v0_4_3" in text or "benchmarks/geometry_full2d/" in text or "ExternalProjectionCorpus" in text


def _is_stale_matrix(summary: dict[str, Any]) -> bool:
    return summary.get("schema_version") != "Full2DMatrixSummaryV044" or not summary.get("run_records_hash")


def _open_debt_ignored(report: dict[str, Any]) -> bool:
    open_entries = report.get("debt_ledger_summary", {}).get("open_entries", [])
    return bool(open_entries) and report.get("closure_allowed") is True


def _run_command(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=900,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-1200:],
        "stderr_tail": completed.stderr[-1200:],
    }


if __name__ == "__main__":
    raise SystemExit(main())
