---
title: "Guardian Base Spec — GeometryFull2D v0.4.5 Real Solver-Causal Full Pipeline"
spec_id: "MARP-GEOLEAN-BASE-010"
status: "USER_APPROVED_ACTIVE"
target_repo: "kabatan/baka_proof"
revision: "reviewed-2026-06-18-no-shortcuts"
supersedes_when_approved:
  - "MARP-GEOLEAN-BASE-009"
claim_target: "V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
authority_model: "After user approval, this document is the only Base Spec authority for the v0.4.5 change. v0.4.4 and older reports, scripts, corpus, and closure are regression evidence only and cannot weaken this spec."
---

# Guardian Base Spec — GeometryFull2D v0.4.5 Real Solver-Causal Full Pipeline

## 0. Purpose

v0.4.5 exists because v0.4.4 still allowed a checker-passing implementation whose proof generation was effectively:

```text
fixed theorem/target shape
  -> fixed Lean lemma proof text
  -> synthesized engine output and causality artifacts
  -> family-coded baseline outcomes
  -> release metrics
```

That is not the intended automated proving pipeline. v0.4.5 requires a real solver-causal pipeline.

The only allowed final claim is:

```text
V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```

This claim means:

```text
For counted GeometryFull2DTarget:1.0.0 formal 2D Euclidean geometry tasks,
the repository runs a real solver-causal pipeline in which solver artifacts are
produced before proof generation, contain theorem-specific mathematical facts,
constructions, side-condition certificates, or algebraic/order/case certificates,
are consumed by the compiler, are necessary for the produced patch, and are
verified by destructive reruns.
```

Final release is all-or-nothing. Work may continue with ReleaseBlockers recorded in DebtLedger, but closure is forbidden until all release blockers, work debts, stale-evidence problems, regression failures, and non-causal proof-generation paths are closed.

## 1. Non-negotiable decisions

### DR-010-001 — Prior closures are negative evidence only

The v0.4.4 `CLOSURE.md`, `release_acceptance_report.json`, generated corpus, generated run records, and generated causality reports are evidence of failure modes to prevent. They may not be used as release success evidence.

### DR-010-002 — Actual solver causality is required, not causality fields

A `SolverCausalityReportV2` is valid only if it records destructive reruns performed by executing the release compiler/proof-worker/final-verifier against mutated solver artifact sets.

Required destructive reruns for every counted B2 success:

```text
positive_control:
  Re-run compiler, ProofWorker, and FinalVerifyGate with the original selected solver artifacts.
  Expected: same patch hash and final theorem.

delete_selected_solver_artifact:
  Remove the selected normalized solver artifact from compiler input.
  Expected: compiler failure OR different non-counted patch OR final theorem not allowed.

corrupt_selected_solver_fact:
  Modify at least one selected solver fact conclusion, construction target, certificate payload, or side condition.
  Expected: compiler failure OR different non-counted patch OR final theorem not allowed.

unsupported_rule_mutation:
  Replace at least one consumed solver rule id with an unsupported rule id.
  Expected: compiler failure OR non-counted result.

side_condition_mutation:
  Remove at least one consumed side condition, nondegeneracy condition, order/case condition, certificate, or generated obligation when applicable.
  Expected: compiler failure OR non-counted result.
```

A report that merely sets `solver_causal_necessity=true` or `mutation_sensitive=true` is invalid. A causality checker that only inspects these booleans is invalid.

### DR-010-003 — Proof text cannot be selected from target shape or corpus metadata

Release compiler/proof generation must not select proof text from:

```text
task_id
theorem_name, except for patch anchoring only
template_id
theorem_family
grammar_family
difficulty_tier
category
provenance
source_ref
projection_kind
target_shape_id
raw target source expression alone
fixed target-shape menus
```

Forbidden code patterns in release proof-decision paths include, but are not limited to:

```python
if target_expr.startswith(...): return "exact ..."
if theorem_family == ...: return ...
if baseline == "B2": final_status = "final_theorem"
if family in {...}: fail_or_pass_baseline(...)
_proof_from_shape(...)
_proof_from_source(...)
proof_text_for_template(...)
```

Allowed proof derivation inputs:

```text
GeometryFull2DClaimSpec for target matching only
SelectedSolverDerivationV1
SolverFactV1 / SolverConstructionV1 / SolverCertificateV1
RuleRegistryFull2D rule contracts
SideConditionCalculusFull2D results
Lean theorem statement for type checking and patch anchoring
```

The compiler may compare a solver artifact conclusion with the ClaimSpec target. It may not choose a proof strategy from the target expression without a matching solver artifact.

### DR-010-004 — Solver output must precede and determine proof generation

The release pipeline order is fixed:

```text
source theorem with sorry-only proof region
  -> Lean-side structured extraction
  -> ClaimSpec
  -> provider.solve
  -> EngineOutputFull2D with solver facts/constructions/certificates
  -> SelectedSolverDerivationV1
  -> compiler consumes selected solver artifacts
  -> LeanPatchCandidateFull2D
  -> ProofWorker patch application
  -> FinalVerifyGate
  -> SolverBackedProofCertificateFull2D
  -> SolverCausalityReportV2 destructive reruns
```

Any release path that computes proof text before producing normalized solver artifacts is invalid.

### DR-010-005 — Baseline outcome cannot be label-coded

The outcome of B1/B2/B5/B6/B7/B8 must be produced by running the same pipeline with only the declared component disabled.

Forbidden:

```python
if baseline == "B2": success
if family == "Construction450": fail B5
if theorem_family in {...}: fail B6
```

Baseline success/failure must arise from missing solver artifacts, missing construction candidates, missing algebraic/metric/angle/inequality certificates, missing order/case evidence, or missing model outputs in the actual compiler path.

### DR-010-006 — Projection tasks do not count

A task derived by projecting an external problem into a simpler obligation does not count as `ExternalGoalPreserved`.

Counted positive categories:

```text
ExternalGoalPreserved
SealedPostImplementationChallenge
UserReviewedGoal
```

Non-counted categories:

```text
ProjectionNonCounted
ProjectionDerivedSmoke
CompilerRegressionFixture
TargetOutside
Malformed
```

A task is a projection if it reuses only source points/predicates but replaces the original source goal with an easier obligation such as reflexivity, symmetry, midpoint-to-collinearity, a one-step facade lemma, or a goal selected because it is easy for the compiler.

### DR-010-007 — ExternalGoalPreserved requires machine-checkable goal preservation

For `ExternalGoalPreserved`, the release must include `GoalPreservationReportV2` generated by an independent checker, not by the corpus generator's self-declaration.

Valid preservation kinds:

```text
exact_same_formal_goal
formally_equivalent
structure_preserving_translation_with_machine_checked_mapping
```

Invalid:

```text
structurally_preserved_by_reviewed_translator without independent checker evidence
projection_not_counted
point_or_predicate_pool_reuse
easier_goal_derived_from_source
source_ref_only
```

The report must include `SourceGoalASTV1`, `TranslatedGoalASTV1`, a mapping table, and a checker proof or deterministic checker transcript. It must reject dropped hypotheses, unsupported losses, arity changes, predicate-family changes without formal equivalence, and target simplification.

If an external source is unavailable or insufficient after reproducible discovery, Codex must record `ExternalSourceAvailabilityReportV1`. The ExternalGoalPreserved floor may then be reduced only by the number of unavailable tasks and the deficit must be replaced by additional `SealedPostImplementationChallenge` tasks. This prevents environment/source availability from becoming a nonessential HardBlocker while preserving the total counted corpus and challenge strength.

### DR-010-008 — Sealed challenges are independent of the compiler

A `SealedPostImplementationChallenge` is valid only if:

```text
- generated after provider/compiler/rule-registry code hash freeze;
- generated by a script that imports no provider, compiler, rule registry, proof worker, matrix, or release checker code;
- generated from a declarative challenge grammar defined in this Base Spec or a checked grammar file;
- contains no proof text, expected proof lemma, template proof label, expected engine role, or expected rule ids;
- stores only theorem statements with sorry-only proof regions;
- any provider/compiler/rule-registry change after sealing invalidates the seal.
```

If the code changes after sealing, the challenge becomes stale. That is a ReleaseBlocker but not a HardBlocker.

### DR-010-009 — Direct/facade lemma successes are sharply limited

Direct or wrapped facade lemma successes include:

```text
exact lemma
have h : target := by exact lemma ...; exact h
one-step facade theorem matching the target
field-evidence projection
proof using only source hypotheses and one facade lemma without a solver-derived intermediate fact
```

These may account for at most 5% of B2 counted positive final theorem successes. They cannot be counted as solver-intermediate successes.

### DR-010-010 — Full target remains broad

v0.4.5 does not reduce the target to a small smoke scope. `GeometryFull2DTarget:1.0.0` remains the release target. In-target positive tasks may fail honestly as measured failures during development, but final release thresholds must be met without safe-rejecting in-target positives.

## 2. Required architecture

### 2.1 Base pipeline

Base remains domain-neutral and must provide:

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

Base must not import domain-specific implementation internals except through plugin registry contracts.

### 2.2 Canonical release plugin

The only release plugin is:

```text
plugins/geometry_full2d
```

`plugins/geometry_synthetic` and old v0.4.2/v0.4.3/v0.4.4 compatibility paths may remain only as regression fixtures. They must not be imported by release entrypoints.

## 3. Target language

The target remains:

```text
MathAutoResearch.GeometryFull2D
GeometryFull2DTarget:1.0.0
```

Required families include:

```text
incidence, collinearity, concurrency, concyclicity,
parallel, perpendicular, tangent, radical axis, power of point,
metric length, ratio, area,
directed angle mod pi / mod 2pi,
triangle congruence/similarity/centers,
order, betweenness, same-side/opposite-side, orientation,
reflection, rotation, homothety, inversion, spiral similarity,
inequality and domain conditions,
logical conjunction/disjunction/existential construction/finite case split.
```

The facade may use LeanGeo and Mathlib dependencies, but counted theorems must be expressed through the facade grammar and extracted by the v0.4.5 extraction path.

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

A facade structure may contain evidence fields only for bookkeeping; counted geometry success must not be obtained by merely extracting stored evidence.

## 4. Counted task requirements

### 4.1 Corpus floors

Release corpus must include:

```text
positive formal Lean tasks >= 3350
negative / target-outside / malformed tasks >= 500
ExternalGoalPreserved positives >= min(700, available_external_goal_preserved_count_after_discovery)
SealedPostImplementationChallenge positives >= 1200 + external_goal_preserved_deficit
ProjectionNonCounted counted positives = 0
near duplicate positives <= 10%
exact target-shape duplicate max per theorem family <= 5
logical proof-schema duplicate max per theorem family <= 5
one-step facade-lemma theorem fraction <= 0.05
```

UserReviewedGoal has no required floor. If present, every such task must have a valid `ReviewManifestV1`.

### 4.2 Positive families

Required family floors:

```text
Full2DCore500 >= 500
IncidenceParallelPerp350 >= 350
AngleCyclic450 >= 450
Construction450 >= 450
MetricRatioArea350 >= 350
Transformation250 >= 250
OrderCase250 >= 250
Algebraic250 >= 250
Inequality150 >= 150
OlympiadStyle300 >= 300
HardHoldout50 >= 50
```

### 4.3 No proof-coupled corpus generation

A counted corpus generator must not encode proof lemma, expected proof text, expected compiler rule, expected engine role, expected solver artifact, or expected baseline outcome.

Forbidden in counted-corpus generation:

```text
FAMILY -> proof template mapping
target_shape -> exact lemma mapping
theorem source whose goal is chosen only because a known facade lemma closes it
source_ref from external file but goal not preserved
private label that compiler or solver can read to choose proof strategy
```

### 4.4 Sealed challenge grammar

The sealed challenge generator must draw tasks from a declarative grammar file checked into `benchmarks/geometry_full2d_v0_4_5/metadata/sealed_challenge_grammar.json`. The grammar must specify target relation families and allowed constructors, but must not specify proof lemmas, expected rules, or engine roles. The checker must reject challenge tasks whose theorem statement can be solved by a single facade lemma unless the total direct/facade fraction remains under the global ceiling.

## 5. Artifact contracts

### 5.1 ActualTaskPipelineRunV3

Every counted positive result must have:

```yaml
ActualTaskPipelineRunV3:
  schema_version: "ActualTaskPipelineRunV3"
  run_id: "actual_full2d_run:v0_4_5:..."
  task_id: "..."
  baseline_id: "B1 | B2 | B5 | B6 | B7 | B8"
  corpus_manifest_hash: "sha256:..."
  config_hash: "sha256:..."
  repo_tree_hash: "sha256:..."
  selected_implementation_hash: "sha256:..."
  source_theorem_ref: "sha256:..."
  lean_extraction_report_ref: "sha256:..."
  claim_spec_ref: "sha256:..."
  provider_run_manifest_ref: "sha256:..."
  engine_output_refs: ["sha256:..."]
  selected_solver_derivation_ref: "sha256:..."
  compiler_result_refs: ["sha256:..."]
  lean_patch_candidate_ref: "sha256:..."
  proof_worker_result_ref: "sha256:..."
  generated_candidate_file_ref: "sha256:..."
  final_verify_report_ref: "sha256:..."
  solver_causality_report_ref: "sha256:..."
  solver_backed_certificate_ref: "sha256:..."
  causal_chain_hash: "sha256:..."
  final_status: "final_theorem | measured_failure"
```

All referenced artifacts must exist, be content-addressed, and hash-verified.

### 5.2 EngineOutputFull2D

```yaml
EngineOutputFull2D:
  schema_version: "EngineOutputFull2D"
  engine_role: "synthetic_closure | construction_search | algebraic_geometry | metric_angle | transformation | order_case | inequality | lean_proof_search | portfolio_coordinator"
  backend_identity: "..."
  backend_code_hash: "sha256:..."
  input_claim_spec_ref: "sha256:..."
  input_claim_spec_hash: "sha256:..."
  raw_output_hash: "sha256:..."
  normalized_output_ref: "sha256:... | null"
  normalized_output_payload:
    facts: []
    constructions: []
    certificates: []
    solver_steps: []
  real_integration_evidence_ref: "sha256:..."
  fixture_flag: false
  proof_use_status: "not_allowed"
```

The normalized payload must not contain Lean proof text, tactic scripts, theorem names used for proof generation, benchmark metadata, or proof replacement text. It must contain at least one fact, construction, certificate, or solver step for `normalized_success`.

Every normalized fact/construction/certificate must be independently checkable. An engine assertion of the target conclusion is invalid unless it includes either a checked rule-step trace from premises, a construction/existence certificate, an algebraic/metric/order certificate, or a Lean-verified checker artifact. A target fact with no independent checker evidence is a ReleaseBlocker.

The provider/engine implementation must not import release compiler or proof-generation modules. Engine outputs must be generated by provider/engine code before compiler code is called.

### 5.3 Solver fact/construction/certificate schema

A solver fact must include:

```yaml
SolverFactV1:
  fact_id: "sha256:..."
  predicate_family: "..."
  args: [...]
  conclusion: {...}
  premises: [...]
  rule_id: "..."
  side_conditions: [...]
  certificate_ref: "sha256:... | null"
```

A solver construction must include introduced object, construction kind, dependencies, existence/uniqueness side conditions, and generated Lean obligations.

A compiler may only select Lean templates by `rule_id` present in consumed solver facts/constructions/certificates.

Each consumed solver fact/certificate must have `checker_status: passed` and a checker artifact whose input hash matches the fact/certificate payload.

### 5.4 SelectedSolverDerivationV1

Before proof generation, the provider/compiler boundary must produce:

```yaml
SelectedSolverDerivationV1:
  derivation_ref: "sha256:..."
  claim_spec_ref: "sha256:..."
  selected_engine_output_refs: ["sha256:..."]
  selected_fact_ids: ["sha256:..."]
  selected_construction_ids: ["sha256:..."]
  selected_certificate_refs: ["sha256:..."]
  selected_rule_ids: ["..."]
  target_match_status: "exact_target | sufficient_for_target"
  intermediate_fact_refs: ["sha256:..."]
  side_condition_refs: ["sha256:..."]
```

This artifact is invalid if it can be constructed from ClaimSpec alone.

### 5.5 CompilerResultFull2D

A compiler result must include:

```yaml
CompilerResultFull2D:
  compiler_result_ref: "sha256:..."
  selected_solver_derivation_ref: "sha256:..."
  consumed_engine_output_refs: ["sha256:..."]
  consumed_solver_fact_ids: ["sha256:..."]
  consumed_construction_ids: ["sha256:..."]
  consumed_certificate_refs: ["sha256:..."]
  consumed_rule_ids: ["..."]
  generated_obligations: [...]
  side_condition_report_ref: "sha256:..."
  proof_derivation_input_refs: ["sha256:..."]
  proof_derivation_ref: "sha256:..."
  lean_patch_candidate_ref: "sha256:... | null"
  status: "compiled_patch | measured_failure"
```

A compiler result is invalid if it lacks consumed solver facts/constructions/certificates for a counted final theorem.

### 5.6 SolverCausalityReportV2

```yaml
SolverCausalityReportV2:
  schema_version: "SolverCausalityReportV2"
  task_id: "..."
  baseline_id: "..."
  original_patch_ref: "sha256:..."
  selected_solver_derivation_ref: "sha256:..."
  selected_solver_artifact_refs: ["sha256:..."]
  positive_control:
    status: "passed"
    patch_ref: "sha256:..."
    final_verify_status: "final_theorem"
  destructive_tests:
    - test_kind: "delete_selected_solver_artifact"
      status: "failed_as_expected"
      observed_patch_ref: "sha256:... | null"
      observed_final_verify_status: "not_allowed | failed | null"
    - test_kind: "corrupt_selected_solver_fact"
      status: "failed_as_expected"
    - test_kind: "unsupported_rule_mutation"
      status: "failed_as_expected"
    - test_kind: "side_condition_mutation"
      status: "failed_as_expected | not_applicable_no_side_condition"
  solver_causal_necessity: true
  mutation_sensitive: true
  direct_or_wrapped_facade_lemma: false
```

The report must be generated by actual reruns, not field assignment. The checker must verify rerun artifacts, mutated artifact hashes, compiler outputs, and FinalVerifyGate outcomes.

## 6. Baselines

Required baselines unless model provider is enabled:

```text
B1: no geometry solver provider; same ProofWorker, FinalVerifyGate, corpus, resources.
B2: full geometry solver portfolio.
B5: construction engine disabled only.
B6: algebraic/metric/angle/inequality engines disabled only.
B7: order/case engine disabled only.
```

B8 is conditional:

```text
If ModelProviderSet includes a model slot used by the controller/worker, B8 is required.
If no model provider is used, B8 is not applicable and release report must say:
not_applicable_model_provider_not_used.
```

Baseline success/failure must arise from the disabled component's missing artifacts. It must not be computed from theorem family labels.

## 7. Metrics and thresholds

B2 release thresholds:

```text
overall final theorem rate >= 0.85
Full2DCore500 >= 0.95
IncidenceParallelPerp350 >= 0.90
AngleCyclic450 >= 0.85
Construction450 >= 0.80
MetricRatioArea350 >= 0.80
Transformation250 >= 0.70
OrderCase250 >= 0.75
Algebraic250 >= 0.80
Inequality150 >= 0.70
OlympiadStyle300 >= 0.60
HardHoldout50 >= 0.40
solver_causal_success_fraction = 1.00 for counted B2 successes
destructive_rerun_success_fraction = 1.00 for counted B2 successes
direct_or_wrapped_facade_lemma_success_fraction <= 0.05
non_target_intermediate_fact_success_fraction >= 0.50
construction_or_case_or_certificate_success_fraction >= 0.50
ExternalGoalPreserved_success_count >= min(500, admitted_external_goal_preserved_count)
SealedPostImplementationChallenge_success_count >= 700 + external_success_deficit
```

Advantage thresholds:

```text
B2 - B1 overall >= 0.25
B2 - B5 construction subset >= 0.15
B2 - B6 algebraic/metric/angle/inequality subset >= 0.15
B2 - B7 order/case subset >= 0.10
B2 - B8 model-disabled olympiad subset >= 0.05, only when B8 is required
```

## 8. Release report requirements

The release report must include nonempty:

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
mutation_rerun_summary
proof_from_shape_static_analysis_summary
selected_solver_derivation_summary
external_source_availability_summary
```

## 9. Required failure regressions

Release must prove these fail:

```text
v0.4.2 sidecar overlay matrix
v0.4.3 external projection corpus counted as external goal preserved
v0.4.4 target-shape proof synthesis
solver causality report generated by field assignment only
family-coded baseline outcome
engine output containing proof text
compiler selecting proof from target shape without solver facts
source theorem already proved
projection task counted as positive
stale sealed challenge after compiler code change
selected solver derivation constructed from ClaimSpec alone
mutation rerun checker that only reads booleans
engine emits unchecked target fact with no rule trace/certificate/checker artifact
provider/engine imports compiler or proof-generation code
```

## 10. HardBlocker / ReleaseBlocker policy

HardBlocker: stop and report.

```text
spec conflict
unsafe destructive repo operation
license/legal conflict
need for a mathematical semantics choice not specified here
impossible dependency setup after reproducible bootstrap attempts
```

ReleaseBlocker: record in DebtLedger and continue other work.

```text
threshold failure
missing corpus task
missing engine contribution
causality mutation failure
challenge stale after code change
goal preservation failure
acceptance checker failure
```

MeasuredFailure: benchmark task failed honestly. Count in metrics; not a blocker by itself.

## 11. Completion rule

The repository may claim `V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` only when:

```text
release_acceptance.status == passed
closure_allowed == true
hard_blockers == []
release_blockers == []
work_debt_open == []
all required summaries are nonempty
all destructive causality tests pass
no forbidden shortcut appears in release path
```
