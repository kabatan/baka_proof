---
title: AI Documentation Index
version: v0.5
status: ACTIVE
created: 2026-06-11
last_updated: 2026-06-18
purpose: Index active Guardian and AI-operation documents in this workspace.
authority: Navigation and classification only; individual Base Spec and Plan files declare their own authority.
---

# AI Documentation Index

## Active Context

- `docs/ai/ACTIVE_CONTEXT.md` — minimal navigation state. It is not an authority source.

## Active Change

### geometry-full2d-v0_5

Purpose: Guardian-managed v0.5 reviewed-strict recovery track for the GeometryFull2D real solver-causal full pipeline.

Status: imported from the reviewed-strict research-agent bundle and installed as the active user-approved Guardian authority set. WP-01 through WP-06 gates are implemented; implementation proceeds from WP-07. No v0.5 release completion is claimed.

Primary documents:

- `docs/ai/changes/geometry-full2d-v0_5/BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-011`.
- `docs/ai/changes/geometry-full2d-v0_5/PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-011`.
- `docs/ai/changes/geometry-full2d-v0_5/ACCEPTANCE.md` — acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-011`.
- `docs/ai/changes/geometry-full2d-v0_5/RED_CASE_SUITE.md` — required shortcut red-case suite.
- `docs/ai/changes/geometry-full2d-v0_5/REAL_PIPELINE_INVARIANTS.md` — release-critical invariants.
- `docs/ai/changes/geometry-full2d-v0_5/REFACTOR_DIRECTIVE.md` — strict recovery directive.
- `docs/ai/changes/geometry-full2d-v0_5/SOURCE_MAP.md` — traceability aid.
- `docs/ai/changes/geometry-full2d-v0_5/CODEX_HANDOFF.md` — implementation handoff.
- `docs/ai/changes/geometry-full2d-v0_5/SELF_REVIEW_LOG.md` — reviewed bundle self-review log.
- `docs/ai/changes/geometry-full2d-v0_5/FAILURE_ANALYSIS.md` — false-positive closure analysis.
- `docs/ai/changes/geometry-full2d-v0_5/README.md` — change-local index.
- `docs/ai/changes/geometry-full2d-v0_5/evidence/` — import, review, and WP implementation evidence.
- `docs/ai/changes/geometry-full2d-v0_5/debt/debt_ledger.jsonl` — debt ledger.

First commands:

```bash
python scripts/check_active_guardian_spec_v0_5.py
python scripts/check_v0_5_spec_plan_consistency.py docs/ai/changes/geometry-full2d-v0_5
```

## Superseded Geometry Tracks

These tracks are retained as historical evidence, negative evidence, and safety background. They are not active v0.5 release authority for new work.

### geometry-full2d-v0_4_5

Purpose: Previous no-shortcuts recovery attempt.

Status: false-positive closure invalidated by `MARP-GEOLEAN-BASE-011`; retained as negative evidence and a source of red cases. It is not active v0.5 release authority.

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

### geometry-full2d-v0_4_2

Purpose: Previous governed Full2D implementation track.

Status: superseded by later GeometryFull2D tracks; retained only as evidence and as a regression source.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_2/`

### geometry-lean-v0_3 and related tracks

Purpose: Earlier geometry x Lean automated research tracks.

Status: superseded by later GeometryFull2D tracks; retained for historical evidence only.

Locations:

- `docs/ai/changes/geometry-lean-v0_3/`
- `docs/ai/changes/geometry-lean-v0_3a/`
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/`
- `docs/ai/archive/geometry_pre_v0_4_2/`

## Architecture Documents

- `docs/architecture/geometry_lean_pipeline.md`
- `docs/architecture/target_subset_contract.md`
- `docs/architecture/compiler_contract.md`
- `docs/architecture/run_trace_contract.md`
- `docs/architecture/trust_model_geometry.md`
- `docs/architecture/proof_state_dag.md`
- `docs/architecture/no_loose_options.md`
