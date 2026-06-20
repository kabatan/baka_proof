from __future__ import annotations

import argparse
import inspect
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_derivation_target_matcher_v0_6 import check_derivation_target_matcher
from scripts.geometry_full2d_v0_6_compiler import (
    COMPILER_RESULT_DIR,
    EXACT_COMPILE_INPUTS,
    FORBIDDEN_COMPILER_RESULT_KEYS,
    LEAN_PATCH_DIR,
    build_rule_registry_snapshot,
    compile_derivation,
    compiler_import_report,
    current_git_head,
    run_compiler_stage,
    sha256_text,
    side_condition_reports_from_derivation,
    validate_compiler_result_payload,
    validate_patch_candidate_payload,
)
from scripts.geometry_full2d_v0_6_derivation import SELECTED_DERIVATION_DIR, file_sha256
from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_red_cases import evaluate_fixture, load_manifest
from scripts.geometry_full2d_v0_6_schemas import run_self_test as schema_self_test


DEFAULT_RUN_DIR = ROOT / "runs" / "wp09_v0_6_fresh"


def safe_remove_run_dir(path: Path) -> None:
    resolved = path.resolve()
    runs_root = (ROOT / "runs").resolve()
    if not str(resolved).lower().startswith(str(runs_root).lower()):
        raise RuntimeError(f"refusing to remove outside runs directory: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def run_command(args: list[str]) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return {
        "args": args,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "status": "passed" if proc.returncode == 0 else "failed",
    }


def ensure_prerequisites(run_dir: Path, *, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    if fresh:
        safe_remove_run_dir(run_dir)
    report = check_derivation_target_matcher(run_dir, red_cases=False, fresh=True if fresh else False)
    return {
        "schema_version": "CompilerInputLockPrereqReportV06",
        "status": report["status"],
        "errors": report.get("errors", []),
        "run_dir": str(run_dir),
        "fresh": fresh,
        "target_matcher_report": report,
    }


def self_test_report() -> dict[str, Any]:
    errors: list[str] = []
    signature = inspect.signature(compile_derivation)
    expected_params = ["theorem_anchor", "selected_derivation", "rule_registry_snapshot", "side_condition_reports"]
    if list(signature.parameters) != expected_params:
        errors.append("compile_derivation_signature_not_exact")
    schema_report = schema_self_test()
    if schema_report.get("status") != "passed":
        errors.append("schema_self_test_failed")
    import_report = compiler_import_report()
    if import_report.get("status") != "passed":
        errors.extend(f"compiler_forbidden_import:{item}" for item in import_report.get("forbidden_imports", []))
    return {
        "schema_version": "CompilerInputLockSelfTestV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "signature": str(signature),
        "expected_parameters": expected_params,
        "schema_self_test_status": schema_report.get("status"),
        "compiler_import_report": import_report,
    }


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    rows = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") == "RC-004":
            row = evaluate_fixture(fixture)
            rows.append(row)
            for expected in ("K-015", "K-016"):
                if expected not in row.get("detected_K", []):
                    errors.append(f"RC-004:{expected}_not_detected")
            if not row.get("positive_control_passed"):
                errors.append("RC-004:positive_control_failed")

    base_result = {
        "schema_version": "CompilerResultFull2D",
        "compiler_result_id": "sha256:" + "a" * 64,
        "theorem_anchor_ref": "sha256:" + "b" * 64,
        "selected_derivation_ref": "sha256:" + "c" * 64,
        "rule_registry_snapshot_ref": "sha256:" + "d" * 64,
        "side_condition_report_refs": ["sha256:" + "e" * 64],
        "lean_patch_candidate_ref": "sha256:" + "f" * 64,
        "compiler_code_hash": "sha256:" + "1" * 64,
        "compile_inputs": EXACT_COMPILE_INPUTS,
        "git_head": current_git_head(),
    }
    local_cases = {
        "target_expr_input": {**base_result, "target_expr": "Collinear A B C"},
        "target_shape_id_input": {**base_result, "target_shape_id": "collinear"},
        "theorem_name_branch": {**base_result, "theorem_name": "v06_bootstrap_collinear_refl"},
        "statement_hash_branch": {**base_result, "statement_hash": "sha256:" + "2" * 64},
        "proof_region_identity_branch": {**base_result, "proof_region_identity": "region-1"},
        "binder_map_identity_branch": {**base_result, "binder_map_identity": "binder-1"},
        "wrong_api_inputs": {**base_result, "compile_inputs": ["TheoremAnchorV1", "SelectedSolverDerivationV3", "TargetMatchReport"]},
    }
    local_results = {name: validate_compiler_result_payload(payload) for name, payload in local_cases.items()}
    positive_errors = validate_compiler_result_payload(base_result)
    if positive_errors:
        errors.append("local_positive_compiler_result_rejected:" + ",".join(positive_errors))
    for name, result in local_results.items():
        if not result:
            errors.append(f"local_negative_unrejected:{name}")

    registry_snapshot = build_rule_registry_snapshot()
    first_counted_rule = next(rule for rule in registry_snapshot["rules"] if rule.get("counted_release_rule") is True)
    rule_id = str(first_counted_rule["rule_id"])
    selected_derivation = {
        "schema_version": "SelectedSolverDerivationV3",
        "derivation_id": "sha256:" + "9" * 64,
        "claim_spec_ref": "sha256:" + "8" * 64,
        "selected_steps": [
            {
                "step_id": "compiler-trace-positive-step",
                "artifact_ref": "sha256:" + "7" * 64,
                "artifact_kind": "certificate",
                "checker_ref": "sha256:" + "6" * 64,
                "rule_id": rule_id,
                "premises": ["hypothesis:h0"],
                "conclusion": "non_target_intermediate:compiler_trace_positive",
                "is_final_target": False,
                "checked_side_conditions": [{"kind": "compiler_trace_positive", "expr_hash": "sha256:" + "5" * 64}],
            },
            {
                "step_id": "compiler-trace-final-step",
                "artifact_ref": "sha256:" + "4" * 64,
                "artifact_kind": "fact",
                "checker_ref": "sha256:" + "3" * 64,
                "rule_id": rule_id,
                "premises": ["hypothesis:h0"],
                "conclusion": "sha256:" + "2" * 64,
                "is_final_target": True,
                "checked_side_conditions": [{"kind": "compiler_final_positive", "expr_hash": "sha256:" + "1" * 64}],
                "rule_application": {
                    "rule_id": rule_id,
                    "object_args": ["A", "B", "C"],
                    "premise_bindings": ["h0"],
                    "application_source": "claim_hypothesis_target_alignment_v0_6",
                },
            },
        ],
        "final_step_ref": "sha256:" + "2" * 64,
        "has_non_target_intermediate": True,
        "has_checked_side_condition_or_certificate": True,
        "git_head": current_git_head(),
    }
    anchor = {
        "schema_version": "TheoremAnchorV1",
        "anchor_ref": "sha256:" + "3" * 64,
        "theorem_name": "trace_positive_anchor",
        "statement_hash": "sha256:" + "2" * 64,
        "proof_region": {"start_marker": "-- START", "end_marker": "-- END"},
        "binder_map": {"A": "point:A"},
        "proof_region_identity": "trace-positive-region",
        "binder_map_identity": "trace-positive-binder",
        "git_head": current_git_head(),
    }
    side_reports = side_condition_reports_from_derivation(selected_derivation)
    positive_patch = compile_derivation(anchor, selected_derivation, registry_snapshot, side_reports)
    positive_patch_errors = validate_patch_candidate_payload(positive_patch)
    if positive_patch_errors:
        errors.append("local_positive_patch_rejected:" + ",".join(positive_patch_errors))
    fixed_menu_patch = {
        **positive_patch,
        "patch_replacement_text": positive_patch["patch_replacement_text"] + "\n  first\n  | exact collinear_refl_left A B",
    }
    missing_trace_patch = {
        **positive_patch,
        "patch_replacement_text": positive_patch["patch_replacement_text"].replace("registry_lean_lemma:", "registry_lean_lemma_missing:"),
    }
    bad_source_patch = json.loads(json.dumps(positive_patch))
    bad_source_patch["proof_plan"]["rendered_rule_steps"][0]["source"] = "target_shape_branch"
    patch_negative_cases = {
        "fixed_proof_menu": fixed_menu_patch,
        "missing_registry_trace": missing_trace_patch,
        "non_contract_render_source": bad_source_patch,
    }
    patch_negative_results = {name: validate_patch_candidate_payload(payload) for name, payload in patch_negative_cases.items()}
    for name, result in patch_negative_results.items():
        if not result:
            errors.append(f"local_patch_negative_unrejected:{name}")
    return {
        "schema_version": "CompilerInputLockRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "manifest_cases": rows,
        "local_positive_errors": positive_errors,
        "local_negative_results": local_results,
        "local_positive_patch_errors": positive_patch_errors,
        "local_patch_negative_results": patch_negative_results,
    }


def dynamic_taint_report(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    derivation_path = next(iter(sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json"))), None)
    if derivation_path is None:
        return {
            "schema_version": "CompilerDynamicTaintReportV06",
            "status": "failed",
            "errors": ["missing_selected_derivation_for_taint"],
        }
    selected_derivation = read_json(derivation_path)
    registry_snapshot = build_rule_registry_snapshot()
    side_reports = side_condition_reports_from_derivation(selected_derivation)
    base_anchor = {
        "schema_version": "TheoremAnchorV1",
        "anchor_ref": "sha256:" + "a" * 64,
        "theorem_name": "base_theorem",
        "statement_hash": "sha256:" + "b" * 64,
        "proof_region": {"start_marker": "-- START:base", "end_marker": "-- END:base"},
        "binder_map": {"A": "point:A", "B": "point:B", "M": "point:M", "h0": "hyp:h0"},
        "proof_region_identity": "base-region",
        "binder_map_identity": "base-binder",
        "target_expr": "poison-base",
        "theorem_family": "poison-base-family",
        "target_shape_id": "poison-base-shape",
        "task_id": "poison-base-task",
        "source_ref": "poison-base-source",
        "category": "poison-base-category",
        "difficulty_tier": "poison-base-tier",
    }
    base_patch = compile_derivation(base_anchor, selected_derivation, registry_snapshot, side_reports)
    baseline = {
        "patch_replacement_text": base_patch.get("patch_replacement_text"),
        "patch_text_hash": base_patch.get("patch_text_hash"),
        "proof_plan_hash": base_patch.get("proof_plan_hash"),
        "used_rule_ids": base_patch.get("proof_plan", {}).get("used_rule_ids"),
    }
    taint_cases: dict[str, dict[str, Any]] = {
        "theorem_name": {**base_anchor, "theorem_name": "TAINTED_THEOREM_NAME"},
        "statement_hash": {**base_anchor, "statement_hash": "sha256:" + "c" * 64},
        "proof_region_identity": {**base_anchor, "proof_region_identity": "TAINTED_REGION"},
        "binder_map_identity": {**base_anchor, "binder_map_identity": "TAINTED_BINDER"},
        "binder_map": {**base_anchor, "binder_map": {"X": "point:X", "Y": "point:Y"}},
        "raw_target_expr": {**base_anchor, "target_expr": "TAINTED_TARGET_EXPR"},
        "theorem_family": {**base_anchor, "theorem_family": "TAINTED_FAMILY"},
        "target_shape_id": {**base_anchor, "target_shape_id": "TAINTED_SHAPE"},
        "task_id": {**base_anchor, "task_id": "TAINTED_TASK"},
        "source_ref": {**base_anchor, "source_ref": "TAINTED_SOURCE"},
        "category": {**base_anchor, "category": "TAINTED_CATEGORY"},
        "difficulty_tier": {**base_anchor, "difficulty_tier": "TAINTED_TIER"},
    }
    case_results: dict[str, dict[str, Any]] = {}
    for name, anchor in taint_cases.items():
        patch = compile_derivation(anchor, selected_derivation, registry_snapshot, side_reports)
        observed = {
            "patch_replacement_text": patch.get("patch_replacement_text"),
            "patch_text_hash": patch.get("patch_text_hash"),
            "proof_plan_hash": patch.get("proof_plan_hash"),
            "used_rule_ids": patch.get("proof_plan", {}).get("used_rule_ids"),
        }
        stable = observed == baseline
        if not stable:
            errors.append(f"taint_changed_proof_plan_or_text:{name}")
        case_results[name] = {
            "stable": stable,
            "observed_hash": sha256_text(canonical_json(observed)),
        }
    return {
        "schema_version": "CompilerDynamicTaintReportV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "baseline_hash": sha256_text(canonical_json(baseline)),
        "case_results": case_results,
    }


def validate_compiler_outputs(run_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    compiler_rows: list[dict[str, Any]] = []
    for path in sorted((run_dir / COMPILER_RESULT_DIR).glob("*.json")):
        payload = read_json(path)
        payload_errors = validate_compiler_result_payload(payload)
        if payload_errors:
            errors.extend(f"{path.name}:{error}" for error in payload_errors)
        compiler_rows.append({"path": path.relative_to(run_dir).as_posix(), "errors": payload_errors})
    patch_rows: list[dict[str, Any]] = []
    for path in sorted((run_dir / LEAN_PATCH_DIR).glob("*.json")):
        payload = read_json(path)
        payload_errors = validate_patch_candidate_payload(payload)
        if payload_errors:
            errors.extend(f"{path.name}:{error}" for error in payload_errors)
        patch_rows.append({"path": path.relative_to(run_dir).as_posix(), "errors": payload_errors})
    if not compiler_rows:
        errors.append("missing_compiler_results")
    if not patch_rows:
        errors.append("missing_patch_candidates")
    return {
        "schema_version": "CompilerOutputValidationReportV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "compiler_rows": compiler_rows,
        "patch_rows": patch_rows,
    }


def check_compiler_input_lock(run_dir: Path, *, self_test: bool, red_cases: bool, dynamic_taint: bool, fresh: bool) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    prereq = ensure_prerequisites(run_dir, fresh=fresh)
    errors.extend(f"prereq:{error}" for error in prereq.get("errors", []))
    existing_compiler = list((run_dir / COMPILER_RESULT_DIR).glob("*.json")) if (run_dir / COMPILER_RESULT_DIR).exists() else []
    existing_patches = list((run_dir / LEAN_PATCH_DIR).glob("*.json")) if (run_dir / LEAN_PATCH_DIR).exists() else []
    derivation_count = len(list((run_dir / SELECTED_DERIVATION_DIR).glob("*.json"))) if (run_dir / SELECTED_DERIVATION_DIR).exists() else 0
    if not fresh and existing_compiler and existing_patches and len(existing_compiler) == derivation_count and len(existing_patches) == derivation_count:
        compiler_run = {
            "schema_version": "RunCompilerStageV06Report",
            "status": "passed",
            "errors": [],
            "run_dir": str(run_dir),
            "compiler_result_count": len(existing_compiler),
            "patch_candidate_count": len(existing_patches),
            "existing_outputs_reused": True,
        }
    else:
        compiler_run = run_compiler_stage(run_dir)
    errors.extend(f"compiler_run:{error}" for error in compiler_run.get("errors", []))
    output_validation = validate_compiler_outputs(run_dir)
    errors.extend(f"output_validation:{error}" for error in output_validation.get("errors", []))
    self_report = self_test_report() if self_test else None
    if self_report:
        errors.extend(f"self_test:{error}" for error in self_report.get("errors", []))
    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    taint_report = dynamic_taint_report(run_dir) if dynamic_taint else None
    if taint_report:
        errors.extend(f"dynamic_taint:{error}" for error in taint_report.get("errors", []))
    return {
        "schema_version": "CheckCompilerInputLockV06Report",
        "checker_name": "check_compiler_input_lock_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "prerequisites": prereq,
        "compiler_run": compiler_run,
        "output_validation": output_validation,
        "self_test": self_report,
        "red_cases": red_report,
        "dynamic_taint": taint_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 compiler input lock.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--dynamic-taint", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir or DEFAULT_RUN_DIR
    report = check_compiler_input_lock(run_dir, self_test=args.self_test, red_cases=args.red_cases, dynamic_taint=args.dynamic_taint, fresh=args.run_dir is None)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
