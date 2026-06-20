from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_selected_derivation_v0_6 import ensure_prerequisites
from scripts.geometry_full2d_v0_6_derivation import (
    CLAIM_SPEC_DIR,
    SELECTED_DERIVATION_DIR,
    TARGET_MATCH_DIR,
    build_selected_derivations,
    build_target_match_reports,
    current_git_head,
    file_sha256,
    validate_target_match_report,
)
from scripts.geometry_full2d_v0_6_extraction import read_json, write_json


def _claims_by_ref(run_dir: Path) -> dict[str, dict[str, Any]]:
    return {file_sha256(path): read_json(path) for path in sorted((run_dir / CLAIM_SPEC_DIR).glob("*.json"))}


def _derivations_by_path(run_dir: Path) -> dict[Path, dict[str, Any]]:
    return {path: read_json(path) for path in sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json"))}


def red_case_report() -> dict[str, Any]:
    errors: list[str] = []
    selected_ref = "sha256:" + "a" * 64
    claim_ref = "sha256:" + "b" * 64
    final_ref = "sha256:" + "c" * 64
    target_hash = "sha256:" + "d" * 64
    derivation = {
        "derivation_id": "sha256:" + "e" * 64,
        "claim_spec_ref": claim_ref,
        "final_step_ref": final_ref,
        "has_non_target_intermediate": True,
        "has_checked_side_condition_or_certificate": True,
    }
    claim = {"target_hash": target_hash}
    base = {
        "schema_version": "DerivationTargetMatchReportV1",
        "match_report_id": "sha256:" + "f" * 64,
        "selected_derivation_ref": selected_ref,
        "selected_derivation_id": derivation["derivation_id"],
        "claim_spec_ref": claim_ref,
        "status": "passed",
        "final_step_hash": final_ref,
        "target_hash": target_hash,
        "command_log_ref": "sha256:" + "1" * 64,
        "target_match_authority": "hash_entailment_from_checked_selected_derivation",
        "proof_material_emitted": False,
        "git_head": current_git_head(),
    }
    local_cases = {
        "outputs_strategy_label": {**base, "strategy_label": "collinear-target"},
        "outputs_proof_text": {**base, "proof_text": "exact h"},
        "outputs_target_expr": {**base, "target_expr": "Collinear A B C"},
        "outputs_rule_ids": {**base, "rule_ids": ["full2d_rule:direct_target:00"]},
        "final_step_mismatch": {**base, "final_step_hash": "sha256:" + "2" * 64},
        "target_hash_mismatch": {**base, "target_hash": "sha256:" + "3" * 64},
        "no_non_target_support": {**base},
    }
    bad_derivation = {**derivation, "has_non_target_intermediate": False}
    local_results: dict[str, list[str]] = {}
    for name, payload in local_cases.items():
        d = bad_derivation if name == "no_non_target_support" else derivation
        local_results[name] = validate_target_match_report(payload, derivation=d, claim=claim)
    positive_errors = validate_target_match_report(base, derivation=derivation, claim=claim)
    if positive_errors:
        errors.append("local_positive_target_match_rejected:" + ",".join(positive_errors))
    for name, result in local_results.items():
        if not result:
            errors.append(f"local_negative_unrejected:{name}")
    return {
        "schema_version": "DerivationTargetMatcherRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "local_positive_errors": positive_errors,
        "local_negative_results": local_results,
    }


def check_derivation_target_matcher(run_dir: Path, *, red_cases: bool, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    prereq = ensure_prerequisites(run_dir, fresh=fresh)
    errors.extend(f"prereq:{error}" for error in prereq.get("errors", []))
    selected_report = build_selected_derivations(run_dir)
    errors.extend(f"selected_derivation:{error}" for error in selected_report.get("errors", []))
    match_report = build_target_match_reports(run_dir)
    errors.extend(f"target_match:{error}" for error in match_report.get("errors", []))
    claims = _claims_by_ref(run_dir)
    derivations = _derivations_by_path(run_dir)
    derivation_by_name = {path.name: payload for path, payload in derivations.items()}
    validation_rows: list[dict[str, Any]] = []
    for path in sorted((run_dir / TARGET_MATCH_DIR).glob("*.json")):
        payload = read_json(path)
        derivation = derivation_by_name.get(path.name)
        claim = claims.get(str(payload.get("claim_spec_ref")))
        payload_errors = validate_target_match_report(payload, derivation=derivation, claim=claim)
        if payload_errors:
            errors.extend(f"{path.name}:{error}" for error in payload_errors)
        validation_rows.append(
            {
                "path": path.relative_to(run_dir).as_posix(),
                "match_report_id": payload.get("match_report_id"),
                "status": payload.get("status"),
                "errors": payload_errors,
            }
        )
    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    return {
        "schema_version": "CheckDerivationTargetMatcherV06Report",
        "checker_name": "check_derivation_target_matcher_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "prerequisites": prereq,
        "selected_derivation_report": selected_report,
        "target_match_report": match_report,
        "validation_rows": validation_rows,
        "red_cases": red_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 derivation target matcher.")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_derivation_target_matcher(args.run_dir, red_cases=args.red_cases, fresh=args.fresh)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
