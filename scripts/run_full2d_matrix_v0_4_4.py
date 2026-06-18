#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.full2d_v0_4_4_corpus_lib import load_manifest, positive_tasks, resolve  # noqa: E402
from scripts.full2d_v0_4_4_run_checks import load_records  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--execute-all", action="store_true")
    args = parser.parse_args()
    report = run_matrix(Path(args.config), Path(args.run_dir), execute_all=args.execute_all)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_matrix(config_path: Path, run_dir: Path, *, execute_all: bool) -> dict[str, Any]:
    config_path = resolve(config_path)
    run_dir = resolve(run_dir)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    corpus_root = resolve(Path(str(config["benchmark_corpus_root"])))
    baselines = [str(item["id"]) for item in config["baselines"]]
    manifest = load_manifest(corpus_root)
    task_ids = [str(task["task_id"]) for task in positive_tasks(manifest)]
    missing = _missing_records(run_dir, task_ids, baselines)
    runner_reports: list[dict[str, Any]] = []
    errors: list[str] = []
    if missing and execute_all:
        missing_baselines = sorted({baseline for _task_id, baseline in missing})
        command = [
            sys.executable,
            "scripts/run_full2d_actual_task_v0_4_4.py",
            "--config",
            str(config_path),
            "--corpus-root",
            str(corpus_root),
            "--run-dir",
            str(run_dir),
        ]
        for baseline in missing_baselines:
            command.extend(["--baseline", baseline])
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=_no_browser_env(),
            timeout=5400,
        )
        try:
            runner_reports.append(json.loads(completed.stdout))
        except json.JSONDecodeError:
            runner_reports.append({"status": "failed", "stdout_tail": completed.stdout[-1000:], "stderr_tail": completed.stderr[-1000:]})
        if completed.returncode != 0:
            errors.append(f"actual_task_runner_failed:{completed.returncode}")
    missing_after = _missing_records(run_dir, task_ids, baselines)
    if missing_after:
        errors.append(f"missing_records:{len(missing_after)}")

    records = [record for _path, record in load_records(run_dir)]
    positive_set = set(task_ids)
    baseline_counts: dict[str, dict[str, Any]] = {}
    family_counts: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: defaultdict(lambda: {"records": 0, "final_theorem": 0, "measured_failure": 0}))
    seen = Counter()
    for record in records:
        task_id = str(record.get("task_id"))
        baseline = str(record.get("baseline_id"))
        if task_id not in positive_set or baseline not in baselines:
            continue
        seen[(task_id, baseline)] += 1
        family = str(record.get("theorem_family"))
        final_status = str(record.get("final_status"))
        family_counts[baseline][family]["records"] += 1
        if final_status in {"final_theorem", "measured_failure"}:
            family_counts[baseline][family][final_status] += 1

    for baseline in baselines:
        final_count = sum(data["final_theorem"] for data in family_counts[baseline].values())
        measured_count = sum(data["measured_failure"] for data in family_counts[baseline].values())
        count = final_count + measured_count
        baseline_counts[baseline] = {
            "record_count": count,
            "final_theorem": final_count,
            "measured_failure": measured_count,
            "success_rate": final_count / count if count else 0.0,
        }
        if count != len(task_ids):
            errors.append(f"{baseline}:record_count:{count}:expected:{len(task_ids)}")
    duplicates = [f"{task_id}:{baseline}:{count}" for (task_id, baseline), count in seen.items() if count != 1]
    errors.extend(f"duplicate_record:{item}" for item in duplicates[:20])

    summary = {
        "schema_version": "Full2DMatrixSummaryV044",
        "status": "passed" if not errors else "failed",
        "config_path": str(config_path.relative_to(ROOT)),
        "run_dir": str(run_dir.relative_to(ROOT)),
        "corpus_root": str(corpus_root.relative_to(ROOT)),
        "corpus_manifest_hash": str(manifest["manifest_hash"]),
        "config_hash": _sha_file(config_path),
        "run_records_hash": _run_records_hash(run_dir),
        "positive_task_count": len(task_ids),
        "baselines": baselines,
        "conditional_model_baseline": {
            "id": "B8",
            "status": "not_applicable_model_provider_not_used"
            if not config.get("conditional_model_baseline", {}).get("enabled")
            else "required",
        },
        "baseline_counts": baseline_counts,
        "family_counts": {baseline: dict(families) for baseline, families in family_counts.items()},
        "runner_reports": runner_reports,
        "errors": sorted(set(errors)),
    }
    out = run_dir / "matrix_summary_v0_4_4.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _missing_records(run_dir: Path, task_ids: list[str], baselines: list[str]) -> list[tuple[str, str]]:
    existing = {(str(record.get("task_id")), str(record.get("baseline_id"))) for _path, record in load_records(run_dir)}
    return [(task_id, baseline) for task_id in task_ids for baseline in baselines if (task_id, baseline) not in existing]


def _run_records_hash(run_dir: Path) -> str:
    records_dir = run_dir / "actual_task_pipeline_runs_v0_4_4"
    items = []
    for path in sorted(records_dir.glob("*.json")):
        items.append((path.name, _sha_file(path)))
    return _sha_text(json.dumps(items, sort_keys=True, separators=(",", ":")))


def _sha_file(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _no_browser_env() -> dict[str, str]:
    env = os.environ.copy()
    env["BROWSER"] = "python -c \"import sys; sys.exit(0)\""
    no_browser = ROOT / "scripts" / "no_browser_sitecustomize"
    if no_browser.exists():
        env["PYTHONPATH"] = str(no_browser.resolve()) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return env


if __name__ == "__main__":
    raise SystemExit(main())
