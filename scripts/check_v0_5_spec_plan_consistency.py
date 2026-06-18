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
    'GoalPreservationSelfAttestation', 'ProviderImportsCompiler'
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
for phrase in ['--fresh-run','check_acceptance_coverage_v0_5.py','check_no_checker_whitelist_v0_5.py','check_corpus_statement_diversity_v0_5.py']:
    if phrase not in acceptance:
        errors.append(f'acceptance_missing_phrase:{phrase}')
print({'status':'passed' if not errors else 'failed','errors':errors})
sys.exit(0 if not errors else 1)
