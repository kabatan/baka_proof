from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
SHA_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
BASELINES = {"B1", "B2", "B5", "B6", "B7", "B8"}
ENGINE_ROLES = {
    "synthetic_trace",
    "construction",
    "algebraic_metric_certificate",
    "order_case",
    "inequality",
    "lean_search_certificate",
    "external_solver_trace",
}
DOWNSTREAM_IMPORT_PARTS = (
    "compiler",
    "rule_registry",
    "proof_generation",
    "proof_worker",
    "final_verify",
    "matrix",
    "release",
    "release_checker",
    "corpus",
    "corpus_generator",
    "previous_release",
    "prior_release",
    "proof_template",
    "v0_5",
    "v0_4",
)
SCHEMA_ALIASES = {
    "LeanExtractionReportFull2D": "LeanExtractionReportFull2D",
    "GeometryFull2DClaimSpec": "GeometryFull2DClaimSpec",
    "ProviderRunManifestV3": "ProviderRunManifestV3",
    "EngineOutputFull2D": "EngineOutputFull2D",
    "IndependentSolverArtifactCheckV1": "IndependentSolverArtifactCheckV1",
    "SelectedSolverDerivationV3": "SelectedSolverDerivationV3",
    "DerivationTargetMatchReportV1": "DerivationTargetMatchReportV1",
    "CompilerResultFull2D": "CompilerResultFull2D",
    "LeanPatchCandidateFull2D": "LeanPatchCandidateFull2D",
    "ProofWorkerResultFull2D": "ProofWorkerResultFull2D",
    "FinalVerifyReportFull2D": "FinalVerifyReportFull2D",
    "SolverBackedProofCertificateFull2D": "SolverBackedProofCertificateFull2D",
    "ActualTaskPipelineRunV4": "ActualTaskPipelineRunV4",
    "SolverCausalityLiveRunV1": "SolverCausalityLiveRunV1",
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


def validate_file(path: Path, *, current_head: str | None = None) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_payload(payload, current_head=current_head)
    return {"path": path.as_posix(), "status": "passed" if not errors else "failed", "errors": errors}


def validate_payload(payload: Any, *, current_head: str | None = None) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_not_object"]
    schema = SCHEMA_ALIASES.get(str(payload.get("schema_version", "")))
    if schema is None:
        return ["unknown_schema_version"]
    errors: list[str] = []
    current_head = current_head or current_git_head()
    _validate_common(payload, current_head, errors)
    validators: dict[str, Callable[[dict[str, Any], list[str]], None]] = {
        "LeanExtractionReportFull2D": _validate_extraction,
        "GeometryFull2DClaimSpec": _validate_claim_spec,
        "ProviderRunManifestV3": _validate_provider_manifest,
        "EngineOutputFull2D": _validate_engine_output,
        "IndependentSolverArtifactCheckV1": _validate_independent_check,
        "SelectedSolverDerivationV3": _validate_selected_derivation,
        "DerivationTargetMatchReportV1": _validate_target_match_report,
        "CompilerResultFull2D": _validate_compiler_result,
        "LeanPatchCandidateFull2D": _validate_patch_candidate,
        "ProofWorkerResultFull2D": _validate_proof_worker_result,
        "FinalVerifyReportFull2D": _validate_final_verify_report,
        "SolverBackedProofCertificateFull2D": _validate_certificate,
        "ActualTaskPipelineRunV4": _validate_actual_task_run,
        "SolverCausalityLiveRunV1": _validate_causality_live_run,
        "StageFailureReportV1": _validate_stage_failure,
        "DisabledStageReportV1": _validate_disabled_stage,
    }
    validators[schema](payload, errors)
    return sorted(set(errors))


def _validate_common(payload: dict[str, Any], current_head: str, errors: list[str]) -> None:
    text = json.dumps(payload, sort_keys=True).lower()
    for marker in (
        "schema_only_fake_evidence",
        "schema_only_certificate",
        "checker_generated_success_artifacts",
        "fabricated_pipeline_success",
        "static_only_release",
        "report_only_causality",
        "stale_evidence_replay",
    ):
        if marker in text:
            errors.append(f"schema_only_or_forbidden_marker:{marker}")
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
    for key, value in _walk_items(payload):
        if key.endswith("_ref") and value is not None and not valid_ref(value):
            errors.append(f"bad_ref:{key}")
        if key.endswith("_refs"):
            if not isinstance(value, list):
                errors.append(f"bad_ref_list:{key}")
            else:
                for index, item in enumerate(value):
                    if not valid_ref(item):
                        errors.append(f"bad_ref:{key}[{index}]")


def _walk_items(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            full = f"{prefix}.{key}" if prefix else str(key)
            items.append((str(key), item))
            items.extend(_walk_items(item, full))
    elif isinstance(value, list):
        for item in value:
            items.extend(_walk_items(item, prefix))
    return items


def _require(payload: dict[str, Any], keys: list[str], errors: list[str]) -> None:
    for key in keys:
        if key not in payload:
            errors.append(f"missing:{key}")
        elif payload.get(key) in (None, "", [], {}):
            errors.append(f"empty:{key}")


def _require_present(payload: dict[str, Any], keys: list[str], errors: list[str]) -> None:
    for key in keys:
        if key not in payload:
            errors.append(f"missing:{key}")
        elif payload.get(key) in (None, ""):
            errors.append(f"empty:{key}")


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


def _require_ref_or_null(payload: dict[str, Any], key: str, errors: list[str]) -> None:
    if key not in payload:
        errors.append(f"missing:{key}")
        return
    value = payload.get(key)
    if value is not None and not valid_ref(value):
        errors.append(f"bad_ref_or_null:{key}")


def _validate_extraction(payload: dict[str, Any], errors: list[str]) -> None:
    _require_present(
        payload,
        [
            "report_id",
            "theorem_name",
            "statement_hash",
            "elaborated_expression_hash",
            "canonical_target",
            "hypotheses",
            "side_condition_obligations",
            "target_classification",
            "source_file_ref",
            "extraction_method",
            "semantic_extraction_authority",
            "source_theorem_preproved",
            "python_semantic_extraction_used",
            "regex_used_for_semantics",
            "git_head",
            "config_hash",
            "checker_hash_set_ref",
        ],
        errors,
    )
    for key in ["source_file_ref", "statement_hash", "elaborated_expression_hash", "config_hash", "checker_hash_set_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("source_theorem_preproved") is not False:
        errors.append("source_theorem_preproved")
    if payload.get("extraction_method") != "lean_elaborator_structured_theorem":
        errors.append("extraction_method_not_lean_elaborator_structured_theorem")
    if payload.get("semantic_extraction_authority") != "lean_elaborator":
        errors.append("semantic_extraction_authority_not_lean_elaborator")
    if payload.get("python_semantic_extraction_used") is not False:
        errors.append("python_semantic_extraction_used")
    if payload.get("regex_used_for_semantics") is not False:
        errors.append("regex_used_for_semantics")
    if not isinstance(payload.get("hypotheses"), list):
        errors.append("hypotheses_not_list")
    if not isinstance(payload.get("side_condition_obligations"), list):
        errors.append("side_condition_obligations_not_list")


def _validate_claim_spec(payload: dict[str, Any], errors: list[str]) -> None:
    _require_present(payload, ["claim_id", "extraction_report_ref", "canonical_target", "objects", "hypotheses", "side_conditions", "target_hash", "source_ref", "git_head", "content_hash"], errors)
    for key in ["extraction_report_ref", "target_hash", "source_ref", "content_hash"]:
        _require_ref(payload, key, errors)
    if not isinstance(payload.get("objects"), list):
        errors.append("objects_not_list")
    if not isinstance(payload.get("hypotheses"), list):
        errors.append("hypotheses_not_list")
    if "proof" in payload or "tactic_script" in payload:
        errors.append("claimspec_contains_proof_material")


def _validate_provider_manifest(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["manifest_id", "claim_spec_ref", "provider_stage_run_id", "provider_started_at", "provider_completed_at", "engine_output_refs", "imports", "provider_code_hash", "git_head", "config_hash"], errors)
    for key in ["claim_spec_ref", "provider_code_hash", "config_hash"]:
        _require_ref(payload, key, errors)
    _require_ref_list(payload, "engine_output_refs", errors)
    imports = payload.get("imports", [])
    if not isinstance(imports, list):
        errors.append("imports_not_list")
        imports = []
    joined = " ".join(str(item).lower() for item in imports)
    if any(part in joined for part in DOWNSTREAM_IMPORT_PARTS):
        errors.append("provider_imports_downstream_module")
    if str(payload.get("provider_started_at")) >= str(payload.get("provider_completed_at")):
        errors.append("provider_stage_timestamp_order_invalid")


def _validate_engine_output(payload: dict[str, Any], errors: list[str]) -> None:
    _require_present(
        payload,
        [
            "engine_output_id",
            "engine_role",
            "claim_spec_ref",
            "provider_run_manifest_ref",
            "provider_stage_run_id",
            "backend_identity",
            "backend_code_hash",
            "selected_artifacts",
            "independent_checker_refs",
            "proof_text_present",
            "created_before_compiler",
            "git_head",
        ],
        errors,
    )
    if payload.get("engine_role") not in ENGINE_ROLES:
        errors.append("bad_engine_role")
    for key in ["claim_spec_ref", "provider_run_manifest_ref", "backend_code_hash"]:
        _require_ref(payload, key, errors)
    _require_ref_list(payload, "independent_checker_refs", errors, allow_empty=True)
    if payload.get("proof_text_present") is not False:
        errors.append("proof_text_in_engine_output")
    if payload.get("created_before_compiler") is not True:
        errors.append("engine_output_not_before_compiler")
    for forbidden in ("proof", "proof_text", "tactic_script", "lean_lemma_template_id", "proof_replacement_text"):
        if forbidden in payload:
            errors.append(f"engine_output_contains_{forbidden}")
    artifacts = payload.get("selected_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("missing_selected_artifacts")
        return
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"bad_selected_artifact:{index}")
            continue
        if artifact.get("is_final_target") is True and artifact.get("premises") == []:
            errors.append("target_fact_without_derivation")
        if artifact.get("kind") in {"fact", "construction", "certificate"} and not artifact.get("premises") and artifact.get("kind") == "fact":
            errors.append(f"fact_missing_premises:{index}")
        certificate_payload = artifact.get("certificate_payload")
        if isinstance(certificate_payload, str) and certificate_payload in {"FINAL_TARGET", "target_hash", "target_expr"}:
            errors.append("target_as_certificate")
        if isinstance(certificate_payload, dict) and (
            certificate_payload.get("kind") in {"FINAL_TARGET", "target_hash", "target_expr", "target_statement"}
            or certificate_payload.get("payload") in {"FINAL_TARGET", "target_hash", "target_expr"}
        ):
            errors.append("target_as_certificate")


def _validate_independent_check(payload: dict[str, Any], errors: list[str]) -> None:
    _require(
        payload,
        [
            "check_id",
            "checker_name",
            "claim_spec_ref",
            "artifact_ref",
            "artifact_kind",
            "status",
            "premises_verified",
            "side_conditions_verified",
            "conclusion_verified",
            "independent_from_provider",
            "independent_from_compiler",
            "command_log_ref",
            "checker_code_hash",
            "git_head",
        ],
        errors,
    )
    for key in ["claim_spec_ref", "artifact_ref", "command_log_ref", "checker_code_hash"]:
        _require_ref(payload, key, errors)
    if payload.get("status") != "passed":
        errors.append("independent_check_not_passed")
    for key in ["premises_verified", "side_conditions_verified", "conclusion_verified", "independent_from_provider", "independent_from_compiler"]:
        if payload.get(key) is not True:
            errors.append(f"{key}_not_true")
    if payload.get("trusted_engine_boolean") is True:
        errors.append("checker_trusts_engine_boolean")
    if payload.get("trusted_target_conclusion") is True:
        errors.append("checker_trusts_target_conclusion")


def _validate_selected_derivation(payload: dict[str, Any], errors: list[str]) -> None:
    _require(
        payload,
        [
            "derivation_id",
            "claim_spec_ref",
            "selected_steps",
            "final_step_ref",
            "has_non_target_intermediate",
            "has_checked_side_condition_or_certificate",
        ],
        errors,
    )
    for key in ["derivation_id", "claim_spec_ref", "final_step_ref"]:
        _require_ref(payload, key, errors)
    steps = payload.get("selected_steps")
    if not isinstance(steps, list) or not steps:
        errors.append("missing_selected_steps")
    else:
        has_non_target_step = False
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"bad_selected_step:{index}")
                continue
            _require(step, ["step_id", "artifact_ref", "artifact_kind", "checker_ref", "rule_id", "premises", "conclusion", "is_final_target"], errors)
            for key in ["artifact_ref", "checker_ref"]:
                if not valid_ref(step.get(key)):
                    errors.append(f"bad_ref:selected_steps[{index}].{key}")
            if step.get("artifact_kind") not in {"fact", "construction", "certificate", "trace_step", "case_split"}:
                errors.append(f"bad_artifact_kind:selected_steps[{index}]")
            if not isinstance(step.get("premises"), list) or not step.get("premises"):
                errors.append(f"missing_premises:selected_steps[{index}]")
            if not str(step.get("rule_id", "")).startswith("full2d_rule:"):
                errors.append(f"bad_rule_id:selected_steps[{index}]")
            if "proof_text" in step or "tactic_script" in step or "lean_template_id" in step:
                errors.append(f"selected_derivation_contains_proof_material:{index}")
            if step.get("is_final_target") is False:
                has_non_target_step = True
            for marker in (
                "alpha_renamed_target",
                "target_hash_intermediate",
                "trivial_target_wrapper",
                "reflexivity_or_symmetry_equivalent_target",
                "direct_facade_target",
                "normalizes_to_target_without_checked_solver",
            ):
                if step.get(marker) is True:
                    errors.append(f"target_equivalent_intermediate:selected_steps[{index}].{marker}")
        if payload.get("has_non_target_intermediate") is True and not has_non_target_step:
            errors.append("has_non_target_intermediate_without_non_target_step")
    if payload.get("has_non_target_intermediate") is not True and payload.get("has_checked_side_condition_or_certificate") is not True:
        errors.append("missing_semantic_non_target_or_checked_support")
    for marker in (
        "alpha_renamed_target",
        "target_hash_intermediate",
        "trivial_target_wrapper",
        "reflexivity_or_symmetry_equivalent_target",
        "direct_facade_target",
        "normalizes_to_target_without_checked_solver",
    ):
        if payload.get(marker) is True:
            errors.append(f"target_equivalent_intermediate:{marker}")


def _validate_target_match_report(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["match_report_id", "selected_derivation_ref", "claim_spec_ref", "status", "final_step_hash", "target_hash", "command_log_ref", "git_head"], errors)
    for key in ["selected_derivation_ref", "claim_spec_ref", "final_step_hash", "target_hash", "command_log_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("status") != "passed":
        errors.append("target_match_not_passed")
    for forbidden in ("proof_text", "tactic_script", "target_expr", "target_expression_string", "strategy_label", "rule_ids", "corpus_labels"):
        if forbidden in payload:
            errors.append(f"target_matcher_forbidden_output:{forbidden}")


def _validate_compiler_result(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["compiler_result_id", "theorem_anchor_ref", "selected_derivation_ref", "rule_registry_snapshot_ref", "side_condition_report_refs", "lean_patch_candidate_ref", "compiler_code_hash", "compile_inputs", "git_head"], errors)
    for key in ["theorem_anchor_ref", "selected_derivation_ref", "rule_registry_snapshot_ref", "lean_patch_candidate_ref", "compiler_code_hash"]:
        _require_ref(payload, key, errors)
    _require_ref_list(payload, "side_condition_report_refs", errors, allow_empty=True)
    expected_inputs = {"TheoremAnchorV1", "SelectedSolverDerivationV3", "RuleRegistrySnapshot", "SideConditionReport"}
    if set(payload.get("compile_inputs", [])) != expected_inputs:
        errors.append("compiler_api_inputs_not_exact")
    for forbidden in (
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
    ):
        if forbidden in payload:
            errors.append(f"compiler_forbidden_input_or_branch:{forbidden}")


def _validate_patch_candidate(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["patch_id", "compiler_result_ref", "patch_text_hash", "patch_region", "inside_marp_region", "theorem_anchor_ref", "git_head"], errors)
    for key in ["compiler_result_ref", "patch_text_hash", "theorem_anchor_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("inside_marp_region") is not True:
        errors.append("patch_outside_marp_region")
    if payload.get("mutates_theorem_statement") is True:
        errors.append("patch_mutates_theorem_statement")


def _validate_proof_worker_result(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["worker_result_id", "lean_patch_candidate_ref", "patched_candidate_ref", "proof_region_only", "worker_command_log_ref", "claim_final_theorem", "git_head"], errors)
    for key in ["lean_patch_candidate_ref", "patched_candidate_ref", "worker_command_log_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("proof_region_only") is not True:
        errors.append("proof_worker_outside_region")
    if payload.get("claim_final_theorem") is not False:
        errors.append("proof_worker_claims_final_theorem")


def _validate_final_verify_report(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["verify_report_id", "patched_candidate_ref", "lake_env_lean_command", "status", "theorem_statement_unchanged", "no_sorry", "no_admit", "no_axiom", "no_unsafe", "protected_theorem_unchanged", "command_log_ref", "candidate_hash", "git_head"], errors)
    for key in ["patched_candidate_ref", "command_log_ref", "candidate_hash"]:
        _require_ref(payload, key, errors)
    command = payload.get("lake_env_lean_command")
    if not isinstance(command, list) or command[:3] != ["lake", "env", "lean"]:
        errors.append("final_verify_not_lake_env_lean")
    if payload.get("status") != "passed":
        errors.append("final_verify_not_passed")
    for key in ["theorem_statement_unchanged", "no_sorry", "no_admit", "no_axiom", "no_unsafe", "protected_theorem_unchanged"]:
        if payload.get(key) is not True:
            errors.append(f"{key}_not_true")


def _validate_certificate(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["certificate_id", "actual_task_run_ref", "claim_spec_ref", "engine_output_refs", "selected_derivation_ref", "compiler_result_ref", "proof_worker_result_ref", "final_verify_report_ref", "solver_causality_live_run_ref", "causal_chain_hash", "git_head"], errors)
    for key in ["actual_task_run_ref", "claim_spec_ref", "selected_derivation_ref", "compiler_result_ref", "proof_worker_result_ref", "final_verify_report_ref", "solver_causality_live_run_ref", "causal_chain_hash"]:
        _require_ref(payload, key, errors)
    _require_ref_list(payload, "engine_output_refs", errors)
    payload_text = json.dumps(payload, sort_keys=True)
    if "FINAL_TARGET" in payload_text or "target_as_certificate" in payload_text or "target_hash_certificate" in payload_text:
        errors.append("target_as_certificate")


def _validate_actual_task_run(payload: dict[str, Any], errors: list[str]) -> None:
    _require(
        payload,
        [
            "run_id",
            "task_id",
            "baseline_id",
            "git_head",
            "git_status_hash",
            "selected_implementation_hash",
            "corpus_manifest_hash",
            "config_hash",
            "checker_hash_set_ref",
            "release_run_dir_hash",
            "stage_timestamps",
            "source_theorem_ref",
            "extraction_report_ref",
            "claim_spec_ref",
            "provider_run_manifest_ref",
            "engine_output_refs",
            "independent_solver_artifact_check_refs",
            "selected_solver_derivation_ref",
            "derivation_target_match_ref",
            "compiler_result_refs",
            "lean_patch_candidate_ref",
            "proof_worker_result_ref",
            "final_verify_report_ref",
            "final_status",
        ],
        errors,
    )
    if payload.get("baseline_id") not in BASELINES:
        errors.append("bad_baseline_id")
    for key in [
        "git_status_hash",
        "corpus_manifest_hash",
        "config_hash",
        "selected_implementation_hash",
        "checker_hash_set_ref",
        "release_run_dir_hash",
        "source_theorem_ref",
        "extraction_report_ref",
        "claim_spec_ref",
        "provider_run_manifest_ref",
        "selected_solver_derivation_ref",
        "derivation_target_match_ref",
        "lean_patch_candidate_ref",
        "proof_worker_result_ref",
        "final_verify_report_ref",
    ]:
        _require_ref(payload, key, errors)
    _require_ref_or_null(payload, "solver_backed_certificate_ref", errors)
    _require_ref_or_null(payload, "stage_failure_report_ref", errors)
    _require_ref_list(payload, "engine_output_refs", errors)
    _require_ref_list(payload, "independent_solver_artifact_check_refs", errors)
    _require_ref_list(payload, "compiler_result_refs", errors)
    timestamps = payload.get("stage_timestamps")
    if not isinstance(timestamps, dict):
        errors.append("stage_timestamps_not_object")
    else:
        for key in ["extraction_started_at", "provider_started_at", "provider_finished_at", "compiler_started_at", "final_verify_finished_at"]:
            if not timestamps.get(key):
                errors.append(f"missing_stage_timestamp:{key}")
        if timestamps.get("provider_started_at") and timestamps.get("provider_finished_at") and str(timestamps["provider_started_at"]) >= str(timestamps["provider_finished_at"]):
            errors.append("provider_stage_timestamp_order_invalid")
        if timestamps.get("provider_finished_at") and timestamps.get("compiler_started_at") and str(timestamps["provider_finished_at"]) >= str(timestamps["compiler_started_at"]):
            errors.append("compiler_started_before_provider_finished")
    status = payload.get("final_status")
    if status not in {"final_theorem", "measured_failure"}:
        errors.append("bad_final_status")
    if status == "final_theorem" and payload.get("solver_backed_certificate_ref") is None:
        errors.append("final_theorem_missing_solver_backed_certificate_ref")
    if status == "final_theorem" and payload.get("stage_failure_report_ref") is not None:
        errors.append("final_theorem_has_stage_failure_report_ref")
    if status == "measured_failure" and payload.get("stage_failure_report_ref") is None:
        errors.append("measured_failure_missing_stage_failure_report_ref")


def _validate_causality_live_run(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["report_id", "source_actual_run_ref", "temp_run_dir_ref", "mutation_cases", "status"], errors)
    for key in ["report_id", "source_actual_run_ref", "temp_run_dir_ref"]:
        _require_ref(payload, key, errors)
    if payload.get("status") not in {"passed", "failed"}:
        errors.append("bad_causality_status")
    runs = payload.get("mutation_cases")
    if not isinstance(runs, list) or not runs:
        errors.append("causality_report_not_live_rerun")
        return
    required = {
        "positive_control",
        "remove_selected_artifact",
        "corrupt_non_target_intermediate",
        "corrupt_construction_or_certificate",
        "unsupported_rule_mutation",
        "side_condition_mutation",
        "remove_checker_transcript",
    }
    seen: set[str] = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"bad_mutation_run:{index}")
            continue
        kind = str(run.get("mutation_kind"))
        seen.add(kind)
        for key in ["command_log_ref", "input_artifact_set_hash"]:
            if not valid_ref(run.get(key)):
                errors.append(f"bad_ref:mutation_runs[{index}].{key}")
        _require_ref_or_null(run, "output_patch_hash", errors)
        if run.get("final_verify_status") not in {"passed", "failed", "not_run"}:
            errors.append(f"bad_final_verify_status:mutation_cases[{index}]")
        if kind == "positive_control":
            if run.get("final_verify_status") != "passed":
                errors.append("positive_control_final_verify_not_passed")
            if run.get("counted_same_final_theorem") is not True:
                errors.append("positive_control_did_not_reproduce_final_theorem")
        elif run.get("counted_same_final_theorem") is not False:
            errors.append(f"mutation_did_not_break_same_final_theorem:{index}")
    missing = required - seen
    if missing:
        errors.append("missing_mutation_kinds:" + ",".join(sorted(missing)))


def _validate_stage_failure(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["stage", "input_refs", "command_log_ref", "failure_kind", "failure_reason", "git_head"], errors)
    _require_ref_list(payload, "input_refs", errors)
    _require_ref(payload, "command_log_ref", errors)
    if payload.get("failure_kind") in {"label_coded", "summary_only"}:
        errors.append("measured_failure_not_actual_stage_failure")


def _validate_disabled_stage(payload: dict[str, Any], errors: list[str]) -> None:
    _require(payload, ["baseline_id", "disabled_component", "config_ref", "upstream_input_refs", "reason", "stage_removed_or_disabled", "git_head"], errors)
    if payload.get("baseline_id") not in {"B1", "B5", "B6", "B7", "B8"}:
        errors.append("bad_disabled_baseline")
    _require_ref(payload, "config_ref", errors)
    _require_ref_list(payload, "upstream_input_refs", errors)
    if payload.get("stage_removed_or_disabled") is not True:
        errors.append("disabled_stage_not_removed_or_disabled")


def _ref(char: str) -> str:
    return "sha256:" + char * 64


def positive_fixtures() -> dict[str, dict[str, Any]]:
    a, b, c = _ref("a"), _ref("b"), _ref("c")
    head = "test-head"
    common = {"git_head": head}
    return {
        "LeanExtractionReportFull2D": {
            **common,
            "schema_version": "LeanExtractionReportFull2D",
            "report_id": "extract:test",
            "theorem_name": "Geom.Test",
            "statement_hash": a,
            "elaborated_expression_hash": b,
            "canonical_target": {"predicate": "Collinear", "args": ["A", "B", "C"]},
            "hypotheses": [{"name": "h1", "expr": "A <> B"}],
            "side_condition_obligations": [{"kind": "distinct", "args": ["A", "B"]}],
            "target_classification": {"domain": "full2d", "source": "lean_elaborator"},
            "source_file_ref": c,
            "extraction_method": "lean_elaborator_structured_theorem",
            "semantic_extraction_authority": "lean_elaborator",
            "source_theorem_preproved": False,
            "python_semantic_extraction_used": False,
            "regex_used_for_semantics": False,
            "config_hash": a,
            "checker_hash_set_ref": b,
        },
        "GeometryFull2DClaimSpec": {
            **common,
            "schema_version": "GeometryFull2DClaimSpec",
            "claim_id": "claim:test",
            "extraction_report_ref": a,
            "canonical_target": {"predicate": "Collinear", "args": ["A", "B", "C"]},
            "objects": [{"name": "A", "kind": "Point"}],
            "hypotheses": [{"name": "h1", "expr": "A <> B"}],
            "side_conditions": [{"kind": "distinct", "args": ["A", "B"]}],
            "target_hash": b,
            "source_ref": c,
            "content_hash": a,
        },
        "ProviderRunManifestV3": {
            **common,
            "schema_version": "ProviderRunManifestV3",
            "manifest_id": "provider:test",
            "claim_spec_ref": a,
            "provider_stage_run_id": "provider-stage:test",
            "provider_started_at": "2026-06-20T00:00:00Z",
            "provider_completed_at": "2026-06-20T00:00:01Z",
            "engine_output_refs": [b],
            "imports": ["geometry_full2d_v0_6.provider_primitives"],
            "provider_code_hash": c,
            "config_hash": a,
        },
        "EngineOutputFull2D": {
            **common,
            "schema_version": "EngineOutputFull2D",
            "engine_output_id": "engine:test",
            "engine_role": "construction",
            "claim_spec_ref": a,
            "provider_run_manifest_ref": b,
            "provider_stage_run_id": "provider-stage:test",
            "backend_identity": "synthetic-construction-positive",
            "backend_code_hash": c,
            "selected_artifacts": [{"kind": "construction", "conclusion": "Midpoint M A B", "premises": ["hAB"], "is_final_target": False}],
            "independent_checker_refs": [a],
            "proof_text_present": False,
            "created_before_compiler": True,
        },
        "IndependentSolverArtifactCheckV1": {
            **common,
            "schema_version": "IndependentSolverArtifactCheckV1",
            "check_id": "check:test",
            "checker_name": "construction_checker",
            "claim_spec_ref": a,
            "artifact_ref": b,
            "artifact_kind": "construction",
            "status": "passed",
            "premises_verified": True,
            "side_conditions_verified": True,
            "conclusion_verified": True,
            "independent_from_provider": True,
            "independent_from_compiler": True,
            "command_log_ref": c,
            "checker_code_hash": a,
        },
        "SelectedSolverDerivationV3": {
            **common,
            "schema_version": "SelectedSolverDerivationV3",
            "derivation_id": a,
            "claim_spec_ref": a,
            "selected_steps": [
                {
                    "step_id": "s1",
                    "artifact_ref": b,
                    "artifact_kind": "construction",
                    "checker_ref": c,
                    "rule_id": "full2d_rule:construction_midpoint:001",
                    "premises": ["hAB"],
                    "conclusion": "Midpoint M A B",
                    "is_final_target": False,
                }
            ],
            "final_step_ref": b,
            "has_non_target_intermediate": True,
            "has_checked_side_condition_or_certificate": True,
        },
        "DerivationTargetMatchReportV1": {
            **common,
            "schema_version": "DerivationTargetMatchReportV1",
            "match_report_id": "match:test",
            "selected_derivation_ref": a,
            "claim_spec_ref": b,
            "status": "passed",
            "final_step_hash": c,
            "target_hash": c,
            "command_log_ref": a,
        },
        "CompilerResultFull2D": {
            **common,
            "schema_version": "CompilerResultFull2D",
            "compiler_result_id": "compiler:test",
            "theorem_anchor_ref": a,
            "selected_derivation_ref": b,
            "rule_registry_snapshot_ref": c,
            "side_condition_report_refs": [a],
            "lean_patch_candidate_ref": b,
            "compiler_code_hash": c,
            "compile_inputs": ["TheoremAnchorV1", "SelectedSolverDerivationV3", "RuleRegistrySnapshot", "SideConditionReport"],
        },
        "LeanPatchCandidateFull2D": {
            **common,
            "schema_version": "LeanPatchCandidateFull2D",
            "patch_id": "patch:test",
            "compiler_result_ref": a,
            "patch_text_hash": b,
            "patch_region": "MARP",
            "inside_marp_region": True,
            "theorem_anchor_ref": c,
        },
        "ProofWorkerResultFull2D": {
            **common,
            "schema_version": "ProofWorkerResultFull2D",
            "worker_result_id": "worker:test",
            "lean_patch_candidate_ref": a,
            "patched_candidate_ref": b,
            "proof_region_only": True,
            "worker_command_log_ref": c,
            "claim_final_theorem": False,
        },
        "FinalVerifyReportFull2D": {
            **common,
            "schema_version": "FinalVerifyReportFull2D",
            "verify_report_id": "verify:test",
            "patched_candidate_ref": a,
            "lake_env_lean_command": ["lake", "env", "lean", "Candidate.lean"],
            "status": "passed",
            "theorem_statement_unchanged": True,
            "no_sorry": True,
            "no_admit": True,
            "no_axiom": True,
            "no_unsafe": True,
            "protected_theorem_unchanged": True,
            "command_log_ref": b,
            "candidate_hash": c,
        },
        "SolverBackedProofCertificateFull2D": {
            **common,
            "schema_version": "SolverBackedProofCertificateFull2D",
            "certificate_id": "cert:test",
            "actual_task_run_ref": a,
            "claim_spec_ref": b,
            "engine_output_refs": [c],
            "selected_derivation_ref": a,
            "compiler_result_ref": b,
            "proof_worker_result_ref": c,
            "final_verify_report_ref": a,
            "solver_causality_live_run_ref": b,
            "causal_chain_hash": c,
        },
        "ActualTaskPipelineRunV4": {
            **common,
            "schema_version": "ActualTaskPipelineRunV4",
            "run_id": "actual_full2d_run:v0_6:test",
            "task_id": "task:test",
            "baseline_id": "B2",
            "git_status_hash": a,
            "corpus_manifest_hash": a,
            "config_hash": b,
            "checker_hash_set_ref": c,
            "selected_implementation_hash": c,
            "release_run_dir_hash": a,
            "stage_timestamps": {
                "extraction_started_at": "2026-06-20T00:00:00Z",
                "provider_started_at": "2026-06-20T00:00:01Z",
                "provider_finished_at": "2026-06-20T00:00:02Z",
                "compiler_started_at": "2026-06-20T00:00:03Z",
                "final_verify_finished_at": "2026-06-20T00:00:04Z"
            },
            "source_theorem_ref": a,
            "extraction_report_ref": b,
            "claim_spec_ref": b,
            "provider_run_manifest_ref": c,
            "engine_output_refs": [a],
            "independent_solver_artifact_check_refs": [b],
            "selected_solver_derivation_ref": c,
            "derivation_target_match_ref": a,
            "compiler_result_refs": [b],
            "lean_patch_candidate_ref": c,
            "proof_worker_result_ref": a,
            "final_verify_report_ref": b,
            "solver_backed_certificate_ref": c,
            "stage_failure_report_ref": None,
            "final_status": "final_theorem",
        },
        "SolverCausalityLiveRunV1": {
            **common,
            "schema_version": "SolverCausalityLiveRunV1",
            "report_id": a,
            "source_actual_run_ref": b,
            "temp_run_dir_ref": c,
            "mutation_cases": [
                {"mutation_kind": "positive_control", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": c, "final_verify_status": "passed", "counted_same_final_theorem": True},
                {"mutation_kind": "remove_selected_artifact", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
                {"mutation_kind": "corrupt_non_target_intermediate", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
                {"mutation_kind": "corrupt_construction_or_certificate", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
                {"mutation_kind": "unsupported_rule_mutation", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
                {"mutation_kind": "side_condition_mutation", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
                {"mutation_kind": "remove_checker_transcript", "command_log_ref": a, "input_artifact_set_hash": b, "output_patch_hash": None, "final_verify_status": "failed", "counted_same_final_theorem": False},
            ],
            "status": "passed",
        },
        "StageFailureReportV1": {
            **common,
            "schema_version": "StageFailureReportV1",
            "stage": "final_verify",
            "input_refs": [a],
            "command_log_ref": b,
            "failure_kind": "lean_compile_failed",
            "failure_reason": "negative mutation failed to compile",
        },
        "DisabledStageReportV1": {
            **common,
            "schema_version": "DisabledStageReportV1",
            "baseline_id": "B5",
            "disabled_component": "construction",
            "config_ref": a,
            "upstream_input_refs": [b],
            "reason": "declared baseline ablation",
            "stage_removed_or_disabled": True,
        },
    }


def negative_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = positive_fixtures()
    bad: dict[str, dict[str, Any]] = {}
    bad["target_fact_provider"] = {**fixtures["EngineOutputFull2D"], "selected_artifacts": [{"kind": "fact", "conclusion": "FINAL_TARGET", "premises": [], "is_final_target": True}]}
    bad["proof_text_engine_output"] = {**fixtures["EngineOutputFull2D"], "proof_text_present": True, "proof_text": "exact h"}
    bad["provider_imports_compiler"] = {**fixtures["ProviderRunManifestV3"], "imports": ["geometry_full2d_v0_6.compiler"]}
    bad["naked_target_derivation"] = {
        **fixtures["SelectedSolverDerivationV3"],
        "selected_steps": [{**fixtures["SelectedSolverDerivationV3"]["selected_steps"][0], "is_final_target": True}],
        "has_non_target_intermediate": False,
        "has_checked_side_condition_or_certificate": False,
    }
    bad["target_equivalent_intermediate"] = {
        **fixtures["SelectedSolverDerivationV3"],
        "selected_steps": [{**fixtures["SelectedSolverDerivationV3"]["selected_steps"][0], "target_hash_intermediate": True}],
    }
    bad["target_matcher_outputs_strategy"] = {**fixtures["DerivationTargetMatchReportV1"], "strategy_label": "collinear-target"}
    bad["compiler_forbidden_anchor_branch"] = {**fixtures["CompilerResultFull2D"], "theorem_name": "Geom.Target", "statement_hash": _ref("d")}
    bad["proof_worker_claims_final"] = {**fixtures["ProofWorkerResultFull2D"], "claim_final_theorem": True}
    bad["final_verify_accepts_sorry"] = {**fixtures["FinalVerifyReportFull2D"], "no_sorry": False}
    bad["target_as_certificate"] = {**fixtures["SolverBackedProofCertificateFull2D"], "certificate_payload": "FINAL_TARGET"}
    bad["report_only_causality"] = {**fixtures["SolverCausalityLiveRunV1"], "mutation_cases": [], "report_only_causality": True}
    bad["b2_label_final_status"] = {**fixtures["ActualTaskPipelineRunV4"], "final_status": "final_theorem", "solver_backed_certificate_ref": None}
    bad["stage_failure_label_coded"] = {**fixtures["StageFailureReportV1"], "failure_kind": "label_coded"}
    bad["disabled_stage_not_disabled"] = {**fixtures["DisabledStageReportV1"], "stage_removed_or_disabled": False}
    bad["stale_git_head"] = {**fixtures["GeometryFull2DClaimSpec"], "git_head": "stale"}
    bad["hash_mismatch"] = {**fixtures["GeometryFull2DClaimSpec"], "expected_content_hash": _ref("a"), "content_for_hash": "different-content"}
    return bad


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
        "schema_version": "GeometryFull2DV06SchemaValidatorSelfTest",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "positive_results": positive_results,
        "negative_results": negative_results,
    }
