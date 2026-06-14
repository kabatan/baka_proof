---
title: Guardian Active Context — geometry x Lean v0.3 full rebase
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-004
version: v0.3-full-rebase+v0.3A+v0.3B-patch
status: V03B_RCB4_PASS_T58_READY
created: 2026-06-13
last_updated: 2026-06-14
base_spec: MARP-GEOLEAN-BASE-004
plan: MARP-GEOLEAN-PLAN-004
active_patches:
  - MARP-GEOLEAN-BASE-004A
  - MARP-GEOLEAN-PLAN-004A
  - MARP-GEOLEAN-ACCEPTANCE-004A
  - MARP-GEOLEAN-BASE-004B
  - MARP-GEOLEAN-PLAN-004B
  - MARP-GEOLEAN-ACCEPTANCE-004B
purpose: Minimal navigation state for the full v0.3 experiment-ready rebase track.
authority: Navigation only; never overrides the Base Spec, Plan, Source Map, reviewer records, or user approval state.
---

# Guardian Active Context — geometry x Lean v0.3 full rebase

## Status

Guardian Lane is active for the geometry x Lean v0.3 full rebase track, now amended by the v0.3A and v0.3B patches.

The previous v0.3A limited real-integration recovery remains recorded under:

- `docs/ai/changes/geometry-lean-v0_3a/CLOSURE.md`

Current mission:

```text
Resume implementation from the v0.3A harness-ready state to the v0.3B solver-backed proof-repair target defined by MARP-GEOLEAN-BASE-004 / PLAN-004, as amended by MARP-GEOLEAN-BASE-004A / PLAN-004A and MARP-GEOLEAN-BASE-004B / PLAN-004B / ACCEPTANCE-004B.
```

## Implementation Permission

Guardian boundary admission is recorded for `BASE-004 / PLAN-004`.

Implementation permission is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md`

Codex may execute `MARP-GEOLEAN-PLAN-004` within the admitted `MARP-GEOLEAN-BASE-004` scope.

The user approved importing the v0.3A patch bundle on 2026-06-13. Patch import evidence is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md`

The user approved importing the v0.3B solver-backed proof-repair patch bundle on 2026-06-14. Patch import evidence is recorded in:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md`

## Read First

1. `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md`
4. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md`
5. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md`
6. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md`
7. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md`
8. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md`
9. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/SOURCE_MAP_PATCH_v0_3B.md`
10. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/REPO_AUDIT_FOCUS_v0_3B.md`
11. `docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md`
12. `docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md`
13. Current Plan task and required R-IDs/MECHs.
14. Files in the admitted ReadSet before editing.

## Current Known Problem

The repo has completed the v0.3A hardening implementation tasks through T46. Core v0.3A harness readiness is closed as passed; the separate TongGeometry model-backed heavy-search claim remains blocked by unavailable checkpoint artifacts.

The v0.3B patch identifies the remaining intended v0.3 gap: provider-backed geometry chains currently do not yet become final theorem successes through a concrete solver-backed Lean proof-repair path. v0.3B is not complete until `V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY` passes.

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

Completed task:

```text
T43 — Real task standard geometry loop
```

Completed task:

```text
T44 — Artifact-derived Level2 matrix
```

Completed task:

```text
T45 — Release acceptance hardening
```

Completed task:

```text
T46 — Replay and closure claim update
```

Completed task:

```text
T47 — Install v0.3B authority docs
```

Completed task:

```text
T48 — Audit current proof-repair gap
```

Completed task:

```text
T49 — Schema patch
```

Completed task:

```text
T50 — Problem-source format and proof-region guard
```

Completed review checkpoint:

```text
RC-B1 — Schema and problem-source/proof-region guard checkpoint
```

Completed task:

```text
T51 — TraceCompiler emits concrete LeanPatchCandidateV1
```

Completed task:

```text
T52 — ConstructionCompiler emits concrete LeanPatchCandidateV1
```

Completed task:

```text
T53 — Compiler artifact tests
```

Completed review checkpoint:

```text
RC-B2 — Compiler patch candidate checkpoint
```

Completed task:

```text
T54 — ProofWorker patch application
```

Completed task:

```text
T55 — FinalVerifyGate solver-backed provenance
```

Completed task:

```text
T56 — TrustGuard and SolverBackedProofCertificate generation
```

Completed review checkpoint:

```text
RC-B3 — FinalVerifyGate and certificate/trust checkpoint
```

Completed task:

```text
T57 — StandardGeometryProofLoop solver-backed release path
```

Completed review checkpoint:

```text
RC-B4 — Standard loop solver-backed path checkpoint
```

Current task:

```text
T58 — Solver-backed corpus
```

Current task files changed in T46:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_final_command_log.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
src/math_auto_research/workflow/release_acceptance.py
tests/unit/test_replay.py
tests/unit/test_v03a_real_vs_fixture_integration.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_smoke.json
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T50:

```text
benchmarks/leangeo/SolverBackedProblems/README.md
lean/MathAutoResearch/Geometry/Generated/.gitkeep
plugins/geometry_synthetic/patching/proof_region.py
scripts/check_lean_no_sorry.py
tests/unit/test_solver_backed_proof_region.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t50_solver_backed_proof_region.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T51-T53:

```text
plugins/geometry_synthetic/trace_compiler.py
plugins/geometry_synthetic/construction/__init__.py
src/math_auto_research/model_api/proof_worker.py
tests/unit/test_trace_compiler_solver_backed_patch.py
tests/unit/test_trace_compiler_solver_backed_mutation.py
tests/unit/test_construction_compiler_solver_backed_patch.py
tests/unit/test_construction_compiler_solver_backed_mutation.py
tests/unit/test_compiler_patch_candidate_not_final_proof.py
tests/unit/test_raw_provider_output_not_patch_material.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t51_t52_t53_compiler_patch_candidates.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T54:

```text
plugins/geometry_synthetic/patching/apply_patch.py
tests/unit/test_proof_worker_solver_patch_application.py
tests/unit/test_worker_cannot_claim_final.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t54_proof_worker_patch_application.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T55:

```text
src/math_auto_research/lean_integration/final_verify_gate.py
tests/unit/test_final_verify_solver_backed_provenance.py
tests/unit/test_final_verify_rejects_missing_solver_backed_provenance.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t55_final_verify_solver_backed_provenance.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T56:

```text
plugins/geometry_synthetic/proof/certificate_builder.py
plugins/geometry_synthetic/proof/__init__.py
plugins/geometry_synthetic/bridge/__init__.py
tests/unit/test_solver_backed_proof_certificate.py
tests/unit/test_solver_backed_laundering.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t56_solver_backed_certificate_trust.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T57:

```text
plugins/geometry_synthetic/standard_loop.py
src/math_auto_research/lean_integration/proof_region_guard.py
tests/unit/test_standard_geometry_loop_solver_backed.py
tests/unit/test_standard_loop_no_unconditional_provider_block.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t57_standard_loop_solver_backed_path.md
docs/ai/ACTIVE_CONTEXT.md
```

Current task files changed in T47:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/CODEX_HANDOFF_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/REPO_AUDIT_FOCUS_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/SOURCE_MAP_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACTIVE_CONTEXT_PATCH_seed_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/v0_3B_patch_source_sha256sums.txt
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/README.md
docs/ai/INDEX.md
docs/ai/ACTIVE_CONTEXT.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/CODEX_HANDOFF_PROMPT.md
```

Current task files changed in T49:

```text
plugins/geometry_synthetic/patching/lean_patch_candidate_v1.py
plugins/geometry_synthetic/proof/solver_backed_proof_certificate.py
schemas/geometry/lean_patch_candidate_v1.schema.json
schemas/geometry/solver_backed_proof_certificate.schema.json
plugins/geometry_synthetic/trace_compiler.py
plugins/geometry_synthetic/construction/__init__.py
plugins/geometry_synthetic/standard_loop.py
src/math_auto_research/lean_integration/final_verify_gate.py
src/math_auto_research/base/schemas.py
src/math_auto_research/model_api/proof_worker.py
schemas/geometry/trace_compilation_result.schema.json
schemas/geometry/construction_compilation_result.schema.json
schemas/geometry/v03_contract_index.schema.json
schemas/base/final_verify_report.schema.json
schemas/base/public_contracts.schema.json
schemas/model_api/public_contracts.schema.json
scripts/check_solver_backed_patch_schema.py
tests/unit/test_solver_backed_schema.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t49_solver_backed_schema.md
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
- No v0.3B solver-backed proof-repair readiness claim without release blockers 1-47 passing.
- No provider-backed final theorem claim without SolverBackedProofCertificate and FinalVerifyGate final theorem status.
- No solver-backed success from an unchanged already-proved theorem.
- No TongGeometry model-backed claim without tokenizer/lm_s/lm_l/cls, aggregate checkpoint hash, and model_inference_status=available.

## Evidence Folder

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

## Current Claim Ceiling

Allowed:

```text
BASE-004 / PLAN-004 are admitted and user-approved for implementation. BASE-004A / PLAN-004A and BASE-004B / PLAN-004B / ACCEPTANCE-004B patch documents are installed and user-approved.

T46 final replay and v0.3A closure are complete: release blockers 1-34 pass, core_experiment_ready_status=passed, and tonggeometry_model_backed_status=blocked due admitted unavailable external checkpoint artifacts.

After v0.3B patch installation, the intended complete v0.3 closure is not final until solver-backed proof repair also passes. Current allowed status is:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: v0.3A harness-ready passed, v0.3B schema/proof-region/compiler/worker/final-verify/certificate trust pieces and standard loop solver-backed path implemented; corpus/metrics/release flow pending
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: not yet claimed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked
```

No R-ID is VERIFIED.
```

Not allowed yet:

```text
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
v0_3b_solver_backed_ready_no_tong_model_backed_claim
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
- weakening any v0.3B patch blocker;
- counting raw provider output, a compiler result alone, or an unchanged original theorem as solver-backed proof repair;
- keeping provider-backed tasks diagnostic-only while adjusting metrics to claim v0.3B readiness.
