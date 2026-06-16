---
title: AI Documentation Index
version: v0.3
status: ACTIVE
created: 2026-06-11
last_updated: 2026-06-16
purpose: Index active Guardian and AI-operation documents in this workspace.
authority: Navigation and classification only; individual Base Spec and Plan files declare their own authority.
---

# AI Documentation Index

## Active Context

- `docs/ai/ACTIVE_CONTEXT.md` — minimal navigation state. It is not an authority source.

## Active Change

### geometry-full2d-v0_4_3

Purpose: Guardian-managed v0.4.3 real pipeline recovery track for a solver-backed GeometryFull2D Lean automated prover.

Status: v0.4.3 integrated research-agent bundle imported, hash-verified, and installed as the active user-approved Guardian authority set. Implementation has advanced through real-pipeline hardening and matrix-run infrastructure, but strict spec verification currently blocks release closure on corpus duplicate and direct-lemma success ceilings. No v0.4.3 completion claim is made.

Primary documents:

- `docs/ai/changes/geometry-full2d-v0_4_3/BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-008`.
- `docs/ai/changes/geometry-full2d-v0_4_3/PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-008`.
- `docs/ai/changes/geometry-full2d-v0_4_3/ACCEPTANCE.md` — acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-008`.
- `docs/ai/changes/geometry-full2d-v0_4_3/REAL_PIPELINE_INVARIANTS.md` — anti-template and causal evidence invariants.
- `docs/ai/changes/geometry-full2d-v0_4_3/REFACTOR_DIRECTIVE.md` — repository refactor directive.
- `docs/ai/changes/geometry-full2d-v0_4_3/SOURCE_MAP.md` — traceability aid.
- `docs/ai/changes/geometry-full2d-v0_4_3/CODEX_HANDOFF.md` — implementation handoff.
- `docs/ai/changes/geometry-full2d-v0_4_3/README.md` — change-local index.
- `docs/ai/changes/geometry-full2d-v0_4_3/evidence/` — import and implementation evidence.
- `docs/ai/changes/geometry-full2d-v0_4_3/evidence/v0_4_3_release_blocker_report.md` — current release blocker report.
- `docs/ai/changes/geometry-full2d-v0_4_3/debt/debt_ledger.jsonl` — debt ledger.

## Superseded Geometry Tracks

These tracks are retained as historical evidence, negative evidence, and safety background. They are not active release authority for new v0.4.3 work.

### geometry-full2d-v0_4_2

Purpose: Previous governed Full2D implementation track.

Status: superseded by `MARP-GEOLEAN-BASE-008`; retained only as evidence and as the regression source for the v0.4.3 anti-v0.4.2 checks. v0.4.2 release reports are not active v0.4.3 release evidence.

Location:

- `docs/ai/changes/geometry-full2d-v0_4_2/`

### geometry-lean-v0_3

Purpose: Original Guardian-managed implementation track for the geometry x Lean v0.3 mathematical auto-research pipeline.

Status: superseded by `MARP-GEOLEAN-BASE-008`; retained for historical evidence only.

Location:

- `docs/ai/changes/geometry-lean-v0_3/`

### geometry-lean-v0_3A

Purpose: v0.3A recovery track for real provider integration and limited real LeanGeo corpus evidence.

Status: superseded by `MARP-GEOLEAN-BASE-008`; retained for historical evidence only.

Locations:

- `docs/ai/archive/geometry_pre_v0_4_2/specs/MARP-GEOLEAN-BASE-003A.md`
- `docs/ai/archive/geometry_pre_v0_4_2/plans/MARP-GEOLEAN-PLAN-003A.md`
- `docs/ai/changes/geometry-lean-v0_3a/`

### geometry-lean-v0_3-full-rebase

Purpose: Full v0.3 experiment-ready rebase track, later amended by v0.3A and v0.3B patches.

Status: v0.3B solver-backed readiness evidence is retained, but this track is superseded by `MARP-GEOLEAN-BASE-008` for new release work.

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

- `docs/architecture/geometry_lean_pipeline.md` — mirror of the earlier user-provided v0.3 project plan. It is no longer the active v0.4.3 authority.
