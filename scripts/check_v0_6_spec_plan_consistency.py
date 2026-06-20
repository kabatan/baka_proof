#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "docs" / "ai" / "changes" / "geometry-full2d-v0_6"
BASE_ID = "MARP-GEOLEAN-BASE-012"
PLAN_ID = "MARP-GEOLEAN-PLAN-012"
ACCEPTANCE_ID = "MARP-GEOLEAN-ACCEPTANCE-012"
CLAIM = "V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"

FILES = {
    "base": ROOT / "BASE_SPEC.md",
    "plan": ROOT / "PLAN.md",
    "acceptance": ROOT / "ACCEPTANCE.md",
    "red": ROOT / "RED_CASE_SUITE.md",
    "handoff": ROOT / "CODEX_HANDOFF.md",
    "invariants": ROOT / "REAL_PIPELINE_INVARIANTS.md",
    "directive": ROOT / "REFACTOR_DIRECTIVE.md",
    "source_map": ROOT / "SOURCE_MAP.md",
}

RED_CASES = {
    "RC-001": ("Target-fact provider", "RedCase_TargetFactProvider"),
    "RC-002": ("Naked target assertion", "RedCase_NakedTargetAssertion"),
    "RC-003": ("Identity/direct-rule registry", "RedCase_IdentityDirectRuleRegistry"),
    "RC-004": ("Proof-from-shape compiler", "RedCase_ProofFromShapeCompiler"),
    "RC-005": ("Rule-list artifact synthesis", "RedCase_RuleListArtifactSynthesis"),
    "RC-006": ("Report-only causality", "RedCase_ReportOnlyCausality"),
    "RC-007": ("Family-coded baseline", "RedCase_FamilyCodedBaseline"),
    "RC-008": ("Projection benchmark", "RedCase_ProjectionBenchmark"),
    "RC-009": ("Checker omission", "RedCase_CheckerOmission"),
    "RC-010": ("Checker whitelist", "RedCase_CheckerWhitelist"),
    "RC-011": ("Sealed challenge collusion", "RedCase_SealedChallengeCollusion"),
    "RC-012": ("Stale evidence replay", "RedCase_StaleEvidenceReplay"),
    "RC-013": ("Rule hack", "RedCase_RuleHack"),
    "RC-014": ("Target-as-certificate", "RedCase_TargetAsCertificate"),
    "RC-015": ("Checker-generated success artifacts", "RedCase_CheckerGeneratedSuccessArtifacts"),
    "RC-016": ("Static-only green release", "RedCase_StaticOnlyGreenRelease"),
    "RC-017": ("B2-only matrix", "RedCase_B2OnlyMatrix"),
    "RC-018": ("Direct lemma wrapped as intermediate", "RedCase_DirectLemmaWrappedAsIntermediate"),
    "RC-019": ("Provider imports compiler", "RedCase_ProviderImportsCompiler"),
}

FINAL_FLAGS = ("--fresh-run", "--fail-on-stale", "--no-skip", "--all-baselines", "--live-mutations")

REQUIRED_CHECKERS = (
    "check_active_guardian_spec_v0_6.py",
    "check_red_case_suite_v0_6.py --all",
    "check_acceptance_coverage_v0_6.py",
    "check_no_old_release_dependency_v0_6.py",
    "check_schema_contracts_v0_6.py --self-test --red-cases",
    "check_full2d_extraction_corpus_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --run-dir <fresh>",
    "check_full2d_claimspec_v0_6.py --run-dir <fresh> --self-test",
    "check_provider_isolation_v0_6.py --run-dir <fresh> --red-cases",
    "check_engine_output_not_from_compiler_rules_v0_6.py --run-dir <fresh> --red-cases",
    "check_independent_solver_artifacts_v0_6.py --all --red-cases",
    "check_rule_registry_v0_6.py --release --red-cases",
    "check_selected_derivation_v0_6.py --run-dir <fresh> --red-cases",
    "check_derivation_target_matcher_v0_6.py --run-dir <fresh> --red-cases",
    "check_compiler_input_lock_v0_6.py --self-test --red-cases --dynamic-taint",
    "check_proof_worker_final_verify_v0_6.py --self-test --red-cases",
    "check_corpus_independence_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --red-cases",
    "check_statement_diversity_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6",
    "run_full2d_matrix_v0_6.py --config ... --run-dir <fresh> --execute-all --all-baselines --no-skip",
    "check_all_baseline_matrix_v0_6.py --run-dir <fresh> --red-cases",
    "run_solver_causality_live_v0_6.py --run-dir <fresh> --all-b2-successes",
    "check_solver_causality_live_v0_6.py --run-dir <fresh> --red-cases",
    "check_full2d_metrics_v0_6.py --run-dir <fresh>",
    "check_closure_claim_ceiling_v0_6.py",
)

PLAN_BASE_BRIDGES = (
    "Do not optimize for green release first",
    "record it in DebtLedger and continue with the next unblocked work package",
    "Do not implement provider/compiler/matrix release code until this report passes",
    "Compiler API must match Base Spec DR-012-004 exactly",
    "FinalVerifyGate runs",
    "Live destructive causality runner",
    "all-baselines",
    "It must generate closure only if release passes",
)

BASE_DECISION_TERMS = (
    "DR-012-001",
    "DR-012-002",
    "DR-012-003",
    "DR-012-004",
    "DR-012-005",
    "DR-012-006",
    "DR-012-007",
    "DR-012-008",
    "DR-012-009",
    "DR-012-010",
    "DR-012-011",
    "DR-012-012",
    "DR-012-013",
    "DR-012-014",
)

FORBIDDEN = (
    "USER_APPROVED_ACTIVE_DRAFT",
    "geometry-full2d_v0_6",
    "optional bypass",
    "optional shortcut",
)


def main() -> int:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.exists():
            errors.append(f"missing_file:{path}")
            texts[name] = ""
        else:
            texts[name] = path.read_text(encoding="utf-8")

    _check_ids(errors, texts)
    _check_final_flags(errors, texts)
    _check_red_cases(errors, texts)
    _check_acceptance(errors, texts)
    _check_plan(errors, texts)
    _check_base(errors, texts)
    _check_forbidden(errors, texts)

    status = "passed" if not errors else "failed"
    print(json.dumps({"status": status, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


def _check_ids(errors: list[str], texts: dict[str, str]) -> None:
    for name in ("base", "plan", "acceptance", "red", "handoff", "invariants"):
        text = texts[name]
        for item in (BASE_ID, PLAN_ID, ACCEPTANCE_ID, CLAIM):
            if item not in text:
                errors.append(f"{name}:missing:{item}")

    if _field(texts["base"], "spec_id") != BASE_ID:
        errors.append("base_frontmatter_spec_id_mismatch")
    if _field(texts["plan"], "plan_id") != PLAN_ID:
        errors.append("plan_frontmatter_plan_id_mismatch")
    if _field(texts["plan"], "base_spec") != BASE_ID:
        errors.append("plan_frontmatter_base_spec_mismatch")
    if _field(texts["acceptance"], "acceptance_id") != ACCEPTANCE_ID:
        errors.append("acceptance_frontmatter_acceptance_id_mismatch")
    if _field(texts["acceptance"], "base_spec") != BASE_ID:
        errors.append("acceptance_frontmatter_base_spec_mismatch")
    if _field(texts["acceptance"], "plan") != PLAN_ID:
        errors.append("acceptance_frontmatter_plan_mismatch")


def _check_final_flags(errors: list[str], texts: dict[str, str]) -> None:
    for name in ("base", "plan", "acceptance", "handoff"):
        for flag in FINAL_FLAGS:
            if flag not in texts[name]:
                errors.append(f"{name}:missing_final_flag:{flag}")
    final_command_terms = (
        "scripts/check_release_acceptance_v0_6.py",
        "configs/benchmark_runs/geometry_full2d_v0_6.yaml",
        "docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json",
    )
    for name in ("base", "plan", "acceptance", "handoff"):
        for term in final_command_terms:
            if term not in texts[name]:
                errors.append(f"{name}:missing_final_command_term:{term}")


def _check_red_cases(errors: list[str], texts: dict[str, str]) -> None:
    base = texts["base"]
    red = texts["red"]
    base_headings = dict(re.findall(r"(?m)^### (RC-\d{3}) (.+)$", base))
    for rc_id, (heading, fixture_name) in RED_CASES.items():
        if base_headings.get(rc_id) != heading:
            errors.append(f"base_red_case_heading_mismatch:{rc_id}:expected={heading}:actual={base_headings.get(rc_id)}")
        if rc_id not in base:
            errors.append(f"base_missing_red_case_id:{rc_id}")
        if rc_id not in red:
            errors.append(f"red_suite_missing_red_case_id:{rc_id}")
        if heading.lower() not in red.lower():
            errors.append(f"red_suite_missing_base_heading:{rc_id}:{heading}")
        if fixture_name not in red:
            errors.append(f"red_suite_missing_fixture:{fixture_name}")
    if len(set(re.findall(r"RC-\d{3}", red))) != len(RED_CASES):
        errors.append("red_suite_unique_rc_count_mismatch")
    if red.count("RedCase_") != len(RED_CASES):
        errors.append(f"red_suite_fixture_count_mismatch:{red.count('RedCase_')}")
    if "EngineOutputContainsProofText" not in red or "K-010" not in red:
        errors.append("red_suite_missing_non_rc_engine_output_proof_text_fixture")


def _check_acceptance(errors: list[str], texts: dict[str, str]) -> None:
    acceptance = texts["acceptance"]
    for k in range(1, 36):
        kid = f"K-{k:03d}"
        if kid not in acceptance:
            errors.append(f"acceptance_missing:{kid}")
    for checker in REQUIRED_CHECKERS:
        if checker not in acceptance:
            errors.append(f"acceptance_missing_required_checker:{checker}")
    for phrase in (
        "K_to_checker_evidence_map",
        "extraction_summary",
        "claimspec_summary",
        "engine_output_not_from_compiler_rules_summary",
        "Checker cannot fabricate pipeline evidence",
        "Release checker invokes all required checkers",
        "Any checker-generated success artifact",
        "B2-only matrix fails",
        "Field-only causality fails",
        "No stale v0.4.x / draft v0.5 / previous v0.6 evidence",
    ):
        if phrase not in acceptance:
            errors.append(f"acceptance_missing_phrase:{phrase}")


def _check_plan(errors: list[str], texts: dict[str, str]) -> None:
    plan = texts["plan"]
    for wp in range(0, 17):
        label = f"WP{wp:02d}"
        if label not in plan:
            errors.append(f"plan_missing_work_package:{label}")
    for phrase in PLAN_BASE_BRIDGES:
        if phrase not in plan:
            errors.append(f"plan_missing_base_bridge:{phrase}")
    for checker in (
        "check_active_guardian_spec_v0_6.py",
        "check_v0_6_spec_plan_consistency.py",
        "check_red_case_suite_v0_6.py --all",
        "check_acceptance_coverage_v0_6.py",
        "check_full2d_extraction_corpus_v0_6.py",
        "check_full2d_claimspec_v0_6.py",
        "check_engine_output_not_from_compiler_rules_v0_6.py",
        "run_solver_causality_live_v0_6.py",
        "run_full2d_matrix_v0_6.py",
        "check_closure_claim_ceiling_v0_6.py",
    ):
        if checker not in plan:
            errors.append(f"plan_missing_checker_or_runner:{checker}")


def _check_base(errors: list[str], texts: dict[str, str]) -> None:
    base = texts["base"]
    for term in BASE_DECISION_TERMS:
        if term not in base:
            errors.append(f"base_missing_decision:{term}")
    for phrase in (
        "compile_derivation(",
        "TheoremAnchorV1",
        "DerivationTargetMatcher",
        "at least 35 counted rules across at least 15 families",
        "counted positives >= 1200",
        "unique normalized target ASTs >= 900",
        "B2 overall final theorem rate >= 0.70",
        "B2 solver-causal success fraction = 1.00",
        "schema contradiction",
        "license restriction blocking use of required external data",
    ):
        if phrase not in base:
            errors.append(f"base_missing_phrase:{phrase}")


def _check_forbidden(errors: list[str], texts: dict[str, str]) -> None:
    joined = "\n".join(texts.values())
    for forbidden in FORBIDDEN:
        if forbidden in joined:
            errors.append(f"forbidden_term:{forbidden}")


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else None


if __name__ == "__main__":
    raise SystemExit(main())
