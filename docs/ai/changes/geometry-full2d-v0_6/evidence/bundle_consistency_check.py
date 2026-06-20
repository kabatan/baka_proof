from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = {
    'base': ROOT/'geometry_lean_guardian_BASE_SPEC_v0_6_execution_locked_full_pipeline.md',
    'plan': ROOT/'geometry_lean_guardian_PLAN_v0_6_execution_locked_full_pipeline.md',
    'acceptance': ROOT/'geometry_lean_guardian_ACCEPTANCE_v0_6_execution_locked_full_pipeline.md',
    'red': ROOT/'geometry_lean_guardian_RED_CASE_SUITE_v0_6.md',
    'invariants': ROOT/'geometry_lean_guardian_REAL_PIPELINE_INVARIANTS_v0_6.md',
    'handoff': ROOT/'geometry_lean_guardian_CODEX_HANDOFF_v0_6.md',
}
REQUIRED_ALL = [
    'MARP-GEOLEAN-BASE-012',
    'MARP-GEOLEAN-PLAN-012',
    'MARP-GEOLEAN-ACCEPTANCE-012',
    'V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY',
]
REQUIRED_BASE = [
    '--fresh-run', '--fail-on-stale', '--no-skip', '--all-baselines', '--live-mutations',
    'RC-015 Checker-generated success artifacts', 'RC-016 Static-only green release',
    'No target-fact provider', 'No proof-from-shape compiler', 'SolverCausalityLiveRunV1',
    'B1, B2, B5, B6, B7', 'check_acceptance_coverage_v0_6.py',
]
REQUIRED_ACCEPTANCE = [
    'K-034 Checker cannot fabricate pipeline evidence',
    'K-035 Release checker invokes all required checkers',
    'check_red_case_suite_v0_6.py --all',
    'run_full2d_matrix_v0_6.py --config ... --run-dir <fresh> --execute-all --all-baselines --no-skip',
    'run_solver_causality_live_v0_6.py --run-dir <fresh> --all-b2-successes',
]
FORBIDDEN = [
    'USER_APPROVED_ACTIVE_DRAFT',
    'geometry-full2d_v0_6',
    'optional bypass',
]

def check():
    errors=[]
    texts={k:p.read_text(encoding='utf-8') for k,p in FILES.items()}
    joined='\n'.join(texts.values())
    for p in FILES.values():
        if not p.exists(): errors.append(f'missing:{p.name}')
    for term in REQUIRED_ALL:
        for name,text in texts.items():
            if term not in text:
                errors.append(f'{name}:missing:{term}')
    for term in REQUIRED_BASE:
        if term not in texts['base']:
            errors.append(f'base:missing:{term}')
    for term in REQUIRED_ACCEPTANCE:
        if term not in texts['acceptance']:
            errors.append(f'acceptance:missing:{term}')
    for term in FORBIDDEN:
        if term in joined:
            errors.append(f'forbidden:{term}')
    # Ensure all RC labels in base are mirrored in red suite.
    for i in range(1,17):
        label=f'RC-{i:03d}'
        if label not in texts['base']:
            errors.append(f'base_missing_{label}')
        # red suite uses names not RC labels for all, so check Count by RedCase entries.
    if texts['red'].count('RedCase_') < 16:
        errors.append('red_suite_has_too_few_red_cases')
    # Ensure Plan has same final release flags as Acceptance.
    for flag in ['--fresh-run','--fail-on-stale','--no-skip','--all-baselines','--live-mutations']:
        if flag not in texts['plan'] or flag not in texts['acceptance']:
            errors.append(f'flag_missing_in_plan_or_acceptance:{flag}')
    return {'status':'passed' if not errors else 'failed','errors':errors}

if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
