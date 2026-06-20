---
title: AI Documentation Index
version: v0.6
status: ACTIVE
created: 2026-06-11
last_updated: 2026-06-20
purpose: Index active Guardian and AI-operation documents in this workspace.
authority: Navigation and classification only; individual Base Spec and Plan files declare their own authority.
---

# AI Documentation Index

## Active Context

- `docs/ai/ACTIVE_CONTEXT.md` - minimal navigation state. It is not an authority source.

## Active Change

### geometry-full2d-v0_6

Purpose: Guardian-managed v0.6 reviewed-strict execution-locked correction track for the GeometryFull2D real solver-causal full pipeline.

Status: imported from the reviewed-strict research-agent bundle and installed as the active user-approved Guardian authority set. WP00 authority installation is in progress. No v0.6 release completion is claimed.

Primary documents:

- `docs/ai/changes/geometry-full2d-v0_6/BASE_SPEC.md` - correctness authority for `MARP-GEOLEAN-BASE-012`.
- `docs/ai/changes/geometry-full2d-v0_6/PLAN.md` - execution contract for `MARP-GEOLEAN-PLAN-012`.
- `docs/ai/changes/geometry-full2d-v0_6/ACCEPTANCE.md` - acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-012`.
- `docs/ai/changes/geometry-full2d-v0_6/RED_CASE_SUITE.md` - required generalized shortcut red-case suite.
- `docs/ai/changes/geometry-full2d-v0_6/REAL_PIPELINE_INVARIANTS.md` - release-critical invariants.
- `docs/ai/changes/geometry-full2d-v0_6/REFACTOR_DIRECTIVE.md` - strict recovery directive.
- `docs/ai/changes/geometry-full2d-v0_6/SOURCE_MAP.md` - traceability aid.
- `docs/ai/changes/geometry-full2d-v0_6/CODEX_HANDOFF.md` - implementation handoff.
- `docs/ai/changes/geometry-full2d-v0_6/SELF_REVIEW_LOG.md` - reviewed bundle self-review log.
- `docs/ai/changes/geometry-full2d-v0_6/FAILURE_ANALYSIS.md` - failure class analysis.
- `docs/ai/changes/geometry-full2d-v0_6/README.md` - change-local index.
- `docs/ai/changes/geometry-full2d-v0_6/evidence/` - import, review, and WP implementation evidence.
- `docs/ai/changes/geometry-full2d-v0_6/debt/debt_ledger.jsonl` - debt ledger.

First commands:

```bash
python scripts/check_active_guardian_spec_v0_6.py
python scripts/check_v0_6_spec_plan_consistency.py
```

## Superseded Geometry Tracks

These tracks are retained as historical evidence, negative evidence, regression sources, and safety background. They are not active v0.6 release authority for new work.

### geometry-full2d-v0_5

Purpose: Previous reviewed-strict real solver-causal recovery track.

Status: superseded by `MARP-GEOLEAN-BASE-012` / `PLAN-012` / `ACCEPTANCE-012`. Retained as prior implementation evidence and failure-analysis context, not as active v0.6 release authority or closure evidence.

Location:

- `docs/ai/changes/geometry-full2d-v0_5/`

### geometry-full2d-v0_4_5

Purpose: Previous no-shortcuts recovery attempt.

Status: false-positive closure invalidated by later GeometryFull2D authority; retained as negative evidence and a source of red cases. It is not active v0.6 release authority.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_5/`

### geometry-full2d-v0_4_4

Purpose: Previous real solver-causal pipeline track.

Status: superseded by later GeometryFull2D tracks; retained as historical evidence and as a regression source.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_4/`

### geometry-full2d-v0_4_3

Purpose: Previous integrated real-pipeline track.

Status: superseded by later GeometryFull2D tracks; retained as historical evidence and as a regression source.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_3/`

### Older geometry tracks

Older `geometry-*` and `geometry-full2d-*` change directories remain historical evidence unless explicitly referenced by the active v0.6 Base Spec or Plan.
