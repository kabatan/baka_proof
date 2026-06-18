---
title: "Guardian Base Spec — Geometry × Lean Full2D Real Solver-Causal Pipeline v0.4.4 Reviewed"
spec_id: "MARP-GEOLEAN-BASE-009"
revision: "reviewed-2026-06-18"
status: "USER_APPROVED_ACTIVE"
target_repo: "kabatan/baka_proof"
created: "2026-06-18"
supersedes_when_approved:
  - "MARP-GEOLEAN-BASE-008"
  - "previous drafts of MARP-GEOLEAN-BASE-009"
claim_target: "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY"
authority_model: "After approval, this reviewed Base Spec is the only source of truth. Plan, implementation, tests, reports, debt ledgers, and closure may not weaken it. Do not install earlier v0.4.4 drafts beside this file as active authority."
---

# Guardian Base Spec — Geometry × Lean Full2D Real Solver-Causal Pipeline v0.4.4 Reviewed

## 0. Purpose

This Base Spec supersedes the v0.4.3 implementation target and all earlier v0.4.4 drafts after user approval. It exists because the prior implementation produced an apparently valid `ActualTaskPipelineRun` and certificate chain while still relying on projection obligations and fixed facade lemma applications.

The only admitted completion claim is:

```text
V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY
```

This claim means:

```text
For the approved GeometryFull2DTarget:1.0.0 formal 2D Euclidean geometry target language, the repository executes a real solver-backed proving pipeline for counted positive theorem tasks.

A counted success must be caused by solver artifacts and compilers that consume those artifacts. It may not be caused by benchmark labels, projection templates, prewritten proof snippets, facade evidence fields, direct lemma wrappers, proof artifact overlays, task-id-derived references, or source-goal simplification.

The release corpus must contain non-projection formal geometry goals. External-source tasks must preserve the source goal, not merely project points/predicates into easy obligations. Sealed challenge tasks must be generated independently of compiler proof labels and must not expose proof templates to release compilers.
```

## 1. Failure modes this spec explicitly blocks

The following paths are release-failing:

```text
external DSL source -> generated projection theorem -> fixed facade lemma -> certificate chain
benchmark template_id -> proof snippet -> FinalVerifyGate -> counted success
same target-shaped theorem -> solver refs attached but not causally needed -> counted success
smoke extraction JSON -> reused as extraction evidence for many tasks
source theorem already proved -> rewritten as solver-backed success
engine output contains Lean proof text -> compiler copies it
compiler reads task_id/theorem_family/grammar_family/template_id/provenance -> proof decision
renamed or shimmed v0.4.3 release path -> v0.4.4-looking command -> counted success
stale v0.4.4 checker or matrix output -> release report -> closure
```

## 2. Non-negotiable decisions

### DR-009-001 — v0.4.3 closure is not sufficient evidence

The v0.4.3 `CLOSURE.md`, release reports, projection corpus, and `ActualTaskPipelineRunV1` records are evidence from a previous attempt only. They are regression fixtures and negative examples unless they satisfy this reviewed v0.4.4 spec.

### DR-009-002 — No projection-only release corpus

A positive task is not release-admissible merely because it is anchored to an external formal source. A task is projection-only, and therefore non-counted, if the translated target is selected from a generator projection kind such as:

```text
collinear_refl_left, equal_length_symm, directed_angle_eq_symm, between_collinear,
length_le_trans, midpoint_collinear, reflection_has_evidence, rotation_preserves_collinear,
or any structurally similar direct/facade obligation.
```

Projection tasks may remain as regression tests, smoke tests, examples, or measured diagnostics. They do not count toward positive corpus floors, family thresholds, success rates, or advantage metrics.

### DR-009-003 — Release-positive task categories

Every counted positive task must belong to exactly one of these categories:

```text
ExternalGoalPreserved:
  A formal external geometry source whose source goal is preserved as the GeometryFull2D theorem target.
  Requires GoalPreservationReportV1.

SealedSolverChallenge:
  A formal challenge generated/imported through a sealed mechanism independent of compiler proof labels.
  Requires SealedChallengeManifestV1.

UserReviewedGoal:
  A formal Lean theorem approved by user or named reviewer as a legitimate target.
  Requires ReviewManifestV1.
```

`UserReviewedGoal` is allowed but has no fixed release floor. Codex must not block final implementation solely because the user did not supply reviewed goals. Codex must also never relabel its own generated tasks as `UserReviewedGoal`.

### DR-009-004 — Counted success requires solver-causal necessity

Every counted B2 positive final theorem must have an `ActualTaskPipelineRunV2` and a passing `SolverCausalityReportV1`.

Required chain:

```text
source theorem with sorry-only MARP proof region
  -> Lean-side structured extraction for that theorem
  -> GeometryFull2DClaimSpecV2
  -> GeometryFull2DProvider.solve actual run
  -> EngineOutputFull2D artifacts with real execution evidence
  -> compiler consumes normalized solver artifacts
  -> solver-causal mutation checks
  -> LeanPatchCandidateFull2D
  -> ProofWorker patch application
  -> FinalVerifyGate on generated candidate file
  -> SolverBackedProofCertificateFull2D binding all previous artifacts
  -> artifact-derived metrics and advantage reports
```

If removing or corrupting the selected solver artifact still produces the same counted patch and final theorem, the success is not solver-causal and cannot be counted.

### DR-009-005 — Direct/facade lemma dominance is not allowed

The following are shallow proof forms:

```text
exact lemma ... where lemma directly matches the target
have h : target := by exact lemma ...; exact h
direct use of a facade theorem whose premises are exactly the source theorem hypotheses and whose conclusion is the target
projection of an evidence field from a facade structure as the main geometry proof
proof text selected from static target shape without a solver-derived intermediate fact
```

Shallow proof forms may be counted only when they are solver-causal and under the strict ceiling in Acceptance. They do not count as non-target solver intermediate facts merely by being wrapped in `have`.

### DR-009-006 — Compiler input isolation

Release compilers may read only:

```text
GeometryFull2DClaimSpecV2
normalized engine outputs
RuleRegistryFull2D
SideConditionCalculusFull2D
target theorem hash
allowed edit region
selected implementation manifest
```

Release compilers must not read the following for proof decision:

```text
task_id
theorem_name except for patch anchoring
theorem_family
grammar_family
difficulty_tier
template_id
provenance
source_ref except for artifact bookkeeping
benchmark family thresholds
corpus generator private labels
proof text embedded in corpus metadata
```

Static checker, runtime taint checker, and regression tests must enforce this.

### DR-009-007 — Engine outputs are semantic artifacts, not proof text

Engine outputs must not contain Lean proof text, tactic scripts, target-specific theorem names used for proof generation, or proof-region replacement text.

Allowed engine output kinds:

```text
Full2DSyntheticTrace
AuxiliaryConstructionFull2D
AlgebraicCertificateFull2D
MetricAngleTraceFull2D
OrderCaseCoverageFull2D
InequalityCertificateFull2D
TransformationTraceFull2D
LeanSearchHintFull2D
PortfolioDecisionFull2D
```

Each output must be a semantic artifact whose payload is a deterministic function of `ClaimSpec`, engine configuration, and allowed resources. It must not be a function of `task_id`, `template_id`, or benchmark labels.

### DR-009-008 — Baselines must be comparable

Required baselines:

```text
B1: no geometry solver / proof-worker-only baseline
B2: full solver portfolio
B5: construction disabled
B6: algebraic/metric certificate disabled
B7: order/case disabled
```

Conditional baseline:

```text
B8: model-disabled baseline, required only if the selected ModelProviderSet enables a model for strategy, construction, proof search, or proof repair.
```

All baselines must share source corpus, extraction, ProofWorker, FinalVerifyGate, Lean library access, source theorem visibility, resource class, and model provider set except for the single declared disabled component. If no model provider is enabled, B8 is omitted and the release report must mark B8 as `not_applicable_model_provider_not_used`.

### DR-009-009 — Continue-on-debt, but no false closure

Codex stops only for HardBlockers. ReleaseBlockers and WorkDebt must be logged and work continues on independent tasks. Final release fails if any ReleaseBlocker, WorkDebt, evidence inconsistency, or open debt ledger entry remains.

## 3. Target and architecture

### 3.1 Target

The single proof target is:

```text
MathAutoResearch.GeometryFull2D
GeometryFull2DTarget:1.0.0
```

It may use admitted LeanGeo and Mathlib dependencies. Release benchmark statements must be expressed in the facade grammar and extracted through the v0.4.4 extraction path.

Forbidden target semantics:

```lean
def Point := Unit
def collinear ... := True
axiom geometry_solver_sound : ...
axiom every_geometry_goal_true : ...
structure Transformation where
  predicate : Prop
  evidence : predicate
```

Facade structures may contain bookkeeping fields only if counted theorem proofs do not rely primarily on field projection as the geometric proof.

### 3.2 Base pipeline

Base must remain domain-neutral and provide:

```text
ArtifactStore
RunLogger
PluginRegistry
SchemaRegistry
ProofStateDAG kernel
GraphPatch / DAGWriter
TrustGuard
FinalVerifyGate
ModelProviderSet
ResourceGovernor
ReplayVerifier
ReleaseAcceptanceRunner
```

Base may access `plugins/geometry_full2d` only through plugin registry and public capability contracts.

### 3.3 Canonical plugin

The only release plugin is:

```text
plugins/geometry_full2d
```

`plugins/geometry_synthetic` and all v0.3/v0.4.2 compatibility code are forbidden in v0.4.4 release commands.

## 4. Corpus requirements

### 4.1 Release corpus floors

The release corpus must include at least:

```text
positive formal Lean tasks: >= 3350
negative / target-outside / malformed tasks: >= 500
ExternalGoalPreserved positives: >= 700
SealedSolverChallenge positives: >= 1200
UserReviewedGoal positives: no fixed floor; if present, they must be reviewed
ProjectionNonCounted positives counted as release positives: 0
near-duplicate positives: <= 10%
exact target-shape duplicate max per theorem family: <= 5
```

The sum of family floors below is the effective positive floor. Codex must not satisfy the corpus by repeating target-equivalent tasks with renamed variables.

### 4.2 Required positive family floors

```text
Full2DCore500: >= 500
IncidenceParallelPerp350: >= 350
AngleCyclic450: >= 450
Construction450: >= 450
MetricRatioArea350: >= 350
Transformation250: >= 250
OrderCase250: >= 250
Algebraic250: >= 250
Inequality150: >= 150
OlympiadStyle300: >= 300
HardHoldout50: >= 50
```

### 4.3 ExternalGoalPreserved

Each ExternalGoalPreserved task must have:

```yaml
GoalPreservationReportV1:
  source_id: "..."
  source_kind: "Lean | LeanGeoBench | NewclidJGEX | GenesisGeoDSL | other formal DSL"
  source_goal_hash: "sha256:..."
  source_hypotheses_hash: "sha256:..."
  translated_theorem_hash: "sha256:..."
  preservation_kind: "exact_same_formal_goal | structurally_preserved_by_reviewed_translator | formally_equivalent | projection_not_counted"
  preservation_evidence_ref: "sha256:..."
  translator_id: "..."
  translator_code_hash: "sha256:..."
  source_goal_predicate_family: "..."
  translated_goal_predicate_family: "..."
  unsupported_losses: []
  added_hypotheses: []
  dropped_hypotheses: []
  simplified_goal: false
```

Counted preservation kinds:

```text
exact_same_formal_goal
structurally_preserved_by_reviewed_translator
formally_equivalent
```

`structurally_preserved_by_reviewed_translator` is allowed for formal DSL sources only when the source contains an explicit goal and the translator preserves the goal predicate family, mapped goal arguments, and required source hypotheses. It is not allowed for projection obligations that choose an easier target.

`projection_not_counted` is allowed for development and regression only. It does not count toward corpus floors, success rates, or advantage metrics.

### 4.4 UserReviewedGoal

UserReviewedGoal is optional for release floors. If used, each task must have:

```yaml
ReviewManifestV1:
  reviewer: "user | named_reviewer"
  review_date: "..."
  theorem_hash: "sha256:..."
  status: "approved_for_release"
  notes: "..."
```

Codex may prepare candidate tasks but cannot mark them reviewed.

### 4.5 SealedSolverChallenge

SealedSolverChallenge tasks must have:

```yaml
SealedChallengeManifestV1:
  seal_id: "..."
  generator_id: "..."
  generator_code_hash: "sha256:..."
  candidate_implementation_hash_before_seal: "sha256:..."
  generated_task_manifest_hash: "sha256:..."
  proof_text_visible_to_compiler: false
  compiler_private_label_access: false
  source_goal_projection_only: false
```

A final release run is valid only if the selected implementation hash matches the latest sealed challenge manifest. If code changes after sealing, Codex must regenerate or revalidate sealed challenges. This is a ReleaseBlocker, not a HardBlocker.

### 4.6 Source theorem hygiene

Positive release Lean files must contain theorem statements with a MARP proof region containing only `sorry` before the pipeline run.

Forbidden inside counted theorem bodies before pipeline execution:

```lean
exact ...
apply ...
constructor
rfl
trivial
simp
have h : ... := ...
```

Existing external source proofs may be stored separately as source evidence, but the counted release source theorem must be sorry-only.

## 5. Structured extraction

Release extraction must be per theorem and Lean-side / elaborator-backed.

Required report:

```yaml
LeanExtractionReportFull2D:
  report_id: "sha256:..."
  source_file_ref: "sha256:..."
  theorem_name: "..."
  source_statement_hash: "sha256:..."
  elaborated_expr_hash: "sha256:..."
  canonical_statement: CanonicalGeometryStatementV1
  target_classification: TargetClassification
  extraction_method: "lean_elaborator_backed"
  regex_used_for_semantics: false
  dropped_assumptions: []
  proof_region_initial_status: "sorry_only"
```

Release checker rejects smoke-only extraction, hand-written extraction JSON unrelated to the theorem, Python semantic classification, stale extraction caches, or source hash mismatch.

## 6. Provider and engine contracts

### 6.1 Provider request

```python
GeometryFull2DProvider.solve(request: GeometryFull2DSolveRequest) -> GeometryFull2DProviderRun
```

Required request fields:

```yaml
request_id: "..."
task_id: "..."
baseline_id: "..."
claim_spec_ref: "sha256:..."
claim_spec: GeometryFull2DClaimSpecV2
target_library: "GeometryFull2DTarget:1.0.0"
release_mode: true
```

### 6.2 Engine roles

Release-critical engine roles:

```text
synthetic_closure
construction_search
algebraic_geometry
metric_angle
transformation
order_case
inequality
lean_proof_search
portfolio_coordinator
```

### 6.3 EngineOutputFull2D

```yaml
EngineOutputFull2D:
  engine_output_ref: "sha256:..."
  engine_role: "..."
  backend_identity: "..."
  backend_code_hash: "sha256:..."
  input_ref: "sha256:..."
  raw_output_hash: "sha256:..."
  normalized_output_ref: "sha256:... | null"
  normalized_output_payload_ref: "sha256:... | null"
  checker_or_compiler_ref: "sha256:... | null"
  resource_usage_ref: "sha256:..."
  real_integration_flag: true
  real_integration_evidence_ref: "sha256:..."
  fixture_flag: false
  status: "normalized_success | measured_failure | diagnostic"
  proof_use_status: "not_allowed"
```

### 6.4 Real execution evidence

Each normalized success must include evidence of one of:

```text
external_backend_run
internal_algorithm_run
lean_verified_run
```

A real run must be reproducible from input hash, code hash, engine config hash, and resource budget. Self-attesting `real_integration_flag=true` is release-failing.

### 6.5 Engine challenge suite

Each engine must pass a nontrivial challenge suite independent of the release corpus:

```text
synthetic_closure: 50 challenge goals, >= 30 normalized_success; multi-step incidence/parallel/cyclic closure, not reflexivity only
construction_search: 50 challenge goals, >= 25 normalized_success; auxiliary object is necessary
algebraic_geometry: 30 challenge goals, >= 15 normalized_success; nontrivial polynomial/certificate, not duplicate-row only
metric_angle: 40 challenge goals, >= 20 normalized_success; multi-step directed-angle relation, not reflexivity/symmetry only
transformation: 30 challenge goals, >= 10 normalized_success; genuine transformation invariant, not identity/evidence-field projection only
order_case: 30 challenge goals, >= 15 normalized_success; actual case split/coverage artifact
inequality: 30 challenge goals, >= 10 normalized_success; nontrivial inequality/certificate, not reflexivity/transitivity only
lean_proof_search: 50 challenge goals, >= 25 normalized_success; Lean repair using generated nontrivial lemmas
portfolio_coordinator: all challenge families with correct reason codes and fallback behavior
```

## 7. Compiler contracts

Release compilers must consume normalized solver artifacts. They may not infer proof solely from target shape.

A CompilerResultFull2D must include:

```yaml
compiler_result_ref: "sha256:..."
compiler_id: "..."
consumed_engine_output_refs: ["sha256:..."]
consumed_normalized_output_refs: ["sha256:..."]
consumed_rule_ids: ["..."]
proof_derivation_input_refs: ["sha256:..."]
proof_derivation_witnesses: [...]
generated_obligations: [...]
side_condition_report_ref: "sha256:..."
status: "compiled_patch | measured_failure"
```

### 7.1 Solver causality mutation test

Every counted B2 final theorem success must have:

```yaml
SolverCausalityReportV1:
  task_id: "..."
  baseline_id: "B2"
  original_patch_ref: "sha256:..."
  selected_normalized_solver_artifact_refs: ["sha256:..."]
  mutation_cases:
    - mutation_kind: "remove_selected_normalized_output"
      expected: "compiler_fails_or_patch_changes"
      observed: "..."
    - mutation_kind: "change_selected_rule_fact"
      expected: "compiler_fails_or_patch_changes"
      observed: "..."
    - mutation_kind: "replace_engine_output_with_same_shape_wrong_fact"
      expected: "final_verify_fails_or_certificate_rejected"
      observed: "..."
  status: "passed"
```

### 7.2 Non-target intermediate facts

A solver intermediate counts as substantive only if it is one of:

```text
distinct solver-derived fact not syntactically equal to target
auxiliary construction used in proof
case split / coverage result
checked algebraic / metric / inequality certificate conclusion
side-condition discharge used by a later proof step
```

This does not count:

```lean
have h_solver_intermediate : target := by
  exact some_facade_lemma ...
exact h_solver_intermediate
```

## 8. Proof worker, FinalVerifyGate, and certificates

ProofWorker may apply a LeanPatchCandidate but cannot claim a final theorem.

FinalVerifyGate must compile the generated candidate file and verify:

```text
theorem statement hash unchanged
only MARP proof region changed
no sorry
no forbidden axioms
no toy target semantics
admitted imports only
proof-use provenance valid
solver causality report bound
```

SolverBackedProofCertificateFull2D must bind:

```text
source_theorem_ref
lean_extraction_report_ref
claim_spec_ref
provider_run_manifest_ref
engine_output_refs
compiler_result_refs
lean_patch_candidate_ref
proof_worker_result_ref
final_verify_report_ref
solver_causality_report_ref
checked_candidate_file_ref
causal_chain_hash
```

## 9. Metrics and thresholds

### 9.1 Final theorem rates

Thresholds apply only to admissible non-projection corpus tasks:

```text
Overall B2 positive final theorem rate >= 0.85
Full2DCore500 >= 0.95
IncidenceParallelPerp350 >= 0.92
AngleCyclic450 >= 0.90
Construction450 >= 0.85
MetricRatioArea350 >= 0.85
Transformation250 >= 0.75
OrderCase250 >= 0.80
Algebraic250 >= 0.85
Inequality150 >= 0.75
OlympiadStyle300 >= 0.70
HardHoldout50 >= 0.50
```

### 9.2 Advantage thresholds

```text
B2 - B1 overall >= 0.25
B2 - B5 construction subset >= 0.15
B2 - B6 algebraic/metric subset >= 0.15
B2 - B7 order/case subset >= 0.10
B2 - B8 model-disabled olympiad subset >= 0.05, only when B8 is required
```

### 9.3 Substantive success floors

For B2 counted successes:

```text
direct_or_wrapped_facade_lemma_success_fraction <= 0.10
solver_causal_success_fraction = 1.00
non_target_intermediate_fact_success_fraction >= 0.50
construction_or_case_or_certificate_success_fraction >= 0.50
ExternalGoalPreserved_success_count >= 500
SealedSolverChallenge_success_count >= 700
```

`solver_causal_success_fraction` is measured over counted B2 positive final theorem successes. Because every counted B2 positive final theorem success requires a passing `SolverCausalityReportV1`, any value below `1.00` is release-failing.

### 9.4 Used-rule coverage thresholds

B2 counted successes must meet:

```text
used concrete rules >= 35
used rule families >= 15
non-incidence families >= 8
construction families >= 4
algebraic/metric/angle families >= 3
order/case families >= 2
transformation families >= 2
```

Rules count only if certificate-bound, compiler-consumed, mutation-sensitive, and final-theorem successful.

## 10. Release report requirements

The release report must contain nonempty:

```text
checked_rids
freshness_summary
family_floor_summary
metrics_summary
advantage_summary
used_rule_coverage_summary
engine_usage_summary
engine_contribution_summary
measured_failure_summary
corpus_summary
actual_pipeline_run_summary
solver_causality_summary
corpus_goal_preservation_summary
challenge_suite_summary
baseline_comparability_summary
regression_failure_summary
debt_ledger_summary
```

Empty placeholder summary is release-failing.

`checked_rids` must contain concrete checked requirement identifiers from this authority set, including applicable `DR-009-*`, `I-*`, `K-*`, and Plan work-package acceptance gates. Synthetic, undefined, or non-authority identifiers do not satisfy this field.

`freshness_summary` must bind every reused checker, matrix, corpus, and release-evidence artifact to the current repository tree or selected implementation hash, corpus hash, config hash, run directory hash, and checker code hash as applicable. Stale v0.4.2/v0.4.3 outputs, stale v0.4.4 outputs, or unbound sidecar reports cannot satisfy release acceptance.

`family_floor_summary` must report each positive family floor from section 4.2 and fail release acceptance if any family is below its floor.

## 11. Required regression failures

Release must include tests proving that each of the following fails:

```text
v0.4.2 proof artifact overlay matrix
v0.4.3 projection-only corpus counted as external
compiler reads template_id
compiler reads task_id
compiler reads theorem_family
compiler reads grammar_family
compiler reads provenance, source_ref, or generator private labels
compiler succeeds after selected engine artifact removal
compiler succeeds after selected engine fact mutation
engine emits proof text
engine output generated from task_id hash
renamed/shimmed v0.4.3 release path accepted as v0.4.4
stale checker, matrix, corpus, or release output accepted without current hash binding
source theorem already proved
single smoke extraction reused for corpus
open DebtLedger entry ignored by release
UserReviewedGoal counted without ReviewManifestV1
B8 required even when no model provider is enabled
B8 omitted when model provider is enabled
```

## 12. HardBlocker policy

Codex stops only for:

```text
HB-01 active approved specs conflict
HB-02 implementation would require changing Base/Acceptance thresholds
HB-03 destructive operation outside refactor scope
HB-04 dependency license prohibits use
HB-05 required private credential/model and no allowed substitute exists
HB-06 unspecified mathematical semantics with incompatible choices
HB-07 unsound proof-use path cannot be isolated
HB-08 Lean cannot run after bootstrap attempts
HB-09 Guardian source of truth cannot be determined
```

Everything else is ReleaseBlocker or WorkDebt. Continue unrelated work.

## 13. Closure rules

Closure may claim `V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY` only if final release acceptance passes with:

```text
hard_blockers = []
release_blockers = []
work_debt_open = []
all corpus floors pass
all final theorem thresholds pass
all solver-causality checks pass
all regression-failure tests pass
```

Closure must not claim natural-language fidelity, open-problem solving, TongGeometry model-backed readiness, production safety, or correctness outside GeometryFull2DTarget unless separate approved specs and evidence exist.
