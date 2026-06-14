---
title: Guardian Active Context — GeometryFull2D v0.4.2
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-007
version: v0.4.2-governed-full2d
status: V04_2_AUTHORITY_IMPORTED_WP00_READY
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
WP-00 — Install v0.4.2 authority and audit repo
```

Completed preparation:

```text
v0.4.2 research-agent bundle imported.
Bundle hashes verified.
Active context and index updated to point to v0.4.2.
Debt ledger initialized.
```

Remaining WP-00 implementation work:

```text
implement/run active Guardian spec checker;
archive older geometry authority only together with stale reference repair;
produce real status evidence files from checks rather than placeholders.
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
Implementation can begin at WP-00.
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
