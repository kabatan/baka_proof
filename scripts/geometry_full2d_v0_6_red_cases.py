from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RED_CASE_ROOT = ROOT / "tests" / "red_cases" / "geometry_full2d_v0_6"
RED_CASE_MANIFEST = RED_CASE_ROOT / "manifest.json"

REPORT_SCHEMA = "GeometryFull2DRedCaseReportV06"
MANIFEST_SCHEMA = "GeometryFull2DRedCaseManifestV06"
CHECKER_NAME = "check_red_case_suite_v0_6.py"


REQUIRED_CASES: dict[str, dict[str, Any]] = {
    "RC-001": {
        "fixture_name": "RedCase_TargetFactProvider",
        "failure_class": "Target-fact provider",
        "expected_K": ["K-007", "K-013"],
    },
    "RC-002": {
        "fixture_name": "RedCase_NakedTargetAssertion",
        "failure_class": "Naked target assertion",
        "expected_K": ["K-013"],
    },
    "RC-003": {
        "fixture_name": "RedCase_IdentityDirectRuleRegistry",
        "failure_class": "Identity/direct-rule registry",
        "expected_K": ["K-012"],
    },
    "RC-004": {
        "fixture_name": "RedCase_ProofFromShapeCompiler",
        "failure_class": "Proof-from-shape compiler",
        "expected_K": ["K-015", "K-016"],
    },
    "RC-005": {
        "fixture_name": "RedCase_RuleListArtifactSynthesis",
        "failure_class": "Rule-list artifact synthesis",
        "expected_K": ["K-011"],
    },
    "RC-006": {
        "fixture_name": "RedCase_ReportOnlyCausality",
        "failure_class": "Report-only causality",
        "expected_K": ["K-018", "K-019"],
    },
    "RC-007": {
        "fixture_name": "RedCase_FamilyCodedBaseline",
        "failure_class": "Family-coded baseline",
        "expected_K": ["K-025", "K-030"],
    },
    "RC-008": {
        "fixture_name": "RedCase_ProjectionBenchmark",
        "failure_class": "Projection benchmark",
        "expected_K": ["K-020", "K-021"],
    },
    "RC-009": {
        "fixture_name": "RedCase_CheckerOmission",
        "failure_class": "Checker omission",
        "expected_K": ["K-004", "K-035"],
    },
    "RC-010": {
        "fixture_name": "RedCase_CheckerWhitelist",
        "failure_class": "Checker whitelist",
        "expected_K": ["K-005"],
    },
    "RC-011": {
        "fixture_name": "RedCase_SealedChallengeCollusion",
        "failure_class": "Sealed challenge collusion",
        "expected_K": ["K-022"],
    },
    "RC-012": {
        "fixture_name": "RedCase_StaleEvidenceReplay",
        "failure_class": "Stale evidence replay",
        "expected_K": ["K-006", "K-031"],
    },
    "RC-013": {
        "fixture_name": "RedCase_RuleHack",
        "failure_class": "Rule hack",
        "expected_K": ["K-012", "K-029"],
    },
    "RC-014": {
        "fixture_name": "RedCase_TargetAsCertificate",
        "failure_class": "Target-as-certificate",
        "expected_K": ["K-009", "K-013"],
    },
    "RC-015": {
        "fixture_name": "RedCase_CheckerGeneratedSuccessArtifacts",
        "failure_class": "Checker-generated success artifacts",
        "expected_K": ["K-034"],
    },
    "RC-016": {
        "fixture_name": "RedCase_StaticOnlyGreenRelease",
        "failure_class": "Static-only green release",
        "expected_K": ["K-006", "K-018", "K-024", "K-034", "K-035"],
    },
    "RC-017": {
        "fixture_name": "RedCase_B2OnlyMatrix",
        "failure_class": "B2-only matrix",
        "expected_K": ["K-024"],
    },
    "RC-018": {
        "fixture_name": "RedCase_DirectLemmaWrappedAsIntermediate",
        "failure_class": "Direct lemma wrapped as intermediate",
        "expected_K": ["K-013", "K-027"],
    },
    "RC-019": {
        "fixture_name": "RedCase_ProviderImportsCompiler",
        "failure_class": "Provider imports compiler",
        "expected_K": ["K-008"],
    },
    "K-010": {
        "fixture_name": "EngineOutputContainsProofText",
        "failure_class": "Engine output contains proof text",
        "expected_K": ["K-010"],
    },
    "K-013": {
        "fixture_name": "TargetEquivalentIntermediate",
        "failure_class": "Target-equivalent intermediate",
        "expected_K": ["K-013"],
    },
    "K-028": {
        "fixture_name": "NarrowEngineRoleSet",
        "failure_class": "Narrow engine role set",
        "expected_K": ["K-028"],
    },
}


STATIC_PATTERNS: dict[str, re.Pattern[str]] = {
    "K-004": re.compile(r"missing_k_coverage|checker_coverage_matrix\s*=\s*\{\}|omitted_checker", re.DOTALL),
    "K-005": re.compile(r"whitelist|allowlist|suppress.*forbidden|if\s+.*(filename|path|directory|role).*:\s*(return|continue|pass)", re.IGNORECASE | re.DOTALL),
    "K-006": re.compile(r"stale_evidence|static_only_release|current_git_head_bound\s*=\s*False", re.DOTALL),
    "K-007": re.compile(r"target_fact_with_empty_premises|premises\s*=\s*\[\]|selected_fact_is_final_target", re.DOTALL),
    "K-008": re.compile(r"provider_imports_compiler|from\s+.*(compiler|rule_registry|proof_worker|final_verify|matrix|release).*import|import\s+.*(compiler|rule_registry|proof_worker|final_verify|matrix|release)", re.DOTALL),
    "K-009": re.compile(r"target_as_certificate|certificate_is_target|certificate_payload\s*=\s*target|target_hash_certificate", re.DOTALL),
    "K-010": re.compile(r"engine_output_contains_proof_text|proof_text_present|tactic_script|lean_lemma_template_id|proof_replacement_text|exact\s+|by\s+", re.DOTALL),
    "K-011": re.compile(r"rule_list_artifact_synthesis|compiler_selected_rule_list|used_rules_as_engine_artifact|engine_output_from_rule_registry", re.DOTALL),
    "K-012": re.compile(r"identity_direct_rule|direct_facade_rule|alias_inflation|unchecked_rule|fake_broad_family|rule_checker_without_premises", re.DOTALL),
    "K-013": re.compile(r"naked_target_assertion|target_equivalent_intermediate|alpha_renamed_target|target_hash_intermediate|trivial_target_wrapper|direct_facade_target|selected_derivation_only_final_target", re.DOTALL),
    "K-015": re.compile(r"compiler_uses_forbidden_input|compile_from_theorem_anchor|compile_from_target_shape|compile_from_statement_hash|target_expr|theorem_name|statement_hash|proof_region_identity|binder_map_identity", re.DOTALL),
    "K-016": re.compile(r"proof_from_shape|proof_from_family|proof_from_target_shape|proof_from_anchor_identifier|target_shape_id|theorem_family|template_id|difficulty_tier|source_ref", re.DOTALL),
    "K-018": re.compile(r"report_only_causality|no_live_rerun_logs|field_only_causality|final_verify_rerun_logs_missing", re.DOTALL),
    "K-019": re.compile(r"mutation_sensitivity_missing|destructive_causality_passed\s*=\s*False|mutation_same_final_theorem", re.DOTALL),
    "K-020": re.compile(r"projection_counted_positive|projection_task_release_positive|ExternalGoalPreserved.*projection", re.DOTALL),
    "K-021": re.compile(r"self_attested_goal_preservation|source_ref_only_goal_preservation|point_predicate_reuse_only", re.DOTALL),
    "K-022": re.compile(r"sealed_generator_imports_implementation|sealed_generator_reads_run_record|emits_expected_rule_labels|sealed_challenge_collusion", re.DOTALL),
    "K-024": re.compile(r"b2_only_matrix|missing_required_baselines|materialized_from_b2_cache|static_only_release", re.DOTALL),
    "K-025": re.compile(r"family_coded_baseline|baseline_outcome_from_family|baseline_outcome_from_category|hard_coded_baseline_id", re.DOTALL),
    "K-027": re.compile(r"direct_facade_lemma_fraction_too_high|success_threshold_satisfied_by_direct_lemma|direct_lemma_wrapped_as_intermediate", re.DOTALL),
    "K-028": re.compile(r"narrow_engine_role_set|posthoc_enabled_engine_roles|omits_release_critical_role|role_set_after_provider_success", re.DOTALL),
    "K-029": re.compile(r"rule_hack|fake_broad_family|alias_family_counts|unchecked_rule_counts|non_mutation_sensitive_rule", re.DOTALL),
    "K-030": re.compile(r"label_coded_baseline_failure|family_coded_baseline|baseline_result_from_label", re.DOTALL),
    "K-031": re.compile(r"stale_evidence_replay|previous_release_evidence|run_dir_hash_unbound|checker_hash_set_unbound", re.DOTALL),
    "K-034": re.compile(r"checker_generated_success_artifacts|fabricated_pipeline_success|checker_creates_final_verify_success|static_only_release", re.DOTALL),
    "K-035": re.compile(r"checker_omission|missing_required_checker|required_checker_absent|static_only_release", re.DOTALL),
}


PAYLOAD_FLAGS: dict[str, tuple[str, ...]] = {
    "missing_k_coverage": ("K-004",),
    "omitted_checker": ("K-004", "K-035"),
    "checker_whitelist": ("K-005",),
    "suppressed_forbidden_shortcut": ("K-005",),
    "stale_evidence": ("K-006", "K-031"),
    "current_git_head_bound_false": ("K-006",),
    "selected_fact_is_final_target": ("K-007",),
    "target_fact_with_empty_premises": ("K-007", "K-013"),
    "provider_imports_compiler": ("K-008",),
    "imports_downstream_module": ("K-008",),
    "target_as_certificate": ("K-009", "K-013"),
    "certificate_is_target": ("K-009", "K-013"),
    "proof_text_present": ("K-010",),
    "tactic_script_present": ("K-010",),
    "rule_list_artifact_synthesis": ("K-011",),
    "engine_output_from_compiler_selected_rules": ("K-011",),
    "identity_direct_rule": ("K-012",),
    "direct_facade_rule": ("K-012", "K-013", "K-027"),
    "alias_inflation": ("K-012", "K-029"),
    "unchecked_rule": ("K-012", "K-029"),
    "naked_target_assertion": ("K-013",),
    "target_equivalent_intermediate": ("K-013",),
    "alpha_renamed_target": ("K-013",),
    "target_hash_intermediate": ("K-013",),
    "trivial_target_wrapper": ("K-013",),
    "compiler_uses_forbidden_input": ("K-015", "K-016"),
    "proof_from_shape": ("K-015", "K-016"),
    "uses_theorem_anchor_identifier": ("K-015", "K-016"),
    "report_only_causality": ("K-018", "K-019"),
    "no_live_rerun_logs": ("K-018",),
    "mutation_sensitivity_missing": ("K-019",),
    "projection_counted_positive": ("K-020",),
    "self_attested_goal_preservation": ("K-021",),
    "sealed_generator_imports_implementation": ("K-022",),
    "sealed_generator_reads_run_record": ("K-022",),
    "emits_expected_rule_labels": ("K-022",),
    "b2_only_matrix": ("K-024",),
    "missing_required_baselines": ("K-024",),
    "materialized_from_b2_cache": ("K-024",),
    "family_coded_baseline": ("K-025", "K-030"),
    "baseline_outcome_from_family": ("K-025", "K-030"),
    "direct_lemma_wrapped_as_intermediate": ("K-013", "K-027"),
    "fake_broad_family": ("K-012", "K-029"),
    "posthoc_enabled_engine_roles": ("K-028",),
    "omits_release_critical_role": ("K-028",),
    "narrow_engine_role_set": ("K-028",),
    "checker_generated_success_artifacts": ("K-034",),
    "fabricated_pipeline_success": ("K-034",),
    "static_only_release": ("K-006", "K-018", "K-024", "K-034", "K-035"),
}


FORBIDDEN_PROVIDER_IMPORT_PARTS = (
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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_json(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _walk(value: Any) -> list[Any]:
    seen = [value]
    if isinstance(value, dict):
        for item in value.values():
            seen.extend(_walk(item))
    elif isinstance(value, list):
        for item in value:
            seen.extend(_walk(item))
    return seen


def _walk_items(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_walk_items(item))
    elif isinstance(value, list):
        for item in value:
            items.extend(_walk_items(item))
    return items


def detect_static_code(text: str) -> set[str]:
    return {kid for kid, pattern in STATIC_PATTERNS.items() if pattern.search(text)}


def detect_artifact_payload(payload: dict[str, Any]) -> set[str]:
    blockers: set[str] = set()
    text = json.dumps(payload, sort_keys=True)
    blockers.update(detect_static_code(text))

    for key, value in _walk_items(payload):
        normalized_key = key.lower()
        if value is True and normalized_key in PAYLOAD_FLAGS:
            blockers.update(PAYLOAD_FLAGS[normalized_key])
        if normalized_key == "red_case_markers" and isinstance(value, list):
            for marker in value:
                blockers.update(PAYLOAD_FLAGS.get(str(marker).lower(), ()))
        if normalized_key == "imports" and isinstance(value, list):
            import_text = " ".join(str(item) for item in value).lower()
            if any(part in import_text for part in FORBIDDEN_PROVIDER_IMPORT_PARTS):
                blockers.add("K-008")
        if normalized_key == "selected_facts" and isinstance(value, list):
            for fact in value:
                if not isinstance(fact, dict):
                    continue
                is_target = fact.get("is_final_target") is True or fact.get("conclusion") == "FINAL_TARGET"
                if is_target and fact.get("premises") == []:
                    blockers.update({"K-007", "K-013"})
        if normalized_key in {"proof", "proof_text", "tactic_script", "proof_replacement_text"} and value:
            blockers.add("K-010")
        if normalized_key in {"certificate_payload", "certificate"}:
            if isinstance(value, dict) and (
                value.get("kind") in {"target_statement", "target_hash", "target_expr", "schema_normalized_target"}
                or value.get("payload") in {"FINAL_TARGET", "target_hash", "target_expr"}
            ):
                blockers.update({"K-009", "K-013"})

    for value in _walk(payload):
        if isinstance(value, str) and re.search(r"\b(exact|by|rw)\b", value):
            blockers.add("K-010")

    return blockers


def detect_variant(variant: dict[str, Any]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    kind = variant.get("kind")
    if kind == "static-code":
        return detect_static_code(str(variant.get("code", ""))), errors
    if kind == "artifact-run":
        payload = variant.get("payload")
        if not isinstance(payload, dict):
            errors.append("artifact-run payload is missing or not an object")
            return set(), errors
        return detect_artifact_payload(payload), errors
    errors.append(f"unknown variant kind: {kind}")
    return set(), errors


def load_manifest() -> dict[str, Any]:
    if not RED_CASE_MANIFEST.exists():
        return {"schema_version": MANIFEST_SCHEMA, "fixtures": []}
    return read_json(RED_CASE_MANIFEST)


def _validate_fixture_shape(fixture: dict[str, Any], required: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if fixture.get("fixture_name") != required["fixture_name"]:
        errors.append("fixture_name mismatch")
    if fixture.get("failure_class") != required["failure_class"]:
        errors.append("failure_class mismatch")
    if sorted(fixture.get("expected_K", [])) != sorted(required["expected_K"]):
        errors.append("expected_K mismatch")
    if not fixture.get("variants"):
        errors.append("missing variants")
    if not isinstance(fixture.get("positive_control"), dict):
        errors.append("missing positive_control")
    return errors


def evaluate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    case_id = str(fixture.get("red_case_id", ""))
    required = REQUIRED_CASES.get(case_id, {})
    errors = _validate_fixture_shape(fixture, required) if required else ["unknown red_case_id"]
    expected = set(required.get("expected_K", []))
    detected: set[str] = set()
    variant_results: list[dict[str, Any]] = []

    for index, variant in enumerate(fixture.get("variants", []), start=1):
        blockers, variant_errors = detect_variant(variant)
        detected.update(blockers)
        variant_results.append(
            {
                "variant_index": index,
                "kind": variant.get("kind"),
                "detected_K": sorted(blockers),
                "errors": variant_errors,
            }
        )
        errors.extend(f"variant_{index}:{error}" for error in variant_errors)

    positive_control = fixture.get("positive_control", {})
    positive_blockers, positive_errors = detect_variant(positive_control)
    positive_control_passed = not (positive_blockers & expected) and not positive_errors
    if not positive_control_passed:
        errors.append("positive_control_failed")

    missing_expected = sorted(expected - detected)
    if missing_expected:
        errors.append("missing_expected_K:" + ",".join(missing_expected))

    observed_failure = not missing_expected and not errors
    evidence_hash = sha256_json(
        {
            "fixture": fixture,
            "detected": sorted(detected),
            "positive_blockers": sorted(positive_blockers),
        }
    )
    return {
        "red_case_id": case_id,
        "fixture_name": fixture.get("fixture_name"),
        "failure_class": fixture.get("failure_class"),
        "fixture_path": f"{RED_CASE_MANIFEST.relative_to(ROOT).as_posix()}#{case_id}",
        "expected_K": sorted(expected),
        "detected_K": sorted(detected),
        "missing_expected_K": missing_expected,
        "observed_failure": observed_failure,
        "checker_name": CHECKER_NAME,
        "evidence_ref": f"sha256:{evidence_hash}",
        "positive_control_passed": positive_control_passed,
        "positive_control_detected_K": sorted(positive_blockers),
        "variant_results": variant_results,
        "errors": errors,
    }


def run_red_case_suite() -> dict[str, Any]:
    manifest = load_manifest()
    fixtures = manifest.get("fixtures", [])
    errors: list[str] = []
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        errors.append("manifest_schema_mismatch")
    if not isinstance(fixtures, list):
        errors.append("fixtures_not_list")
        fixtures = []

    fixture_ids = [str(fixture.get("red_case_id", "")) for fixture in fixtures if isinstance(fixture, dict)]
    expected_ids = list(REQUIRED_CASES)
    missing = sorted(set(expected_ids) - set(fixture_ids))
    extra = sorted(set(fixture_ids) - set(expected_ids))
    duplicate = sorted({case_id for case_id in fixture_ids if fixture_ids.count(case_id) > 1})
    if missing:
        errors.append("missing_fixtures:" + ",".join(missing))
    if extra:
        errors.append("unknown_fixtures:" + ",".join(extra))
    if duplicate:
        errors.append("duplicate_fixtures:" + ",".join(duplicate))

    results = [evaluate_fixture(fixture) for fixture in fixtures if isinstance(fixture, dict)]
    failed = [result["red_case_id"] for result in results if not result["observed_failure"]]
    if failed:
        errors.append("fixtures_not_rejected:" + ",".join(sorted(failed)))

    positive_failed = [result["red_case_id"] for result in results if not result["positive_control_passed"]]
    if positive_failed:
        errors.append("positive_controls_failed:" + ",".join(sorted(positive_failed)))

    report = {
        "schema_version": REPORT_SCHEMA,
        "checker_name": CHECKER_NAME,
        "manifest_path": RED_CASE_MANIFEST.relative_to(ROOT).as_posix(),
        "status": "passed" if not errors else "failed",
        "all_rejected": not errors,
        "red_case_count": len(results),
        "expected_red_case_count": len(REQUIRED_CASES),
        "errors": errors,
        "red_cases": results,
    }
    report["evidence_ref"] = "sha256:" + sha256_json(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate GeometryFull2D v0.6 red-case fixtures.")
    parser.add_argument("--all", action="store_true", help="Require all v0.6 red and K-level fixtures.")
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args(argv)
    if not args.all:
        print("error: --all is required for WP01 acceptance", file=sys.stderr)
        return 2

    report = run_red_case_suite()
    if args.output:
        write_json(args.output if args.output.is_absolute() else ROOT / args.output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
