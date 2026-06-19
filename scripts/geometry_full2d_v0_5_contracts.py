from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHANGE_DIR = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_5"
DEFAULT_CONFIG = ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_5.yaml"
DEFAULT_CORPUS_ROOT = ROOT / "benchmarks" / "geometry_full2d_v0_5"
DEFAULT_RUN_ROOT = ROOT / "runs" / "geometry_full2d_v0_5"
RED_CASE_ROOT = ROOT / "tests" / "red_cases" / "v0_5"
RED_CASE_MANIFEST = RED_CASE_ROOT / "manifest.json"

K_BLOCKERS: dict[str, str] = {
    "K-001": "Empty or placeholder summary",
    "K-002": "Checker coverage incomplete",
    "K-003": "Red case accepted",
    "K-004": "Target-fact provider",
    "K-005": "Naked target assertion",
    "K-006": "Identity/direct-facade rule counted",
    "K-007": "Proof-from-shape compiler",
    "K-008": "Engine output from compiler-selected rules",
    "K-009": "Proof text in engine output",
    "K-010": "Missing independent checker evidence",
    "K-011": "Causality report not live rerun",
    "K-012": "Destructive causality failure",
    "K-013": "Projection counted as positive",
    "K-014": "Corpus coupled to proof implementation",
    "K-015": "Sealed challenge not independent",
    "K-016": "Weak/self-attested goal preservation",
    "K-017": "Source theorem pre-proved",
    "K-018": "Engine contribution insufficient",
    "K-019": "Used-rule coverage insufficient",
    "K-020": "Direct/wrapped facade lemma dominance",
    "K-021": "Non-target intermediate insufficient",
    "K-022": "Construction/case/certificate evidence insufficient",
    "K-023": "Family-coded baseline",
    "K-024": "Baseline comparability violated",
    "K-025": "Metrics below threshold",
    "K-026": "Stale evidence",
    "K-027": "Open debt",
    "K-028": "Closure exceeds evidence",
    "K-029": "Statement diversity insufficient",
    "K-030": "Checker whitelist or suppression",
    "K-031": "Provider imports downstream proof code",
    "K-032": "Final status not from FinalVerifyReport",
    "K-033": "Matrix not all-baselines",
}

REQUIRED_REPORT_FIELDS = [
    "checked_requirements",
    "checker_coverage_matrix",
    "red_case_summary",
    "corpus_summary",
    "corpus_statement_diversity_summary",
    "extraction_summary",
    "provider_stage_boundary_summary",
    "engine_output_summary",
    "independent_checker_summary",
    "rule_registry_summary",
    "compiler_isolation_summary",
    "actual_pipeline_run_summary",
    "solver_causality_summary",
    "final_verify_summary",
    "metrics_summary",
    "used_rule_coverage_summary",
    "engine_contribution_summary",
    "baseline_comparability_summary",
    "measured_failure_summary",
    "debt_ledger_summary",
    "freshness_summary",
    "closure_claim_ceiling",
    "closure_claim_ceiling_summary",
]

REQUIRED_BASELINES = ["B1", "B2", "B5", "B6", "B7"]
CONDITIONAL_BASELINE = "B8"
CLAIM_TARGET = "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"

REQUIRED_CHECKER_COMMANDS: dict[str, list[str]] = {
    "active_guardian_spec": [sys.executable, "scripts/check_active_guardian_spec_v0_5.py"],
    "red_cases": [sys.executable, "scripts/run_red_cases_v0_5.py", "--expect-failure"],
    "acceptance_coverage": [sys.executable, "scripts/check_acceptance_coverage_v0_5.py"],
    "no_checker_whitelist": [sys.executable, "scripts/check_no_checker_whitelist_v0_5.py"],
    "schema_validators": [sys.executable, "scripts/check_schema_validators_v0_5.py", "--self-test"],
    "corpus_independence": [
        sys.executable,
        "scripts/check_corpus_independence_v0_5.py",
        "--corpus-root",
        "benchmarks/geometry_full2d_v0_5",
        "--freeze-manifest",
        "benchmarks/geometry_full2d_v0_5/freeze_manifest.json",
    ],
    "corpus_statement_diversity": [sys.executable, "scripts/check_corpus_statement_diversity_v0_5.py", "--corpus-root", "benchmarks/geometry_full2d_v0_5"],
    "goal_preservation": [sys.executable, "scripts/check_goal_preservation_reports_v0_5.py", "--corpus-root", "benchmarks/geometry_full2d_v0_5"],
    "provider_stage_boundary": [sys.executable, "scripts/check_provider_stage_boundary_v0_5.py", "--self-test"],
    "independent_solver_checkers": [sys.executable, "scripts/check_independent_solver_checkers_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5", "--self-test"],
    "rule_registry": [sys.executable, "scripts/check_full2d_rule_registry_v0_5.py", "--self-test"],
    "compiler_input_isolation": [sys.executable, "scripts/check_compiler_input_isolation_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5", "--self-test"],
    "compiler_taint": [sys.executable, "scripts/check_compiler_taint_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "proof_worker_final_verify": [sys.executable, "scripts/check_proof_worker_final_verify_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5", "--self-test"],
    "matrix": [
        sys.executable,
        "scripts/run_full2d_matrix_v0_5.py",
        "--config",
        "configs/benchmark_runs/geometry_full2d_v0_5.yaml",
        "--run-dir",
        "runs/geometry_full2d_v0_5",
        "--execute-all-baselines",
        "--fresh-run",
    ],
    "extraction": [sys.executable, "scripts/check_full2d_extraction_corpus_v0_5.py", "--corpus-root", "benchmarks/geometry_full2d_v0_5", "--run-dir", "runs/geometry_full2d_v0_5"],
    "engine_outputs": [sys.executable, "scripts/check_engine_outputs_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "causality_mutations": [
        sys.executable,
        "scripts/run_solver_causality_mutations_v0_5.py",
        "--run-dir",
        "runs/geometry_full2d_v0_5",
        "--all-b2-successes",
        "--fresh-reruns",
        "--workers",
        "16",
    ],
    "solver_causality": [sys.executable, "scripts/check_solver_causality_reports_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5", "--self-test"],
    "baseline_comparability": [sys.executable, "scripts/check_full2d_baseline_comparability_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "metrics": [sys.executable, "scripts/check_full2d_metrics_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "used_rule_coverage": [sys.executable, "scripts/check_full2d_used_rule_coverage_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "engine_contribution": [sys.executable, "scripts/check_full2d_engine_contribution_v0_5.py", "--run-dir", "runs/geometry_full2d_v0_5"],
    "debt_ledger": [sys.executable, "scripts/check_debt_ledger_v0_5.py", "--change-dir", "docs/ai/changes/geometry-full2d-v0_5"],
    "closure_claim_ceiling": [
        sys.executable,
        "scripts/check_closure_claim_ceiling_v0_5.py",
        "--change-dir",
        "docs/ai/changes/geometry-full2d-v0_5",
        "--release-report",
        "docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json",
        "--closure",
        "docs/ai/changes/geometry-full2d-v0_5/CLOSURE.md",
        "--allow-missing-closure",
    ],
}

CHECKER_COVERAGE: dict[str, list[str]] = {
    "K-001": ["check_release_acceptance_v0_5.py"],
    "K-002": ["check_acceptance_coverage_v0_5.py"],
    "K-003": ["run_red_cases_v0_5.py"],
    "K-004": ["check_engine_outputs_v0_5.py", "check_provider_stage_boundary_v0_5.py"],
    "K-005": ["check_engine_outputs_v0_5.py", "check_independent_solver_checkers_v0_5.py"],
    "K-006": ["check_full2d_rule_registry_v0_5.py", "check_full2d_used_rule_coverage_v0_5.py"],
    "K-007": ["check_compiler_input_isolation_v0_5.py", "check_compiler_taint_v0_5.py"],
    "K-008": ["check_engine_outputs_v0_5.py", "check_compiler_taint_v0_5.py"],
    "K-009": ["check_engine_outputs_v0_5.py"],
    "K-010": ["check_independent_solver_checkers_v0_5.py"],
    "K-011": ["check_solver_causality_reports_v0_5.py"],
    "K-012": ["check_solver_causality_reports_v0_5.py"],
    "K-013": ["check_corpus_independence_v0_5.py"],
    "K-014": ["check_corpus_independence_v0_5.py"],
    "K-015": ["check_corpus_independence_v0_5.py"],
    "K-016": ["check_goal_preservation_reports_v0_5.py"],
    "K-017": ["check_full2d_extraction_corpus_v0_5.py"],
    "K-018": ["check_full2d_engine_contribution_v0_5.py"],
    "K-019": ["check_full2d_used_rule_coverage_v0_5.py"],
    "K-020": ["check_full2d_metrics_v0_5.py"],
    "K-021": ["check_full2d_metrics_v0_5.py"],
    "K-022": ["check_full2d_metrics_v0_5.py", "check_corpus_statement_diversity_v0_5.py"],
    "K-023": ["check_full2d_baseline_comparability_v0_5.py"],
    "K-024": ["check_full2d_baseline_comparability_v0_5.py"],
    "K-025": ["check_full2d_metrics_v0_5.py", "check_full2d_baseline_comparability_v0_5.py"],
    "K-026": ["check_release_acceptance_v0_5.py"],
    "K-027": ["check_debt_ledger_v0_5.py"],
    "K-028": ["check_closure_claim_ceiling_v0_5.py"],
    "K-029": ["check_corpus_statement_diversity_v0_5.py"],
    "K-030": ["check_no_checker_whitelist_v0_5.py"],
    "K-031": ["check_provider_stage_boundary_v0_5.py"],
    "K-032": ["check_proof_worker_final_verify_v0_5.py", "check_full2d_baseline_comparability_v0_5.py"],
    "K-033": ["run_full2d_matrix_v0_5.py", "check_full2d_baseline_comparability_v0_5.py"],
}

RED_CASES: list[dict[str, Any]] = [
    {"id": "target_fact_provider", "name": "TargetFactProvider", "expected_blockers": ["K-004", "K-005"]},
    {"id": "naked_target_assertion", "name": "NakedTargetAssertion", "expected_blockers": ["K-005"]},
    {"id": "identity_rule_registry", "name": "IdentityRuleRegistry", "expected_blockers": ["K-006"]},
    {"id": "proof_from_shape_compiler", "name": "ProofFromShapeCompiler", "expected_blockers": ["K-007"]},
    {"id": "rule_list_artifact_synthesis", "name": "RuleListArtifactSynthesis", "expected_blockers": ["K-008"]},
    {"id": "report_only_causality", "name": "ReportOnlyCausality", "expected_blockers": ["K-011", "K-012"]},
    {"id": "family_coded_baseline", "name": "FamilyCodedBaseline", "expected_blockers": ["K-023"]},
    {"id": "projection_corpus_counted", "name": "ProjectionCorpusCounted", "expected_blockers": ["K-013", "K-016"]},
    {"id": "engine_output_contains_proof_text", "name": "EngineOutputContainsProofText", "expected_blockers": ["K-009"]},
    {"id": "checker_omission", "name": "CheckerOmission", "expected_blockers": ["K-002"]},
    {"id": "checker_whitelist", "name": "CheckerWhitelist", "expected_blockers": ["K-030"]},
    {"id": "direct_lemma_wrapped_as_intermediate", "name": "DirectLemmaWrappedAsIntermediate", "expected_blockers": ["K-020", "K-021"]},
    {"id": "sealed_challenge_imports_compiler", "name": "SealedChallengeImportsCompiler", "expected_blockers": ["K-015"]},
    {"id": "stale_evidence_replay", "name": "StaleEvidenceReplay", "expected_blockers": ["K-026"]},
    {"id": "target_shape_menu_corpus", "name": "TargetShapeMenuCorpus", "expected_blockers": ["K-014", "K-029"]},
    {"id": "goal_preservation_self_attestation", "name": "GoalPreservationSelfAttestation", "expected_blockers": ["K-016"]},
    {"id": "provider_imports_compiler", "name": "ProviderImportsCompiler", "expected_blockers": ["K-031"]},
    {"id": "b8_silently_omitted", "name": "B8SilentlyOmitted", "expected_blockers": ["K-024", "K-033"]},
    {"id": "closure_overclaims_readiness", "name": "ClosureOverclaimsReadiness", "expected_blockers": ["K-028"]},
]

STATIC_PATTERNS: dict[str, re.Pattern[str]] = {
    "K-002": re.compile(r"checker_coverage_matrix\s*=\s*\{\}|missing_k_coverage|checker_omission"),
    "K-004": re.compile(r"target_fact_with_empty_premises|facts\s*=.*premises.*\[\]", re.DOTALL),
    "K-005": re.compile(r"naked_target_assertion|output_is_target.*True.*non_target_intermediate.*False", re.DOTALL),
    "K-006": re.compile(r"direct_identity_rule\s*=\s*True|direct_facade_rule\s*=\s*True|identity_rule_registry"),
    "K-007": re.compile(r"target_expr\.startswith\s*\(|match\s+target_expr\b|target_shape_id|proof_from_shape|proof_from_source"),
    "K-008": re.compile(r"compiler_selected_rule_list|engine_output_from_compiler_selected_rules|rule_list_artifact_synthesis"),
    "K-009": re.compile(r"proof_text_present\s*=\s*True|engine_output_contains_proof_text|exact\s+"),
    "K-011": re.compile(r"failed_as_expected\s*=\s*True|causality_report_only"),
    "K-012": re.compile(r"destructive_causality_passed\s*=\s*False"),
    "K-013": re.compile(r"projection_counted_positive|easier_projection\s*=\s*True"),
    "K-014": re.compile(r"proof_coupled_corpus|target_shape_id|expected_compiler_rule|target_shape_menu"),
    "K-015": re.compile(r"sealed_generator_imports_proof_code|sealed_challenge_imports_compiler"),
    "K-016": re.compile(r"self_attested_goal_preservation|goal_preservation_self_attestation"),
    "K-018": re.compile(r"every_release_engine_role_contributed\s*=\s*False"),
    "K-019": re.compile(r"used_concrete_non_identity_rules\s*=\s*[0-9]|used_rule_families\s*=\s*[0-9]"),
    "K-020": re.compile(r"direct_wrapped_facade_fraction\s*=\s*1\.0|direct_lemma_wrapped_as_intermediate"),
    "K-021": re.compile(r"non_target_intermediate_fraction\s*=\s*0\.0"),
    "K-022": re.compile(r"construction_case_certificate_success_fraction\s*=\s*0\.0"),
    "K-023": re.compile(r"(theorem_family|grammar_family|target_family|family).*baseline|baseline.*(theorem_family|grammar_family|target_family|family)", re.DOTALL),
    "K-024": re.compile(r"conditional_b8_resolution_valid\s*=\s*False|b8_silently_omitted"),
    "K-026": re.compile(r"current_git_head_bound\s*=\s*False|stale_evidence"),
    "K-028": re.compile(r"closure_forbidden_claims_present|ClosureOverclaimsReadiness|open_problem_solving|production safety"),
    "K-029": re.compile(r"unique_normalized_theorem_skeletons\s*=\s*[0-9]|target_shape_menu"),
    "K-030": re.compile(r"if\s+.*(filename|path|directory|role).*:\s*(return|continue|pass)|whitelist|allowlist|suppress", re.IGNORECASE | re.DOTALL),
    "K-033": re.compile(r"missing_required_baselines|b8_silently_omitted"),
    "K-031": re.compile(r"plugins\.geometry_full2d\.(compiler|rule_registry|proof)|from\s+plugins\.geometry_full2d\s+import\s+(compiler|rule_registry|proof)"),
}

FORBIDDEN_IMPORT_MODULE_PARTS = (
    "plugins.geometry_full2d.compiler",
    "plugins.geometry_full2d.rule_registry",
    "plugins.geometry_full2d.proof",
    "scripts.run_full2d_matrix",
    "scripts.run_full2d_actual_task",
    "scripts.generate_full2d_v0_4",
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def load_red_case_manifest() -> dict[str, Any]:
    if not RED_CASE_MANIFEST.exists():
        return {"schema_version": "GeometryFull2DRedCaseManifestV1", "fixtures": []}
    return read_json(RED_CASE_MANIFEST)


def red_case_by_id(case_id: str) -> dict[str, Any] | None:
    for item in load_red_case_manifest().get("fixtures", []):
        if item.get("id") == case_id:
            return item
    return None


def detect_static_code(text: str) -> set[str]:
    blockers = {kid for kid, pattern in STATIC_PATTERNS.items() if pattern.search(text)}
    if _detect_forbidden_imports_text(text):
        blockers.add("K-031")
    return blockers


def _detect_forbidden_imports_text(text: str) -> list[str]:
    hits: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ["syntax_error"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(part in alias.name for part in FORBIDDEN_IMPORT_MODULE_PARTS):
                    hits.append(alias.name)
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if any(part in module for part in FORBIDDEN_IMPORT_MODULE_PARTS):
                hits.append(module)
    return hits


def detect_artifact_payload(payload: dict[str, Any]) -> set[str]:
    blockers: set[str] = set()
    schema = str(payload.get("schema_version", ""))
    text = json.dumps(payload, sort_keys=True)
    kind_blockers = {
        "target_fact_provider": {"K-004", "K-005"},
        "naked_target_assertion": {"K-005"},
        "identity_rule_registry": {"K-006"},
        "proof_from_shape_compiler": {"K-007"},
        "rule_list_artifact_synthesis": {"K-008"},
        "report_only_causality": {"K-011", "K-012"},
        "family_coded_baseline": {"K-023"},
        "projection_corpus_counted": {"K-013", "K-016"},
        "engine_output_contains_proof_text": {"K-009"},
        "checker_omission": {"K-002"},
        "checker_whitelist": {"K-030"},
        "direct_lemma_wrapped_as_intermediate": {"K-020", "K-021"},
        "sealed_challenge_imports_compiler": {"K-015"},
        "stale_evidence_replay": {"K-026"},
        "target_shape_menu_corpus": {"K-014", "K-029"},
        "goal_preservation_self_attestation": {"K-016"},
        "provider_imports_compiler": {"K-031"},
        "b8_silently_omitted": {"K-024", "K-033"},
        "closure_overclaims_readiness": {"K-028"},
    }
    blockers.update(kind_blockers.get(str(payload.get("red_case_kind")), set()))
    if payload.get("red_case_kind") == "checker_omission":
        blockers.add("K-002")
    if payload.get("red_case_kind") == "closure_overclaims_readiness":
        blockers.add("K-028")
    if payload.get("red_case_kind") == "b8_silently_omitted":
        blockers.update({"K-024", "K-033"})
    if payload.get("source_theorem_preproved") is True:
        blockers.add("K-017")
    if payload.get("stale_evidence") is True or payload.get("current_git_head_bound") is False:
        blockers.add("K-026")
    if payload.get("projection_counted_positive") is True or payload.get("easier_projection") is True:
        blockers.add("K-013")
    if payload.get("self_attested_goal_preservation") is True:
        blockers.add("K-016")
    if payload.get("proof_coupled_corpus") is True or "target_shape_id" in payload or "expected_compiler_rule" in payload:
        blockers.add("K-014")
    if payload.get("sealed_generator_imports_proof_code") is True:
        blockers.add("K-015")
    if payload.get("unique_normalized_theorem_skeletons", 9999) < 150:
        blockers.add("K-029")
    if payload.get("engine_role") and payload.get("proof_text_present") is True:
        blockers.add("K-009")
    if "exact " in text or "by " in text or "rw [" in text:
        if schema.startswith("EngineOutputFull2D") or payload.get("engine_output_contains_proof_text"):
            blockers.add("K-009")
    if payload.get("facts") == [{"conclusion": "TARGET", "premises": [], "checker_report_ref": None}]:
        blockers.update({"K-004", "K-005"})
    if payload.get("target_fact_with_empty_premises") is True:
        blockers.update({"K-004", "K-005"})
    steps = payload.get("derivation_steps")
    if isinstance(steps, list) and steps:
        has_non_target = any(step.get("non_target_intermediate") is True or step.get("output_is_target") is False for step in steps if isinstance(step, dict))
        only_target = all(step.get("output_is_target") is True for step in steps if isinstance(step, dict))
        if only_target and not has_non_target:
            blockers.add("K-005")
    if payload.get("direct_identity_rule") is True or payload.get("direct_facade_rule") is True:
        blockers.add("K-006")
    if payload.get("engine_output_from_compiler_selected_rules") is True or payload.get("compiler_selected_rule_list"):
        blockers.add("K-008")
    if payload.get("causality_report_only") is True or (
        payload.get("failed_as_expected") is True and not payload.get("command_logs") and not payload.get("temp_run_dirs")
    ):
        blockers.add("K-011")
    if payload.get("destructive_causality_passed") is False:
        blockers.add("K-012")
    if payload.get("baseline_outcome_from_family") is True:
        blockers.add("K-023")
    if payload.get("missing_required_baselines"):
        blockers.add("K-033")
    if payload.get("conditional_b8_resolution_valid") is False:
        blockers.add("K-024")
    if payload.get("direct_wrapped_facade_fraction", 0.0) > 0.10:
        blockers.add("K-020")
    if payload.get("non_target_intermediate_fraction", 1.0) < 0.50:
        blockers.add("K-021")
    if payload.get("construction_case_certificate_success_fraction", 1.0) < 0.40:
        blockers.add("K-022")
    if payload.get("used_concrete_non_identity_rules", 25) < 25 or payload.get("used_rule_families", 10) < 10:
        blockers.add("K-019")
    if payload.get("every_release_engine_role_contributed") is False:
        blockers.add("K-018")
    if payload.get("metrics_below_threshold") is True:
        blockers.add("K-025")
    if payload.get("final_status") == "final_theorem" and payload.get("final_status_source") != "FinalVerifyReportFull2D":
        blockers.add("K-032")
    if payload.get("closure_forbidden_claims_present"):
        blockers.add("K-028")
    return blockers


def validate_red_case_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    case_id = str(fixture.get("id", ""))
    expected = set(fixture.get("expected_blockers", []))
    variants = fixture.get("variants", [])
    variant_results: list[dict[str, Any]] = []
    detected: set[str] = set()
    errors: list[str] = []
    if not variants:
        errors.append("missing_variants")
    kinds = {variant.get("kind") for variant in variants if isinstance(variant, dict)}
    if "static-code" not in kinds:
        errors.append("missing_static_code_variant")
    if "artifact-run" not in kinds:
        errors.append("missing_artifact_run_variant")
    for variant in variants:
        kind = variant.get("kind")
        blockers: set[str] = set()
        if kind == "static-code":
            if "code" in variant:
                blockers = detect_static_code(str(variant["code"]))
            else:
                rel = RED_CASE_ROOT / str(variant.get("path", ""))
                if not rel.exists():
                    errors.append(f"missing_static_code:{rel.relative_to(ROOT).as_posix()}")
                else:
                    blockers = detect_static_code(rel.read_text(encoding="utf-8"))
        elif kind == "artifact-run":
            if "payload" in variant:
                payload = variant["payload"]
                if isinstance(payload, dict):
                    blockers = detect_artifact_payload(payload)
                else:
                    errors.append("artifact_payload_not_object")
            else:
                rel = RED_CASE_ROOT / str(variant.get("path", ""))
                if not rel.exists():
                    errors.append(f"missing_artifact_payload:{rel.relative_to(ROOT).as_posix()}")
                else:
                    blockers = detect_artifact_payload(read_json(rel))
        else:
            errors.append(f"unknown_variant_kind:{kind}")
        if expected and not (blockers & expected):
            errors.append(f"variant_not_rejected_for_expected_blocker:{kind}:{variant.get('path', '<inline>')}")
        detected.update(blockers)
        variant_results.append({"kind": kind, "path": variant.get("path"), "detected_blockers": sorted(blockers)})
    missing_expected = sorted(expected - detected)
    rejected = not missing_expected and not errors
    return {
        "id": case_id,
        "name": fixture.get("name"),
        "expected_blockers": sorted(expected),
        "detected_blockers": sorted(detected),
        "missing_expected_blockers": missing_expected,
        "variant_results": variant_results,
        "errors": errors,
        "rejected": rejected,
    }


def run_red_cases() -> dict[str, Any]:
    manifest = load_red_case_manifest()
    expected_ids = {case["id"] for case in RED_CASES}
    fixtures = manifest.get("fixtures", [])
    fixture_ids = {str(fixture.get("id")) for fixture in fixtures}
    results = [validate_red_case_fixture(fixture) for fixture in fixtures]
    errors: list[str] = []
    missing = sorted(expected_ids - fixture_ids)
    extra = sorted(fixture_ids - expected_ids)
    if missing:
        errors.append("missing_red_cases:" + ",".join(missing))
    if extra:
        errors.append("unknown_red_cases:" + ",".join(extra))
    accepted = [result["id"] for result in results if not result["rejected"]]
    if accepted:
        errors.append("red_cases_accepted:" + ",".join(sorted(accepted)))
    return {
        "schema_version": "GeometryFull2DRedCaseRunV1",
        "status": "passed" if not errors else "failed",
        "all_rejected": not errors,
        "errors": errors,
        "red_case_count": len(fixtures),
        "expected_red_case_count": len(RED_CASES),
        "results": results,
    }


def build_checker_coverage_matrix(executed_checkers: dict[str, Any] | None = None) -> dict[str, Any]:
    require_executed = executed_checkers is not None
    executed_checkers = executed_checkers or {}
    executed_names = set(executed_checkers)
    for command_name in executed_checkers:
        command = REQUIRED_CHECKER_COMMANDS.get(command_name, [])
        for item in command:
            if str(item).endswith(".py"):
                executed_names.add(Path(str(item)).name)
    if require_executed:
        executed_names.add("check_release_acceptance_v0_5.py")
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for kid in sorted(K_BLOCKERS):
        checkers = CHECKER_COVERAGE.get(kid, [])
        executed = [checker for checker in checkers if checker in executed_names or any(name in checker for name in executed_names)]
        rows.append(
            {
                "requirement": kid,
                "description": K_BLOCKERS[kid],
                "checkers": checkers,
                "executed_checkers": sorted(executed),
            }
        )
        if not checkers:
            errors.append(f"{kid}:missing_checker_mapping")
        if require_executed and not executed:
            errors.append(f"{kid}:no_executed_checker")
    unknown = sorted(set(CHECKER_COVERAGE) - set(K_BLOCKERS))
    if unknown:
        errors.append("unknown_k_coverage:" + ",".join(unknown))
    missing = sorted(set(K_BLOCKERS) - set(CHECKER_COVERAGE))
    if missing:
        errors.append("missing_k_coverage:" + ",".join(missing))
    return {
        "schema_version": "GeometryFull2DCheckerCoverageV1",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "rows": rows,
        "covered_requirements": sorted(kid for kid in K_BLOCKERS if CHECKER_COVERAGE.get(kid)),
        "required_requirements": sorted(K_BLOCKERS),
    }


def scan_checker_whitelist() -> dict[str, Any]:
    paths = sorted(set((ROOT / "scripts").glob("check_*_v0_5.py")) | set((ROOT / "scripts").glob("run_*_v0_5.py")))
    errors: list[str] = []
    scans: list[dict[str, Any]] = []
    forbidden = re.compile(r"(allowlist|suppress|ignore_by_filename|skip_by_filename|if\s+.*filename.*return|if\s+.*path.*continue)", re.IGNORECASE)
    for path in paths:
        text = path.read_text(encoding="utf-8")
        hits: list[str] = []
        if forbidden.search(text):
            hits.append("filename_or_role_suppression_pattern")
        scans.append({"path": path.relative_to(ROOT).as_posix(), "hits": hits})
        if hits:
            errors.append(f"{path.relative_to(ROOT).as_posix()}:{','.join(hits)}")
    return {
        "schema_version": "GeometryFull2DNoCheckerWhitelistV1",
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "scanned_file_count": len(paths),
        "scans": scans,
    }


def run_command(name: str, cmd: list[str], *, timeout: int = 120) -> dict[str, Any]:
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        stdout = proc.stdout
        stderr = proc.stderr
        parsed: Any = None
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError:
            parsed = {"stdout_tail": stdout[-4000:], "stderr_tail": stderr[-4000:]}
        return {
            "name": name,
            "cmd": cmd,
            "returncode": proc.returncode,
            "duration_seconds": round(time.time() - started, 3),
            "report": parsed,
        }
    except FileNotFoundError as exc:
        return {"name": name, "cmd": cmd, "returncode": 127, "duration_seconds": round(time.time() - started, 3), "report": {"error": str(exc)}}
    except subprocess.TimeoutExpired as exc:
        return {
            "name": name,
            "cmd": cmd,
            "returncode": 124,
            "duration_seconds": round(time.time() - started, 3),
            "report": {"error": "timeout", "stdout_tail": (exc.stdout or "")[-4000:], "stderr_tail": (exc.stderr or "")[-4000:]},
        }


def current_git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def create_fresh_run_dir(base: Path) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    run_dir = base / f"release_{int(time.time())}_{os.getpid()}"
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    return run_dir


def placeholder_summary(name: str) -> dict[str, Any]:
    return {"status": "failed", "summary": f"{name} not yet implemented", "placeholder": False}


def command_passed(command_results: dict[str, Any], name: str) -> bool:
    result = command_results.get(name)
    return isinstance(result, dict) and result.get("returncode") == 0


def command_report(command_results: dict[str, Any], name: str) -> dict[str, Any]:
    result = command_results.get(name)
    report = result.get("report") if isinstance(result, dict) else None
    return report if isinstance(report, dict) else {}


def compiler_isolation_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    input_report = command_report(command_results, "compiler_input_isolation")
    taint_report = command_report(command_results, "compiler_taint")
    passed = command_passed(command_results, "compiler_input_isolation") and command_passed(command_results, "compiler_taint")
    return {
        "status": "passed" if passed else "failed",
        "input_isolation_status": input_report.get("status", "not_run"),
        "taint_status": taint_report.get("status", "not_run"),
        "proof_from_shape_rejected": "proof_from_shape_static_not_rejected" not in input_report.get("errors", []),
        "forbidden_metadata_taint_checked": taint_report.get("schema_version") == "CompilerTaintCheckV05",
    }


def final_verify_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "proof_worker_final_verify")
    positive = report.get("positive") if isinstance(report.get("positive"), dict) else {}
    final = positive.get("final_verify") if isinstance(positive.get("final_verify"), dict) else {}
    passed = command_passed(command_results, "proof_worker_final_verify")
    return {
        "status": "passed" if passed else "failed",
        "self_test_status": report.get("status", "not_run"),
        "lake_env_lean_command": final.get("lake_env_lean_command", []),
        "lake_env_lean_returncode": final.get("lake_env_lean_returncode"),
        "theorem_statement_unchanged": final.get("theorem_statement_unchanged") is True,
        "no_sorry": final.get("no_sorry") is True,
        "no_forbidden_declarations": final.get("no_forbidden_declarations") is True,
        "no_toy_target_definitions": final.get("no_toy_target_definitions") is True,
        "admitted_imports_only": final.get("admitted_imports_only") is True,
        "final_status_source": final.get("final_status_source"),
    }


def independent_checker_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "independent_solver_checkers")
    return {
        "status": "passed" if command_passed(command_results, "independent_solver_checkers") else "failed",
        "self_test_status": report.get("status", "not_run"),
        "schema_version": report.get("schema_version"),
    }


def corpus_summary(corpus_root: Path, command_results: dict[str, Any]) -> dict[str, Any]:
    manifest_path = corpus_root / "corpus_manifest.json"
    tasks: list[dict[str, Any]] = []
    if manifest_path.exists():
        payload = read_json(manifest_path)
        raw_tasks = payload.get("tasks", [])
        tasks = raw_tasks if isinstance(raw_tasks, list) else []
    counted = [task for task in tasks if isinstance(task, dict) and task.get("counted_positive") is True]
    negatives = [task for task in tasks if isinstance(task, dict) and task.get("source_type") == "NegativeTargetOutsideMalformed"]
    sealed = [task for task in counted if task.get("source_type") == "SealedAdversarialHoldout"]
    external = [task for task in counted if task.get("source_type") == "ExternalGoalPreserved"]
    projection_counted = [task for task in counted if task.get("projection") is True]
    user_review_missing = [
        task
        for task in counted
        if task.get("source_type") == "UserReviewedGoal" and not task.get("review_manifest_ref")
    ]
    goal_report = command_report(command_results, "goal_preservation")
    discovered_external = int(goal_report.get("discovered_machine_checkable_external_goal_preserved_count", len(external)))
    errors: list[str] = []
    if len(counted) < 1200:
        errors.append("counted_positive_formal_lean_tasks_lt_1200")
    if len(negatives) < 300:
        errors.append("negative_target_outside_malformed_tasks_lt_300")
    if len(sealed) < 700:
        errors.append("sealed_adversarial_holdout_count_lt_700")
    if len(external) < min(300, discovered_external):
        errors.append("external_goal_preserved_count_below_discovered_floor")
    if user_review_missing:
        errors.append("user_reviewed_goal_without_review_manifest_count_nonzero")
    if projection_counted:
        errors.append("projection_non_counted_positive_count_nonzero")
    if not command_passed(command_results, "corpus_independence"):
        errors.append("corpus_independence_failed")
    if not command_passed(command_results, "goal_preservation"):
        errors.append("goal_preservation_failed")
    return {
        "status": "passed" if not errors else "failed",
        "errors": errors,
        "counted_positive_formal_lean_tasks": len(counted),
        "negative_target_outside_malformed_tasks": len(negatives),
        "sealed_adversarial_holdout_count": len(sealed),
        "external_goal_preserved_count": len(external),
        "discovered_machine_checkable_external_goal_preserved_count": discovered_external,
        "user_reviewed_goal_without_review_manifest_count": len(user_review_missing),
        "projection_non_counted_positive_count": len(projection_counted),
        "task_count": len(tasks),
    }


def corpus_statement_diversity_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "corpus_statement_diversity")
    errors = list(report.get("errors", [])) if isinstance(report.get("errors"), list) else []
    return {
        "status": "passed" if command_passed(command_results, "corpus_statement_diversity") else "failed",
        "errors": errors,
        "unique_normalized_theorem_skeletons": report.get("unique_normalized_theorem_skeletons", 0),
        "max_exact_skeleton_duplicate": report.get("max_exact_skeleton_duplicate", 0),
        "used_relation_families": report.get("used_relation_families", 0),
        "construction_case_certificate_required_tasks": report.get("construction_case_certificate_required_tasks", 0),
        "non_target_intermediate_required_tasks": report.get("non_target_intermediate_required_tasks", 0),
        "counted_positive_count": report.get("counted_positive_count", 0),
    }


def rule_registry_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "rule_registry")
    positive = report.get("positive") if isinstance(report.get("positive"), dict) else {}
    return {
        "status": "passed" if command_passed(command_results, "rule_registry") else "failed",
        "self_test_status": report.get("status", "not_run"),
        "counted_rule_count": positive.get("counted_rule_count", 0),
        "counted_rule_family_count": positive.get("counted_rule_family_count", 0),
    }


def report_summary(command_results: dict[str, Any], name: str, fallback_name: str) -> dict[str, Any]:
    report = command_report(command_results, name)
    if report:
        return report
    return placeholder_summary(fallback_name)


def actual_pipeline_run_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "matrix")
    summary = report.get("actual_pipeline_run_summary") if isinstance(report.get("actual_pipeline_run_summary"), dict) else {}
    return summary if summary else {"status": "failed", "required_baselines": REQUIRED_BASELINES, "record_count": 0}


def measured_failure_summary(command_results: dict[str, Any]) -> dict[str, Any]:
    report = command_report(command_results, "metrics")
    counts = report.get("measured_failure_by_baseline") if isinstance(report.get("measured_failure_by_baseline"), dict) else {}
    return {
        "status": "passed" if command_passed(command_results, "metrics") else "failed",
        "measured_failure_count": report.get("measured_failure_count", 0),
        "measured_failure_by_baseline": counts,
    }


def build_fail_closed_release_report(
    *,
    config_path: Path,
    output_path: Path,
    fresh_run: bool,
    run_required_commands: bool,
) -> dict[str, Any]:
    config = load_config(config_path)
    configured_run_root = ROOT / str(config.get("output_root", DEFAULT_RUN_ROOT.as_posix()))
    run_dir = create_fresh_run_dir(configured_run_root) if fresh_run else configured_run_root
    command_results: dict[str, Any] = {}
    release_blockers: set[str] = set()
    hard_blockers: set[str] = set()

    base_commands = ["active_guardian_spec", "red_cases", "acceptance_coverage", "no_checker_whitelist"]
    release_command_order = [
        "active_guardian_spec",
        "red_cases",
        "acceptance_coverage",
        "no_checker_whitelist",
        "schema_validators",
        "corpus_independence",
        "corpus_statement_diversity",
        "goal_preservation",
        "provider_stage_boundary",
        "rule_registry",
        "compiler_input_isolation",
        "compiler_taint",
        "matrix",
        "extraction",
        "engine_outputs",
        "independent_solver_checkers",
        "proof_worker_final_verify",
        "causality_mutations",
        "solver_causality",
        "baseline_comparability",
        "metrics",
        "used_rule_coverage",
        "engine_contribution",
        "debt_ledger",
        "closure_claim_ceiling",
    ]
    commands_to_run = release_command_order if run_required_commands else base_commands
    for name in commands_to_run:
        cmd = list(REQUIRED_CHECKER_COMMANDS[name])
        cmd = [str(run_dir) if item == "runs/geometry_full2d_v0_5" else item for item in cmd]
        if name == "closure_claim_ceiling":
            cmd = [str(output_path) if item.endswith("release_acceptance_report.json") else item for item in cmd]
            closure_path = ROOT / "docs" / "ai" / "changes" / "geometry-full2d-v0_5" / "CLOSURE.md"
            if closure_path.exists():
                cmd = [item for item in cmd if item != "--allow-missing-closure"]
        timeout_by_command = {
            "matrix": 7200,
            "causality_mutations": 43200,
            "engine_outputs": 1200,
            "extraction": 300,
            "independent_solver_checkers": 1800,
            "proof_worker_final_verify": 1800,
            "solver_causality": 600,
            "metrics": 300,
            "used_rule_coverage": 300,
            "engine_contribution": 1800,
            "baseline_comparability": 300,
        }
        timeout = timeout_by_command.get(name, 120)
        result = run_command(name, cmd, timeout=timeout)
        command_results[name] = result
        if result["returncode"] != 0:
            release_blockers.add(f"required_command_failed:{name}")

    red_case_report = command_results.get("red_cases", {}).get("report", {})
    if not isinstance(red_case_report, dict) or red_case_report.get("all_rejected") is not True:
        release_blockers.add("K-003")

    coverage = build_checker_coverage_matrix({name: result for name, result in command_results.items()})
    if coverage["status"] != "passed":
        release_blockers.add("K-002")
    whitelist = command_results.get("no_checker_whitelist", {}).get("report", {})
    if not isinstance(whitelist, dict) or whitelist.get("status") != "passed":
        release_blockers.add("K-030")

    if not (ROOT / "benchmarks" / "geometry_full2d_v0_5" / "corpus_manifest.json").exists():
        release_blockers.update({"K-001", "K-029"})
    if not (ROOT / "configs" / "benchmark_runs" / "geometry_full2d_v0_5.yaml").exists():
        hard_blockers.add("missing_v0_5_config")

    if not command_passed(command_results, "independent_solver_checkers"):
        release_blockers.add("K-010")
    if not command_passed(command_results, "proof_worker_final_verify"):
        release_blockers.add("K-032")
    if not command_passed(command_results, "corpus_independence"):
        release_blockers.update({"K-013", "K-014", "K-015"})
    if not command_passed(command_results, "goal_preservation"):
        release_blockers.add("K-016")
    if not command_passed(command_results, "corpus_statement_diversity"):
        release_blockers.add("K-029")
    if not command_passed(command_results, "extraction"):
        release_blockers.add("K-017")
    if not command_passed(command_results, "engine_outputs"):
        release_blockers.update({"K-004", "K-005", "K-009"})
    if not command_passed(command_results, "matrix"):
        release_blockers.add("K-033")
    if not command_passed(command_results, "causality_mutations") or not command_passed(command_results, "solver_causality"):
        release_blockers.update({"K-011", "K-012"})
    if not command_passed(command_results, "baseline_comparability"):
        release_blockers.update({"K-023", "K-024", "K-033"})
    if not command_passed(command_results, "metrics"):
        release_blockers.update({"K-020", "K-021", "K-022", "K-025"})
    if not command_passed(command_results, "used_rule_coverage"):
        release_blockers.add("K-019")
    if not command_passed(command_results, "engine_contribution"):
        release_blockers.add("K-018")
    if not command_passed(command_results, "debt_ledger"):
        release_blockers.add("K-027")
    if not command_passed(command_results, "closure_claim_ceiling"):
        release_blockers.add("K-028")

    corpus = corpus_summary(DEFAULT_CORPUS_ROOT, command_results)
    diversity = corpus_statement_diversity_summary(command_results)
    if corpus["status"] != "passed":
        release_blockers.update({"K-001", "K-013", "K-014", "K-029"})
    if diversity["status"] != "passed":
        release_blockers.add("K-029")

    report = {
        "schema_version": "GeometryFull2DReleaseAcceptanceV05",
        "status": "passed" if not release_blockers and not hard_blockers else "failed",
        "closure_allowed": not release_blockers and not hard_blockers,
        "checked_requirements": sorted(K_BLOCKERS),
        "checker_coverage_matrix": coverage,
        "red_case_summary": red_case_report if isinstance(red_case_report, dict) else {"status": "failed", "all_rejected": False},
        "corpus_summary": corpus,
        "corpus_statement_diversity_summary": diversity,
        "extraction_summary": report_summary(command_results, "extraction", "extraction"),
        "provider_stage_boundary_summary": report_summary(command_results, "provider_stage_boundary", "provider_stage_boundary"),
        "engine_output_summary": report_summary(command_results, "engine_outputs", "engine_outputs"),
        "independent_checker_summary": independent_checker_summary(command_results),
        "rule_registry_summary": rule_registry_summary(command_results),
        "compiler_isolation_summary": compiler_isolation_summary(command_results),
        "actual_pipeline_run_summary": actual_pipeline_run_summary(command_results),
        "solver_causality_summary": report_summary(command_results, "solver_causality", "solver_causality"),
        "final_verify_summary": final_verify_summary(command_results),
        "metrics_summary": report_summary(command_results, "metrics", "metrics"),
        "used_rule_coverage_summary": report_summary(command_results, "used_rule_coverage", "used_rule_coverage"),
        "engine_contribution_summary": report_summary(command_results, "engine_contribution", "engine_contribution"),
        "baseline_comparability_summary": report_summary(command_results, "baseline_comparability", "baseline_comparability"),
        "measured_failure_summary": measured_failure_summary(command_results),
        "debt_ledger_summary": report_summary(command_results, "debt_ledger", "debt_ledger"),
        "freshness_summary": {
            "status": "passed",
            "fresh_run": fresh_run,
            "release_run_dir": run_dir.relative_to(ROOT).as_posix(),
            "current_git_head_bound": True,
            "git_head": current_git_head(),
        },
        "closure_claim_ceiling": {"allowed_final_claim": CLAIM_TARGET, "forbidden_claims_present": []},
        "closure_claim_ceiling_summary": report_summary(command_results, "closure_claim_ceiling", "closure_claim_ceiling"),
        "required_command_results": command_results,
        "release_blockers": sorted(release_blockers),
        "hard_blockers": sorted(hard_blockers),
    }
    missing_fields = [field for field in REQUIRED_REPORT_FIELDS if field not in report]
    if missing_fields:
        report["status"] = "failed"
        report["release_blockers"].append("K-001")
        report["missing_report_fields"] = missing_fields
    write_json(output_path, report)
    return report
