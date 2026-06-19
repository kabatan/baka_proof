#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_full2d.compiler_v0_5 import compile_selected_derivation, run_compiler_cli
from scripts.geometry_full2d_v0_5_compiler_fixtures import prepare_compiler_fixture
from scripts.geometry_full2d_v0_5_schemas import validate_payload


COMPILER_PATH = ROOT / "plugins" / "geometry_full2d" / "compiler_v0_5.py"
SOLVER_DERIVATION_PATH = ROOT / "plugins" / "geometry_full2d" / "solver_derivation.py"
FORBIDDEN_PATTERNS = {
    "target_expr_startswith": re.compile(r"target_expr\.startswith\s*\("),
    "match_target_expr": re.compile(r"match\s+target_expr\b"),
    "target_shape_id": re.compile(r"\btarget_shape_id\b"),
    "template_id": re.compile(r"\btemplate_id\b"),
    "theorem_family": re.compile(r"\btheorem_family\b"),
    "grammar_family": re.compile(r"\bgrammar_family\b"),
    "difficulty_tier": re.compile(r"\bdifficulty_tier\b"),
    "benchmark_config": re.compile(r"\bbenchmark_config\b"),
    "corpus_manifest": re.compile(r"\bcorpus_manifest\b"),
}
SOLVER_FORBIDDEN_PATTERNS = {
    "solver_source_string_branch": re.compile(r"\bsource\s*=\s*target_source_expr\s*\([^)]*\).*?if\s+.*\bin\s+source\b", re.DOTALL),
    "solver_target_expr_startswith": re.compile(r"target_source_expr\s*\([^)]*\)\.startswith\s*\("),
    "solver_target_shape_id": re.compile(r"\btarget_shape_id\b"),
    "solver_template_id_metadata": re.compile(r"\btemplate_id\b"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    report = self_test_report(Path(args.run_dir)) if args.self_test else check_compiler_input_isolation(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_compiler_input_isolation(run_dir: Path) -> dict[str, Any]:
    static_report = scan_compiler_source()
    dynamic_report = run_dynamic_fixture(run_dir)
    errors = []
    if static_report["status"] != "passed":
        errors.extend(static_report["errors"])
    if dynamic_report["status"] != "passed":
        errors.extend(dynamic_report["errors"])
    return {
        "schema_version": "CompilerInputIsolationCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "static_report": static_report,
        "dynamic_report": dynamic_report,
    }


def scan_compiler_source(extra_text: str | None = None) -> dict[str, Any]:
    text = extra_text if extra_text is not None else COMPILER_PATH.read_text(encoding="utf-8")
    hits = [name for name, pattern in FORBIDDEN_PATTERNS.items() if pattern.search(text)]
    solver_hits: list[str] = []
    if extra_text is None:
        solver_text = SOLVER_DERIVATION_PATH.read_text(encoding="utf-8")
        solver_hits.extend(name for name, pattern in SOLVER_FORBIDDEN_PATTERNS.items() if pattern.search(solver_text))
        if "artifact_operator" not in solver_text:
            solver_hits.append("solver_missing_artifact_operator_selector")
        if "engine_artifact_derivation_operator" not in solver_text:
            solver_hits.append("solver_missing_engine_artifact_selection_provenance")
    return {
        "schema_version": "CompilerInputStaticScanV05",
        "status": "passed" if not hits and not solver_hits else "failed",
        "errors": hits + solver_hits,
        "path": COMPILER_PATH.relative_to(ROOT).as_posix(),
        "solver_path": SOLVER_DERIVATION_PATH.relative_to(ROOT).as_posix(),
    }


def run_dynamic_fixture(run_dir: Path) -> dict[str, Any]:
    del run_dir
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fixture = prepare_compiler_fixture(root)
        cli = run_compiler_cli(
            claim_spec_json=fixture["claim_path"],
            selected_derivation_json=fixture["selected_derivation_path"],
            rule_registry_json=fixture["rule_registry_path"],
            output_dir=root / "compiler_run",
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
        result_path = root / "compiler_run" / "compiler_stage" / "compiler_result.json"
        result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
        schema_errors = validate_payload(result, current_head="test-head") if isinstance(result, dict) else ["compiler_result_not_object"]
        proof_text = str(result.get("proof_text", ""))
        errors: list[str] = []
        if cli["status"] != "passed":
            errors.append("compiler_cli_failed")
        errors.extend(f"schema:{error}" for error in schema_errors)
        if result.get("target_expr_branch_used") is not False:
            errors.append("target_expr_branch_used")
        if result.get("forbidden_metadata_used") is not False:
            errors.append("forbidden_metadata_used")
        if result.get("compiler_selected_rule_list_without_derivation") is not False:
            errors.append("compiler_selected_rule_list_without_derivation")
        for required in ["solver-derived facts", "generated obligations", "consumed RuleRegistry contracts", "step:target_from_support"]:
            if required not in proof_text:
                errors.append(f"proof_text_missing_citation:{required}")
        if result.get("used_rule_ids") != ["full2d_rule:incidence_collinearity:01", "full2d_rule:incidence_collinearity:02"]:
            errors.append("used_rules_not_from_selected_derivation")
        return {
            "schema_version": "CompilerInputDynamicFixtureV05",
            "status": "passed" if not errors else "failed",
            "errors": sorted(set(errors)),
            "compiler_cli_report": cli,
        }


def self_test_report(run_dir: Path) -> dict[str, Any]:
    positive = check_compiler_input_isolation(run_dir)
    bad_static = scan_compiler_source("def compile(target_expr):\n    if target_expr.startswith('collinear'):\n        return 'bad'\n")
    with tempfile.TemporaryDirectory() as tmp:
        fixture = prepare_compiler_fixture(Path(tmp))
        naked = copy.deepcopy(fixture["selected_derivation"])
        naked["derivation_steps"] = [naked["derivation_steps"][1]]
        naked["derivation_steps"][0]["input_refs"] = []
        naked["selected_facts"] = []
        naked["selected_certificates"] = []
        bad_compile = compile_selected_derivation(
            claim_spec=fixture["claim"],
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation=naked,
            selected_solver_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry=fixture["rule_registry"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
        missing_operator = copy.deepcopy(fixture["selected_derivation"])
        missing_operator["derivation_steps"][1].pop("proof_selection_source", None)
        missing_operator["derivation_steps"][1].pop("derivation_operator", None)
        missing_operator_compile = compile_selected_derivation(
            claim_spec=fixture["claim"],
            claim_spec_ref=fixture["claim_ref"],
            selected_derivation=missing_operator,
            selected_solver_derivation_ref=fixture["selected_derivation_ref"],
            rule_registry=fixture["rule_registry"],
            rule_registry_ref=fixture["rule_registry_ref"],
            side_condition_checker_refs=fixture["side_condition_checker_refs"],
        )
    errors: list[str] = []
    if positive["status"] != "passed":
        errors.append("positive_input_isolation_failed")
    if bad_static["status"] != "failed" or "target_expr_startswith" not in bad_static["errors"]:
        errors.append("proof_from_shape_static_not_rejected")
    if bad_compile["status"] != "failed" or "naked_target_assertion" not in bad_compile["errors"]:
        errors.append("naked_target_derivation_not_rejected")
    if missing_operator_compile["status"] != "failed" or not any("derivation_operator" in error or "proof_selection" in error for error in missing_operator_compile.get("errors", [])):
        errors.append("missing_artifact_operator_derivation_not_rejected")
    return {
        "schema_version": "CompilerInputIsolationSelfTestV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "positive": positive,
        "bad_static": bad_static,
        "bad_compile": bad_compile,
        "missing_operator_compile": missing_operator_compile,
    }


if __name__ == "__main__":
    raise SystemExit(main())
