---
title: AI Documentation Index
version: v0.4.5
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

### geometry-full2d-v0_4_5

Purpose: Guardian-managed v0.4.5 real solver-causal no-shortcuts Full2D pipeline track for a GeometryFull2D Lean automated prover.

Status: reviewed no-shortcuts research-agent bundle imported, hash-checked, self-consistency checked, and installed as the active user-approved Guardian authority set. Implementation work for WP-01 and later has not started.

Primary documents:

- `docs/ai/changes/geometry-full2d-v0_4_5/BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-010`.
- `docs/ai/changes/geometry-full2d-v0_4_5/PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-010`.
- `docs/ai/changes/geometry-full2d-v0_4_5/ACCEPTANCE.md` — acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-010`.
- `docs/ai/changes/geometry-full2d-v0_4_5/REAL_PIPELINE_INVARIANTS.md` — release-critical invariants.
- `docs/ai/changes/geometry-full2d-v0_4_5/REFACTOR_DIRECTIVE.md` — v0.4.4 shortcut quarantine and replacement directive.
- `docs/ai/changes/geometry-full2d-v0_4_5/SOURCE_MAP.md` — traceability aid.
- `docs/ai/changes/geometry-full2d-v0_4_5/CODEX_HANDOFF.md` — implementation handoff.
- `docs/ai/changes/geometry-full2d-v0_4_5/SELF_REVIEW_LOG.md` — reviewed bundle self-review log.
- `docs/ai/changes/geometry-full2d-v0_4_5/FAILURE_ANALYSIS.md` — failure analysis motivating v0.4.5.
- `docs/ai/changes/geometry-full2d-v0_4_5/README.md` — change-local index.
- `docs/ai/changes/geometry-full2d-v0_4_5/evidence/` — import evidence.
- `docs/ai/changes/geometry-full2d-v0_4_5/debt/debt_ledger.jsonl` — debt ledger.

First command:

```bash
python scripts/check_active_guardian_spec_v0_4_5.py
```

## Superseded Geometry Tracks

These tracks are retained as historical evidence, negative evidence, and safety background. They are not active v0.4.5 release authority for new work.

### geometry-full2d-v0_4_4

Purpose: Previous real solver-causal pipeline track.

Status: v0.4.4 release acceptance passed for its scoped claim, but it is superseded by `MARP-GEOLEAN-BASE-010`; retained as historical evidence and as a regression source. It is not active v0.4.5 release authority.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_4/`

### geometry-full2d-v0_4_3

Purpose: Previous integrated real-pipeline track.

Status: v0.4.3 release acceptance passed for its scoped claim, but it is superseded by later GeometryFull2D tracks; retained as historical evidence and as a regression source. It is not active v0.4.5 release authority.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_3/`

### geometry-full2d-v0_4_2

Purpose: Previous governed Full2D implementation track.

Status: superseded by later GeometryFull2D tracks; retained only as evidence and as a regression source. v0.4.2 release reports are not active release evidence.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_2/`

### geometry-lean-v0_3

Purpose: Original Guardian-managed implementation track for the geometry x Lean v0.3 mathematical auto-research pipeline.

Status: superseded by later GeometryFull2D tracks; retained for historical evidence only.

Location:

- `docs/ai/changes/geometry-lean-v0_3/`

### geometry-lean-v0_3A

Purpose: v0.3A recovery track for real provider integration and limited real LeanGeo corpus evidence.

Status: superseded by later GeometryFull2D tracks; retained for historical evidence only.

Locations:

- `docs/ai/archive/geometry_pre_v0_4_2/specs/MARP-GEOLEAN-BASE-003A.md`
- `docs/ai/archive/geometry_pre_v0_4_2/plans/MARP-GEOLEAN-PLAN-003A.md`
- `docs/ai/changes/geometry-lean-v0_3a/`

### geometry-lean-v0_3-full-rebase

Purpose: Full v0.3 experiment-ready rebase track, later amended by v0.3A and v0.3B patches.

Status: superseded by later GeometryFull2D tracks; retained for historical evidence only.

Location:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/`

## Archive Staging

- `docs/ai/archive/geometry_pre_v0_4_2/` — retained archive location for older geometry Guardian authority documents.

## Architecture Documents

- `docs/architecture/geometry_lean_pipeline.md`
- `docs/architecture/target_subset_contract.md`
- `docs/architecture/compiler_contract.md`
- `docs/architecture/run_trace_contract.md`
- `docs/architecture/trust_model_geometry.md`
- `docs/architecture/proof_state_dag.md`
- `docs/architecture/no_loose_options.md`

## Source Mirrors

- `docs/architecture/geometry_lean_pipeline.md` — mirror of the earlier user-provided v0.3 project plan. It is no longer the active v0.4.5 authority.
