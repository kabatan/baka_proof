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

from math_auto_research.lean_integration.goal_anchor import extract_theorem_statement, hash_text
from plugins.geometry_full2d.proof_worker_v0_5 import (
    apply_lean_patch_candidate_full2d_v0_5,
    final_verify_gate_full2d_v0_5,
    make_lean_patch_candidate,
    sha256_file,
    sha256_text,
    write_json,
)
from scripts.geometry_full2d_v0_5_schemas import validate_payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", default="runs/geometry_full2d_v0_5")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_report = self_test_report(Path(args.run_dir))
        if has_proof_worker_final_verify_artifacts(Path(args.run_dir)):
            run_report = check_existing_reports(Path(args.run_dir))
            report = combined_report(
                "ProofWorkerFinalVerifySelfTestAndRunCheckV05",
                self_report,
                run_report,
                self_key="self_test",
                run_key="run_check",
            )
        else:
            report = self_report
    else:
        report = check_existing_reports(Path(args.run_dir))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def check_existing_reports(run_dir: Path) -> dict[str, Any]:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    worker_count = 0
    final_count = 0
    for path in proof_worker_report_paths(root):
        worker_count += 1
        payload = json.loads(path.read_text(encoding="utf-8"))
        errors.extend(f"{path.relative_to(root).as_posix()}:{error}" for error in validate_payload(payload, current_head="runtime"))
        if payload.get("worker_claims_final_theorem") is not False:
            errors.append(f"{path.relative_to(root).as_posix()}:worker_claims_final_theorem")
        if payload.get("proof_region_only") is not True:
            errors.append(f"{path.relative_to(root).as_posix()}:worker_not_proof_region_only")
    for path in final_verify_report_paths(root):
        final_count += 1
        payload = json.loads(path.read_text(encoding="utf-8"))
        errors.extend(f"{path.relative_to(root).as_posix()}:{error}" for error in validate_payload(payload, current_head="runtime"))
        if payload.get("status") == "passed" and payload.get("proof_use_status") != "final_theorem":
            errors.append(f"{path.relative_to(root).as_posix()}:passed_not_final_theorem")
        if payload.get("final_status_source") != "FinalVerifyReportFull2D":
            errors.append(f"{path.relative_to(root).as_posix()}:final_status_source_not_final_verify")
    return {
        "schema_version": "ProofWorkerFinalVerifyCheckV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "proof_worker_report_count": worker_count,
        "final_verify_report_count": final_count,
    }


def has_proof_worker_final_verify_artifacts(run_dir: Path) -> bool:
    root = run_dir if run_dir.is_absolute() else ROOT / run_dir
    return bool(proof_worker_report_paths(root) or final_verify_report_paths(root))


def proof_worker_report_paths(root: Path) -> list[Path]:
    paths = set(root.rglob("proof_worker_result.json"))
    aggregate = root / "proof_worker_results"
    if aggregate.exists():
        paths.update(path for path in aggregate.glob("*.json") if path.is_file())
    return sorted(paths)


def final_verify_report_paths(root: Path) -> list[Path]:
    paths = set(root.rglob("final_verify_report.json"))
    aggregate = root / "final_verify_reports"
    if aggregate.exists():
        paths.update(path for path in aggregate.glob("*.json") if path.is_file())
    return sorted(paths)


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


def self_test_report(run_dir: Path) -> dict[str, Any]:
    del run_dir
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        positive = run_positive_fixture(root / "positive")
        negatives = {
            "preproved_source": run_preproved_source_negative(root / "preproved_source"),
            "patch_outside_region": run_patch_outside_region_negative(root / "patch_outside_region"),
            "statement_changed": run_final_verify_negative(root / "statement_changed", mutate_statement=True),
            "sorry_present": run_final_verify_negative(root / "sorry_present", replacement="  sorry"),
            "forbidden_declaration": run_final_verify_negative(root / "forbidden_declaration", append_text="\naxiom forbidden_wp10 : True\n"),
            "toy_target_definition": run_final_verify_negative(root / "toy_target_definition", append_text="\ndef ToyGeometry := True\n"),
            "non_admitted_import": run_final_verify_negative(root / "non_admitted_import", prepend_text="import System.IO\n"),
        }
    errors: list[str] = []
    if positive["status"] != "passed":
        errors.append("positive_fixture_failed")
    expected_negative_errors = {
        "preproved_source": "source_theorem_not_sorry_only",
        "patch_outside_region": "patch_not_proof_region_only",
        "statement_changed": "theorem_statement_changed",
        "sorry_present": "sorry_present",
        "forbidden_declaration": "forbidden_declarations",
        "toy_target_definition": "toy_target_definitions",
        "non_admitted_import": "non_admitted_imports",
    }
    for name, expected in expected_negative_errors.items():
        report = negatives[name]
        if report["status"] != "failed" or expected not in report.get("errors", []):
            errors.append(f"negative_not_rejected:{name}:{expected}")
    return {
        "schema_version": "ProofWorkerFinalVerifySelfTestV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "positive": positive,
        "negatives": negatives,
    }


def run_positive_fixture(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    theorem_name = "wp10_positive"
    source_path = root / "WP10Positive.lean"
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    patch = valid_patch(source_path, theorem_name, "  exact collinear_refl_left A B")
    worker = apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id="wp10_self_test",
        task_id=theorem_name,
    )
    candidate_path = Path(str(worker.get("generated_candidate_path", "")))
    provenance = provenance_for(patch, worker)
    final = final_verify_gate_full2d_v0_5(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        target_obligation_id=f"obligation:{theorem_name}",
        proof_use_provenance=provenance,
        output_dir=root / "out",
    )
    errors: list[str] = []
    errors.extend(f"worker_schema:{error}" for error in validate_payload(worker, current_head="self-test"))
    errors.extend(f"final_schema:{error}" for error in validate_payload(final, current_head="self-test"))
    if worker.get("status") != "patch_applied":
        errors.append("worker_not_patch_applied")
    if final.get("status") != "passed":
        errors.append("final_verify_not_passed")
    if final.get("proof_use_status") != "final_theorem":
        errors.append("final_verify_not_final_theorem")
    if final.get("lake_env_lean_command", [])[:3] != ["lake", "env", "lean"]:
        errors.append("final_verify_did_not_use_lake_env_lean")
    if final.get("lake_env_lean_returncode") != 0:
        errors.append("lake_env_lean_nonzero")
    return {
        "schema_version": "ProofWorkerFinalVerifyPositiveFixtureV05",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "worker": worker,
        "final_verify": final,
    }


def run_preproved_source_negative(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    theorem_name = "wp10_preproved"
    source_path = root / "WP10Preproved.lean"
    source_path.write_text(source_text(theorem_name, replacement="  exact collinear_refl_left A B"), encoding="utf-8")
    patch = valid_patch(source_path, theorem_name, "  exact collinear_refl_left A B")
    return apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id="wp10_self_test",
        task_id=theorem_name,
    )


def run_patch_outside_region_negative(root: Path) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    theorem_name = "wp10_bad_patch"
    source_path = root / "WP10BadPatch.lean"
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    patch = valid_patch(source_path, theorem_name, "  exact collinear_refl_left A B")
    patch["proof_region_only"] = False
    return apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id="wp10_self_test",
        task_id=theorem_name,
    )


def run_final_verify_negative(
    root: Path,
    *,
    replacement: str = "  exact collinear_refl_left A B",
    mutate_statement: bool = False,
    append_text: str = "",
    prepend_text: str = "",
) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    theorem_name = "wp10_negative"
    source_path = root / "WP10Negative.lean"
    source_path.write_text(source_text(theorem_name), encoding="utf-8")
    patch = valid_patch(source_path, theorem_name, "  exact collinear_refl_left A B")
    worker = apply_lean_patch_candidate_full2d_v0_5(
        source_path=source_path,
        patch_candidate=patch,
        output_dir=root / "out",
        run_id="wp10_self_test",
        task_id=theorem_name,
    )
    candidate_path = Path(str(worker.get("generated_candidate_path", "")))
    candidate_text = candidate_path.read_text(encoding="utf-8")
    if replacement != "  exact collinear_refl_left A B":
        candidate_text = candidate_text.replace("  exact collinear_refl_left A B", replacement)
    if mutate_statement:
        candidate_text = candidate_text.replace("collinear A A B", "collinear A B A")
    if append_text:
        candidate_text += append_text
    if prepend_text:
        candidate_text = prepend_text + candidate_text
    candidate_path.write_text(candidate_text, encoding="utf-8")
    provenance = provenance_for(patch, worker)
    return final_verify_gate_full2d_v0_5(
        source_path=source_path,
        candidate_path=candidate_path,
        theorem_name=theorem_name,
        target_obligation_id=f"obligation:{theorem_name}",
        proof_use_provenance=provenance,
        output_dir=root / "out_negative",
    )


def valid_patch(source_path: Path, theorem_name: str, replacement: str) -> dict[str, Any]:
    statement_hash = hash_text(extract_theorem_statement(source_path.read_text(encoding="utf-8"), theorem_name))
    return make_lean_patch_candidate(
        compiler_result_ref=sha256_text("compiler:" + theorem_name),
        theorem_name=theorem_name,
        theorem_statement_hash=statement_hash,
        patch_text=replacement,
        solver_dependency_refs=(sha256_text("selected-derivation:" + theorem_name),),
    )


def provenance_for(patch: dict[str, Any], worker: dict[str, Any]) -> dict[str, str]:
    return {
        "claim_spec_ref": sha256_text("claim"),
        "compiler_result_ref": str(patch["compiler_result_ref"]),
        "lean_patch_candidate_ref": str(patch["patch_id"]),
        "proof_worker_result_ref": str(worker["worker_result_id"]),
        "proof_region_diff_ref": str(worker["proof_region_diff_ref"]),
        "generated_candidate_file_ref": str(worker["generated_candidate_file_ref"]),
    }


def source_text(theorem_name: str, *, replacement: str = "  sorry") -> str:
    return "\n".join(
        [
            "import MathAutoResearch.GeometryFull2D.Extraction",
            "",
            "open MathAutoResearch.GeometryFull2D",
            "",
            f"theorem {theorem_name} (A B : Point) (_h : A ≠ B) : collinear A A B := by",
            f"  -- MARP_PROOF_REGION_START:{theorem_name}",
            replacement,
            f"  -- MARP_PROOF_REGION_END:{theorem_name}",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
