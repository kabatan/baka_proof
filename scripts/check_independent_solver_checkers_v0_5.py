#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
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
        report = self_test_report(Path(args.run_dir))
    else:
        report = run_independent_solver_checkers(Path(args.run_dir), claim_spec_json=Path(args.claim_spec_json) if args.claim_spec_json else None)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


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
