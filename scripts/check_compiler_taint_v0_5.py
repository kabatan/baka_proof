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

from plugins.geometry_full2d.compiler_v0_5 import compile_selected_derivation, run_compiler_cli
from scripts.geometry_full2d_v0_5_compiler_fixtures import prepare_compiler_fixture, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    args = parser.parse_args()
    report = check_compiler_taint(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_compiler_taint(run_dir: Path) -> dict[str, Any]:
    del run_dir
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture = prepare_compiler_fixture(root)
        base = run_compiler_cli(
            claim_spec_json=fixture["claim_path"],
            selected_derivation_json=fixture["selected_derivation_path"],
            rule_registry_json=fixture["rule_registry_path"],
            output_dir=root / "base",
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
        tainted_claim = copy.deepcopy(fixture["claim"])
        tainted_claim.update(
            {
                "target_shape_id": "mutated_shape_menu",
                "template_id": "mutated_template",
                "task_id": "mutated_task_id",
                "theorem_family": "mutated_family",
                "grammar_family": "mutated_grammar",
                "difficulty_tier": "mutated_difficulty",
                "baseline_id": "B7",
                "source_ref": "mutated_source_ref",
                "corpus_manifest_ref": "mutated_corpus_manifest",
            }
        )
        tainted_claim_path = root / "tainted_claim.json"
        write_json(tainted_claim_path, tainted_claim)
        tainted = run_compiler_cli(
            claim_spec_json=tainted_claim_path,
            selected_derivation_json=fixture["selected_derivation_path"],
            rule_registry_json=fixture["rule_registry_path"],
            output_dir=root / "tainted",
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
        mutated_derivation = copy.deepcopy(fixture["selected_derivation"])
        mutated_derivation["derivation_steps"][1]["rule_id"] = "full2d_rule:incidence_collinearity:03"
        derivation_mutation = compile_selected_derivation(
            claim_spec=fixture["claim"],
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation=mutated_derivation,
            selected_solver_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry=fixture["rule_registry"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
        base_result = read_result(root / "base")
        tainted_result = read_result(root / "tainted")
        errors: list[str] = []
        if base["status"] != "passed":
            errors.append("base_compile_failed")
        if tainted["status"] != "passed":
            errors.append("tainted_metadata_compile_failed")
        if proof_decision_view(base_result) != proof_decision_view(tainted_result):
            errors.append("forbidden_metadata_changed_proof_decision")
        if derivation_mutation["status"] != "passed":
            errors.append("selected_derivation_mutation_failed_instead_of_changed")
        elif proof_decision_view(base_result) == proof_decision_view(derivation_mutation["compiler_result"]):
            errors.append("selected_derivation_mutation_did_not_change_output")
        return {
            "schema_version": "CompilerTaintCheckV05",
            "status": "passed" if not errors else "failed",
            "errors": errors,
            "base": base,
            "tainted_metadata": tainted,
            "selected_derivation_mutation_status": derivation_mutation["status"],
            "selected_derivation_mutation_errors": derivation_mutation.get("errors", []),
        }


def proof_decision_view(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "proof_text": result.get("proof_text"),
        "used_rule_ids": result.get("used_rule_ids"),
        "generated_obligations": result.get("generated_obligations"),
        "solver_fact_refs": result.get("solver_fact_refs"),
        "solver_construction_refs": result.get("solver_construction_refs"),
        "solver_certificate_refs": result.get("solver_certificate_refs"),
        "derivation_step_refs": result.get("derivation_step_refs"),
        "target_expr_branch_used": result.get("target_expr_branch_used"),
        "forbidden_metadata_used": result.get("forbidden_metadata_used"),
    }


def read_result(root: Path) -> dict[str, Any]:
    path = root / "compiler_stage" / "compiler_result.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


if __name__ == "__main__":
    raise SystemExit(main())
