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

from scripts.check_full2d_baseline_comparability import REQUIRED_BASELINES  # noqa: E402
from scripts.check_full2d_corpus_manifest_v0_4_3 import (  # noqa: E402
    canonical_manifest_hash,
    check_corpus_manifest_v0_4_3,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    report = run_matrix(Path(args.config), Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_matrix(config_path: Path, run_dir: Path) -> dict[str, Any]:
    config_path = _resolve(config_path)
    run_dir = _resolve(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    config = _read_json(config_path, errors)
    corpus_root = _resolve(Path(str(config.get("benchmark_corpus_root", "benchmarks/geometry_full2d")))) if isinstance(config, dict) else ROOT / "benchmarks" / "geometry_full2d"
    corpus_manifest = _read_json(corpus_root / "corpus_manifest.json", errors)
    corpus_report = check_corpus_manifest_v0_4_3(corpus_root)
    baseline_report = _write_baseline_comparability_report(run_dir, config_path, config)
    records = _load_run_records(run_dir)
    record_summary = _record_summary(records)
    matrix_errors = list(errors)
    if corpus_report["status"] != "passed":
        matrix_errors.extend(f"corpus:{error}" for error in corpus_report.get("errors", []))
    if not records:
        matrix_errors.append("no_actual_task_pipeline_runs_available_for_matrix")
    summary = {
        "schema_version": "1.0.0",
        "matrix_id": config.get("matrix_id") if isinstance(config, dict) else None,
        "run_id": config.get("run_id") if isinstance(config, dict) else None,
        "status": "passed" if not matrix_errors else "failed",
        "config_path": str(config_path),
        "config_hash": _sha_file(config_path),
        "corpus_root": str(corpus_root),
        "corpus_manifest_hash": canonical_manifest_hash(corpus_manifest) if isinstance(corpus_manifest, dict) else None,
        "sidecar_overlay_used": False,
        "actual_task_pipeline_run_summary": record_summary,
        "baseline_comparability_summary": baseline_report["baseline_comparability_summary"],
        "corpus_summary": corpus_report.get("corpus_summary", {}),
        "errors": sorted(set(matrix_errors)),
    }
    (run_dir / "matrix_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def _write_baseline_comparability_report(run_dir: Path, config_path: Path, config: dict[str, Any] | None) -> dict[str, Any]:
    baselines = {}
    if isinstance(config, dict) and isinstance(config.get("baselines"), list):
        for baseline in config["baselines"]:
            if isinstance(baseline, dict) and baseline.get("baseline_id") in REQUIRED_BASELINES:
                baselines[str(baseline["baseline_id"])] = {
                    "disabled_component": baseline.get("disabled_component"),
                    "disabled_engine_roles": baseline.get("disabled_engine_roles", []),
                    "final_verify_enabled": baseline.get("final_verify_enabled"),
                    "proof_worker_enabled": baseline.get("proof_worker_enabled"),
                    "source_theorem_visibility": baseline.get("source_theorem_visibility"),
                    "lean_library_access": baseline.get("lean_library_access"),
                    "resource_class": baseline.get("resource_class"),
                }
    report = {
        "schema_version": "1.0.0",
        "report_id": "BaselineComparabilityReportV1:" + _sha_text(json.dumps(baselines, sort_keys=True)),
        "config_hash": _sha_file(config_path),
        "baselines": baselines,
        "final_verify_same": len({item.get("final_verify_enabled") for item in baselines.values()}) == 1,
        "proof_worker_same": len({item.get("proof_worker_enabled") for item in baselines.values()}) == 1,
        "source_theorem_visibility_same": len({item.get("source_theorem_visibility") for item in baselines.values()}) == 1,
        "lean_library_access_same": len({item.get("lean_library_access") for item in baselines.values()}) == 1,
        "resource_class_same": len({item.get("resource_class") for item in baselines.values()}) == 1,
        "baseline_comparability_summary": {
            "baseline_count": len(baselines),
            "required_baselines_present": sorted(set(baselines).intersection(REQUIRED_BASELINES)),
            "required_baselines_missing": sorted(REQUIRED_BASELINES - set(baselines)),
            "final_verify_same": len({item.get("final_verify_enabled") for item in baselines.values()}) == 1,
            "proof_worker_same": len({item.get("proof_worker_enabled") for item in baselines.values()}) == 1,
            "lean_library_access_same": len({item.get("lean_library_access") for item in baselines.values()}) == 1,
        },
    }
    (run_dir / "baseline_comparability_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _record_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    by_baseline: dict[str, dict[str, int]] = {}
    for record in records:
        baseline = str(record.get("baseline_id", "<missing>"))
        bucket = by_baseline.setdefault(baseline, {"records": 0, "final_theorem": 0, "measured_failure": 0})
        bucket["records"] += 1
        if record.get("final_status") == "final_theorem":
            bucket["final_theorem"] += 1
        elif record.get("final_status") == "measured_failure":
            bucket["measured_failure"] += 1
    return {
        "record_count": len(records),
        "by_baseline": by_baseline,
        "derived_from_actual_task_pipeline_runs": True,
    }


def _load_run_records(run_dir: Path) -> list[dict[str, Any]]:
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
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}" if path.exists() else ""


def _sha_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
