---
title: AI Documentation Index
version: v0.1
status: ACTIVE
created: 2026-06-11
purpose: Index active Guardian and AI-operation documents in this workspace.
authority: Navigation and classification only; individual Base Spec and Plan files declare their own authority.
---

# AI Documentation Index

## Active Context

- `docs/ai/ACTIVE_CONTEXT.md` — minimal navigation state. It is not an authority source.

## Active Changes

### geometry-lean-v0_3

Purpose: Guardian-managed implementation track for the geometry × Lean v0.3 mathematical auto-research pipeline.

Status: fixture-level release acceptance and final reviews passed; full v0.3 completion is blocked by real-integration and corpus evidence ceilings.

Primary documents:

- `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md` — correctness authority after admission and user approval.
- `docs/ai/changes/geometry-lean-v0_3/PLAN.md` — execution contract after admission and user approval.
- `docs/ai/changes/geometry-lean-v0_3/source_map.md` — source-to-R-ID traceability aid.
- `docs/ai/changes/geometry-lean-v0_3/RESOURCE_POLICY.md` — companion local resource policy template.
- `docs/ai/changes/geometry-lean-v0_3/REVIEW_PACKET.md` — review scope and evidence index for Guardian reviewers.
- `docs/ai/changes/geometry-lean-v0_3/CLOSURE_TEMPLATE.md` — final closure template for future implementation work.
- `docs/ai/changes/geometry-lean-v0_3/evidence/v03_completion_blocker_report.md` — blocker report for full v0.3 completion.

### geometry-lean-v0_3A

Purpose: Guardian-managed recovery track for resolving v0.3 completion blockers through real provider integration and a limited real LeanGeo corpus.

Status: final reviews passed for limited real-integration evidence only. This does not claim full v0.3 completion, real Level 2 advantage, arbitrary LeanGeo support, production safety, source-faithfulness, acceptance-completeness, or R-ID VERIFIED status.

Primary documents:

- `docs/ai/specs/MARP-GEOLEAN-BASE-003A.md` — candidate recovery correctness authority after admission.
- `docs/ai/plans/MARP-GEOLEAN-PLAN-003A.md` — candidate recovery execution contract after admission.
- `docs/ai/changes/geometry-lean-v0_3a/source_map.md` — source-to-R-ID traceability aid.
- `docs/ai/changes/geometry-lean-v0_3a/README.md` — recovery change index.
- `docs/ai/changes/geometry-lean-v0_3a/evidence/` — recovery evidence.

### geometry-lean-v0_3-full-rebase

Purpose: Guardian-managed full v0.3 experiment-ready rebase track targeting `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`.

Status: Base Spec/Plan Guardian-admitted and user-approved. v0.3A patch is installed and user-approved. T45 release acceptance hardening is complete; T46 final replay and closure is ready.

Primary documents:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md` — correctness authority for `MARP-GEOLEAN-BASE-004`, amended by `MARP-GEOLEAN-BASE-004A`.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md` — execution contract for `MARP-GEOLEAN-PLAN-004`, amended by `MARP-GEOLEAN-PLAN-004A`.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md` — active Base Spec patch `MARP-GEOLEAN-BASE-004A`.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md` — active Plan patch `MARP-GEOLEAN-PLAN-004A`.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md` — active acceptance patch.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md` — source-to-requirement traceability aid.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md` — repository cleanup directive for the rebase.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/ACCEPTANCE_MATRIX.md` — final acceptance evidence and command matrix.
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/` — import, review, approval, and implementation evidence.

Architecture documents:

- `docs/architecture/geometry_lean_pipeline.md`
- `docs/architecture/target_subset_contract.md`
- `docs/architecture/compiler_contract.md`
- `docs/architecture/run_trace_contract.md`
- `docs/architecture/trust_model_geometry.md`
- `docs/architecture/proof_state_dag.md`
- `docs/architecture/no_loose_options.md`

Decision records:

- `docs/decision_records/DR-GEO-001-target-leangeo-subset.md`
- `docs/decision_records/DR-GEO-002-no-agent-cd-core.md`
- `docs/decision_records/DR-GEO-003-extraction-first.md`
- `docs/decision_records/DR-GEO-004-geotrace-not-proof.md`
- `docs/decision_records/DR-GEO-005-aux-construction-contract.md`
- `docs/decision_records/DR-GEO-006-run-attribution-logs.md`

Evidence:

- `docs/ai/changes/geometry-lean-v0_3/evidence/`
- Current non-Git hash snapshot: `docs/ai/changes/geometry-lean-v0_3/evidence/source_hashes_after_source_fidelity_review.md`

## Source Mirrors

- `docs/architecture/geometry_lean_pipeline.md` — mirror of the user-provided v0.3 project plan.
