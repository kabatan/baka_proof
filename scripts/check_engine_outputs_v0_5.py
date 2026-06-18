#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES
from plugins.geometry_full2d.provider_cli import run_provider_cli
from scripts.check_provider_stage_boundary_v0_5 import sample_claim_spec
from scripts.geometry_full2d_v0_5_schemas import validate_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = self_test_report() if args.self_test else check_engine_outputs(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_engine_outputs(run_dir: Path) -> dict[str, Any]:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    output_dir = root / "provider_stage" / "engine_outputs"
    errors: list[str] = []
    reports: list[dict[str, Any]] = []
    if not output_dir.exists():
        return {
            "schema_version": "EngineOutputsCheckV05",
            "status": "failed",
            "errors": ["missing_provider_stage_engine_outputs"],
            "engine_output_count": 0,
            "roles_seen": [],
        }
    for path in sorted(output_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}:unreadable_json:{exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{path.name}:payload_not_object")
            continue
        item_errors = validate_engine_output_payload(payload)
        errors.extend(f"{path.name}:{error}" for error in item_errors)
        reports.append(payload)
    roles_seen = sorted({str(item.get("engine_role")) for item in reports})
    missing_roles = sorted(set(ENGINE_ROLES) - set(roles_seen))
    if missing_roles:
        errors.append("missing_engine_roles:" + ",".join(missing_roles))
    return {
        "schema_version": "EngineOutputsCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "engine_output_count": len(reports),
        "roles_seen": roles_seen,
    }


def validate_engine_output_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_payload(payload, current_head="test-head")
    if payload.get("schema_version") != "EngineOutputFull2D:2":
        errors.append("bad_engine_output_schema_version")
    if payload.get("proof_text_present") is not False:
        errors.append("proof_text_present")
    if payload.get("proof_use_status") != "not_allowed":
        errors.append("proof_use_status_not_allowed")
    if payload.get("forbidden_metadata_consumed_by_compiler") not in ([], None):
        errors.append("forbidden_metadata_consumed_by_compiler")
    if not payload.get("normalized_artifact_refs") and not payload.get("facts") and not payload.get("constructions") and not payload.get("certificates") and payload.get("engine_status") == "normalized_success":
        errors.append("normalized_success_without_semantic_artifact")
    if payload.get("engine_status") == "normalized_success" and not payload.get("independent_checker_report_refs"):
        errors.append("normalized_success_missing_independent_checker_ref")
    for index, fact in enumerate(payload.get("facts", [])):
        if isinstance(fact, dict) and fact.get("premises") == [] and str(fact.get("conclusion", "")).upper() in {"TARGET", "TARGET_GOAL"}:
            errors.append(f"target_fact_empty_premises:{index}")
    text = json.dumps(payload, sort_keys=True).lower()
    for token in [" exact ", " by ", "rw [", "simp ", "nlinarith", "linarith"]:
        if token in text:
            errors.append("proof_text_like_token_in_engine_output")
    return sorted(set(errors))


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        claim = root / "claim.json"
        claim.write_text(json.dumps(sample_claim_spec(), indent=2, sort_keys=True), encoding="utf-8")
        run_dir = root / "run"
        cli = run_provider_cli(claim, run_dir, "engine_outputs_selftest")
        positive = check_engine_outputs(run_dir)
        bad = dict(json.loads((run_dir / "provider_stage" / "engine_outputs" / "synthetic_closure.json").read_text(encoding="utf-8")))
        bad["facts"] = [{"conclusion": "TARGET", "premises": [], "checker_report_ref": None}]
        bad["proof_text_present"] = True
        negative_errors = validate_engine_output_payload(bad)
        errors: list[str] = []
        if cli["status"] != "passed":
            errors.append("provider_cli_failed")
        if positive["status"] != "passed":
            errors.append("positive_engine_outputs_failed")
        if not {"proof_text_present", "target_fact_empty_premises:0"}.issubset(set(negative_errors)):
            errors.append("mutated_engine_output_not_rejected")
        return {
            "schema_version": "EngineOutputsSelfTestV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "provider_cli_report": cli,
            "positive": positive,
            "negative_errors": negative_errors,
        }


if __name__ == "__main__":
    raise SystemExit(main())
