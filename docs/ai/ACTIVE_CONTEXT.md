---
title: Guardian Active Context — GeometryFull2D v0.4.4
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-009
version: v0.4.4-real-solver-causal
status: USER_APPROVED_ACTIVE
created: 2026-06-18
last_updated: 2026-06-18
base_spec: MARP-GEOLEAN-BASE-009
plan: MARP-GEOLEAN-PLAN-009
acceptance: MARP-GEOLEAN-ACCEPTANCE-009
purpose: Minimal navigation state for the active GeometryFull2D v0.4.4 Guardian track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, invariants, evidence, or user approval state.
---

# Guardian Active Context — GeometryFull2D v0.4.4

## Status

Guardian Lane is active for the GeometryFull2D v0.4.4 real solver-causal pipeline track.

Current mission:

```text
Implement V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY under MARP-GEOLEAN-BASE-009 / PLAN-009 / ACCEPTANCE-009.
```

The v0.4.3 track is superseded for new release claims. It remains historical evidence and a regression source only; it is not active v0.4.4 release authority.

## Implementation Permission

The current user request approved importing the reviewed research-agent v0.4.4 Guardian bundle and preparing the workspace so implementation can begin.

Import evidence is recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_4/evidence/v0_4_4_bundle_import.md
```

Before editing implementation code for WP01 and later, read the current Plan task, required source anchors, admitted ReadSet, changed files, and the current v0.4.4 claim ceiling.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_4_4/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_4_4/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_4_4/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_4_4/REAL_PIPELINE_INVARIANTS.md`
5. `docs/ai/changes/geometry-full2d-v0_4_4/REFACTOR_DIRECTIVE.md`
6. `docs/ai/changes/geometry-full2d-v0_4_4/SOURCE_MAP.md`
7. `docs/ai/changes/geometry-full2d-v0_4_4/README.md`
8. `docs/ai/changes/geometry-full2d-v0_4_4/CODEX_HANDOFF.md`
9. `docs/ai/changes/geometry-full2d-v0_4_4/SELF_REVIEW_LOG.md`
10. `docs/ai/changes/geometry-full2d-v0_4_4/FAILURE_ANALYSIS.md`
11. Current Plan work package and required source anchors.
12. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP00 — Authority reset and work-start preparation.
```

Completed preparation:

```text
v0.4.4 reviewed research-agent bundle imported.
Bundle hashes checked.
Bundle self-consistency check passed.
Active context and index updated to point to v0.4.4.
v0.4.3 Guardian docs marked superseded for v0.4.4 release claims.
v0.4.4 debt ledger initialized.
scripts/check_active_guardian_spec_v0_4_4.py added for authority checks.
```

Implementation work for WP01 and later has not started.

## Non-Negotiables

- Do not close from v0.4.3 release evidence.
- Do not count projection-only tasks as release positives.
- Do not relabel Codex-generated tasks as `UserReviewedGoal`.
- Do not require user-reviewed tasks as a release blocker when absent.
- Do not select proof text from `task_id`, `template_id`, `theorem_family`, `grammar_family`, difficulty, provenance, source refs, or generator-private labels.
- Do not fabricate solver refs.
- Do not count any positive theorem without `ActualTaskPipelineRunV2` and `SolverCausalityReportV1`.
- Do not let engine outputs contain Lean proof text, tactic scripts, theorem-specific proof replacements, or target theorem names used for proof generation.
- Do not claim a solver-causal success if removing or corrupting the selected solver artifact still accepts the same proof patch.
- Do not require B8 unless a model provider is enabled.
- Stop only for HardBlockers HB-01 through HB-09 in the active Base Spec.

## Evidence Folder

```text
docs/ai/changes/geometry-full2d-v0_4_4/evidence/
```

## Current Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-009 / PLAN-009 / ACCEPTANCE-009 are installed as the active v0.4.4 Guardian authority set, and implementation can begin from WP01.
```

Not allowed yet:

```text
V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
