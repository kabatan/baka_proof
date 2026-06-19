from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from plugins.geometry_full2d.engine_contracts import canonical_json


ROOT = Path(__file__).resolve().parents[2]
SHA_PREFIX = "sha256:"
ALLOWED_LEAN_TEMPLATES = {
    "lean_template:assumption_support",
    "lean_template:checked_certificate",
    "lean_template:collinear_refl_left",
    "lean_template:collinear_refl_right",
    "lean_template:between_collinear",
    "lean_template:midpoint_collinear",
    "lean_template:equal_length_refl",
    "lean_template:equal_length_symm",
    "lean_template:length_le_refl",
    "lean_template:length_le_trans",
    "lean_template:directed_angle_eq_refl",
    "lean_template:directed_angle_eq_symm",
    "lean_template:directed_angle_eq_mod_2pi_refl",
    "lean_template:directed_angle_eq_mod_2pi_symm",
    "lean_template:area_eq_refl",
    "lean_template:area_eq_symm",
    "lean_template:ratio_eq_refl",
    "lean_template:ratio_eq_symm",
    "lean_template:reflection_has_evidence",
    "lean_template:homothety_has_evidence",
    "lean_template:inversion_has_evidence",
    "lean_template:spiral_similarity_has_evidence",
    "lean_template:chord_is_symmetric",
    "lean_template:equilateral_is_isosceles_left",
    "lean_template:circle_construction_on_circle",
    "lean_template:line_circle_intersection_on_line",
    "lean_template:constructed_center_identity",
    "lean_template:rotation_preserves_collinear_of_eq",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-spec-json", required=True)
    parser.add_argument("--selected-derivation-json", required=True)
    parser.add_argument("--rule-registry-json", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--claim-spec-ref")
    parser.add_argument("--selected-derivation-ref")
    parser.add_argument("--rule-registry-ref")
    parser.add_argument("--side-condition-checker-ref", action="append", default=[])
    args = parser.parse_args()
    report = run_compiler_cli(
        claim_spec_json=Path(args.claim_spec_json),
        selected_derivation_json=Path(args.selected_derivation_json),
        rule_registry_json=Path(args.rule_registry_json),
        output_dir=Path(args.output_dir),
        claim_spec_ref=args.claim_spec_ref,
        selected_derivation_ref=args.selected_derivation_ref,
        rule_registry_ref=args.rule_registry_ref,
        side_condition_checker_refs=tuple(args.side_condition_checker_ref),
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


def run_compiler_cli(
    *,
    claim_spec_json: Path,
    selected_derivation_json: Path,
    rule_registry_json: Path,
    output_dir: Path,
    claim_spec_ref: str | None = None,
    selected_derivation_ref: str | None = None,
    rule_registry_ref: str | None = None,
    side_condition_checker_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    claim_path = resolve_path(claim_spec_json)
    selected_path = resolve_path(selected_derivation_json)
    registry_path = resolve_path(rule_registry_json)
    output_root = resolve_path(output_dir)
    claim_spec = read_json(claim_path)
    selected = read_json(selected_path)
    registry = read_json(registry_path)
    refs = {
        "claim_spec_ref": claim_spec_ref or sha256_file(claim_path),
        "selected_solver_derivation_ref": selected_derivation_ref or sha256_file(selected_path),
        "rule_registry_ref": rule_registry_ref or sha256_file(registry_path),
    }
    report = compile_selected_derivation(
        claim_spec=claim_spec,
        selected_derivation=selected,
        rule_registry=registry,
        side_condition_checker_refs=side_condition_checker_refs,
        **refs,
    )
    stage_dir = output_root / "compiler_stage"
    artifact_paths: dict[str, str] = {}
    if report["status"] == "passed":
        result_ref, result_path = write_content_json(stage_dir / "compiler_result.json", report["compiler_result"], id_field="result_id")
        artifact_paths[result_ref] = result_path.relative_to(output_root).as_posix()
        report["compiler_result_ref"] = result_ref
    summary = {
        "schema_version": "GeometryFull2DCompilerCLIRunV05",
        "status": report["status"],
        "errors": report["errors"],
        "claim_spec_ref": refs["claim_spec_ref"],
        "selected_solver_derivation_ref": refs["selected_solver_derivation_ref"],
        "rule_registry_ref": refs["rule_registry_ref"],
        "side_condition_checker_refs": list(side_condition_checker_refs),
        "compiler_result_ref": report.get("compiler_result_ref"),
        "artifact_paths": artifact_paths,
        "output_dir": str(output_root),
    }
    write_json(stage_dir / "compiler_cli_summary.json", summary)
    return summary


def compile_selected_derivation(
    *,
    claim_spec: dict[str, Any],
    claim_spec_ref: str,
    selected_derivation: dict[str, Any],
    selected_solver_derivation_ref: str,
    rule_registry: dict[str, Any],
    rule_registry_ref: str,
    side_condition_checker_refs: tuple[str, ...],
) -> dict[str, Any]:
    errors = validate_compile_inputs(claim_spec, selected_derivation, rule_registry, side_condition_checker_refs)
    if errors:
        return {"status": "failed", "errors": sorted(set(errors))}
    rules_by_id = {
        str(rule["rule_id"]): rule
        for rule in rule_registry.get("rules", [])
        if isinstance(rule, dict) and rule.get("counted") is True
    }
    steps = [step for step in selected_derivation.get("derivation_steps", []) if isinstance(step, dict)]
    consumed_rule_ids = tuple(dict.fromkeys(str(step.get("rule_id")) for step in steps))
    generated_obligations = tuple(
        obligation
        for rule_id in consumed_rule_ids
        for obligation in rules_by_id[rule_id].get("generated_obligations", [])
    )
    rule_templates_by_id = {rule_id: str(rule.get("lean_template_id", "")) for rule_id, rule in rules_by_id.items()}
    try:
        proof_text = build_solver_citing_proof_text(selected_derivation, consumed_rule_ids, generated_obligations, rule_templates_by_id)
    except (KeyError, ValueError) as exc:
        return {"status": "failed", "errors": [f"proof_template_binding_error:{exc}"]}
    unsigned = {
        "schema_version": "CompilerResultFull2D",
        "claim_spec_ref": claim_spec_ref,
        "selected_solver_derivation_ref": selected_solver_derivation_ref,
        "rule_registry_ref": rule_registry_ref,
        "side_condition_checker_refs": list(side_condition_checker_refs),
        "proof_text": proof_text,
        "consumed_rule_ids": list(consumed_rule_ids),
        "used_rule_ids": list(consumed_rule_ids),
        "used_rule_refs": list(consumed_rule_ids),
        "generated_obligations": list(dict.fromkeys(generated_obligations)),
        "solver_fact_refs": list(selected_derivation.get("selected_facts", [])),
        "solver_construction_refs": list(selected_derivation.get("selected_constructions", [])),
        "solver_certificate_refs": list(selected_derivation.get("selected_certificates", [])),
        "derivation_step_refs": [str(step.get("step_id")) for step in steps],
        "independent_checker_report_refs": [str(step.get("independent_checker_report_ref")) for step in steps],
        "target_expr_branch_used": False,
        "forbidden_metadata_used": False,
        "compiler_selected_rule_list_without_derivation": False,
        "input_contract": "claimspec_ref_selected_derivation_ref_rule_registry_ref_side_condition_checker_refs_only",
        "proof_use_status": "compiler_output_only",
        "status": "compiled_patch",
    }
    return {"status": "passed", "errors": [], "compiler_result": unsigned}


def validate_compile_inputs(
    claim_spec: dict[str, Any],
    selected_derivation: dict[str, Any],
    rule_registry: dict[str, Any],
    side_condition_checker_refs: tuple[str, ...],
) -> list[str]:
    errors: list[str] = []
    rules = rule_registry.get("rules")
    if not isinstance(rules, list):
        return ["rule_registry_rules_not_list"]
    counted_rules = {
        str(rule.get("rule_id")): rule
        for rule in rules
        if isinstance(rule, dict) and rule.get("counted") is True
    }
    steps = selected_derivation.get("derivation_steps")
    if not isinstance(steps, list) or not steps:
        return ["selected_derivation_missing_steps"]
    selected_engine_refs = {str(ref) for ref in selected_derivation.get("selected_engine_output_refs", [])}
    if not selected_engine_refs:
        errors.append("selected_derivation_missing_selected_engine_outputs")
    elif any(not ref.startswith(SHA_PREFIX) for ref in selected_engine_refs):
        errors.append("selected_engine_output_ref_not_sha256")
    has_non_target = bool(selected_derivation.get("selected_constructions") or selected_derivation.get("selected_certificates"))
    target_steps = 0
    non_target_outputs: set[str] = set()
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"bad_derivation_step:{index}")
            continue
        rule_id = str(step.get("rule_id", ""))
        rule = counted_rules.get(rule_id)
        if rule is None:
            errors.append(f"unknown_or_noncounted_rule:{index}:{rule_id}")
        elif rule.get("direct_identity_rule") is True or rule.get("direct_facade_rule") is True:
            errors.append(f"identity_or_facade_rule_selected:{index}:{rule_id}")
        checker_ref = str(step.get("independent_checker_report_ref", ""))
        if not checker_ref.startswith(SHA_PREFIX):
            errors.append(f"bad_checker_ref:{index}")
        supporting_engine = str(step.get("supporting_engine_output_ref", ""))
        if not supporting_engine.startswith(SHA_PREFIX):
            errors.append(f"bad_supporting_engine_ref:{index}")
        elif supporting_engine not in selected_engine_refs:
            errors.append(f"supporting_engine_not_selected:{index}")
        supporting_artifact = str(step.get("supporting_artifact_ref", ""))
        if not supporting_artifact.startswith(SHA_PREFIX):
            errors.append(f"bad_supporting_artifact_ref:{index}")
        if not isinstance(step.get("proof_bindings"), dict):
            errors.append(f"missing_proof_bindings:{index}")
        if "lean_template_id" in step:
            errors.append(f"selected_derivation_supplies_lean_template_id:{index}")
        elif rule is not None:
            lean_template_id = str(rule.get("lean_template_id", ""))
            if not lean_template_id.startswith("lean_template:"):
                errors.append(f"rule_registry_template_not_executable:{index}:{rule_id}")
            elif lean_template_id not in ALLOWED_LEAN_TEMPLATES:
                errors.append(f"unsupported_rule_registry_template:{index}:{rule_id}:{lean_template_id}")
        if step.get("output_is_target") is True:
            target_steps += 1
            if step.get("proof_selection_source") != "engine_artifact_derivation_operator":
                errors.append(f"target_step_proof_selection_not_engine_artifact_operator:{index}")
            if not str(step.get("derivation_operator", "")).strip():
                errors.append(f"target_step_missing_derivation_operator:{index}")
            if not step.get("input_refs"):
                errors.append(f"target_step_missing_inputs:{index}")
            if str(step.get("output_expr", "")).strip() != target_source_expr(claim_spec).strip():
                errors.append(f"target_step_output_expr_mismatch:{index}")
            target_inputs = {str(ref) for ref in step.get("input_refs", [])}
            if not (target_inputs & non_target_outputs or target_inputs & set(map(str, selected_derivation.get("selected_constructions", []))) or target_inputs & set(map(str, selected_derivation.get("selected_certificates", [])))):
                errors.append(f"target_step_not_supported_by_selected_non_target_artifact:{index}")
        else:
            has_non_target = True
            non_target_outputs.add(str(step.get("output_ref", "")))
            if not str(step.get("output_expr", "")):
                errors.append(f"non_target_step_missing_output_expr:{index}")
        if step.get("non_target_intermediate") is True:
            has_non_target = True
    if target_steps != 1:
        errors.append("selected_derivation_target_step_count_not_one")
    if not has_non_target:
        errors.append("naked_target_assertion")
    for index, ref in enumerate(side_condition_checker_refs):
        if not str(ref).startswith(SHA_PREFIX):
            errors.append(f"bad_side_condition_checker_ref:{index}")
    return errors


def build_solver_citing_proof_text(
    selected_derivation: dict[str, Any],
    consumed_rule_ids: tuple[str, ...],
    generated_obligations: tuple[str, ...],
    rule_templates_by_id: dict[str, str],
) -> str:
    facts = ", ".join(map(str, selected_derivation.get("selected_facts", []))) or "none"
    constructions = ", ".join(map(str, selected_derivation.get("selected_constructions", []))) or "none"
    certificates = ", ".join(map(str, selected_derivation.get("selected_certificates", []))) or "none"
    obligations = ", ".join(dict.fromkeys(map(str, generated_obligations))) or "none"
    steps = [step for step in selected_derivation.get("derivation_steps", []) if isinstance(step, dict)]
    step_lines = [
        f"  -- solver step {step.get('step_id')} uses {step.get('rule_id')} from {list(step.get('input_refs', []))} to {step.get('output_ref')}"
        for step in steps
    ]
    citation_lines = [
        f"-- solver-derived facts: {facts}",
        f"-- solver-derived constructions: {constructions}",
        f"-- solver-derived certificates: {certificates}",
        f"-- generated obligations: {obligations}",
        f"-- consumed RuleRegistry contracts: {', '.join(consumed_rule_ids)}",
        *(line[2:] if line.startswith("  ") else line for line in step_lines),
    ]
    proof_lines = list(citation_lines)
    proof_names: dict[str, str] = {}
    for step in steps:
        step_id = str(step.get("step_id"))
        proof_var = proof_name(step_id)
        proof_names[str(step.get("output_ref"))] = proof_var
        output_expr = str(step.get("output_expr", "")).strip() or "True"
        proof_lines.append(f"have {proof_var} : {output_expr} := by")
        proof_lines.extend("  " + line for line in build_step_exact(step, rule_templates_by_id).splitlines())
    target_steps = [step for step in steps if step.get("output_is_target") is True]
    target_var = proof_name(str(target_steps[-1].get("step_id"))) if target_steps else ""
    proof_lines.append(f"exact {target_var}" if target_var else "exact by trivial")
    return "\n".join(proof_lines)


def build_step_exact(step: dict[str, Any], rule_templates_by_id: dict[str, str]) -> str:
    rule_id = str(step.get("rule_id", ""))
    template = str(rule_templates_by_id.get(rule_id, ""))
    bindings = step.get("proof_bindings", {})
    if not isinstance(bindings, dict):
        bindings = {}
    try:
        if template == "lean_template:assumption_support":
            return f"exact {bindings['h']}"
        if template == "lean_template:checked_certificate":
            return "trivial"
        if template == "lean_template:collinear_refl_left":
            return f"exact collinear_refl_left {bindings['A']} {bindings['B']}"
        if template == "lean_template:collinear_refl_right":
            return f"exact collinear_refl_right {bindings['A']} {bindings['B']}"
        if template == "lean_template:between_collinear":
            return f"exact between_collinear {bindings['A']} {bindings['B']} {bindings['C']} {bindings['h']}"
        if template == "lean_template:midpoint_collinear":
            return f"exact midpoint_collinear {bindings['A']} {bindings['M']} {bindings['B']} {bindings['h']}"
        if template == "lean_template:equal_length_refl":
            return f"exact equal_length_refl {bindings['A']} {bindings['B']}"
        if template == "lean_template:equal_length_symm":
            return f"exact equal_length_symm {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['h']}"
        if template == "lean_template:length_le_refl":
            return f"exact length_le_refl {bindings['A']} {bindings['B']}"
        if template == "lean_template:length_le_trans":
            return f"exact length_le_trans {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} {bindings['h0']} {bindings['h1']}"
        if template == "lean_template:directed_angle_eq_refl":
            return f"exact directed_angle_eq_refl {bindings['A']} {bindings['B']} {bindings['C']}"
        if template == "lean_template:directed_angle_eq_symm":
            return f"exact directed_angle_eq_symm {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} {bindings['h']}"
        if template == "lean_template:directed_angle_eq_mod_2pi_refl":
            return f"exact directed_angle_eq_mod_2pi_refl {bindings['A']} {bindings['B']} {bindings['C']}"
        if template == "lean_template:directed_angle_eq_mod_2pi_symm":
            return f"exact directed_angle_eq_mod_2pi_symm {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} {bindings['h']}"
        if template == "lean_template:area_eq_refl":
            return f"exact area_eq_refl {bindings['A']} {bindings['B']} {bindings['C']}"
        if template == "lean_template:area_eq_symm":
            return f"exact area_eq_symm {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} {bindings['h']}"
        if template == "lean_template:ratio_eq_refl":
            return f"exact ratio_eq_refl {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']}"
        if template == "lean_template:ratio_eq_symm":
            return f"exact ratio_eq_symm {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} {bindings['G']} {bindings['H']} {bindings['h']}"
        if template == "lean_template:reflection_has_evidence":
            return f"exact reflection_has_evidence {bindings['r']}"
        if template == "lean_template:homothety_has_evidence":
            return f"exact homothety_has_evidence {bindings['h']}"
        if template == "lean_template:inversion_has_evidence":
            return f"exact inversion_has_evidence {bindings['i']}"
        if template == "lean_template:spiral_similarity_has_evidence":
            return f"exact spiral_similarity_has_evidence {bindings['s']}"
        if template == "lean_template:chord_is_symmetric":
            return f"exact chord_is_symmetric {bindings['A']} {bindings['B']} {bindings['c']} {bindings['h']}"
        if template == "lean_template:equilateral_is_isosceles_left":
            return f"exact equilateral_is_isosceles_left {bindings['A']} {bindings['B']} {bindings['C']} {bindings['h']}"
        if template == "lean_template:circle_construction_on_circle":
            return f"exact circle_construction_on_circle {bindings['O']} {bindings['P']} {bindings['c']} {bindings['h']}"
        if template == "lean_template:line_circle_intersection_on_line":
            return f"exact line_circle_intersection_on_line {bindings['P']} {bindings['l']} {bindings['c']} {bindings['h']}"
        if template == "lean_template:constructed_center_identity":
            return f"exact constructed_center_identity {bindings['O']} {bindings['c']} {bindings['h']}"
        if template == "lean_template:rotation_preserves_collinear_of_eq":
            return f"exact rotation_preserves_collinear_of_eq {bindings['A']} {bindings['B']} {bindings['C']} {bindings['D']} {bindings['E']} {bindings['F']} rfl rfl rfl"
    except KeyError as exc:
        raise ValueError(f"missing_binding:{str(exc).strip(chr(39))}") from exc
    raise ValueError(f"unsupported_solver_template:{template}")


def proof_name(step_id: str) -> str:
    return "h_solver_" + "".join(char if char.isalnum() else "_" for char in step_id)


def target_source_expr(claim_spec: dict[str, Any]) -> str:
    target = claim_spec.get("target", {})
    return str(target.get("source_expr", "")) if isinstance(target, dict) else ""


def write_content_json(path: Path, payload_without_id: dict[str, Any], *, id_field: str) -> tuple[str, Path]:
    ref = sha256_text(canonical_json(payload_without_id))
    payload = {id_field: ref, "content_sha256": ref, **payload_without_id}
    write_json(path, payload)
    return ref, path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
