---
title: "Guardian Base Spec — geometry × Lean v0.3 full rebase implementation"
spec_id: "MARP-GEOLEAN-BASE-004"
version: "v0.3-full-rebase"
status: "USER_APPROVED_ACTIVE_WITH_V0_3A_PATCH"
created: "2026-06-12"
target_repo: "https://github.com/kabatan/baka_proof"
supersedes:
  - "MARP-GEOLEAN-BASE-002"
  - "MARP-GEOLEAN-BASE-003"
  - "all root-level geometry_lean_guardian_* draft files in kabatan/baka_proof"
  - "all fixture-level completion claims for geometry × Lean v0.3"
paired_plan: "MARP-GEOLEAN-PLAN-004"
active_patches:
  - "MARP-GEOLEAN-BASE-004A"
lane: "Guardian Lane"
---

# Guardian Base Spec — geometry × Lean v0.3 full rebase implementation

## 0. Authority and use

This Base Spec defines **what correctness means** for the next implementation pass in `kabatan/baka_proof`.

This file is the implementation authority after user approval. The Plan, Active Context, Source Map, run notes, Codex memory, previous specs, root-level draft markdown, and implementation convenience choices must not weaken, reinterpret, or extend this Base Spec.

This Base Spec is amended by `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md`. The patch does not replace this file. It supersedes only the explicitly listed patched R-IDs, release blockers, and claim profiles; all other invariants in `MARP-GEOLEAN-BASE-004` remain in force.

This Base Spec is intentionally detailed. Codex agents must implement the system by reading the R-IDs, MECHs, acceptance clauses, release blockers, and file-path requirements directly. If a Codex agent finds ambiguity, it must stop and report the ambiguity instead of inventing a simpler architecture.

### 0.1 Supersession

After approval, this Base Spec supersedes every previous geometry × Lean Guardian draft in the repo. In particular:

- `geometry_lean_guardian_BASE_SPEC_draft_v0_2.md`
- `geometry_lean_guardian_PLAN_draft_v0_2.md`
- `geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md`
- `geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md`
- `geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md`
- `geometry_lean_guardian_v0_2_sha256sums.txt`
- any previous `MARP-GEOLEAN-BASE-002`, `MARP-GEOLEAN-BASE-003`, `MARP-GEOLEAN-PLAN-002`, or `MARP-GEOLEAN-PLAN-003` implementation authority
- any fixture-level CLOSURE or release-acceptance report that claimed completion beyond its evidence ceiling

Superseded files must not remain as active or root-level guidance. They must be deleted or moved only as non-authoritative evidence indexes under the new change folder. See `R-REBASE-*`.

### 0.2 Claim target

This rebase has a strict target:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

A repo may claim this only when all required contracts, Base/plugin separation, real dependency bootstrap, real provider integration, LeanGeoSubsetV1 corpus, compiler contracts, resource governance, and release acceptance commands pass.

This target is stronger than fixture-level acceptance. It does **not** mean the pipeline solves open problems. It also does **not** mean arbitrary LeanGeo/Mathlib geometry is supported.

### 0.3 Terms

- **Base**: domain-neutral runtime under `src/math_auto_research/base`, `src/math_auto_research/proof_state`, `src/math_auto_research/plugin_api`, and generic workflow/evaluation modules.
- **Plugin**: domain-specific implementation under `plugins/geometry_synthetic/**` and `lean/MathAutoResearch/Geometry/**`.
- **Provider**: the selected `GeometrySolverProvider`. Base sees one provider. Internally the provider may use Newclid-compatible, GenesisGeo-compatible, and TongGeometry-compatible engines.
- **Proof-use**: any artifact used to close an obligation, produce `goal_level_allowed`, or produce `final_theorem`.
- **Experiment-ready**: non-fixture end-to-end runs can be launched and replayed against the approved pilot corpus. It does not require positive Level 2 advantage, only that the real Level 2 matrix can run and produce evidence.

---

## 1. Scope

### 1.1 In scope

The implementation MUST include all of the following:

1. Rebase and cleanup of current repo guidance so that only this approved spec/plan controls implementation.
2. Domain-neutral Base runtime with stable schema-backed records.
3. Domain-neutral ProofStateDAG with `Obligation`, `Derivation`, `EvidenceRef`, `GraphPatch`, `DAGWriter`, acyclicity, closure, invalidation, and StateReader.
4. ArtifactStore, RunLogger, immutable hashing, diagnostic bundles, replay metadata, and release-acceptance machinery.
5. Base-level `ModelProviderSet` with model slots injected into model-consuming plugins.
6. `ResearchControllerPlugin` and `ProofWorkerPlugin` contracts as model consumers, not model owners.
7. Local resource governance for all Lean builds, provider calls, proof worker runs, local model calls when applicable, and heavy search.
8. Reproducible dependency bootstrap for Lean/lake, LeanGeo-compatible support, Newclid-compatible engine, GenesisGeo-compatible engine/model/checkpoint where applicable, TongGeometry-compatible engine, Python dependencies, and local solver binaries.
9. Lean integration: `LeanPort`, `GoalAnchor`, protected theorem hash, `ProofRegionGuard`, `LeanErrorSummary`, and `FinalVerifyGate`.
10. `geometry_synthetic` plugin with `geometry.solve` facade.
11. `LeanGeoSubsetV1TheoremGrammar` and `TargetLibraryManifest` for exactly one target library.
12. `GeometryExtractionContract`: Lean theorem/goal/context to `GeometryClaimSpec`.
13. `GeometrySolverPolicy`, `GeometryExecutionPlan`, `CompositeSyntheticGeometryProvider`, `ProviderRunManifest`, and engine-role adapters.
14. Real integration paths for:
    - Newclid-compatible symbolic closure
    - GenesisGeo-compatible construction proposer
    - TongGeometry-compatible heavy search
15. `GeoTraceV1`, `RuleRegistryV1` with side-condition calculus, `TraceCompiler`.
16. `AuxiliaryConstructionCandidateV1`, `ConstructionCompiler`.
17. Geometry BridgeGate, TrustGuard classification, proof-use provenance checks.
18. A non-fixture `LeanGeoSubsetV1.RealSmokeCorpus` and `geometry_level2_pilot` evaluation population.
19. Regression, mutation, integration, and smoke tests that distinguish fixture behavior from real integration behavior.
20. A release acceptance script that refuses overclaims.

### 1.2 Out of scope

The implementation MUST NOT include or claim:

1. Natural-language problem to Lean theorem formalization.
2. Informal problem fidelity audit.
3. Diagram image recognition.
4. Multi-target bridge across LeanGeo, Mathlib geometry, and local micro-library.
5. AgentC/AgentD core modes or A/B/C/D runtime taxonomy.
6. Provider-specific proof semantics in Base.
7. Raw DSL problem proof-use path.
8. Arbitrary Newclid/GenesisGeo/TongGeometry trace translation.
9. Coordinate/Wu/Groebner/SOS proof path as proof-use authority.
10. Broad LeanGeo support outside the approved subset/corpus.
11. Open-problem solving claims.
12. Fixture-only completion claims.
13. Unbounded background solver execution outside `ResourceGovernor`.

### 1.3 Allowed internal oracles

Provider internals MAY use coordinate, Wu, Groebner, SOS, neural, guided-tree-search, heuristic, or analytic methods as search oracles. Their outputs remain non-proof artifacts unless converted into accepted `GeoTraceV1` or `AuxiliaryConstructionCandidateV1` and then passed through compiler, ProofWorker, LeanPort, and FinalVerifyGate.

---

## 2. Non-negotiable invariants

### INV-001 — Domain-neutral Base

Base MUST NOT import, name-match, branch on, or contain business logic for:

```text
LeanGeo
Newclid
GenesisGeo
TongGeometry
geometry_synthetic
collinear
parallel
perpendicular
concyclic
equal_angle
equal_length
midpoint
auxiliary point
```

Base may load plugin schemas and manifests by registry ID. Base may store opaque plugin payload refs and hashes.

### INV-002 — Exactly one selected implementation per boundary

Each run MUST record scalar selected implementations:

```yaml
SelectedImplementations:
  target_library: "LeanGeoSubsetV1:<version>"
  model_provider_set: "model_provider_set:<id>:<version>"
  research_controller_plugin: "research_controller:<id>:<version>"
  proof_worker_plugin: "proof_worker:<id>:<version>"
  geometry_solver_provider: "geometry_solver_provider:<id>:<version>"
  geometry_solver_policy: "geometry_solver_policy:<id>:<version>"
  rule_registry: "RuleRegistryV1:<version>"
  resource_policy: "ResourcePolicy:<id>:<version>"
  trust_boundary: "strict_lean:<version>"
```

Arrays of target libraries, arrays of provider backends, AgentC/D mode selections, and trace compiler variant selections are forbidden in core runtime configs.

### INV-003 — Plugin-only domain intelligence

All geometry-specific grammar, extraction, rendering, solver policy, provider wrappers, trace rules, side-condition calculus, construction semantics, and Lean bridge templates MUST live under:

```text
plugins/geometry_synthetic/**
lean/MathAutoResearch/Geometry/**
schemas/geometry/**
configs/solver_policies/geometry_*.yaml
benchmarks/geometry/**
```

### INV-004 — GraphPatch-only mutation

Plugins MUST NOT mutate ProofStateDAG state directly. Plugins propose `GraphPatch`. Base `DAGWriter` validates schema IDs, rule IDs, acyclicity, trust status, evidence validity, and status transitions before commit.

### INV-005 — Raw output is never proof

The following are never proof evidence by themselves:

```text
raw model output
controller rationale
worker success text
raw provider output
raw Newclid trace
raw GenesisGeo rationale
raw TongGeometry trace
raw DSL problem
raw coordinate/Wu/analytic proof
raw logs
timeout/unknown result
```

### INV-006 — Lean final verification authority

Only `FinalVerifyGate` may emit:

```text
result_level = lean_theorem
proof_use_status = final_theorem
```

Required checks:

1. Lean build succeeds for the target.
2. Protected theorem statement hash is unchanged.
3. No `sorry` in target or generated helper lemmas.
4. No forbidden axioms or unsafe declarations according to strict policy.
5. Generated proof imports are from admitted files only.
6. The proof-use path originates from approved extraction and compile steps.

### INV-007 — Extraction-first proof-use path

Allowed proof-use path:

```text
Lean theorem / goal / context
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> geometry.solve
  -> GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> TraceCompiler or ConstructionCompiler
  -> Lean patch candidate
  -> ProofWorkerPlugin
  -> LeanPort
  -> FinalVerifyGate
  -> lean_theorem
```

Forbidden proof-use path:

```text
raw DSL problem -> solver -> proof-use artifact
```

Direct DSL input is allowed only for debug/exploration artifacts with `proof_use_status = not_allowed | search_only`.

### INV-008 — Target library is fixed

The target library is exactly:

```text
LeanGeoSubsetV1
```

Mathlib may be a dependency. Local shim lemmas may wrap LeanGeo concepts. A local toy geometry library may be used only for tests that explicitly assert it is not the target. Release acceptance fails if final theorem support is satisfied only by local toy definitions.

### INV-009 — Real integration, not fixture-only completion

Fixtures are required for tests, but fixture adapters cannot satisfy `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`.

Full experiment-ready claim requires real dependency resolution and non-fixture evidence for:

1. LeanGeo-compatible target support.
2. Newclid-compatible symbolic closure.
3. GenesisGeo-compatible construction proposer.
4. TongGeometry-compatible heavy search.
5. A non-fixture LeanGeoSubsetV1 corpus and Level 2 pilot matrix.

If one of these cannot be installed or vendored, Codex must keep the component blocked and must not claim full experiment-ready status.

### INV-010 — Resource-governed execution

All external processes and heavy operations MUST pass through `ResourceGovernor` and approved `ProcessRunner` wrappers. Direct `subprocess.Popen`, untracked multiprocessing, background daemons, or unmanaged solver CLI calls in provider code are forbidden outside allowlisted wrappers.

---

## 3. Repository rebase and cleanup requirements

### R-REBASE-001 — Approved location of Guardian authority

After approval, the authoritative files MUST be placed at:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/SOURCE_MAP.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/REFACTOR_DIRECTIVE.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/ACCEPTANCE_MATRIX.md
docs/ai/ACTIVE_CONTEXT.md
```

The root directory MUST NOT contain active Guardian draft markdown after T02 cleanup.

### R-REBASE-002 — Delete or retire superseded specs

Codex MUST remove active, root-level, or ambiguous superseded specification files. At minimum:

```text
geometry_lean_guardian_ACTIVE_CONTEXT_draft_v0_2.md
geometry_lean_guardian_BASE_SPEC_draft_v0_2.md
geometry_lean_guardian_PLAN_draft_v0_2.md
geometry_lean_guardian_RESOURCE_POLICY_TEMPLATE_draft_v0_2.md
geometry_lean_guardian_SOURCE_MAP_draft_v0_2.md
geometry_lean_guardian_v0_2_sha256sums.txt
```

If preservation is needed for evidence, Codex may store only a short hash index:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/superseded_spec_index.md
```

It must not copy old specs verbatim into an active docs path.

### R-REBASE-003 — Preserve v0.3 architecture only as source, not authority

`geometry_lean_pipeline_plan_v0_3.md` is a source document, not implementation authority. It MUST be removed from root or moved to:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/source/geometry_lean_pipeline_plan_v0_3.md
```

with a header stating:

```text
NON-AUTHORITATIVE SOURCE. Superseded by MARP-GEOLEAN-BASE-004.
```

### R-REBASE-004 — Consolidate Python package layout

The canonical Python package root is:

```text
src/math_auto_research/**
```

If a top-level `math_auto_research/**` package exists, Codex MUST audit it. If it duplicates or shadows `src/math_auto_research`, it MUST be deleted or converted into a non-package migration note. No implementation module may remain in both locations.

Acceptance:

- `python -c "import math_auto_research; print(math_auto_research.__file__)"` points under `src/` or installed editable package path.
- `scripts/check_package_layout.py` fails if duplicate package modules exist.

### R-REBASE-005 — Remove fixture-only production paths

Fixture providers, fake LeanGeo targets, local toy geometry targets, and dummy final verification artifacts may exist only under:

```text
tests/fixtures/**
plugins/geometry_synthetic/tests/fixtures/**
lean/MathAutoResearch/Geometry/Fixtures/**
```

They MUST NOT be selected by default configs, release configs, or real experiment configs.

---

## 4. Required repository anatomy

After implementation, the repo MUST converge to this structure. Existing files not fitting this layout must be moved, deleted, or justified in `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_audit.md`.

```text
baka_proof/
  README.md
  pyproject.toml
  lakefile.lean
  lake-manifest.json
  lean-toolchain
  Makefile
  .gitignore

  docs/
    ai/
      ACTIVE_CONTEXT.md
      changes/
        geometry-lean-v0_3-full-rebase/
          BASE_SPEC.md
          PLAN.md
          SOURCE_MAP.md
          REFACTOR_DIRECTIVE.md
          ACCEPTANCE_MATRIX.md
          CLOSURE_TEMPLATE.md
          evidence/
            .gitkeep
    architecture/
      geometry_lean_contract.md
      proof_state_dag.md
      trust_model_geometry.md
      resource_governance.md
      model_provider_set.md
      no_loose_options.md
    runbooks/
      local_setup.md
      running_level2_pilot.md
      adding_geometry_rule.md
      adding_provider_adapter.md

  src/math_auto_research/
    __init__.py
    base/
      artifacts/
      logging/
      diagnostics/
      registry/
      resources/
      trust/
      model_provider/
    proof_state/
      dag_core.py
      graph_patch.py
      dag_writer.py
      closure_engine.py
      invalidation.py
      state_reader.py
    plugin_api/
      manifest.py
      capability.py
      schemas.py
    model_api/
      research_controller.py
      proof_worker.py
      model_invocation.py
      action_plan.py
      work_order.py
      state_pack.py
    lean_integration/
      lean_port.py
      goal_anchor.py
      final_verify_gate.py
      proof_region_guard.py
      lean_error_summary.py
    workflow/
      standard_geometry_loop.py
      replay.py
      release_acceptance.py
    evaluation/
      evaluation_funnel.py
      benchmark_matrix.py
      metrics.py
      reproducibility_report.py
    cli/
      main.py
      validate_schema.py
      validate_artifact.py
      run_geometry_level2_matrix.py
      summarize_run.py

  plugins/
    geometry_synthetic/
      plugin.yaml
      README.md
      target_subset/
        leangeo_subset_v1.yaml
        theorem_grammar.py
        predicate_mapping.yaml
        construction_mapping.yaml
        relation_mapping.yaml
        fixtures/
      extraction/
        extraction_contract.py
        extraction_report.py
        claim_spec.py
      solver_policy/
        geometry_solver_policy.py
        geometry_solver_policy_v1.yaml
        execution_plan.py
      providers/
        provider_api.py
        composite_provider.py
        newclid_adapter.py
        genesisgeo_adapter.py
        tonggeometry_adapter.py
        provider_run_manifest.py
      trace/
        geotrace_v1.py
        rule_registry_v1.py
        side_condition_calculus.py
        trace_compiler.py
      construction/
        auxiliary_construction_candidate_v1.py
        construction_compiler.py
      bridge/
        geometry_bridge_report.py
        relation_to_goal.py
      renderers/
        research_state_renderer.py
        worker_state_renderer.py

  lean/
    MathAutoResearch/
      Base/
      ProofState/
      Geometry/
        LeanGeoSubsetV1/
          Grammar.lean
          BridgeShim.lean
          ConstructionTemplates.lean
          RuleTemplates.lean
          Examples.lean
        Generated/
          .gitkeep

  schemas/
    base/
    proof_state/
    model/
    resources/
    geometry/
    evaluation/

  configs/
    selected_implementations/
      geometry_default.yaml
    model_provider_sets/
      default.example.yaml
    resource/
      default_local.yaml
      local.example.yaml
    solver_policies/
      geometry_synthetic_v1.yaml
    benchmark_runs/
      geometry_real_smoke.yaml
      geometry_level2_pilot.yaml
      geometry_level2_ablation.yaml

  benchmarks/
    geometry/
      leangeo_real_smoke.jsonl
      geometry_level2_pilot.jsonl
      rejected_by_extraction.jsonl

  scripts/
    bootstrap_env.sh
    probe_dependencies.py
    probe_local_resources.py
    check_old_specs_removed.py
    check_package_layout.py
    check_domain_contamination.py
    check_no_loose_options.py
    check_model_hardcode.py
    check_resource_bypass.py
    check_no_fixture_release.py
    check_release_acceptance.py
    run_geometry_level2_matrix.py
    generate_repro_report.py

  tests/
    unit/
    integration/
    regression/
    mutation/
    fixtures/

  runs/
    README.md
    .gitkeep

  artifacts/
    README.md
    .gitkeep

  vendor/
    README.md
```

---

## 5. Stable schemas and records

### R-SCHEMA-001 — Schema implementation technology

All cross-boundary records MUST be implemented as Pydantic v2 models or an equivalent typed schema layer that can emit JSON Schema. If Codex chooses an equivalent layer, it must provide identical validation, serialization, schema generation, and version stamping behavior.

Required behavior:

- `schema_version` appears in every serialized artifact.
- Unknown fields are rejected for proof-critical records.
- Hashes are deterministic.
- Schema changes alter schema hash and invalidate proof-critical caches.
- JSON schemas are emitted under `schemas/**`.

### R-SCHEMA-002 — Required Base records

Required Base records:

```text
ArtifactRef
RunRecord
RunConfig
SelectedImplementations
TrustReport
DiagnosticBundle
DependencyResolutionReport
LocalResourceProfile
ResourceBudgetProfile
ResourceUsageReport
FinalVerifyReport
ReleaseAcceptanceReport
```

### R-SCHEMA-003 — Required proof-state records

Required ProofState records:

```text
ObligationNode
DerivationNode
EvidenceRef
GraphPatch
GraphPatchCommitResult
DAGSnapshot
StateReaderSummary
```

### R-SCHEMA-004 — Required model records

Required model records:

```text
ModelProviderSetManifest
ModelSlot
ModelInvocationRequest
ModelInvocationRecord
ResearchControllerPluginManifest
ProofWorkerPluginManifest
ResearchStatePack
ActionPlan
WorkOrder
WorkerResult
ControllerStrategyLog
```

### R-SCHEMA-005 — Required geometry records

Required geometry records:

```text
TargetLibraryManifest
LeanGeoSubsetV1TheoremGrammar
PredicateMapping
ConstructionMapping
RelationMapping
GeometryExtractionReport
GeometryClaimSpec
GeometrySolveRequest
GeometryExecutionPlan
ProviderRunManifest
ProviderResult
ProviderDiagnostic
GeoTraceV1
RuleRegistryV1
TraceCompilationResult
AuxiliaryConstructionCandidateV1
ConstructionCompilationResult
GeometryBridgeReport
```

### R-SCHEMA-006 — Required evaluation records

Required evaluation records:

```text
BenchmarkTask
BenchmarkMatrix
EvaluationFunnel
MetricsReport
ResearchContributionRecord
ReproducibilityReport
```

---

## 6. Base runtime requirements

### R-BASE-001 — ArtifactStore

ArtifactStore MUST store all proof-critical and replay-critical artifacts by content hash.

Required methods:

```python
put_bytes(data: bytes, kind: str, metadata: dict) -> ArtifactRef
put_json(obj: BaseModel | dict, kind: str, metadata: dict) -> ArtifactRef
get(ref: ArtifactRef) -> bytes
verify(ref: ArtifactRef) -> bool
```

DAG nodes store only `ArtifactRef`, not raw contents.

### R-BASE-002 — RunLogger

RunLogger MUST link:

- selected implementations
- dependency report
- resource profile
- model invocations
- provider run manifests
- resource usage reports
- graph patches
- final verification reports
- release acceptance report

### R-BASE-003 — DiagnosticBundle

Every rejection, blocker, unsupported expression, resource rejection, dependency failure, provider timeout, extraction failure, compiler failure, and final verification failure MUST emit a `DiagnosticBundle`.

Required fields:

```yaml
DiagnosticBundle:
  diagnostic_id: "diag:<hash>"
  kind: "schema_error | unsupported_target | dependency_unavailable | extraction_rejected | provider_failed | provider_timeout | unsupported_rule | missing_side_condition | construction_blocked | lean_failed | theorem_hash_changed | resource_rejected | release_blocker"
  blame_layer: "base | model_provider | controller | worker | lean | geometry_plugin | provider | rule_registry | compiler | resource | dependency | unknown"
  severity: "repairable | retry_with_budget | blocked_until_dependency | plugin_bug_suspected | terminal"
  reason_codes: []
  repair_options: []
  evidence_refs: []
```

### R-BASE-004 — TrustGuard

TrustGuard MUST classify result levels and proof-use statuses.

Geometry result levels:

```text
diagnostic_only
raw_candidate
checked_claim_artifact
lean_patch_candidate
lean_compiled_candidate
lean_theorem
```

Proof-use statuses:

```text
not_allowed
search_only
claim_level_only
goal_level_allowed
final_theorem
```

Only `FinalVerifyGate` may produce `lean_theorem` or `final_theorem`.

---

## 7. ProofStateDAG requirements

### R-DAG-001 — Minimal node types

Base ProofStateDAG MUST use only:

```text
Obligation
Derivation
EvidenceRef
```

No geometry-specific Base node classes are allowed.

### R-DAG-002 — Closure semantics

```text
Obligation is closed iff at least one incoming proof-use Derivation is closed.

Derivation is closed iff:
  all required child Obligations are closed;
  all required gates passed;
  all EvidenceRefs are valid under the current TrustBoundary;
  proof_use_status is sufficient for the parent Obligation.
```

### R-DAG-003 — Acyclicity

Proof-use subgraph MUST be acyclic. Search-context edges do not participate in closure and may be stored in RunLogger/ResearchEventLog instead of DAG.

### R-DAG-004 — Invalidation

Invalidate or mark stale when any proof-critical hash changes:

```text
schema_hash
selected_implementations_hash
target_library_manifest_hash
geometry_extraction_contract_hash
geometry_claim_spec_hash
solver_policy_hash
execution_plan_hash
provider_adapter_hash
rule_registry_hash
construction_mapping_hash
trust_boundary_hash
protected_theorem_statement_hash
lean_dependency_hash
```

### R-DAG-005 — DAGWriter validation

DAGWriter MUST reject a patch if:

1. payload schema is unknown.
2. rule ID is unknown.
3. proof-use edge creates a cycle.
4. evidence kind is not allowed by rule.
5. status transition violates lattice.
6. raw output is used as proof evidence.
7. plugin tries to mutate Base-owned payload.
8. plugin tries to close a final theorem without FinalVerifyGate.
9. geometry-specific code bypasses Base GraphPatch validation.

---

## 8. Model provider and controller/worker requirements

### R-MODEL-001 — Base-level ModelProviderSet

Models are connected through Base-level `ModelProviderSet`.

`ResearchControllerPlugin` and `ProofWorkerPlugin` are model consumers. They MUST NOT own, hard-code, or secretly select GPT-Pro, Codex, DeepResearch, or any model.

### R-MODEL-002 — Model slots

Required model slots:

```yaml
model_slots:
  strategist:
    required_by: ["ResearchControllerPlugin"]
  proof_worker:
    required_by: ["ProofWorkerPlugin"]
  critic:
    required_by: []
    allowed_by: ["ResearchControllerPlugin", "ProofWorkerPlugin"]
```

Slots may be backed by one model, a local model, an API model, DeepResearch-style orchestration, or a multi-agent wrapper. Base sees only slot invocation contracts.

### R-MODEL-003 — Model invocation logging

Every model call MUST emit `ModelInvocationRecord` with:

```text
slot_id
provider_set_hash
request_hash
response_hash
token/usage metadata if available
redacted transcript artifact ref if stored
proof_use_status = not_allowed
```

### R-MODEL-004 — Controller contract

`ResearchControllerPlugin` input/output:

```python
plan_next_actions(state: ResearchStatePack, models: ModelProviderSet, context: RunContext) -> ActionPlan
```

It may propose:

- WorkOrders
- geometry.solve requests
- lemma candidates
- proof repair strategies
- construction requests
- diagnostics

It may not close proof obligations.

### R-MODEL-005 — ProofWorker contract

`ProofWorkerPlugin` input/output:

```python
execute_work_order(work_order: WorkOrder, models: ModelProviderSet, lean_port: LeanPort, resource_governor: ResourceGovernor) -> WorkerResult
```

It may edit admitted proof regions and helper lemma regions only.

---

## 9. Environment bootstrap requirements

### R-ENV-001 — Codex is authorized to bootstrap dependencies after approval

After this Base Spec and Plan are Guardian-admitted and the user explicitly approves implementation, Codex is authorized to install, vendor, pin, and configure required dependencies for approved scope.

This R-ID is not current permission while the documents are still candidates for review.

Allowed:

- Lean/lake dependencies
- LeanGeo-compatible package or source
- Python dependencies
- Newclid-compatible engine
- GenesisGeo-compatible engine/model/checkpoint
- TongGeometry-compatible engine
- local solver binaries
- system build tools when necessary

Codex MUST record all changes in repo-managed files.

### R-ENV-002 — DependencyResolutionReport

Every bootstrap attempt MUST emit:

```yaml
DependencyResolutionReport:
  report_id: "dep:<hash>"
  created_at: "..."
  os: "..."
  python_version: "..."
  lean_version: "..."
  lake_version: "..."
  packages: []
  engines:
    - role: "symbolic_closure"
      family: "newclid_compatible"
      install_status: "installed | vendored | unavailable | failed | skipped_by_policy"
      version_or_commit: "..."
      source: "git | pypi | local | release | manual"
      checkpoint_hash: null
      evidence_refs: []
    - role: "construction_proposer"
      family: "genesisgeo_compatible"
      install_status: "installed | vendored | unavailable | failed | skipped_by_policy"
    - role: "heavy_search"
      family: "tonggeometry_compatible"
      install_status: "installed | vendored | unavailable | failed | skipped_by_policy"
  unresolved:
    - component: "..."
      consequence: "blocks_experiment_ready | blocks_heavy_search | nonblocking"
```

### R-ENV-003 — No silent substitution

If LeanGeo-compatible support cannot be installed, Codex MUST NOT switch target to Mathlib-only or local toy geometry. It must mark real LeanGeo final theorem support blocked.

If Newclid/GenesisGeo/TongGeometry-compatible engines cannot be installed or vendored, Codex MUST NOT claim full experiment-ready. It may continue implementing scaffolding and fixtures.

---

## 10. Resource governance requirements

### R-RSRC-001 — ResourceGovernor is mandatory

All Lean builds, provider engines, proof worker subprocesses, local model calls when applicable, and heavy search runs MUST use `ResourceGovernor`.

### R-RSRC-002 — LocalResourceProfile

`probe_local_resources.py` MUST emit:

```yaml
LocalResourceProfile:
  profile_id: "sha256:..."
  os: "..."
  cpu_physical_cores: 0
  cpu_logical_cores: 0
  total_ram_mb: 0
  available_ram_mb_at_probe: 0
  gpu_devices: []
  disk_free_mb:
    artifact_root: 0
    temp_root: 0
  provider_engine_availability:
    symbolic_closure: "available | unavailable | unknown"
    construction_proposer: "available | unavailable | unknown"
    heavy_search: "available | unavailable | unknown"
```

### R-RSRC-003 — Budget profiles

Required budgets:

```text
tiny
small
medium
heavy
extreme
```

Defaults:

- reserve at least 15% CPU or 1–2 logical cores, whichever is larger.
- reserve at least 20% RAM or 4 GB, whichever is larger.
- reserve at least 10% disk free space.
- heavy search is exclusive by default.
- `extreme` may use most resources but must still use process groups, heartbeat, hard timeout, and reporting.

### R-RSRC-004 — Engine semaphores

Required semaphores:

```text
lean_build
final_verify
proof_worker
model_slot
symbolic_closure
construction_proposer
heavy_search
```

`heavy_search` MUST NOT run concurrently with another `heavy_search` unless local override explicitly permits and the override is logged.

### R-RSRC-005 — Timeout and process cleanup

Every external engine run must have:

1. soft timeout
2. hard timeout
3. heartbeat
4. process group cleanup
5. ResourceUsageReport
6. raw log artifact ref
7. no orphan children after kill

---

## 11. Lean integration requirements

### R-LEAN-001 — LeanPort

`LeanPort` MUST provide:

```python
compile_file(path: Path, budget: ResourceBudget) -> LeanCompileResult
extract_goals(path: Path, theorem_name: str) -> list[GoalAnchor]
summarize_errors(result: LeanCompileResult) -> LeanErrorSummary
```

### R-LEAN-002 — GoalAnchor

`GoalAnchor` MUST include:

```yaml
GoalAnchor:
  goal_id: "goal:<hash>"
  theorem_name: "..."
  file_path: "..."
  goal_hash: "sha256:..."
  protected_statement_hash: "sha256:..."
  lean_context_snapshot_hash: "sha256:..."
```

### R-LEAN-003 — ProofRegionGuard

ProofWorker may edit only:

- admitted proof block
- admitted helper lemma block
- generated files under `lean/MathAutoResearch/Geometry/Generated/**`

It MUST NOT edit theorem statement, assumptions, LeanGeo predicate definitions, or target library semantics.

### R-LEAN-004 — FinalVerifyGate

`FinalVerifyGate` MUST emit `FinalVerifyReport` and check:

- `lake build` or target Lean build succeeds.
- protected theorem statement hash unchanged.
- no sorry.
- no forbidden axioms.
- no unsafe declarations if strict policy forbids them.
- no local toy target substituted.
- proof-use provenance is valid.

---

## 12. TargetSubsetContract

### R-GEO-001 — TargetLibraryManifest

There is exactly one target library:

```yaml
TargetLibraryManifest:
  target_library_id: "LeanGeoSubsetV1"
  source_dependency: "LeanGeo-compatible"
  version_or_commit: "..."
  namespace_map_ref: "sha256:..."
  theorem_grammar_ref: "sha256:..."
  predicate_mapping_ref: "sha256:..."
  construction_mapping_ref: "sha256:..."
  relation_mapping_ref: "sha256:..."
```

### R-GEO-002 — LeanGeoSubsetV1 theorem grammar

`LeanGeoSubsetV1` MUST be theorem grammar, not just predicate list.

Required grammar categories:

```text
Object declarations:
  point variables
  lines from two distinct points
  circles from registered constructors

Hypothesis forms:
  distinctness
  collinearity
  parallel
  perpendicular
  midpoint
  concyclicity
  equal length
  equal angle where supported

Target forms:
  collinearity
  parallel
  perpendicular
  concyclicity
  equal length
  equal angle where supported

Rejected forms:
  arbitrary Mathlib geometry expression
  unsupported local notation
  unsupported quantifier alternation
  unsupported orientation semantics
  unsupported diagram case split
```

Every grammar entry MUST have positive, negative, ambiguous, and mutation fixtures.

### R-GEO-003 — Predicate, construction, relation mappings

Predicate mapping MUST specify:

- canonical predicate
- permutation policy
- required side conditions
- degeneracy policy
- orientation policy if applicable

Construction mapping MUST specify:

- construction ID
- Lean template ID
- required existence conditions
- uniqueness requirements if needed
- generated obligations

Relation mapping MUST classify:

```text
exact
sufficient
related
none
```

Only `exact` and correctly directed `sufficient` may proceed to compilation.

---

## 13. Geometry extraction requirements

### R-EXTRACT-001 — GeometryExtractionContract

The extractor MUST accept only Lean goals in `LeanGeoSubsetV1TheoremGrammar`.

It MUST produce `GeometryExtractionReport` and, if accepted, `GeometryClaimSpec`.

It MUST safe-reject unsupported expressions.

### R-EXTRACT-002 — Semantic extraction

The extractor MUST:

1. extract objects and relations from Lean context.
2. canonicalize accepted predicates.
3. normalize accepted local notation only if mapped.
4. extract nondegeneracy and orientation assumptions.
5. classify relation to target.
6. reject ambiguous or unsupported forms.
7. preserve protected theorem hash.

### R-EXTRACT-003 — GeometryClaimSpec provenance

`GeometryClaimSpec` in proof-use path MUST reference:

```text
GeometryExtractionReport
GoalAnchor
protected_statement_hash
target_library_manifest_hash
```

A `GeometryClaimSpec` created from raw DSL input has `proof_use_status = not_allowed`.

---

## 14. Geometry solver provider requirements

### R-SOLVER-001 — One Base-visible provider

Base sees exactly one `GeometrySolverProvider`.

```python
solve(request: GeometrySolveRequest, context: ProviderContext) -> ProviderResult
```

Base must not branch on Newclid/GenesisGeo/TongGeometry.

### R-SOLVER-002 — Composite provider internal roles

The selected provider has internal roles:

```yaml
internal_roles:
  symbolic_closure:
    family: "newclid_compatible"
    purpose: "primary symbolic closure and GeoTraceV1 source"
  construction_proposer:
    family: "genesisgeo_compatible"
    purpose: "auxiliary construction candidate generation"
  heavy_search:
    family: "tonggeometry_compatible"
    purpose: "heavy/extreme budget proof-plan or construction search"
```

### R-SOLVER-003 — Newclid-compatible role

Newclid-compatible adapter MUST:

1. convert `GeometryClaimSpec` to a supported engine input.
2. run real symbolic closure when dependency resolved.
3. normalize accepted output to `GeoTraceV1`.
4. return unsupported rules as blockers.
5. emit `ProviderRunManifest`.
6. emit `ResourceUsageReport`.

A fixture-only adapter cannot satisfy full experiment-ready.

### R-SOLVER-004 — GenesisGeo-compatible role

GenesisGeo-compatible adapter MUST:

1. run only when policy requests construction proposal.
2. normalize output to `AuxiliaryConstructionCandidateV1`.
3. keep raw construction rationale as non-proof artifact.
4. emit `ProviderRunManifest`.
5. emit `ResourceUsageReport`.

Raw Genesis output cannot close obligations.

### R-SOLVER-005 — TongGeometry-compatible role

TongGeometry-compatible adapter MUST:

1. run only for `heavy` or `extreme` budget or explicit policy escalation.
2. use `heavy_search` semaphore.
3. return proof-plan diagnostics, construction candidates, or normalized `GeoTraceV1` if supported.
4. keep raw Tong output non-proof.
5. emit `ProviderRunManifest`.
6. emit `ResourceUsageReport`.

### R-SOLVER-006 — GeometrySolverPolicy

Default routing:

```text
1. Try Newclid-compatible symbolic_closure.
2. If closure fails and policy permits, call GenesisGeo-compatible construction_proposer.
3. If construction candidate is admitted, retry symbolic_closure with admitted construction.
4. If budget is heavy/extreme, optionally call TongGeometry-compatible heavy_search.
5. Consolidate normalized artifacts and diagnostics.
```

Policy MUST be deterministic, versioned, hashed, logged, and resource-aware.

---

## 15. CompilerContract

### R-RULE-001 — RuleRegistryV1

`RuleRegistryV1` MUST be target-library-specific for `LeanGeoSubsetV1`.

Each supported rule MUST include:

```yaml
rule_id: "geo.<name>.v1"
provider_trace_patterns: []
lean_template_id: "..."
premise_pattern: []
conclusion_pattern: []
required_side_conditions: []
generated_obligations: []
auto_discharge_policy: "context_lookup | simple_tactic | proof_worker | blocker"
unsupported_variants: []
fixtures:
  positive: []
  negative: []
  ambiguous: []
  mutation: []
```

A rule missing side conditions or fixtures is invalid.

### R-TRACE-001 — GeoTraceV1

`GeoTraceV1` MUST contain normalized steps only:

```yaml
GeoTraceV1:
  trace_id: "trace:<hash>"
  source_provider_result: "sha256:..."
  target_library: "LeanGeoSubsetV1"
  claim_spec_ref: "sha256:..."
  steps:
    - step_id: "..."
      rule_id: "..."
      premises: []
      conclusion: "..."
      side_condition_refs: []
      source_raw_ref: "sha256:..."
  unsupported_steps: []
```

### R-TRACE-002 — TraceCompiler

TraceCompiler MUST compile only supported steps.

Unsupported rule, malformed trace, missing side condition, orientation mismatch, or unsupported variant MUST produce blocker diagnostics, not proof success.

### R-AUX-001 — AuxiliaryConstructionCandidateV1

Required fields:

```yaml
AuxiliaryConstructionCandidateV1:
  construction_id: "aux:<hash>"
  source_provider_result: "sha256:..."
  construction_kind: "intersection_of_two_nonparallel_lines | foot_of_perpendicular | midpoint | line_through_two_distinct_points | circle_through_center_and_point | plugin_supported"
  introduced_objects: []
  dependencies: {}
  required_side_conditions:
    nondegeneracy: []
    incidence: []
    existence: []
    uniqueness_if_needed: []
    orientation: []
    diagram_cases: []
  lean_introduction_plan:
    theorem_template_id: "..."
    generated_obligations: []
  proof_use_status: "not_allowed_until_final_verify"
```

### R-AUX-002 — ConstructionCompiler

ConstructionCompiler MUST:

1. validate construction kind.
2. validate dependency refs.
3. generate Lean introduction patch candidate.
4. generate side-condition obligations.
5. block if existence/nondegeneracy cannot be established.
6. never treat natural-language rationale as proof.

---

## 16. Bridge and trust requirements

### R-BRIDGE-001 — GeometryBridgeGate

BridgeGate is lightweight but mandatory.

It verifies:

1. proof-use path began from extraction.
2. `GeometryClaimSpec` corresponds to `GoalAnchor`.
3. relation to goal is exact or sufficiently directed.
4. protected theorem identity is unchanged.
5. raw DSL-originated path is not used.

BridgeGate is not final verification.

### R-TRUST-001 — Trust classification

TrustGuard MUST reject proof-use closure for:

- model output
- raw provider output
- raw DSL input
- unsupported trace
- fixture provider output in release config
- construction rationale
- worker text claim
- Lean compile success without protected hash/no-sorry checks

### R-TRUST-002 — Allowed claims

Allowed after evidence:

- schemas/contracts implemented.
- dependency bootstrap resolved or blocked with report.
- real Newclid/GenesisGeo/TongGeometry adapter smoke evidence exists.
- LeanGeoSubsetV1 extraction works on approved corpus.
- specific Lean theorem fixture passed FinalVerifyGate.
- Level2 pilot matrix ran and produced replayable metrics.
- observed improvement on metric X if metrics actually show it.

Disallowed without separate evidence:

- open-problem solving.
- arbitrary LeanGeo/Mathlib support.
- raw solver trace trusted as proof.
- fixture-level acceptance equals v0.3 full completion.
- resource policy optimal for all machines.

---

## 17. Evaluation requirements

### R-EVAL-001 — Corpus definitions

Required corpora:

```text
LeanGeoSubsetV1.RealSmokeCorpus:
  non-fixture Lean files importing LeanGeo-compatible dependency.
  minimum 12 tasks.
  includes accepted extraction, safe-reject extraction, final verification, provider trace, and auxiliary construction cases.

GeometryLevel2PilotCorpus:
  non-fixture benchmark matrix population.
  minimum 25 tasks.
  includes at least:
    10 simple symbolic closure tasks;
    5 auxiliary-construction tasks;
    5 proof-worker-only baseline tasks;
    5 safe-reject or blocker tasks.
```

If actual LeanGeo package lacks enough examples, Codex may author synthetic Lean theorem files using real LeanGeo definitions. These are allowed only if they import LeanGeo-compatible dependency and are represented in TargetLibraryManifest. They must not use local toy predicates as target semantics.

### R-EVAL-002 — Baseline matrix

Required evaluation configs:

```text
B0: ProofWorker-only
B1: ResearchController + ProofWorker, no geometry.solve
B2: Full geometry-enabled pipeline
B3: strong-model without geometry.solve
B4: lower-model + geometry.solve
B5: full provider with auxiliary construction disabled
```

These are evaluation configurations, not runtime Agent modes.

### R-EVAL-003 — Metrics

Required metrics:

```text
final_theorem_rate
lean_compile_success_rate
proof_repair_success_rate
geometry_solve_request_count
provider_success_rate_by_role
trace_compile_success_rate
construction_candidate_accepted_count
side_condition_blocker_count
resource_usage_by_role
timeout_count
diagnostic_kind_counts
replay_success_rate
```

### R-EVAL-004 — Experiment-ready does not require positive advantage

`V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` requires the Level2 pilot matrix to run and replay. It does not require geometry-enabled pipeline to outperform baselines. A positive advantage claim requires metrics showing the advantage.

---

## 18. Required tests and release commands

### R-TEST-001 — Required command surface

Final repo MUST support:

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
make smoke-real-newclid
make smoke-real-genesisgeo
make smoke-real-tonggeometry
make smoke-geometry-provider
make smoke-geometry-trace
make smoke-geometry-construction
make smoke-geometry-final-verify
make smoke-level2-pilot

python scripts/check_old_specs_removed.py
python scripts/check_package_layout.py
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
```

### R-TEST-002 — Required regression families

Regression suite MUST include:

1. domain contamination.
2. old specs removed.
3. no loose options.
4. model hard-code.
5. resource bypass and orphan cleanup.
6. dependency substitution.
7. fixture release misuse.
8. raw output laundering.
9. raw DSL proof-use laundering.
10. extraction mutation.
11. RuleRegistry side-condition mutation.
12. TraceCompiler malformed/unsupported trace.
13. ConstructionCompiler missing existence/nondegeneracy.
14. ProofRegionGuard theorem statement mutation.
15. FinalVerifyGate no-sorry/no-axiom.

### R-TEST-003 — Release acceptance fails on blockers

Release acceptance MUST fail if:

1. old root draft specs remain active.
2. Base imports geometry-specific modules or names.
3. AgentC/D core modes exist.
4. target library is not exactly LeanGeoSubsetV1.
5. real dependency report is missing or unresolved for claimed components.
6. fixture provider selected in release config.
7. Newclid/GenesisGeo/TongGeometry real smoke evidence missing.
8. provider process bypasses ResourceGovernor.
9. raw output closes an obligation.
10. raw DSL problem reaches `goal_level_allowed`.
11. RuleRegistry rule lacks side-condition calculus.
12. missing side condition is silently assumed.
13. theorem statement can be changed and still pass FinalVerifyGate.
14. `ProviderRunManifest`, `ResourceUsageReport`, or `DependencyResolutionReport` missing.
15. Level2 pilot matrix has not run/replayed.
16. closure claims lack fresh evidence.

---

## 19. Mechanisms

### MECH-REBASE-001 — Repo cleanup mechanism

```text
audit current repo
  -> list root docs and duplicate packages
  -> install approved BASE_SPEC/PLAN under docs/ai/changes/geometry-lean-v0_3-full-rebase/
  -> delete or hash-index superseded root specs
  -> consolidate Python package under src/math_auto_research
  -> ensure fixture-only code is under tests/fixtures
  -> run check_old_specs_removed.py and check_package_layout.py
```

### MECH-BOOT-001 — Dependency bootstrap

```text
probe system
  -> inspect Lean/lake/Python
  -> add/pin LeanGeo-compatible dependency
  -> add/pin Python dependencies
  -> install/vendor Newclid-compatible engine
  -> install/vendor GenesisGeo-compatible engine/checkpoint
  -> install/vendor TongGeometry-compatible engine
  -> run smoke commands
  -> emit DependencyResolutionReport
  -> fail full experiment-ready claim if unresolved
```

### MECH-MODEL-001 — Model injection

```text
RunConfig
  -> SelectedImplementations.model_provider_set
  -> ModelProviderSetManifest
  -> resolve model slots
  -> inject slot handles into ResearchControllerPlugin and ProofWorkerPlugin
  -> record ModelInvocationRecord
  -> model outputs remain non-proof artifacts
```

### MECH-RSRC-001 — Resource governance

```text
LocalResourceProfile
  -> ResourceBudgetProfile
  -> ResourceGovernor admission
  -> named semaphore acquisition
  -> ProcessRunner process group
  -> heartbeat monitor
  -> timeout / kill
  -> ResourceUsageReport
  -> ProviderRunManifest / RunRecord linkage
```

### MECH-PROOF-001 — Verified geometry proof path

```text
Lean theorem/goal
  -> GoalAnchor
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> GeometrySolverPolicy
  -> CompositeSyntheticGeometryProvider
  -> GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> RuleRegistryV1/TraceCompiler or ConstructionCompiler
  -> Lean patch candidate
  -> ProofWorkerPlugin
  -> LeanPort
  -> FinalVerifyGate
  -> lean_theorem
```

### MECH-EVAL-001 — Level2 pilot evaluation

```text
approved corpus
  -> run B0/B1/B2/B3/B4/B5 configs
  -> each run logs selected implementations, dependency report, resource profile
  -> collect final theorem status and diagnostics
  -> generate MetricsReport
  -> replay sampled runs
  -> generate ReproducibilityReport
  -> release acceptance may claim experiment-ready, not advantage unless metrics support it
```

---

## 20. Release blockers

The following are completion-blocking for `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`:

1. Base Spec and Plan not approved or not installed under the new change folder.
2. Superseded root spec files remain active.
3. Duplicate `math_auto_research` package layout remains ambiguous.
4. Base imports geometry-specific modules or names.
5. AgentC/D core runtime terminology appears in classes, modes, enums, CLI options, or configs.
6. `SelectedImplementations` uses arrays for any selected boundary.
7. Controller/worker hard-code model identifiers or endpoints instead of model slots.
8. Environment setup is skipped because a dependency is missing.
9. Dependency failures are not captured in `DependencyResolutionReport`.
10. LeanGeo target support is silently replaced.
11. Real Newclid/GenesisGeo/TongGeometry smoke evidence missing.
12. Fixture adapters selected in release config.
13. Provider process bypasses `ResourceGovernor`.
14. Heavy search can starve Lean final verification.
15. Raw provider/model output closes an obligation.
16. Raw DSL-originated problem can produce goal-level proof-use.
17. RuleRegistry rule missing side-condition calculus.
18. Missing side condition silently assumed.
19. TraceCompiler attempts arbitrary trace translation and marks unsupported rules as success.
20. ConstructionCompiler treats natural-language rationale as proof.
21. Protected theorem statement can change without FinalVerifyGate rejection.
22. `ProviderRunManifest`, `ResourceUsageReport`, `DependencyResolutionReport`, or `FinalVerifyReport` missing for relevant runs.
23. Level2 pilot corpus absent or fixture-only.
24. Level2 pilot matrix cannot run/replay.
25. Closure claims exceed evidence.

---

## 21. Final closure requirements

A closure report for this rebase MUST include:

```text
approved spec path
approved plan path
commit hash
repo audit evidence
deleted/superseded spec evidence
dependency resolution report
local resource profile
selected implementations hash
real Newclid smoke report
real GenesisGeo smoke report
real TongGeometry smoke report
LeanGeo target manifest
LeanGeoSubsetV1 corpus manifest
test command evidence
release acceptance report
Level2 pilot run report
reproducibility report
known blockers, if any
allowed claims
disallowed claims
```

Allowed closure claim only if all release blockers are absent:

```text
The repo is V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY for the approved LeanGeoSubsetV1 geometry × Lean scope.
```
