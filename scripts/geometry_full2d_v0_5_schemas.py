from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHA_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
BASELINES = {"B1", "B2", "B5", "B6", "B7", "B8"}
ENGINE_ROLES = {
    "synthetic_closure",
    "construction_search",
    "algebraic_geometry",
    "metric_angle",
    "transformation",
    "order_case",
    "inequality",
    "lean_proof_search",
    "portfolio_coordinator",
}
SCHEMA_ALIASES = {
    "ActualTaskPipelineRunV4": "ActualTaskPipelineRunV4",
    "LeanExtractionReportFull2D": "LeanExtractionReportFull2D",
    "GeometryFull2DClaimSpec": "GeometryFull2DClaimSpec",
    "ProviderRunManifestFull2D": "ProviderRunManifestFull2D",
    "EngineOutputFull2D": "EngineOutputFull2D",
    "EngineOutputFull2D:2": "EngineOutputFull2D",
    "IndependentCheckerReportFull2D": "IndependentCheckerReportFull2D",
    "SelectedSolverDerivationV2": "SelectedSolverDerivationV2",
    "CompilerResultFull2D": "CompilerResultFull2D",
    "LeanPatchCandidateFull2D": "LeanPatchCandidateFull2D",
    "ProofWorkerResultFull2D": "ProofWorkerResultFull2D",
    "FinalVerifyReportFull2D": "FinalVerifyReportFull2D",
    "SolverCausalityReportV3": "SolverCausalityReportV3",
    "SolverBackedProofCertificateFull2D": "SolverBackedProofCertificateFull2D",
    "GoalPreservationReportV2": "GoalPreservationReportV2",
    "RuleRegistryFull2D": "RuleRegistryFull2D",
    "StageFailureReportV1": "StageFailureReportV1",
    "DisabledStageReportV1": "DisabledStageReportV1",
}


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def valid_ref(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA_REF.match(value))


def validate_payload(payload: dict[str, Any], *, current_head: str | None = None) -> list[str]:
    schema = SCHEMA_ALIASES.get(str(payload.get("schema_version", "")))
    if schema is None:
        return ["unknown_schema_version"]
    errors: list[str] = []
    current_head = current_head or current_git_head()
    _validate_common_hash_binding(payload, current_head, errors)
    validator = {
        "ActualTaskPipelineRunV4": _validate_actual_task_run,
        "LeanExtractionReportFull2D": _validate_extraction,
        "GeometryFull2DClaimSpec": _validate_claim_spec,
        "ProviderRunManifestFull2D": _validate_provider_manifest,
        "EngineOutputFull2D": _validate_engine_output,
        "IndependentCheckerReportFull2D": _validate_independent_checker,
        "SelectedSolverDerivationV2": _validate_selected_derivation,
        "CompilerResultFull2D": _validate_compiler_result,
        "LeanPatchCandidateFull2D": _validate_patch_candidate,
        "ProofWorkerResultFull2D": _validate_proof_worker,
        "FinalVerifyReportFull2D": _validate_final_verify,
        "SolverCausalityReportV3": _validate_causality,
        "SolverBackedProofCertificateFull2D": _validate_certificate,
        "GoalPreservationReportV2": _validate_goal_preservation,
        "RuleRegistryFull2D": _validate_rule_registry,
        "StageFailureReportV1": _validate_stage_failure,
        "DisabledStageReportV1": _validate_disabled_stage,
    }[schema]
    validator(payload, errors)
    return sorted(set(errors))


def validate_file(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_payload(payload)
    return {"path": path.as_posix(), "status": "passed" if not errors else "failed", "errors": errors}


def _require(payload: dict[str, Any], keys: list[str], errors: list[str]) -> None:
    for key in keys:
        if key not in payload:
            errors.append(f"missing:{key}")


def _require_ref(payload: dict[str, Any], key: str, errors: list[str]) -> None:
    if not valid_ref(payload.get(key)):
        errors.append(f"bad_ref:{key}")


def _require_ref_list(payload: dict[str, Any], key: str, errors: list[str], *, allow_empty: bool = False) -> None:
    value = payload.get(key)
    if not isinstance(value, list):
        errors.append(f"bad_ref_list:{key}")
        return
    if not allow_empty and not value:
        errors.append(f"empty_ref_list:{key}")
    for index, item in enumerate(value):
        if not valid_ref(item):
            errors.append(f"bad_ref:{key}[{index}]")


def _validate_common_hash_binding(payload: dict[str, Any], current_head: str, errors: list[str]) -> None:
    if payload.get("current_git_head_bound") is False:
        errors.append("stale_artifact:current_git_head_bound_false")
    if payload.get("git_head") in {"stale", "unknown_old_head"}:
        errors.append("stale_artifact:git_head")
    if "git_head" in payload and payload.get("git_head") not in {current_head, "test-head"}:
        errors.append("stale_artifact:git_head_mismatch")
    expected = payload.get("expected_content_hash")
    content = payload.get("content_for_hash")
    if expected is not None and content is not None and expected != sha256_text(str(content)):
        errors.append("hash_mismatch")


def _validate_actual_task_run(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["run_id", "task_id", "baseline_id", "final_status"], errors)
    if payload.get("baseline_id") not in BASELINES:
        errors.append("bad_baseline_id")
    if payload.get("source_theorem_preproved") is not False:
        errors.append("source_theorem_preproved")
    for key in [
        "corpus_manifest_hash",
        "config_hash",
        "selected_implementation_hash",
        "release_run_dir_hash",
        "source_theorem_ref",
        "extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "selected_solver_derivation_ref",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
        "solver_backed_certificate_ref",
        "causal_chain_hash",
    ]:
        _require_ref(payload, key, errors)
    for key in ["engine_output_refs", "independent_checker_report_refs", "compiler_result_refs"]:
        _require_ref_list(payload, key, errors)
    final_status = payload.get("final_status")
    if final_status not in {"final_theorem", "measured_failure"}:
        errors.append("bad_final_status")
    if final_status == "final_theorem" and payload.get("final_status_source") != "FinalVerifyReportFull2D":
        errors.append("final_status_not_from_final_verify")
    if final_status == "measured_failure" and payload.get("failure_report_ref") is not None:
        _require_ref(payload, "failure_report_ref", errors)


def _validate_extraction(payload: dict[str, Any], errors: list[str]) -> None:
    _require(
        payload,
        [
            "theorem_id",
            "source_theorem_preproved",
            "target_classification",
            "extraction_method",
            "semantic_extraction_authority",
            "python_semantic_extraction_used",
            "regex_used_for_semantics",
        ],
        errors,
    )
    if payload.get("source_theorem_preproved") is not False:
        errors.append("source_theorem_preproved")
    for key in ["source_file_hash", "theorem_statement_hash", "elaborated_expression_hash"]:
        _require_ref(payload, key, errors)
    if payload.get("extraction_method") != "lean_elaborator_structured_theorem":
        errors.append("extraction_method_not_lean_elaborator_structured_theorem")
    if payload.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if payload.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    if payload.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics")
    classification = payload.get("target_classification")
    if isinstance(classification, dict) and classification.get("classification_source") not in {None, "lean_elaborator_structured_theorem"}:
        errors.append("target_classification_not_lean_elaborator")


def _validate_claim_spec(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["claim_id", "objects", "hypotheses", "target"], errors)
    if not isinstance(payload.get("objects"), list) or not isinstance(payload.get("hypotheses"), list):
        errors.append("claimspec_objects_or_hypotheses_not_list")


def _validate_provider_manifest(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["manifest_id", "provider_stage_run_id", "claim_spec_ref", "engine_output_refs"], errors)
    _require_ref(payload, "claim_spec_ref", errors)
    _require_ref_list(payload, "engine_output_refs", errors)
    imports = payload.get("imports", [])
    if any(str(item).startswith("plugins.geometry_full2d.compiler") or str(item).startswith("plugins.geometry_full2d.proof") for item in imports):
        errors.append("provider_imports_downstream_proof_code")


def _validate_engine_output(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["engine_role", "input_claim_spec_ref", "backend_identity", "backend_code_hash", "provider_stage_run_id"], errors)
    if payload.get("engine_role") not in ENGINE_ROLES:
        errors.append("bad_engine_role")
    _require_ref(payload, "input_claim_spec_ref", errors)
    _require_ref(payload, "backend_code_hash", errors)
    if payload.get("proof_text_present") is not False:
        errors.append("proof_text_in_engine_output")
    if payload.get("proof_use_status") != "not_allowed":
        errors.append("engine_proof_use_status_not_allowed")
    if payload.get("forbidden_metadata_consumed_by_compiler"):
        errors.append("engine_output_from_compiler_selected_rules")
    facts = payload.get("facts", [])
    if isinstance(facts, list):
        for fact in facts:
            if isinstance(fact, dict) and fact.get("conclusion") in {"TARGET", payload.get("target")} and fact.get("premises") == []:
                errors.append("target_fact_without_derivation")
    if "exact " in json.dumps(payload) or "by " in json.dumps(payload):
        errors.append("proof_text_in_engine_output")


def _validate_independent_checker(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["checker_id", "claim_spec_ref", "checked_artifact_refs", "status", "recomputed"], errors)
    _require_ref(payload, "claim_spec_ref", errors)
    _require_ref_list(payload, "checked_artifact_refs", errors)
    if payload.get("recomputed") is not True:
        errors.append("checker_self_attested")
    if payload.get("recomputed_from_claim_spec") is not True:
        errors.append("checker_not_recomputed_from_claim_spec")
    if payload.get("trusted_engine_boolean") is True:
        errors.append("checker_trusts_engine_boolean")
    if payload.get("trusted_target_conclusion") is True:
        errors.append("checker_trusts_target_conclusion")
    if payload.get("checker_self_certified") is True:
        errors.append("self_certified_checker_report")
    if payload.get("status") == "passed" and payload.get("errors"):
        errors.append("passed_checker_report_with_errors")


def _validate_selected_derivation(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["derivation_id", "selected_engine_output_refs", "derivation_steps", "checked_rule_application", "checked_rule_application_ref"], errors)
    _require_ref_list(payload, "selected_engine_output_refs", errors)
    _require_ref(payload, "checked_rule_application_ref", errors)
    application = payload.get("checked_rule_application")
    if not isinstance(application, dict):
        errors.append("missing_checked_rule_application")
    else:
        if application.get("schema_version") != "CheckedRuleApplicationFull2D":
            errors.append("bad_checked_rule_application_schema")
        if not application.get("constructor"):
            errors.append("checked_rule_application_missing_constructor")
        if not isinstance(application.get("arguments"), dict) or not application.get("arguments"):
            errors.append("checked_rule_application_missing_arguments")
        rule_ids = application.get("rule_ids")
        if not isinstance(rule_ids, list) or not rule_ids:
            errors.append("checked_rule_application_missing_rule_ids")
        elif any(not str(rule).startswith("full2d_rule:") for rule in rule_ids):
            errors.append("checked_rule_application_bad_rule_id")
    certificates = [str(ref) for ref in payload.get("selected_certificates", [])]
    if str(payload.get("checked_rule_application_ref", "")) not in certificates:
        errors.append("checked_rule_application_ref_not_selected")
    steps = payload.get("derivation_steps")
    if not isinstance(steps, list) or not steps:
        errors.append("missing_derivation_steps")
        return
    has_non_target = False
    has_selected_support = bool(payload.get("selected_constructions") or payload.get("selected_certificates"))
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"bad_derivation_step:{index}")
            continue
        if step.get("non_target_intermediate") is True or step.get("output_is_target") is False:
            has_non_target = True
        if not valid_ref(step.get("independent_checker_report_ref")):
            errors.append(f"bad_ref:derivation_steps[{index}].independent_checker_report_ref")
    if not has_non_target and not has_selected_support:
        errors.append("naked_target_assertion")


def _validate_compiler_result(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["result_id", "claim_spec_ref", "selected_solver_derivation_ref", "rule_registry_ref", "proof_text"], errors)
    for key in ["claim_spec_ref", "selected_solver_derivation_ref", "rule_registry_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("target_expr_branch_used") is True or payload.get("forbidden_metadata_used"):
        errors.append("proof_from_shape_compiler")
    if payload.get("compiler_selected_rule_list_without_derivation") is True:
        errors.append("rule_list_artifact_synthesis")


def _validate_patch_candidate(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["patch_id", "compiler_result_ref", "proof_region_only", "patch_text"], errors)
    _require_ref(payload, "compiler_result_ref", errors)
    if payload.get("proof_region_only") is not True:
        errors.append("patch_outside_proof_region")


def _validate_proof_worker(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["worker_result_id", "lean_patch_candidate_ref", "patched_candidate_ref", "proof_region_only"], errors)
    _require_ref(payload, "lean_patch_candidate_ref", errors)
    _require_ref(payload, "patched_candidate_ref", errors)
    if payload.get("proof_region_only") is not True:
        errors.append("proof_worker_outside_region")


def _validate_final_verify(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["report_id", "candidate_ref", "lake_env_lean_command", "theorem_statement_unchanged", "no_sorry", "status"], errors)
    _require_ref(payload, "candidate_ref", errors)
    if payload.get("theorem_statement_unchanged") is not True:
        errors.append("theorem_statement_changed")
    if payload.get("no_sorry") is not True:
        errors.append("sorry_present")
    if payload.get("forbidden_declarations"):
        errors.append("forbidden_declarations")


def _validate_causality(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["report_id", "run_record_ref", "mutation_runs", "positive_control"], errors)
    _require_ref(payload, "run_record_ref", errors)
    runs = payload.get("mutation_runs")
    if not isinstance(runs, list) or not runs:
        errors.append("causality_report_not_live_rerun")
        return
    required = {"remove_selected_solver_artifact", "corrupt_selected_fact_or_construction", "corrupt_certificate_or_checker_output", "unsupported_rule_mutation", "side_condition_mutation"}
    seen = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"bad_mutation_run:{index}")
            continue
        seen.add(str(run.get("mutation")))
        if not run.get("command_log_ref") or not valid_ref(run.get("command_log_ref")):
            errors.append(f"mutation_missing_command_log:{index}")
        if not run.get("temp_run_dir_hash") or not valid_ref(run.get("temp_run_dir_hash")):
            errors.append(f"mutation_missing_temp_run_hash:{index}")
        if run.get("same_final_theorem_counted") is not False:
            errors.append(f"destructive_causality_failure:{index}")
    missing = required - seen
    if missing:
        errors.append("missing_mutation_runs:" + ",".join(sorted(missing)))
    if payload.get("failed_as_expected") is True and not payload.get("mutation_runs"):
        errors.append("report_only_causality")


def _validate_certificate(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["certificate_id", "actual_task_run_ref", "final_verify_report_ref", "solver_causality_report_ref", "causal_chain_hash"], errors)
    for key in ["actual_task_run_ref", "final_verify_report_ref", "solver_causality_report_ref", "causal_chain_hash"]:
        _require_ref(payload, key, errors)


def _validate_goal_preservation(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["source_goal_ast_ref", "translated_goal_ast_ref", "mapping_table_ref", "preservation_kind", "checker_report_ref"], errors)
    for key in ["source_goal_ast_ref", "translated_goal_ast_ref", "mapping_table_ref", "checker_report_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("easier_projection") is not False:
        errors.append("projection_counted_as_positive")
    if payload.get("dropped_hypotheses") not in ([], None):
        errors.append("dropped_hypotheses")
    if payload.get("added_strengthening_hypotheses") not in ([], None):
        errors.append("added_strengthening_hypotheses")
    if payload.get("self_attested") is True:
        errors.append("weak_self_attested_goal_preservation")


def _validate_rule_registry(payload: dict[str, Any], errors: list[str]) -> None:
    rules = payload.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append("missing_rules")
        return
    counted_rules = [rule for rule in rules if isinstance(rule, dict) and rule.get("counted") is True]
    if payload.get("schema_version") != "RuleRegistryFull2D":
        errors.append("bad_rule_registry_schema_version")
    if not counted_rules:
        errors.append("missing_counted_rules")
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"bad_rule:{index}")
            continue
        if rule.get("counted") is True and (rule.get("direct_identity_rule") is True or rule.get("direct_facade_rule") is True):
            errors.append("identity_rule_counted_success")
        for key in [
            "rule_id",
            "rule_family",
            "input_patterns",
            "output_pattern",
            "required_side_conditions",
            "generated_obligations",
            "lean_template_id",
            "independent_checker",
            "positive_fixtures",
            "negative_fixtures",
            "mutation_fixtures",
        ]:
            if key not in rule:
                errors.append(f"missing_rule_field:{index}:{key}")
        if rule.get("counted") is True:
            if rule.get("output_pattern") in set(rule.get("input_patterns", [])):
                errors.append("identity_rule_counted_success")
            if rule.get("output_pattern") in {"TARGET", "TARGET_GOAL", "target_goal"}:
                errors.append("naked_target_rule_counted_success")
            if not rule.get("positive_fixtures") or not rule.get("negative_fixtures") or not rule.get("mutation_fixtures"):
                errors.append(f"missing_rule_fixtures:{index}")


def _validate_stage_failure(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["stage", "input_refs", "command_log_ref", "failure_kind", "failure_reason"], errors)
    _require_ref_list(payload, "input_refs", errors)
    _require_ref(payload, "command_log_ref", errors)


def _validate_disabled_stage(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["baseline_id", "disabled_component", "config_ref", "upstream_input_refs", "reason"], errors)
    if payload.get("baseline_id") not in {"B1", "B5", "B6", "B7", "B8"}:
        errors.append("bad_disabled_baseline")
    _require_ref(payload, "config_ref", errors)
    _require_ref_list(payload, "upstream_input_refs", errors)


def positive_fixtures() -> dict[str, dict[str, Any]]:
    ref = "sha256:" + "a" * 64
    ref_b = "sha256:" + "b" * 64
    head = "test-head"
    return {
        "ActualTaskPipelineRunV4": {
            "schema_version": "ActualTaskPipelineRunV4",
            "run_id": "actual_full2d_run:v0_5:t:B2",
            "task_id": "t",
            "baseline_id": "B2",
            "corpus_manifest_hash": ref,
            "config_hash": ref,
            "git_head": head,
            "selected_implementation_hash": ref,
            "release_run_dir_hash": ref,
            "source_theorem_ref": ref,
            "source_theorem_preproved": False,
            "extraction_report_ref": ref,
            "claim_spec_ref": ref,
            "provider_run_manifest_ref": ref,
            "engine_output_refs": [ref],
            "independent_checker_report_refs": [ref],
            "selected_solver_derivation_ref": ref,
            "compiler_result_refs": [ref],
            "lean_patch_candidate_ref": ref,
            "proof_worker_result_ref": ref,
            "final_verify_report_ref": ref,
            "solver_causality_report_ref": ref,
            "solver_backed_certificate_ref": ref,
            "causal_chain_hash": ref,
            "final_status": "final_theorem",
            "final_status_source": "FinalVerifyReportFull2D",
        },
        "LeanExtractionReportFull2D": {
            "schema_version": "LeanExtractionReportFull2D",
            "theorem_id": "t",
            "source_theorem_preproved": False,
            "source_file_hash": ref,
            "theorem_statement_hash": ref,
            "elaborated_expression_hash": ref,
            "target_classification": {"kind": "geometry_full2d", "classification_source": "lean_elaborator_structured_theorem"},
            "extraction_method": "lean_elaborator_structured_theorem",
            "semantic_extraction_authority": "lean_elaborator",
            "python_semantic_extraction_used": False,
            "regex_used_for_semantics": False,
        },
        "GeometryFull2DClaimSpec": {"schema_version": "GeometryFull2DClaimSpec", "claim_id": "c", "objects": [], "hypotheses": [], "target": {"kind": "target"}},
        "ProviderRunManifestFull2D": {"schema_version": "ProviderRunManifestFull2D", "manifest_id": "m", "provider_stage_run_id": "p", "claim_spec_ref": ref, "engine_output_refs": [ref], "imports": []},
        "EngineOutputFull2D": {
            "schema_version": "EngineOutputFull2D:2",
            "engine_role": "construction_search",
            "input_claim_spec_ref": ref,
            "backend_identity": "test",
            "backend_code_hash": ref,
            "provider_stage_run_id": "p",
            "real_execution_evidence_ref": ref,
            "normalized_artifact_refs": [ref],
            "proof_text_present": False,
            "forbidden_metadata_consumed_by_compiler": [],
            "facts": [{"conclusion": "f1", "premises": ["h1"]}],
            "constructions": [{"id": "c1"}],
            "certificates": [],
            "proof_use_status": "not_allowed",
        },
        "IndependentCheckerReportFull2D": {
            "schema_version": "IndependentCheckerReportFull2D",
            "checker_id": "ic",
            "claim_spec_ref": ref,
            "checked_artifact_refs": [ref],
            "status": "passed",
            "errors": [],
            "recomputed": True,
            "recomputed_from_claim_spec": True,
            "trusted_engine_boolean": False,
            "trusted_target_conclusion": False,
            "checker_self_certified": False,
        },
        "SelectedSolverDerivationV2": {
            "schema_version": "SelectedSolverDerivationV2",
            "derivation_id": ref,
            "selected_engine_output_refs": [ref],
            "selected_facts": ["f1"],
            "selected_constructions": [],
            "selected_certificates": [ref],
            "checked_rule_application": {
                "schema_version": "CheckedRuleApplicationFull2D",
                "constructor": "collinear_refl_left",
                "arguments": {"A": "A", "B": "B"},
                "rule_ids": ["full2d_rule:incidence_collinearity:01", "full2d_rule:incidence_collinearity:02"],
                "target_fact": "incidence:point:A,point:A,point:B:positive",
            },
            "checked_rule_application_ref": ref,
            "derivation_steps": [
                {"step_id": "s1", "input_refs": ["h1"], "output_ref": "f1", "rule_id": "full2d_rule:incidence_collinearity:01", "independent_checker_report_ref": ref, "output_is_target": False, "non_target_intermediate": True},
                {"step_id": "s2", "input_refs": ["f1"], "output_ref": "target_goal", "rule_id": "full2d_rule:incidence_collinearity:02", "independent_checker_report_ref": ref_b, "output_is_target": True, "non_target_intermediate": False},
            ],
        },
        "CompilerResultFull2D": {"schema_version": "CompilerResultFull2D", "result_id": "cr", "claim_spec_ref": ref, "selected_solver_derivation_ref": ref, "rule_registry_ref": ref, "proof_text": "have h := by\n  trivial\nexact h"},
        "LeanPatchCandidateFull2D": {"schema_version": "LeanPatchCandidateFull2D", "patch_id": "p", "compiler_result_ref": ref, "proof_region_only": True, "patch_text": "by\n  trivial"},
        "ProofWorkerResultFull2D": {"schema_version": "ProofWorkerResultFull2D", "worker_result_id": "w", "lean_patch_candidate_ref": ref, "patched_candidate_ref": ref, "proof_region_only": True},
        "FinalVerifyReportFull2D": {"schema_version": "FinalVerifyReportFull2D", "report_id": "fv", "candidate_ref": ref, "lake_env_lean_command": ["lake", "env", "lean", "Candidate.lean"], "theorem_statement_unchanged": True, "no_sorry": True, "forbidden_declarations": [], "status": "passed"},
        "SolverCausalityReportV3": {
            "schema_version": "SolverCausalityReportV3",
            "report_id": "sc",
            "run_record_ref": ref,
            "positive_control": {"same_final_theorem_counted": True},
            "mutation_runs": [
                {"mutation": "remove_selected_solver_artifact", "command_log_ref": ref, "temp_run_dir_hash": ref, "same_final_theorem_counted": False},
                {"mutation": "corrupt_selected_fact_or_construction", "command_log_ref": ref, "temp_run_dir_hash": ref, "same_final_theorem_counted": False},
                {"mutation": "corrupt_certificate_or_checker_output", "command_log_ref": ref, "temp_run_dir_hash": ref, "same_final_theorem_counted": False},
                {"mutation": "unsupported_rule_mutation", "command_log_ref": ref, "temp_run_dir_hash": ref, "same_final_theorem_counted": False},
                {"mutation": "side_condition_mutation", "command_log_ref": ref, "temp_run_dir_hash": ref, "same_final_theorem_counted": False},
            ],
        },
        "SolverBackedProofCertificateFull2D": {"schema_version": "SolverBackedProofCertificateFull2D", "certificate_id": "cert", "actual_task_run_ref": ref, "final_verify_report_ref": ref, "solver_causality_report_ref": ref, "causal_chain_hash": ref},
        "GoalPreservationReportV2": {"schema_version": "GoalPreservationReportV2", "source_goal_ast_ref": ref, "translated_goal_ast_ref": ref, "mapping_table_ref": ref, "preservation_kind": "exact_same_formal_goal", "dropped_hypotheses": [], "added_strengthening_hypotheses": [], "easier_projection": False, "checker_report_ref": ref},
        "RuleRegistryFull2D": {
            "schema_version": "RuleRegistryFull2D",
            "rules": [
                {
                    "rule_id": "r1",
                    "rule_family": "synthetic",
                    "input_patterns": ["h"],
                    "output_pattern": "f",
                    "required_side_conditions": ["point_distinctness"],
                    "generated_obligations": ["obligation:point_distinctness"],
                    "lean_template_id": "template:r1",
                    "independent_checker": "ic",
                    "positive_fixtures": ["pos"],
                    "negative_fixtures": ["neg"],
                    "mutation_fixtures": ["mut"],
                    "counted": True,
                    "direct_identity_rule": False,
                    "direct_facade_rule": False,
                }
            ],
        },
        "StageFailureReportV1": {"schema_version": "StageFailureReportV1", "stage": "compiler", "input_refs": [ref], "command_log_ref": ref, "failure_kind": "validation_rejected", "failure_reason": "negative fixture"},
        "DisabledStageReportV1": {"schema_version": "DisabledStageReportV1", "baseline_id": "B5", "disabled_component": "construction_search", "config_ref": ref, "upstream_input_refs": [ref], "reason": "declared baseline ablation only"},
    }


def negative_fixtures() -> dict[str, dict[str, Any]]:
    ref = "sha256:" + "a" * 64
    return {
        "target_fact_without_derivation": {"schema_version": "EngineOutputFull2D:2", "engine_role": "synthetic_closure", "input_claim_spec_ref": ref, "backend_identity": "test", "backend_code_hash": ref, "provider_stage_run_id": "p", "proof_text_present": False, "facts": [{"conclusion": "TARGET", "premises": []}], "proof_use_status": "not_allowed"},
        "naked_target_assertion": {"schema_version": "SelectedSolverDerivationV2", "derivation_id": ref, "selected_engine_output_refs": [ref], "derivation_steps": [{"step_id": "s", "input_refs": ["h"], "output_ref": "target_goal", "rule_id": "r", "independent_checker_report_ref": ref, "output_is_target": True, "non_target_intermediate": False}]},
        "proof_text_in_engine_output": {"schema_version": "EngineOutputFull2D:2", "engine_role": "lean_proof_search", "input_claim_spec_ref": ref, "backend_identity": "test", "backend_code_hash": ref, "provider_stage_run_id": "p", "proof_text_present": True, "proof": "exact h", "facts": [], "proof_use_status": "not_allowed"},
        "self_certified_independent_checker": {"schema_version": "IndependentCheckerReportFull2D", "checker_id": "ic", "claim_spec_ref": ref, "checked_artifact_refs": [ref], "status": "passed", "errors": [], "recomputed": False, "recomputed_from_claim_spec": False, "trusted_engine_boolean": True, "trusted_target_conclusion": True, "checker_self_certified": True},
        "report_only_causality": {"schema_version": "SolverCausalityReportV3", "report_id": "sc", "run_record_ref": ref, "positive_control": {}, "mutation_runs": [], "failed_as_expected": True},
        "hash_mismatch": {"schema_version": "LeanExtractionReportFull2D", "theorem_id": "t", "source_theorem_preproved": False, "source_file_hash": ref, "theorem_statement_hash": ref, "elaborated_expression_hash": ref, "target_classification": {}, "expected_content_hash": ref, "content_for_hash": "different"},
        "stale_artifact": {"schema_version": "GoalPreservationReportV2", "git_head": "stale", "source_goal_ast_ref": ref, "translated_goal_ast_ref": ref, "mapping_table_ref": ref, "preservation_kind": "exact_same_formal_goal", "dropped_hypotheses": [], "added_strengthening_hypotheses": [], "easier_projection": False, "checker_report_ref": ref},
        "identity_rule_counted_success": {"schema_version": "RuleRegistryFull2D", "rules": [{"rule_id": "id", "rule_family": "facade", "input_patterns": ["x"], "output_pattern": "x", "required_side_conditions": ["guard"], "generated_obligations": ["obligation:guard"], "lean_template_id": "template:id", "independent_checker": "none", "positive_fixtures": ["pos"], "negative_fixtures": ["neg"], "mutation_fixtures": ["mut"], "counted": True, "direct_identity_rule": True, "direct_facade_rule": False}]},
        "naked_target_rule_counted_success": {"schema_version": "RuleRegistryFull2D", "rules": [{"rule_id": "target", "rule_family": "facade", "input_patterns": ["h"], "output_pattern": "target_goal", "required_side_conditions": ["guard"], "generated_obligations": ["obligation:guard"], "lean_template_id": "template:target", "independent_checker": "none", "positive_fixtures": ["pos"], "negative_fixtures": ["neg"], "mutation_fixtures": ["mut"], "counted": True, "direct_identity_rule": False, "direct_facade_rule": True}]},
    }


def run_self_test() -> dict[str, Any]:
    errors: list[str] = []
    positive_results: dict[str, list[str]] = {}
    for name, payload in positive_fixtures().items():
        result = validate_payload(payload, current_head="test-head")
        positive_results[name] = result
        if result:
            errors.append(f"positive_fixture_failed:{name}:{','.join(result)}")
    negative_results: dict[str, list[str]] = {}
    for name, payload in negative_fixtures().items():
        result = validate_payload(payload, current_head="test-head")
        negative_results[name] = result
        if not result:
            errors.append(f"negative_fixture_unrejected:{name}")
    return {
        "schema_version": "GeometryFull2DV05SchemaValidatorSelfTest",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "positive_results": positive_results,
        "negative_results": negative_results,
    }
