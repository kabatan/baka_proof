---
title: Guardian Active Context — GeometryFull2D v0.5
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-011
version: v0.5-real-solver-causal-reviewed-strict
status: USER_APPROVED_ACTIVE
created: 2026-06-18
last_updated: 2026-06-18
base_spec: MARP-GEOLEAN-BASE-011
plan: MARP-GEOLEAN-PLAN-011
acceptance: MARP-GEOLEAN-ACCEPTANCE-011
purpose: Minimal navigation state for the active GeometryFull2D v0.5 Guardian recovery track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, invariants, evidence, or user approval state.
---

# Guardian Active Context — GeometryFull2D v0.5

## Status

Guardian Lane is active for the GeometryFull2D v0.5 reviewed-strict real solver-causal full pipeline correction track.

Current mission:

```text
Implement V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY under MARP-GEOLEAN-BASE-011 / PLAN-011 / ACCEPTANCE-011.
```

The v0.4.5 closure is invalidated as a false-positive checker-passing scaffold. It remains negative evidence and a red-case source only; it is not active release authority.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_5/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_5/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_5/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_5/RED_CASE_SUITE.md`
5. `docs/ai/changes/geometry-full2d-v0_5/REAL_PIPELINE_INVARIANTS.md`
6. `docs/ai/changes/geometry-full2d-v0_5/REFACTOR_DIRECTIVE.md`
7. `docs/ai/changes/geometry-full2d-v0_5/CODEX_HANDOFF.md`
8. `docs/ai/changes/geometry-full2d-v0_5/FAILURE_ANALYSIS.md`
9. Current Plan work package and required source anchors.
10. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP-04 — Corpus system without proof coupling.
```

Completed preparation:

```text
v0.5 reviewed-strict research-agent bundle imported.
Bundle self-consistency check passed.
Active context and index updated to point to v0.5.
v0.4.5 Guardian authority and closure marked superseded/invalidated as false-positive closure evidence.
v0.5 debt ledger initialized.
Post-admission review loop found fixable Plan/Base/Acceptance alignment gaps and patched them:
  - full Base Spec floor/threshold decision checks;
  - matrix execution before causality, metrics after causality;
  - sealed holdout after implementation freeze;
  - no empty-premise target fact counted success;
  - explicit disabled/failing baseline reports;
  - conditional B8 and closure claim ceiling checks.
WP-01 red-case suite implemented with 19 executable red cases, each with static-code and artifact-run variants.
WP-02 fail-closed acceptance harness, K coverage checker, and checker-suppression guard implemented.
WP-02 evidence captured in docs/ai/changes/geometry-full2d-v0_5/evidence/wp01_wp02_redcase_acceptance_harness.md and wp02_release_acceptance_smoke.json.
WP-03 schema validators implemented with positive/negative self-tests for required v0.5 artifact schemas.
```

Implementation work for WP-04 and later has not started.

## Non-Negotiables

- Do not implement another report-shaped pipeline.
- Do not target green acceptance first.
- Implement red cases and acceptance coverage before provider/compiler/rule implementation.
- Do not use v0.4.5 closure or run records as v0.5 success evidence.
- Do not suppress checker findings by filename, role, or release path.
- Do not count target-fact providers, naked target assertions, identity rules, proof-from-shape compilers, report-only causality, family-coded baselines, or stale evidence.

## Evidence Folder

```text
docs/ai/changes/geometry-full2d-v0_5/evidence/
```

## Current Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-011 / PLAN-011 / ACCEPTANCE-011 are installed as the active v0.5 Guardian authority set, and recovery implementation can begin from WP-00/WP-01.
```

Not allowed yet:

```text
V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
