from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_COUNTED_ARTIFACTS = {
    "source_problem_ref.json",
    "generated_candidate_file_ref.json",
    "lean_patch_candidate.json",
    "worker_result.json",
    "final_verify_report.json",
    "solver_backed_proof_certificate.json",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    counted = 0
    for task_result in _task_results(run_dir, errors):
        if not task_result.get("solver_backed_final_theorem"):
            continue
        counted += 1
        label = f"{task_result.get('baseline_id')}:{task_result.get('task_entry_id')}"
        artifact_index = task_result.get("artifact_index", {})
        missing = sorted(REQUIRED_COUNTED_ARTIFACTS - set(artifact_index))
        if missing:
            errors.append(f"{label}:missing_artifacts:{','.join(missing)}")
            continue
        final_report = _read_json(artifact_index["final_verify_report.json"], errors, label)
        certificate = _read_json(artifact_index["solver_backed_proof_certificate.json"], errors, label)
        worker = _read_json(artifact_index["worker_result.json"], errors, label)
        if final_report.get("proof_use_status") != "final_theorem":
            errors.append(f"{label}:final_verify_not_final_theorem")
        if final_report.get("solver_backed_proof_status") != "passed":
            errors.append(f"{label}:solver_backed_proof_status_not_passed")
        if worker.get("patch_applied") is not True:
            errors.append(f"{label}:patch_not_applied")
        if certificate.get("certificate_id") != task_result.get("solver_backed_proof_certificate_ref"):
            errors.append(f"{label}:certificate_ref_mismatch")
    payload = {"status": "failed" if errors else "passed", "counted": counted, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


def _task_results(run_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    index_path = run_dir / "per_task_artifact_index.json"
    if not index_path.exists():
        errors.append("missing_per_task_artifact_index")
        return []
    index = json.loads(index_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for label, path in sorted(index.items()):
        task_path = Path(path)
        if not task_path.exists():
            errors.append(f"{label}:missing_task_result")
            continue
        results.append(json.loads(task_path.read_text(encoding="utf-8")))
    return results


def _read_json(path: str, errors: list[str], label: str) -> dict[str, Any]:
    artifact_path = Path(path)
    if not artifact_path.exists():
        errors.append(f"{label}:missing_artifact_file:{artifact_path}")
        return {}
    return json.loads(artifact_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
