---
title: Source Fidelity Audit — v0.3 Guardian Documents
created: 2026-06-11
status: REVIEW_PASSED
purpose: Record the audit of Guardian documents against `geometry_lean_pipeline_plan_v0_3.md`.
authority: Evidence only; does not grant user implementation approval and does not mark R-IDs VERIFIED.
---

# Source Fidelity Audit — v0.3 Guardian Documents

## Scope

Source checked:

- `geometry_lean_pipeline_plan_v0_3.md`

Guardian documents corrected:

- `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md`
- `docs/ai/changes/geometry-lean-v0_3/PLAN.md`
- `docs/ai/changes/geometry-lean-v0_3/source_map.md`
- `docs/ai/changes/geometry-lean-v0_3/README.md`
- `docs/ai/INDEX.md`
- `docs/ai/ACTIVE_CONTEXT.md`

## Findings and Fixes

### FID-001 — v0.3 contract details were summarized too broadly

Finding: The Base Spec covered the major v0.3 design boundaries, but did not explicitly preserve every detailed v0.3 schema family, field group, workflow, release blocker, and final checklist item.

Fix: Added `R-V03-*` source-fidelity overlay requirements to `BASE_SPEC.md` and assigned them to implementation tasks in `PLAN.md`.

### FID-002 — Repository documentation anatomy was incomplete

Finding: The previous document set did not require the full v0.3 documentation and decision-record anatomy.

Fix: Added `R-V03-DOC-001` and updated expected repository additions / Plan T01.

### FID-003 — Model schema path drift

Finding: The Plan used `schemas/model/**`, while v0.3 names the model API schema area as `schemas/model_api/**`.

Fix: Updated Plan T02 and added `R-V03-SCHEMA-001` to make `schemas/model_api/**` the v0.3 source-fidelity target.

### FID-004 — Auxiliary construction kind drift

Finding: The Base Spec used `circle_through_center_and_point` and allowed a broad `plugin_supported` proof-use kind. v0.3 uses `circle_with_center_through_point` and deliberately restricts proof-use construction kinds.

Fix: Updated `R-AUX-001` and added `R-V03-AUX-001`, which fixes the spelling and forbids unsupported construction kinds from entering proof-use path.

### FID-005 — Trust-level naming drift

Finding: The Base Spec used summarized result levels such as `raw_candidate`, `checked_claim_artifact`, and `lean_theorem`, while v0.3 defines trust classifications ending in `final_theorem`.

Fix: Updated `R-TRUST-002` and added `R-V03-TRUST-001` to require the exact v0.3 trust levels.

### FID-006 — Local execution extensions could be mistaken for v0.3 semantics

Finding: Dependency bootstrap, local resource governance, and `ModelProviderSet` were inherited from drafts/user decisions, but are not themselves v0.3 mathematical pipeline semantics.

Fix: Added `R-V03-EXT-001` and source-map labels so these are treated as local execution constraints that cannot widen, weaken, or replace v0.3 semantics.

### FID-007 — Release acceptance did not explicitly fail on missing v0.3 detail

Finding: Release blockers covered many safety items, but did not explicitly fail if a detailed `R-V03-*` requirement or v0.3 checklist item was missing.

Fix: Added release blockers for missing/waived/contradicted `R-V03-*`, missing v0.3 schema fields, missing documentation anatomy, incomplete evaluation/replay funnel, and local-extension semantic conflicts.

## Claim Limit

This audit supports only the claim that Guardian documents were corrected to better preserve the provided v0.3 source plan. It does not prove implementation correctness, pipeline behavior, Lean verification, or Level 2 evaluation results.

## Review Result

Guardian source-fidelity review passed after these fixes. See `source_fidelity_review.md`.
