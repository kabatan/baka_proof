---
title: Guardian Active Context — geometry × Lean v0.3
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-003
version: v0.3-admission-candidate
status: T02_COMPLETE
created: 2026-06-11
base_spec: MARP-GEOLEAN-BASE-003
plan: MARP-GEOLEAN-PLAN-003
purpose: Minimal navigation state for the current Guardian change.
authority: Navigation only; never overrides Base Spec, Plan, source map, evidence, or user approval state.
---

# Guardian Active Context — geometry × Lean v0.3

## Status

Guardian Lane is active for the geometry × Lean v0.3 implementation track.

Implementation permission: **granted** by the 2026-06-11 user request and recorded in:

- `docs/ai/changes/geometry-lean-v0_3/evidence/user_implementation_approval.md`

Implementation remains limited to the reviewed Base Spec and Plan. Git initialization and frequent commits are authorized.

## Read First

1. `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3/source_map.md`
4. Current Plan task and required R-IDs.
5. Files in the admitted ReadSet before editing.

## Current Task Pointer

Current gate: `T02 — Stable schemas and SelectedImplementations` complete.

Next task: `T03 — Dependency bootstrap and DependencyResolutionReport`.

## Evidence Directory

Default evidence path:

```text
docs/ai/changes/geometry-lean-v0_3/evidence/
```

Use this directory for source hashes, review outputs, permission records, dependency reports, command logs, and closure evidence.

## Stop Conditions

Stop and request decision if any work requires:

- weakening or reinterpreting a Base Spec R-ID;
- using a second target library;
- adding AgentC/AgentD core modes;
- hard-coding a model into controller/worker code;
- bypassing `ResourceGovernor`;
- trusting raw provider/model output as proof evidence;
- claiming completion without fresh evidence.
