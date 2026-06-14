---
title: Guardian Active Context — GeometryFull2D v0.4.2
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-007
version: v0.4.2-governed-full2d
status: V04_2_WP13_LEAN_PROOF_SEARCH_PASSED_WP14_READY
created: 2026-06-15
last_updated: 2026-06-15
base_spec: MARP-GEOLEAN-BASE-007
plan: MARP-GEOLEAN-PLAN-007
acceptance: MARP-GEOLEAN-ACCEPTANCE-007
purpose: Minimal navigation state for the active GeometryFull2D v0.4.2 Guardian track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, contracts, evidence, or user approval state.
---

# Guardian Active Context — GeometryFull2D v0.4.2

## Status

Guardian Lane is active for the GeometryFull2D v0.4.2 governed full implementation track.

Current mission:

```text
Implement V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY under MARP-GEOLEAN-BASE-007 / PLAN-007 / ACCEPTANCE-007.
```

The v0.3-family tracks are superseded as active release authority. They remain historical evidence and safety background only.

## Implementation Permission

The current user request approved importing the research-agent v0.4.2 Guardian bundle and preparing the workspace so implementation can begin.

Import evidence is recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_2/evidence/v0_4_2_bundle_import.md
```

Before editing implementation code, read the current Plan task, required requirements, admitted ReadSet, and changed files. Keep claim scope below release completion until final acceptance passes.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_4_2/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_4_2/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_4_2/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_4_2/ENGINE_CONTRACTS.md`
5. `docs/ai/changes/geometry-full2d-v0_4_2/BLOCKER_AND_DEBT_POLICY.md`
6. `docs/ai/changes/geometry-full2d-v0_4_2/REFACTOR_DIRECTIVE.md`
7. `docs/ai/changes/geometry-full2d-v0_4_2/SOURCE_MAP.md`
8. `docs/ai/changes/geometry-full2d-v0_4_2/README.md`
9. Current Plan work package and required source anchors.
10. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP-14 — PortfolioCoordinator
```

Completed preparation:

```text
v0.4.2 research-agent bundle imported.
Bundle hashes verified.
Active context and index updated to point to v0.4.2.
Debt ledger initialized.
scripts/check_active_guardian_spec.py reports exactly one active geometry spec: MARP-GEOLEAN-BASE-007.
Initial progress acceptance reports hard_blockers=[] and progress_ok_with_debt.
WP-01 plugin boundary checker passed.
WP-02 Lean facade checker, elaboration-backed facade materialization, lean-no-sorry, and lean-build passed.
WP-03 structured Lean extraction checker passed.
WP-04 ClaimSpec canonical bridge checker passed.
WP-05 engine contracts and provider skeleton checker passed.
WP-06 SyntheticClosureEngine smoke passed.
WP-07 ConstructionSearchEngine smoke passed.
WP-08 AlgebraicGeometryEngine smoke passed.
WP-09 MetricAngleEngine smoke passed.
WP-10 TransformationEngine smoke passed.
WP-11 OrderCaseEngine smoke passed.
WP-12 InequalityEngine smoke passed.
WP-13 LeanProofSearchEngine smoke passed.
WP-15 RuleRegistryFull2D floor checker passed.
```

Open ReleaseBlocker / WorkDebt items are recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_2/debt/debt_ledger.jsonl
```

## Non-Negotiables

- Do not close with experiment-ready only, proof plumbing only, or a v0.3B-style partial claim.
- Do not lower corpus floors, solve-rate floors, advantage thresholds, or engine role requirements.
- Do not use `plugins/geometry_synthetic` in the v0.4.2 release path.
- Do not use toy geometry semantics, axioms, `sorry`, `admit`, or raw solver/model output as proof evidence.
- Do not count safe-reject as success for in-target positive tasks.
- Do not stop for ReleaseBlockers or WorkDebt; record them and continue independent work.
- Stop only for HardBlockers HB-01 through HB-09 in the active Base Spec / Blocker policy.

## Evidence Folder

```text
docs/ai/changes/geometry-full2d-v0_4_2/evidence/
```

## Current Claim Ceiling

Allowed:

```text
MARP-GEOLEAN-BASE-007 / PLAN-007 / ACCEPTANCE-007 are installed as the active user-approved v0.4.2 Guardian authority set.
WP-00 through WP-13 and WP-15 have passed progress checks.
```

Not allowed yet:

```text
V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```

TongGeometry trained checkpoints are not release-critical for v0.4.2 and must not block the v0.4.2 release path.
