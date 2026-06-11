---
title: Guardian Base Spec — geometry × Lean 自動研究 pipeline v0.3
spec_id: MARP-GEOLEAN-BASE-003
version: v0.3-admission-candidate
status: SOURCE_FIDELITY_REVIEW_PASSED_PENDING_USER_IMPLEMENTATION_APPROVAL
created: 2026-06-10
last_updated: 2026-06-11
lane: Guardian Lane
purpose: Define correctness requirements for implementing the geometry × Lean v0.3 pipeline.
authority: Authoritative after guardian admission and explicit user implementation approval; not an implementation plan.
source_documents:
  - geometry_lean_pipeline_plan_v0_3.md
  - geometry_lean_pipeline_review_v0_2_revised.md
  - fatal_risks_1_2_3_geometry_lean_review.md
  - math_auto_research_pipeline_final_repo_plan_v1_2.md
  - user decisions through 2026-06-10 conversation
intended_repository_root: C:\Users\bakat\work\AI_math_research
---

# Guardian Base Spec — geometry × Lean 自動研究 pipeline v0.3

## Context Packet

Spec ID: `MARP-GEOLEAN-BASE-003`  
Type: Change Base Spec / implementation authority candidate  
Status: Source-fidelity review passed. Explicit user approval is still required before this becomes implementation authority.  
Parent: none declared in this workspace. If a repo-wide Base Spec is later added, this spec must be admitted as a child and must declare exact parent R-IDs before conflicting implementation work proceeds.  
Scope: v0.3 geometry × Lean plan を Codex agent が実装できる Guardian Base Spec に変換する。今回の改訂では、環境構築権限、Base-level `ModelProviderSet`、Composite synthetic geometry solver、local PC resource governance を追加する。  
Applies To: `src/math_auto_research/**`, `plugins/geometry_synthetic/**`, `lean/MathAutoResearch/Geometry/**`, `schemas/**`, `configs/**`, `benchmarks/geometry/**`, `tests/**`, `scripts/**`, `docs/architecture/**`, `docs/ai/**`.  
Blocking Questions: none. `QD-001` from the previous draft is retired and replaced by `R-ENV-*`.  
Non-blocking Debt: source documents S2-S4 are referenced by the v0.3 plan and draft source map but are not present in the current workspace; source-fidelity claims are therefore limited to the provided v0.3 source plan and draft Guardian artifacts unless those sources are supplied.  
Known Exceptions: none.  
Read-First R-IDs: `R-ARCH-001`, `R-NOOPT-001`, `R-ENV-001`, `R-MODEL-001`, `R-RSRC-001`, `R-GEO-001`, `R-EXTRACT-001`, `R-SOLVER-001`, `R-RULE-001`, `R-TRUST-001`, `R-VERIFY-001`, `R-V03-SCHEMA-001`, `R-V03-EXT-001`.  
Context Packet Authority: non-authoritative digest. The R-ID body below is authoritative.

---

## 0. Authority, status, and implementation permission

This file defines **what correctness means** for the geometry × Lean v0.3 implementation.

It is not an implementation plan. The paired Plan must not add requirements, weaken requirements, reinterpret this Base Spec, or convert excluded items into implementation tasks. If this Base Spec and the Plan conflict, this Base Spec wins.

Implementation may begin only after the user explicitly approves this Base Spec and the paired Plan. Until approval, Codex may read, review, refine, and propose changes, but must not start repository implementation.

---

## 1. Purpose

The purpose of this change is to implement the initial `geometry × Lean` target of the mathematical automatic research pipeline.

The system must take a Lean theorem that is already correctly formalized in a deliberately restricted `LeanGeoSubsetV1`, use model/controller plugins and synthetic geometry solver providers to search for proof strategies, auxiliary constructions, and trace candidates, and produce a final Lean theorem only when Lean final verification succeeds without changing the protected theorem statement.

The implementation must preserve the project’s core design philosophy:

1. Base pipeline remains domain-neutral.
2. Domain intelligence lives in plugins.
3. ProofStateDAG is minimal and proof-use oriented.
4. Plugin updates go through GraphPatch and DAGWriter.
5. Raw solver/provider/model output is never proof evidence by itself.
6. Lean final verification is the authority for `final_theorem` claims in this initial geometry target.
7. Environment bootstrap is allowed, but dependency changes must be reproducible and logged.
8. Models are not hard-coded inside controller/worker plugins; models are provided through a Base-level `ModelProviderSet`.
9. Newclid / GenesisGeo / TongGeometry are not Base concepts; they are internal engine roles inside the selected `GeometrySolverProvider`.
10. Local PC resource usage is managed by a deterministic `ResourceGovernor`; heavy solver runs must not starve Lean build, ProofWorker, or system responsiveness.

---

## 2. Scope

### 2.1 In scope

The implementation MUST include:

1. Base runtime contracts for artifacts, run logging, trust reports, diagnostics, selected implementations, replay metadata, release acceptance checks, and resource governance.
2. Domain-neutral ProofStateDAG core with `Obligation`, `Derivation`, `EvidenceRef`, `GraphPatch`, `DAGWriter`, closure, acyclicity, invalidation, and StateReader summaries.
3. Base-level model connection contracts: `ModelProviderSet`, `ModelSlot`, `ModelInvocationRecord`, and injection into controller/worker plugins.
4. Model-consuming plugin contracts: `ResearchControllerPlugin`, `ProofWorkerPlugin`, `ResearchStatePack`, `ActionPlan`, `WorkOrder`, and `WorkerResult`.
5. Reproducible dependency bootstrap: Lean/lake, LeanGeo-compatible package, Python packages, Newclid-compatible engine, GenesisGeo-compatible model/engine, TongGeometry-compatible engine where available.
6. Local resource management: `LocalResourceProfile`, `ResourceBudgetProfile`, `ResourceGovernor`, per-engine semaphores, admission control, timeout/kill policy, and `ResourceUsageReport`.
7. Lean integration: `LeanPort`, `GoalAnchor`, protected theorem statement hash, `ProofRegionGuard`, `LeanErrorSummary`, and `FinalVerifyGate`.
8. Geometry plugin `geometry_synthetic` with `geometry.solve` facade.
9. `TargetSubsetContract`: `LeanGeoSubsetV1TheoremGrammar`, predicate / construction / relation mapping, fixtures, `GeometryExtractionContract`, `GeometryExtractionReport`, and `GeometryClaimSpec`.
10. `GeometrySolverProvider` boundary, deterministic `GeometrySolverPolicy`, `GeometryExecutionPlan`, `ProviderRunManifest`, and `ProviderResult`.
11. Composite synthetic geometry provider with internal roles: Newclid-compatible symbolic closure, GenesisGeo-compatible auxiliary construction proposer, TongGeometry-compatible heavy search oracle. Base must see only one selected provider.
12. `CompilerContract`: `GeoTraceV1`, `RuleRegistryV1`, side-condition calculus, `TraceCompiler`, `AuxiliaryConstructionCandidateV1`, `ConstructionCompiler`.
13. `BridgeGate`, `TrustGuard`, and result-level classification suitable for geometry × Lean.
14. Run trace and evaluation records: `ControllerStrategyLog`, `ResearchContributionRecord`, `EvaluationFunnel`, reproducibility report, `ProviderRunManifest`, and `ResourceUsageReport`.
15. Regression and mutation tests that prevent option creep, proof-use laundering, extraction unsoundness, missing side conditions, protected theorem edits, dependency substitution, and resource policy bypass.
16. Level 2 evaluation harness showing whether `geometry.solve` improves Lean proof completion relative to controller/worker-only baselines.

### 2.2 Out of scope

The implementation MUST NOT attempt to include:

1. Natural-language problem to Lean theorem formalization.
2. Informal problem fidelity audit.
3. Diagram image recognition.
4. Multi-target library bridge across LeanGeo, Mathlib geometry, and a local geometry micro-library.
5. AgentC / AgentD core modes or A/B/C/D runtime taxonomy.
6. Provider-specific proof semantics in Base.
7. Raw DSL problem proof-use path.
8. Arbitrary Newclid / GenesisGeo / TongGeometry trace translation.
9. Coordinate / Wu / Groebner / SOS proof path as proof-use authority.
10. A claim that the system solves open problems.
11. Unbounded background solver execution outside `ResourceGovernor`.
12. A claim that local resource profiles are portable across machines.

Coordinate, Wu, Groebner, SOS, or analytic methods MAY be used inside a provider only as search hints or construction/diagnostic generators. Their outputs remain non-proof artifacts unless converted into accepted `GeoTraceV1` or `AuxiliaryConstructionCandidateV1` artifacts and then verified through the compiler and Lean final verification path.

---

## 3. Source classification

| Source unit | Classification | Normative effect |
|---|---:|---|
| User decision: no loose optional AgentC/D; remove AgentC/D taxonomy from core | EXACT | `R-NOOPT-002`, `R-MODEL-001` |
| User decision: model connections must be externally swappable | EXACT | `R-MODEL-*` |
| User decision: Codex may perform dependency setup | EXACT | `R-ENV-*` |
| User decision: Newclid / GenesisGeo / TongGeometry should be used as synthetic solvers, not coordinate solvers | EXACT | `R-SOLVER-*`, `R-ENGINE-*` |
| User decision: local PC resources may be substantially allocated, but must be planned carefully | LOCAL_EXECUTION_EXTENSION | `R-RSRC-*`, `R-V03-EXT-001` |
| v0.3 decision: target library fixed to LeanGeoSubsetV1 | EXACT | `R-GEO-001` |
| v0.3 decision: proof-use path starts from Lean goal extraction | EXACT | `R-EXTRACT-001` |
| v0.3 decision: raw DSL / raw trace not proof | EXACT | `R-TRUST-001` |
| v0.3 decision: auxiliary construction candidate is standard contract | EXACT | `R-AUX-001` |
| v0.3 decision: RuleRegistryV1 has side-condition calculus | EXACT | `R-RULE-001` |
| fatal risk review: Lean theorem to DSL extraction is semantic, not parser-only | EXACT | `R-EXTRACT-001`, `R-EXTRACT-002` |
| fatal risk review: TraceCompiler needs supported rule subset and side-condition calculus | EXACT | `R-RULE-*`, `R-TRACE-*` |
| fatal risk review: target library must be one library | EXACT | `R-GEO-001`, `R-GEO-002` |
| v1.2 base/domain separation and GraphPatch-only mutation | ADAPTED | `R-ARCH-*`, `R-DAG-*` |
| finite_graph-specific claim templates, certificates, coverage | OUT_OF_SCOPE | not implemented in this geometry initial target |
| Guardian Lane process | REFERENCE_ONLY for artifact format; normative only where explicitly stated in R-IDs | `R-GUARD-*` |
| v0.3 detailed contract schemas, workflows, blockers, and checklist | EXACT | `R-V03-*` |

---

## 4. Requirement IDs

### 4.1 Guardian and authority requirements

#### R-GUARD-001 — Base Spec authority

MUST: This Base Spec is the authority for correctness after approval. The Plan, task instructions, active context, source map, handoff notes, and agent memory must not override it.

Acceptance:

- `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md` exists.
- `docs/ai/changes/geometry-lean-v0_3/PLAN.md` declares this spec ID.
- Plan tasks map to R-IDs and do not introduce requirements not present here.

#### R-GUARD-002 — Evidence-bound claims

MUST: Final closure claims must be limited to evidence actually produced by commands or review artifacts. Strong claims such as `ACCEPTANCE_COMPLETE`, `VERIFIED`, or `SOURCE_FAITHFUL` must cite fresh evidence files and must have no blocking QuestionDebt for the claimed scope.

Acceptance:

- `CLOSURE.md` template or generated closure includes command evidence paths.
- Release acceptance script emits a machine-readable report.
- Closure cannot claim final theorem success without `FinalVerifyReport` references.

#### R-GUARD-003 — Implementation permission gate

MUST: Codex must not implement until the user approves the Base Spec and Plan. Drafting, review, and refinement are allowed before approval.

Acceptance:

- `ACTIVE_CONTEXT.md` states `Implementation permission: missing` until user approval is recorded.
- Plan task `T00` records user approval before implementation tasks can be marked admitted.

---

### 4.2 Architecture and boundary requirements

#### R-ARCH-001 — Domain-neutral Base

MUST: Base runtime must not import or branch on `geometry_synthetic`, LeanGeo predicates, Newclid, GenesisGeo, TongGeometry, or any geometry-specific concept except through registered schemas and plugin manifests.

Acceptance:

- Domain contamination test fails if `src/math_auto_research/base/**` or `src/math_auto_research/proof_state/**` imports `plugins.geometry_synthetic` or references `Newclid`, `GenesisGeo`, `TongGeometry`, `LeanGeoSubsetV1`, `collinear`, `parallel`, `perpendicular`, or `concyclic`.
- Base schemas contain no geometry-specific field names.

#### R-ARCH-002 — Plugin-owned domain intelligence

MUST: Geometry-specific grammar, extraction, solver policy, trace rules, side conditions, construction semantics, rendering, and provider wrappers must live under `plugins/geometry_synthetic/**` or `lean/MathAutoResearch/Geometry/**`, not Base.

Acceptance:

- `plugins/geometry_synthetic/plugin.yaml` registers the geometry capability and schemas.
- Base registries load plugin schemas by manifest, not hard-coded imports.

#### R-ARCH-003 — Stable contracts first

MUST: All public cross-boundary records must be schema-backed and versioned.

Required schemas:

- Base: `ArtifactRef`, `RunRecord`, `TrustReport`, `DiagnosticBundle`, `SelectedImplementations`, `LocalResourceProfile`, `ResourceBudgetProfile`, `ResourceUsageReport`.
- Proof state: `ObligationNode`, `DerivationNode`, `EvidenceRef`, `GraphPatch`, `GraphPatchCommitResult`.
- Model API: `ModelProviderSetManifest`, `ModelSlot`, `ModelInvocationRequest`, `ModelInvocationRecord`, `ResearchStatePack`, `ActionPlan`, `WorkOrder`, `WorkerResult`.
- Geometry: `LeanGeoSubsetV1TheoremGrammar`, `GeometryExtractionReport`, `GeometryClaimSpec`, `GeometrySolveRequest`, `GeometryExecutionPlan`, `ProviderRunManifest`, `ProviderResult`, `GeoTraceV1`, `RuleRegistryV1`, `AuxiliaryConstructionCandidateV1`, `TraceCompilationResult`, `ConstructionCompilationResult`, `GeometryBridgeReport`.
- Evaluation: `ControllerStrategyLog`, `ResearchContributionRecord`, `EvaluationFunnel`, `MetricsReport`.

Acceptance:

- JSON schemas or Pydantic/dataclass schemas exist for every listed record.
- Schema version appears in every serialized artifact.
- Proof-critical schema changes invalidate affected cached artifacts.

---

### 4.3 No loose options requirements

#### R-NOOPT-001 — No loose options

MUST: The core runtime must not expose optional runtime modes for agents, providers, target libraries, trace compilers, trust bypasses, bridge targets, or resource-governor bypasses.

Acceptance:

- `SelectedImplementations` has scalar fields, not arrays, for target library, model provider set, controller, worker, provider, solver policy, rule registry, resource policy, and trust boundary.
- `scripts/check_no_loose_options.py` fails on core `AgentC`, `AgentD`, `mode_a`, `mode_b`, `mode_c`, `mode_d`, multiple target libraries, provider-specific branches in Base, or trust/resource bypass flags.

#### R-NOOPT-002 — Agent C/D taxonomy removed

MUST: Agent C/D terminology must not appear as core runtime classes, modes, enums, CLI options, config modes, or benchmark run modes.

Allowed:

- A `ResearchControllerPlugin` may internally use multi-agent orchestration, deep research, population search, or rater logic.
- Such internals must be recorded only through `ControllerStrategyLog` capability flags and counts.

Acceptance:

- No `AgentC` / `AgentD` core classes or run modes exist.
- Baselines are evaluation configurations, not runtime agent modes.

#### R-NOOPT-003 — Exactly-one-selected implementation

MUST: Each run must have exactly one selected implementation for each public boundary.

Required scalar selections:

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

MUST NOT: Represent Newclid / GenesisGeo / TongGeometry as three Base-level provider options. They are internal roles of the selected `GeometrySolverProvider`.

Acceptance:

- `SelectedImplementations` is logged in every `RunRecord`.
- Cache keys include `SelectedImplementations` hash.

---

### 4.4 Environment bootstrap requirements

#### R-ENV-001 — Reproducible dependency bootstrap authorization

MUST: Codex is authorized to perform reproducible dependency setup for the approved scope, including Lean/lake packages, LeanGeo-compatible dependencies, Python packages, Newclid-compatible provider dependencies, GenesisGeo-compatible model files, TongGeometry-compatible local engines, solver binaries, and local build tools.

MUST: All dependency additions must be recorded in repo-managed files.

Required records when applicable:

- `lakefile.lean` / `lake-manifest.json`.
- `pyproject.toml` / lockfile such as `uv.lock` or equivalent.
- `scripts/bootstrap_env.sh` or equivalent.
- `configs/dependencies/*.yaml`.
- `docs/ai/changes/geometry-lean-v0_3/evidence/dependency_resolution.md`.

MUST NOT: Silently replace LeanGeoSubsetV1 with Mathlib-only geometry or a local toy library as the target library.

Acceptance:

- `make setup` or `scripts/bootstrap_env.sh` produces a `DependencyResolutionReport`.
- Dependency resolution report includes versions, commits, model/checkpoint hashes if applicable, and commands run.
- If dependency resolution fails, real LeanGeo final theorem support remains blocked, but schema/scaffold/test-fixture work may continue.

#### R-ENV-002 — DependencyResolutionReport

MUST: Every dependency bootstrap attempt must emit `DependencyResolutionReport`.

Required fields:

```yaml
DependencyResolutionReport:
  report_id: "..."
  created_at: "..."
  os: "..."
  python_version: "..."
  lean_version: "..."
  lake_version: "..."
  packages:
    - name: "..."
      source: "git | local | pypi | release | manual"
      version_or_commit: "..."
      lock_ref: "..."
  engines:
    - role: "symbolic_closure | construction_proposer | heavy_search"
      family: "newclid_compatible | genesisgeo_compatible | tonggeometry_compatible"
      install_status: "installed | unavailable | skipped_by_policy | failed"
      version_or_commit: "..."
      checkpoint_hash: "nullable sha256:..."
  unresolved:
    - component: "..."
      consequence: "blocks_real_final_theorem | blocks_heavy_search | nonblocking"
  evidence_refs:
    - "sha256:..."
```

Acceptance:

- Report is stored as artifact and linked from `RunRecord` or setup evidence.
- Release acceptance fails if a required component is unavailable but claimed as available.

#### R-ENV-003 — Environment setup may not weaken target scope

MUST: If LeanGeo-compatible target support cannot be installed or pinned, Codex must not switch target library. It must mark real LeanGeo final theorem support as blocked and continue only with non-final scaffolding or fixtures.

Acceptance:

- `check_release_acceptance.py` fails any real final theorem claim unless `DependencyResolutionReport` shows target dependency resolved.

---

### 4.5 Model provider requirements

#### R-MODEL-001 — Base-level ModelProviderSet

MUST: Models are connected through a Base-level `ModelProviderSet`. ResearchController and ProofWorker plugins are model consumers, not model owners.

MUST: GPT-Pro, Codex, DeepResearch, local models, smaller models, or multi-agent orchestration must be swappable by changing `ModelProviderSetManifest` and selected implementations, not by changing Base code.

Acceptance:

- `src/math_auto_research/base/model_provider_set.py` or equivalent exists.
- `ResearchControllerPluginManifest` declares required/allowed model slots.
- `ProofWorkerPluginManifest` declares required/allowed model slots.
- No controller/worker plugin hard-codes provider credentials or model identifiers outside manifest/config.

#### R-MODEL-002 — Model slots

MUST: `ModelProviderSetManifest` define named model slots. Slots may be backed by one model, a model wrapper, or an orchestration provider, but Base sees only slot invocation contracts.

Example:

```yaml
ModelProviderSetManifest:
  provider_set_id: "model_provider_set:geometry_default:v1"
  model_slots:
    strategist:
      provider: "openai_or_replacement"
      model_id: "gpt-pro-or-replacement"
      capabilities: ["long_context_reasoning", "strategy_generation"]
    proof_worker:
      provider: "codex_or_replacement"
      model_id: "codex-agent-or-replacement"
      capabilities: ["repo_editing", "lean_error_repair"]
    critic:
      provider: "openai_or_local_or_none"
      model_id: "declared-or-disabled"
      capabilities: ["proof_plan_review"]
  invocation_policy:
    logging_required: true
    raw_model_output_proof_use: false
```

Acceptance:

- RunRecord logs provider set hash and used slot IDs.
- Model invocation records are artifacts, not proof evidence.

#### R-MODEL-003 — Model output is never proof evidence

MUST: Model output may propose proof edits, work orders, solver calls, auxiliary constructions, or diagnostics, but may not directly close obligations.

Acceptance:

- TrustGuard rejects `model_output` evidence kind for proof-use closure.
- Regression test: model says “proved” without Lean final verification -> cannot produce `final_theorem`.

---

### 4.6 Local resource governance requirements

#### R-RSRC-001 — ResourceGovernor is mandatory

MUST: All Lean builds, ProofWorker runs, provider engine calls, model calls where locally constrained, and heavy searches must be admitted through a deterministic `ResourceGovernor`.

MUST NOT: Provider adapters spawn untracked long-running processes.

Acceptance:

- `ResourceGovernor` provides admission control and process group management.
- `scripts/check_resource_bypass.py` fails on direct `subprocess.Popen`, `multiprocessing`, or solver CLI calls outside approved runner wrappers in provider code, except explicit allowlisted wrappers.

#### R-RSRC-002 — LocalResourceProfile

MUST: The implementation must provide a local resource probe and store a `LocalResourceProfile`.

Required fields:

```yaml
LocalResourceProfile:
  profile_id: "sha256:..."
  created_at: "..."
  os: "..."
  cpu_physical_cores: 0
  cpu_logical_cores: 0
  total_ram_mb: 0
  available_ram_mb_at_probe: 0
  gpu_devices:
    - name: "..."
      vram_total_mb: 0
      vram_available_mb_at_probe: 0
      backend: "cuda | metal | rocm | none | unknown"
  disk_free_mb:
    artifact_root: 0
    temp_root: 0
  lean_build_parallelism_default: 0
  provider_engine_availability:
    symbolic_closure: "available | unavailable | unknown"
    construction_proposer: "available | unavailable | unknown"
    heavy_search: "available | unavailable | unknown"
```

Acceptance:

- `scripts/probe_local_resources.py --json` emits this record.
- ResourceProfile hash is stored in `RunRecord`.

#### R-RSRC-003 — ResourceBudgetProfile

MUST: Budget profiles must be machine-relative, not hard-coded to one PC. Defaults must reserve system headroom.

Required budget names:

```text
tiny, small, medium, heavy, extreme
```

Default policy:

- Reserve at least 1–2 logical cores or 15% CPU capacity, whichever is larger, for OS, editor, Codex runtime, and Lean feedback.
- Reserve at least 20% RAM or 4 GB, whichever is larger, unless user overrides locally.
- Reserve at least 10% artifact/temp disk free space.
- Reserve GPU VRAM headroom when GPU-backed construction proposer is active.
- `extreme` may use most PC resources, but must still use admission control, process groups, kill policy, and periodic heartbeat.

Acceptance:

- `configs/resource/default_local.yaml` exists.
- `configs/resource/local.example.yaml` documents overrides.
- `ResourceGovernor` refuses a run if estimated minimum resources exceed configured safe limits, returning `resource_rejected` diagnostic.

#### R-RSRC-004 — Engine-role resource semaphores

MUST: Composite provider internal engines must use named semaphores, not ad hoc parallelism.

Required roles:

```yaml
engine_roles:
  symbolic_closure:
    intended_engine_family: "newclid_compatible"
    default_parallelism: "cpu_moderate"
  construction_proposer:
    intended_engine_family: "genesisgeo_compatible"
    default_parallelism: "gpu_or_cpu_guarded"
  heavy_search:
    intended_engine_family: "tonggeometry_compatible"
    default_parallelism: "exclusive_or_near_exclusive"
```

MUST: `heavy_search` is exclusive by default and may run only for `budget in {heavy, extreme}` or explicit policy escalation.

Acceptance:

- Simulated concurrent run test proves `heavy_search` does not run concurrently with another `heavy_search` unless config explicitly permits.
- Lean final verification queue is not starved by heavy provider runs.

#### R-RSRC-005 — Timeout, heartbeat, and kill policy

MUST: Every external engine run must have timeout, heartbeat, and process cleanup policy.

Required behavior:

1. Soft timeout writes partial logs and sends graceful termination.
2. Hard timeout kills process group.
3. Interrupted runs produce `DiagnosticBundle` and `ResourceUsageReport`.
4. Partial raw logs may be stored as artifacts but are not proof evidence.
5. Heavy search runs must checkpoint if the engine supports it; otherwise they must be safely restartable.

Acceptance:

- Timeout integration test kills a dummy long-running provider and verifies no orphan child process remains.
- ResourceUsageReport records wall time, peak RSS if available, CPU time if available, GPU memory if available, exit status, and timeout status.

#### R-RSRC-006 — Scheduler priorities

MUST: The scheduler must prioritize quick feedback and final verification over heavy search.

Default priority order:

1. FinalVerifyGate / Lean final theorem verification.
2. Lean build / Lean error summarization.
3. ProofWorker short repair tasks.
4. Newclid-compatible symbolic closure.
5. GenesisGeo-compatible construction proposer.
6. TongGeometry-compatible heavy search.
7. Maintenance / background cache refresh.

Acceptance:

- Scheduler test shows a queued Lean verification job can preempt or wait ahead of heavy search admissions.
- Heavy search cannot monopolize all worker slots.

---

### 4.7 ProofStateDAG requirements

#### R-DAG-001 — Minimal core node types

MUST: Base ProofStateDAG core node types remain `Obligation`, `Derivation`, and `EvidenceRef`.

MUST NOT: Add geometry-specific node types to Base.

Acceptance:

- Core DAG tests cover closure, acyclicity, invalidation, GraphPatch commit, and projection.
- No geometry-specific classes under `src/math_auto_research/proof_state/**`.

#### R-DAG-002 — GraphPatch-only mutation

MUST: Plugins cannot directly mutate DAG state. Plugins propose `GraphPatch`; Base `DAGWriter` validates and commits.

Acceptance:

- Mutation test fails if plugin writes DAG store directly.
- DAGWriter checks schema IDs, rule IDs, acyclicity, evidence validity, trust rules, and status-lattice transitions.

#### R-DAG-003 — Artifact separation

MUST: Raw solver logs, model transcripts, Lean files, trace files, and certificates are artifacts. DAG holds only refs, hashes, evidence status, and closure dependency.

Acceptance:

- Regression test rejects raw logs inserted as proof-use DAG nodes.

---

### 4.8 Lean and verification requirements

#### R-LEAN-001 — Protected theorem statement

MUST: The target theorem statement hash must be protected. ProofWorker may edit only admitted proof regions unless a task explicitly permits helper lemma additions.

Acceptance:

- Mutation test changes theorem statement and FinalVerifyGate rejects it.
- ProofRegionGuard rejects edits outside allowed proof blocks or helper lemma blocks.

#### R-VERIFY-001 — FinalVerifyGate authority

MUST: Only `FinalVerifyGate` may produce `result_level = final_theorem` or `proof_use_status = final_theorem`.

Required checks:

- Lean build succeeds for target.
- Protected theorem statement hash unchanged.
- No `sorry` in protected target and generated helper lemmas.
- No forbidden axioms or unsafe declarations according to configured policy.
- All generated proof imports are from admitted files.

Acceptance:

- Regression test: raw provider trace with “proved” does not become final theorem.
- Regression test: Lean file compiles with modified statement -> fails protected-hash check.

---

### 4.9 Geometry target and extraction requirements

#### R-GEO-001 — Single target library: LeanGeoSubsetV1

MUST: The initial target library is `LeanGeoSubsetV1` only.

MUST NOT: Add Mathlib geometry or a local geometry micro-library as a second target. Mathlib may be a dependency and LeanGeo shim lemmas may exist only as adapter support, not as a separate target.

Acceptance:

- `TargetLibraryManifest` contains exactly one target library.
- Release acceptance fails if a benchmark is satisfied only by local toy geometry definitions not mapped to LeanGeoSubsetV1.

#### R-GEO-002 — LeanGeoSubsetV1 theorem grammar

MUST: `LeanGeoSubsetV1` is defined as theorem grammar, not merely a predicate list.

Required grammar areas:

- Object declarations: points, lines from two distinct points, circles from registered constructors.
- Hypothesis forms: distinctness, collinearity, parallel, perpendicular, midpoint, concyclicity, equal length, equal angle where supported.
- Target forms: restricted collinearity, parallel, perpendicular, concyclicity, equal length, equal angle.
- Rejected forms: arbitrary Mathlib expression, unsupported local notation, unsupported quantifier alternation, unsupported orientation semantics, unsupported diagram case split.

Acceptance:

- Positive, negative, ambiguous, and safe-reject fixtures exist.
- Extractor tests cover every grammar entry.

#### R-EXTRACT-001 — Extraction-first proof-use path

MUST: Proof-use geometry solver path starts from Lean goal/context extraction.

Allowed proof-use path:

```text
Lean theorem / goal
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> geometry.solve
  -> GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> compiler
  -> Lean patch candidate
  -> ProofWorker
  -> FinalVerifyGate
```

Disallowed proof-use path:

```text
raw DSL problem -> solver -> proof-use artifact
```

Acceptance:

- Regression test: raw DSL problem run cannot produce `goal_level_allowed` or `final_theorem`.

#### R-EXTRACT-002 — Semantic extraction, not parser-only

MUST: Extractor must canonicalize Lean expressions into `GeometryClaimSpec` and classify relation to goal.

Required extraction work:

- Extract accepted predicates, objects, constructions, and relations.
- Remove or normalize implicit coercions, typeclasses, and local notation only within accepted grammar.
- Extract nondegeneracy, orientation, and diagram assumptions where supported.
- Classify target relation as `exact`, `sufficient`, `related`, or `none`.
- Safe-reject unsupported expressions.

Acceptance:

- Fixture tests cover local notation, coercion-like wrappers where applicable, missing nondegeneracy, unsupported angle semantics, and ambiguous targets.

---

### 4.10 Geometry solver provider requirements

#### R-SOLVER-001 — One Base-visible provider

MUST: Base sees exactly one selected `GeometrySolverProvider` per run.

MUST NOT: Base branches on Newclid / GenesisGeo / TongGeometry.

Acceptance:

- `RunRecord.SelectedImplementations.geometry_solver_provider` is scalar.
- Domain contamination test fails if Base references engine family names.

#### R-SOLVER-002 — Composite synthetic geometry provider roles

MUST: The selected provider may internally use three engine roles:

1. `symbolic_closure`: Newclid-compatible engine. Primary trace/closure engine.
2. `construction_proposer`: GenesisGeo-compatible engine. Auxiliary construction proposer.
3. `heavy_search`: TongGeometry-compatible engine. Heavy/extreme budget search oracle.

MUST: Internal engines communicate outward only through provider-normalized records: `GeoTraceV1`, `AuxiliaryConstructionCandidateV1`, `ProviderDiagnostic`, and `ProviderRunManifest`.

Acceptance:

- ProviderRunManifest records internal engine family, version, commit/checkpoint, config, seed, normalized output hashes, raw log hashes, and resource usage refs.

#### R-ENGINE-001 — Newclid-compatible symbolic closure role

MUST: Newclid-compatible engine is the first integration target and primary symbolic closure / trace candidate source.

Expected use:

- Convert `GeometryClaimSpec` to Newclid/JGEX-like input through provider adapter.
- Run symbolic closure / DDAR-style proof search where available.
- Normalize derived relations/proof steps to `GeoTraceV1`.
- Return unsupported rules as blockers, not proofs.

Acceptance:

- Newclid adapter smoke test returns either normalized `GeoTraceV1` or structured diagnostic for a known fixture.

#### R-ENGINE-002 — GenesisGeo-compatible construction proposer role

MUST: GenesisGeo-compatible engine output is treated as auxiliary construction proposal, not proof evidence.

Expected use:

- Trigger after symbolic closure fails or when solver policy requests construction proposals.
- Return `AuxiliaryConstructionCandidateV1` records.
- Allow ProofStateDAG obligations for side conditions generated by `ConstructionCompiler`.

Acceptance:

- Regression test: GenesisGeo raw construction rationale cannot close an obligation.

#### R-ENGINE-003 — TongGeometry-compatible heavy search role

MUST: TongGeometry-compatible engine is a heavy-search oracle, not a default proof-use backend.

Expected use:

- Run only for `budget = heavy | extreme` or explicit `GeometrySolverPolicy` escalation.
- Use exclusive or near-exclusive resource semaphore by default.
- Return construction candidates, proof-plan candidates, or normalized `GeoTraceV1` only if adapter can faithfully normalize supported subset.
- Raw TongGeometry trace is not proof evidence.

Acceptance:

- Resource policy test shows heavy search cannot start under `tiny/small/medium` unless policy explicitly escalates and logs reason.
- Trust regression test shows raw Tong output remains `diagnostic_only` or `search_only`.

#### R-SOLVER-003 — GeometrySolverPolicy

MUST: `GeometrySolverPolicy` is deterministic, versioned, hashed, logged, and resource-aware.

Default routing:

1. Try Newclid-compatible symbolic closure for supported `GeometryClaimSpec`.
2. If closure fails and constructions are useful, run GenesisGeo-compatible construction proposer under budget.
3. Re-run symbolic closure with admitted construction candidates when policy permits.
4. If budget is `heavy` or `extreme`, optionally run TongGeometry-compatible heavy search.
5. Return consolidated provider result with normalized artifacts and diagnostics.

Acceptance:

- ExecutionPlan records engine roles selected, budget, resource semaphores, timeouts, and reason codes.
- Policy hash changes when routing table or budget defaults change.

---

### 4.11 Compiler and auxiliary construction requirements

#### R-RULE-001 — RuleRegistryV1 with side-condition calculus

MUST: `RuleRegistryV1` is a target-library-specific registry for `LeanGeoSubsetV1`. It is not just a mapping from DSL rule names to Lean theorem names.

Each supported rule MUST specify:

- `rule_id` and version.
- Supported provider trace patterns.
- Lean lemma/template ID.
- Premise pattern.
- Conclusion pattern.
- Required side conditions.
- Generated obligations.
- Auto-discharge policy.
- Unsupported variants.
- Positive, negative, ambiguous fixtures.

Acceptance:

- `RuleRegistryV1` validation fails a rule missing side conditions or fixtures.
- Missing side conditions become obligations or blockers; never silent assumptions.

#### R-TRACE-001 — TraceCompiler scope

MUST: `TraceCompiler` compiles only supported `GeoTraceV1` rule subset to Lean patch candidates.

MUST NOT: Attempt arbitrary provider trace translation.

Acceptance:

- Unsupported rule returns blocker.
- Malformed trace is rejected fail-safe.
- Positive fixture compiles through Lean where dependencies are available.

#### R-AUX-001 — AuxiliaryConstructionCandidateV1

MUST: Auxiliary construction proposals are first-class typed artifacts, not natural-language suggestions.

Required fields:

```yaml
AuxiliaryConstructionCandidateV1:
  construction_id: "aux:<hash>"
  source_provider_result: "sha256:..."
  construction_kind: "intersection_of_two_nonparallel_lines | foot_of_perpendicular | midpoint | line_through_two_distinct_points | circle_with_center_through_point"
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

Acceptance:

- Natural-language auxiliary point rationale cannot become proof evidence.
- ConstructionCompiler generates Lean introduction patch or explicit blocker.

#### R-AUX-002 — ConstructionCompiler

MUST: `ConstructionCompiler` turns accepted auxiliary construction candidates into Lean introduction patch candidates and generated side-condition obligations.

Acceptance:

- Missing existence/nondegeneracy condition becomes ProofStateDAG obligation or blocker.
- Final proof-use requires Lean compile and FinalVerifyGate.

---

### 4.12 Trust, bridge, and run trace requirements

#### R-TRUST-001 — Raw output is never proof

MUST: Raw model output, raw provider output, raw Newclid/GenesisGeo/TongGeometry trace, raw DSL problem, raw coordinate proof, and raw analytical proof are never proof evidence.

Acceptance:

- TrustGuard tests cover every raw output kind.

#### R-TRUST-002 — Result levels

MUST: Geometry trust levels are the v0.3 trust classifications:

```text
diagnostic_only
extracted_claim
raw_provider_result
checked_trace
construction_candidate_checked
lean_patch_candidate
lean_compiled
final_theorem
```

Only `FinalVerifyGate` can emit `final_theorem`.

#### R-BRIDGE-001 — Geometry BridgeGate is lightweight but mandatory

MUST: Geometry BridgeGate verifies extraction origin, relation to Lean goal, protected theorem identity, and proof-use path provenance.

MUST NOT: Treat BridgeGate as a replacement for Lean final verification.

Acceptance:

- Raw DSL-originated run cannot pass goal-level proof-use.
- Extracted goal relation `related` or `none` cannot close target theorem.

#### R-RUN-001 — ProviderRunManifest

MUST: Each provider run emits `ProviderRunManifest` including internal engine choices and resource usage refs.

Acceptance:

- Manifest includes engine family, version/commit, config hash, checkpoint hash where relevant, seed, raw log hash, normalized artifact hashes, unsupported rule count, side condition loss count, and `ResourceUsageReport` refs.

#### R-RUN-002 — ControllerStrategyLog

MUST: Controller internals are not standardized, but lightweight attribution logging is required.

Required examples:

- controller ID and manifest hash.
- capability flags: single model, multi-agent, deep research, population search, rater, human hint.
- action counts: work orders, geometry solve requests, proof repair requests, construction requests.
- generated object counts.
- contribution refs.

Acceptance:

- Evaluation can distinguish controller-only vs geometry-enabled runs without core AgentC/D modes.

#### R-RUN-003 — ResourceUsageReport

MUST: Every admitted external process run emits `ResourceUsageReport`.

Required fields:

```yaml
ResourceUsageReport:
  report_id: "..."
  run_id: "..."
  component: "lean | proof_worker | model_slot | provider_engine | checker"
  engine_role: "none | symbolic_closure | construction_proposer | heavy_search"
  budget: "tiny | small | medium | heavy | extreme"
  admitted: true
  queue_wait_sec: 0
  wall_time_sec: 0
  cpu_time_sec: 0
  peak_rss_mb: 0
  gpu_vram_peak_mb: null
  exit_status: "success | failed | timeout_soft | timeout_hard | killed | resource_rejected"
  logs_ref: "sha256:..."
```

---

### 4.13 Evaluation and release requirements

#### R-EVAL-001 — Level 2 target

MUST: The initial evaluation target is Level 2 domain-tool advantage for Lean-verified geometry proof completion.

Compare at minimum:

- `B0`: ProofWorker-only.
- `B1`: ResearchController + ProofWorker, no `geometry.solve`.
- `B2`: Full geometry-enabled pipeline.
- `B3`: Strong-model without `geometry.solve`.
- `B4`: Lower-model + `geometry.solve`.
- `B5`: Full provider with auxiliary construction disabled, for construction contribution diagnosis.

Acceptance:

- Evaluation harness records final theorem rate, proof repair success, auxiliary construction accepted count, trace compile success, side-condition blocker count, and resource usage.

#### R-TEST-001 — Required regression families

MUST: Test suite include:

1. Domain contamination tests.
2. No loose options tests.
3. Dependency substitution tests.
4. Resource bypass and timeout tests.
5. Extraction mutation tests.
6. RuleRegistry / TraceCompiler mutation tests.
7. AuxiliaryConstruction / ConstructionCompiler mutation tests.
8. Controller observability / non-proof-use tests.
9. FinalVerifyGate misuse tests.
10. Provider raw-output laundering tests.

Acceptance:

- `make test-regression` and `make test-mutation` run these families.

#### R-CLAIM-001 — Allowed claims

Allowed closure claims after evidence:

- “Schemas and contracts implemented.”
- “Dependency bootstrap attempted / resolved with report.”
- “ResourceGovernor enforced process admission for tested providers.”
- “LeanGeoSubsetV1 extraction fixtures pass.”
- “A specific Lean theorem fixture passed FinalVerifyGate.”
- “In this benchmark matrix, geometry-enabled pipeline improved metric X over baseline Y.”

Disallowed claims without separate evidence and audit:

- “The pipeline solves open problems.”
- “The pipeline handles all LeanGeo / Mathlib geometry.”
- “Newclid / GenesisGeo / TongGeometry traces are trusted proofs.”
- “Resource settings are optimal for all PCs.”

---

### 4.14 v0.3 source-fidelity overlay requirements

These R-IDs prevent the implementation from satisfying only the summarized requirements above while missing detailed v0.3 contract fields, workflows, blockers, or repository construction areas. They are exact requirements from `geometry_lean_pipeline_plan_v0_3.md` unless explicitly marked as local execution extension.

#### R-V03-DOC-001 — v0.3 repository documentation anatomy

MUST: The repository documentation target from v0.3 must be represented, not only this Guardian change packet.

Required architecture documents:

- `docs/architecture/geometry_lean_pipeline.md`
- `docs/architecture/target_subset_contract.md`
- `docs/architecture/compiler_contract.md`
- `docs/architecture/run_trace_contract.md`
- `docs/architecture/trust_model_geometry.md`
- `docs/architecture/proof_state_dag.md`
- `docs/architecture/no_loose_options.md`

Required decision records:

- `DR-GEO-001-target-leangeo-subset.md`
- `DR-GEO-002-no-agent-cd-core.md`
- `DR-GEO-003-extraction-first.md`
- `DR-GEO-004-geotrace-not-proof.md`
- `DR-GEO-005-aux-construction-contract.md`
- `DR-GEO-006-run-attribution-logs.md`

Acceptance:

- Release acceptance checks that these documents exist or that a generated documentation index maps each v0.3 document/DR to its current location.
- These documents must not redefine requirements in conflict with this Base Spec.

#### R-V03-SCHEMA-001 — Exact v0.3 public contract schema coverage

MUST: The implementation must provide schema-backed, versioned records for every v0.3 public contract, with the fields and allowed values specified in the v0.3 source plan unless a later admitted Base Spec explicitly changes them.

Required v0.3 schema families:

- Base/runtime: `RunRecord`, `ArtifactRef`, `TrustReport`, `DiagnosticBundle`, `PluginManifest`, `SelectedImplementations`, `FinalVerifyReport`, `ResearchContributionRecord`.
- ProofStateDAG: `Obligation`, `Derivation`, `EvidenceRef`, `GraphPatch`, `GraphPatchCommitResult`, DAG closure status and blocker summaries.
- Model API: `ResearchControllerPlugin`, `ProofWorkerPlugin`, `ResearchStatePack`, `WorkerStatePack`, `ActionPlan`, `WorkOrder`, `WorkerResult`, `ControllerStrategyLog`.
- Target subset/extraction: `LeanGeoSubsetV1TheoremGrammar`, `GrammarFixtureSet`, `PredicateMapping`, `ConstructionMapping`, `RelationMapping`, `GeometryExtractionContract`, `GeometryExtractionReport`, `GeometryClaimSpec`.
- Solver provider: `GeometrySolverProvider`, `GeometrySolveRequest`, `GeometrySolverPolicy`, `GeometryExecutionPlan`, `ProviderRunManifest`, `ProviderResult`.
- Compiler/construction: `GeoTraceV1`, `TraceCheckerResult`, `GeometryRuleContract`, `SideConditionReport`, `TraceCompilationResult`, `AuxiliaryConstructionCandidateV1`, `ConstructionCheckResult`, `ConstructionCompilationResult`.
- Bridge/trust: `GeometryBridgeReport` and v0.3 trust-level classifications.
- Evaluation/replay: `EvaluationFunnel`, `ReproducibilityReport`, metrics report, benchmark run matrix records.

Acceptance:

- Schema validation tests fail if a required v0.3 field, enum value, provenance ref, status field, or proof-use note is missing.
- Schema validation tests fail if extra proof-use status values create a path not allowed by v0.3.
- `schemas/model_api/**` is the v0.3 model schema location. Compatibility aliases may exist, but they must point to the same schemas rather than creating a second model contract.

#### R-V03-TARGET-001 — Exact TargetSubsetContract details

MUST: `TargetSubsetContract` must include the exact v0.3 components and safe-reject semantics:

1. `LeanGeoSubsetV1TheoremGrammar`.
2. Predicate, construction, and relation mappings.
3. `GeometryExtractionContract`.
4. `GeometryExtractionReport`.
5. `GeometryClaimSpec`.
6. Fixtures and safe-reject policy.

MUST: Grammar support must include v0.3 object declarations, allowed/conditional/rejected hypothesis forms, allowed/rejected target forms, positive/negative/ambiguous/mutation fixtures, mapping side conditions, and relation-to-goal proof-use policy.

MUST: `GeometryClaimSpec` cannot exist in a proof-use path without accepted `GeometryExtractionReport` provenance.

Acceptance:

- Fixture tests cover every v0.3 grammar entry and every v0.3 fixture category.
- `relation_to_goal = related | none` cannot close the target theorem.
- `sufficient` proceeds only when `direction_needed` and `direction_available` satisfy the v0.3 relation mapping.

#### R-V03-MODEL-001 — Exact model plugin contract details

MUST: `ResearchControllerPlugin` and `ProofWorkerPlugin` must expose only the v0.3 boundary contracts:

- Core sees `ResearchStatePack -> ActionPlan` for controller strategy.
- Core sees `WorkOrder -> WorkerResult` for proof editing/repair.
- Controller internals such as single strong model, smaller model, DeepResearch-style planning, multi-agent orchestration, population search, rater/evaluator loop, and human-guided strategy remain plugin internals.

MUST: `ActionPlan`, `WorkOrder`, and `WorkerResult` include the v0.3 fields, task kinds, constraints, escalation policies, artifacts, final verification references, and proof-use notes.

Acceptance:

- Regression tests prove controller rationale is diagnostic only.
- Regression tests prove `WorkerResult.status = success_claimed` cannot close a theorem without `FinalVerifyReport`.
- ProofWorker cannot edit the protected theorem statement, add `sorry`, add forbidden axioms, change LeanGeo definitions, or claim final success without `FinalVerifyReport`.

#### R-V03-RUN-001 — Exact run trace, contribution, and DAG/log separation

MUST: `ControllerStrategyLog`, `ResearchContributionRecord`, `RunRecord`, `EvaluationFunnel`, and `ReproducibilityReport` must include the v0.3 fields and allowed status values.

MUST: ProofStateDAG must not become a log database. An item belongs in ProofStateDAG only if removing it changes closure status, proof-use reachability, blocker visibility, cache invalidation, or final theorem contribution tracing.

Acceptance:

- Tests distinguish `used_in_search`, `used_in_final_proof`, `diagnostic_only`, `abandoned`, and `refuted_key_branch`.
- Every run records selected implementations and has no `mode A/B/C/D` field.
- Replay restores selected controller, worker, provider, solver policy, rule registry, trust boundary, artifacts, provider manifests, controller strategy logs, and final verification state where applicable.

#### R-V03-SOLVER-001 — Exact solver provider contract details

MUST: `GeometrySolveRequest`, `GeometrySolverPolicy`, `GeometryExecutionPlan`, `ProviderRunManifest`, and `ProviderResult` must include the v0.3 fields, intents, trust targets, budgets, constraints, reason codes, manifest internals, adapter versions, raw/normalized output hashes, unsupported rule count, and side-condition loss count.

MUST: Provider internals may include Newclid-compatible, GenesisGeo-compatible, TongGeometry-compatible, local search, auxiliary construction model, coordinate oracle for search hints, Wu/Groebner oracle for search hints, or custom internals, but core sees only one selected `GeometrySolverProvider`.

MUST: Coordinate, Wu, Groebner, analytic, or custom internals are search hints only unless normalized into v0.3 accepted artifacts and then Lean-verified.

Acceptance:

- `ProviderResult.proof_use_status` remains `not_allowed`.
- `trust_target = final_theorem` in a request cannot authorize final proof-use promotion.
- Provider-specific names do not appear in Base control flow.

#### R-V03-COMPILER-001 — Exact CompilerContract and RuleRegistry details

MUST: `CompilerContract` must include v0.3 `GeoTraceV1`, `RuleRegistryV1`, `SideConditionReport`, `TraceCompiler`, `AuxiliaryConstructionCandidateV1`, `ConstructionCompiler`, and mutation tests.

MUST: `GeoTraceV1`, `TraceCheckerResult`, `GeometryRuleContract`, `SideConditionReport`, and `TraceCompilationResult` must include the v0.3 fields and allowed statuses.

MUST: Initial supported rule families are narrow and explicit: collinearity propagation, parallel/perpendicular transfer, midpoint basic consequences, concyclicity basic consequences, equal length transfer from midpoint/circle constructors, angle transfer for registered parallel/cyclic patterns, and construction-introduction rules for supported auxiliary constructions.

Acceptance:

- Supported rules require Lean lemma/template, premise pattern, conclusion pattern, required side conditions, generated obligations, unsupported variants, and positive/negative/ambiguous fixtures.
- Release blockers from v0.3 RuleRegistry section are machine-checkable.
- Trace schema validity is never treated as proof.

#### R-V03-AUX-001 — Exact auxiliary construction contract details

MUST: v0.3 proof-use auxiliary construction kinds are exactly:

- `line_through_two_distinct_points`
- `intersection_of_two_nonparallel_lines`
- `foot_of_perpendicular`
- `midpoint`
- `circle_with_center_through_point`

MUST NOT: `plugin_supported`, arbitrary free points, arbitrary point-on-line/circle with relation, general line-circle intersection, or general two-circle intersection enter proof-use path in v0.3.

MUST: `AuxiliaryConstructionCandidateV1`, `ConstructionCheckResult`, and `ConstructionCompilationResult` must include the v0.3 fields, including source provenance, introduced objects, dependencies, intended use, side conditions, introduction plan, generated obligations, blockers, and proof-use status.

Acceptance:

- Unsupported construction kinds may be diagnostic/research hints only.
- Construction rationale cannot become proof evidence.
- Construction introduction cannot change the protected theorem statement.
- Generated side-condition obligations are tracked.

#### R-V03-DAG-001 — Exact ProofStateDAG integration and closure rule

MUST: Geometry integration must use only the Base core node types `Obligation`, `Derivation`, and `EvidenceRef`.

MUST: The v0.3 GraphPatch examples are normative patterns for extraction accepted, trace compiled with missing side condition, auxiliary construction introduced, and Lean final proof succeeds.

MUST: A target theorem obligation is closed iff there exists a proof-use derivation with `proof_use_status = final_theorem`, all required side-condition obligations are closed, `FinalVerifyReport` is valid, and the protected theorem statement hash is unchanged.

Acceptance:

- ProviderResult, GeoTraceV1, construction candidates, controller rationale, and worker success claims cannot close target theorem obligations.
- DAGWriter enforces GraphPatch-only mutation and closure rule.

#### R-V03-TRUST-001 — Exact BridgeGate and trust-level details

MUST: GeometryBridgeGate must check exactly the v0.3 proof-use provenance concerns: accepted extraction origin, exact/sufficient relation in the required direction, target library `LeanGeoSubsetV1`, generated patch target, no raw DSL origin, and protected theorem statement hash.

MUST: `GeometryBridgeReport` must include the v0.3 target goal, source claim, relation-to-goal, semantic status, `proof_use_at_goal_level`, and `missing_links` fields.

MUST: The trust classifications are the v0.3 levels:

```text
diagnostic_only
extracted_claim
raw_provider_result
checked_trace
construction_candidate_checked
lean_patch_candidate
lean_compiled
final_theorem
```

Acceptance:

- Only `final_theorem` from `FinalVerifyGate` may close a target theorem.
- Compatibility aliases must be report-only and must not create a second proof-use status lattice.

#### R-V03-WORKFLOW-001 — Exact v0.3 standard proof loop and workflows

MUST: The implementation must follow the v0.3 20-step standard proof loop from LeanPort compile through GoalAnchor, ProofStateDAG, controller ActionPlan, extraction, solver policy, provider, checker/compiler, ProofWorker, LeanPort, FinalVerifyGate, DAGWriter, RunLogger, and StateReader update.

MUST: The implementation must support the v0.3 workflows for auxiliary construction, proof trace, proof repair, unsupported trace, and discovery/research artifacts.

Acceptance:

- Integration tests or replay fixtures show each standard loop stage either produces the required artifact or a structured blocker.
- Unsupported trace is never partial proof.
- Discovery artifacts remain unverified hints unless formalized through WorkOrder, GeometrySolveRequest, or DAG obligation and ultimately Lean-verified.

#### R-V03-EVAL-001 — Exact evaluation, metrics, and replay requirements

MUST: Evaluation must target Level 2 domain-tool advantage only, not open-problem solving.

MUST: The benchmark pool is fixed before extraction to prevent cherry-picking.

MUST: Baselines `B0` through `B5`, `EvaluationFunnel` counts/rejection breakdown, proof metrics, auxiliary construction metrics, controller reasoning metrics, provider metrics, resource metrics, and `ReproducibilityReport` fields match v0.3.

Acceptance:

- Evaluation reports distinguish model-only, worker-only, controller-only, geometry-enabled, lower-model plus geometry, and construction-disabled ablation runs as evaluation configurations, not runtime core modes.
- Claims state accepted/rejected/supported/final-success counts, not just final wins.

#### R-V03-TEST-001 — Exact v0.3 mutation, release-blocker, and final checklist coverage

MUST: Regression, mutation, and release acceptance checks must cover every item listed in v0.3 sections 22, 23, and 28.

Required coverage includes:

- Extraction mutation tests.
- RuleRegistry / TraceCompiler mutation tests.
- AuxiliaryConstruction / ConstructionCompiler mutation tests.
- Controller observability tests.
- Final verification misuse tests.
- Option creep regression tests.
- Release blockers for target/extraction, model/controller, solver provider, compiler, trust/final verification, evaluation/replay.
- Final release acceptance checklist for TargetSubsetContract, model boundaries, solver provider, CompilerContract, ProofState/Trust, and Evaluation/replay.

Acceptance:

- `check_release_acceptance.py` fails if any v0.3 checklist item lacks an implemented check, explicit waiver, or blocked status with evidence.

#### R-V03-EXT-001 — Local execution extensions must not change v0.3 semantics

MUST: `R-ENV-*`, `R-RSRC-*`, and Base-level `ModelProviderSet` requirements are local execution / reproducibility / dependency-governance extensions inherited from the prepared drafts and user decisions. They may constrain how v0.3 is implemented, but they must not widen, weaken, or replace the v0.3 mathematical pipeline semantics.

MUST: If an extension conflicts with exact v0.3 requirements, Codex must stop and request a Base Spec revision rather than silently choosing the extension.

Acceptance:

- Source map labels these items as local execution extensions where applicable.
- Release closure distinguishes v0.3 functional requirements from local execution extensions.
- No local execution extension can authorize a second target library, raw DSL proof-use path, core AgentC/D mode, provider-specific proof semantics, or bypass of FinalVerifyGate.

---

## 5. Mechanisms

### MECH-BOOT-001 — Dependency bootstrap mechanism

```text
inspect repo
  -> probe system and toolchain
  -> add/pin Lean/lake dependencies
  -> add/pin Python/provider dependencies
  -> install or configure Newclid-compatible engine
  -> install or configure GenesisGeo-compatible engine/checkpoint if available
  -> install or configure TongGeometry-compatible engine if available
  -> run smoke commands
  -> emit DependencyResolutionReport
  -> mark unavailable components as blocked, not silently substituted
```

### MECH-MODEL-001 — Model injection mechanism

```text
RunConfig
  -> SelectedImplementations.model_provider_set
  -> ModelProviderSetManifest
  -> ModelSlot resolution
  -> ResearchControllerPlugin receives slot handles
  -> ProofWorkerPlugin receives slot handles
  -> model outputs become ActionPlan / WorkOrder / diagnostics
  -> no model output becomes proof evidence
```

### MECH-RSRC-001 — Local resource governance mechanism

```text
LocalResourceProfile
  -> ResourceBudgetProfile
  -> ResourceGovernor admission
  -> per-role semaphore acquisition
  -> process group runner
  -> heartbeat monitor
  -> timeout / kill policy
  -> ResourceUsageReport
  -> ProviderRunManifest / RunRecord linkage
```

### MECH-SOLVER-001 — Composite provider mechanism

```text
GeometryClaimSpec
  -> GeometrySolverPolicy
  -> GeometryExecutionPlan
  -> symbolic_closure / Newclid-compatible attempt
  -> if needed: construction_proposer / GenesisGeo-compatible candidates
  -> symbolic_closure retry with admitted candidate when policy permits
  -> if budget permits: heavy_search / TongGeometry-compatible oracle
  -> normalize to GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> ProviderResult + ProviderRunManifest
```

### MECH-PROOF-001 — Verified proof path

```text
Lean theorem / goal
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> geometry.solve
  -> GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> RuleRegistryV1 / TraceCompiler or ConstructionCompiler
  -> Lean patch candidate
  -> ProofWorkerPlugin
  -> LeanPort
  -> FinalVerifyGate
  -> final_theorem
```

---

## 6. Release blockers

Release acceptance MUST fail if any of the following occurs:

1. Base imports or branches on geometry-specific concepts.
2. AgentC/D core runtime modes exist.
3. Target library is not exactly `LeanGeoSubsetV1`.
4. Real final theorem support is claimed without resolved LeanGeo-compatible dependency.
5. Models are hard-coded into controller/worker plugins rather than injected through `ModelProviderSet`.
6. Provider-specific engine names appear in Base logic.
7. External provider process runs outside `ResourceGovernor`.
8. Heavy search can starve Lean final verification or run without budget admission.
9. Raw provider/model output can close an obligation.
10. Raw DSL-originated problem can produce goal-level proof-use.
11. RuleRegistry supports a rule without side-condition calculus.
12. Missing side condition is silently assumed.
13. Protected theorem statement can be changed while still passing final verification.
14. ProviderRunManifest, ResourceUsageReport, or DependencyResolutionReport is missing for runs that require them.
15. Closure claims are not backed by fresh evidence.
16. Any `R-V03-*` detailed source-fidelity requirement is missing, waived without evidence, or contradicted.
17. v0.3 public contract schemas omit required fields, provenance refs, status values, fixtures, or proof-use notes.
18. v0.3 repository documentation and decision-record anatomy is absent without an index mapping to equivalent files.
19. Evaluation/replay cannot report accepted/rejected/supported/final-success funnel counts.
20. A local execution extension changes v0.3 semantics instead of stopping for Base Spec revision.

---

## 7. Expected final repository additions

The v0.3 repository target anatomy in `geometry_lean_pipeline_plan_v0_3.md` is the source-fidelity target for final implementation. The tree below records the Guardian/local-execution additions that may coexist with that anatomy. If paths differ, implementation must either use the v0.3 path or provide an index mapping the v0.3 path to the actual path without creating a second contract.

```text
docs/
  architecture/
    geometry_lean_pipeline.md
    target_subset_contract.md
    compiler_contract.md
    run_trace_contract.md
    trust_model_geometry.md
    proof_state_dag.md
    no_loose_options.md
  decision_records/
    DR-GEO-001-target-leangeo-subset.md
    DR-GEO-002-no-agent-cd-core.md
    DR-GEO-003-extraction-first.md
    DR-GEO-004-geotrace-not-proof.md
    DR-GEO-005-aux-construction-contract.md
    DR-GEO-006-run-attribution-logs.md

src/math_auto_research/
  base/
    artifacts/
    logging/
    model_provider_set.py
    resources/
      local_resource_profile.py
      resource_budget.py
      resource_governor.py
      process_runner.py
    trust/
    registry/
  proof_state/
    dag_core.py
    graph_patch.py
    dag_writer.py
    closure_engine.py
    state_reader.py
    blocker_summarizer.py
  model_api/
    research_controller.py
    proof_worker.py
    action_plan.py
    work_order.py
    state_packs.py
    controller_strategy_log.py
  lean_integration/
  plugin_api/
  workflow/
  evaluation/

plugins/geometry_synthetic/
  plugin.yaml
  target_subset/
  extraction/
  solver_provider/
  solver_policy/
  providers/
    composite_provider.py
    newclid_adapter.py
    genesisgeo_adapter.py
    tonggeometry_adapter.py
  compiler/
    geotrace.py
    rule_registry.py
    trace_compiler.py
    construction_candidate.py
    construction_compiler.py
  bridge/
  renderers/
  tests/
  tests/

lean/MathAutoResearch/Geometry/
  LeanGeoSubset.lean
  Bridge.lean
  Generated/

schemas/
  base/
  model_api/
  resources/
  proof_state/
  geometry/
  evaluation/

configs/
  selected_implementations/geometry_default.yaml
  resource/default_local.yaml
  resource/local.example.yaml
  solver_policies/geometry_synthetic_v1.yaml
  model_provider_sets/default.example.yaml
  benchmark_runs/geometry_level2_smoke.yaml
  benchmark_runs/geometry_level2_ablation.yaml

scripts/
  bootstrap_env.sh
  probe_local_resources.py
  check_no_loose_options.py
  check_domain_contamination.py
  check_resource_bypass.py
  check_release_acceptance.py
  run_geometry_level2_matrix.py
  generate_repro_report.py
```
