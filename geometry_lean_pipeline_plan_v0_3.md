---
title: 数学自動研究 pipeline — geometry × Lean 初期対象計画
version: v0.3-geometry-lean-research-verified
created: 2026-06-09
status: draft; v0.2 と revised review を踏まえた再整理版
intended_reader:
  - 実装者
  - 研究計画レビュー担当者
  - model / solver / Lean integration / geometry plugin 設計者
  - repository architecture 設計者
based_on:
  - geometry_lean_pipeline_plan_v0_2.md
  - geometry_lean_pipeline_review_v0_2_revised.md
  - fatal_risks_1_2_3_geometry_lean_review.md
  - math_auto_research_pipeline_final_repo_plan_v1_2.md
main_decisions:
  - Agent C/D taxonomy は core architecture から削除する
  - target library は LeanGeoSubsetV1 に固定する
  - proof-use 経路は Lean goal extraction から始める
  - raw DSL problem / raw solver trace は proof evidence ではない
  - 補助点生成を標準 contract として扱う
  - RuleRegistryV1 は side-condition calculus を持つ
  - Controller / provider の探索寄与は lightweight log で測定する
  - optional runtime mode を増やさず、狭い plugin boundary だけを残す
---

# 数学自動研究 pipeline — geometry × Lean 初期対象計画 v0.3

## 0. この文書の目的

この文書は、数学自動研究 pipeline の初期対象を **geometry × Lean** に置く場合の、最終的に目指すべき architecture / contract / repository target / release acceptance を定義する。

v0.2 では、初期 target を `LeanGeoSubsetV1` に固定し、Agent C/D taxonomy を core から削除し、`ResearchControllerPlugin` / `ProofWorkerPlugin` / `GeometrySolverProvider` という狭い plugin boundary に整理した。これは正しい方向である。

ただし、その後の review により、v0.2 には次の弱点が残っていた。

```text
1. LeanGeoSubsetV1 が predicate list 寄りで、theorem grammar と fixture による境界定義が不足していた。
2. 補助点生成は ProviderResult に入っていたが、AuxiliaryConstructionCandidate の proof 化 contract が弱かった。
3. RuleRegistry / TraceCompiler の supported rule subset と side-condition calculus がまだ抽象的だった。
4. ResearchControllerPlugin と GeometrySolverProvider の探索寄与を測る logging が弱かった。
5. Provider abstraction は安全境界として正しいが、reproducibility のための ProviderRunManifest が不足していた。
```

v0.3 は、これらを **optional component の追加**ではなく、次の 3 つの標準 contract bundle に圧縮して取り込む。

```text
A. TargetSubsetContract
   LeanGeoSubsetV1TheoremGrammar、GeometryExtractionContract、fixtures、safe reject policy。

B. CompilerContract
   GeoTraceV1、RuleRegistryV1、AuxiliaryConstructionCandidateV1、TraceCompiler、ConstructionCompiler、side-condition calculus。

C. RunTraceContract
   ProviderRunManifest、ControllerStrategyLog、ResearchContributionRecord、EvaluationFunnel。
```

この文書は実装順や MVP を定義するものではない。v1.2 と同様、最終的に repository が満たすべき構造・contract・release acceptance を定義する。ただし、v1.2 の finite_graph 初期対象を、ここでは **geometry × Lean / synthetic geometry solver / LeanGeoSubsetV1** に置き換える。

---

## 1. v0.3 の一文要約

```text
LeanGeoSubsetV1 により正しく定式化済みの幾何 theorem を入力とし、
ResearchControllerPlugin が証明方針・補題候補・補助構成要求・作業指示を出し、
ProofWorkerPlugin が Lean proof edit / repair を行い、
GeometrySolverProvider が Newclid / GenesisGeo / TongGeometry 系 solver や guided search を内部利用して
GeoTraceV1 / AuxiliaryConstructionCandidateV1 / Diagnostic を返し、
GeometryExtractionContract、RuleRegistryV1 side-condition calculus、TraceCompiler、ConstructionCompiler、FinalVerifyGate を通して、
theorem statement hash unchanged の Lean theorem を生成する verified geometry research pipeline である。
```

v0.3 の最重要点は次である。

```text
1. 本 pipeline は Lean proof closing だけを目的にしない。
   LLM controller の数学的考察、補題候補、補助点要求、proof repair 方針も研究 artifact として扱う。

2. ただし、探索 artifact はそのまま proof evidence ではない。
   proof-use は Lean goal extraction、GeoTraceV1 / AuxiliaryConstructionCandidateV1、RuleRegistryV1、Compiler、Lean final verification を通ったものだけに限る。

3. Agent C/D taxonomy は復活させない。
   multi-agent、DeepResearch-style planning、population search、rater は ResearchControllerPlugin 内部実装として許すが、core mode にはしない。

4. Newclid / GenesisGeo / TongGeometry は core option ではない。
   core は GeometrySolverProvider だけを知る。provider 内部は差し替え可能だが、core semantics は GeoTraceV1 / AuxiliaryConstructionCandidateV1 に固定する。

5. optional を増やさない。
   各 run では target library、controller、worker、provider、solver policy、trust boundary を exactly one selected implementation として記録する。
```

---

## 2. v0.2 からの主要変更

| v0.2 | v0.3 |
|---|---|
| LeanGeoSubsetV1 を accepted expression subset として定義 | **LeanGeoSubsetV1TheoremGrammar + fixtures** として定義 |
| ProviderResult に construction candidates を含める | **AuxiliaryConstructionCandidateV1 + ConstructionCompiler** を標準 contract に昇格 |
| RuleRegistry は side-condition calculus を持つと記述 | **RuleRegistryV1 の supported rule contract / fixture / mutation tests** を明示 |
| Controller は opaque plugin | core からは opaque のまま、**ControllerStrategyLog** で lightweight attribution を記録 |
| Provider は singular boundary | singular boundary は維持し、**ProviderRunManifest** で internals / seed / checkpoint / normalizer を記録 |
| Level 2 domain-tool advantage | **EvaluationFunnel** と contribution metrics を追加して cherry-pick と過剰主張を防ぐ |
| BridgeGate / TraceCompiler / ConstructionCompiler の役割がやや混在 | geometry 版では **BridgeGate を軽量化し、CompilerContract と FinalVerifyGate を重くする** |
| baseline は最低限 | runtime option は増やさず、**evaluation config として最小 baseline matrix** を定義 |

---

## 3. Scope

### 3.1 初期対象

```text
Input:
  LeanGeoSubsetV1 により正しく定式化済みの Euclidean geometry theorem。

Goal:
  target theorem statement を変更せず、sorry-free / forbidden-axiom-free の Lean proof を生成する。

Solver source:
  Newclid / GenesisGeo / TongGeometry 系の synthetic geometry solver、guided search、auxiliary construction generator。

Main result:
  FinalVerifyGate を通った Lean theorem。

Initial evaluation claim:
  未解決問題解決ではなく、Level 2 domain-tool advantage。
```

### 3.2 Pipeline が責任を持つもの

```text
- Lean formal theorem の proof search / proof repair / final verification。
- Lean goal から GeometryClaimSpec への sound subset extraction。
- solver trace / construction candidate を Lean proof candidate に変換する deterministic compiler。
- side condition / nondegeneracy / orientation / construction existence の obligation 化。
- raw provider result と proof evidence の分離。
- theorem statement hash unchanged / no sorry / no forbidden axioms の確認。
- controller / worker / provider / construction / trace の寄与記録。
```

### 3.3 Pipeline が責任を持たないもの

```text
- 自然言語問題から Lean theorem を作ること。
- informal problem と Lean theorem の忠実性保証。
- diagram image recognition。
- 任意の geometry DSL trace の Lean 化。
- LeanGeo / Mathlib / local library の multi-target bridge。
- AlphaGeometry / TongGeometry と同じ土俵の solve-rate 競争。
- 座標法 / Wu / Groebner / SOS を主表現にした幾何証明。
```

### 3.4 Claim scope

```yaml
ResearchClaimScope:
  formal_artifact_claim:
    statement: "This Lean theorem was proved."
    authority: "FinalVerifyGate / Lean kernel"
    pipeline_core_responsibility: true

  original_problem_claim:
    statement: "The original informal geometry problem was solved."
    authority: "external human audit"
    pipeline_core_responsibility: false
    required_metadata:
      - original_problem_ref
      - formal_theorem_ref
      - audit_status
```

---

## 4. Non-negotiable design invariants

### 4.1 No loose options invariant

```text
Core runtime must not accumulate optional modes.
```

Allowed replacement:

```text
- Replace selected ResearchControllerPlugin.
- Replace selected ProofWorkerPlugin.
- Replace selected GeometrySolverProvider.
- Replace selected model inside a plugin.
- Replace provider internals while preserving output contract.
```

Disallowed optionality:

```text
- AgentC / AgentD core modes.
- Multiple core agent modes.
- Multiple bridge target libraries in one release target.
- Mathlib geometry as parallel target.
- local micro-library as parallel target.
- Provider-specific proof semantics in core.
- TraceCompiler variants selected by controller.
- TrustGuard bypass flags.
- raw DSL problem proof-use path.
```

### 4.2 Exactly-one-selected invariant

Each run records exactly one selected implementation for each boundary.

```yaml
SelectedImplementations:
  target_library: "LeanGeoSubsetV1"
  research_controller_plugin: "research_controller:<id>:<version>"
  proof_worker_plugin: "proof_worker:<id>:<version>"
  geometry_solver_provider: "geometry_solver_provider:<id>:<version>"
  solver_policy: "geometry_solver_policy:<id>:<version>"
  rule_registry: "RuleRegistryV1:<version>"
  trust_boundary: "strict_lean"
```

This is not an optional-mode system. It is a single runtime with replaceable implementations behind narrow contracts.

### 4.3 Lean theorem immutability invariant

```text
Protected theorem statement hash is immutable during a proof run.
```

Allowed edits:

```text
- proof body in allowed region
- local helper lemmas in allowed region
- generated proof files
- namespace-local bridge lemmas if explicitly allowed by WorkOrder
```

Disallowed edits:

```text
- target theorem statement
- target theorem assumptions
- LeanGeo predicate definitions
- adding axioms
- using sorry
- weakening the target
- replacing the target with an easier theorem
```

### 4.4 LeanGeoSubsetV1 fixed target invariant

```text
Full v0.3 target library is exactly LeanGeoSubsetV1.
Mathlib is dependency only.
Local geometry library is fixture / shim only.
```

### 4.5 Extraction-before-solver invariant

Proof-use geometry solving must start from Lean goal extraction.

```text
Lean goal
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> GeometrySolverProvider
```

This path is not proof-use eligible:

```text
raw DSL problem
  -> solver
  -> trace
  -> proof claim
```

Direct DSL input may be stored as debug / exploration artifact, but cannot close a ProofStateDAG obligation.

### 4.6 Raw trace is not proof invariant

```text
ProviderResult, raw solver log, raw DSL trace, controller rationale, worker success claim are not proof evidence.
```

Only this path can close a Lean goal:

```text
Lean patch / proof candidate
  -> Lean compile
  -> no sorry
  -> no forbidden axioms
  -> theorem statement hash unchanged
  -> FinalVerifyGate passed
```

### 4.7 Search oracle separation invariant

Provider internals may use coordinate / Wu / analytic / neural / guided-tree-search methods as search oracles.

```text
Allowed:
  Use coordinate / Wu / analytic methods to propose construction candidates, lemma candidates, trace hints, diagnostics.

Disallowed:
  Treat coordinate / Wu / analytic proof as LeanGeo proof evidence unless it is compiled and verified through the standard Lean path.
```

---

## 5. Top-level architecture

```text
Layer 1: Model plugin layer
  ResearchControllerPlugin, ProofWorkerPlugin.
  Models, DeepResearch-style planning, multi-agent orchestration, population search, rater are plugin internals.

Layer 2: Base runtime
  Scheduler, ArtifactStore, RunLogger, TrustGuard, DiagnosticBundle, plugin manifests, replay.

Layer 2.5: ProofStateDAG core
  Obligation, Derivation, EvidenceRef, GraphPatch, DAGWriter, closure engine, StateReader.

Layer 3: Geometry domain plugin facade
  geometry.solve, GeometryExtractionContract, GeometryClaimSpec, GeometrySolverProvider boundary.

Layer 4: TargetSubsetContract
  LeanGeoSubsetV1TheoremGrammar, mappings, fixtures, safe reject policy.

Layer 5: CompilerContract
  GeoTraceV1, RuleRegistryV1, AuxiliaryConstructionCandidateV1, TraceCompiler, ConstructionCompiler.

Layer 6: Lean integration
  LeanPort, GoalAnchor, ProofWorker editing boundary, FinalVerifyGate.

Layer 7: RunTrace and evaluation
  ProviderRunManifest, ControllerStrategyLog, ResearchContributionRecord, EvaluationFunnel, replay reports.
```

### 5.1 Base knows

```text
RunRecord
ArtifactRef
TrustReport
DiagnosticBundle
PluginManifest
SelectedImplementations
Obligation / Derivation / EvidenceRef
GraphPatch
FinalVerifyReport
ResearchContributionRecord
```

### 5.2 Base does not know

```text
Newclid internals
GenesisGeo internals
TongGeometry internals
specific GPT / Codex / local model APIs
geometry rule semantics beyond registered RuleRegistry contracts
LeanGeo theorem internals beyond target subset schemas
coordinate / Wu / analytic proof internals
```

---

## 6. Repository target anatomy

```text
math-auto-research/
  docs/
    architecture/
      geometry_lean_pipeline_plan_v0_3.md
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
      trust/
      diagnostics/
      registry/
      scheduler/
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
      lean_port.py
      goal_anchor.py
      final_verify_gate.py
      proof_region_guard.py
      lean_error_summarizer.py
    workflow/
      standard_geometry_loop.py
      replay.py
      release_acceptance.py
    evaluation/
      benchmark_funnel.py
      baselines.py
      metrics.py
      reproducibility_report.py

  plugins/
    geometry_synthetic/
      plugin.yaml
      README.md
      target_subset/
        leangeo_subset_v1.yaml
        theorem_grammar.py
        fixtures/
      extraction/
        geometry_extraction_contract.py
        extraction_report.py
        claim_spec.py
        predicate_mapping.yaml
        construction_mapping.yaml
        relation_mapping.yaml
      solver_provider/
        provider_api.py
        provider_manifest.py
        provider_run_manifest.py
        execution_plan.py
        solver_policy.py
      trace/
        geotrace_v1.py
        trace_checker.py
        rule_registry_v1.yaml
        side_condition_calculus.py
        trace_compiler.py
      construction/
        auxiliary_construction_candidate_v1.py
        construction_checker.py
        construction_compiler.py
      bridge/
        geometry_bridge_report.py
        relation_to_goal.py
      renderers/
        research_state_renderer.py
        worker_state_renderer.py
      tests/
        fixtures/
        test_extraction.py
        test_rule_registry.py
        test_trace_compiler.py
        test_construction_compiler.py
        test_option_creep.py

  lean/
    MathAutoResearch/
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
    model_api/
    geometry/
      leangeo_subset_grammar.schema.json
      extraction_report.schema.json
      geometry_claim_spec.schema.json
      geotrace_v1.schema.json
      rule_registry_v1.schema.json
      auxiliary_construction_candidate_v1.schema.json
      provider_run_manifest.schema.json
      controller_strategy_log.schema.json
      research_contribution_record.schema.json
      evaluation_funnel.schema.json

  configs/
    default.yaml
    selected_implementations.example.yaml
    benchmark_runs/
      geometry_level2_smoke.yaml
      geometry_level2_ablation.yaml

  benchmarks/
    geometry/
      pool_manifest.yaml
      accepted_leangeo_subset_v1.jsonl
      rejected_by_extraction.jsonl

  tests/
    unit/
    integration/
    regression/
    mutation/

  scripts/
    check_release_acceptance.py
    run_geometry_level2_matrix.py
    generate_repro_report.py
```

---

## 7. TargetSubsetContract

TargetSubsetContract defines what the pipeline accepts as an initial theorem target.

It consists of:

```text
1. LeanGeoSubsetV1TheoremGrammar
2. predicate / construction / relation mappings
3. GeometryExtractionContract
4. GeometryExtractionReport
5. GeometryClaimSpec
6. fixtures and safe-reject policy
```

### 7.1 LeanGeoSubsetV1TheoremGrammar

LeanGeoSubsetV1 is not just a list of predicates. It is a theorem grammar.

```yaml
LeanGeoSubsetV1TheoremGrammar:
  version: "1.0.0"
  target_library: "LeanGeo"

  object_declarations:
    allowed:
      - id: "point_variables_only"
        description: "Theorem variables are points in the LeanGeo plane type."
      - id: "lines_from_two_distinct_points"
        description: "Lines are introduced through registered constructors from distinct points."
      - id: "circles_from_registered_constructors"
        description: "Circles are introduced only by supported construction templates."
    rejected:
      - "arbitrary object-level quantifier alternation"
      - "unregistered local geometric structures"
      - "raw Mathlib affine/metric geometry objects outside LeanGeoSubsetV1"

  hypothesis_forms:
    allowed:
      - "A ≠ B"
      - "collinear A B C"
      - "parallel (line A B) (line C D)"
      - "perpendicular (line A B) (line C D)"
      - "midpoint M A B"
      - "concyclic A B C D"
      - "equal_length A B C D"
      - "equal_angle A B C D E F"
    conditional:
      - form: "between A B C"
        condition: "orientation_policy_v1 must define supported semantics"
      - form: "same_side A B lineCD"
        condition: "diagram_case_policy_v1 must define supported semantics"

  target_forms:
    allowed:
      - "collinear A B C"
      - "parallel (line A B) (line C D)"
      - "perpendicular (line A B) (line C D)"
      - "concyclic A B C D"
      - "equal_length A B C D"
      - "equal_angle A B C D E F"
    rejected:
      - "target requiring unsupported orientation semantics"
      - "target using arbitrary Mathlib geometry expression"
      - "target with unsupported local notation"
      - "target requiring unsupported quantifier alternation"
      - "target whose conclusion is only related to provider target"
```

### 7.2 Fixture categories

Every accepted grammar entry must have fixtures.

```yaml
GrammarFixtureSet:
  grammar_entry_id: "..."
  positive_fixtures:
    - lean_file: "..."
      theorem_name: "..."
      expected_extraction: "accepted"

  negative_fixtures:
    - lean_file: "..."
      theorem_name: "..."
      expected_extraction: "rejected"
      reason_code: "missing_nondegeneracy | unsupported_target | unsupported_notation"

  ambiguous_fixtures:
    - lean_file: "..."
      theorem_name: "..."
      expected_extraction: "rejected"
      reason_code: "ambiguous_orientation | ambiguous_line_construction"

  mutation_fixtures:
    - mutation: "remove_distinctness_assumption"
      expected: "rejected_or_side_condition_obligation"
```

### 7.3 Mapping contracts

```yaml
PredicateMapping:
  target_library: "LeanGeoSubsetV1"
  mappings:
    - leangeo_predicate: "collinear"
      canonical_predicate: "Collinear(A,B,C)"
      normalization:
        permutation_policy: "registered"
        degeneracy_policy: "requires_distinctness_if_rule_demands"

    - leangeo_predicate: "parallel"
      canonical_predicate: "Parallel(Line(A,B), Line(C,D))"
      required_side_conditions:
        - "A ≠ B"
        - "C ≠ D"

    - leangeo_predicate: "equal_angle"
      canonical_predicate: "EqAngle(A,B,C,D,E,F)"
      angle_policy: "LeanGeoSubsetV1.angle_policy_v1"
      required_side_conditions:
        - "A ≠ B"
        - "C ≠ B"
        - "D ≠ E"
        - "F ≠ E"
```

```yaml
ConstructionMapping:
  target_library: "LeanGeoSubsetV1"
  supported_constructors:
    - constructor_id: "line_through_two_distinct_points"
      lean_template_id: "leangeo.constructor.line_two_points.v1"
      required_side_conditions:
        - "A ≠ B"

    - constructor_id: "midpoint"
      lean_template_id: "leangeo.constructor.midpoint.v1"
      required_side_conditions: []

    - constructor_id: "foot_of_perpendicular"
      lean_template_id: "leangeo.constructor.foot_perpendicular.v1"
      required_side_conditions:
        - "line is nondegenerate"
```

```yaml
RelationMapping:
  relation_to_goal:
    allowed_values:
      - exact
      - sufficient
      - related
      - none
    proof_use_policy:
      exact: "may proceed to compilation"
      sufficient: "may proceed only if direction_needed is claim_implies_goal"
      related: "diagnostic_only"
      none: "rejected"
```

### 7.4 GeometryExtractionContract

```yaml
GeometryExtractionContract:
  contract_id: "geometry_extraction_contract_v1"
  target_library: "LeanGeoSubsetV1"
  accepted_grammar_ref: "sha256:..."
  predicate_mapping_ref: "sha256:..."
  construction_mapping_ref: "sha256:..."
  relation_mapping_ref: "sha256:..."

  input:
    - theorem_name
    - goal_hash
    - lean_context_snapshot_hash
    - protected_statement_hash

  output:
    - GeometryExtractionReport
    - GeometryClaimSpec if accepted

  fail_safe_policy:
    unsupported_expression: "reject"
    ambiguous_orientation: "reject_or_generate_blocker"
    missing_nondegeneracy: "generate_side_condition_obligation_or_reject"
    unnormalized_local_notation: "reject"
    target_library_mismatch: "reject"
```

### 7.5 GeometryExtractionReport

```yaml
GeometryExtractionReport:
  extraction_report_id: "..."
  contract_id: "geometry_extraction_contract_v1"
  theorem_name: "..."
  goal_hash: "sha256:..."
  protected_statement_hash: "sha256:..."
  target_library: "LeanGeoSubsetV1"

  status: "accepted | rejected | blocked"
  reason_codes:
    - "..."

  extracted_objects:
    points: []
    lines: []
    circles: []

  extracted_hypotheses:
    - canonical_form: "..."
      source_lean_expr_hash: "sha256:..."

  extracted_target:
    canonical_form: "..."
    source_lean_expr_hash: "sha256:..."

  side_condition_summary:
    nondegeneracy:
      found: []
      missing: []
    orientation:
      found: []
      missing: []
    diagram_assumptions:
      found: []
      missing: []

  relation_to_goal:
    kind: "exact | sufficient | related | none"
    direction_needed: "claim_implies_goal | equivalence | not_applicable"
    direction_available: "extraction_contract_checked | none"
```

### 7.6 GeometryClaimSpec

`GeometryClaimSpec` cannot exist in proof-use path without `GeometryExtractionReport` provenance.

```yaml
GeometryClaimSpec:
  claim_spec_id: "geo_claim:<hash>"
  version: "1.0.0"
  source:
    extraction_report_ref: "sha256:..."
    theorem_name: "..."
    goal_hash: "sha256:..."
    protected_statement_hash: "sha256:..."

  objects:
    points: []
    lines: []
    circles: []

  hypotheses:
    - "Collinear(A,B,C)"
    - "Parallel(Line(A,B),Line(C,D))"

  target:
    relation: "..."

  required_side_conditions:
    - "A ≠ B"

  solver_semantic_profile:
    angle_policy: "angle_policy_v1"
    orientation_policy: "orientation_policy_v1"
    construction_policy: "construction_policy_v1"
```

---

## 8. Model plugin contracts

### 8.1 ResearchControllerPlugin

ResearchControllerPlugin is the only strategy boundary.

It may internally be:

```text
- a single strong model
- a smaller model
- DeepResearch-style planning
- multi-agent orchestration
- population search
- rater / evaluator loop
- human-guided strategy system
```

Core does not know these internals. Core sees only `ResearchStatePack -> ActionPlan`.

```yaml
ResearchControllerPlugin:
  controller_id: "research_controller:<name>:<version>"
  controller_manifest_hash: "sha256:..."
  input_schema: "ResearchStatePack.v1"
  output_schema: "ActionPlan.v1"

  input:
    ResearchStatePack:
      target_goal_summary: "..."
      open_frontier: []
      blockers: []
      reusable_results: []
      extraction_diagnostics: []
      solver_feedback: []
      allowed_actions: []
      forbidden_actions: []

  output:
    ActionPlan:
      work_orders: []
      geometry_solve_requests: []
      lemma_candidates: []
      auxiliary_construction_requests: []
      abandon_or_split_decisions: []
      rationale_ref: "sha256:..."
```

Controller rationale is diagnostic only. It is never proof evidence.

### 8.2 ProofWorkerPlugin

ProofWorkerPlugin is the only Lean editing / repair worker boundary.

```yaml
ProofWorkerPlugin:
  worker_id: "proof_worker:<name>:<version>"
  worker_manifest_hash: "sha256:..."
  input_schema: "WorkOrder.v1"
  output_schema: "WorkerResult.v1"

  responsibilities:
    - edit allowed proof region
    - integrate TraceCompiler patch candidates
    - introduce auxiliary constructions through ConstructionCompiler plans
    - run LeanPort / lake build when allowed
    - summarize Lean errors
    - return blockers when local repair fails

  forbidden:
    - edit protected theorem statement
    - add sorry
    - add forbidden axiom
    - change LeanGeo definitions
    - claim final success without FinalVerifyReport
```

### 8.3 WorkOrder

```yaml
WorkOrder:
  work_order_id: "..."
  target:
    theorem_name: "..."
    protected_statement_hash: "sha256:..."
    editable_region_ref: "sha256:..."

  task_kind:
    - "complete_proof"
    - "repair_proof"
    - "integrate_trace_patch"
    - "introduce_auxiliary_construction"
    - "discharge_side_condition"
    - "add_local_helper_lemma"

  inputs:
    proof_state_summary_ref: "sha256:..."
    trace_compilation_result_ref: "nullable sha256:..."
    construction_introduction_plan_ref: "nullable sha256:..."
    relevant_lemmas: []

  constraints:
    no_sorry: true
    theorem_statement_hash_must_remain: true
    forbidden_axioms: []
    max_local_repair_attempts: 3

  escalation_policy:
    return_to_controller_if:
      - "same_error_repeats"
      - "missing_lemma_required"
      - "unsupported_rule"
      - "side_condition_blocked"
```

### 8.4 WorkerResult

```yaml
WorkerResult:
  worker_result_id: "..."
  work_order_id: "..."
  status: "success_claimed | failed | blocked | diagnostic"

  produced_artifacts:
    lean_patch_ref: "nullable sha256:..."
    edited_file_ref: "nullable sha256:..."
    lean_log_ref: "nullable sha256:..."
    diagnostic_ref: "nullable sha256:..."

  final_verify_report_ref: "nullable sha256:..."
  proof_use_status: "not_allowed | lean_compiled | final_theorem"

  note:
    worker_success_claim_is_not_proof: true
```

---

## 9. ControllerStrategyLog and contribution tracking

ResearchControllerPlugin remains opaque to core semantics, but not invisible to evaluation.

### 9.1 ControllerStrategyLog

```yaml
ControllerStrategyLog:
  controller_id: "research_controller:<name>:<version>"
  controller_manifest_hash: "sha256:..."
  run_id: "..."
  strategy_fingerprint: "sha256:..."

  internal_capability_summary:
    uses_single_strong_model: true
    uses_smaller_model: false
    uses_multi_agent_orchestration: false
    uses_population_search: false
    uses_rater_or_evaluator: false
    uses_deep_planning: false
    uses_human_guidance: false

  action_counts:
    work_orders: 0
    geometry_solve_requests: 0
    proof_repair_requests: 0
    extraction_diagnostic_requests: 0
    auxiliary_construction_requests: 0
    lemma_candidate_requests: 0
    abandon_branch_decisions: 0

  generated_research_objects:
    lemma_candidates: 0
    auxiliary_construction_requests: 0
    case_split_candidates: 0
    proof_strategy_candidates: 0

  final_contribution_summary:
    contributed_to_final_theorem: "yes | no | unknown"
    contribution_refs: []
```

This log does not standardize controller internals. It only records what is needed for replay, attribution, and ablation.

### 9.2 ResearchContributionRecord

```yaml
ResearchContributionRecord:
  contribution_id: "contrib:<hash>"
  artifact_ref: "sha256:..."
  artifact_type:
    - "proof_edit"
    - "geotrace_step"
    - "auxiliary_construction"
    - "lemma_candidate"
    - "case_split_candidate"
    - "proof_strategy"
    - "diagnostic_blocker"
    - "side_condition_obligation"

  generated_by:
    boundary: "research_controller | proof_worker | geometry_solver_provider | human | scripted"
    implementation_id: "..."

  verification_status:
    - "unverified_hint"
    - "schema_checked"
    - "compiler_checked"
    - "lean_compiled"
    - "used_in_final_theorem"
    - "refuted"
    - "abandoned"

  final_contribution:
    status: "unused | used_in_search | used_in_final_proof | refuted_key_branch | diagnostic_only"
    linked_final_theorem: "nullable"
```

### 9.3 What belongs in DAG vs logs

ProofStateDAG should not become a log database.

An item belongs in ProofStateDAG only if removing it changes at least one of:

```text
- closure status
- proof-use reachability
- blocker visibility
- cache invalidation
- final theorem contribution tracing
```

Everything else belongs in ResearchEventLog, ControllerStrategyLog, ProviderRunManifest, or ArtifactStore.

---

## 10. GeometrySolverProvider and SolverPolicy

### 10.1 GeometrySolverProvider boundary

Core sees exactly one selected GeometrySolverProvider per run.

```yaml
GeometrySolverProvider:
  provider_id: "geometry_solver_provider:<name>:<version>"
  provider_manifest_hash: "sha256:..."
  input_schema: "GeometrySolveRequest.v1"
  output_schema: "ProviderResult.v1"

  may_use_internal_engines:
    - "Newclid-compatible"
    - "GenesisGeo-compatible"
    - "TongGeometry-compatible"
    - "local_search"
    - "auxiliary_construction_model"
    - "coordinate_oracle_for_search_hint"
    - "Wu_or_Groebner_oracle_for_search_hint"
    - "custom"

  proof_semantics:
    provider_result_is_not_proof: true
    raw_trace_is_not_proof: true
```

### 10.2 GeometrySolveRequest

```yaml
GeometrySolveRequest:
  request_id: "..."
  run_id: "..."
  source_claim:
    geometry_claim_spec_ref: "sha256:..."
    extraction_report_ref: "sha256:..."

  intent:
    - "produce_proof_trace"
    - "find_auxiliary_construction"
    - "produce_trace_and_constructions"
    - "diagnose_blocker"
    - "explore"

  trust_target:
    - "diagnostic"
    - "trace_candidate"
    - "construction_candidate"
    - "lean_patch_candidate"
    - "final_theorem"

  budget: "tiny | small | medium | heavy | extreme"

  constraints:
    target_library: "LeanGeoSubsetV1"
    output_trace_contract: "GeoTraceV1"
    output_construction_contract: "AuxiliaryConstructionCandidateV1"
    raw_dsl_input_allowed_for_proof_use: false
```

### 10.3 GeometrySolverPolicy

GeometrySolverPolicy is deterministic, versioned, logged, and testable. It is not a learned policy by default.

```yaml
GeometrySolverPolicy:
  policy_id: "geometry_solver_policy_v1"
  policy_hash: "sha256:..."

  decides:
    - provider_request_shape
    - resource budget translation
    - trace vs construction request balance
    - retry / fallback
    - unsupported trace handling
    - diagnostic classification

  does_not_decide:
    - proof-use promotion
    - theorem status
    - TrustGuard override
    - FinalVerifyGate result
```

### 10.4 GeometryExecutionPlan

```yaml
GeometryExecutionPlan:
  execution_plan_id: "..."
  execution_plan_hash: "sha256:..."
  request_hash: "sha256:..."
  geometry_claim_spec_hash: "sha256:..."
  solver_policy_id: "geometry_solver_policy_v1"
  solver_policy_hash: "sha256:..."

  selected_provider:
    provider_id: "geometry_solver_provider:<name>:<version>"
    provider_manifest_hash: "sha256:..."

  provider_intent:
    produce_geotrace: true
    produce_auxiliary_constructions: true
    produce_diagnostics: true

  resource_policy:
    budget: "small"
    timeout_sec: 0
    memory_mb: 0
    parallelism: 0

  reason_codes:
    - "extraction_exact"
    - "target_in_leangeo_subset_v1"
    - "construction_search_useful"
```

### 10.5 ProviderRunManifest

Provider abstraction is a safety boundary, not a reproducibility boundary. Provider internals must be logged.

```yaml
ProviderRunManifest:
  provider_id: "geometry_solver_provider:<name>:<version>"
  provider_manifest_hash: "sha256:..."
  run_id: "..."
  request_id: "..."
  claim_spec_hash: "sha256:..."
  execution_plan_hash: "sha256:..."

  internal_engines:
    - engine_family: "newclid_compatible | genesisgeo_compatible | tonggeometry_compatible | local_search | custom | analytic_hint_oracle"
      engine_name: "..."
      engine_version: "..."
      git_commit: "nullable"
      checkpoint_hash: "nullable sha256:..."
      rule_file_hash: "nullable sha256:..."
      config_hash: "sha256:..."
      random_seed: 0

  adapter:
    raw_trace_schema_version: "..."
    geotrace_normalizer_version: "..."
    construction_candidate_schema_version: "..."
    mapping_table_hash: "sha256:..."

  outputs:
    raw_log_hash: "sha256:..."
    geotrace_hash: "nullable sha256:..."
    construction_candidates_hash: "nullable sha256:..."
    unsupported_rule_count: 0
    side_condition_loss_count: 0
```

### 10.6 ProviderResult

```yaml
ProviderResult:
  provider_result_id: "..."
  request_id: "..."
  provider_run_manifest_ref: "sha256:..."

  status: "success | diagnostic | timeout | failed"
  result_kinds:
    - "geotrace_candidate"
    - "auxiliary_construction_candidates"
    - "diagnostic"

  artifact_refs:
    raw_log_ref: "sha256:..."
    raw_trace_ref: "nullable sha256:..."
    geotrace_v1_ref: "nullable sha256:..."
    construction_candidates_ref: "nullable sha256:..."
    diagnostic_ref: "nullable sha256:..."

  proof_use_status: "not_allowed"
  note: "ProviderResult is never proof evidence."
```

---

## 11. CompilerContract

CompilerContract defines how provider outputs become Lean proof candidates.

It consists of:

```text
1. GeoTraceV1
2. RuleRegistryV1
3. SideConditionReport
4. TraceCompiler
5. AuxiliaryConstructionCandidateV1
6. ConstructionCompiler
7. mutation tests
```

---

## 12. GeoTraceV1

### 12.1 Purpose

GeoTraceV1 is the canonical trace format. Provider-specific trace formats must be normalized to GeoTraceV1 before they can be checked by RuleRegistryV1.

```yaml
GeoTraceV1:
  trace_id: "geotrace:<hash>"
  version: "1.0.0"
  source:
    provider_result_ref: "sha256:..."
    provider_run_manifest_ref: "sha256:..."
    geometry_claim_spec_ref: "sha256:..."

  target:
    final_relation: "..."
    relation_to_claim_target: "exact | sufficient | related | none"

  objects:
    points: []
    lines: []
    circles: []

  steps:
    - step_id: "step:001"
      rule_id: "geo_rule:<id>:<version>"
      premises:
        - "..."
      conclusion: "..."
      referenced_objects: []
      side_condition_claims: []
      source_span_ref: "nullable"

  metadata:
    normalizer_version: "..."
    unsupported_original_steps: 0
    provider_confidence: "nullable"
```

### 12.2 TraceChecker

```yaml
TraceCheckerResult:
  trace_id: "..."
  schema_valid: true
  all_rules_registered: false
  supported_steps: []
  unsupported_steps: []
  malformed_steps: []
  target_relation_status: "matches_claim | sufficient | related | mismatch"
  result: "accepted_for_compilation | blocked | rejected"
```

Trace schema validity is not proof. It only allows the trace to enter RuleRegistryV1 checks.

---

## 13. RuleRegistryV1

### 13.1 Purpose

RuleRegistryV1 is the safety boundary between solver trace and Lean proof candidate.

It is not a name mapping. It is a rule-by-rule contract containing:

```text
- DSL / GeoTrace rule id
- Lean lemma or template
- premise pattern
- conclusion pattern
- required side conditions
- generated obligations
- automatic discharge policy
- unsupported variant behavior
- positive / negative / ambiguous fixtures
```

### 13.2 Rule contract schema

```yaml
GeometryRuleContract:
  rule_id: "geo_rule:parallel_angle_transfer:1"
  target_library: "LeanGeoSubsetV1"
  lean_template_id: "leangeo.rule.parallel_angle_transfer.v1"

  premise_pattern:
    - "Parallel(Line(A,B), Line(C,D))"
    - "Collinear(A,B,X)"
    - "Collinear(C,D,Y)"

  conclusion_pattern:
    - "EqAngle(A,X,?,C,Y,?)"

  required_side_conditions:
    nondegeneracy:
      - "A ≠ B"
      - "C ≠ D"
    orientation:
      - "angle_policy_v1_supported"
    diagram_assumptions: []

  generated_obligations:
    - obligation_kind: "nondegeneracy"
      canonical_form: "A ≠ B"
      discharge_policy: "from_context | simple_tactic | proof_worker | blocker"

  unsupported_variants:
    - "undirected_angle_mismatch"
    - "mod_pi_policy_mismatch"
    - "missing_distinctness"

  fixtures:
    positive:
      - "fixtures/rules/parallel_angle_transfer/positive_001.lean"
    negative:
      - "fixtures/rules/parallel_angle_transfer/missing_distinctness.lean"
    ambiguous:
      - "fixtures/rules/parallel_angle_transfer/orientation_ambiguous.lean"
```

### 13.3 Minimal supported rule families

The exact rule list is finalized in `rule_registry_v1.yaml`. The release target should be small but explicit.

Initial supported families may include:

```text
- collinearity propagation
- parallel / perpendicular transfer
- midpoint basic consequences
- concyclicity basic consequences
- equal length transfer from midpoint / circle constructors
- angle transfer for registered parallel / cyclic patterns
- construction-introduction rules for supported auxiliary constructions
```

The initial target is not broad automatic geometry. It is a narrow deterministic compiler for selected LeanGeoSubsetV1 rules.

### 13.4 SideConditionReport

```yaml
SideConditionReport:
  report_id: "..."
  source:
    geotrace_ref: "sha256:..."
    rule_registry_hash: "sha256:..."

  per_step:
    - step_id: "step:001"
      rule_id: "geo_rule:..."
      required_side_conditions:
        - "A ≠ B"
      found_in_context:
        - "A ≠ B"
      generated_obligations: []
      blockers: []
      status: "passed | generated_obligations | blocked | rejected"

  global_status: "passed | generated_obligations | blocked | rejected"
```

### 13.5 RuleRegistry release blockers

```text
[ ] Supported rule has no Lean lemma/template.
[ ] Supported rule has no required side-condition list.
[ ] Supported rule lacks positive fixture.
[ ] Supported rule lacks negative fixture.
[ ] Unsupported rule can be treated as supported.
[ ] Removing one premise from a step still compiles as accepted.
[ ] Missing side condition silently disappears.
[ ] Angle orientation mismatch is treated as proof success.
```

---

## 14. AuxiliaryConstructionCandidateV1

### 14.1 Purpose

Auxiliary construction is central to geometry. It must be a typed artifact, not a natural language suggestion.

Construction candidates are not proof evidence. They are proof-search aids that can become Lean proof contributions only after ConstructionCompiler + ProofWorker + FinalVerifyGate.

### 14.2 Initial supported construction kinds

The v0.3 contract deliberately restricts construction kinds.

```text
Supported in v0.3 target:
  - line_through_two_distinct_points
  - intersection_of_two_nonparallel_lines
  - foot_of_perpendicular
  - midpoint
  - circle_with_center_through_point

Not supported in v0.3 proof-use target:
  - arbitrary free point with constraints
  - arbitrary point_on_line_with_relation
  - arbitrary point_on_circle_with_relation
  - general line-circle intersection with tangent/non-tangent case split
  - general two-circle intersection
```

Rejected construction types may still be recorded as diagnostic or research hints, but cannot enter proof-use path.

### 14.3 Schema

```yaml
AuxiliaryConstructionCandidateV1:
  construction_id: "aux:<hash>"
  version: "1.0.0"
  source:
    provider_result_ref: "sha256:..."
    provider_run_manifest_ref: "sha256:..."
    geometry_claim_spec_ref: "sha256:..."

  construction_kind:
    - "line_through_two_distinct_points"
    - "intersection_of_two_nonparallel_lines"
    - "foot_of_perpendicular"
    - "midpoint"
    - "circle_with_center_through_point"

  introduced_objects:
    - name_hint: "X"
      object_type: "Point | Line | Circle"

  dependencies:
    points: []
    lines: []
    circles: []
    hypotheses: []

  intended_use:
    helps_prove:
      - "target_relation"
      - "intermediate_relation"
      - "side_condition"
    rationale_summary: "diagnostic only; not proof evidence"

  required_side_conditions:
    nondegeneracy: []
    incidence: []
    existence: []
    uniqueness_if_needed: []
    orientation: []
    diagram_cases: []

  lean_introduction_plan:
    theorem_template_id: "leangeo.constructor.<id>.v1 | missing"
    generated_obligations:
      - obligation_kind: "nondegeneracy | incidence | distinctness | orientation | existence"
        canonical_form: "..."
        discharge_policy: "from_context | simple_tactic | proof_worker | blocker"

  proof_use_status: "not_allowed_until_final_verify"
```

### 14.4 ConstructionChecker

```yaml
ConstructionCheckResult:
  construction_id: "..."
  schema_valid: true
  construction_kind_supported: true
  dependencies_resolved: true
  required_side_conditions_classified: true
  name_conflict_status: "none | auto_renamed | blocked"
  result: "accepted_for_compilation | blocked | rejected"
  blockers: []
```

### 14.5 ConstructionCompiler

```text
AuxiliaryConstructionCandidateV1
  -> ConstructionChecker
  -> side-condition classification
  -> Lean construction introduction plan
  -> generated side-condition obligations
  -> ProofWorker edits Lean proof
  -> Lean compile
  -> FinalVerifyGate
```

```yaml
ConstructionCompilationResult:
  result_id: "..."
  construction_candidate_ref: "sha256:..."
  status: "lean_patch_candidate | blocked | rejected"

  lean_introduction_patch_ref: "nullable sha256:..."
  generated_obligations:
    - obligation_id: "obl:..."
      obligation_kind: "nondegeneracy | incidence | existence | orientation"
      payload_ref: "sha256:..."

  blockers:
    - blocker_kind: "missing_existence_theorem | missing_nondegeneracy | unsupported_construction | name_conflict"
      diagnostic_ref: "sha256:..."

  proof_use_status: "not_allowed"
```

### 14.6 Auxiliary construction release blockers

```text
[ ] Candidate can be introduced without existence theorem or registered constructor template.
[ ] Required nondegeneracy can be dropped silently.
[ ] Name conflict can overwrite existing object.
[ ] Construction rationale is treated as proof evidence.
[ ] Unsupported construction kind enters proof-use path.
[ ] Construction introduction changes protected theorem statement.
[ ] Generated side-condition obligation is not tracked.
```

---

## 15. TraceCompiler

### 15.1 Role

TraceCompiler turns a checked subset of GeoTraceV1 into Lean patch candidates.

It does not prove the theorem by itself.

```text
GeoTraceV1
  -> TraceChecker
  -> RuleRegistryV1
  -> SideConditionReport
  -> TraceCompiler
  -> Lean patch candidate
  -> ProofWorker integration
  -> LeanPort compile
  -> FinalVerifyGate
```

### 15.2 TraceCompilationResult

```yaml
TraceCompilationResult:
  result_id: "..."
  geotrace_ref: "sha256:..."
  rule_registry_hash: "sha256:..."
  side_condition_report_ref: "sha256:..."

  status: "lean_patch_candidate | blocked | rejected"
  lean_patch_ref: "nullable sha256:..."

  generated_obligations:
    - obligation_id: "obl:..."
      obligation_kind: "side_condition"
      payload_ref: "sha256:..."

  blockers:
    - blocker_kind: "unsupported_rule | missing_side_condition | orientation_mismatch | target_mismatch"
      step_id: "step:..."
      diagnostic_ref: "sha256:..."

  proof_use_status: "not_allowed"
```

### 15.3 Compiler policy

```text
1. Unsupported rule returns blocker.
2. Missing side condition becomes an obligation or blocker.
3. Orientation mismatch returns blocker.
4. Target mismatch returns rejected.
5. Lean patch candidate is not proof evidence.
6. Only FinalVerifyGate can produce final_theorem status.
```

---

## 16. ProofStateDAG integration

### 16.1 Core node types

The geometry plan inherits the domain-neutral ProofStateDAG kernel.

```text
Obligation:
  target theorem, extracted geometry claim, side condition, construction obligation, unsupported-rule blocker.

Derivation:
  extraction, trace compilation, construction introduction, final Lean proof.

EvidenceRef:
  extraction report, provider result, side-condition report, trace compilation result, construction compilation result, final verify report.
```

Core node types remain:

```text
Obligation / Derivation / EvidenceRef
```

No geometry-specific node type is added to Base.

### 16.2 GraphPatch examples

#### Extraction accepted

```yaml
GraphPatch:
  add_obligations:
    - kind: "geometry_claim"
      owner: "plugin:geometry_synthetic"
      payload_schema_id: "geometry.claim_spec.v1"
      payload_ref: "sha256:..."
  attach_evidence:
    - evidence_kind: "geometry_extraction_report"
      artifact_ref: "sha256:..."
  add_derivations:
    - rule_id: "geometry.extraction.v1"
      proves: ["obl:geometry_claim"]
      required_gates: ["schema", "extraction_contract"]
      proof_use_status: "search_only"
```

#### Trace compiled but side condition missing

```yaml
GraphPatch:
  add_obligations:
    - kind: "side_condition"
      owner: "plugin:geometry_synthetic"
      payload_schema_id: "geometry.side_condition_obligation.v1"
      payload_ref: "sha256:..."
  attach_evidence:
    - evidence_kind: "trace_compilation_result"
      artifact_ref: "sha256:..."
  blockers:
    - blocker_kind: "missing_nondegeneracy"
```

#### Auxiliary construction introduced

```yaml
GraphPatch:
  add_obligations:
    - kind: "construction_side_condition"
      owner: "plugin:geometry_synthetic"
      payload_schema_id: "geometry.construction_side_condition.v1"
      payload_ref: "sha256:..."
  attach_evidence:
    - evidence_kind: "construction_compilation_result"
      artifact_ref: "sha256:..."
```

#### Lean final proof succeeds

```yaml
GraphPatch:
  attach_evidence:
    - evidence_kind: "lean_final_verify_report"
      artifact_ref: "sha256:..."
  add_derivations:
    - rule_id: "geometry.lean_final_proof.v1"
      proves: ["obl:target_goal"]
      required_gates: ["lean_final", "trust"]
      proof_use_status: "final_theorem"
```

### 16.3 Closure rule

```text
A target theorem obligation is closed iff:
  there exists a proof-use derivation with proof_use_status = final_theorem,
  all required side-condition obligations are closed,
  FinalVerifyReport is valid,
  protected theorem statement hash is unchanged.
```

ProviderResult, GeoTraceV1, construction candidates, controller rationale, worker success claims cannot close target theorem obligations.

---

## 17. BridgeGate and TrustGuard

### 17.1 GeometryBridgeGate is lightweight

In finite graph setting, BridgeGate must connect ClaimSpec / IR / encoding / certificate to a goal. In geometry × Lean, final authority is Lean final verification. Therefore BridgeGate should be lighter.

GeometryBridgeGate checks:

```text
- GeometryClaimSpec came from accepted GeometryExtractionReport.
- relation_to_goal is exact or sufficient in the required direction.
- target library is LeanGeoSubsetV1.
- generated patch targets the protected theorem / goal.
- proof-use path did not start from raw DSL input.
- theorem statement hash is protected.
```

It does not replace FinalVerifyGate.

### 17.2 GeometryBridgeReport

```yaml
GeometryBridgeReport:
  bridge_report_id: "..."
  target_goal:
    theorem_name: "..."
    goal_hash: "sha256:..."
    protected_statement_hash: "sha256:..."

  source_claim:
    geometry_claim_spec_hash: "sha256:..."
    extraction_report_hash: "sha256:..."

  relation_to_goal:
    kind: "exact | sufficient | related | none"
    direction_needed: "claim_implies_goal | equivalence | not_applicable"
    direction_available: "extraction_contract_checked | lean_checked | none"

  semantic_status:
    target_library: "LeanGeoSubsetV1"
    predicate_mapping_status: "defined"
    construction_mapping_status: "defined"
    rule_registry_status: "defined"
    side_condition_status: "passed | generated_obligations | blocked"
    trace_compilation_status: "lean_patch_candidate | blocked | rejected | not_applicable"
    construction_compilation_status: "lean_patch_candidate | blocked | rejected | not_applicable"
    lean_final_status: "passed | failed | not_run"

  proof_use_at_goal_level: false
  missing_links: []
```

### 17.3 Trust levels

```text
diagnostic_only:
  No mathematical conclusion.

extracted_claim:
  Lean goal was converted to GeometryClaimSpec.

raw_provider_result:
  Provider returned trace / construction candidates / diagnostic. Not proof-use.

checked_trace:
  GeoTraceV1 schema and supported rule subset checked. Not proof-use by itself.

construction_candidate_checked:
  Construction candidate schema and side conditions classified. Not proof-use by itself.

lean_patch_candidate:
  Compiler produced Lean patch candidate. Not proof-use by itself.

lean_compiled:
  Lean file compiled, but final theorem gate may still be pending.

final_theorem:
  FinalVerifyGate passed with theorem statement hash unchanged.
```

### 17.4 TrustGuard rules

```text
1. ProviderResult never closes a Lean goal.
2. Raw solver logs never close an obligation.
3. GeoTraceV1 schema-valid trace never closes a Lean goal.
4. checked_trace never closes a Lean goal.
5. AuxiliaryConstructionCandidate never closes a Lean goal.
6. lean_patch_candidate never closes a Lean goal.
7. Controller rationale is never proof evidence.
8. Worker claim of success is not proof evidence without FinalVerifyReport.
9. Theorem statement hash mismatch invalidates final theorem status.
10. FinalVerifyReport can close a target theorem only through DAGWriter / TrustGuard.
```

---

## 18. Standard proof loop

```text
1. LeanPort compiles current Lean file.
2. GoalAnchor is created for target theorem / unsolved subgoal.
3. ProofStateDAG records target obligation.
4. StateReader renders ResearchStatePack.
5. ResearchControllerPlugin emits ActionPlan.
6. ActionPlan may create WorkOrder or GeometrySolveRequest.
7. If geometry solving is requested, Lean goal is first processed by GeometryExtractionContract.
8. GeometryClaimSpec is created only if extraction is accepted.
9. GeometrySolverPolicy creates GeometryExecutionPlan.
10. Selected GeometrySolverProvider executes the plan.
11. ProviderResult is normalized to GeoTraceV1 / AuxiliaryConstructionCandidateV1 / Diagnostic.
12. TraceChecker / ConstructionChecker classify artifacts.
13. RuleRegistryV1 and side-condition calculus produce obligations or blockers.
14. TraceCompiler / ConstructionCompiler emit Lean patch candidates or blockers.
15. ProofWorkerPlugin edits Lean proof using patch candidates and context.
16. LeanPort compiles edited file.
17. FinalVerifyGate checks no sorry, no forbidden axioms, protected theorem hash unchanged.
18. DAGWriter commits GraphPatch with final theorem evidence or blockers.
19. RunLogger records ProviderRunManifest, ControllerStrategyLog, ResearchContributionRecord, EvaluationFunnel events.
20. StateReader returns updated ResearchStatePack.
```

---

## 19. Main workflows

### 19.1 Auxiliary construction workflow

```text
Lean goal
  -> GeometryExtractionContract accepted
  -> GeometryClaimSpec
  -> provider returns AuxiliaryConstructionCandidateV1
  -> ConstructionChecker validates schema / dependencies / construction kind
  -> side-condition calculus classifies nondegeneracy / existence / uniqueness / orientation
  -> ConstructionCompiler creates Lean introduction patch candidate
  -> ProofWorker introduces construction in Lean
  -> generated side-condition obligations are discharged or become blockers
  -> FinalVerifyGate decides final success
```

Construction candidates are research artifacts and proof-search aids. They are not proof evidence.

### 19.2 Proof trace workflow

```text
Lean goal
  -> GeometryExtractionContract accepted
  -> GeometryClaimSpec
  -> provider returns GeoTraceV1
  -> TraceChecker validates schema and target relation
  -> RuleRegistryV1 checks supported rules
  -> side-condition calculus generates obligations
  -> TraceCompiler creates Lean patch candidate
  -> ProofWorker integrates patch
  -> Lean build
  -> FinalVerifyGate
```

### 19.3 Proof repair workflow

```text
Lean compile failure
  -> LeanErrorSummarizer
  -> WorkerStatePack
  -> ProofWorker attempts local repair
  -> repeated failure escalates to ResearchControllerPlugin
  -> controller may request new solve, new construction, new lemma, or different proof strategy
```

### 19.4 Unsupported trace workflow

```text
Provider returns trace
  -> unsupported rule appears
  -> TraceCompiler returns blocker
  -> blocker is recorded in ProofStateDAG
  -> Controller receives concise unsupported-rule summary
  -> Controller may ask for a different plan or construction
```

Unsupported trace is never partial proof.

### 19.5 Discovery / research artifact workflow

```text
Controller proposes lemma / strategy / auxiliary construction request / case idea
  -> ResearchContributionRecord records it as unverified_hint
  -> if formalized, it becomes WorkOrder, GeometrySolveRequest, or DAG obligation
  -> if used in final Lean theorem, reverse reachability marks used_in_final_proof
  -> otherwise it remains used_in_search / diagnostic_only / abandoned
```

---

## 20. RunTraceContract

RunTraceContract is not proof-critical, but it is required for reproducibility and evaluation.

It includes:

```text
- RunRecord
- SelectedImplementations
- ProviderRunManifest
- ControllerStrategyLog
- ResearchContributionRecord
- EvaluationFunnel
- ReproducibilityReport
```

### 20.1 RunRecord

```yaml
RunRecord:
  run_id: "..."
  created_at: "..."
  target_library: "LeanGeoSubsetV1"
  selected_implementations_ref: "sha256:..."
  benchmark_group: "..."
  baseline_group: "..."
  human_hint_level: "none | light | heavy"
  trust_boundary: "strict_lean"
```

No `mode A/B/C/D` field is used.

### 20.2 EvaluationFunnel

The benchmark pool must be fixed before extraction to avoid cherry-picking.

```yaml
EvaluationFunnel:
  run_matrix_id: "..."
  benchmark_pool_ref: "sha256:..."

  counts:
    total_theorems: 0
    extraction_accepted: 0
    extraction_rejected: 0
    solver_attempted: 0
    provider_returned_geotrace: 0
    provider_returned_aux_construction: 0
    trace_supported_by_rule_registry: 0
    construction_accepted_by_compiler: 0
    construction_introduced_in_lean: 0
    side_conditions_discharged: 0
    lean_patch_compiled: 0
    final_theorem_success: 0

  rejection_breakdown:
    unsupported_expression: 0
    missing_nondegeneracy: 0
    unsupported_orientation: 0
    unsupported_rule: 0
    unsupported_construction: 0
    final_verify_failed: 0
```

### 20.3 ReproducibilityReport

```yaml
ReproducibilityReport:
  run_id: "..."
  replay_status: "passed | failed | partial"
  selected_implementations_restored: true
  artifacts_restored: true
  provider_manifest_restored: true
  controller_strategy_log_restored: true
  final_verify_replayed: true
  differences: []
```

---

## 21. Evaluation target: Level 2 domain-tool advantage

v0.3's first research evaluation target is Level 2.

```text
Level 2: Domain-tool advantage
  LeanGeoSubsetV1 theorem set に対して、
  geometry.solve + TraceCompiler + ConstructionCompiler + Lean final verification を含む pipeline が、
  model-only / worker-only baseline より、
  Lean final theorem rate、proof repair success、auxiliary construction introduction、side-condition discharge、required interaction count のいずれかで明確に改善する。
```

This is not a claim of open-problem solving.

### 21.1 Minimal baseline matrix

Baselines are evaluation configurations, not runtime architecture modes.

```text
B0: ProofWorker-only
  ProofWorkerPlugin only. No ResearchController, no geometry.solve.

B1: Controller + ProofWorker, no geometry.solve
  Measures controller reasoning without domain solver.

B2: Geometry-enabled full pipeline
  Controller + ProofWorker + geometry.solve + trace/construction compilers.

B3: Strong-model without geometry.solve
  Tests whether strong model alone solves the same set.

B4: Lower-model + geometry.solve
  Tests whether domain solver compensates for weaker model reasoning.

B5: Same provider, construction generation disabled
  Evaluation-only ablation to measure auxiliary construction contribution.
```

`B5` is not a core optional mode. It is an evaluation configuration controlled by run matrix and logged in `baseline_group`.

### 21.2 Metrics

```text
Proof metrics:
  - Lean final verification rate
  - theorem statement hash preserving success rate
  - proof repair success rate
  - side-condition discharge rate
  - unsupported-rule blocker rate

Auxiliary construction metrics:
  - construction candidates generated
  - construction candidates accepted by schema
  - construction candidates accepted by ConstructionCompiler
  - construction candidates introduced in Lean
  - introduced constructions used in final proof
  - construction candidates causing blockers

Controller reasoning metrics:
  - lemma candidates generated
  - useful lemma candidates
  - proof strategy candidates generated
  - geometry solve requests caused by controller
  - required interaction count
  - human hint level

Provider metrics:
  - GeoTraceV1 returned count
  - auxiliary construction returned count
  - unsupported rule count
  - side-condition loss count
  - replay success rate
  - provider result reproducibility

Resource metrics:
  - wall time
  - model calls
  - solver calls
  - local compute budget used
  - Lean compile attempts
```

---

## 22. CI / regression / mutation tests

### 22.1 Extraction mutation tests

```text
[ ] Removing A ≠ B makes extraction rejected or creates side-condition obligation.
[ ] between A B C and between A C B are not silently identified.
[ ] local notation that cannot be normalized is safe-rejected.
[ ] Mathlib geometry target mixed into LeanGeoSubsetV1 target is rejected.
[ ] raw DSL problem cannot enter proof-use path.
[ ] relation_to_goal = related cannot close target theorem.
```

### 22.2 RuleRegistry / TraceCompiler mutation tests

```text
[ ] Removing one premise from GeoTraceV1 step is rejected.
[ ] Unsupported rule disguised as supported rule is rejected.
[ ] Angle orientation inversion becomes blocker.
[ ] Missing side condition becomes generated obligation or blocker.
[ ] Final claim mismatch is not proof-use.
[ ] Malformed trace fails safe.
[ ] Positive rule fixture compiles.
[ ] Negative rule fixture fails for the intended reason.
```

### 22.3 AuxiliaryConstruction / ConstructionCompiler mutation tests

```text
[ ] Candidate without existence theorem is not introduced.
[ ] Required nondegeneracy removal produces blocker.
[ ] Unsupported construction kind cannot enter proof-use path.
[ ] Name conflict auto-renames or blocks.
[ ] Construction introduction cannot change theorem statement hash.
[ ] Construction rationale is not proof evidence.
[ ] Generated side-condition obligations are tracked.
```

### 22.4 Controller observability tests

```text
[ ] ResearchControllerPlugin cannot mutate DAG directly.
[ ] Controller rationale is not proof evidence.
[ ] ControllerStrategyLog exists for every run.
[ ] human_hint_level is logged when human guidance is used.
[ ] Strategy fingerprint is comparable across runs.
```

### 22.5 Final verification misuse tests

```text
[ ] theorem statement hash mismatch fails.
[ ] generated helper lemma with sorry fails.
[ ] forbidden axiom fails.
[ ] WorkerResult success without FinalVerifyReport fails.
[ ] ProviderResult proof_plan cannot become final theorem evidence.
[ ] Lean final status cannot be set without LeanPort / FinalVerifyGate artifact.
```

### 22.6 Option creep regression tests

```text
[ ] Adding AgentC / AgentD as core runtime mode fails release acceptance.
[ ] Enabling second target library fails release acceptance.
[ ] Adding provider-specific branch in Base fails regression.
[ ] Adding provider-specific proof semantics in TrustGuard fails regression.
[ ] Allowing direct DSL input to close obligation fails regression.
[ ] Adding TraceCompiler variant selected by controller fails regression.
```

---

## 23. Release blockers

Full v0.3 release is blocked if any of the following holds.

```text
Target / extraction:
  [ ] Target library is not exactly LeanGeoSubsetV1.
  [ ] LeanGeoSubsetV1TheoremGrammar is missing.
  [ ] Grammar fixtures are missing.
  [ ] GeometryExtractionContract is missing.
  [ ] GeometryClaimSpec can be created without accepted extraction provenance.
  [ ] Unsupported expression is not safe-rejected.
  [ ] relation_to_goal classifier is missing.

Model / controller:
  [ ] Agent C/D exists as core runtime mode.
  [ ] Core has model-specific GPT-Pro / Codex branches.
  [ ] ResearchControllerPlugin can mutate DAG directly.
  [ ] Controller rationale can become proof evidence.
  [ ] ControllerStrategyLog is missing from runs.

Solver provider:
  [ ] Core branches on Newclid / GenesisGeo / TongGeometry names.
  [ ] ProviderRunManifest is missing.
  [ ] ProviderResult can become proof evidence.
  [ ] raw DSL problem can enter proof-use path.

Compiler:
  [ ] RuleRegistryV1 lacks side-condition calculus.
  [ ] Supported rule lacks Lean lemma/template.
  [ ] Supported rule lacks fixtures.
  [ ] Unsupported rule can produce Lean patch candidate as if supported.
  [ ] AuxiliaryConstructionCandidateV1 schema is missing.
  [ ] ConstructionCompiler is missing.
  [ ] Unsupported construction can enter proof-use path.

Trust / final verification:
  [ ] ProofWorker can modify protected theorem statement undetected.
  [ ] FinalVerifyGate does not check no-sorry.
  [ ] FinalVerifyGate does not check theorem statement hash.
  [ ] Worker success claim closes target theorem without FinalVerifyReport.
  [ ] raw trace / construction rationale / controller rationale raises proof_use_status.

Evaluation / replay:
  [ ] EvaluationFunnel is missing.
  [ ] Run replay cannot restore selected controller / worker / provider / rule registry.
  [ ] ResearchContributionRecord cannot distinguish used_in_search from used_in_final_proof.
```

---

## 24. Workstreams as repo construction areas

These are not MVP phases. They are construction areas required for the final target.

### Workstream A: Base runtime and artifact integrity

Deliverables:

```text
ArtifactStore
RunLogger
TrustGuard
DiagnosticBundle
SelectedImplementations
plugin manifest hashing
replay discipline
```

Acceptance:

```text
All proof-critical artifacts have stable hashes.
Raw provider outputs cannot become proof-use evidence.
Selected controller / worker / provider / rule registry manifests are replayable.
```

### Workstream B: ProofStateDAG core

Deliverables:

```text
Obligation / Derivation / EvidenceRef
GraphPatch
DAGWriter
closure engine
StateReader
ResearchStatePack / WorkerStatePack rendering hooks
```

Acceptance:

```text
Plugins cannot directly mutate DAG.
Model plugins receive summarized state, not full DAG.
Proof-use edges remain acyclic.
DAG inclusion criterion is enforced.
```

### Workstream C: Lean integration

Deliverables:

```text
LeanPort
GoalAnchor
FinalVerifyGate
protected theorem hash checker
no-sorry checker
forbidden axiom checker
Lean error summarizer
editable-region guard
```

Acceptance:

```text
ProofWorker cannot change protected theorem statement undetected.
Final theorem status requires Lean verification.
Lean failure becomes structured feedback.
```

### Workstream D: Model plugin contracts

Deliverables:

```text
ResearchControllerPlugin API
ProofWorkerPlugin API
ActionPlan
WorkOrder
WorkerResult
ResearchStatePack / WorkerStatePack
ControllerStrategyLog
```

Acceptance:

```text
No core GPT-Pro / Codex references.
No AgentC/D core mode.
Composite controllers can be used without changing Base.
Controller internals are logged without being standardized.
```

### Workstream E: TargetSubsetContract

Deliverables:

```text
LeanGeoSubsetV1TheoremGrammar
predicate mapping
construction mapping
relation mapping
fixtures
GeometryExtractionContract
GeometryExtractionReport
GeometryClaimSpec
```

Acceptance:

```text
Accepted theorem grammar is explicit.
Unsupported expressions reject safely.
relation_to_goal is classified.
Nondegeneracy / orientation / diagram assumptions are extracted or blocked.
```

### Workstream F: GeometrySolverProvider and SolverPolicy

Deliverables:

```text
GeometrySolverProvider contract
GeometrySolveRequest
GeometryExecutionPlan
ProviderResult
ProviderRunManifest
GeometrySolverPolicy
failure classification
```

Acceptance:

```text
Core sees exactly one provider.
Provider outputs GeoTraceV1 / AuxiliaryConstructionCandidateV1 / Diagnostic.
ProviderResult cannot be proof-use evidence.
Provider internals are reproducibility-logged.
```

### Workstream G: GeoTraceV1 and RuleRegistryV1

Deliverables:

```text
GeoTraceV1 schema
TraceChecker
RuleRegistryV1
SideConditionReport
supported rule subset
positive / negative / ambiguous fixtures
```

Acceptance:

```text
Supported rules have Lean templates and side-condition contracts.
Unsupported rules become blockers.
Malformed trace is rejected.
Mutation tests fail for missing premise / missing side condition / orientation mismatch.
```

### Workstream H: AuxiliaryConstructionCandidateV1 and ConstructionCompiler

Deliverables:

```text
AuxiliaryConstructionCandidateV1
ConstructionChecker
ConstructionCompiler
Lean introduction templates
generated side-condition obligations
construction contribution logging
```

Acceptance:

```text
Only supported construction kinds enter proof-use path.
Existence and nondegeneracy requirements are explicit.
Construction candidate is not proof evidence.
Final contribution is recorded only after Lean final theorem uses it.
```

### Workstream I: TraceCompiler and ProofWorker integration

Deliverables:

```text
TraceCompiler
Lean patch templates
TraceCompilationResult
ProofWorker import-trace workflow
positive compile fixtures
```

Acceptance:

```text
Lean patch candidates compile on positive fixtures.
Side-condition obligations enter ProofStateDAG.
TraceCompilationResult is not proof-use until FinalVerifyGate.
```

### Workstream J: Evaluation / replay / release acceptance

Deliverables:

```text
EvaluationFunnel
Level 2 run matrix
baseline configs
ResearchContributionRecord
reproducibility report
release acceptance checker
option creep regression tests
```

Acceptance:

```text
Domain-tool advantage can be measured.
Run replay restores model/plugin/provider manifests and proof artifacts.
Release blockers are machine-checkable.
```

---

## 25. Decision records

```text
DR-GEO-001:
  Initial target is geometry × Lean, with Lean theorem already formalized.

DR-GEO-002:
  Target library is LeanGeoSubsetV1 only.

DR-GEO-003:
  Mathlib is dependency only, not separate bridge target.

DR-GEO-004:
  local geometry micro-library is not proof target.

DR-GEO-005:
  LeanGeoSubsetV1 is defined by theorem grammar + fixtures, not just predicate list.

DR-GEO-006:
  Proof-use geometry solving starts from Lean goal extraction.

DR-GEO-007:
  GeometryExtractionContract is required before GeometryClaimSpec creation.

DR-GEO-008:
  Direct raw DSL problem input is not proof-use eligible.

DR-GEO-009:
  GeoTraceV1 is canonical trace contract.

DR-GEO-010:
  Raw solver trace is not proof evidence.

DR-GEO-011:
  RuleRegistryV1 includes side-condition calculus.

DR-GEO-012:
  Supported rule subset only can produce Lean patch candidates.

DR-GEO-013:
  Unsupported rule / missing side condition / orientation mismatch becomes blocker.

DR-GEO-014:
  AuxiliaryConstructionCandidateV1 is a first-class research artifact.

DR-GEO-015:
  Auxiliary construction candidates are not proof evidence.

DR-GEO-016:
  ConstructionCompiler is required for construction proof-use path.

DR-GEO-017:
  Final theorem status requires Lean final verification.

DR-GEO-018:
  Agent A/B/C/D taxonomy is removed from core.

DR-GEO-019:
  Core model boundaries are ResearchControllerPlugin and ProofWorkerPlugin only.

DR-GEO-020:
  Multi-agent orchestration is internal to ResearchControllerPlugin, not core mode.

DR-GEO-021:
  Core solver boundary is GeometrySolverProvider only.

DR-GEO-022:
  Newclid / GenesisGeo / TongGeometry are provider-internal implementation details, not core options.

DR-GEO-023:
  ProviderRunManifest is required for reproducibility.

DR-GEO-024:
  ControllerStrategyLog is required for attribution, but controller internals are not standardized.

DR-GEO-025:
  ResearchContributionRecord distinguishes search contribution from final proof contribution.

DR-GEO-026:
  Exactly one target library, controller, worker, provider, solver policy, rule registry, and trust boundary are selected per run.

DR-GEO-027:
  Evaluation Level 2 is domain-tool advantage for Lean-verified geometry proof.
```

---

## 26. Main risks and mitigations

### 26.1 Extraction remains too hard

Risk:

```text
LeanGeo theorem syntax may be more complex than expected, blocking GeometryClaimSpec generation.
```

Mitigation:

```text
LeanGeoSubsetV1TheoremGrammar is deliberately closed and explicit.
Unsupported expressions reject safely.
Extraction diagnostics are first-class.
Benchmark funnel reports rejected / accepted counts.
```

### 26.2 RuleRegistryV1 becomes too broad

Risk:

```text
Trying to support arbitrary solver trace rules sinks the project.
```

Mitigation:

```text
Supported rule subset only.
Rule-by-rule Lean template and side-condition contract.
Unsupported rules become blockers.
Provider may search broadly, but proof-use requires supported GeoTraceV1.
```

### 26.3 Auxiliary construction becomes natural-language hint only

Risk:

```text
Provider proposes useful-looking auxiliary points, but they cannot be introduced into Lean safely.
```

Mitigation:

```text
AuxiliaryConstructionCandidateV1 schema.
Supported construction kinds only.
ConstructionCompiler with existence / nondegeneracy / generated obligations.
Final contribution only after Lean final proof.
```

### 26.4 Solver provider portfolio leaks into core

Risk:

```text
Newclid / GenesisGeo / TongGeometry-specific branches accumulate in Base.
```

Mitigation:

```text
Core sees GeometrySolverProvider and canonical outputs only.
Provider internals are logged in ProviderRunManifest.
Regression test forbids provider-specific branches in Base.
```

### 26.5 Model plugin grows into new AgentC/D subsystem

Risk:

```text
ResearchControllerPlugin internally uses population / rater and starts requiring core support.
```

Mitigation:

```text
Controller internal state is artifact/log only.
Core accepts only ActionPlan / WorkOrder / GeometrySolveRequest.
ControllerStrategyLog records capabilities without standardizing internals.
No population node type enters core DAG unless formalized as an Obligation through GraphPatch.
```

### 26.6 Evaluation overclaims

Risk:

```text
A small accepted subset makes results look stronger than they are.
```

Mitigation:

```text
Benchmark pool fixed before extraction.
EvaluationFunnel reports accepted / rejected / supported / final success counts.
Claims are limited to Level 2 domain-tool advantage.
```

---

## 27. Plan statement

```text
本研究は、APN 型の Lean feedback loop と proof-state reuse を参考にしつつ、
AlphaProof のような汎用 Lean prover を再現するのではなく、
LeanGeoSubsetV1 に限定した geometry × Lean DomainProofCompiler を構築する。

初期対象は、Lean により正しく定式化済みの初等幾何 theorem を、
synthetic geometry solver と model-pluggable proof workflow を用いて、
Lean final verification まで閉じることである。

本 pipeline は Lean proof closing だけを目的としない。
ResearchControllerPlugin は Lean feedback、ProofStateDAG summary、solver feedback を用いて、
証明方針、補題候補、補助構成の要求、proof repair 方針を生成できる。
GeometrySolverProvider は Newclid / GenesisGeo / TongGeometry 系 solver、guided tree search、auxiliary construction models などを内部利用し、
GeoTraceV1 だけでなく AuxiliaryConstructionCandidateV1 も返せる。

ただし、これらの探索 artifact はそのまま proof evidence にはならない。
補助構成は AuxiliaryConstructionCandidateV1 と ConstructionCompiler を通して Lean に導入され、
trace は GeoTraceV1 と RuleRegistryV1 side-condition calculus を通して Lean patch candidate になり、
ProofWorker が Lean proof に統合し、FinalVerifyGate が theorem statement hash unchanged / no sorry / no forbidden axioms を確認した場合にのみ、
最終 theorem への貢献として認める。

core architecture は、具体モデル名や Agent A/B/C/D taxonomy を持たない。
ResearchControllerPlugin と ProofWorkerPlugin だけを model boundary とし、
単一モデル、GPT-Pro 型強モデル、Codex 型 worker、DeepResearch 型 orchestration、複数 agent は、
すべて plugin 内部実装として扱う。

幾何 solver についても、Newclid / GenesisGeo / TongGeometry を core option として列挙しない。
core は GeometrySolverProvider だけを知り、provider は GeometryClaimSpec を受け取り、
GeoTraceV1、AuxiliaryConstructionCandidateV1、または diagnostic を返す。

評価上の最初の主張は、未解決問題の解決ではなく、
LeanGeoSubsetV1 の幾何 theorem に対して、geometry.solve を組み込んだ pipeline が、
model-only / worker-only baseline より Lean final theorem rate、補助点発見・導入、proof repair 成功、side-condition discharge、required interaction count で改善する、
という Level 2 domain-tool advantage である。
```

---

## 28. Final release acceptance checklist

```text
TargetSubsetContract:
  [ ] Target library is LeanGeoSubsetV1 only.
  [ ] LeanGeoSubsetV1TheoremGrammar is documented.
  [ ] Accepted / rejected / ambiguous fixtures exist.
  [ ] Predicate / construction / relation mappings are documented.
  [ ] GeometryExtractionContract is implemented.
  [ ] GeometryExtractionReport is produced for every proof-use geometry solve.
  [ ] GeometryClaimSpec cannot exist without extraction provenance.
  [ ] raw DSL problem cannot close any obligation.

Model boundaries:
  [ ] Agent C/D core modes are absent.
  [ ] ResearchControllerPlugin and ProofWorkerPlugin contracts are stable.
  [ ] No core GPT-Pro / Codex references exist.
  [ ] Controller rationale is not proof evidence.
  [ ] Worker success claim is not proof evidence without FinalVerifyReport.
  [ ] ControllerStrategyLog is recorded.

Solver provider:
  [ ] GeometrySolverProvider boundary is singular.
  [ ] Selected provider manifest is logged and replayable.
  [ ] ProviderRunManifest is produced.
  [ ] Provider-specific names do not appear in Base control flow.
  [ ] ProviderResult cannot become proof evidence.

CompilerContract:
  [ ] GeoTraceV1 schema is stable.
  [ ] RuleRegistryV1 has side-condition calculus.
  [ ] Supported rules have Lean lemma/templates.
  [ ] Supported rules have positive and negative fixtures.
  [ ] Unsupported rules become blockers.
  [ ] AuxiliaryConstructionCandidateV1 schema is stable.
  [ ] ConstructionCompiler is implemented.
  [ ] Unsupported construction kinds are blocked.
  [ ] TraceCompiler / ConstructionCompiler outputs are not proof evidence.

ProofState / Trust:
  [ ] ProofStateDAG uses Obligation / Derivation / EvidenceRef core only.
  [ ] Plugins update DAG only through GraphPatch.
  [ ] Proof-use subgraph is acyclic.
  [ ] ProofWorker cannot modify protected theorem statement undetected.
  [ ] FinalVerifyGate checks theorem hash, no sorry, and forbidden axioms.
  [ ] raw trace / construction rationale / controller rationale cannot raise proof_use_status.

Evaluation / replay:
  [ ] EvaluationFunnel is generated.
  [ ] ResearchContributionRecord distinguishes used_in_search from used_in_final_proof.
  [ ] Run replay can reconstruct selected controller / worker / provider / solver policy / rule registry / trust boundary.
  [ ] Level 2 domain-tool advantage logs can be generated.
  [ ] Option creep regression tests pass.
```

---

## 29. Final summary

v0.3 の最終方針は次である。

```text
1. 初期対象は geometry × Lean、target は LeanGeoSubsetV1 に固定する。
2. LeanGeoSubsetV1 は theorem grammar + fixtures として定義する。
3. proof-use 経路は必ず Lean goal extraction から始める。
4. raw DSL problem / raw provider result / raw trace / controller rationale / worker claim は proof evidence ではない。
5. Agent C/D taxonomy は core から削除し、ResearchControllerPlugin に統合する。
6. Newclid / GenesisGeo / TongGeometry は core option ではなく GeometrySolverProvider 内部実装とする。
7. 補助点生成は AuxiliaryConstructionCandidateV1 + ConstructionCompiler により標準化する。
8. GeoTraceV1 は RuleRegistryV1 side-condition calculus を通らなければ Lean patch candidate にならない。
9. 最終 authority は FinalVerifyGate / Lean kernel である。
10. 研究探索の寄与は ControllerStrategyLog / ProviderRunManifest / ResearchContributionRecord / EvaluationFunnel で測る。
11. optional runtime mode は増やさず、各 run は exactly-one-selected implementation を持つ。
```

この形により、v0.2 の「狭い plugin boundary」「No loose options」「AgentC/D 削除」という整理を維持しつつ、補助点生成・solver trace・controller reasoning を実際に研究 contribution として測れる geometry × Lean pipeline になる。
