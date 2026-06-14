from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    checked = 0
    for task_result in _task_results(run_dir, errors):
        if not task_result.get("solver_backed_final_theorem"):
            continue
        checked += 1
        label = f"{task_result.get('baseline_id')}:{task_result.get('task_entry_id')}"
        artifact_index = task_result.get("artifact_index", {})
        worker = _read_json(artifact_index.get("worker_result.json"), errors, label)
        source_ref = _read_json(artifact_index.get("source_problem_ref.json"), errors, label)
        generated_ref = _read_json(artifact_index.get("generated_candidate_file_ref.json"), errors, label)
        source_path = Path(str(source_ref.get("source_problem_path") or task_result.get("theorem_file_path", "")))
        generated_path = Path(str(generated_ref.get("generated_candidate_path") or worker.get("worker_output", {}).get("generated_candidate_path", "")))
        if worker.get("patch_applied") is not True:
            errors.append(f"{label}:counted_without_patch_applied")
        if not source_path.exists():
            errors.append(f"{label}:missing_source_problem:{source_path}")
            continue
        if not generated_path.exists():
            errors.append(f"{label}:missing_generated_candidate:{generated_path}")
            continue
        source_text = source_path.read_text(encoding="utf-8")
        generated_text = generated_path.read_text(encoding="utf-8")
        theorem_name = str(task_result.get("theorem_name", "")).rsplit(".", 1)[-1]
        source_region = _region_text(source_text, theorem_name)
        generated_region = _region_text(generated_text, theorem_name)
        if "sorry" not in source_region:
            errors.append(f"{label}:source_region_not_original_sorry_problem")
        if "sorry" in generated_region:
            errors.append(f"{label}:generated_region_still_contains_sorry")
        if source_region == generated_region:
            errors.append(f"{label}:generated_region_unchanged")
    payload = {"status": "failed" if errors else "passed", "checked": checked, "errors": errors}
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


def _read_json(path: str | None, errors: list[str], label: str) -> dict[str, Any]:
    if not path:
        errors.append(f"{label}:missing_artifact_ref")
        return {}
    artifact_path = Path(path)
    if not artifact_path.exists():
        errors.append(f"{label}:missing_artifact_file:{artifact_path}")
        return {}
    return json.loads(artifact_path.read_text(encoding="utf-8"))


def _region_text(text: str, theorem_name: str) -> str:
    start = f"-- MARP_PROOF_REGION_START:{theorem_name}"
    end = f"-- MARP_PROOF_REGION_END:{theorem_name}"
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


if __name__ == "__main__":
    raise SystemExit(main())
