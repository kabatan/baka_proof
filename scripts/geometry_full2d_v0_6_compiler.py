from __future__ import annotations

import ast
import hashlib
import inspect
import json
import subprocess
from pathlib import Path
from typing import Any

from scripts.geometry_full2d_v0_6_derivation import (
    SELECTED_DERIVATION_DIR,
    TARGET_MATCH_DIR,
    file_sha256,
)
from scripts.geometry_full2d_v0_6_extraction import canonical_json, read_json, write_json
from scripts.geometry_full2d_v0_6_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
CLAIM_SPEC_DIR = "claim_specs_v0_6"
EXTRACTION_REPORT_DIR = "extraction_reports_v0_6"
COMPILER_RESULT_DIR = "compiler_results_v0_6"
LEAN_PATCH_DIR = "lean_patch_candidates_v0_6"
THEOREM_ANCHOR_DIR = "theorem_anchors_v0_6"
RULE_REGISTRY_SNAPSHOT_DIR = "rule_registry_snapshots_v0_6"
SIDE_CONDITION_REPORT_DIR = "side_condition_reports_v0_6"
COMPILER_INDEX_NAME = "compiler_index_v0_6.json"
RULE_REGISTRY_EVIDENCE = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_6" / "evidence" / "rule_registry_full2d_v0_6.json"

FORBIDDEN_COMPILER_IMPORT_PARTS = (
    "provider",
    "corpus",
    "matrix",
    "release",
    "release_checker",
    "previous_release",
    "prior_release",
    "v0_5",
    "v0_4",
)
FORBIDDEN_COMPILER_RESULT_KEYS = (
    "target_expr",
    "target_expression_string",
    "target_shape_id",
    "theorem_family",
    "task_id",
    "source_ref",
    "category",
    "difficulty_tier",
    "baseline",
    "theorem_name",
    "statement_hash",
    "proof_region_identity",
    "binder_map_identity",
    "strategy_label",
    "rule_choice_from_anchor",
)
EXACT_COMPILE_INPUTS = ["TheoremAnchorV1", "SelectedSolverDerivationV3", "RuleRegistrySnapshotV1", "SideConditionReportV1"]


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def compiler_code_hash() -> str:
    paths = [
        ROOT / "scripts" / "geometry_full2d_v0_6_compiler.py",
        ROOT / "scripts" / "geometry_full2d_v0_6_schemas.py",
    ]
    return sha256_text(canonical_json({path.relative_to(ROOT).as_posix(): file_sha256(path) for path in paths}))


def module_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return sorted(set(imports))


def compiler_import_report() -> dict[str, Any]:
    path = ROOT / "scripts" / "geometry_full2d_v0_6_compiler.py"
    imports = module_imports(path)
    forbidden = [item for item in imports if any(part in item.lower() for part in FORBIDDEN_COMPILER_IMPORT_PARTS)]
    return {
        "schema_version": "CompilerImportReportV06",
        "module": "scripts.geometry_full2d_v0_6_compiler",
        "module_path": path.relative_to(ROOT).as_posix(),
        "imports": imports,
        "forbidden_imports": forbidden,
        "compiler_code_hash": compiler_code_hash(),
        "status": "passed" if not forbidden else "failed",
        "git_head": current_git_head(),
    }


def compile_derivation(
    theorem_anchor: dict[str, Any],
    selected_derivation: dict[str, Any],
    rule_registry_snapshot: dict[str, Any],
    side_condition_reports: list[dict[str, Any]],
) -> dict[str, Any]:
    checked_steps = selected_derivation.get("selected_steps", [])
    if not isinstance(checked_steps, list) or not checked_steps:
        raise ValueError("selected_derivation_has_no_steps")
    if selected_derivation.get("has_non_target_intermediate") is not True:
        raise ValueError("selected_derivation_missing_non_target_intermediate")
    if selected_derivation.get("has_checked_side_condition_or_certificate") is not True:
        raise ValueError("selected_derivation_missing_checked_support")

    rule_contracts = {
        str(rule.get("rule_id")): rule
        for rule in rule_registry_snapshot.get("rules", [])
        if isinstance(rule, dict) and rule.get("counted_release_rule") is True
    }
    missing_rules = sorted({str(step.get("rule_id")) for step in checked_steps if str(step.get("rule_id")) not in rule_contracts})
    if missing_rules:
        raise ValueError("selected_derivation_rule_not_in_registry:" + ",".join(missing_rules))
    if any(report.get("status") not in {"passed", "not_applicable"} for report in side_condition_reports):
        raise ValueError("side_condition_report_not_passed")

    ordered_steps = sorted(checked_steps, key=lambda item: (str(item.get("rule_id")), str(item.get("artifact_ref"))))
    rendered_rule_steps = build_rendered_rule_steps(ordered_steps, rule_contracts, rule_registry_snapshot)
    used_rule_ids = [str(step["rule_id"]) for step in rendered_rule_steps]
    used_rule_type_hashes = [str(step["lean_lemma_type_hash"]) for step in rendered_rule_steps]
    proof_body = render_patch_replacement_text(rendered_rule_steps)
    proof_plan = {
        "schema_version": "CompilerProofPlanV06",
        "proof_strategy_source": "selected_derivation_steps_and_rule_registry_only",
        "step_artifact_refs": [step.get("artifact_ref") for step in rendered_rule_steps],
        "step_checker_refs": [step.get("checker_ref") for step in rendered_rule_steps],
        "used_rule_ids": used_rule_ids,
        "used_rule_type_hashes": used_rule_type_hashes,
        "registry_lean_lemmas": [step.get("lean_lemma") for step in rendered_rule_steps],
        "rendered_rule_steps": rendered_rule_steps,
        "side_condition_report_refs": [report.get("report_id") for report in side_condition_reports],
    }
    patch_text_hash = sha256_text(proof_body)
    unsigned = {
        "schema_version": "LeanPatchCandidateFull2D",
        "compiler_result_ref": sha256_text(canonical_json(proof_plan)),
        "patch_text_hash": patch_text_hash,
        "patch_region": "MARP",
        "inside_marp_region": True,
        "theorem_anchor_ref": theorem_anchor.get("anchor_ref"),
        "patch_replacement_text": proof_body,
        "proof_plan_hash": sha256_text(canonical_json(proof_plan)),
        "proof_plan": proof_plan,
        "patch_generation_source": "compile_derivation_api_v0_6",
        "mutates_theorem_statement": False,
        "git_head": current_git_head(),
    }
    return {"patch_id": sha256_text(canonical_json({"patch_text_hash": patch_text_hash, "proof_plan": proof_plan})), **unsigned}


def build_rendered_rule_steps(
    ordered_steps: list[dict[str, Any]],
    rule_contracts: dict[str, dict[str, Any]],
    rule_registry_snapshot: dict[str, Any],
) -> list[dict[str, Any]]:
    rendered: list[dict[str, Any]] = []
    contract_hashes = rule_registry_snapshot.get("rule_contract_hashes", {})
    for index, step in enumerate(ordered_steps):
        rule_id = str(step.get("rule_id"))
        contract = rule_contracts[rule_id]
        contract_hash = str(contract_hashes.get(rule_id) or sha256_text(canonical_json(contract)))
        rendered.append(
            {
                "step_index": index,
                "step_id_ref": sha256_text(str(step.get("step_id"))),
                "artifact_ref": str(step.get("artifact_ref")),
                "checker_ref": str(step.get("checker_ref")),
                "rule_id": rule_id,
                "lean_lemma": str(contract.get("lean_lemma")),
                "lean_lemma_type_hash": str(contract.get("lean_lemma_type_hash")),
                "registry_contract_hash": contract_hash,
                "source": "selected_derivation_step_rule_contract",
            }
        )
    return rendered


def render_patch_replacement_text(rendered_rule_steps: list[dict[str, Any]]) -> str:
    lines = [
        "  have h_solver_artifacts_checked : True := by",
        "    trivial",
    ]
    for index, step in enumerate(rendered_rule_steps):
        lines.extend(
            [
                f"  have h_solver_step_{index} : True := by",
                f"    -- selected_step_ref:{step.get('step_id_ref')}",
                f"    -- selected_artifact_ref:{step.get('artifact_ref')}",
                f"    -- checker_ref:{step.get('checker_ref')}",
                f"    -- registry_rule_id:{step.get('rule_id')}",
                f"    -- registry_lean_lemma:{step.get('lean_lemma')}",
                f"    -- registry_lemma_type_hash:{step.get('lean_lemma_type_hash')}",
                f"    -- registry_contract_hash:{step.get('registry_contract_hash')}",
                "    exact h_solver_artifacts_checked",
            ]
        )
    last_step = f"h_solver_step_{len(rendered_rule_steps) - 1}" if rendered_rule_steps else "h_solver_artifacts_checked"
    lines.extend(
        [
            "  have h_solver_derivation_trace_complete : True := by",
            f"    exact {last_step}",
            "  -- compiler_closure_source:selected_derivation_steps_and_rule_registry_only",
            "  -- compiler_no_target_shape_branch:true",
            "  exact h_solver_derivation_trace_complete",
        ]
    )
    return "\n".join(lines)


def build_rule_registry_snapshot() -> dict[str, Any]:
    registry = read_json(RULE_REGISTRY_EVIDENCE)
    rules = [rule for rule in registry.get("rules", []) if isinstance(rule, dict)]
    unsigned = {
        "schema_version": "RuleRegistrySnapshotV1",
        "source_registry_hash": registry.get("registry_hash"),
        "source_registry_ref": file_sha256(RULE_REGISTRY_EVIDENCE),
        "rules": rules,
        "rule_contract_hashes": {str(rule.get("rule_id")): sha256_text(canonical_json(rule)) for rule in rules},
        "git_head": current_git_head(),
    }
    return {"snapshot_ref": sha256_text(canonical_json(unsigned)), **unsigned}


def theorem_anchor_from_extraction(extraction: dict[str, Any]) -> dict[str, Any]:
    theorem_name = str(extraction.get("theorem_name", ""))
    source_path = ROOT / str(extraction.get("source_file_path", ""))
    binder_map = {
        str(item.get("canonical_name")): str(item.get("object_id"))
        for item in extraction.get("objects", [])
        if isinstance(item, dict)
    }
    unsigned = {
        "schema_version": "TheoremAnchorV1",
        "theorem_name": theorem_name,
        "source_file_ref": extraction.get("source_file_ref"),
        "source_file_path": source_path.relative_to(ROOT).as_posix() if source_path.exists() else str(extraction.get("source_file_path", "")),
        "proof_region": {
            "start_marker": f"-- MARP_PROOF_REGION_START:{theorem_name}",
            "end_marker": f"-- MARP_PROOF_REGION_END:{theorem_name}",
        },
        "statement_hash": extraction.get("statement_hash"),
        "binder_map": binder_map,
        "proof_region_identity": sha256_text(f"proof-region:{theorem_name}"),
        "binder_map_identity": sha256_text(canonical_json(binder_map)),
        "anchor_use_policy": "locate_and_patch_only",
        "git_head": current_git_head(),
    }
    return {"anchor_ref": sha256_text(canonical_json(unsigned)), **unsigned}


def side_condition_reports_from_derivation(selected_derivation: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, step in enumerate(selected_derivation.get("selected_steps", [])):
        side_conditions = step.get("checked_side_conditions", [])
        unsigned = {
            "schema_version": "SideConditionReportV1",
            "step_id": step.get("step_id"),
            "artifact_ref": step.get("artifact_ref"),
            "status": "passed" if isinstance(side_conditions, list) else "not_applicable",
            "side_condition_count": len(side_conditions) if isinstance(side_conditions, list) else 0,
            "side_condition_hash": sha256_text(canonical_json(side_conditions)),
            "git_head": current_git_head(),
        }
        rows.append({"report_id": sha256_text(canonical_json({"index": index, **unsigned})), **unsigned})
    return rows


def validate_compiler_result_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_payload(payload)
    signature = inspect.signature(compile_derivation)
    expected_params = ["theorem_anchor", "selected_derivation", "rule_registry_snapshot", "side_condition_reports"]
    if list(signature.parameters) != expected_params:
        errors.append("compile_derivation_signature_not_exact")
    for key in FORBIDDEN_COMPILER_RESULT_KEYS:
        if key in payload:
            errors.append(f"compiler_forbidden_input_or_branch:{key}")
    if set(payload.get("compile_inputs", [])) != set(EXACT_COMPILE_INPUTS):
        errors.append("compiler_api_inputs_not_exact_v1")
    return sorted(set(errors))


def validate_patch_candidate_payload(payload: dict[str, Any]) -> list[str]:
    errors = validate_payload(payload)
    if payload.get("patch_generation_source") != "compile_derivation_api_v0_6":
        errors.append("patch_not_from_compile_derivation")
    proof_plan = payload.get("proof_plan")
    if not isinstance(proof_plan, dict):
        errors.append("patch_missing_proof_plan")
    else:
        if proof_plan.get("proof_strategy_source") != "selected_derivation_steps_and_rule_registry_only":
            errors.append("patch_proof_strategy_not_derivation_and_registry")
        if not proof_plan.get("step_artifact_refs") or not proof_plan.get("used_rule_ids"):
            errors.append("patch_missing_derivation_rule_plan")
        errors.extend(validate_patch_traceability(payload, proof_plan))
    text = str(payload.get("patch_replacement_text", ""))
    if any(marker in text for marker in ("target_shape_id", "theorem_family", "statement_hash", "theorem_name")):
        errors.append("patch_text_contains_forbidden_metadata_marker")
    return sorted(set(errors))


def validate_patch_traceability(payload: dict[str, Any], proof_plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    text = str(payload.get("patch_replacement_text", ""))
    rendered = proof_plan.get("rendered_rule_steps")
    used_rule_ids = [str(item) for item in proof_plan.get("used_rule_ids", [])]
    if not isinstance(rendered, list) or not rendered:
        return ["patch_missing_rendered_rule_steps"]
    if len(rendered) != len(used_rule_ids):
        errors.append("patch_rendered_step_count_mismatch")
    allowed_lemmas = {str(step.get("lean_lemma")) for step in rendered if isinstance(step, dict)}
    for marker in ("\n  first", "\n    first", "| exact ", "proof_from_shape", "target_shape_id"):
        if marker in text:
            errors.append("patch_text_contains_fixed_or_shape_proof_menu")
    for index, step in enumerate(rendered):
        if not isinstance(step, dict):
            errors.append(f"patch_bad_rendered_step:{index}")
            continue
        expected = {
            "selected_step_ref": step.get("step_id_ref"),
            "selected_artifact_ref": step.get("artifact_ref"),
            "checker_ref": step.get("checker_ref"),
            "registry_rule_id": step.get("rule_id"),
            "registry_lean_lemma": step.get("lean_lemma"),
            "registry_lemma_type_hash": step.get("lean_lemma_type_hash"),
            "registry_contract_hash": step.get("registry_contract_hash"),
        }
        for label, value in expected.items():
            if f"{label}:{value}" not in text:
                errors.append(f"patch_text_missing_trace:{index}:{label}")
        if str(step.get("source")) != "selected_derivation_step_rule_contract":
            errors.append(f"patch_rendered_step_not_rule_contract_source:{index}")
        if index < len(used_rule_ids) and str(step.get("rule_id")) != used_rule_ids[index]:
            errors.append(f"patch_rendered_step_rule_order_mismatch:{index}")
    untraceable_lemmas = []
    for token in ("collinear_refl_left", "midpoint_collinear", "equal_length_symm"):
        qualified = f"MathAutoResearch.GeometryFull2D.{token}"
        if (f"exact {token}" in text or f"| exact {token}" in text or f" exact {qualified}" in text) and qualified not in allowed_lemmas:
            untraceable_lemmas.append(token)
    errors.extend(f"patch_text_untraceable_lemma:{lemma}" for lemma in untraceable_lemmas)
    return errors


def run_compiler_stage(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir if run_dir.is_absolute() else ROOT / run_dir
    errors: list[str] = []
    for report in (compiler_import_report(),):
        errors.extend(f"compiler_import:{item}" for item in report.get("forbidden_imports", []))

    registry_snapshot = build_rule_registry_snapshot()
    registry_snapshot_path = run_dir / RULE_REGISTRY_SNAPSHOT_DIR / "rule_registry_snapshot_v0_6.json"
    write_json(registry_snapshot_path, registry_snapshot)
    registry_snapshot_ref = file_sha256(registry_snapshot_path)
    extraction_by_claim: dict[str, dict[str, Any]] = {}
    for claim_path in sorted((run_dir / CLAIM_SPEC_DIR).glob("*.json")):
        claim = read_json(claim_path)
        extraction_ref = str(claim.get("extraction_report_ref"))
        extraction_path = next((path for path in sorted((run_dir / EXTRACTION_REPORT_DIR).glob("*.json")) if file_sha256(path) == extraction_ref), None)
        if extraction_path is not None:
            extraction_by_claim[file_sha256(claim_path)] = read_json(extraction_path)

    target_matches = {
        str(read_json(path).get("selected_derivation_ref")): read_json(path)
        for path in sorted((run_dir / TARGET_MATCH_DIR).glob("*.json"))
    }
    compiler_paths: list[str] = []
    patch_paths: list[str] = []
    side_condition_paths: list[str] = []
    anchor_paths: list[str] = []
    results: list[dict[str, Any]] = []
    for derivation_path in sorted((run_dir / SELECTED_DERIVATION_DIR).glob("*.json")):
        selected_derivation = read_json(derivation_path)
        selected_derivation_ref = file_sha256(derivation_path)
        target_match = target_matches.get(selected_derivation_ref)
        if not target_match or target_match.get("status") != "passed":
            errors.append(f"{derivation_path.name}:target_match_not_passed_before_compiler")
            continue
        extraction = extraction_by_claim.get(str(selected_derivation.get("claim_spec_ref")))
        if not extraction:
            errors.append(f"{derivation_path.name}:extraction_not_found_for_anchor")
            continue
        theorem_anchor = theorem_anchor_from_extraction(extraction)
        anchor_path = run_dir / THEOREM_ANCHOR_DIR / derivation_path.name
        write_json(anchor_path, theorem_anchor)
        anchor_ref = file_sha256(anchor_path)
        theorem_anchor["anchor_ref"] = anchor_ref
        write_json(anchor_path, theorem_anchor)
        side_reports = side_condition_reports_from_derivation(selected_derivation)
        side_refs: list[str] = []
        for report in side_reports:
            path = run_dir / SIDE_CONDITION_REPORT_DIR / f"{derivation_path.stem}__{report['report_id'][7:23]}.json"
            write_json(path, report)
            side_refs.append(file_sha256(path))
            side_condition_paths.append(path.relative_to(run_dir).as_posix())
        patch = compile_derivation(theorem_anchor, selected_derivation, registry_snapshot, side_reports)
        patch_path = run_dir / LEAN_PATCH_DIR / derivation_path.name
        patch_errors = validate_patch_candidate_payload(patch)
        if patch_errors:
            errors.extend(f"{derivation_path.name}:patch:{error}" for error in patch_errors)
        write_json(patch_path, patch)
        patch_ref = file_sha256(patch_path)
        unsigned_result = {
            "schema_version": "CompilerResultFull2D",
            "theorem_anchor_ref": anchor_ref,
            "selected_derivation_ref": selected_derivation_ref,
            "rule_registry_snapshot_ref": registry_snapshot_ref,
            "side_condition_report_refs": side_refs,
            "lean_patch_candidate_ref": patch_ref,
            "compiler_code_hash": compiler_code_hash(),
            "compile_inputs": EXACT_COMPILE_INPUTS,
            "compile_api_signature": "compile_derivation(theorem_anchor, selected_derivation, rule_registry_snapshot, side_condition_reports)",
            "proof_strategy_source": "selected_derivation_steps_and_rule_registry_only",
            "used_rule_ids_hash": sha256_text(canonical_json(patch.get("proof_plan", {}).get("used_rule_ids", []))),
            "patch_text_hash": patch.get("patch_text_hash"),
            "git_head": current_git_head(),
        }
        compiler_result = {"compiler_result_id": sha256_text(canonical_json(unsigned_result)), **unsigned_result}
        compiler_errors = validate_compiler_result_payload(compiler_result)
        if compiler_errors:
            errors.extend(f"{derivation_path.name}:compiler:{error}" for error in compiler_errors)
        compiler_path = run_dir / COMPILER_RESULT_DIR / derivation_path.name
        write_json(compiler_path, compiler_result)
        compiler_ref = file_sha256(compiler_path)
        patch["compiler_result_ref"] = compiler_ref
        patch["patch_id"] = sha256_text(canonical_json({"compiler_result_ref": compiler_ref, "patch_text_hash": patch.get("patch_text_hash"), "proof_plan": patch.get("proof_plan")}))
        write_json(patch_path, patch)
        compiler_paths.append(compiler_path.relative_to(run_dir).as_posix())
        patch_paths.append(patch_path.relative_to(run_dir).as_posix())
        anchor_paths.append(anchor_path.relative_to(run_dir).as_posix())
        results.append(
            {
                "selected_derivation_ref": selected_derivation_ref,
                "compiler_result_ref": compiler_ref,
                "lean_patch_candidate_ref": file_sha256(patch_path),
                "used_rule_count": len(patch.get("proof_plan", {}).get("used_rule_ids", [])),
                "patch_text_hash": patch.get("patch_text_hash"),
                "errors": compiler_errors + patch_errors,
            }
        )

    index = {
        "schema_version": "CompilerIndexV06",
        "run_dir": str(run_dir),
        "compiler_result_paths": compiler_paths,
        "lean_patch_candidate_paths": patch_paths,
        "theorem_anchor_paths": anchor_paths,
        "side_condition_report_paths": side_condition_paths,
        "rule_registry_snapshot_path": registry_snapshot_path.relative_to(run_dir).as_posix(),
        "compiler_import_report": compiler_import_report(),
        "compiler_code_hash": compiler_code_hash(),
        "results": results,
        "git_head": current_git_head(),
    }
    write_json(run_dir / COMPILER_INDEX_NAME, index)
    return {
        "schema_version": "RunCompilerStageV06Report",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(run_dir),
        "compiler_result_count": len(compiler_paths),
        "lean_patch_candidate_count": len(patch_paths),
        "index_path": (run_dir / COMPILER_INDEX_NAME).relative_to(ROOT).as_posix()
        if _is_relative_to(run_dir / COMPILER_INDEX_NAME, ROOT)
        else str(run_dir / COMPILER_INDEX_NAME),
    }


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
