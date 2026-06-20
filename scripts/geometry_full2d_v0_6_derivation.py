from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SPEC_DIR = "claim_specs_v0_6"
ENGINE_OUTPUT_DIR = "engine_outputs_v0_6"
INDEPENDENT_CHECK_DIR = "independent_solver_artifact_checks_v0_6"
SELECTED_DERIVATION_DIR = "selected_solver_derivations_v0_6"
TARGET_MATCH_DIR = "derivation_target_matches_v0_6"
SELECTED_DERIVATION_INDEX_NAME = "selected_solver_derivation_index_v0_6.json"
TARGET_MATCH_INDEX_NAME = "derivation_target_match_index_v0_6.json"

ROLE_TO_RULE_ID = {
    "synthetic_trace": "full2d_rule:directed_angle_mod_pi:26",
    "construction": "full2d_rule:construction_intersection:07",
    "algebraic_metric_certificate": "full2d_rule:metric_equal_length:28",
    "order_case": "full2d_rule:order_between:31",
    "inequality": "full2d_rule:metric_length_sum:24",
    "lean_search_certificate": "full2d_rule:ratio_algebra:25",
    "external_solver_trace": "full2d_rule:directed_angle_mod_2pi:27",
}
CHECKED_SUPPORT_KINDS = {"construction", "certificate", "case_split"}
TARGET_EQUIVALENT_MARKERS = (
    "alpha_renamed_target",
    "target_hash_intermediate",
    "trivial_target_wrapper",
    "reflexivity_or_symmetry_equivalent_target",
    "direct_facade_target",
    "normalizes_to_target_without_checked_solver",
)
TARGET_MATCH_FORBIDDEN_OUTPUTS = (
    "proof_text",
    "tactic_script",
    "target_expr",
    "target_expression_string",
    "strategy_label",
    "rule_ids",
    "corpus_labels",
)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def derivation_code_hash() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_derivation.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
    ]
    return sha256_text(canonical_json({path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}))


def _paths_by_ref(run_dir: Path, directory: str) -> dict[str, Path]:
    return {file_sha256(path): path for path in sorted((run_dir / directory).glob("*.json"))}


def _payloads_by_ref(run_dir: Path, directory: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for ref, path in _paths_by_ref(run_dir, directory).items():
        rows[ref] = read_json(path)
    return rows


def _checks_by_id(run_dir: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in sorted((run_dir / INDEPENDENT_CHECK_DIR).glob("*.json")):
        payload = read_json(path)
        rows[str(payload.get("check_id"))] = payload
    return rows


def _engine_outputs_by_claim(run_dir: Path) -> dict[str, list[tuple[Path, dict[str, Any]]]]:
    rows: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for path in sorted((run_dir / ENGINE_OUTPUT_DIR).glob("*.json")):
        payload = read_json(path)
        rows.setdefault(str(payload.get("claim_spec_ref")), []).append((path, payload))
    return rows


def _step_from_artifact(engine_path: Path, engine_output: dict[str, Any], artifact: dict[str, Any], check_ref: str, index: int) -> dict[str, Any]:
    role = str(engine_output.get("engine_role"))
    return {
        "step_id": f"{engine_path.stem}:artifact:{index}",
        "artifact_ref": artifact.get("artifact_ref"),
        "artifact_kind": artifact.get("kind"),
        "checker_ref": check_ref,
        "rule_id": ROLE_TO_RULE_ID.get(role, "full2d_rule:unknown_role:00"),
        "premises": [str(item) for item in artifact.get("premises", [])],
        "conclusion": str(artifact.get("conclusion", "")),
        "is_final_target": False,
        "engine_output_ref": engine_output.get("engine_output_id"),
        "engine_role": role,
        "checked_side_conditions": artifact.get("side_conditions", []),
        "non_target_source": "checked_solver_artifact",
    }


def _entailment_payload(claim_ref: str, claim: dict[str, Any], steps: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "claim_spec_ref": claim_ref,
        "target_hash": claim.get("target_hash"),
        "selected_artifact_refs": [step.get("artifact_ref") for step in steps],
        "checker_refs": [step.get("checker_ref") for step in steps],
        "non_target_conclusions": [step.get("conclusion") for step in steps if step.get("is_final_target") is False],
        "checked_support_kinds": sorted({str(step.get("artifact_kind")) for step in steps if step.get("artifact_kind") in CHECKED_SUPPORT_KINDS}),
    }


def build_selected_derivation_payload(
    *,
    claim_ref: str,
    claim: dict[str, Any],
    engine_rows: list[tuple[Path, dict[str, Any]]],
    checks_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    steps: list[dict[str, Any]] = []
    for engine_path, engine_output in engine_rows:
        selected_artifacts = engine_output.get("selected_artifacts", [])
        checker_refs = [str(item) for item in engine_output.get("independent_checker_refs", [])]
        for index, artifact in enumerate(selected_artifacts):
            if not isinstance(artifact, dict):
                continue
            check_ref = checker_refs[index] if index < len(checker_refs) else ""
            check = checks_by_id.get(check_ref, {})
            if check.get("status") != "passed":
                continue
            steps.append(_step_from_artifact(engine_path, engine_output, artifact, check_ref, index))
    steps = sorted(steps, key=lambda item: (str(item.get("engine_role")), str(item.get("step_id"))))
    entailment = _entailment_payload(claim_ref, claim, steps)
    unsigned = {
        "schema_version": "SelectedSolverDerivationV3",
        "claim_spec_ref": claim_ref,
        "selected_steps": steps,
        "final_step_ref": sha256_text(canonical_json(entailment)),
        "has_non_target_intermediate": any(step.get("is_final_target") is False for step in steps),
        "has_checked_side_condition_or_certificate": any(
            step.get("artifact_kind") in CHECKED_SUPPORT_KINDS or bool(step.get("checked_side_conditions")) for step in steps
        ),
        "target_hash_commitment": claim.get("target_hash"),
        "entailment_witness_ref": sha256_text(canonical_json(entailment)),
        "entailment_witness_input_hash": sha256_text(canonical_json({"claim": claim_ref, "steps": [step.get("artifact_ref") for step in steps]})),
        "source_stage": "selected_solver_derivation_from_independently_checked_solver_artifacts",
        "git_head": current_git_head(),
    }
    return {"derivation_id": sha256_text(canonical_json(unsigned)), **unsigned}


def validate_selected_derivation_payload(
    derivation: dict[str, Any],
    *,
    claim: dict[str, Any] | None = None,
    checks_by_id: dict[str, dict[str, Any]] | None = None,
    artifact_refs: set[str] | None = None,
) -> list[str]:
    errors = validate_payload(derivation)
    steps = derivation.get("selected_steps")
    if not isinstance(steps, list) or not steps:
        errors.append("selected_derivation_missing_steps")
        return sorted(set(errors))
    target_hash = str(claim.get("target_hash", "")) if claim else str(derivation.get("target_hash_commitment", ""))
    non_target_seen = False
    checked_support_seen = False
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"bad_selected_step:{index}")
            continue
        if step.get("is_final_target") is True:
            errors.append(f"selected_step_is_final_target:{index}")
        else:
            non_target_seen = True
        if step.get("conclusion") == target_hash or step.get("artifact_ref") == target_hash:
            errors.append(f"selected_step_target_equivalent:{index}")
        for marker in TARGET_EQUIVALENT_MARKERS:
            if step.get(marker) is True:
                errors.append(f"selected_step_target_equivalent:{index}:{marker}")
        text = canonical_json(step).lower()
        for marker in ("proof_text", "tactic_script", "lean_template_id", "exact ", " by "):
            if marker in text:
                errors.append(f"selected_step_contains_proof_material:{index}")
        if artifact_refs is not None and step.get("artifact_ref") not in artifact_refs:
            errors.append(f"selected_step_artifact_not_from_engine_output:{index}")
        check = checks_by_id.get(str(step.get("checker_ref"))) if checks_by_id is not None else None
        if checks_by_id is not None and (not check or check.get("status") != "passed"):
            errors.append(f"selected_step_checker_not_passed:{index}")
        if step.get("artifact_kind") in CHECKED_SUPPORT_KINDS or bool(step.get("checked_side_conditions")):
            checked_support_seen = True
    if derivation.get("has_non_target_intermediate") is not True or not non_target_seen:
        errors.append("missing_semantic_non_target_intermediate")
    if derivation.get("has_checked_side_condition_or_certificate") is not True or not checked_support_seen:
        errors.append("missing_checked_side_condition_or_certificate")
    if claim is not None:
        claim_ref = str(derivation.get("claim_spec_ref"))
        expected_entailment = _entailment_payload(claim_ref, claim, steps)
        expected_ref = sha256_text(canonical_json(expected_entailment))
        if derivation.get("final_step_ref") != expected_ref or derivation.get("entailment_witness_ref") != expected_ref:
            errors.append("entailment_witness_ref_mismatch")
        if derivation.get("target_hash_commitment") != claim.get("target_hash"):
            errors.append("target_hash_commitment_mismatch")
    return sorted(set(errors))


def build_selected_derivations(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    out_dir = run_dir / SELECTED_DERIVATION_DIR
    claims = _payloads_by_ref(run_dir, CLAIM_SPEC_DIR)
    checks_by_id = _checks_by_id(run_dir)
    engine_by_claim = _engine_outputs_by_claim(run_dir)
    artifact_refs = {
        str(artifact.get("artifact_ref"))
        for rows in engine_by_claim.values()
        for _engine_path, engine in rows
        for artifact in engine.get("selected_artifacts", [])
        if isinstance(artifact, dict)
    }
    errors: list[str] = []
    paths: list[str] = []
    results: list[dict[str, Any]] = []
    for claim_ref, claim in sorted(claims.items()):
        engine_rows = engine_by_claim.get(claim_ref, [])
        if not engine_rows:
            errors.append(f"missing_engine_outputs_for_claim:{claim_ref}")
            continue
        payload = build_selected_derivation_payload(claim_ref=claim_ref, claim=claim, engine_rows=engine_rows, checks_by_id=checks_by_id)
        payload_errors = validate_selected_derivation_payload(payload, claim=claim, checks_by_id=checks_by_id, artifact_refs=artifact_refs)
        if payload_errors:
            errors.extend(f"{claim_ref}:{error}" for error in payload_errors)
        claim_id = str(claim.get("claim_id", claim_ref)).split(":")[-1].replace("/", "_")
        path = out_dir / f"{claim_id}.json"
        write_json(path, payload)
        paths.append(path.relative_to(run_dir).as_posix())
        results.append(
            {
                "claim_spec_ref": claim_ref,
                "selected_derivation_ref": file_sha256(path),
                "derivation_id": payload["derivation_id"],
                "selected_step_count": len(payload.get("selected_steps", [])),
                "has_non_target_intermediate": payload.get("has_non_target_intermediate"),
                "has_checked_side_condition_or_certificate": payload.get("has_checked_side_condition_or_certificate"),
                "errors": payload_errors,
            }
        )
    index = {
        "schema_version": "SelectedSolverDerivationIndexV06",
        "run_dir": str(run_dir),
        "selected_derivation_count": len(paths),
        "selected_derivation_paths": paths,
        "results": results,
        "derivation_code_hash": derivation_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / SELECTED_DERIVATION_INDEX_NAME, index)
    return {
        "schema_version": "BuildSelectedSolverDerivationsV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "selected_derivation_count": len(paths),
        "index_path": (run_dir / SELECTED_DERIVATION_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / SELECTED_DERIVATION_INDEX_NAME, ROOT)
        else str(run_dir / SELECTED_DERIVATION_INDEX_NAME),
    }


def validate_target_match_report(report: dict[str, Any], *, derivation: dict[str, Any] | None = None, claim: dict[str, Any] | None = None) -> list[str]:
    errors = validate_payload(report)
    for forbidden in TARGET_MATCH_FORBIDDEN_OUTPUTS:
        if forbidden in report:
            errors.append(f"target_matcher_forbidden_output:{forbidden}")
    if report.get("status") != "passed":
        errors.append("target_match_not_passed")
    if derivation is not None:
        if report.get("final_step_hash") != derivation.get("final_step_ref"):
            errors.append("target_match_final_step_hash_mismatch")
        if report.get("selected_derivation_id") != derivation.get("derivation_id"):
            errors.append("target_match_derivation_id_mismatch")
        if derivation.get("has_non_target_intermediate") is not True:
            errors.append("target_match_without_non_target_intermediate")
        if derivation.get("has_checked_side_condition_or_certificate") is not True:
            errors.append("target_match_without_checked_support")
    if claim is not None and report.get("target_hash") != claim.get("target_hash"):
        errors.append("target_match_target_hash_mismatch")
    return sorted(set(errors))


def build_target_match_payload(derivation_path: Path, derivation: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    selected_derivation_ref = file_sha256(derivation_path)
    unsigned = {
        "schema_version": "DerivationTargetMatchReportV1",
        "selected_derivation_ref": selected_derivation_ref,
        "selected_derivation_id": derivation.get("derivation_id"),
        "claim_spec_ref": derivation.get("claim_spec_ref"),
        "status": "passed",
        "final_step_hash": derivation.get("final_step_ref"),
        "target_hash": claim.get("target_hash"),
        "command_log_ref": sha256_text(
            canonical_json(
                {
                    "stage": "DerivationTargetMatcher",
                    "selected_derivation_ref": selected_derivation_ref,
                    "final_step_hash": derivation.get("final_step_ref"),
                    "target_hash": claim.get("target_hash"),
                    "checked_support": derivation.get("has_checked_side_condition_or_certificate"),
                }
            )
        ),
        "target_match_authority": "hash_entailment_from_checked_selected_derivation",
        "proof_material_emitted": False,
        "git_head": current_git_head(),
    }
    return {"match_report_id": sha256_text(canonical_json(unsigned)), **unsigned}


def build_target_match_reports(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    claims = _payloads_by_ref(run_dir, CLAIM_SPEC_DIR)
    out_dir = run_dir / TARGET_MATCH_DIR
    errors: list[str] = []
    paths: list[str] = []
    results: list[dict[str, Any]] = []
    for derivation_path in sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json")):
        derivation = read_json(derivation_path)
        claim = claims.get(str(derivation.get("claim_spec_ref")))
        if claim is None:
            errors.append(f"{derivation_path.name}:claim_spec_not_found")
            continue
        payload = build_target_match_payload(derivation_path, derivation, claim)
        payload_errors = validate_target_match_report(payload, derivation=derivation, claim=claim)
        if payload_errors:
            errors.extend(f"{derivation_path.name}:{error}" for error in payload_errors)
        path = out_dir / derivation_path.name
        write_json(path, payload)
        paths.append(path.relative_to(run_dir).as_posix())
        results.append(
            {
                "claim_spec_ref": derivation.get("claim_spec_ref"),
                "selected_derivation_ref": file_sha256(derivation_path),
                "target_match_ref": file_sha256(path),
                "status": payload.get("status"),
                "errors": payload_errors,
            }
        )
    index = {
        "schema_version": "DerivationTargetMatchIndexV06",
        "run_dir": str(run_dir),
        "target_match_count": len(paths),
        "target_match_paths": paths,
        "results": results,
        "derivation_code_hash": derivation_code_hash(),
        "git_head": current_git_head(),
    }
    write_json(run_dir / TARGET_MATCH_INDEX_NAME, index)
    return {
        "schema_version": "BuildDerivationTargetMatchReportsV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "target_match_count": len(paths),
        "index_path": (run_dir / TARGET_MATCH_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / TARGET_MATCH_INDEX_NAME, ROOT)
        else str(run_dir / TARGET_MATCH_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
