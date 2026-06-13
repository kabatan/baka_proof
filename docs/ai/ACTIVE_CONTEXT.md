---
title: Guardian Active Context — geometry x Lean v0.3 full rebase
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-004
version: v0.3-full-rebase
status: BASE004_PLAN004_ADMITTED_PENDING_IMPLEMENTATION_APPROVAL
created: 2026-06-13
last_updated: 2026-06-13
base_spec: MARP-GEOLEAN-BASE-004
plan: MARP-GEOLEAN-PLAN-004
purpose: Minimal navigation state for the full v0.3 experiment-ready rebase track.
authority: Navigation only; never overrides the Base Spec, Plan, Source Map, reviewer records, or user approval state.
---

# Guardian Active Context — geometry x Lean v0.3 full rebase

## Status

Guardian Lane is active for the geometry x Lean v0.3 full rebase preparation track.

The previous v0.3A limited real-integration recovery remains recorded under:

- `docs/ai/changes/geometry-lean-v0_3a/CLOSURE.md`

Current mission:

```text
Rebase kabatan/baka_proof from the fixture-level / limited-recovery implementation state to the full v0.3 experiment-ready implementation defined by MARP-GEOLEAN-BASE-004 and MARP-GEOLEAN-PLAN-004.
```

## Implementation Permission

Guardian boundary admission is recorded for `BASE-004 / PLAN-004`.

Implementation permission is not yet recorded.

Codex may review and prepare Guardian documents. Codex must not modify implementation code for PLAN-004 tasks until all of the following exist:

- Guardian boundary admission for `BASE_SPEC.md` and `PLAN.md`;
- explicit user approval for implementing `MARP-GEOLEAN-BASE-004` and `MARP-GEOLEAN-PLAN-004`;
- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md`.

## Read First

1. `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md`
4. `docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md`
5. Current Plan task and required R-IDs/MECHs.
6. Files in the admitted ReadSet before editing.

## Current Known Problem

The repo currently contains historical root-level Guardian drafts and a fixture/limited-recovery implementation state. That state is not sufficient for `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`.

The next implementation pass must delete or retire drifted guidance and implement the real v0.3 contracts under `BASE-004`.

## Current Task Pointer

Completed preparation gate:

```text
BASE-004 / PLAN-004 Guardian boundary review passed.
```

Current preparation task:

```text
Record explicit user implementation approval for BASE-004 / PLAN-004 and prepare T00 approval gate.
```

After Guardian admission and explicit user implementation approval, proceed to:

```text
T00 — Approval gate
T01 — Current repo audit
T02 — Cleanup superseded specs and ambiguous root guidance
```

## Non-Negotiables

- No active old root-level Guardian draft specs after T02.
- No AgentC/D core modes.
- No multiple target libraries.
- No Base branching on Newclid, GenesisGeo, TongGeometry, LeanGeo, or geometry-specific predicates.
- No fixture provider selected in release configs.
- No raw provider, model, or DSL output as proof.
- No raw DSL proof-use path.
- No external provider execution outside `ResourceGovernor`.
- No theorem statement mutation.
- No final theorem claim without `FinalVerifyGate`.
- No v0.3 full completion claim without real Newclid, GenesisGeo, TongGeometry, LeanGeo corpus, and release acceptance evidence.

## Evidence Folder

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

## Current Claim Ceiling

Allowed:

```text
BASE-004 / PLAN-004 are admitted as the next Guardian Base Spec / Plan candidate for full v0.3 implementation preparation.
Implementation is not approved, no code changes are authorized, and no R-ID is VERIFIED.
```

Not allowed yet:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
real Newclid integration under BASE-004
real GenesisGeo integration under BASE-004
real TongGeometry integration under BASE-004
real Level 2 advantage
arbitrary LeanGeo support
open-problem solving
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```

## Stop Conditions

Stop and request decision if any work requires:

- weakening or reinterpreting a Base Spec R-ID;
- keeping old root-level specs as active guidance after T02;
- using a second target library;
- adding AgentC/AgentD core modes;
- hard-coding a model endpoint into controller/worker code;
- putting Newclid, GenesisGeo, TongGeometry, or LeanGeo logic in Base;
- selecting fixture providers in release configs;
- trusting raw provider/model output as proof evidence;
- bypassing `ResourceGovernor`;
- mutating a protected theorem statement;
- claiming completion without fresh evidence.
