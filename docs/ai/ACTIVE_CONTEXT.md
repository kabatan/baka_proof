---
title: Guardian Active Context — geometry x Lean v0.3 full rebase
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-004
version: v0.3-full-rebase+v0.3A-patch
status: V03A_PATCH_T43_READY
created: 2026-06-13
last_updated: 2026-06-13
base_spec: MARP-GEOLEAN-BASE-004
plan: MARP-GEOLEAN-PLAN-004
active_patches:
  - MARP-GEOLEAN-BASE-004A
  - MARP-GEOLEAN-PLAN-004A
purpose: Minimal navigation state for the full v0.3 experiment-ready rebase track.
authority: Navigation only; never overrides the Base Spec, Plan, Source Map, reviewer records, or user approval state.
---

# Guardian Active Context — geometry x Lean v0.3 full rebase

## Status

Guardian Lane is active for the geometry x Lean v0.3 full rebase track, now amended by the v0.3A patch.

The previous v0.3A limited real-integration recovery remains recorded under:

- `docs/ai/changes/geometry-lean-v0_3a/CLOSURE.md`

Current mission:

```text
Rebase kabatan/baka_proof from the fixture-level / limited-recovery implementation state to the full v0.3 experiment-ready implementation defined by MARP-GEOLEAN-BASE-004 / PLAN-004, as amended by MARP-GEOLEAN-BASE-004A / PLAN-004A.
```

## Implementation Permission

Guardian boundary admission is recorded for `BASE-004 / PLAN-004`.

Implementation permission is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md`

Codex may execute `MARP-GEOLEAN-PLAN-004` within the admitted `MARP-GEOLEAN-BASE-004` scope.

The user approved importing the v0.3A patch bundle on 2026-06-13. Patch import evidence is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md`

## Read First

1. `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md`
4. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md`
5. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md`
6. `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md`
7. `docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md`
8. Current Plan task and required R-IDs/MECHs.
9. Files in the admitted ReadSet before editing.

## Current Known Problem

The repo has a partially implemented full-rebase track, but v0.3A deviation audit shows it is not sufficient for `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`.

The next implementation pass must continue the v0.3A hardening tasks, starting with the real-task standard geometry loop in T43.

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

Completed task:

```text
T28 — AuxiliaryConstructionCandidateV1
```

Completed task:

```text
T29 — ConstructionCompiler
```

Completed checkpoint:

```text
RC-6 — compiler and construction path review
```

Completed task:

```text
T30 — GeometryBridgeGate and TrustGuard
```

Completed task:

```text
T31 — Standard geometry proof loop
```

Completed task:

```text
T32 — Run trace and contribution records
```

Completed task:

```text
T33 — Safety regression suite
```

Completed checkpoint:

```text
RC-7 — standard loop and trust/bridge safety review
```

Completed task:

```text
T34 — Level2 pilot benchmark matrix
```

Completed task:

```text
T35 — Replay and reproducibility
```

Completed task:

```text
T36 — Release acceptance script
```

Completed task:

```text
T37 — Final evidence, reviews, closure
```

Completed task:

```text
T38 — Install patch authority and record current deviation audit
```

Completed task:

```text
T39 — Dependency claim-profile schema and probe update
```

Completed task:

```text
T40 — Provider module layout refactor
```

Completed task:

```text
T41 — TongGeometry claim-profile smoke hardening
```

Completed task:

```text
T42 — Nontrivial LeanGeoSubsetV1 corpus replacement
```

Current task:

```text
T43 — Real task standard geometry loop
```

Current task files changed in T42:

```text
benchmarks/leangeo/RealSmokeCorpus.lean
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/rejected_by_extraction.jsonl
scripts/check_level2_corpus_nontrivial.py
tests/unit/test_geometry_corpus_manifests.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t42_level2_corpus_nontrivial.md
docs/ai/ACTIVE_CONTEXT.md
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
- No v0.3 full completion claim without all original and v0.3A patch release blockers passing.
- No TongGeometry model-backed claim without tokenizer/lm_s/lm_l/cls, aggregate checkpoint hash, and model_inference_status=available.

## Evidence Folder

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

## Current Claim Ceiling

Allowed:

```text
BASE-004 / PLAN-004 are admitted and user-approved for implementation. BASE-004A / PLAN-004A patch documents are installed and user-approved. T42 nontrivial corpus hardening is complete. T43 is ready to implement.
No v0.3A completion claim is admitted, and no R-ID is VERIFIED.
```

Not allowed yet:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY
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
- fabricating TongGeometry model checkpoint evidence;
- satisfying corpus nontriviality by metadata labels only;
- satisfying matrix acceptance without per-task artifacts;
- weakening any v0.3A patch blocker.
