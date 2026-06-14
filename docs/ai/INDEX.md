---
title: AI Documentation Index
version: v0.2
status: ACTIVE
created: 2026-06-11
last_updated: 2026-06-15
purpose: Index active Guardian and AI-operation documents in this workspace.
authority: Navigation and classification only; individual Base Spec and Plan files declare their own authority.
---

# AI Documentation Index

## Active Context

- `docs/ai/ACTIVE_CONTEXT.md` — minimal navigation state. It is not an authority source.

## Active Change

### geometry-full2d-v0_4_2

Purpose: Guardian-managed v0.4.2 governed full implementation track for a GeometryFull2D Lean automated prover.

Status: v0.4.2 research-agent bundle imported, hash-verified, and installed as the active user-approved Guardian authority set. Implementation can begin at WP-00. No v0.4.2 completion claim is made.

Primary documents:

- `docs/ai/changes/geometry-full2d-v0_4_2/BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-007`.
- `docs/ai/changes/geometry-full2d-v0_4_2/PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-007`.
- `docs/ai/changes/geometry-full2d-v0_4_2/ACCEPTANCE.md` — acceptance authority for `MARP-GEOLEAN-ACCEPTANCE-007`.
- `docs/ai/changes/geometry-full2d-v0_4_2/ENGINE_CONTRACTS.md` — required engine role contracts.
- `docs/ai/changes/geometry-full2d-v0_4_2/BLOCKER_AND_DEBT_POLICY.md` — mandatory continue-on-debt and HardBlocker policy.
- `docs/ai/changes/geometry-full2d-v0_4_2/REFACTOR_DIRECTIVE.md` — repository refactor directive.
- `docs/ai/changes/geometry-full2d-v0_4_2/SOURCE_MAP.md` — traceability aid.
- `docs/ai/changes/geometry-full2d-v0_4_2/README.md` — change-local index.
- `docs/ai/changes/geometry-full2d-v0_4_2/evidence/` — import and implementation evidence.
- `docs/ai/changes/geometry-full2d-v0_4_2/debt/debt_ledger.jsonl` — debt ledger.

## Superseded Geometry Tracks

These tracks are retained as historical evidence and safety background. They are not active release authority for new v0.4.2 work.

### geometry-lean-v0_3

Purpose: Original Guardian-managed implementation track for the geometry x Lean v0.3 mathematical auto-research pipeline.

Status: superseded by `MARP-GEOLEAN-BASE-007`; retained for historical evidence only.

Location:

- `docs/ai/changes/geometry-lean-v0_3/`

### geometry-lean-v0_3A

Purpose: v0.3A recovery track for real provider integration and limited real LeanGeo corpus evidence.

Status: superseded by `MARP-GEOLEAN-BASE-007`; retained for historical evidence only.

Locations:

- `docs/ai/archive/geometry_pre_v0_4_2/specs/MARP-GEOLEAN-BASE-003A.md`
- `docs/ai/archive/geometry_pre_v0_4_2/plans/MARP-GEOLEAN-PLAN-003A.md`
- `docs/ai/changes/geometry-lean-v0_3a/`

### geometry-lean-v0_3-full-rebase

Purpose: Full v0.3 experiment-ready rebase track, later amended by v0.3A and v0.3B patches.

Status: v0.3B solver-backed readiness evidence is retained, but this track is superseded by `MARP-GEOLEAN-BASE-007` for new release work.

Location:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/`

## Archive Staging

- `docs/ai/archive/geometry_pre_v0_4_2/` — reserved archive location for older geometry Guardian authority documents. Physical archival is WP-00 implementation work because current scripts and tests still reference older evidence paths.

## Architecture Documents

- `docs/architecture/geometry_lean_pipeline.md`
- `docs/architecture/target_subset_contract.md`
- `docs/architecture/compiler_contract.md`
- `docs/architecture/run_trace_contract.md`
- `docs/architecture/trust_model_geometry.md`
- `docs/architecture/proof_state_dag.md`
- `docs/architecture/no_loose_options.md`

## Source Mirrors

- `docs/architecture/geometry_lean_pipeline.md` — mirror of the earlier user-provided v0.3 project plan. It is no longer the active v0.4.2 authority.
