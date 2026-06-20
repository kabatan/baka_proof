from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_provider_isolation_v0_6 import ensure_provider_outputs
from scripts.geometry_full2d_v0_6_extraction import CLAIM_SPEC_DIR, read_json, write_json
from scripts.geometry_full2d_v0_6_provider import ENGINE_OUTPUT_DIR, PROVIDER_MANIFEST_DIR, validate_engine_output_payload
from scripts.geometry_full2d_v0_6_red_cases import load_manifest, evaluate_fixture
from scripts.geometry_full2d_v0_6_schemas import ENGINE_ROLES, validate_payload


def claim_by_ref(run_dir: Path) -> dict[str, dict[str, Any]]:
    from scripts.geometry_full2d_v0_6_provider import file_sha256

    claims: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / CLAIM_SPEC_DIR).glob("*.json")):
        claims[file_sha256(path)] = read_json(path)
    return claims


def engine_refs_from_manifests(run_dir: Path) -> set[str]:
    refs: set[str] = set()
    for path in sorted((run_dir / PROVIDER_MANIFEST_DIR).glob("*.json")):
        try:
            payload = read_json(path)
        except Exception:
            continue
        for ref in payload.get("engine_output_refs", []):
            refs.add(str(ref))
    return refs


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    wanted = {"RC-001": "K-007", "RC-005": "K-011", "K-010": "K-010", "RC-014": "K-009"}
    rows = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") in wanted:
            row = evaluate_fixture(fixture)
            rows.append(row)
            expected_k = wanted[str(fixture.get("red_case_id"))]
            if expected_k not in row.get("detected_K", []):
                errors.append(f"{fixture.get('red_case_id')}:{expected_k}_not_detected")
            if not row.get("positive_control_passed"):
                errors.append(f"{fixture.get('red_case_id')}:positive_control_failed")
    present = {str(row.get("red_case_id")) for row in rows}
    for case_id in sorted(set(wanted) - present):
        errors.append(f"{case_id}_fixture_missing")

    base_ref = "sha256:" + "a" * 64
    bad_cases = {
        "target_fact_provider": {
            "schema_version": "EngineOutputFull2D",
            "engine_output_id": "engine:test",
            "engine_role": "synthetic_trace",
            "claim_spec_ref": base_ref,
            "provider_run_manifest_ref": "sha256:" + "b" * 64,
            "provider_stage_run_id": "provider-stage:test",
            "backend_identity": "negative",
            "backend_code_hash": "sha256:" + "c" * 64,
            "selected_artifacts": [{"kind": "fact", "conclusion": base_ref, "conclusion_hash": base_ref, "premises": [], "is_final_target": True}],
            "independent_checker_refs": [],
            "proof_text_present": False,
            "created_before_compiler": True,
            "git_head": "test-head",
        },
        "rule_list_synthesis": {
            "schema_version": "EngineOutputFull2D",
            "engine_output_id": "engine:test",
            "engine_role": "construction",
            "claim_spec_ref": base_ref,
            "provider_run_manifest_ref": "sha256:" + "b" * 64,
            "provider_stage_run_id": "provider-stage:test",
            "backend_identity": "negative",
            "backend_code_hash": "sha256:" + "c" * 64,
            "selected_artifacts": [
                {
                    "kind": "construction",
                    "conclusion": "non_target",
                    "premises": ["h"],
                    "is_final_target": False,
                    "derivation_source": "compiler_selected_rule_list",
                }
            ],
            "compiler_selected_rule_list": ["full2d_rule:fake"],
            "independent_checker_refs": [],
            "proof_text_present": False,
            "created_before_compiler": True,
            "git_head": "test-head",
        },
        "proof_text": {
            "schema_version": "EngineOutputFull2D",
            "engine_output_id": "engine:test",
            "engine_role": "lean_search_certificate",
            "claim_spec_ref": base_ref,
            "provider_run_manifest_ref": "sha256:" + "b" * 64,
            "provider_stage_run_id": "provider-stage:test",
            "backend_identity": "negative",
            "backend_code_hash": "sha256:" + "c" * 64,
            "selected_artifacts": [{"kind": "certificate", "conclusion": "non_target", "premises": ["h"], "is_final_target": False}],
            "independent_checker_refs": [],
            "proof_text_present": True,
            "proof_text": "exact h",
            "created_before_compiler": True,
            "git_head": "test-head",
        },
    }
    local_results = {name: validate_engine_output_payload(payload, {"target_hash": base_ref}) for name, payload in bad_cases.items()}
    if not any("selected_artifact_is_final_target" in item or "target_fact_without_derivation" in item for item in local_results["target_fact_provider"]):
        errors.append("local_target_fact_negative_unrejected")
    if not any("engine_output_from_compiler_rules" in item or "selected_artifact_from_compiler_rules" in item for item in local_results["rule_list_synthesis"]):
        errors.append("local_rule_list_negative_unrejected")
    if not any("proof_text" in item for item in local_results["proof_text"]):
        errors.append("local_proof_text_negative_unrejected")
    return {
        "schema_version": "EngineOutputNoCompilerRulesRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "cases": rows,
        "local_negative_results": local_results,
    }


def check_engine_outputs(run_dir: Path, *, red_cases: bool = False) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    provider_run = ensure_provider_outputs(run_dir)
    errors.extend(f"provider_run:{error}" for error in provider_run.get("errors", []))
    claims = claim_by_ref(run_dir)
    manifest_refs = engine_refs_from_manifests(run_dir)
    role_seen: set[str] = set()
    output_results: list[dict[str, Any]] = []

    for path in sorted((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        try:
            payload = read_json(path)
        except Exception as exc:
            errors.append(f"{path.name}:unreadable:{exc}")
            continue
        claim = claims.get(str(payload.get("claim_spec_ref")))
        output_errors = validate_engine_output_payload(payload, claim)
        output_errors.extend(validate_payload(payload))
        if claim is None:
            output_errors.append("claim_spec_ref_not_found")
        if payload.get("engine_output_id") not in manifest_refs:
            output_errors.append("engine_output_not_referenced_by_provider_manifest")
        if payload.get("created_before_compiler") is not True:
            output_errors.append("created_before_compiler_not_true")
        role = str(payload.get("engine_role"))
        if role in ENGINE_ROLES:
            role_seen.add(role)
        selected = payload.get("selected_artifacts")
        if not isinstance(selected, list) or not selected:
            output_errors.append("missing_selected_artifacts")
        else:
            for index, artifact in enumerate(selected):
                if isinstance(artifact, dict) and artifact.get("derivation_source") != "provider_stage_solver_algorithm":
                    output_errors.append(f"selected_artifact_not_from_provider_solver:{index}")
        output_results.append({"path": path.relative_to(run_dir).as_posix(), "status": "passed" if not output_errors else "failed", "errors": sorted(set(output_errors))})
        errors.extend(f"{path.name}:{error}" for error in sorted(set(output_errors)))

    if not output_results:
        errors.append("missing_engine_outputs")
    missing_roles = sorted(set(ENGINE_ROLES) - role_seen)
    if missing_roles:
        errors.append("missing_engine_roles:" + ",".join(missing_roles))

    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))

    return {
        "schema_version": "CheckEngineOutputNotFromCompilerRulesV06Report",
        "checker_name": "check_engine_output_not_from_compiler_rules_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "provider_run": provider_run,
        "engine_output_results": output_results,
        "engine_roles_seen": sorted(role_seen),
        "red_cases": red_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check v0.6 engine outputs are real provider artifacts, not compiler rule-list or proof-text artifacts.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_engine_outputs(Path(args.run_dir), red_cases=args.red_cases)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
