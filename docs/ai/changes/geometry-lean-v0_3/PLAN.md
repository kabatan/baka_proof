---
title: Guardian Plan — geometry × Lean 自動研究 pipeline v0.3
plan_id: MARP-GEOLEAN-PLAN-003
version: v0.3-admission-candidate
status: SOURCE_FIDELITY_REVIEW_PASSED_PENDING_USER_IMPLEMENTATION_APPROVAL
created: 2026-06-10
last_updated: 2026-06-11
base_spec: MARP-GEOLEAN-BASE-003
purpose: Define implementation order, ReadSets, evidence gates, and verification commands for the approved Base Spec.
authority: Execution contract after guardian admission and explicit user implementation approval; cannot add or weaken Base Spec requirements.
---

# Guardian Plan — geometry × Lean 自動研究 pipeline v0.3

## Context Packet

Plan ID: `MARP-GEOLEAN-PLAN-003`  
Type: Guardian Plan Contract candidate  
Status: Source-fidelity review passed. Implementation still requires explicit user approval of both Base Spec and Plan.  
Parent: `MARP-GEOLEAN-BASE-003`  
Scope: Implement the geometry × Lean v0.3 pipeline under Guardian Lane, including dependency bootstrap, Base-level model provider injection, composite synthetic geometry provider, and local PC resource governance.  
Blocking Questions: none. Previous `QD-001` is retired. Dependency failures are handled by `DependencyResolutionReport`, not by silent substitution.  
Read-First R-IDs: `R-GUARD-001`, `R-NOOPT-001`, `R-ENV-001`, `R-MODEL-001`, `R-RSRC-001`, `R-GEO-001`, `R-EXTRACT-001`, `R-SOLVER-001`, `R-RULE-001`, `R-VERIFY-001`, `R-V03-SCHEMA-001`, `R-V03-EXT-001`.  
Context Packet Authority: non-authoritative digest. The task table and acceptance mappings below are authoritative for implementation order.

---

## 0. Plan boundary

This Plan defines how Codex agents should implement the approved Base Spec. It does not add requirements. If this Plan conflicts with `MARP-GEOLEAN-BASE-003`, the Base Spec wins.

Implementation must not start until the user explicitly approves this Base Spec and Plan.

The implementation is expected to be done by Codex agents. The plan therefore emphasizes exact contracts, file paths, verification commands, stop conditions, and evidence artifacts over human effort estimates.

---

## 1. Execution model for Codex agents

### 1.1 Standard task loop

For each task, Codex must:

1. Read `docs/ai/ACTIVE_CONTEXT.md`.
2. Read the current Plan task.
3. Read the relevant Base Spec R-IDs and MECH entries.
4. Read files being changed.
5. Implement only admitted task scope.
6. Run the task’s verification commands.
7. Store long logs under `docs/ai/changes/geometry-lean-v0_3/evidence/` or a configured evidence path.
8. Update `ACTIVE_CONTEXT.md` and task evidence pointers.
9. Stop if the task’s stop condition is met.

### 1.2 Global stop conditions

Codex must stop and request user/reviewer decision if:

- It needs to weaken or reinterpret a Base Spec R-ID.
- It needs to use a second target library to make tests pass.
- It needs to add AgentC/AgentD core modes.
- It needs to hard-code GPT-Pro, Codex, DeepResearch, or any model into controller/worker code instead of using `ModelProviderSet`.
- It needs provider-specific proof semantics in Base.
- It needs to trust provider/model output without FinalVerifyGate.
- It cannot route provider execution through `ResourceGovernor`.
- It cannot produce evidence for a claimed task closure.
- It detects Base/Plan conflict.

### 1.3 Dependency failure policy

Dependency failure is not a blocking question by itself.

If LeanGeo / Newclid / GenesisGeo / TongGeometry dependency setup fails, Codex must:

1. Continue implementing schema, scaffolding, fixtures, resource governance, and tests that do not require the missing component.
2. Emit `DependencyResolutionReport` with exact failure evidence.
3. Mark any real integration claim depending on the missing component as blocked.
4. Not substitute another target library or a toy proof target.

### 1.4 Global verification commands

The repository must eventually support:

```bash
make fmt
make lint
make typecheck
make test
make test-unit
make test-integration
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
make smoke-env-bootstrap
make smoke-resource-governor
make smoke-model-provider-set
make smoke-geometry-extraction
make smoke-geometry-provider
make smoke-geometry-trace
make smoke-geometry-construction
make smoke-geometry-final-verify
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
```

Early tasks may implement commands incrementally, but final release acceptance requires the full command set.

### 1.5 v0.3 source-fidelity overlay

Every implementation task must treat `R-V03-*` requirements as cross-cutting source-fidelity overlays. A task is not complete if it implements only the summarized Base R-ID while omitting the detailed v0.3 fields, enum values, workflows, mutation tests, release blockers, or checklist items assigned to that area.

Local execution extensions such as dependency bootstrap, `ResourceGovernor`, and `ModelProviderSet` constrain implementation and reproducibility. They must not change the v0.3 target semantics, proof-use path, trust model, selected target library, or release claims.

---

## 2. Task dependency graph

```text
T00 Guardian setup and approval gate
  -> T01 Repository AI docs and scaffolding
  -> T02 Stable schemas and SelectedImplementations
  -> T03 Dependency bootstrap and DependencyResolutionReport
  -> T04 LocalResourceProfile and ResourceGovernor
  -> T05 ArtifactStore, RunLogger, diagnostics
  -> T06 ProofStateDAG core
  -> T07 Plugin registry and manifest loading
  -> T08 ModelProviderSet and model-consuming plugin contracts
  -> T09 Lean integration and FinalVerifyGate skeleton
  -> T10 geometry_synthetic plugin scaffold
  -> T11 LeanGeo dependency discovery and TargetLibraryManifest
  -> T12 LeanGeoSubsetV1 theorem grammar
  -> T13 GeometryExtractionContract
  -> T14 GeometrySolverPolicy and resource-aware ExecutionPlan
  -> T15 Composite GeometrySolverProvider shell
  -> T16 Newclid-compatible symbolic closure adapter
  -> T17 GenesisGeo-compatible construction proposer adapter
  -> T18 TongGeometry-compatible heavy-search adapter
  -> T19 GeoTraceV1 and RuleRegistryV1
  -> T20 TraceCompiler
  -> T21 AuxiliaryConstructionCandidateV1 and ConstructionCompiler
  -> T22 BridgeGate, TrustGuard, and proof-use classification
  -> T23 Standard geometry proof loop
  -> T24 RunTrace, ProviderRunManifest, ResourceUsageReport, contribution tracking
  -> T25 Regression and mutation suite
  -> T26 EvaluationFunnel and Level 2 matrix
  -> T27 Release acceptance and closure
```

Review checkpoints:

```text
RC-1 after T07: Base/plugin boundary and schemas.
RC-2 after T13: target subset and extraction.
RC-3 after T18: provider/resource integration.
RC-4 after T21: compiler and construction path.
RC-5 after T23/T25: proof loop and safety tests.
RC-6 after T27: release acceptance and closure.
```

---

## 3. Tasks

### T00 — Guardian setup and implementation approval gate

Supports R-IDs: `R-GUARD-001`, `R-GUARD-003`.  
MECHs: none.

Purpose: Ensure Guardian artifacts exist and implementation is explicitly approved before code work.

Deliverables:

- `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md` admitted as the candidate Base Spec.
- `docs/ai/changes/geometry-lean-v0_3/PLAN.md` admitted as the candidate Plan.
- `docs/ai/changes/geometry-lean-v0_3/source_map.md`.
- `docs/ai/ACTIVE_CONTEXT.md`.
- User implementation approval record in `docs/ai/changes/geometry-lean-v0_3/evidence/user_implementation_approval.md` or equivalent, after the user explicitly approves implementation.

Implementation notes:

- Do not modify implementation code in this task.
- If user implementation approval is absent, stop after creating/reviewing candidate Guardian docs.

Verification:

```bash
test -f docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md
test -f docs/ai/changes/geometry-lean-v0_3/PLAN.md
test -f docs/ai/ACTIVE_CONTEXT.md
```

Stop condition:

- Stop if implementation approval is missing.

---

### T01 — Repository AI docs and scaffolding

Supports R-IDs: `R-GUARD-001`, `R-GUARD-002`, `R-V03-DOC-001`.  
MECHs: none.

Deliverables:

- `docs/ai/changes/geometry-lean-v0_3/` directory.
- `docs/ai/changes/geometry-lean-v0_3/evidence/` directory.
- `docs/architecture/geometry_lean_pipeline.md` copied or summarized from approved plan.
- `docs/ai/changes/geometry-lean-v0_3/CLOSURE_TEMPLATE.md`.
- v0.3 architecture documents and decision record placeholders required by `R-V03-DOC-001`.

Verification:

```bash
find docs/ai/changes/geometry-lean-v0_3 -maxdepth 2 -type d | sort
```

---

### T02 — Stable schemas and SelectedImplementations

Supports R-IDs: `R-ARCH-003`, `R-NOOPT-001`, `R-NOOPT-003`, `R-V03-SCHEMA-001`.  
MECHs: `MECH-MODEL-001`, `MECH-RSRC-001`.

Deliverables:

- Base schemas under `schemas/base/**`.
- Model API schemas under `schemas/model_api/**`.
- Resource schemas under `schemas/resources/**`.
- Geometry schemas placeholders under `schemas/geometry/**`.
- `SelectedImplementations` schema.
- `configs/selected_implementations/geometry_default.yaml`.
- Schema validation CLI or test helper.

Implementation notes:

- Implement scalar selected implementation fields only.
- Do not add arrays for target libraries or provider backends.

Verification:

```bash
make test-unit TEST_FILTER=schema
python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml
```

Review checkpoint: none.

---

### T03 — Dependency bootstrap and DependencyResolutionReport

Supports R-IDs: `R-ENV-001`, `R-ENV-002`, `R-ENV-003`, `R-V03-EXT-001`.  
MECHs: `MECH-BOOT-001`.

Deliverables:

- `scripts/bootstrap_env.sh` or equivalent Python bootstrap entrypoint.
- `scripts/probe_dependencies.py`.
- `DependencyResolutionReport` schema and serializer.
- Repo-managed dependency files: `lakefile.lean`, `pyproject.toml`, lockfiles where applicable.
- Evidence file for bootstrap attempt.

Implementation notes:

- Codex may install/pin LeanGeo-compatible dependency and provider dependencies.
- Codex must not silently switch to Mathlib-only or local toy target.
- If a dependency cannot be resolved, emit report and mark dependent real-integration tasks blocked, not completed.

Verification:

```bash
make smoke-env-bootstrap
python scripts/probe_dependencies.py --json > docs/ai/changes/geometry-lean-v0_3/evidence/dependency_probe.json
python -m math_auto_research.cli.validate_artifact docs/ai/changes/geometry-lean-v0_3/evidence/dependency_probe.json
```

Stop condition:

- Stop only if Codex needs to weaken target library or bypass dependency reporting.

---

### T04 — LocalResourceProfile and ResourceGovernor

Supports R-IDs: `R-RSRC-001`, `R-RSRC-002`, `R-RSRC-003`, `R-RSRC-004`, `R-RSRC-005`, `R-RSRC-006`, `R-V03-EXT-001`.  
MECHs: `MECH-RSRC-001`.

Deliverables:

- `src/math_auto_research/base/resources/local_resource_profile.py`.
- `src/math_auto_research/base/resources/resource_budget.py`.
- `src/math_auto_research/base/resources/resource_governor.py`.
- `src/math_auto_research/base/resources/process_runner.py`.
- `scripts/probe_local_resources.py`.
- `configs/resource/default_local.yaml`.
- `configs/resource/local.example.yaml`.
- `ResourceUsageReport` schema.
- Tests for admission, semaphores, timeout, orphan cleanup, and priority.

Implementation notes:

- Implement named semaphores for `lean`, `proof_worker`, `symbolic_closure`, `construction_proposer`, `heavy_search`.
- `heavy_search` must be exclusive by default.
- Use process groups where supported; fall back to documented platform-specific cleanup where not.
- Store resource reports for dummy runs even before real engines are integrated.

Verification:

```bash
make smoke-resource-governor
python scripts/probe_local_resources.py --json > docs/ai/changes/geometry-lean-v0_3/evidence/local_resource_profile.json
make test-unit TEST_FILTER=resource
make test-regression TEST_FILTER=resource_bypass
```

Review checkpoint: RC-1 may inspect this with Base boundary.

---

### T05 — ArtifactStore, RunLogger, diagnostics

Supports R-IDs: `R-ARCH-003`, `R-RUN-003`, `R-GUARD-002`.  
MECHs: `MECH-RSRC-001`.

Deliverables:

- Artifact hashing and immutable artifact store.
- `RunRecord`, `DiagnosticBundle`, `TrustReport` base records.
- Run logger linking selected implementations, dependency profile, resource profile, and artifacts.

Verification:

```bash
make test-unit TEST_FILTER=artifact
make test-unit TEST_FILTER=run_logger
```

---

### T06 — ProofStateDAG core

Supports R-IDs: `R-DAG-001`, `R-DAG-002`, `R-DAG-003`, `R-V03-DAG-001`, `R-V03-RUN-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- `Obligation`, `Derivation`, `EvidenceRef`.
- `GraphPatch`, `DAGWriter`, closure engine, acyclicity, invalidation.
- StateReader summaries.
- Domain contamination tests.

Verification:

```bash
make test-unit TEST_FILTER=proof_state
make test-regression TEST_FILTER=domain_contamination
```

---

### T07 — Plugin registry and manifest loading

Supports R-IDs: `R-ARCH-001`, `R-ARCH-002`, `R-NOOPT-001`, `R-NOOPT-002`, `R-SOLVER-001`.  
MECHs: `MECH-SOLVER-001`.

Deliverables:

- Plugin manifest schema.
- Capability registry.
- Schema registry.
- Plugin loader that loads geometry plugin without importing domain concepts into Base.
- `scripts/check_domain_contamination.py`.
- `scripts/check_no_loose_options.py`.

Verification:

```bash
make test-unit TEST_FILTER=plugin_registry
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
```

Review checkpoint RC-1:

- Verify Base/plugin separation.
- Verify no loose options.
- Verify schemas are stable.

---

### T08 — ModelProviderSet and model-consuming plugin contracts

Supports R-IDs: `R-MODEL-001`, `R-MODEL-002`, `R-MODEL-003`, `R-NOOPT-003`, `R-V03-MODEL-001`, `R-V03-EXT-001`.  
MECHs: `MECH-MODEL-001`.

Deliverables:

- `ModelProviderSetManifest` loader.
- Slot invocation interface.
- `ModelInvocationRecord` artifact.
- `ResearchControllerPluginManifest` and `ProofWorkerPluginManifest`.
- Minimal dummy controller/worker using declared model slots or deterministic fixture model.
- `configs/model_provider_sets/default.example.yaml`.

Implementation notes:

- Do not hard-code GPT-Pro/Codex/DeepResearch in controller/worker code.
- Provide example slots named `strategist`, `proof_worker`, and `critic`, but allow model replacement through manifest.

Verification:

```bash
make smoke-model-provider-set
make test-unit TEST_FILTER=model_provider
make test-regression TEST_FILTER=model_output_not_proof
```

---

### T09 — Lean integration and FinalVerifyGate skeleton

Supports R-IDs: `R-LEAN-001`, `R-VERIFY-001`, `R-TRUST-002`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- LeanPort wrapper.
- GoalAnchor extraction where possible.
- Protected theorem statement hashing.
- ProofRegionGuard.
- FinalVerifyGate skeleton.
- no-sorry / forbidden-axiom checks.

Verification:

```bash
make lean-build
make lean-no-sorry
make test-unit TEST_FILTER=final_verify
make test-regression TEST_FILTER=theorem_statement_hash
```

---

### T10 — geometry_synthetic plugin scaffold

Supports R-IDs: `R-ARCH-002`, `R-GEO-001`, `R-SOLVER-001`.  
MECHs: `MECH-SOLVER-001`.

Deliverables:

- `plugins/geometry_synthetic/plugin.yaml`.
- `geometry.solve` facade.
- Geometry capability card.
- Empty but schema-valid plugin components.

Verification:

```bash
make test-unit TEST_FILTER=geometry_plugin_scaffold
python scripts/check_domain_contamination.py
```

---

### T11 — LeanGeo dependency discovery and TargetLibraryManifest

Supports R-IDs: `R-ENV-001`, `R-ENV-003`, `R-GEO-001`.  
MECHs: `MECH-BOOT-001`.

Deliverables:

- LeanGeo-compatible dependency added/pinned if available.
- `TargetLibraryManifest` for exactly `LeanGeoSubsetV1`.
- Namespace/theorem discovery report.
- If unavailable: blocker report, not target substitution.

Verification:

```bash
make smoke-env-bootstrap
make lean-build || true
python -m math_auto_research.cli.report_target_library_status
```

Stop condition:

- Stop if implementation attempts to replace LeanGeoSubsetV1 with another target.

---

### T12 — LeanGeoSubsetV1 theorem grammar

Supports R-IDs: `R-GEO-002`, `R-EXTRACT-002`, `R-V03-TARGET-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- Grammar schema and manifest.
- Predicate / construction / relation mapping for supported subset.
- Positive, negative, ambiguous, and safe-reject fixtures.
- Lean shim file only if it wraps LeanGeo concepts; not a separate target.

Verification:

```bash
make test-unit TEST_FILTER=target_subset
make lean-build
```

---

### T13 — GeometryExtractionContract

Supports R-IDs: `R-EXTRACT-001`, `R-EXTRACT-002`, `R-BRIDGE-001`, `R-V03-TARGET-001`, `R-V03-TRUST-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- Extractor from Lean goal/context to `GeometryClaimSpec` for supported grammar.
- `GeometryExtractionReport`.
- Relation classifier: `exact | sufficient | related | none`.
- Safe-reject diagnostics.
- Nondegeneracy/orientation/diagram assumption extraction where supported.

Verification:

```bash
make smoke-geometry-extraction
make test-unit TEST_FILTER=geometry_extraction
make test-mutation TEST_FILTER=extraction
```

Review checkpoint RC-2:

- Verify extraction is semantic and safe-rejecting.
- Verify raw DSL path cannot be proof-use.

---

### T14 — GeometrySolverPolicy and resource-aware ExecutionPlan

Supports R-IDs: `R-SOLVER-003`, `R-RSRC-003`, `R-RSRC-004`, `R-RSRC-006`, `R-V03-SOLVER-001`, `R-V03-EXT-001`.  
MECHs: `MECH-RSRC-001`, `MECH-SOLVER-001`.

Deliverables:

- `GeometrySolverPolicy` implementation.
- `GeometryExecutionPlan` schema.
- Budget routing table.
- Reason codes.
- Resource semaphore requests per engine role.
- Fallback/escalation logic.

Default routing must implement:

```text
Newclid-compatible symbolic closure
  -> GenesisGeo-compatible construction proposer if needed and budget permits
  -> Newclid retry with admitted construction candidates if policy permits
  -> TongGeometry-compatible heavy search only for heavy/extreme or explicit escalation
```

Verification:

```bash
make test-unit TEST_FILTER=geometry_solver_policy
make test-unit TEST_FILTER=resource_budget
```

---

### T15 — Composite GeometrySolverProvider shell

Supports R-IDs: `R-SOLVER-001`, `R-SOLVER-002`, `R-RUN-001`, `R-RUN-003`, `R-V03-SOLVER-001`.  
MECHs: `MECH-SOLVER-001`, `MECH-RSRC-001`.

Deliverables:

- `CompositeSyntheticGeometryProvider`.
- Provider-normalized `ProviderResult`.
- `ProviderRunManifest`.
- Engine role adapters with dummy implementations.
- ResourceGovernor integration.

Verification:

```bash
make smoke-geometry-provider
make test-unit TEST_FILTER=composite_provider
make test-regression TEST_FILTER=provider_not_base_branching
```

---

### T16 — Newclid-compatible symbolic closure adapter

Supports R-IDs: `R-ENGINE-001`, `R-RSRC-004`, `R-RUN-001`, `R-V03-SOLVER-001`, `R-V03-COMPILER-001`.  
MECHs: `MECH-SOLVER-001`, `MECH-RSRC-001`.

Deliverables:

- Newclid-compatible adapter.
- Input conversion from `GeometryClaimSpec` to engine format.
- Output normalization to `GeoTraceV1` or diagnostic.
- Raw log capture.
- Resource admission for `symbolic_closure`.

Verification:

```bash
make smoke-geometry-provider ENGINE_ROLE=symbolic_closure
make test-integration TEST_FILTER=newclid_adapter || true
```

Notes:

- If real Newclid cannot be installed, fixture adapter may remain for scaffold tests, but real integration claim is blocked by DependencyResolutionReport.

---

### T17 — GenesisGeo-compatible construction proposer adapter

Supports R-IDs: `R-ENGINE-002`, `R-AUX-001`, `R-RSRC-004`, `R-RUN-001`, `R-V03-SOLVER-001`, `R-V03-AUX-001`.  
MECHs: `MECH-SOLVER-001`, `MECH-RSRC-001`.

Deliverables:

- GenesisGeo-compatible adapter.
- Output normalization to `AuxiliaryConstructionCandidateV1`.
- GPU/CPU resource guard if applicable.
- Raw rationale remains non-proof artifact.

Verification:

```bash
make smoke-geometry-provider ENGINE_ROLE=construction_proposer
make test-regression TEST_FILTER=genesis_output_not_proof
```

---

### T18 — TongGeometry-compatible heavy-search adapter

Supports R-IDs: `R-ENGINE-003`, `R-RSRC-004`, `R-RSRC-005`, `R-RSRC-006`, `R-RUN-001`, `R-V03-SOLVER-001`, `R-V03-EXT-001`.  
MECHs: `MECH-SOLVER-001`, `MECH-RSRC-001`.

Deliverables:

- TongGeometry-compatible adapter.
- Heavy/extreme budget gate.
- Exclusive semaphore.
- Timeout/heartbeat/kill integration.
- Output normalization to construction candidates, proof-plan diagnostics, or supported `GeoTraceV1` only.

Verification:

```bash
make smoke-geometry-provider ENGINE_ROLE=heavy_search BUDGET=heavy
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
```

Review checkpoint RC-3:

- Verify resource policy and provider integration.
- Verify Base does not branch on engine family names.

---

### T19 — GeoTraceV1 and RuleRegistryV1

Supports R-IDs: `R-RULE-001`, `R-TRACE-001`, `R-V03-COMPILER-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- `GeoTraceV1` schema.
- `RuleRegistryV1` schema and validator.
- Initial supported rule subset for LeanGeoSubsetV1.
- Side-condition calculus.
- Fixtures per rule.

Verification:

```bash
make test-unit TEST_FILTER=geotrace
make test-unit TEST_FILTER=rule_registry
make test-mutation TEST_FILTER=rule_registry
```

---

### T20 — TraceCompiler

Supports R-IDs: `R-TRACE-001`, `R-TRUST-001`, `R-VERIFY-001`, `R-V03-COMPILER-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- Trace compiler from supported `GeoTraceV1` to Lean patch candidate.
- Blocker diagnostics for unsupported rules and missing side conditions.
- Lean compile fixture tests.

Verification:

```bash
make smoke-geometry-trace
make test-unit TEST_FILTER=trace_compiler
make test-mutation TEST_FILTER=trace_compiler
```

---

### T21 — AuxiliaryConstructionCandidateV1 and ConstructionCompiler

Supports R-IDs: `R-AUX-001`, `R-AUX-002`, `R-VERIFY-001`, `R-V03-AUX-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- Auxiliary construction candidate schema.
- Construction compiler.
- Side-condition obligation generation.
- Lean introduction patch candidate generation.
- Tests for accepted/rejected construction kinds.

Verification:

```bash
make smoke-geometry-construction
make test-unit TEST_FILTER=construction_compiler
make test-mutation TEST_FILTER=construction_compiler
```

Review checkpoint RC-4:

- Verify compiler/construction path is narrow and deterministic.

---

### T22 — BridgeGate, TrustGuard, and proof-use classification

Supports R-IDs: `R-TRUST-001`, `R-TRUST-002`, `R-BRIDGE-001`, `R-VERIFY-001`, `R-V03-TRUST-001`.  
MECHs: `MECH-PROOF-001`.

Deliverables:

- GeometryBridgeReport.
- TrustGuard classification for geometry result levels.
- Proof-use provenance check.
- Raw-output laundering regressions.

Verification:

```bash
make test-unit TEST_FILTER=trust_guard
make test-unit TEST_FILTER=geometry_bridge
make test-regression TEST_FILTER=proof_use_laundering
```

---

### T23 — Standard geometry proof loop

Supports R-IDs: `R-EXTRACT-001`, `R-SOLVER-003`, `R-TRACE-001`, `R-AUX-002`, `R-VERIFY-001`, `R-V03-WORKFLOW-001`, `R-V03-DAG-001`.  
MECHs: `MECH-PROOF-001`, `MECH-SOLVER-001`, `MECH-MODEL-001`.

Deliverables:

- End-to-end loop:
  `Lean goal -> extraction -> provider -> compiler -> ProofWorker -> LeanPort -> FinalVerifyGate`.
- WorkOrder generation.
- WorkerResult handling.
- ProofStateDAG GraphPatch integration.
- Structured feedback to ResearchController.

Verification:

```bash
make smoke-geometry-final-verify
make test-integration TEST_FILTER=geometry_standard_loop
```

Review checkpoint RC-5 may start after T23 and T25.

---

### T24 — RunTrace, ProviderRunManifest, ResourceUsageReport, contribution tracking

Supports R-IDs: `R-RUN-001`, `R-RUN-002`, `R-RUN-003`, `R-EVAL-001`, `R-V03-RUN-001`, `R-V03-EVAL-001`.  
MECHs: `MECH-RSRC-001`, `MECH-SOLVER-001`.

Deliverables:

- ProviderRunManifest linkage.
- ControllerStrategyLog.
- ResourceUsageReport integration.
- ResearchContributionRecord.
- Reproducibility report generator skeleton.

Verification:

```bash
make test-unit TEST_FILTER=run_trace
python scripts/generate_repro_report.py --run-dir runs/fixture_run
```

---

### T25 — Regression and mutation suite

Supports R-IDs: `R-TEST-001`, `R-V03-TEST-001`, all safety R-IDs.  
MECHs: all.

Deliverables:

- Domain contamination test.
- No loose options test.
- Dependency substitution test.
- Resource bypass/timeout/orphan tests.
- Extraction mutation tests.
- RuleRegistry / TraceCompiler mutation tests.
- ConstructionCompiler mutation tests.
- Controller/model output non-proof tests.
- FinalVerifyGate misuse tests.
- Provider raw-output laundering tests.

Verification:

```bash
make test-regression
make test-mutation
```

---

### T26 — EvaluationFunnel and Level 2 matrix

Supports R-IDs: `R-EVAL-001`, `R-RUN-002`, `R-RUN-003`, `R-CLAIM-001`, `R-V03-EVAL-001`.  
MECHs: `MECH-MODEL-001`, `MECH-SOLVER-001`, `MECH-RSRC-001`.

Deliverables:

- `configs/benchmark_runs/geometry_level2_smoke.yaml`.
- `configs/benchmark_runs/geometry_level2_ablation.yaml`.
- Baselines B0–B5.
- Metrics collector.
- Resource-aware run matrix.
- Report distinguishing model-only, controller-only, geometry-enabled, and construction-disabled runs.

Verification:

```bash
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
```

---

### T27 — Release acceptance and closure

Supports R-IDs: all MUST R-IDs, all `R-V03-*` R-IDs, especially `R-GUARD-002`, `R-CLAIM-001`, `R-V03-TEST-001`, `R-V03-EXT-001`.  
MECHs: all.

Deliverables:

- `scripts/check_release_acceptance.py`.
- Final acceptance report.
- `docs/ai/changes/geometry-lean-v0_3/CLOSURE.md`.
- Evidence index.

Verification:

```bash
make fmt
make lint
make typecheck
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
```

Closure rules:

- Closure may claim only what evidence supports.
- If real LeanGeo/Newclid/GenesisGeo/TongGeometry integration is blocked, closure must explicitly say which component is blocked and what remains fixture-only.
- No open-problem or all-geometry claims.

Review checkpoint RC-6:

- Run Guardian reviewers.
- Check source fidelity, Base Spec conformance, safety regressions, and evidence-bound claims.

---

## 4. Resource execution plan detail

### 4.1 Default solver resource policy

The default local policy is conservative enough to keep Codex/Lean responsive while allowing heavy search when explicitly admitted.

```yaml
ResourcePolicy:
  policy_id: "ResourcePolicy:geometry_local_default:v1"
  global_headroom:
    reserve_logical_cores_min: 2
    reserve_cpu_fraction_min: 0.15
    reserve_ram_mb_min: 4096
    reserve_ram_fraction_min: 0.20
    reserve_disk_fraction_min: 0.10
  queues:
    final_verify:
      priority: 100
    lean_feedback:
      priority: 90
    proof_worker:
      priority: 80
    symbolic_closure:
      priority: 60
    construction_proposer:
      priority: 45
    heavy_search:
      priority: 20
  semaphores:
    lean_build:
      default_max_parallel: 1
    symbolic_closure:
      default_max_parallel_formula: "max(1, floor((logical_cores - reserved_cores) * 0.50))"
    construction_proposer:
      default_max_parallel_formula: "1 if gpu_bound else max(1, floor((logical_cores - reserved_cores) * 0.25))"
    heavy_search:
      default_max_parallel: 1
      exclusive_by_default: true
```

### 4.2 Budget profile semantics

```text
tiny:
  quick extraction, grammar, rule lookup, short Lean check, no Genesis/Tong by default.

small:
  Newclid-compatible symbolic closure, short timeout, no heavy construction search by default.

medium:
  Newclid + limited GenesisGeo construction proposals; no Tong by default.

heavy:
  Newclid + GenesisGeo + possible Tong heavy search; resource governor reserves headroom.

extreme:
  long TongGeometry-compatible search allowed, but still tracked, killable, and non-starving.
```

### 4.3 Provider engine use policy

```text
Newclid-compatible symbolic_closure:
  First-line engine. Called often. Must be cheap enough for small/medium loops.

GenesisGeo-compatible construction_proposer:
  Called when closure fails or when construction candidates are explicitly requested by policy. Output is typed construction candidates, not proof.

TongGeometry-compatible heavy_search:
  Called only under heavy/extreme. Intended for difficult auxiliary construction and proof-plan discovery. Raw trace is not proof. Must be exclusive by default.
```

### 4.4 Resource failure handling

If a task is rejected or killed by resource policy:

1. Emit `DiagnosticBundle(kind=resource_rejected | solver_timeout)`.
2. Emit `ResourceUsageReport` if process was admitted.
3. Save partial logs as artifacts.
4. Return `diagnostic_only` or `search_only` result.
5. Do not mark proof obligation closed.
6. SolverPolicy may propose smaller budget, construction-disabled path, or split/repair action.

---

## 5. Acceptance summary

The implementation is not complete unless all of the following are true:

1. Base/plugin separation passes contamination tests.
2. AgentC/D taxonomy is absent from core.
3. ModelProviderSet injection works and logs model slots.
4. Dependency bootstrap is reproducible and reported.
5. LocalResourceProfile and ResourceGovernor are enforced.
6. Composite provider runs through ResourceGovernor and logs ProviderRunManifest.
7. LeanGeoSubsetV1 is the single target library.
8. Extractor safe-rejects unsupported Lean goals.
9. Newclid/GenesisGeo/TongGeometry raw outputs cannot become proof evidence.
10. RuleRegistryV1 has side-condition calculus.
11. TraceCompiler and ConstructionCompiler produce only Lean patch candidates.
12. FinalVerifyGate is the only source of `final_theorem`.
13. Regression and mutation tests pass.
14. Level 2 evaluation harness runs and produces evidence-bound metrics.
