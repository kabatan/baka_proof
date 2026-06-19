#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.provider_cli import run_provider_cli
from scripts.check_provider_stage_boundary_v0_5 import sample_claim_spec
from scripts.geometry_full2d_v0_5_independent_checkers import (
    CHECKER_KIND_BY_ROLE,
    check_synthetic_trace,
    read_json,
    run_independent_solver_checkers,
    strip_identity,
    target_fact,
    validate_checker_report_payload,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    parser.add_argument("--claim-spec-json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_report = self_test_report(Path(args.run_dir))
        run_dir = Path(args.run_dir)
        if has_matrix_independent_checker_reports(run_dir):
            run_report = check_matrix_independent_checker_reports(run_dir)
        elif has_independent_checker_artifacts(run_dir):
            run_report = run_independent_solver_checkers(run_dir, claim_spec_json=Path(args.claim_spec_json) if args.claim_spec_json else None)
        else:
            run_report = None
        if run_report is not None:
            report = combined_report(
                "IndependentSolverCheckersSelfTestAndRunCheckV05",
                self_report,
                run_report,
                self_key="self_test",
                run_key="run_check",
            )
        else:
            report = self_report
    else:
        report = run_independent_solver_checkers(Path(args.run_dir), claim_spec_json=Path(args.claim_spec_json) if args.claim_spec_json else None)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def has_independent_checker_artifacts(run_dir: Path) -> bool:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    return (root / "provider_stage" / "engine_outputs").exists() or (root / "provider_task_runs").exists()


def has_matrix_independent_checker_reports(run_dir: Path) -> bool:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    reports = root / "independent_checker_reports"
    records = root / "actual_task_pipeline_runs"
    return reports.exists() and records.exists()


def check_matrix_independent_checker_reports(run_dir: Path) -> dict[str, Any]:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    report_dir = root / "independent_checker_reports"
    report_files = sorted(path for path in report_dir.glob("*.json") if "__summary" not in path.name) if report_dir.exists() else []
    ref_index: dict[str, dict[str, Any]] = {}
    roles_seen: set[str] = set()
    kinds_seen: set[str] = set()
    for path in report_files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            errors.append(f"{path.name}:report_not_object")
            continue
        ref_index[hash_payload(payload)] = payload
        schema_errors = validate_checker_report_payload(payload)
        errors.extend(f"{path.name}:{error}" for error in schema_errors)
        if payload.get("status") == "passed":
            roles_seen.add(str(payload.get("engine_role", "")))
            kinds_seen.add(str(payload.get("checker_kind", "")))
    b2_records = load_b2_final_records(root)
    if not b2_records:
        errors.append("missing_b2_final_theorem_records")
    unresolved_record_refs = 0
    unresolved_derivation_refs = 0
    for record_path, record in b2_records:
        task_id = str(record.get("task_id", record_path.stem))
        for ref in record.get("independent_checker_report_refs", []):
            if str(ref) not in ref_index:
                unresolved_record_refs += 1
                errors.append(f"{task_id}:record_checker_ref_unresolved:{ref}")
        derivation_path = root / "selected_solver_derivations" / f"{safe_id(task_id)}__B2.json"
        if not derivation_path.exists():
            errors.append(f"{task_id}:selected_derivation_missing_for_checker_ref_audit")
            continue
        derivation = json.loads(derivation_path.read_text(encoding="utf-8"))
        if not isinstance(derivation, dict):
            errors.append(f"{task_id}:selected_derivation_not_object")
            continue
        for index, step in enumerate(derivation.get("derivation_steps", [])):
            if not isinstance(step, dict):
                continue
            ref = str(step.get("independent_checker_report_ref", ""))
            if ref not in ref_index:
                unresolved_derivation_refs += 1
                errors.append(f"{task_id}:derivation_step_checker_ref_unresolved:{index}:{ref}")
    required_kinds = set(CHECKER_KIND_BY_ROLE.values())
    missing_kinds = sorted(required_kinds - kinds_seen)
    if missing_kinds:
        errors.append("missing_checker_kinds:" + ",".join(missing_kinds))
    return {
        "schema_version": "IndependentSolverCheckersMatrixRunCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(root),
        "report_count": len(report_files),
        "b2_final_theorem_records": len(b2_records),
        "checker_kinds_covered": sorted(kinds_seen),
        "required_checker_kinds": sorted(required_kinds),
        "roles_seen": sorted(role for role in roles_seen if role),
        "unresolved_record_refs": unresolved_record_refs,
        "unresolved_derivation_refs": unresolved_derivation_refs,
    }


def load_b2_final_records(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    records_dir = root / "actual_task_pipeline_runs"
    rows: list[tuple[Path, dict[str, Any]]] = []
    if records_dir.exists():
        for path in sorted(records_dir.glob("*__B2.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and payload.get("baseline_id") == "B2" and payload.get("final_status") == "final_theorem":
                rows.append((path, payload))
    return rows


def hash_payload(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def safe_id(value: str) -> str:
    return "".join(char if char.isalnum() or char in "_.-" else "_" for char in value)


def combined_report(
    schema_version: str,
    self_report: dict[str, Any],
    run_report: dict[str, Any],
    *,
    self_key: str,
    run_key: str,
) -> dict[str, Any]:
    errors: list[str] = []
    if self_report.get("status") != "passed":
        errors.append(f"{self_key}_failed")
    if run_report.get("status") != "passed":
        errors.append(f"{run_key}_failed")
    errors.extend(f"{self_key}:{error}" for error in self_report.get("errors", []) if isinstance(error, str))
    errors.extend(f"{run_key}:{error}" for error in run_report.get("errors", []) if isinstance(error, str))
    return {
        "schema_version": schema_version,
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        self_key: self_report,
        run_key: run_report,
    }


def self_test_report(default_run_dir: Path) -> dict[str, Any]:
    del default_run_dir
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        claim = sample_claim_spec()
        claim_path = root / "claim.json"
        claim_path.write_text(json.dumps(claim, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        run_dir = root / "run"
        provider = run_provider_cli(claim_path, run_dir, "independent_checker_selftest")
        positive = run_independent_solver_checkers(run_dir)
        synthetic_artifact = strip_identity(read_json(run_dir / "provider_stage" / "normalized_artifacts" / "synthetic_closure.json"))
        mutated_fact = copy.deepcopy(synthetic_artifact)
        mutated_fact["target_fact"] = "TARGET"
        mutated_errors = check_synthetic_trace(claim, mutated_fact)
        missing_premise = copy.deepcopy(synthetic_artifact)
        for step in missing_premise.get("steps", []):
            if isinstance(step, dict) and step.get("output_fact") == target_fact(claim):
                step["input_facts"] = []
        missing_premise_errors = check_synthetic_trace(claim, missing_premise)
        naked_target = copy.deepcopy(synthetic_artifact)
        naked_target["steps"] = [
            {
                "step_id": "bad:naked_target",
                "rule_id": "full2d_rule:incidence_collinearity:02",
                "input_facts": [],
                "output_fact": target_fact(claim),
                "discharged_side_conditions": [],
            }
        ]
        naked_target_errors = check_synthetic_trace(claim, naked_target)
        self_certified_report = copy.deepcopy(positive["reports"][0])
        self_certified_report["recomputed"] = False
        self_certified_report["recomputed_from_claim_spec"] = False
        self_certified_report["checker_self_certified"] = True
        self_certified_report["trusted_engine_boolean"] = True
        self_certified_errors = validate_checker_report_payload(self_certified_report)
        errors: list[str] = []
        if provider["status"] != "passed":
            errors.append("provider_cli_failed")
        if positive["status"] != "passed":
            errors.append("positive_independent_checker_failed")
        if "synthetic_target_fact_mismatch" not in mutated_errors:
            errors.append("mutated_fact_not_rejected")
        if not any(error.startswith("synthetic_target_step_missing_premises") for error in missing_premise_errors):
            errors.append("missing_premise_not_rejected")
        if "synthetic_trace_missing_non_target_intermediate" not in naked_target_errors:
            errors.append("naked_target_not_rejected")
        if "self_certified_checker_report" not in self_certified_errors or "checker_self_attested" not in self_certified_errors:
            errors.append("self_certified_report_not_rejected")
        return {
            "schema_version": "IndependentSolverCheckersSelfTestV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "provider_cli_report": provider,
            "positive": positive,
            "negative_errors": {
                "mutated_fact": mutated_errors,
                "missing_premise": missing_premise_errors,
                "naked_target": naked_target_errors,
                "self_certified_report": self_certified_errors,
            },
        }


if __name__ == "__main__":
    raise SystemExit(main())
