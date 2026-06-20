from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.geometry_full2d_v0_6_extraction import canonical_json, write_json
from scripts.geometry_full2d_v0_6_proof_worker import (
    LEAN_PATCH_DIR,
    THEOREM_ANCHOR_DIR,
    apply_lean_patch_candidate_v0_6,
    build_solver_backed_certificate_v0_6,
    current_git_head,
    final_verify_gate_v0_6,
    run_proof_worker_final_verify_stage,
    sha256_text,
)
from scripts.geometry_full2d_v0_6_red_cases import evaluate_fixture, load_manifest
from scripts.geometry_full2d_v0_6_schemas import validate_payload


def source_text(theorem_name: str, *, replacement: str = "  sorry") -> str:
    return "\n".join(
        [
            "import MathAutoResearch.GeometryFull2D.Inequality",
            "",
            "namespace MathAutoResearch.GeometryFull2D",
            "",
            f"theorem {theorem_name} (A B : Point) : collinear A A B := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            replacement,
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
            "end MathAutoResearch.GeometryFull2D",
            "",
        ]
    )


def anchor_for(source_path: Path, theorem_name: str) -> dict[str, Any]:
    unsigned = {
        "schema_version": "TheoremAnchorV1",
        "theorem_name": theorem_name,
        "source_file_path": str(source_path),
        "source_file_ref": sha256_text(source_path.read_text(encoding="utf-8")),
        "proof_region": {
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "statement_hash": sha256_text(theorem_name),
        "binder_map": {"A": "point:A", "B": "point:B"},
        "proof_region_identity": sha256_text("region:" + theorem_name),
        "binder_map_identity": sha256_text("binder:" + theorem_name),
        "anchor_use_policy": "locate_and_patch_only",
        "git_head": current_git_head(),
    }
    return {"anchor_ref": sha256_text(canonical_json(unsigned)), **unsigned}


def patch_for(anchor: dict[str, Any], patch_text: str, *, inside_marp_region: bool = True) -> dict[str, Any]:
    unsigned = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": sha256_text("compiler:" + str(anchor.get("anchor_ref"))),
        "patch_text_hash": sha256_text(patch_text),
        "patch_region": "MARP",
        "inside_marp_region": inside_marp_region,
        "theorem_anchor_ref": anchor.get("anchor_ref"),
        "patch_replacement_text": patch_text,
        "proof_plan_hash": sha256_text("self-test-proof-plan"),
        "proof_plan": {
            "schema_version": "CompilerProofPlanV06",
            "proof_strategy_source": "self_test_fixture_not_release_evidence",
            "used_rule_ids": ["self_test_fixture"],
            "step_artifact_refs": [sha256_text("artifact")],
            "step_checker_refs": [sha256_text("checker")],
        },
        "patch_generation_source": "check_proof_worker_final_verify_v0_6_self_test",
        "mutates_theorem_statement": False,
        "git_head": current_git_head(),
    }
    return {"patch_id": sha256_text(canonical_json(unsigned)), **unsigned}


def run_positive_fixture(root: Path) -> dict[str, Any]:
    theorem_name = "wp10_v06_positive"
    source_path = root / "WP10Positive.lean"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    anchor = anchor_for(source_path, theorem_name)
    patch = patch_for(anchor, "  exact collinear_refl_left A B")
    worker = apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=anchor,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id="wp10_positive",
    )
    final = final_verify_gate_v0_6(
        source_path=source_path,
        candidate_path=Path(str(worker.get("generated_candidate_path"))),
        theorem_anchor=anchor,
        proof_worker_result=worker,
        output_dir=root / "out",
    )
    errors: list[str] = []
    worker_schema = validate_payload(worker, current_head=current_git_head())
    final_schema = validate_payload(final, current_head=current_git_head())
    errors.extend(f"worker_schema:{error}" for error in worker_schema)
    errors.extend(f"final_schema:{error}" for error in final_schema)
    if worker.get("status") != "patch_applied":
        errors.append("worker_not_patch_applied")
    if worker.get("claim_final_theorem") is not False:
        errors.append("worker_claimed_final_theorem")
    if final.get("status") != "passed":
        errors.append("final_verify_not_passed")
    if final.get("lake_env_lean_returncode") != 0:
        errors.append("lake_env_lean_nonzero")
    certificate = build_solver_backed_certificate_v0_6(
        actual_task_run_ref=sha256_text("self_test_actual_task_run"),
        claim_spec_ref=sha256_text("self_test_claim_spec"),
        engine_output_refs=[sha256_text("self_test_engine_output")],
        selected_derivation_ref=sha256_text("self_test_selected_derivation"),
        compiler_result_ref=str(patch["compiler_result_ref"]),
        proof_worker_result_ref=str(worker.get("worker_result_id")),
        final_verify_report_ref=str(final.get("verify_report_id")),
        solver_causality_live_run_ref=sha256_text("self_test_solver_causality_live_run"),
    )
    certificate_errors = validate_payload(certificate, current_head=current_git_head())
    errors.extend(f"certificate_schema:{error}" for error in certificate_errors)
    return {
        "schema_version": "ProofWorkerFinalVerifyPositiveFixtureV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "worker": worker,
        "final_verify": final,
        "certificate_binding": certificate,
    }


def run_worker_negative(root: Path, name: str, *, source_replacement: str = "  sorry", inside_marp_region: bool = True) -> dict[str, Any]:
    theorem_name = f"wp10_v06_worker_negative_{name}"
    source_path = root / f"{theorem_name}.lean"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_text(theorem_name, replacement=source_replacement), encoding="utf-8")
    anchor = anchor_for(source_path, theorem_name)
    patch = patch_for(anchor, "  exact collinear_refl_left A B", inside_marp_region=inside_marp_region)
    return apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=anchor,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id=name,
    )


def run_final_negative(root: Path, name: str, *, mutate: str) -> dict[str, Any]:
    theorem_name = f"wp10_v06_final_negative_{name}"
    source_path = root / f"{theorem_name}.lean"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    anchor = anchor_for(source_path, theorem_name)
    patch = patch_for(anchor, "  exact collinear_refl_left A B")
    worker = apply_lean_patch_candidate_v0_6(
        source_path=source_path,
        theorem_anchor=anchor,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id=name,
    )
    candidate_path = Path(str(worker.get("generated_candidate_path")))
    text = candidate_path.read_text(encoding="utf-8")
    if mutate == "statement_changed":
        text = text.replace("collinear A A B", "collinear A B A")
    elif mutate == "sorry_present":
        text = text.replace("exact collinear_refl_left A B", "sorry")
    elif mutate == "admit_present":
        text = text.replace("exact collinear_refl_left A B", "admit")
    elif mutate == "axiom_present":
        text += "\naxiom forbidden_wp10_v06 : True\n"
    elif mutate == "unsafe_present":
        text += "\nunsafe axiom forbidden_unsafe_wp10_v06 : True\n"
    elif mutate == "toy_target_definition":
        text += "\ndef ToyGeometry := True\n"
    elif mutate == "non_admitted_import":
        text = "import System.IO\n" + text
    elif mutate == "stale_candidate_hash":
        text = text.replace("exact collinear_refl_left A B", "exact collinear_refl_left A B\n  -- stale candidate mutation")
    else:
        raise ValueError(f"unknown final negative mutation: {mutate}")
    candidate_path.write_text(text, encoding="utf-8")
    return final_verify_gate_v0_6(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_anchor=anchor,
        proof_worker_result=worker,
        output_dir=root / "out_negative",
    )


def self_test_report() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        positive = run_positive_fixture(root / "positive")
        run_dir_failure = run_dir_failure_fixture(root / "run_dir_failure")
        negatives = {
            "preproved_source": run_worker_negative(root / "neg_preproved", "preproved_source", source_replacement="  exact collinear_refl_left A B"),
            "patch_outside_region": run_worker_negative(root / "neg_outside", "patch_outside_region", inside_marp_region=False),
            "statement_changed": run_final_negative(root / "neg_statement", "statement_changed", mutate="statement_changed"),
            "sorry_present": run_final_negative(root / "neg_sorry", "sorry_present", mutate="sorry_present"),
            "admit_present": run_final_negative(root / "neg_admit", "admit_present", mutate="admit_present"),
            "axiom_present": run_final_negative(root / "neg_axiom", "axiom_present", mutate="axiom_present"),
            "unsafe_present": run_final_negative(root / "neg_unsafe", "unsafe_present", mutate="unsafe_present"),
            "toy_target_definition": run_final_negative(root / "neg_toy", "toy_target_definition", mutate="toy_target_definition"),
            "non_admitted_import": run_final_negative(root / "neg_import", "non_admitted_import", mutate="non_admitted_import"),
            "stale_candidate_hash": run_final_negative(root / "neg_stale", "stale_candidate_hash", mutate="stale_candidate_hash"),
        }
    expected_errors = {
        "preproved_source": "source_theorem_not_sorry_only",
        "patch_outside_region": "patch_not_inside_marp_region",
        "statement_changed": "theorem_statement_changed",
        "sorry_present": "sorry_present",
        "admit_present": "admit_present",
        "axiom_present": "axiom_present",
        "unsafe_present": "unsafe_present",
        "toy_target_definition": "toy_target_definitions",
        "non_admitted_import": "non_admitted_imports",
        "stale_candidate_hash": "stale_or_mismatched_candidate_hash",
    }
    errors: list[str] = []
    if positive.get("status") != "passed":
        errors.append("positive_fixture_failed")
    if run_dir_failure.get("status") != "passed":
        errors.append("run_dir_failure_fixture_failed")
    negative_results: dict[str, dict[str, Any]] = {}
    for name, expected in expected_errors.items():
        report = negatives[name]
        observed_errors = [str(item) for item in report.get("errors", [])]
        rejected = report.get("status") == "failed" and expected in observed_errors
        if not rejected:
            errors.append(f"negative_not_rejected:{name}:{expected}")
        negative_results[name] = {
            "status": report.get("status"),
            "expected_error": expected,
            "observed_errors": observed_errors,
            "rejected": rejected,
        }
    return {
        "schema_version": "ProofWorkerFinalVerifySelfTestV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "positive": positive,
        "run_dir_failure_fixture": run_dir_failure,
        "negative_results": negative_results,
    }


def run_dir_failure_fixture(root: Path) -> dict[str, Any]:
    theorem_name = "wp10_v06_run_dir_failure"
    source_path = root / "RunDirFailure.lean"
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    anchor = anchor_for(source_path, theorem_name)
    patch = patch_for(anchor, "  exact solver_missing_wp10_v06_proof")
    write_json(root / THEOREM_ANCHOR_DIR / "run_dir_failure.json", anchor)
    write_json(root / LEAN_PATCH_DIR / "run_dir_failure.json", patch)
    stage = run_proof_worker_final_verify_stage(root)
    observed_errors = [str(item) for item in stage.get("errors", [])]
    rejected = stage.get("status") == "failed" and any("final_verify_status_not_passed" in item for item in observed_errors)
    errors = [] if rejected else ["run_dir_final_verify_failure_not_rejected"]
    return {
        "schema_version": "ProofWorkerFinalVerifyRunDirFailureFixtureV06",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "stage_status": stage.get("status"),
        "observed_errors": observed_errors,
    }


def red_case_report() -> dict[str, Any]:
    manifest = load_manifest()
    wanted = {"RC-015": "K-034", "RC-016": "K-024"}
    rows = []
    errors: list[str] = []
    for fixture in manifest.get("fixtures", []):
        if isinstance(fixture, dict) and fixture.get("red_case_id") in wanted:
            row = evaluate_fixture(fixture)
            rows.append(row)
            expected = wanted[str(fixture.get("red_case_id"))]
            if expected not in row.get("detected_K", []):
                errors.append(f"{fixture.get('red_case_id')}:{expected}_not_detected")
            if not row.get("positive_control_passed"):
                errors.append(f"{fixture.get('red_case_id')}:positive_control_failed")
    local_negative_expectations = {
        "worker_claims_final": {"schema_version": "ProofWorkerResultFull2D", "worker_result_id": sha256_text("worker"), "lean_patch_candidate_ref": sha256_text("patch"), "patched_candidate_ref": sha256_text("candidate"), "proof_region_only": True, "worker_command_log_ref": sha256_text("cmd"), "claim_final_theorem": True, "git_head": "test-head"},
        "final_verify_accepts_sorry": {"schema_version": "FinalVerifyReportFull2D", "verify_report_id": sha256_text("verify"), "patched_candidate_ref": sha256_text("candidate"), "lake_env_lean_command": ["lake", "env", "lean", "Candidate.lean"], "status": "passed", "theorem_statement_unchanged": True, "no_sorry": False, "no_admit": True, "no_axiom": True, "no_unsafe": True, "protected_theorem_unchanged": True, "command_log_ref": sha256_text("cmd"), "candidate_hash": sha256_text("candidate"), "git_head": "test-head"},
        "final_verify_not_lake": {"schema_version": "FinalVerifyReportFull2D", "verify_report_id": sha256_text("verify"), "patched_candidate_ref": sha256_text("candidate"), "lake_env_lean_command": ["lean", "Candidate.lean"], "status": "passed", "theorem_statement_unchanged": True, "no_sorry": True, "no_admit": True, "no_axiom": True, "no_unsafe": True, "protected_theorem_unchanged": True, "command_log_ref": sha256_text("cmd"), "candidate_hash": sha256_text("candidate"), "git_head": "test-head"},
    }
    local_results = {name: validate_payload(payload, current_head="test-head") for name, payload in local_negative_expectations.items()}
    for name, result in local_results.items():
        if not result:
            errors.append(f"local_negative_unrejected:{name}")
    return {
        "schema_version": "ProofWorkerFinalVerifyRedCaseReportV06",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "manifest_cases": rows,
        "local_negative_results": local_results,
    }


def run_dir_report(run_dir: Path) -> dict[str, Any]:
    return run_proof_worker_final_verify_stage(run_dir)


def check_proof_worker_final_verify(run_dir: Path | None, *, self_test: bool, red_cases: bool) -> dict[str, Any]:
    errors: list[str] = []
    self_report = self_test_report() if self_test else None
    if self_report:
        errors.extend(f"self_test:{error}" for error in self_report.get("errors", []))
    red_report = red_case_report() if red_cases else None
    if red_report:
        errors.extend(f"red_cases:{error}" for error in red_report.get("errors", []))
    run_report = run_dir_report(run_dir) if run_dir is not None else None
    if run_report:
        errors.extend(f"run_dir:{error}" for error in run_report.get("errors", []))
    return {
        "schema_version": "CheckProofWorkerFinalVerifyV06Report",
        "checker_name": "check_proof_worker_final_verify_v0_6.py",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "self_test": self_report,
        "red_cases": red_report,
        "run_dir_report": run_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check GeometryFull2D v0.6 ProofWorker and FinalVerifyGate.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--red-cases", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check_proof_worker_final_verify(args.run_dir, self_test=args.self_test, red_cases=args.red_cases)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        write_json(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
