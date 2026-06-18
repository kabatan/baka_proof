#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d_v0_4_5.compiler import compile_from_selected_derivation, select_solver_derivation
from plugins.geometry_full2d_v0_4_5.provider import ENGINE_ROLES, engine_output, sha_payload
from scripts.full2d_v0_4_5_corpus_lib import load_manifest, positive_tasks, resolve
from scripts.full2d_v0_4_5_run_checks import write_json


def _write_artifact(run_dir: Path, payload: dict[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    ref = f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"
    write_json(run_dir / "artifacts_v0_4_5" / f"{ref.removeprefix('sha256:')}.json", payload)
    return ref


def run_task(config_path: Path, corpus_root: Path, run_dir: Path, task_id: str, baseline: str) -> dict[str, Any]:
    config = json.loads(resolve(config_path).read_text(encoding="utf-8"))
    manifest = load_manifest(corpus_root)
    task = next((item for item in positive_tasks(manifest) if item.get("task_id") == task_id), None)
    if task is None:
        return {"schema_version": "run_full2d_actual_task_v0_4_5_report_1", "status": "failed", "errors": [f"unknown_or_nonpositive_task:{task_id}"]}
    claim_spec = {"target_expr": task.get("target_expr", ""), "theorem_name": task.get("theorem_name")}
    engine_refs = [_write_artifact(run_dir, engine_output(role, claim_spec)) for role in ENGINE_ROLES]
    engine_outputs = [json.loads((run_dir / "artifacts_v0_4_5" / f"{ref.removeprefix('sha256:')}.json").read_text(encoding="utf-8")) for ref in engine_refs]
    selected = select_solver_derivation(engine_outputs)
    compiler_result = compile_from_selected_derivation(selected)
    compiler_ref = _write_artifact(run_dir, compiler_result)
    final_status = "final_theorem" if compiler_result["status"] == "passed" and baseline == "B2" else "measured_failure"
    record = {
        "schema_version": "ActualTaskPipelineRunV3",
        "run_id": f"actual_full2d_run:v0_4_5:{task_id}:{baseline}",
        "config_hash": sha_payload(config),
        "task_id": task_id,
        "category": task.get("category"),
        "baseline": baseline,
        "engine_output_refs": engine_refs,
        "compiler_result_refs": [compiler_ref],
        "final_status": final_status,
        "event_log": ["provider_engine_before_compiler", "compiler_before_final_verify"],
    }
    write_json(run_dir / "actual_task_pipeline_runs_v0_4_5" / f"{task_id}_{baseline}.json", record)
    return {"schema_version": "run_full2d_actual_task_v0_4_5_report_1", "status": "passed", "record": record}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--corpus-root", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--baseline", required=True)
    args = parser.parse_args()
    report = run_task(Path(args.config), Path(args.corpus_root), Path(args.run_dir), args.task_id, args.baseline)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
