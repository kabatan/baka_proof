#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
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

from plugins.geometry_full2d.compiler_v0_5 import run_compiler_cli
from plugins.geometry_full2d.proof_worker_v0_5 import apply_lean_patch_candidate_full2d_v0_5


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
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    args = parser.parse_args()
    report = run_causality_mutations(Path(args.run_dir), all_b2_successes=args.all_b2_successes, fresh_reruns=args.fresh_reruns, workers=args.workers)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_causality_mutations(run_dir: Path, *, all_b2_successes: bool, fresh_reruns: bool, workers: int) -> dict[str, Any]:
    run_dir = resolve(run_dir)
    errors: list[str] = []
    if not all_b2_successes:
        errors.append("all_b2_successes_flag_required")
    if not fresh_reruns:
        errors.append("fresh_reruns_flag_required")
    records = load_b2_success_records(run_dir)
    rerun_root = run_dir / "solver_causality_task_reruns"
    if rerun_root.exists():
        shutil.rmtree(rerun_root)
    rerun_root.mkdir(parents=True)
    registry_path = run_dir / "rule_registry" / "rule_registry_full2d.json"
    reports: list[dict[str, Any]] = []
    task_results: list[dict[str, Any]] = []
    worker_count = max(1, int(workers))
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [
            executor.submit(process_causality_record, run_dir, rerun_root, registry_path, record_path, record)
            for record_path, record in records
        ]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            task_results.append(result)
            errors.extend(f"{result.get('task_id', 'unknown')}:{error}" for error in result.get("errors", []))
            report = result.get("report")
            if isinstance(report, dict):
                reports.append(report)
    summary = {
        "schema_version": "SolverCausalityMutationRunV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "run_dir": str(run_dir),
        "all_b2_successes": all_b2_successes,
        "fresh_reruns": fresh_reruns,
        "worker_count": worker_count,
        "b2_success_count": len(records),
        "report_count": len(reports),
        "mutation_run_count": sum(len(report.get("mutation_runs", [])) for report in reports),
        "task_rerun_count": sum(result.get("rerun_count", 0) for result in task_results),
        "task_results": sorted(task_results, key=lambda item: str(item.get("task_id")))[:20],
    }
    write_json(run_dir / "solver_causality_mutation_summary_v0_5.json", summary)
    return summary


def process_causality_record(
    run_dir: Path,
    rerun_root: Path,
    registry_path: Path,
    record_path: Path,
    record: dict[str, Any],
) -> dict[str, Any]:
    task_id = str(record["task_id"])
    errors: list[str] = []
    task_rerun = build_task_rerun_inputs(run_dir, rerun_root, record, registry_path)
    errors.extend(task_rerun["errors"])
    report_ref, report = build_report_for_record(run_dir, record, task_rerun)
    if report.get("destructive_causality_passed") is not True:
        errors.append("destructive_causality_not_passed")
    cert_ref, _ = write_artifact(
        run_dir,
        Path("solver_backed_certificates") / f"{safe_id(task_id)}.json",
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
    return {
        "task_id": task_id,
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "report": report,
        "rerun_count": len(task_rerun.get("runs", {})),
    }


def build_task_rerun_inputs(run_dir: Path, rerun_root: Path, record: dict[str, Any], registry_path: Path) -> dict[str, Any]:
    task_id = str(record["task_id"])
    theorem_name = str(record.get("theorem_name") or task_id)
    source_record_path = run_dir / "source_theorems" / f"{safe_id(task_id)}.json"
    claim_path = run_dir / "claim_specs" / f"{safe_id(task_id)}.json"
    derivation_path = run_dir / "selected_solver_derivations" / f"{safe_id(task_id)}.json"
    errors: list[str] = []
    missing_inputs = [path for path in [source_record_path, claim_path, derivation_path, registry_path] if not path.exists()]
    if missing_inputs:
        return {"errors": [f"missing_rerun_input:{path.relative_to(run_dir).as_posix()}" for path in missing_inputs], "runs": {}}
    source_record = read_json(source_record_path)
    formal_statement = str(source_record.get("formal_statement", ""))
    header = formal_statement.split(":= by", 1)[0].strip()
    if not header:
        return {"errors": ["source_theorem_header_missing"], "runs": {}}
    base_derivation = read_json(derivation_path)
    task_manifest_ref, _ = write_artifact(
        run_dir,
        Path("solver_causality_task_reruns") / "task_manifests" / f"{safe_id(task_id)}.json",
        {
            "schema_version": "SolverCausalityTaskManifestV05",
            "task_id": task_id,
            "theorem_name": theorem_name,
            "run_record_ref": sha256_text(canonical_json(record)),
        },
        id_field="manifest_id",
    )
    runs: dict[str, dict[str, Any]] = {}
    for mutation in ["positive_control", *MUTATIONS]:
        temp_dir = rerun_root / "tasks" / safe_id(task_id) / safe_id(mutation)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True)
        source_path = temp_dir / "Source.lean"
        source_path.write_text(single_theorem_source(header, theorem_name, "  sorry"), encoding="utf-8")
        selected = mutate_selected_derivation(base_derivation, mutation)
        selected_path = temp_dir / "selected_solver_derivation.json"
        write_json(selected_path, selected)
        side_refs = tuple(str(ref) for ref in record.get("independent_checker_report_refs", [])[:2])
        if mutation == "side_condition_mutation":
            side_refs = ("bad_side_condition_ref",)
        compiler_summary = run_compiler_cli(
            claim_spec_json=claim_path,
            selected_derivation_json=selected_path,
            rule_registry_json=registry_path,
            output_dir=temp_dir / "compiler_run",
            claim_spec_ref=str(record.get("claim_spec_ref")),
            selected_derivation_ref=sha256_file(selected_path),
            rule_registry_ref=str(record.get("rule_registry_ref") or sha256_file(registry_path)),
            side_condition_checker_refs=side_refs,
        )
        compiler_result_path = temp_dir / "compiler_run" / "compiler_stage" / "compiler_result.json"
        compiler_result = read_json(compiler_result_path) if compiler_result_path.exists() else {}
        compiler_ref = str(compiler_summary.get("compiler_result_ref") or sha256_text(canonical_json(compiler_summary)))
        proof_text = str(compiler_result.get("proof_text", ""))
        if compiler_summary.get("status") != "passed" or not proof_text:
            proof_text = f"exact __full2d_{safe_id(mutation)}_requires_selected_solver_artifact"
        patch = make_rerun_patch_candidate(
            compiler_result_ref=compiler_ref,
            theorem_name=theorem_name,
            patch_text=indent_proof_text(proof_text),
            solver_dependency_refs=(str(record.get("selected_solver_derivation_ref")), *side_refs),
        )
        patch_path = temp_dir / "lean_patch_candidate.json"
        write_json(patch_path, patch)
        worker = apply_lean_patch_candidate_full2d_v0_5(
            source_path=source_path,
            patch_candidate=patch,
            output_dir=temp_dir / "proof_worker_run",
            run_id=mutation,
            task_id=task_id,
        )
        candidate_path = Path(str(worker.get("generated_candidate_path") or ""))
        if not candidate_path.exists():
            fallback = temp_dir / "Candidate.failed.lean"
            fallback.write_text(single_theorem_source(header, theorem_name, f"  exact __full2d_{safe_id(mutation)}_proof_worker_failed"), encoding="utf-8")
            candidate_path = fallback
        command_ref, command_log = run_final_verify_task_command(
            run_dir=run_dir,
            task_id=task_id,
            theorem_name=theorem_name,
            mutation=mutation,
            candidate_path=candidate_path,
            task_manifest_ref=task_manifest_ref,
        )
        same_final = command_log.get("returncode") == 0
        if mutation == "positive_control" and not same_final:
            errors.append("positive_control_final_verify_failed")
        if mutation != "positive_control" and same_final:
            errors.append(f"mutation_unexpectedly_verified:{mutation}")
        runs[mutation] = {
            "temp_run_dir": temp_dir.relative_to(run_dir).as_posix(),
            "temp_run_dir_hash": hash_directory(temp_dir),
            "compiler_status": compiler_summary.get("status"),
            "compiler_errors": compiler_summary.get("errors", []),
            "compiler_summary_ref": sha256_text(canonical_json(compiler_summary)),
            "proof_worker_status": worker.get("status"),
            "proof_worker_errors": worker.get("errors", []),
            "proof_worker_result_ref": str(worker.get("worker_result_id") or sha256_text(canonical_json(worker))),
            "input_hashes": [sha256_file(claim_path), sha256_file(selected_path), sha256_file(registry_path)],
            "output_hashes": [sha256_file(candidate_path), str(worker.get("worker_result_id") or sha256_text(canonical_json(worker))), command_ref],
            "candidate_ref": sha256_file(candidate_path),
            "command_log_ref": command_ref,
            "command_log_returncode": command_log.get("returncode"),
            "same_final_theorem_counted": same_final,
        }
    return {"errors": errors, "runs": runs}


def mutate_selected_derivation(base_derivation: dict[str, Any], mutation: str) -> dict[str, Any]:
    selected = json.loads(canonical_json(base_derivation))
    if mutation == "positive_control":
        return selected
    if mutation == "remove_selected_solver_artifact":
        selected["selected_engine_output_refs"] = []
        selected["selected_facts"] = []
        selected["selected_constructions"] = []
        selected["selected_certificates"] = []
        selected["derivation_steps"] = []
        return selected
    if mutation == "corrupt_selected_fact_or_construction":
        selected["selected_facts"] = ["fact:corrupted_selected_solver_fact"]
        application = selected.get("checked_rule_application")
        bindings = application.get("arguments") if isinstance(application, dict) else {}
        if isinstance(bindings, dict):
            for key in ["h", "h0", "h1", "A", "r"]:
                if key in bindings:
                    bindings[key] = "__full2d_corrupted_binding"
                    break
        return selected
    if mutation == "corrupt_certificate_or_checker_output":
        for step in selected.get("derivation_steps", []):
            if isinstance(step, dict):
                step["independent_checker_report_ref"] = "corrupted_checker_output_ref"
        selected["selected_certificates"] = ["certificate:corrupted_checker_output"]
        selected["checked_rule_application_ref"] = "corrupted_checker_output_ref"
        return selected
    if mutation == "unsupported_rule_mutation":
        for step in selected.get("derivation_steps", []):
            if isinstance(step, dict):
                step["rule_id"] = "full2d_rule:unsupported_mutation:99"
                break
        return selected
    if mutation == "side_condition_mutation":
        selected["side_condition_mutation_marker"] = "invalid_side_condition_checker_ref_required"
        return selected
    return selected


def make_rerun_patch_candidate(
    *,
    compiler_result_ref: str,
    theorem_name: str,
    patch_text: str,
    solver_dependency_refs: tuple[str, ...],
) -> dict[str, Any]:
    body = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": compiler_result_ref,
        "theorem_name": theorem_name,
        "target_theorem_name": theorem_name,
        "proof_region_only": True,
        "allowed_edit_region": {
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
            "policy": "MARP proof region only",
        },
        "patch_text": patch_text,
        "proof_region_replacement_text": patch_text,
        "solver_dependency_refs": list(solver_dependency_refs),
        "proof_use_status": "lean_patch_candidate",
        "status": "lean_patch_candidate",
    }
    patch_id = sha256_text(canonical_json(body))
    return {"patch_id": patch_id, "content_sha256": patch_id, **body}


def indent_proof_text(proof_text: str) -> str:
    return "\n".join(("  " + line) if line else "" for line in proof_text.splitlines())


def single_theorem_source(header: str, theorem_name: str, proof_text: str) -> str:
    return "\n".join(
        [
            "import MathAutoResearch.GeometryFull2D.Inequality",
            "",
            "namespace MathAutoResearch.GeometryFull2D",
            "",
            f"{header} := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            proof_text,
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
            "end MathAutoResearch.GeometryFull2D",
            "",
        ]
    )


def run_final_verify_task_command(
    *,
    run_dir: Path,
    task_id: str,
    theorem_name: str,
    mutation: str,
    candidate_path: Path,
    task_manifest_ref: str,
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
        stderr_tail = str(exc.stderr or "solver causality task final verify timed out")[-4000:]
    ref, path = write_artifact(
        run_dir,
        Path("command_logs") / "solver_causality" / f"{safe_id(task_id)}__{safe_id(mutation)}.json",
        {
            "schema_version": "CommandLogV05",
            "task_id": task_id,
            "theorem_name": theorem_name,
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
            "task_count": 1,
            "duration_seconds": round(time.time() - started, 3),
        },
        id_field="command_log_id",
    )
    return ref, json.loads(path.read_text(encoding="utf-8"))


def build_report_for_record(run_dir: Path, record: dict[str, Any], task_rerun: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    task_id = str(record["task_id"])
    run_record_ref = sha256_text(canonical_json(record))
    runs_by_mutation = task_rerun.get("runs", {}) if isinstance(task_rerun, dict) else {}
    positive_run = runs_by_mutation.get("positive_control", {})
    mutation_runs: list[dict[str, Any]] = []
    for mutation in MUTATIONS:
        stage_run = runs_by_mutation.get(mutation, {})
        same_final = stage_run.get("same_final_theorem_counted") is True
        mutation_runs.append(
            {
                "mutation": mutation,
                "temp_run_dir": stage_run.get("temp_run_dir"),
                "temp_run_dir_hash": stage_run.get("temp_run_dir_hash"),
                "command_log_ref": stage_run.get("command_log_ref"),
                "input_hashes": [run_record_ref, *stage_run.get("input_hashes", [])],
                "output_hashes": [*stage_run.get("output_hashes", []), stage_run.get("candidate_ref", sha256_text("missing_mutation_candidate:" + mutation))],
                "rerun_stage_sequence": ["compiler", "proof_worker", "final_verify"],
                "compiler_status": stage_run.get("compiler_status"),
                "compiler_errors": stage_run.get("compiler_errors", []),
                "proof_worker_status": stage_run.get("proof_worker_status"),
                "proof_worker_errors": stage_run.get("proof_worker_errors", []),
                "failure_reason": mutation_failure_reason(stage_run),
                "same_final_theorem_counted": same_final,
                "fresh_temp_run": True,
            }
        )
    positive_same_final = positive_run.get("same_final_theorem_counted") is True
    destructive_passed = positive_same_final and all(item.get("same_final_theorem_counted") is False for item in mutation_runs) and not task_rerun.get("errors")
    body = {
        "schema_version": "SolverCausalityReportV3",
        "run_record_ref": run_record_ref,
        "task_id": task_id,
        "baseline_id": "B2",
        "positive_control": {
            "temp_run_dir": positive_run.get("temp_run_dir"),
            "temp_run_dir_hash": positive_run.get("temp_run_dir_hash"),
            "command_log_ref": positive_run.get("command_log_ref"),
            "same_final_theorem_counted": positive_same_final,
            "fresh_temp_run": True,
            "input_hashes": [run_record_ref, *positive_run.get("input_hashes", [])],
            "output_hashes": [*positive_run.get("output_hashes", []), positive_run.get("candidate_ref", sha256_text("missing_positive_candidate"))],
            "rerun_stage_sequence": ["compiler", "proof_worker", "final_verify"],
            "compiler_status": positive_run.get("compiler_status"),
            "proof_worker_status": positive_run.get("proof_worker_status"),
        },
        "mutation_runs": mutation_runs,
        "live_rerun_status": "fresh_temp_dirs_with_command_logs",
        "destructive_causality_passed": destructive_passed,
        "task_rerun_errors": task_rerun.get("errors", []),
    }
    report_ref, path = write_artifact(run_dir, Path("solver_causality_reports") / f"{safe_id(task_id)}.json", body, id_field="report_id")
    report = json.loads(path.read_text(encoding="utf-8"))
    return report_ref, report


def mutation_failure_reason(stage_run: dict[str, Any]) -> str:
    compiler_status = stage_run.get("compiler_status")
    if compiler_status != "passed":
        return "compiler rejected mutated SelectedSolverDerivationV2 before proof generation"
    if stage_run.get("proof_worker_status") != "patch_applied":
        return "ProofWorker rejected mutated compiler patch candidate"
    if stage_run.get("command_log_returncode") != 0:
        return "FinalVerifyGate rejected solver-mutated candidate"
    return "mutation did not block final verification"


def hash_directory(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
