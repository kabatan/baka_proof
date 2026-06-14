from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TARGET_BASELINES = {"B2", "B4"}
PROOF_USE_ARTIFACTS = {
    "extraction_report.json",
    "provider_run_manifest.json",
    "provider_result.json",
    "trace_compilation_result.json",
    "construction_candidate.json",
    "construction_compilation_result.json",
    "lean_patch_candidate.json",
    "worker_result.json",
    "final_verify_report.json",
    "solver_backed_proof_certificate.json",
}
FIXTURE_TOKENS = (
    "GEOMETRY_FINAL_VERIFY_FIXTURE",
    "def Point := Unit",
    "def Coll",
    "ToyGeometry",
    "LocalToyGeometry",
    "toy_geometry",
    "fixture_provider",
    "provider_run_manifest:fixture",
    "trace_compiler_fixture",
    "construction_compiler_fixture",
    "legacy_collinearity_identity_fixture",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir)
    errors: list[str] = []
    checked = 0
    for task_result in _task_results(run_dir, errors):
        baseline_id = str(task_result.get("baseline_id"))
        if baseline_id not in TARGET_BASELINES or not task_result.get("solver_backed_final_theorem"):
            continue
        checked += 1
        _check_task(task_result, errors)
    payload = {"status": "failed" if errors else "passed", "checked": checked, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if errors else 0


def _check_task(task_result: dict[str, Any], errors: list[str]) -> None:
    label = f"{task_result.get('baseline_id')}:{task_result.get('task_entry_id')}"
    artifact_index = task_result.get("artifact_index", {})
    provider_manifest = _read_json(artifact_index.get("provider_run_manifest.json"), errors, label)
    certificate = _read_json(artifact_index.get("solver_backed_proof_certificate.json"), errors, label)
    if provider_manifest.get("fixture_flag") is True:
        errors.append(f"{label}:provider_manifest_fixture_flag")
    if provider_manifest.get("real_integration_flag") is not True:
        errors.append(f"{label}:provider_manifest_not_real_integration")
    engine_runs = provider_manifest.get("engine_runs", [])
    if not engine_runs:
        errors.append(f"{label}:provider_manifest_missing_engine_runs")
    for index, engine_run in enumerate(engine_runs):
        if not isinstance(engine_run, dict):
            errors.append(f"{label}:engine_run_{index}_not_object")
            continue
        if engine_run.get("fixture_flag") is True:
            errors.append(f"{label}:engine_run_{index}_fixture_flag")
        if engine_run.get("real_integration_flag") is not True:
            errors.append(f"{label}:engine_run_{index}_not_real_integration")
        for field in ("adapter_version", "engine_version", "engine_family", "diagnostic_ref", "normalized_output_ref"):
            value = str(engine_run.get(field, ""))
            if "fixture" in value.lower():
                errors.append(f"{label}:engine_run_{index}_{field}_fixture:{value}")

    solver_artifact = certificate.get("normalized_solver_artifact", {})
    source_role = solver_artifact.get("source_engine_role")
    solver_ref = solver_artifact.get("ref")
    if not any(
        isinstance(run, dict)
        and run.get("engine_role") == source_role
        and run.get("normalized_output_ref") == solver_ref
        for run in engine_runs
    ):
        errors.append(f"{label}:missing_solver_artifact_engine_run:{source_role}:{solver_ref}")

    for name in PROOF_USE_ARTIFACTS:
        path = artifact_index.get(name)
        if not path:
            continue
        _check_no_fixture_json(Path(path), errors, label, name)
    for name in ("source_problem_ref.json", "generated_candidate_file_ref.json"):
        ref = _read_json(artifact_index.get(name), errors, label)
        for path_value in _artifact_paths(ref):
            _check_no_fixture_text(Path(path_value), errors, label)
    if _uses_run_fixture(task_result, artifact_index):
        errors.append(f"{label}:run_fixture_artifact_path")


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


def _artifact_paths(payload: dict[str, Any]) -> tuple[str, ...]:
    paths: list[str] = []
    for key, value in payload.items():
        if key.endswith("_path") and isinstance(value, str) and value:
            paths.append(value)
    return tuple(paths)


def _check_no_fixture_json(path: Path, errors: list[str], label: str, name: str) -> None:
    if not path.exists():
        errors.append(f"{label}:missing_artifact_file:{path}")
        return
    text = path.read_text(encoding="utf-8")
    for token in FIXTURE_TOKENS:
        if token in text:
            errors.append(f"{label}:fixture_token:{name}:{token}")


def _check_no_fixture_text(path: Path, errors: list[str], label: str) -> None:
    if not path.exists() or not path.is_file():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    for token in FIXTURE_TOKENS:
        if token in text:
            errors.append(f"{label}:fixture_token:{path}:{token}")
    if re.search(r"\brun_fixture\s*\(", text):
        errors.append(f"{label}:run_fixture_token:{path}")


def _uses_run_fixture(task_result: dict[str, Any], artifact_index: dict[str, Any]) -> bool:
    haystack = json.dumps({"task_result": task_result, "artifact_index": artifact_index}, sort_keys=True)
    return "run_fixture" in haystack or "GEOMETRY_FINAL_VERIFY_FIXTURE" in haystack


if __name__ == "__main__":
    raise SystemExit(main())
