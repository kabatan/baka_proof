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


REQUIRED_BASELINES = {"B1", "B2", "B5", "B6", "B7", "B8"}
INTENDED_DISABLED = {
    "B1": ("geometry_solver", ()),
    "B2": ("none", ()),
    "B5": ("construction_search", ("construction_search",)),
    "B6": ("algebraic_geometry", ("algebraic_geometry",)),
    "B7": ("order_case", ("order_case",)),
    "B8": ("model_provider", ()),
}
INVARIANT_FIELDS = (
    "final_verify_enabled",
    "proof_worker_enabled",
    "source_theorem_visibility",
    "lean_library_access",
    "resource_class",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--config", default="configs/benchmark_runs/geometry_full2d_v0_4_3.yaml")
    args = parser.parse_args()
    report = check_baseline_comparability(Path(args.run_dir), Path(args.config))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_baseline_comparability(run_dir: Path, config_path: Path) -> dict[str, Any]:
    run_dir = _resolve(run_dir)
    config_path = _resolve(config_path)
    errors: list[str] = []
    config = _read_json(config_path, errors)
    baselines = _baselines_by_id(config, errors)
    errors.extend(_validate_baseline_config(baselines))
    matrix_report = _read_optional_json(run_dir / "baseline_comparability_report.json", errors)
    if matrix_report is None:
        errors.append("missing_baseline_comparability_report")
    else:
        if matrix_report.get("config_hash") != _sha_file(config_path):
            errors.append("baseline_comparability_config_hash_mismatch")
        reported = matrix_report.get("baselines", {})
        if not isinstance(reported, dict) or set(reported) != REQUIRED_BASELINES:
            errors.append("baseline_comparability_report_baselines_mismatch")
        if matrix_report.get("final_verify_same") is not True:
            errors.append("baseline_comparability_final_verify_not_same")
        if matrix_report.get("proof_worker_same") is not True:
            errors.append("baseline_comparability_proof_worker_not_same")
        if matrix_report.get("lean_library_access_same") is not True:
            errors.append("baseline_comparability_lean_library_access_not_same")
    direct_report_errors = _check_direct_lemma_b1_counting(run_dir)
    errors.extend(direct_report_errors)
    return {
        "schema_version": "1.0.0",
        "status": "passed" if not errors else "failed",
        "run_dir": str(run_dir),
        "baseline_comparability_summary": {
            "required_baselines": sorted(REQUIRED_BASELINES),
            "config_hash": _sha_file(config_path) if config_path.exists() else None,
            "baseline_count": len(baselines),
            "matrix_report_present": matrix_report is not None,
        },
        "errors": sorted(set(errors)),
    }


def _validate_baseline_config(baselines: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_BASELINES - set(baselines))
    if missing:
        errors.append(f"missing_required_baselines:{','.join(missing)}")
        return errors
    b2 = baselines["B2"]
    for baseline_id in sorted(REQUIRED_BASELINES):
        baseline = baselines[baseline_id]
        intended_component, intended_roles = INTENDED_DISABLED[baseline_id]
        if baseline.get("disabled_component") != intended_component:
            errors.append(f"{baseline_id}:disabled_component_mismatch:{baseline.get('disabled_component')}!={intended_component}")
        roles = tuple(str(role) for role in baseline.get("disabled_engine_roles", []))
        if roles != intended_roles:
            errors.append(f"{baseline_id}:disabled_engine_roles_mismatch:{roles}!={intended_roles}")
        for field in INVARIANT_FIELDS:
            if baseline.get(field) != b2.get(field):
                errors.append(f"{baseline_id}:invariant_field_mismatch:{field}")
        if baseline.get("final_verify_enabled") is not True:
            errors.append(f"{baseline_id}:final_verify_disabled")
        if baseline.get("proof_worker_enabled") is not True:
            errors.append(f"{baseline_id}:proof_worker_disabled")
        if baseline_id == "B1" and baseline.get("uses_geometry_solve") is not False:
            errors.append("B1:geometry_solver_not_disabled")
        if baseline_id != "B1" and baseline.get("uses_geometry_solve") is not True:
            errors.append(f"{baseline_id}:geometry_solver_unexpectedly_disabled")
    return errors


def _check_direct_lemma_b1_counting(run_dir: Path) -> list[str]:
    records = _iter_run_records(run_dir)
    if not records:
        return []
    by_task_baseline = {(record.get("task_id"), record.get("baseline_id")): record for record in records}
    errors: list[str] = []
    for record in records:
        if record.get("baseline_id") != "B2" or record.get("final_status") != "final_theorem":
            continue
        if not _certificate_says_direct_lemma(record, run_dir):
            continue
        b1 = by_task_baseline.get((record.get("task_id"), "B1"))
        if b1 is None:
            errors.append(f"{record.get('task_id')}:direct_lemma_b1_record_missing")
        elif b1.get("final_status") != "final_theorem":
            errors.append(f"{record.get('task_id')}:direct_lemma_b1_success_not_counted")
    return errors


def _certificate_says_direct_lemma(record: dict[str, Any], run_dir: Path) -> bool:
    artifact_paths = record.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        return False
    ref = record.get("solver_backed_certificate_ref")
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        return False
    path = Path(path_value)
    if not path.is_absolute():
        path = run_dir / path
    if not path.exists():
        return False
    try:
        cert = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return cert.get("direct_lean_lemma_baseline_expected") is True


def _iter_run_records(run_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    records_dir = run_dir / "actual_task_pipeline_runs"
    if records_dir.exists():
        for path in sorted(records_dir.glob("*.json")):
            payload = _read_json(path, [])
            if isinstance(payload, dict):
                records.append(payload)
    jsonl_path = run_dir / "actual_task_pipeline_runs.jsonl"
    if jsonl_path.exists():
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                payload = json.loads(line)
                if isinstance(payload, dict):
                    records.append(payload)
    return records


def _baselines_by_id(config: dict[str, Any] | None, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(config, dict):
        return {}
    baselines = config.get("baselines", [])
    if not isinstance(baselines, list):
        errors.append("config_baselines_not_list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for baseline in baselines:
        if isinstance(baseline, dict) and baseline.get("baseline_id"):
            result[str(baseline["baseline_id"])] = baseline
    return result


def _read_optional_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _read_json(path, errors)


def _read_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"missing_json:{path}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}:json_error:{exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{path}:not_object")
        return None
    return payload


def _sha_file(path: Path) -> str:
    if not path.exists():
        return ""
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
