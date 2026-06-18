#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "docs" / "ai" / "changes" / "geometry-full2d-v0_5"
files = {
    'base': ROOT/'BASE_SPEC.md',
    'plan': ROOT/'PLAN.md',
    'acceptance': ROOT/'ACCEPTANCE.md',
    'red': ROOT/'RED_CASE_SUITE.md',
    'handoff': ROOT/'CODEX_HANDOFF.md',
}
required = [
    'MARP-GEOLEAN-BASE-011',
    'MARP-GEOLEAN-PLAN-011',
    'MARP-GEOLEAN-ACCEPTANCE-011',
    'V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY',
]
red_cases = [
    'TargetFactProvider', 'NakedTargetAssertion', 'IdentityRuleRegistry', 'ProofFromShapeCompiler',
    'RuleListArtifactSynthesis', 'ReportOnlyCausality', 'FamilyCodedBaseline', 'ProjectionCorpusCounted',
    'EngineOutputContainsProofText', 'CheckerOmission', 'CheckerWhitelist', 'DirectLemmaWrappedAsIntermediate',
    'SealedChallengeImportsCompiler', 'StaleEvidenceReplay', 'TargetShapeMenuCorpus',
    'GoalPreservationSelfAttestation', 'ProviderImportsCompiler', 'B8SilentlyOmitted',
    'ClosureOverclaimsReadiness'
]
errors=[]
for name,path in files.items():
    text=path.read_text(encoding='utf-8')
    if name in {'base','plan','acceptance'}:
        for item in required:
            if item not in text:
                errors.append(f'{name}:missing:{item}')
for rc in red_cases:
    if rc not in files['base'].read_text(encoding='utf-8') or rc not in files['red'].read_text(encoding='utf-8'):
        errors.append(f'redcase_missing:{rc}')
base=files['base'].read_text(encoding='utf-8')
acceptance=files['acceptance'].read_text(encoding='utf-8')
for k in range(1,34):
    kid=f'K-{k:03d}'
    if kid not in acceptance:
        errors.append(f'acceptance_missing:{kid}')
for phrase in ['--fresh-run','check_acceptance_coverage_v0_5.py','check_no_checker_whitelist_v0_5.py','check_corpus_statement_diversity_v0_5.py','check_closure_claim_ceiling_v0_5.py']:
    if phrase not in acceptance:
        errors.append(f'acceptance_missing_phrase:{phrase}')
plan=files['plan'].read_text(encoding='utf-8')
for phrase in [
    'Base Spec to Plan coverage matrix',
    'No Plan acceptance item is sufficient by itself',
    'WP-10A',
    'implementation freeze',
    'conditional B8',
    'StageFailureReportV1',
    'DisabledStageReportV1',
    'check_closure_claim_ceiling_v0_5.py',
]:
    if phrase not in plan:
        errors.append(f'plan_missing_phrase:{phrase}')
for phrase in [
    'Conditional B8 is not an escape hatch',
    'matrix record materialization -> causality reruns -> metrics/summaries',
    'StageFailureReportV1',
    'DisabledStageReportV1',
    'synthetic_closure` engine role name does not permit synthetic proof closure',
    'Closure is a separate artifact from the release report',
]:
    if phrase not in base:
        errors.append(f'base_missing_phrase:{phrase}')
for phrase in [
    'corpus_summary.counted_positive_formal_lean_tasks >= 1200',
    'corpus_summary.negative_target_outside_malformed_tasks >= 300',
    'corpus_summary.sealed_adversarial_holdout_count >= 700',
    'corpus_statement_diversity_summary.used_relation_families >= 8',
    'corpus_statement_diversity_summary.construction_case_certificate_required_tasks >= 350',
    'corpus_statement_diversity_summary.non_target_intermediate_required_tasks >= 600',
    'metrics_summary.construction_case_certificate_success_fraction >= 0.40',
    'used_rule_coverage_summary.used_concrete_non_identity_rules >= 25',
    'used_rule_coverage_summary.used_rule_families >= 10',
    'baseline_comparability_summary.B2_minus_B1_overall_advantage >= 0.15',
    'baseline_comparability_summary.conditional_b8_resolution_valid == true',
    'closure_claim_ceiling.allowed_final_claim',
    'forbidden_claims_present',
]:
    if phrase not in acceptance:
        errors.append(f'acceptance_missing_decision_check:{phrase}')
for phrase in [
    'A target fact with empty premises is never a counted success',
    'WP-11 — Actual matrix execution and baselines',
    'WP-12 — Live destructive solver causality reruns',
]:
    if phrase not in plan:
        errors.append(f'plan_missing_review_fix:{phrase}')
print({'status':'passed' if not errors else 'failed','errors':errors})
sys.exit(0 if not errors else 1)
