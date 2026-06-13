---
title: Guardian Active Context — geometry x Lean v0.3 full rebase
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-004
version: v0.3-full-rebase
status: V03_FULL_REBASE_T28_IN_PROGRESS
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

Implementation permission is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md`

Codex may execute `MARP-GEOLEAN-PLAN-004` within the admitted `MARP-GEOLEAN-BASE-004` scope.

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

Completed task:

```text
T00 — Approval gate
```

Completed task:

```text
T01 — Current repo audit
```

Completed task:

```text
T02 — Cleanup superseded specs and ambiguous root guidance
```

Completed review checkpoint:

```text
RC-0 — repo rebase and old-spec deletion
```

Completed task:

```text
T03 — Canonical package and repo skeleton
```

Completed task:

```text
T04 — Stable schema framework
```

Completed task:

```text
T05 — SelectedImplementations and configs
```

Completed task:

```text
T06 — ArtifactStore, RunLogger, DiagnosticBundle
```

Completed task:

```text
T07 — ProofStateDAG core
```

Completed review checkpoint:

```text
RC-1 — Base schemas, package layout, and Base/plugin boundary
```

Completed task:

```text
T08 — Plugin registry and manifest loader
```

Completed task:

```text
T09 — ResourceGovernor and ProcessRunner
```

Completed task:

```text
T10 — Dependency bootstrap
```

Completed task:

```text
T11 — LeanGeo dependency and TargetLibraryManifest
```

Completed task:

```text
T12 — Resource/dependency smoke evidence
```

Completed review checkpoint:

```text
RC-2 — resource governance and dependency bootstrap
```

Completed task:

```text
T13 — ModelProviderSet
```

Completed task:

```text
T14 — ResearchControllerPlugin and ProofWorkerPlugin contracts
```

Completed task:

```text
T15 — LeanPort, ProofRegionGuard, FinalVerifyGate
```

Current gate:

```text
RC-3 — model provider and Lean verification boundary
```

Completed review checkpoint:

```text
RC-3 — model provider and Lean verification boundary
```

Completed task:

```text
T16 — geometry_synthetic plugin scaffold
```

Completed task:

```text
T17 — LeanGeoSubsetV1 theorem grammar and mappings
```

Completed task:

```text
T18 — real corpus manifests
```

Completed task:

```text
T19 — GeometryExtractionContract
```

Completed task:

```text
T20 — extraction mutation tests
```

Current gate:

```text
RC-4 — target subset and extraction
```

Completed review checkpoint:

```text
RC-4 — target subset and extraction
```

Completed task:

```text
T21 — GeometrySolverPolicy and GeometryExecutionPlan
```

Completed task:

```text
T22 — CompositeSyntheticGeometryProvider shell
```

Completed task:

```text
T23 — Newclid-compatible real adapter
```

Completed task:

```text
T24 — GenesisGeo-compatible real adapter
```

Completed task:

```text
T25 — TongGeometry-compatible real adapter
```

Completed checkpoint:

```text
RC-5 — real provider integration review
```

Completed task:

```text
T26 — GeoTraceV1 and RuleRegistryV1
```

Completed task:

```text
T27 — TraceCompiler
```

Current task:

```text
T28 — AuxiliaryConstructionCandidateV1
```

Current task files changed:

```text
plugins/geometry_synthetic/providers/
plugins/geometry_synthetic/trace/
tests/unit/
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
BASE-004 / PLAN-004 are admitted and user-approved for implementation. T00, T01, T02, RC-0, T03, T04, T05, T06, T07, RC-1, T08, T09, T10, T11, T12, RC-2, T13, T14, T15, RC-3, T16, T17, T18, T19, T20, RC-4, T21, T22, T23, T24, T25, RC-5, T26, and T27 are complete. T28 is in progress.
No v0.3 completion claim is admitted, and no R-ID is VERIFIED.
```

Not allowed yet:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
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
