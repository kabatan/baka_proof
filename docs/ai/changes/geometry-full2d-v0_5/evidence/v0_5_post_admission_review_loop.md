# v0.5 Post-Admission Review Loop

Status: review fixes applied; implementation has not started beyond authority preparation.

Date: 2026-06-18

## Scope

The review checked whether `PLAN.md` necessarily forces `BASE_SPEC.md`, whether Acceptance covers all release-critical requirements, and whether the documents leave room for shortcut closure.

## Findings Fixed

1. Acceptance explicitly listed only a subset of Base Spec corpus floors, diversity floors, release thresholds, rule coverage, and baseline advantage thresholds.
2. Matrix execution and causality ordering was inconsistent. The authority now separates matrix record materialization from metrics: matrix execution discovers B2 final-theorem successes, causality reruns those successes, and metrics/summaries are computed after causality.
3. Sealed holdout timing was ambiguous. WP-04 now implements generators/checkers only; WP-10A creates an implementation freeze and then materializes counted SealedAdversarialHoldout tasks.
4. Provider target-fact language could allow empty-premise target facts if independently certified. PLAN now says empty-premise target facts are never counted success.
5. Baseline schema could force fake placeholder artifacts for disabled or failing baselines. BASE_SPEC now defines content-addressed `StageFailureReportV1` and `DisabledStageReportV1` and forbids null refs in final release records.
6. Conditional B8 could be silently omitted. BASE_SPEC / PLAN / ACCEPTANCE now require explicit B8 resolution and checker evidence.
7. Closure could be treated as implied by the release report. BASE_SPEC / PLAN / ACCEPTANCE now require `check_closure_claim_ceiling_v0_5.py` before and after `CLOSURE.md`.

## Review Result

`guardian_boundary_reviewer` re-review result:

```text
RESULT: PASS
No remaining blocker/fixable Base Spec / Plan / Acceptance consistency issues found in the re-review scope.
```

Checks reported by the reviewer:

```text
python scripts/check_v0_5_spec_plan_consistency.py docs/ai/changes/geometry-full2d-v0_5
python scripts/check_active_guardian_spec_v0_5.py
```

## Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-011 / PLAN-011 / ACCEPTANCE-011 have been tightened by post-admission review and can be used to begin WP-01 implementation.
```

Not allowed:

```text
V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
