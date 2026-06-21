from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_provider import (
    ENGINE_OUTPUT_DIR,
    PROVIDER_ORDER_WITNESS_NAME,
    PROVIDER_MANIFEST_DIR,
    provider_import_report,
    run_provider_stage,
    validate_provider_manifest_payload,
)
from scripts.geometry_full2d_v0_6_red_cases import load_manifest, evaluate_fixture
from scripts.geometry_full2d_v0_6_schemas import validate_payload
from scripts.geometry_full2d_v0_6_extraction import read_json, write_json


def ensure_provider_outputs(run_dir: Path) -> dict[str, Any]:
    manifest_dir = run_dir / PROVIDER_MANIFEST_DIR
    engine_dir = run_dir / ENGINE_OUTPUT_DIR
    if not manifest_dir.exists() or not list(manifest_dir.glob("*.json")) or not engine_dir.exists() or not list(engine_dir.glob("*.json")):
        return run_provider_stage(run_dir)
    return {
        "schema_version": "RunProviderStageV06Report",
        "status": "passed",
        "errors": [],
        "run_dir": str(run_dir),
        "provider_manifest_count": len(list(manifest_dir.glob("*.json"))),
        "engine_output_count": len(list(engine_dir.glob("*.json"))),
        "provider_index_path": str(run_dir / "provider_index_v0_6.json"),
        "existing_outputs_reused": True,
    }


def validate_stage_order(run_dir: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    witness_path = run_dir / PROVIDER_ORDER_WITNESS_NAME
    if not witness_path.exists():
        errors.append("missing_provider_stage_order_witness")
        return errors
    try:
        witness = read_json(witness_path)
    except Exception as exc:
        errors.append(f"provider_stage_order_witness_unreadable:{exc}")
        return errors
    if witness.get("schema_version") != "ProviderStageOrderWitnessV06":
        errors.append("provider_stage_order_witness_bad_schema")
    if witness.get("provider_completed_before_compiler_started") is not True:
        errors.append("provider_stage_order_witness_not_before_compiler")
    if witness.get("compiler_stage_state") == "artifacts_present":
        errors.append("compiler_artifacts_present_before_or_at_provider_completion")
    if witness.get("compiler_artifacts_observed_at_provider_completion") not in ([], None):
        errors.append("compiler_artifacts_observed_at_provider_completion")
    provider_completed_at = str(manifest.get("provider_completed_at", ""))
    if not provider_completed_at:
        errors.append("missing_provider_completed_at")
    return errors


def validate_global_stage_order(run_dir: Path, provider_completed_values: list[str]) -> list[str]:
    errors: list[str] = []
    provider_completed_at = max((value for value in provider_completed_values if value), default="")
    if not provider_completed_at:
        return errors
    scan_roots = [
        run_dir / "compiler_results_v0_6",
        run_dir / "actual_task_pipeline_runs_v0_6",
    ]
    for root in scan_roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("*.json")):
            errors.extend(_compiler_timestamp_errors(path, run_dir, provider_completed_at))
    return sorted(set(errors))


def _compiler_timestamp_errors(path: Path, run_dir: Path, provider_completed_at: str) -> list[str]:
    errors: list[str] = []
    try:
        payload = read_json(path)
    except Exception:
        return errors
    timestamps = payload.get("stage_timestamps") if isinstance(payload, dict) else None
    if isinstance(timestamps, dict):
        compiler_started_at = timestamps.get("compiler_started_at")
        if compiler_started_at and provider_completed_at and str(compiler_started_at) <= provider_completed_at:
            errors.append(f"{path.relative_to(run_dir).as_posix()}:compiler_started_not_after_provider_completed")
    compiler_started_at = payload.get("compiler_started_at") if isinstance(payload, dict) else None
    if compiler_started_at and provider_completed_at and str(compiler_started_at) <= provider_completed_at:
        errors.append(f"{path.relative_to(run_dir).as_posix()}:compiler_started_not_after_provider_completed")
    return errors


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    rows = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") == "RC-019":
            row = evaluate_fixture(fixture)
            rows.append(row)
            if "K-008" not in row.get("detected_K", []):
                errors.append("RC-019:K-008_not_detected")
            if not row.get("positive_control_passed"):
                errors.append("RC-019:positive_control_failed")
    if not rows:
        errors.append("RC-019_fixture_missing")

    bad_manifests = {
        "compiler": ["scripts.geometry_full2d_v0_6_compiler"],
        "release": ["scripts.geometry_full2d_v0_6_release"],
        "corpus": ["scripts.geometry_full2d_v0_6_corpus"],
        "previous_release": ["scripts.geometry_full2d_v0_5_provider"],
        "proof_template": ["scripts.geometry_full2d_v0_6_proof_templates"],
    }
    local_negative_errors: dict[str, list[str]] = {}
    for name, imports in bad_manifests.items():
        bad_manifest = {
            "schema_version": "ProviderRunManifestV3",
            "manifest_id": "provider:test",
            "claim_spec_ref": "sha256:" + "a" * 64,
            "provider_stage_run_id": "provider-stage:test",
            "provider_started_at": "2026-06-20T00:00:00Z",
            "provider_completed_at": "2026-06-20T00:00:01Z",
            "engine_output_refs": ["sha256:" + "b" * 64],
            "imports": imports,
            "provider_code_hash": "sha256:" + "c" * 64,
            "git_head": "test-head",
            "config_hash": "sha256:" + "d" * 64,
        }
        local_errors = validate_provider_manifest_payload(bad_manifest)
        local_negative_errors[name] = local_errors
        if not any("forbidden_provider_import" in item or "provider_imports_downstream_module" in item for item in local_errors):
            errors.append(f"local_provider_import_negative_unrejected:{name}")
    return {
        "schema_version": "ProviderIsolationRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "cases": rows,
        "local_negative_errors": local_negative_errors,
    }


def check_provider_isolation(run_dir: Path, *, red_cases: bool = False) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    provider_run = ensure_provider_outputs(run_dir)
    errors.extend(f"provider_run:{error}" for error in provider_run.get("errors", []))

    import_scan = provider_import_report()
    if import_scan.get("status") != "passed":
        errors.extend(f"provider_import_scan:{item}" for item in import_scan.get("forbidden_imports", []))

    manifest_results: list[dict[str, Any]] = []
    manifest_dir = run_dir / PROVIDER_MANIFEST_DIR
    provider_completed_values: list[str] = []
    for path in sorted(manifest_dir.glob("*.json")):
        try:
            payload = read_json(path)
        except Exception as exc:
            errors.append(f"{path.name}:unreadable:{exc}")
            continue
        payload_errors = validate_provider_manifest_payload(payload)
        payload_errors.extend(validate_stage_order(run_dir, payload))
        provider_completed_values.append(str(payload.get("provider_completed_at", "")))
        engine_paths = payload.get("engine_output_paths", [])
        if not isinstance(engine_paths, list) or not engine_paths:
            payload_errors.append("missing_engine_output_paths")
        else:
            missing = [str(item) for item in engine_paths if not (run_dir / str(item)).exists()]
            payload_errors.extend(f"missing_engine_output_path:{item}" for item in missing)
        schema_errors = validate_payload(payload)
        payload_errors.extend(schema_errors)
        manifest_results.append({"path": path.relative_to(run_dir).as_posix(), "status": "passed" if not payload_errors else "failed", "errors": sorted(set(payload_errors))})
        errors.extend(f"{path.name}:{error}" for error in sorted(set(payload_errors)))

    if not manifest_results:
        errors.append("missing_provider_manifests")
    global_stage_order_errors = validate_global_stage_order(run_dir, provider_completed_values)
    errors.extend(f"global_stage_order:{error}" for error in global_stage_order_errors)

    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))

    return {
        "schema_version": "CheckProviderIsolationV06Report",
        "checker_name": "check_provider_isolation_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "provider_run": provider_run,
        "import_scan": import_scan,
        "manifest_results": manifest_results,
        "global_stage_order_errors": global_stage_order_errors,
        "red_cases": red_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 provider isolation and provider-before-compiler order.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_provider_isolation(Path(args.run_dir), red_cases=args.red_cases)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
