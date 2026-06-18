from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from plugins.geometry_full2d.engine_contracts import ENGINE_ROLES, canonical_json, hash_ref
from scripts.geometry_full2d_v0_5_schemas import validate_payload


ROOT = Path(__file__).resolve().parents[1]
IDENTITY_KEYS = {"artifact_id", "output_id", "content_sha256", "payload_sha256", "artifact_sha256"}
CHECKER_KIND_BY_ROLE = {
    "synthetic_closure": "synthetic_trace_replay",
    "construction_search": "construction_existence_side_condition_validation",
    "algebraic_geometry": "algebraic_certificate_replay",
    "metric_angle": "metric_angle_relation_replay",
    "transformation": "external_trace_normalization_replay",
    "order_case": "order_case_split_validation",
    "inequality": "inequality_certificate_replay",
    "lean_proof_search": "lean_search_certificate_check",
    "portfolio_coordinator": "external_trace_normalization_replay",
}


def run_independent_solver_checkers(run_dir: Path, *, claim_spec_json: Path | None = None, write_reports: bool = True) -> dict[str, Any]:
    root = resolve_path(run_dir)
    stage_dir = root / "provider_stage"
    summary_path = stage_dir / "provider_cli_summary.json"
    if not summary_path.exists():
        return {
            "schema_version": "IndependentSolverCheckersSummaryV05",
            "status": "failed",
            "errors": ["missing_provider_cli_summary"],
            "run_dir": str(root),
            "report_count": 0,
            "checker_kinds_covered": [],
        }
    provider_summary = read_json(summary_path)
    artifact_paths = provider_summary.get("artifact_paths", {})
    if not isinstance(artifact_paths, dict):
        artifact_paths = {}
    claim_ref = str(provider_summary.get("claim_spec_ref", ""))
    claim_path = resolve_claim_path(root, provider_summary, artifact_paths, claim_ref, claim_spec_json)
    errors: list[str] = []
    if claim_path is None or not claim_path.exists():
        errors.append("missing_claim_spec_for_recomputation")
        claim_spec: dict[str, Any] = {}
    else:
        claim_spec = read_json(claim_path)
        if claim_ref.startswith("sha256:") and sha256_file(claim_path) != claim_ref:
            errors.append("claim_spec_ref_hash_mismatch")
    engine_dir = stage_dir / "engine_outputs"
    if not engine_dir.exists():
        errors.append("missing_provider_stage_engine_outputs")
    reports: list[dict[str, Any]] = []
    report_paths: dict[str, str] = {}
    for path in sorted(engine_dir.glob("*.json")) if engine_dir.exists() else []:
        engine_output = read_json(path)
        report = check_engine_output_artifacts(engine_output, claim_spec, claim_ref, root, artifact_paths)
        reports.append(report)
        errors.extend(f"{report['engine_role']}:{error}" for error in report.get("errors", []))
        schema_errors = validate_checker_report_payload(report)
        errors.extend(f"{report['engine_role']}:report_schema:{error}" for error in schema_errors)
        if write_reports:
            ref, report_path = write_report(root / "independent_checker_stage" / "reports" / f"{report['engine_role']}.json", report)
            report_paths[ref] = report_path.relative_to(root).as_posix()
    roles_seen = sorted({str(report.get("engine_role")) for report in reports})
    missing_roles = sorted(set(ENGINE_ROLES) - set(roles_seen))
    if missing_roles:
        errors.append("missing_engine_roles:" + ",".join(missing_roles))
    kinds = sorted({str(report.get("checker_kind")) for report in reports if report.get("status") == "passed"})
    required_kinds = sorted(set(CHECKER_KIND_BY_ROLE.values()))
    missing_kinds = sorted(set(required_kinds) - set(kinds))
    if missing_kinds:
        errors.append("missing_checker_kinds:" + ",".join(missing_kinds))
    summary = {
        "schema_version": "IndependentSolverCheckersSummaryV05",
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "run_dir": str(root),
        "claim_spec_ref": claim_ref,
        "report_count": len(reports),
        "roles_seen": roles_seen,
        "checker_kinds_covered": kinds,
        "required_checker_kinds": required_kinds,
        "report_paths": report_paths,
        "reports": reports,
    }
    if write_reports:
        write_json(root / "independent_checker_stage" / "independent_checker_summary.json", summary)
    return summary


def check_engine_output_artifacts(
    engine_output: dict[str, Any],
    claim_spec: dict[str, Any],
    claim_ref: str,
    run_dir: Path,
    artifact_paths: dict[str, Any],
) -> dict[str, Any]:
    role = str(engine_output.get("engine_role", "unknown"))
    checker_kind = CHECKER_KIND_BY_ROLE.get(role, "unknown_checker")
    errors: list[str] = []
    schema_errors = validate_payload(engine_output, current_head="test-head")
    errors.extend(f"engine_output_schema:{error}" for error in schema_errors)
    if engine_output.get("input_claim_spec_ref") != claim_ref:
        errors.append("engine_output_claim_ref_mismatch")
    if engine_output.get("proof_text_present") is not False:
        errors.append("proof_text_present")
    if engine_output.get("proof_use_status") != "not_allowed":
        errors.append("proof_use_status_not_allowed")
    if engine_output.get("forbidden_metadata_consumed_by_compiler"):
        errors.append("forbidden_metadata_consumed_by_compiler")
    if engine_output.get("engine_status") != "normalized_success":
        checked_refs = [str(engine_output.get("output_id"))] if str(engine_output.get("output_id", "")).startswith("sha256:") else [hash_ref(canonical_json(engine_output))]
        return checker_report(role, checker_kind, claim_ref, checked_refs, errors)
    artifact_refs = [str(ref) for ref in engine_output.get("normalized_artifact_refs", []) if isinstance(ref, str)]
    if not artifact_refs:
        errors.append("normalized_success_missing_artifact_ref")
        return checker_report(role, checker_kind, claim_ref, [hash_ref(canonical_json(engine_output))], errors)
    semantic_artifacts: list[dict[str, Any]] = []
    for ref in artifact_refs:
        loaded, load_errors = load_semantic_artifact(run_dir, artifact_paths, ref)
        errors.extend(load_errors)
        if loaded is not None:
            semantic_artifacts.append(loaded)
    if not semantic_artifacts:
        errors.append("no_replayable_semantic_artifact")
        return checker_report(role, checker_kind, claim_ref, artifact_refs, errors)
    for artifact in semantic_artifacts:
        errors.extend(role_replay_errors(role, claim_spec, artifact, engine_output))
    return checker_report(role, checker_kind, claim_ref, artifact_refs, errors)


def checker_report(role: str, checker_kind: str, claim_ref: str, checked_refs: list[str], errors: list[str]) -> dict[str, Any]:
    unsigned = {
        "schema_version": "IndependentCheckerReportFull2D",
        "engine_role": role,
        "checker_kind": checker_kind,
        "claim_spec_ref": claim_ref,
        "checked_artifact_refs": checked_refs,
        "status": "passed" if not errors else "failed",
        "errors": sorted(set(errors)),
        "recomputed": True,
        "recomputed_from_claim_spec": True,
        "trusted_engine_boolean": False,
        "trusted_target_conclusion": False,
        "checker_self_certified": False,
        "proof_use_status": "not_allowed",
        "checker_code_ref": sha256_file(Path(__file__)),
    }
    checker_id = "independent_checker:" + role + ":" + sha256_text(canonical_json(unsigned))[7:23]
    return {"checker_id": checker_id, **unsigned}


def validate_checker_report_payload(report: dict[str, Any]) -> list[str]:
    errors = validate_payload(report, current_head="test-head")
    if report.get("recomputed_from_claim_spec") is not True:
        errors.append("checker_not_recomputed_from_claim_spec")
    if report.get("trusted_target_conclusion") is True:
        errors.append("checker_trusts_target_conclusion")
    if report.get("checker_self_certified") is True:
        errors.append("self_certified_checker_report")
    if report.get("status") == "passed" and report.get("errors"):
        errors.append("passed_report_with_errors")
    if report.get("status") not in {"passed", "failed"}:
        errors.append("bad_checker_status")
    return sorted(set(errors))


def role_replay_errors(role: str, claim_spec: dict[str, Any], artifact: dict[str, Any], engine_output: dict[str, Any]) -> list[str]:
    common = common_artifact_errors(role, claim_spec, artifact, engine_output)
    checker = {
        "synthetic_closure": check_synthetic_trace,
        "construction_search": check_construction_artifact,
        "algebraic_geometry": check_algebraic_certificate,
        "metric_angle": check_metric_angle_trace,
        "transformation": check_transformation_trace,
        "order_case": check_order_case_gate,
        "inequality": check_inequality_certificate,
        "lean_proof_search": check_lean_search_trace,
        "portfolio_coordinator": check_portfolio_decision,
    }.get(role)
    if checker is None:
        return common + ["unknown_engine_role_for_checker"]
    return common + checker(claim_spec, artifact)


def common_artifact_errors(role: str, claim_spec: dict[str, Any], artifact: dict[str, Any], engine_output: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("proof_use_status") != "not_allowed":
        errors.append("artifact_proof_use_status_not_allowed")
    if artifact.get("checker_self_certified") is True or artifact.get("self_attested") is True:
        errors.append("self_certified_artifact")
    if artifact.get("checker_result") == "passed" and len(artifact) <= 4:
        errors.append("report_only_checker_result")
    text = json.dumps(artifact, sort_keys=True).lower()
    for token in (" exact ", " by ", "rw [", "simp ", "nlinarith", "linarith"):
        if token in text:
            errors.append("proof_text_like_token_in_artifact")
    target = target_fact(claim_spec)
    for index, fact in enumerate(engine_output.get("facts", [])):
        if isinstance(fact, dict) and fact.get("conclusion") == target and not fact.get("premises"):
            errors.append(f"engine_output_target_fact_missing_premises:{index}")
    if role != str(artifact.get("engine_role", role)) and artifact.get("engine_role") is not None:
        errors.append("artifact_engine_role_mismatch")
    return errors


def check_synthetic_trace(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    target = target_fact(claim_spec)
    if artifact.get("target_fact") != target:
        errors.append("synthetic_target_fact_mismatch")
    steps = artifact.get("steps")
    if not isinstance(steps, list) or not steps:
        return errors + ["synthetic_trace_missing_steps"]
    prior_outputs: set[str] = set()
    non_target_outputs: set[str] = set()
    target_steps = 0
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"synthetic_bad_step:{index}")
            continue
        output = str(step.get("output_fact", ""))
        inputs = [str(item) for item in step.get("input_facts", [])]
        if not str(step.get("rule_id", "")).startswith("full2d_rule:"):
            errors.append(f"synthetic_bad_rule_id:{index}")
        if output == target:
            target_steps += 1
            if not inputs:
                errors.append(f"synthetic_target_step_missing_premises:{index}")
            if not any(item in non_target_outputs for item in inputs):
                errors.append(f"synthetic_target_step_without_non_target_support:{index}")
        else:
            non_target_outputs.add(output)
        prior_outputs.add(output)
    if target_steps != 1:
        errors.append("synthetic_trace_target_step_count_not_one")
    if not non_target_outputs:
        errors.append("synthetic_trace_missing_non_target_intermediate")
    if is_collinear_reflexive_target(claim_spec):
        args = target_args(claim_spec)
        expected_support = f"synthetic_support:repeated_point_collinearity:{','.join(args)}"
        if expected_support not in prior_outputs:
            errors.append("synthetic_recomputed_support_missing")
    elif target in hypothesis_fact_keys(claim_spec):
        errors.append("synthetic_direct_target_hypothesis_success")
    else:
        errors.append("synthetic_unsupported_claimspec")
    return errors


def check_construction_artifact(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = str(artifact.get("construction_kind", ""))
    deps = tuple(str(item) for item in artifact.get("dependencies", ()))
    required_side = tuple(str(item) for item in artifact.get("required_side_conditions", ()))
    obligations = tuple(str(item) for item in artifact.get("generated_obligations", ()))
    if not artifact.get("construction_id"):
        errors.append("construction_missing_id")
    if obligations != tuple(f"obligation:{condition}" for condition in required_side):
        errors.append("construction_obligations_not_recomputed_from_side_conditions")
    if kind == "line_through_two_points":
        points = tuple(point_object_ids(claim_spec)[:2])
        if deps != points:
            errors.append("construction_line_dependencies_mismatch")
        if not required_side or not all(condition in all_side_conditions(claim_spec) for condition in required_side):
            errors.append("construction_line_side_conditions_missing")
        if not artifact.get("introduced_objects"):
            errors.append("construction_line_missing_introduced_object")
    elif kind == "midpoint_collinearity_witness":
        if deps != target_args(claim_spec) or not has_midpoint_hypothesis(claim_spec, deps):
            errors.append("construction_midpoint_not_recomputed")
    elif kind in {"circle_construction_projection", "line_circle_intersection_projection", "center_construction_projection"}:
        if deps != target_args(claim_spec) or not has_projection_hypothesis(claim_spec, kind, deps):
            errors.append("construction_projection_not_recomputed")
    else:
        errors.append("construction_unknown_kind")
    return errors


def check_algebraic_certificate(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    family = target_family(claim_spec)
    args = target_args(claim_spec)
    steps = tuple(str(item) for item in artifact.get("reduction_steps", ()))
    if str(artifact.get("target_family")) != family:
        errors.append("algebraic_target_family_mismatch")
    if family == "metric" and "equal_length" in target_source_expr(claim_spec) and len(args) == 4:
        if args[:2] == args[2:]:
            if "cancel_identical_distance_terms" not in steps:
                errors.append("algebraic_reflexive_metric_step_missing")
        elif not hypothesis_with_args(claim_spec, "equal_length", args[2:] + args[:2]):
            errors.append("algebraic_reverse_equal_length_hypothesis_missing")
        elif "apply_symmetric_equality_rewrite" not in steps:
            errors.append("algebraic_metric_symmetry_step_missing")
    elif family in {"incidence", "collinear"} and len(args) == 3 and has_repeated_point(args):
        if "det(" not in str(artifact.get("polynomial_goal", "")) or "reduce_determinant_with_equal_rows_to_zero" not in steps:
            errors.append("algebraic_collinearity_certificate_not_replayed")
    else:
        errors.append("algebraic_unsupported_claimspec")
    if artifact.get("checker_result") != "passed":
        errors.append("algebraic_certificate_internal_status_not_passed")
    return errors


def check_metric_angle_trace(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    family = target_family(claim_spec)
    args = target_args(claim_spec)
    if artifact.get("target_fact") != target_fact(claim_spec):
        errors.append("metric_angle_target_fact_mismatch")
    rules = tuple(str(item) for item in artifact.get("rule_ids", ()))
    if not rules:
        errors.append("metric_angle_missing_rules")
    if family == "angle" and "directed_angle_eq_mod_pi" in target_source_expr(claim_spec) and len(args) == 6:
        if args[:3] == args[3:]:
            if artifact.get("normalization_policy") != "directed_angle_mod_pi_reflexivity":
                errors.append("metric_angle_reflexive_policy_mismatch")
        elif not hypothesis_with_args(claim_spec, "directed_angle_eq_mod_pi", args[3:] + args[:3]):
            errors.append("metric_angle_reverse_hypothesis_missing")
    elif family in {"incidence", "collinear"} and len(args) == 3 and (args[0] == args[1] or args[1] == args[2]):
        if not has_nonzero_baseline(args, all_side_conditions(claim_spec)):
            errors.append("metric_angle_side_condition_missing")
        if artifact.get("normalized_value") != "0 mod pi":
            errors.append("metric_angle_normalized_value_mismatch")
    else:
        errors.append("metric_angle_unsupported_claimspec")
    return errors


def check_transformation_trace(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    family = target_family(claim_spec)
    args = target_args(claim_spec)
    kind = str(artifact.get("transformation_kind", ""))
    if family == "transformation" and "rotation_preserves_collinear" in target_source_expr(claim_spec) and len(args) == 6:
        for index in range(3):
            if equality_hypothesis(claim_spec, args[index], args[index + 3]) is None:
                errors.append("transformation_rotation_equality_hypothesis_missing")
                break
    elif family == "transformation" and "reflection_image" in target_source_expr(claim_spec) and len(args) == 1:
        if kind != "reflection_evidence_projection":
            errors.append("transformation_reflection_kind_mismatch")
    elif family in {"incidence", "collinear"} and len(args) == 3 and has_repeated_point(args):
        if not all_side_conditions(claim_spec):
            errors.append("transformation_side_conditions_missing")
        if kind != "rotation_zero_angle_identity":
            errors.append("transformation_repeated_kind_mismatch")
    else:
        errors.append("transformation_unsupported_claimspec")
    if not artifact.get("construction_witnesses"):
        errors.append("transformation_missing_witnesses")
    if not artifact.get("rule_ids"):
        errors.append("transformation_missing_rules")
    return errors


def check_order_case_gate(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if artifact.get("target_fact") != target_fact(claim_spec):
        errors.append("order_case_target_fact_mismatch")
    cases = artifact.get("cases")
    if not isinstance(cases, list) or not cases:
        return errors + ["order_case_missing_cases"]
    rules = tuple(str(item) for item in artifact.get("coverage_rule_ids", ()))
    if not rules:
        errors.append("order_case_missing_coverage_rules")
    args = target_args(claim_spec)
    between = between_hypothesis(claim_spec, args)
    statuses = {str(case.get("status")) for case in cases if isinstance(case, dict)}
    if between:
        if "closed_by_between_order" not in statuses:
            errors.append("order_case_between_status_missing")
    elif has_repeated_point(args):
        if "closed_by_repeated_point" not in statuses:
            errors.append("order_case_repeated_status_missing")
    else:
        errors.append("order_case_unsupported_claimspec")
    obligations = [item for case in cases if isinstance(case, dict) for item in case.get("obligations", ())]
    if target_fact(claim_spec) not in obligations:
        errors.append("order_case_target_obligation_missing")
    return errors


def check_inequality_certificate(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    args = target_args(claim_spec)
    source = target_source_expr(claim_spec)
    steps = tuple(str(item) for item in artifact.get("certificate_steps", ()))
    scope = str(artifact.get("certificate_scope", ""))
    if target_family(claim_spec) == "inequality" and "length_le" in source and len(args) == 4:
        if args[:2] == args[2:]:
            if "apply_reflexive_order_certificate" not in steps:
                errors.append("inequality_reflexive_step_missing")
        elif length_le_trans_hypotheses(claim_spec, args) is None:
            errors.append("inequality_transitive_hypotheses_missing")
        elif "compose_length_inequalities_by_transitivity" not in steps:
            errors.append("inequality_transitive_step_missing")
    elif scope == "side_condition_domain":
        pair = first_distinct_point_pair(nondegeneracy_conditions(claim_spec))
        if pair is None:
            errors.append("inequality_domain_pair_missing")
        elif str(artifact.get("inequality_goal")) != f"squared_distance({pair[0]}, {pair[1]}) > 0":
            errors.append("inequality_domain_goal_mismatch")
        if "expand_squared_distance_as_sum_of_squares" not in steps:
            errors.append("inequality_domain_step_missing")
    else:
        errors.append("inequality_unsupported_claimspec")
    return errors


def check_lean_search_trace(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    args = target_args(claim_spec)
    if not (target_family(claim_spec) in {"incidence", "collinear"} and len(args) == 3 and args[0] == args[1]):
        errors.append("lean_search_unsupported_claimspec")
    if artifact.get("target_fact") != target_fact(claim_spec):
        errors.append("lean_search_target_fact_mismatch")
    used_rules = tuple(str(item) for item in artifact.get("used_rule_refs", ()))
    if not used_rules:
        errors.append("lean_search_missing_used_rules")
    if artifact.get("semantic_check_status") != "passed":
        errors.append("lean_search_semantic_check_not_passed")
    if str(artifact.get("source_statement_hash", "")) != str(claim_spec.get("source_statement_hash", "")):
        errors.append("lean_search_source_statement_hash_mismatch")
    return errors


def check_portfolio_decision(claim_spec: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_features = portfolio_features(claim_spec)
    if artifact.get("selection_features") != expected_features:
        errors.append("portfolio_features_mismatch")
    expected_order, expected_reasons, expected_groups = portfolio_policy(expected_features)
    if tuple(artifact.get("selected_engine_order", ())) != expected_order:
        errors.append("portfolio_order_mismatch")
    if tuple(artifact.get("reason_codes", ())) != expected_reasons:
        errors.append("portfolio_reason_codes_mismatch")
    groups = tuple(tuple(item) for item in artifact.get("parallel_groups", ()))
    if groups != expected_groups:
        errors.append("portfolio_parallel_groups_mismatch")
    if artifact.get("llm_semantics_used") is not False:
        errors.append("portfolio_llm_semantics_used")
    application = artifact.get("checked_rule_application")
    if not isinstance(application, dict):
        errors.append("portfolio_missing_checked_rule_application")
    else:
        if application.get("schema_version") != "CheckedRuleApplicationFull2D":
            errors.append("rule_application_schema_invalid")
        if not application.get("constructor"):
            errors.append("rule_application_missing_constructor")
        if not isinstance(application.get("arguments"), dict) or not application.get("arguments"):
            errors.append("rule_application_missing_arguments")
        rule_ids = application.get("rule_ids")
        if not isinstance(rule_ids, list) or not rule_ids or any(not str(rule).startswith("full2d_rule:") for rule in rule_ids):
            errors.append("rule_application_bad_rule_ids")
        if application.get("target_fact") != target_fact(claim_spec):
            errors.append("rule_application_target_fact_mismatch")
        text = json.dumps(application, sort_keys=True).lower()
        if "exact " in text or " by " in text:
            errors.append("rule_application_contains_proof_text")
    return errors


def resolve_claim_path(
    run_dir: Path,
    provider_summary: dict[str, Any],
    artifact_paths: dict[str, Any],
    claim_ref: str,
    explicit: Path | None,
) -> Path | None:
    if explicit is not None:
        return resolve_path(explicit)
    path_value = artifact_paths.get(claim_ref) if claim_ref else None
    if isinstance(path_value, str):
        return resolve_artifact_path(run_dir, path_value)
    path_value = provider_summary.get("claim_spec_path")
    if isinstance(path_value, str):
        return resolve_artifact_path(run_dir, path_value)
    candidate = run_dir / "provider_stage" / "claim_spec.json"
    return candidate if candidate.exists() else None


def load_semantic_artifact(run_dir: Path, artifact_paths: dict[str, Any], ref: str) -> tuple[dict[str, Any] | None, list[str]]:
    path_value = artifact_paths.get(ref)
    if not isinstance(path_value, str):
        return None, [f"missing_artifact_path:{ref}"]
    path = resolve_artifact_path(run_dir, path_value)
    if not path.exists():
        return None, [f"artifact_path_not_found:{ref}"]
    payload = read_json(path)
    if not isinstance(payload, dict):
        return None, [f"artifact_not_object:{ref}"]
    semantic = strip_identity(payload)
    if sha256_text(canonical_json(semantic)) != ref:
        return semantic, [f"artifact_ref_hash_mismatch:{ref}"]
    return semantic, []


def write_report(path: Path, report: dict[str, Any]) -> tuple[str, Path]:
    ref = sha256_text(canonical_json(report))
    write_json(path, report)
    return ref, path


def strip_identity(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in IDENTITY_KEYS}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def resolve_artifact_path(run_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else run_dir / path


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def target_dict(claim_spec: dict[str, Any]) -> dict[str, Any]:
    target = claim_spec.get("target", {})
    return target if isinstance(target, dict) else {}


def target_family(claim_spec: dict[str, Any]) -> str:
    return str(target_dict(claim_spec).get("family", ""))


def target_args(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(item) for item in target_dict(claim_spec).get("args", ()))


def target_source_expr(claim_spec: dict[str, Any]) -> str:
    return str(target_dict(claim_spec).get("source_expr", "")).lower()


def target_fact(claim_spec: dict[str, Any]) -> str:
    return f"{target_family(claim_spec)}:{','.join(target_args(claim_spec))}:positive"


def hypothesis_fact_keys(claim_spec: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for item in claim_spec.get("hypotheses", ()):
        if isinstance(item, dict):
            args = ",".join(str(arg) for arg in item.get("args", ()))
            keys.add(f"{item.get('family')}:{args}:{item.get('polarity', 'positive')}")
    return keys


def point_object_ids(claim_spec: dict[str, Any]) -> list[str]:
    return [
        str(item["object_id"])
        for item in claim_spec.get("objects", ())
        if isinstance(item, dict) and item.get("kind") == "Point" and item.get("object_id")
    ]


def all_side_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    if not isinstance(buckets, dict):
        return ()
    collected: list[str] = []
    for values in buckets.values():
        if isinstance(values, (list, tuple)):
            collected.extend(str(item) for item in values)
    return tuple(collected)


def nondegeneracy_conditions(claim_spec: dict[str, Any]) -> tuple[str, ...]:
    buckets = claim_spec.get("side_conditions", {})
    values = buckets.get("nondegeneracy", ()) if isinstance(buckets, dict) else ()
    return tuple(str(item) for item in values) if isinstance(values, (list, tuple)) else ()


def has_repeated_point(args: tuple[str, ...]) -> bool:
    return len(args) >= 3 and (args[0] == args[1] or args[0] == args[2] or args[1] == args[2])


def is_collinear_reflexive_target(claim_spec: dict[str, Any]) -> bool:
    return target_family(claim_spec) in {"incidence", "collinear"} and len(target_args(claim_spec)) == 3 and has_repeated_point(target_args(claim_spec))


def hypothesis_with_args(claim_spec: dict[str, Any], token: str, args: tuple[str, ...]) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if isinstance(item, dict) and token in str(item.get("source_expr", "")).lower() and tuple(str(arg) for arg in item.get("args", ())) == args:
            return item
    return None


def has_midpoint_hypothesis(claim_spec: dict[str, Any], args: tuple[str, ...]) -> bool:
    return any(
        isinstance(item, dict)
        and "midpoint" in str(item.get("source_expr", "")).lower()
        and tuple(str(arg) for arg in item.get("args", ())) == args
        for item in claim_spec.get("hypotheses", ())
    )


def has_projection_hypothesis(claim_spec: dict[str, Any], kind: str, args: tuple[str, ...]) -> bool:
    tokens = {
        "circle_construction_projection": "circle_with_center_through_point",
        "line_circle_intersection_projection": "line_circle_intersection",
        "center_construction_projection": "constructed_center_point",
    }
    token = tokens.get(kind, "")
    return any(
        isinstance(item, dict)
        and token in str(item.get("source_expr", "")).lower()
        and tuple(str(arg) for arg in item.get("args", ())) == args
        for item in claim_spec.get("hypotheses", ())
    )


def has_nonzero_baseline(args: tuple[str, ...], side_conditions: tuple[str, ...]) -> bool:
    pairs = {(args[0], args[2]), (args[2], args[0]), (args[0], args[1]), (args[1], args[2])}
    compact_conditions = {condition.replace(" ", "") for condition in side_conditions}
    return any(f"{a}!={b}".replace(" ", "") in compact_conditions for a, b in pairs if a != b)


def equality_hypothesis(claim_spec: dict[str, Any], left: str, right: str) -> dict[str, Any] | None:
    for item in claim_spec.get("hypotheses", ()):
        if not isinstance(item, dict):
            continue
        source = str(item.get("source_expr", ""))
        if "=" not in source or "!=" in source or "!=" in source:
            continue
        if tuple(str(arg) for arg in item.get("args", ())) == (left, right):
            return item
    return None


def between_hypothesis(claim_spec: dict[str, Any], args: tuple[str, ...]) -> str | None:
    for item in claim_spec.get("hypotheses", ()):
        if isinstance(item, dict) and "between" in str(item.get("source_expr", "")).lower() and tuple(str(arg) for arg in item.get("args", ())) == args:
            return str(item.get("predicate_id", "hyp:between"))
    return None


def first_distinct_point_pair(side_conditions: tuple[str, ...]) -> tuple[str, str] | None:
    for condition in side_conditions:
        if "!=" not in condition:
            continue
        left, right = condition.split("!=", 1)
        left = left.strip()
        right = right.strip()
        if left and right and left != right:
            return (left, right)
    return None


def length_le_trans_hypotheses(claim_spec: dict[str, Any], target: tuple[str, ...]) -> tuple[dict[str, Any], dict[str, Any]] | None:
    candidates = [
        item
        for item in claim_spec.get("hypotheses", ())
        if isinstance(item, dict) and "length_le" in str(item.get("source_expr", "")).lower() and len(tuple(item.get("args", ()))) == 4
    ]
    for first in candidates:
        first_args = tuple(str(arg) for arg in first.get("args", ()))
        if first_args[:2] != target[:2]:
            continue
        for second in candidates:
            second_args = tuple(str(arg) for arg in second.get("args", ()))
            if first_args[2:] == second_args[:2] and second_args[2:] == target[2:]:
                return first, second
    return None


def portfolio_features(claim_spec: dict[str, Any]) -> dict[str, str]:
    side_count = len(all_side_conditions(claim_spec))
    object_count = len(claim_spec.get("objects", ())) if isinstance(claim_spec.get("objects", ()), (list, tuple)) else 0
    return {
        "target_family": target_family(claim_spec) or "unknown",
        "side_condition_count": str(side_count),
        "object_count": str(object_count),
        "has_claim_spec": "true",
    }


def portfolio_policy(features: dict[str, str]) -> tuple[tuple[str, ...], tuple[str, ...], tuple[tuple[str, ...], ...]]:
    if features["target_family"] in {"incidence", "collinear"}:
        order = (
            "synthetic_closure",
            "construction_search",
            "metric_angle",
            "algebraic_geometry",
            "transformation",
            "order_case",
            "inequality",
            "lean_proof_search",
            "portfolio_coordinator",
        )
        reasons = (
            "target_family:incidence_prefers_synthetic_first",
            "side_conditions:domain_engines_after_primary_trace",
            "proof_candidate:last_after_normalized_artifacts",
            "policy:no_llm_semantics",
        )
        return order, reasons, (("metric_angle", "algebraic_geometry"), ("transformation", "order_case", "inequality"))
    return ENGINE_ROLES, ("target_family:generic_full_order", "policy:no_llm_semantics"), (("synthetic_closure", "algebraic_geometry"),)
