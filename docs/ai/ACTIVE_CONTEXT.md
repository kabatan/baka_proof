---
title: Guardian Active Context — GeometryFull2D v0.4.3
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-008
version: v0.4.3-real-full2d-recovery
status: V04_3_AUTHORITY_INSTALLED_IMPLEMENTATION_NOT_STARTED
created: 2026-06-15
last_updated: 2026-06-15
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
Implement V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY under MARP-GEOLEAN-BASE-008 / PLAN-008 / ACCEPTANCE-008.
```

The v0.4.2 track is superseded as active release authority. It remains evidence and a regression source only; it is not valid v0.4.3 completion evidence.

## Implementation Permission

The current user request approved importing the research-agent v0.4.3 integrated Guardian bundle and preparing the workspace so implementation can begin.

Import evidence is recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_3/evidence/v0_4_3_bundle_import.md
```

Before editing implementation code, read the current Plan task, required R-IDs/source anchors, admitted ReadSet, and changed files. Keep claim scope below release completion until final acceptance passes.

## Read First

1. `docs/ai/changes/geometry-full2d-v0_4_3/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_4_3/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_4_3/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_4_3/REAL_PIPELINE_INVARIANTS.md`
5. `docs/ai/changes/geometry-full2d-v0_4_3/REFACTOR_DIRECTIVE.md`
6. `docs/ai/changes/geometry-full2d-v0_4_3/SOURCE_MAP.md`
7. `docs/ai/changes/geometry-full2d-v0_4_3/README.md`
8. `docs/ai/changes/geometry-full2d-v0_4_3/CODEX_HANDOFF.md`
9. Current Plan work package and required R-IDs.
10. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current task:

```text
WP-00 — Install authority and freeze old claims
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

Implementation work for WP-01 and later has not started under v0.4.3 in this import step.

Open ReleaseBlocker / WorkDebt items are recorded in:

```text
docs/ai/changes/geometry-full2d-v0_4_3/debt/debt_ledger.jsonl
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
MARP-GEOLEAN-BASE-008 / PLAN-008 / ACCEPTANCE-008 are installed as the active user-approved v0.4.3 Guardian authority set.
The repository is prepared to resume implementation from WP-00 under the v0.4.3 plan.
```

Not allowed yet:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
