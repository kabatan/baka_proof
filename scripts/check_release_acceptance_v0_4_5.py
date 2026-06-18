#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> dict[str, object]:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    parsed = None
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        parsed = {"stdout": proc.stdout[-1000:], "stderr": proc.stderr[-1000:]}
    return {"cmd": cmd, "returncode": proc.returncode, "report": parsed}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    config = json.loads((ROOT / args.config).read_text(encoding="utf-8"))
    corpus_root = config["benchmark_corpus_root"]
    run_dir = config["output_root"]
    commands = {
        "active_guardian_spec": [sys.executable, "scripts/check_active_guardian_spec_v0_4_5.py"],
        "shortcut_static": [sys.executable, "scripts/check_release_path_forbidden_shortcuts_v0_4_5.py", "--static-only"],
        "corpus_manifest": [sys.executable, "scripts/check_full2d_corpus_manifest_v0_4_5.py", "--corpus-root", corpus_root],
        "actual_pipeline": [sys.executable, "scripts/check_actual_task_pipeline_runs_v0_4_5.py", "--run-dir", run_dir, "--self-test"],
        "matrix": [sys.executable, "scripts/run_full2d_matrix_v0_4_5.py", "--config", args.config, "--run-dir", run_dir, "--execute-all"],
        "causality_mutations": [sys.executable, "scripts/run_solver_causality_mutations_v0_4_5.py", "--run-dir", run_dir, "--all-b2-successes"],
        "solver_causality": [sys.executable, "scripts/check_solver_causality_reports_v0_4_5.py", "--run-dir", run_dir, "--self-test"],
        "metrics": [sys.executable, "scripts/check_full2d_metrics_v0_4_5.py", "--run-dir", run_dir],
        "regressions": [sys.executable, "scripts/check_v0_4_5_regression_failures.py"],
        "shortcut_full": [sys.executable, "scripts/check_release_path_forbidden_shortcuts_v0_4_5.py", "--config", args.config, "--run-dir", run_dir],
    }
    results = {name: _run(cmd) for name, cmd in commands.items()}
    blockers: list[str] = []
    for name, result in results.items():
        if result["returncode"] != 0:
            blockers.append(f"required_command_failed:{name}")
    corpus = results["corpus_manifest"]["report"]
    summary = corpus.get("corpus_summary", {}) if isinstance(corpus, dict) else {}
    if summary.get("positive_count", 0) < 3350:
        blockers.append("K-014_positive_formal_lean_tasks_lt_3350")
    if summary.get("negative_count", 0) < 500:
        blockers.append("K-014_negative_tasks_lt_500")
    metrics = results["metrics"]["report"]
    if isinstance(metrics, dict) and metrics.get("B2_success_count", 0) == 0:
        blockers.append("K-020_no_B2_successes")
    if isinstance(metrics, dict) and metrics.get("solver_causal_success_fraction") != 1.0:
        blockers.append("K-020_solver_causal_success_fraction")
    if isinstance(metrics, dict) and metrics.get("destructive_rerun_success_fraction") != 1.0:
        blockers.append("K-020_destructive_rerun_success_fraction")
    report = {
        "schema_version": "release_acceptance_v0_4_5_report_1",
        "status": "passed" if not blockers else "failed",
        "closure_allowed": not blockers,
        "hard_blockers": [],
        "release_blockers": sorted(set(blockers)),
        "required_results": results,
    }
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
