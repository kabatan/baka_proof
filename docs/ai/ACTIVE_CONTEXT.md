---
title: Guardian Active Context — GeometryFull2D v0.4.3
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-008
version: v0.4.3-real-full2d-recovery
status: V04_3_RELEASE_BLOCKED_STRICT_SPEC_VERIFICATION
created: 2026-06-15
last_updated: 2026-06-16
base_spec: MARP-GEOLEAN-BASE-008
plan: MARP-GEOLEAN-PLAN-008
acceptance: MARP-GEOLEAN-ACCEPTANCE-008
purpose: Minimal navigation state for the active GeometryFull2D v0.4.3 Guardian track.
authority: Navigation only; never overrides the Base Spec, Plan, Acceptance, invariants, evidence, or user approval state.
---

# Guardian Active Context — GeometryFull2D v0.4.3

## Status

Guardian Lane is active for the GeometryFull2D v0.4.3 real pipeline recovery track.

Current mission:

```text
Implement V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY under MARP-GEOLEAN-BASE-008 / PLAN-008 / ACCEPTANCE-008, currently blocked by strict corpus duplicate and direct-lemma success ceilings.
```

The v0.4.2 track is superseded as active release authority. It remains evidence and a regression source only; it is not valid v0.4.3 completion evidence.

## Implementation Permission

The current user request approved importing the research-agent v0.4.3 integrated Guardian bundle and preparing the workspace so implementation can begin.

Import evidence is recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_3/evidence/v0_4_3_bundle_import.md
```

Before editing implementation code, read the current Plan task, required R-IDs/source anchors, admitted ReadSet, changed files, and the current blocker report. Keep claim scope below release completion until final acceptance passes.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_4_3/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_4_3/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_4_3/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_4_3/REAL_PIPELINE_INVARIANTS.md`
5. `docs/ai/changes/geometry-full2d-v0_4_3/REFACTOR_DIRECTIVE.md`
6. `docs/ai/changes/geometry-full2d-v0_4_3/SOURCE_MAP.md`
7. `docs/ai/changes/geometry-full2d-v0_4_3/README.md`
8. `docs/ai/changes/geometry-full2d-v0_4_3/CODEX_HANDOFF.md`
9. `docs/ai/changes/geometry-full2d-v0_4_3/evidence/v0_4_3_release_blocker_report.md`
10. Current Plan work package and required R-IDs.
11. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP-11 / WP-13 / WP-14 / WP-21 — resolve strict corpus duplicate and direct-lemma release blockers
```

Completed preparation:

```text
v0.4.3 integrated research-agent bundle imported.
Bundle hashes verified.
Active context and index updated to point to v0.4.3.
v0.4.2 Guardian docs marked superseded for release claims.
v0.4.3 debt ledger initialized.
scripts/check_active_guardian_spec_v0_4_3.py added for authority checks.
```

Implementation progressed through substantial v0.4.3 hardening, Lean elaborator extraction, matrix-run infrastructure, and strict checker updates. Release closure is blocked by strict corpus and metrics evidence, not by Lean bootstrap or browser/environment state.

Open ReleaseBlocker / WorkDebt items are recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_3/debt/debt_ledger.jsonl
```

Current blocker report:

```text
docs/ai/changes/geometry-full2d-v0_4_3/evidence/v0_4_3_release_blocker_report.md
```

## Non-Negotiables

- Do not mark v0.4.2 passed status as v0.4.3 completion.
- Do not use `template_id`, `theorem_family`, or `task_id` to select proof text in the v0.4.3 release path.
- Do not fabricate solver refs.
- Do not count proof artifacts unless they belong to a valid `ActualTaskPipelineRunV1`.
- Do not count Codex-generated tasks as human curated without an explicit user/reviewer manifest.
- Do not let release-critical engines output Lean proof snippets, tactic scripts, proof-region replacements, or benchmark dispatch fields.
- Do not let compilers read benchmark labels to choose proof text.
- Do not weaken baselines to create artificial advantage.
- Do not omit causal-chain hash or anti-v0.4.2 regression evidence.
- Do not close release while debt ledger entries remain open.
- Stop only for HardBlockers HB-01 through HB-09 in the active Base Spec.

## Evidence Folder

```text
docs/ai/changes/geometry-full2d-v0_4_3/evidence/
```

## Current Claim Ceiling

Allowed:

```text
The v0.4.3 implementation contains substantial real-pipeline hardening, Lean elaborator extraction, matrix-run infrastructure, and strict blocker checkers, but release closure is blocked by corpus duplicate and direct-lemma success ceilings.
```

Not allowed yet:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
