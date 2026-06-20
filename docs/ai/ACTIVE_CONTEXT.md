---
title: Guardian Active Context - GeometryFull2D v0.6
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-012
version: v0.6-execution-locked-reviewed-strict
status: USER_APPROVED_ACTIVE
created: 2026-06-20
last_updated: 2026-06-20
base_spec: MARP-GEOLEAN-BASE-012
plan: MARP-GEOLEAN-PLAN-012
acceptance: MARP-GEOLEAN-ACCEPTANCE-012
purpose: Minimal navigation state for the active GeometryFull2D v0.6 Guardian execution-locked correction track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, invariants, evidence, or user approval state.
---

# Guardian Active Context - GeometryFull2D v0.6

## Status

Guardian Lane is active for the GeometryFull2D v0.6 reviewed-strict execution-locked real solver-causal full pipeline correction track.

Current mission:

```text
Implement V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY under MARP-GEOLEAN-BASE-012 / PLAN-012 / ACCEPTANCE-012.
```

The active work is not to make a release checker green first. The active work is to build the real pipeline required by the v0.6 authority set, beginning with shortcut red-case rejection and then implementing each real pipeline stage.

Prior v0.4.x and v0.5 tracks are retained as historical evidence, regression sources, and failure-analysis context only. They are not active v0.6 release authority and cannot be used as closure evidence for v0.6.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_6/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_6/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_6/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_6/RED_CASE_SUITE.md`
5. `docs/ai/changes/geometry-full2d-v0_6/REAL_PIPELINE_INVARIANTS.md`
6. `docs/ai/changes/geometry-full2d-v0_6/REFACTOR_DIRECTIVE.md`
7. `docs/ai/changes/geometry-full2d-v0_6/CODEX_HANDOFF.md`
8. `docs/ai/changes/geometry-full2d-v0_6/FAILURE_ANALYSIS.md`
9. `docs/ai/changes/geometry-full2d-v0_6/SOURCE_MAP.md`
10. Current Plan work package and required source anchors.
11. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP00 - Install v0.6 authority and invalidate earlier closures.
```

Completed preparation:

```text
v0.6 reviewed-strict research-agent bundle imported.
Bundle self-consistency checker passed before import.
RED_CASE_SUITE.md normalized to list RC-001 through RC-019 from MARP-GEOLEAN-BASE-012.
Active context and index point to v0.6.
v0.5 authority is superseded as historical prior evidence; v0.5 files are not active release authority.
v0.6 active authority and consistency checkers are installed.
```

## Claim Ceiling

Allowed now:

```text
v0.6 authority has been imported and the workspace is prepared to begin implementation under WP01 after admission checks pass.
```

Forbidden until the final v0.6 fresh release command passes:

```text
full pipeline completed
real solver-causal pipeline ready
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
```

## First Checks

```bash
python scripts/check_active_guardian_spec_v0_6.py
python scripts/check_v0_6_spec_plan_consistency.py
```
