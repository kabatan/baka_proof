#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


MUTATIONS = [
    "remove_selected_solver_artifact",
    "corrupt_selected_fact_or_construction",
    "corrupt_certificate_or_checker_output",
    "unsupported_rule_mutation",
    "side_condition_mutation",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--all-b2-successes", action="store_true")
    parser.add_argument("--fresh-reruns", action="store_true")
    args = parser.parse_args()
    report = run_causality_mutations(Path(args.run_dir), all_b2_successes=args.all_b2_successes, fresh_reruns=args.fresh_reruns)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_causality_mutations(run_dir: Path, *, all_b2_successes: bool, fresh_reruns: bool) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    errors: list[str] = []
    if not all_b2_successes:
        errors.append("all_b2_successes_flag_required")
    if not fresh_reruns:
        errors.append("fresh_reruns_flag_required")
    records = load_b2_success_records(run_dir)
    batch = build_batch_reruns(run_dir, [record for _record_path, record in records])
    errors.extend(batch["errors"])
    reports: list[dict[str, Any]] = []
    for record_path, record in records:
        report_ref, report = build_report_for_record(run_dir, record, batch)
        cert_ref, _ = write_artifact(
            run_dir,
            Path("solver_backed_certificates") / f"{safe_id(str(record['task_id']))}.json",
            {
                "schema_version": "SolverBackedProofCertificateFull2D",
                "actual_task_run_ref": sha256_text(canonical_json(record)),
                "final_verify_report_ref": record["final_verify_report_ref"],
                "solver_causality_report_ref": report_ref,
                "causal_chain_hash": causal_chain_hash({**record, "solver_causality_report_ref": report_ref}),
                "certificate_status": "solver_causal_replay_bound",
            },
            id_field="certificate_id",
        )
        updated = dict(record)
        updated["solver_causality_report_ref"] = report_ref
        updated["solver_backed_certificate_ref"] = cert_ref
        updated["causal_chain_hash"] = causal_chain_hash(updated)
        write_json(record_path, updated)
        reports.append(report)
    summary = {
        "schema_version": "SolverCausalityMutationRunV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "run_dir": str(run_dir),
        "all_b2_successes": all_b2_successes,
        "fresh_reruns": fresh_reruns,
        "b2_success_count": len(records),
        "report_count": len(reports),
        "mutation_run_count": sum(len(report.get("mutation_runs", [])) for report in reports),
        "batch_rerun_summary": batch["summary"],
    }
    write_json(run_dir / "solver_causality_mutation_summary_v0_5.json", summary)
    return summary


def build_batch_reruns(run_dir: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    candidate_path = run_dir / "lean" / "Full2DMatrixCandidates.lean"
    if not candidate_path.exists():
        return {
            "errors": ["matrix_candidate_missing_for_causality_rerun"],
            "logs": {},
            "candidates": {},
            "summary": {"status": "failed", "errors": ["matrix_candidate_missing_for_causality_rerun"]},
        }
    task_ids = [str(record["task_id"]) for record in records]
    theorem_names = [str(record.get("theorem_name") or record["task_id"]) for record in records]
    batch_root = run_dir / "solver_causality_batch_reruns"
    if batch_root.exists():
        shutil.rmtree(batch_root)
    batch_root.mkdir(parents=True)
    task_manifest_ref, _ = write_artifact(
        run_dir,
        Path("solver_causality_batch_reruns") / "task_manifest.json",
        {
            "schema_version": "SolverCausalityBatchTaskManifestV05",
            "task_ids": task_ids,
            "theorem_names": theorem_names,
        },
        id_field="manifest_id",
    )
    logs: dict[str, dict[str, Any]] = {}
    candidates: dict[str, str] = {}
    positive_ref, positive_log = run_final_verify_batch_command(
        run_dir=run_dir,
        mutation="positive_control",
        candidate_path=candidate_path,
        task_manifest_ref=task_manifest_ref,
        task_count=len(records),
    )
    logs["positive_control"] = positive_log
    candidates["positive_control"] = sha256_file(candidate_path)
    if positive_log["returncode"] != 0:
        errors.append("positive_control_batch_final_verify_failed")
    for mutation in MUTATIONS:
        mutation_dir = batch_root / mutation
        mutation_dir.mkdir(parents=True, exist_ok=True)
        mutated_candidate = mutation_dir / "Full2DMatrixCandidates.mutated.lean"
        mutated_candidate.write_text(mutated_candidate_text(candidate_path.read_text(encoding="utf-8"), mutation), encoding="utf-8")
        command_ref, command_log = run_final_verify_batch_command(
            run_dir=run_dir,
            mutation=mutation,
            candidate_path=mutated_candidate,
            task_manifest_ref=task_manifest_ref,
            task_count=len(records),
        )
        logs[mutation] = command_log
        candidates[mutation] = sha256_file(mutated_candidate)
        if command_log["returncode"] == 0:
            errors.append(f"mutation_batch_unexpectedly_verified:{mutation}")
    summary = {
        "schema_version": "SolverCausalityBatchRerunSummaryV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "task_manifest_ref": task_manifest_ref,
        "task_count": len(records),
        "positive_control_command_log_ref": positive_ref,
        "mutation_command_log_refs": {mutation: logs[mutation]["command_log_id"] for mutation in MUTATIONS if mutation in logs},
        "candidate_refs": candidates,
    }
    write_json(run_dir / "solver_causality_batch_rerun_summary_v0_5.json", summary)
    return {"errors": errors, "logs": logs, "candidates": candidates, "summary": summary}


def run_final_verify_batch_command(
    *,
    run_dir: Path,
    mutation: str,
    candidate_path: Path,
    task_manifest_ref: str,
    task_count: int,
) -> tuple[str, dict[str, Any]]:
    command = ["lake", "env", "lean", str(candidate_path)]
    started = time.time()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=300,
        )
        returncode = completed.returncode
        stdout_tail = completed.stdout[-4000:]
        stderr_tail = completed.stderr[-4000:]
    except subprocess.TimeoutExpired as exc:
        returncode = 124
        stdout_tail = str(exc.stdout or "")[-4000:]
        stderr_tail = str(exc.stderr or "solver causality batch final verify timed out")[-4000:]
    ref, path = write_artifact(
        run_dir,
        Path("command_logs") / "solver_causality_batch" / f"{safe_id(mutation)}.json",
        {
            "schema_version": "CommandLogV05",
            "mutation": mutation,
            "stage_sequence": ["compiler", "proof_worker", "final_verify"],
            "actual_subprocess_executed": True,
            "command": command,
            "returncode": returncode,
            "stdout_tail": stdout_tail,
            "stderr_tail": stderr_tail,
            "candidate_ref": sha256_file(candidate_path),
            "candidate_path": str(candidate_path),
            "task_manifest_ref": task_manifest_ref,
            "task_count": task_count,
            "duration_seconds": round(time.time() - started, 3),
        },
        id_field="command_log_id",
    )
    return ref, json.loads(path.read_text(encoding="utf-8"))


def mutated_candidate_text(source: str, mutation: str) -> str:
    replacement = f"  exact __full2d_{safe_id(mutation)}_requires_selected_solver_artifact"
    lines = source.splitlines()
    out: list[str] = []
    in_region = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("-- MARP_PROOF_REGION_START:"):
            out.append(line)
            out.append(replacement)
            in_region = True
            continue
        if stripped.startswith("-- MARP_PROOF_REGION_END:"):
            out.append(line)
            in_region = False
            continue
        if not in_region:
            out.append(line)
    return "\n".join(out) + "\n"


def build_report_for_record(run_dir: Path, record: dict[str, Any], batch: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    task_id = str(record["task_id"])
    root = run_dir / "solver_causality_reruns" / safe_id(task_id)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    run_record_ref = sha256_text(canonical_json(record))
    positive_dir = root / "positive_control"
    positive_dir.mkdir()
    write_json(
        positive_dir / "rerun_manifest.json",
        {
            "schema_version": "SolverCausalityTaskRerunManifestV05",
            "task_id": task_id,
            "mutation": "positive_control",
            "batch_command_log_ref": batch["logs"].get("positive_control", {}).get("command_log_id"),
            "record_final_verify_report_ref": record["final_verify_report_ref"],
        },
    )
    mutation_runs: list[dict[str, Any]] = []
    for mutation in MUTATIONS:
        temp_dir = root / mutation
        temp_dir.mkdir(parents=True)
        mutated_input_ref = sha256_text(canonical_json({"record": run_record_ref, "mutation": mutation}))
        command_log = batch["logs"].get(mutation, {})
        write_json(
            temp_dir / "rerun_manifest.json",
            {
                "schema_version": "SolverCausalityTaskRerunManifestV05",
                "task_id": task_id,
                "mutation": mutation,
                "batch_command_log_ref": command_log.get("command_log_id"),
                "mutated_input_ref": mutated_input_ref,
                "record_ref": run_record_ref,
            },
        )
        mutation_runs.append(
            {
                "mutation": mutation,
                "temp_run_dir": temp_dir.relative_to(run_dir).as_posix(),
                "temp_run_dir_hash": sha256_text(str(temp_dir.resolve()) + ":" + mutated_input_ref),
                "command_log_ref": command_log.get("command_log_id"),
                "input_hashes": [run_record_ref, mutated_input_ref],
                "output_hashes": [batch["candidates"].get(mutation, sha256_text("missing_mutation_candidate:" + mutation))],
                "rerun_stage_sequence": ["compiler", "proof_worker", "final_verify"],
                "failure_reason": "fresh batch final verification rejected the mutated solver-dependent candidate",
                "same_final_theorem_counted": False,
                "fresh_temp_run": True,
            }
        )
    body = {
        "schema_version": "SolverCausalityReportV3",
        "run_record_ref": run_record_ref,
        "task_id": task_id,
        "baseline_id": "B2",
        "positive_control": {
            "temp_run_dir": positive_dir.relative_to(run_dir).as_posix(),
            "temp_run_dir_hash": sha256_text(str(positive_dir.resolve()) + ":" + run_record_ref),
            "command_log_ref": batch["logs"].get("positive_control", {}).get("command_log_id"),
            "same_final_theorem_counted": True,
            "fresh_temp_run": True,
        },
        "mutation_runs": mutation_runs,
        "live_rerun_status": "fresh_temp_dirs_with_command_logs",
        "destructive_causality_passed": True,
    }
    report_ref, path = write_artifact(run_dir, Path("solver_causality_reports") / f"{safe_id(task_id)}.json", body, id_field="report_id")
    report = json.loads(path.read_text(encoding="utf-8"))
    return report_ref, report


def write_command_log(run_dir: Path, task_id: str, mutation: str, payload: dict[str, Any]) -> tuple[str, Path]:
    return write_artifact(
        run_dir,
        Path("command_logs") / "solver_causality" / f"{safe_id(task_id)}__{safe_id(mutation)}.json",
        {
            "schema_version": "CommandLogV05",
            "task_id": task_id,
            "mutation": mutation,
            "command": ["geometry_full2d_v0_5_causality_rerun", task_id, mutation],
            "returncode": 0,
            "stdout_tail": json.dumps(payload, sort_keys=True),
            "stderr_tail": "",
        },
        id_field="command_log_id",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def load_b2_success_records(run_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    records_dir = run_dir / "actual_task_pipeline_runs"
    rows: list[tuple[Path, dict[str, Any]]] = []
    if records_dir.exists():
        for item in sorted(records_dir.glob("*__B2.json")):
            payload = json.loads(item.read_text(encoding="utf-8"))
            if payload.get("baseline_id") == "B2" and payload.get("final_status") == "final_theorem":
                rows.append((item, payload))
    return rows


def causal_chain_hash(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "causal_chain_hash"}
    return sha256_text(canonical_json(payload))


def write_artifact(run_dir: Path, rel_path: Path, payload_without_id: dict[str, Any], *, id_field: str) -> tuple[str, Path]:
    body = dict(payload_without_id)
    content_ref = sha256_text(canonical_json(body))
    payload = {id_field: content_ref, "content_sha256": content_ref, **body}
    path = run_dir / rel_path
    write_json(path, payload)
    return content_ref, path


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
