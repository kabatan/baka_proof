---
title: "Guardian Base Spec — Geometry × Lean Full2D Real Pipeline Recovery v0.4.3 Integrated"
spec_id: "MARP-GEOLEAN-BASE-008"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-009"
target_repo: "kabatan/baka_proof"
created: "2026-06-15"
supersedes_when_approved:
  - "MARP-GEOLEAN-BASE-007"
claim_target: "V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY"
authority_model: "After approval, this Base Spec is the only source of truth. Existing v0.4.2 code, checkers, reports, and docs are evidence only; they are not allowed to weaken this spec."
---

# Guardian Base Spec — Geometry × Lean Full2D Real Pipeline Recovery v0.4.3 Integrated

## 0. Purpose and failure being corrected

This Base Spec supersedes the current v0.4.2 Full2D implementation target after user approval. It exists because the prior implementation passed a formal release checker while failing the intended full-prover meaning.

The failure mode to eliminate is:

```text
synthetic/generated corpus
  -> template_id selects a hard-coded Lean proof replacement
  -> fabricated normalized solver reference
  -> FinalVerifyGate compiles the patch
  -> matrix counts final theorem from overlay artifacts
  -> release report claims full prover readiness
```

v0.4.3 does not allow this path. The only admitted completion claim is:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
```

This document already includes the anti-gaming hardening that was previously considered as a separate addendum. There is no separate v0.4.3A authority document; all anti-gaming requirements are part of `MARP-GEOLEAN-BASE-008` itself.

This claim means:

```text
For the approved GeometryFull2DTarget:1.0.0 formal 2D Euclidean geometry target language, the repository executes a real solver-backed proving pipeline per counted positive theorem:

Lean theorem source
  -> Lean-side structured extraction for that exact theorem
  -> GeometryFull2DClaimSpec
  -> GeometryFull2DProvider.solve actual run
  -> engine outputs with real run evidence
  -> compiler output derived from actual normalized solver artifact
  -> LeanPatchCandidateFull2D
  -> ProofWorker patch application
  -> FinalVerifyGate on generated candidate
  -> SolverBackedProofCertificateFull2D binding every previous artifact
  -> artifact-derived metrics and advantage reports.

No in-target positive theorem may be counted by safe reject, by template label, by proof-artifact overlay alone, by a pre-proved source theorem, by fabricated solver refs, or by proof patches that bypass provider and compiler output.
```

The final claim remains all-or-nothing. Progress may continue with debt, but final release cannot pass while any release blocker, work debt, evidence inconsistency, or open debt ledger item remains.

## 1. Non-negotiable decisions

### DR-008-001 — v0.4.2 acceptance is not sufficient evidence

The existing v0.4.2 `release_acceptance_report.json`, synthetic corpus, proof artifact batch, and release status are not valid proof of v0.4.3 completion. They may be used only as negative evidence and regression targets.

Codex must not reuse v0.4.2's release-passing path as a completion path.

### DR-008-002 — No template-backed final theorem counting

A theorem is not solver-backed merely because its `template_id` maps to a Lean proof snippet.

Forbidden for release path:

```text
- selecting proof text directly from benchmark template_id;
- selecting proof text directly from theorem_family;
- fabricating normalized_solver_ref from task_id, theorem_name, or template_id;
- using proof artifact sidecar overlay without a corresponding actual provider run;
- counting a source theorem that already contains a proof;
- marking Codex-generated template tasks as human-curated evidence without explicit user/external review.
```

### DR-008-003 — Counted success requires ActualTaskPipelineRunV1

Every counted positive release success must have exactly one `ActualTaskPipelineRunV1` record.

Required chain:

```text
ActualTaskPipelineRunV1
  source_theorem_ref
  lean_extraction_report_ref
  claim_spec_ref
  provider_run_manifest_ref
  engine_output_refs
  compiler_result_refs
  lean_patch_candidate_ref
  proof_worker_result_ref
  final_verify_report_ref
  solver_backed_certificate_ref
```

The record must be content-addressed and replayable. Missing chain element = release failure.

### DR-008-004 — Matrix must execute or replay actual pipeline runs

`run_full2d_matrix.py` must not compute success from manifest labels or sidecar overlays alone.

Allowed matrix modes:

```text
execute:
  run the full pipeline for each task and baseline.

replay:
  replay previously recorded ActualTaskPipelineRunV1 records only if:
    - frozen corpus manifest hash matches;
    - config hash matches;
    - selected implementation hash matches;
    - repository tree hash or recorded code hash matches;
    - every artifact hash verifies;
    - every replayed task has a valid SolverBackedProofCertificateFull2D.
```

Anything else is not release evidence.

### DR-008-005 — Open DebtLedger entries block release

Final release acceptance must parse `docs/ai/changes/geometry-full2d-v0_4_3/debt/debt_ledger.jsonl`. Any entry with `status != closed` blocks release.

Release report fields must not be empty placeholders:

```text
metrics_summary != {}
advantage_summary != {}
used_rule_coverage_summary != {}
engine_usage_summary != {}
measured_failure_summary != {}
checked_rids != []
```

### DR-008-006 — Structured extraction must be per theorem, not smoke-only

Release extraction must run on each counted positive theorem or on a deterministic replay artifact generated from that exact theorem.

Forbidden:

```text
- a single fixed smokeStatement JSON used for all tasks;
- hand-written JSON unrelated to the theorem being counted;
- Python regex classification of theorem targets;
- Python fabrication of exact_goal relation;
- accepting in-target positive theorem without Lean-side extraction evidence.
```

### DR-008-007 — Real integration flag is not self-attested

An engine cannot prove `real_integration_flag=true` by setting a field.

Each engine record must include `real_integration_evidence_ref` that points to a verifier artifact proving one of:

```text
external_backend_run:
  command, version, input hash, output hash, resource usage, exit status.

internal_algorithm_run:
  algorithm identity, code hash, input hash, output hash, non-template challenge evidence, deterministic replay result.

lean_verified_run:
  Lean file/checker hash, theorem/checker name, lake env lean output, checked result hash.
```

For v0.4.3 release, local deterministic algorithms are allowed only if their output is a function of ClaimSpec / engine input, not of task_id / theorem_name / template_id.

### DR-008-008 — GeometryFull2DTarget remains full release target

The target remains `GeometryFull2DTarget:1.0.0`. The target language and proof target are not reduced.

In-target positive tasks may fail honestly as measured failures, but they cannot be safe-rejected or counted by diagnostic-only outputs.

### DR-008-009 — Full target does not mean natural-language fidelity

The pipeline is responsible for formal Lean theorem tasks in GeometryFull2DTarget. It is not responsible for proving that a natural-language olympiad problem was faithfully formalized unless a separate source-fidelity spec is approved.

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

Base must not import `plugins.geometry_full2d` internals except through plugin registry and declared contracts.

### 2.2 Canonical release plugin

The only release plugin is:

```text
plugins/geometry_full2d
```

`plugins/geometry_synthetic` and v0.3/v0.4.2 compatibility code may remain only outside release path. Any v0.4.3 release command importing `plugins.geometry_synthetic` is a release blocker.

### 2.3 Proof target

The single proof target is:

```text
MathAutoResearch.GeometryFull2D
GeometryFull2DTarget:1.0.0
```

It may use admitted LeanGeo and Mathlib dependencies, but release benchmark statements must be expressed in the facade grammar and extracted through the v0.4.3 extraction path.

Forbidden in target semantics:

```lean
def Point := Unit
def collinear ... := True
axiom geometry_solver_sound : ...
axiom every_geometry_goal_true : ...
structure Transformation where
  predicate : Prop
  evidence : predicate
```

A facade structure may contain evidence fields only for bookkeeping, not as the main theorem source for counted transformation/geometry success. Counted theorem proofs must reference solver/compiler artifacts and real Lean lemmas, not merely destruct stored evidence.

## 3. Target language scope

GeometryFull2DTarget includes 2D Euclidean geometry over the facade API.

Required objects:

```text
Point, Line, Circle, Segment, Ray, Triangle, Polygon, Angle, DirectedAngle,
Length, Ratio, Area, Vector2D, Reflection, Rotation, Homothety, Inversion,
SpiralSimilarity, TriangleCenter, AuxiliaryObject
```

Required relation families:

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

For release, a positive task is in-target iff structured extraction returns:

```yaml
TargetClassification:
  target_status: "in_target_positive"
  grammar_id: "GeometryFull2DTheoremGrammarV1"
  relation_to_goal: "exact_goal"
  unsupported_constructs: []
```

## 4. ActualTaskPipelineRunV1

Every counted success must be represented by:

```yaml
ActualTaskPipelineRunV1:
  schema_version: "1.0.0"
  run_id: "actual_full2d_run:..."
  task_id: "..."
  baseline_id: "B2 | B4 | ..."
  frozen_corpus_manifest_hash: "sha256:..."
  config_hash: "sha256:..."
  selected_implementations_hash: "sha256:..."
  source_theorem_ref: "sha256:..."
  source_theorem_path: "..."
  source_theorem_preproved: false
  lean_extraction_report_ref: "sha256:..."
  claim_spec_ref: "sha256:..."
  provider_run_manifest_ref: "sha256:..."
  engine_output_refs:
    - "sha256:..."
  compiler_result_refs:
    - "sha256:..."
  lean_patch_candidate_ref: "sha256:..."
  proof_worker_result_ref: "sha256:..."
  generated_candidate_file_ref: "sha256:..."
  final_verify_report_ref: "sha256:..."
  solver_backed_certificate_ref: "sha256:..."
  causal_chain_hash: "sha256:..."
  final_status: "final_theorem | measured_failure"
```

Release checker must load the referenced artifacts and verify all hashes.

## 5. Structured extraction

### 5.1 Required extraction command

There must be a Lean-side command or Lean elaborator-backed executable that receives:

```text
source file path
theorem full name
```

and emits JSON for exactly that theorem.

Required output:

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
```

A checker must reject any counted task if the extraction report theorem name or source statement hash does not match the counted source theorem.

### 5.2 Corpus-wide extraction requirement

For release, extraction must be performed for:

```text
100% of counted positive successes;
100% of measured failures in sampled release metrics;
100% of target-outside / malformed negative tasks used for safe-reject metrics.
```

A smoke-only extraction checker is insufficient.

## 6. Provider and engine contracts

### 6.1 Provider

```python
GeometryFull2DProvider.solve(request: GeometryFull2DSolveRequest) -> GeometryFull2DProviderRun
```

Each solve request must include:

```yaml
GeometryFull2DSolveRequest:
  request_id: "..."
  task_id: "..."
  claim_spec_ref: "sha256:..."
  claim_spec: GeometryFull2DClaimSpec
  target_library: "GeometryFull2DTarget:1.0.0"
  budget: "tiny | small | medium | heavy | extreme"
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

### 6.3 Engine output

```yaml
EngineOutputFull2D:
  schema_version: "1.0.0"
  engine_role: "..."
  backend_identity: "..."
  backend_code_hash: "sha256:..."
  input_ref: "sha256:..."
  raw_output_hash: "sha256:..."
  normalized_output_ref: "sha256:... | null"
  checker_or_compiler_ref: "sha256:... | null"
  resource_usage_ref: "sha256:..."
  real_integration_flag: true
  real_integration_evidence_ref: "sha256:..."
  fixture_flag: false
  status: "normalized_success | measured_failure | diagnostic"
  proof_use_status: "not_allowed"
```

### 6.4 Engine verification

Release must run `scripts/check_full2d_engine_real_execution.py` and fail if:

```text
- real_integration_flag is true but no evidence artifact exists;
- normalized_output_ref is generated from task_id/template_id instead of engine output;
- engine output does not depend on claim_spec input;
- backend_identity contains fixture/dummy/hardcoded/smoke;
- engine source file contains task-specific theorem name or template-id switch in release path;
- engine only passes one smoke theorem and is never used in counted successes;
- engine emits normalized_success but no compiler consumes the output.
```

## 7. Compiler contracts

The release compilers are:

```text
TraceCompilerFull2D
ConstructionCompilerFull2D
AlgebraicCompilerFull2D
MetricAngleCompilerFull2D
TransformationCompilerFull2D
OrderCaseCompilerFull2D
InequalityCompilerFull2D
LeanProofSearchCompilerFull2D
PortfolioCompilerFull2D
```

A compiler result must include:

```yaml
CompilerResultFull2D:
  compiler_result_ref: "sha256:..."
  compiler_id: "..."
  consumed_engine_output_refs:
    - "sha256:..."
  consumed_rule_ids:
    - "..."
  generated_obligations:
    - "..."
  side_condition_report_ref: "sha256:..."
  lean_patch_candidate_ref: "sha256:... | null"
  status: "compiled_patch | measured_failure"
```

The compiler must not read benchmark `template_id` to decide proof text. It may use rule ids and normalized solver artifacts only.

## 8. LeanPatchCandidateFull2D

A release patch candidate must include:

```yaml
LeanPatchCandidateFull2D:
  patch_id: "sha256:..."
  target_theorem_name: "..."
  target_statement_hash: "sha256:..."
  allowed_edit_region: "MARP proof region only"
  proof_region_replacement_ref: "sha256:..."
  proof_region_replacement_text: "..."
  source_compiler_result_refs:
    - "sha256:..."
  source_engine_output_refs:
    - "sha256:..."
  source_rule_ids:
    - "..."
  raw_provider_output_used_as_proof: false
```

Patch checker must fail if proof text is selected directly from benchmark labels.

## 9. Final verification and certificate

A counted success must have:

```yaml
SolverBackedProofCertificateFull2D:
  certificate_id: "sha256:..."
  task_id: "..."
  source_statement_hash: "sha256:..."
  extraction_report_ref: "sha256:..."
  claim_spec_ref: "sha256:..."
  provider_run_manifest_ref: "sha256:..."
  engine_output_refs:
    - "sha256:..."
  compiler_result_refs:
    - "sha256:..."
  lean_patch_candidate_ref: "sha256:..."
  proof_worker_result_ref: "sha256:..."
  final_verify_report_ref: "sha256:..."
  proof_region_diff_ref: "sha256:..."
  checked_candidate_file_ref: "sha256:..."
  theorem_hash_unchanged: true
  no_sorry: true
  no_forbidden_axioms: true
  raw_solver_output_used_as_proof: false
  proof_use_status: "solver_backed_final_theorem"
  status: "passed"
```

Certificate checker must verify every referenced artifact exists and hashes match.

## 10. Corpus requirements

Release corpus must include at least:

```text
positive formal Lean tasks: 3000
negative / target-outside / malformed tasks: 500
external_formal or user_reviewed_human_curated positive tasks: 900
synthetic_generated positives: <= 50% of positives
near_duplicate positives: <= 10%
exact template duplicate max per theorem family: 5
```

Codex-generated local tasks do not count as `human_curated_formal` unless user supplies an explicit approval manifest.

Allowed positive provenance:

```text
external_formal:
  comes from an external formal benchmark / repository / paper source with source_ref.

user_reviewed_human_curated:
  created or reviewed by the user or a separate reviewer, with review_manifest_ref.

synthetic_generated:
  generated by Codex/scripts/models. Counts only as synthetic.
```

Forbidden:

```text
provenance: human_curated_formal
```

unless mapped to `user_reviewed_human_curated` with an explicit review manifest.

## 11. Benchmark and metrics

### 11.1 Positive families

Required family floors remain:

```text
Full2DCore500
IncidenceParallelPerp350
AngleCyclic450
Construction450
MetricRatioArea350
Transformation250
OrderCase250
Algebraic250
Inequality150
OlympiadStyle300
HardHoldout50
```

### 11.2 Performance thresholds

Release acceptance must verify the existing threshold set, but now from actual pipeline run records, not summaries:

```text
Overall positive final theorem rate >= 0.85
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
safe-reject success on in-target positives = 0
```

### 11.3 Advantage requirements

Advantage must be computed from actual baseline runs:

```text
B2 full portfolio - B1 no geometry solver >= 0.25 overall final theorem rate
B2 - B5 construction disabled >= 0.15 on construction subset
B2 - B6 algebraic disabled >= 0.15 on algebraic/metric subset
B2 - B7 order/case disabled >= 0.10 on order/case subset
B2 - B8 model disabled >= 0.05 on olympiad-style subset if model provider is used
```

If a baseline is disabled or simulated without executing comparable tasks, advantage is invalid.


## 12. Substantive benchmark and anti-gaming requirements

The release corpus must not merely contain syntactically valid GeometryFull2D statements. It must contain substantive formal geometry tasks whose success requires actual pipeline execution. This section is part of this Base Spec, not an addendum.

### 12.1 SubstantiveTaskProfileV1

Every positive release task must include:

```yaml
SubstantiveTaskProfileV1:
  task_id: "..."
  source_kind: "external_formal | user_reviewed_human_curated | synthetic_generated"
  theorem_family: "..."
  geometry_features:
    - "incidence | angle | cyclic | construction | metric | area | ratio | transformation | order_case | inequality | algebraic"
  required_reasoning_depth: 0
  requires_construction: true | false
  requires_side_condition_discharge: true | false
  requires_case_split_or_order_reasoning: true | false
  requires_nontrivial_metric_or_algebraic_reasoning: true | false
  direct_lean_lemma_baseline_expected: true | false
  review_manifest_ref: "sha256:... | null"
```

### 12.2 Substantive floors

Final release fails unless the corpus satisfies all of the following, in addition to the existing corpus-size floors:

```text
substantive positive tasks with required_reasoning_depth >= 2: >= 1200
substantive positive tasks with required_reasoning_depth >= 4: >= 350
construction-required tasks: >= 350
side-condition-discharge-required tasks: >= 350
case/order reasoning required tasks: >= 250
metric/angle/algebraic/inequality nontrivial tasks: >= 500
transformation nontrivial tasks: >= 150
olympiad-style tasks with depth >= 4: >= 150
hard holdout tasks with no exact theorem-family duplicate: >= 50
```

A task of the form `P -> P`, reflexivity only, repeated-point collinearity only, stored-structure-evidence extraction only, or direct facade lemma application counts as `required_reasoning_depth <= 1` unless a valid `ReviewManifestV1` explicitly justifies otherwise.

### 12.3 Direct lemma ceiling

More than 20% of counted positive final-theorem successes may not be solved by a single direct facade lemma application with no solver-generated intermediate fact, construction, side-condition report, case/order evidence, algebraic certificate, metric/angle certificate, or inequality certificate.

The release checker must compute and report:

```text
direct_lemma_success_fraction
solver_intermediate_success_fraction
construction_used_success_fraction
side_condition_used_success_fraction
multi_step_trace_success_fraction
```

### 12.4 Curated provenance is not self-certified by Codex

`user_reviewed_human_curated` requires an explicit review artifact not authored by the implementation agent in the same work unit.

Allowed review evidence:

```yaml
ReviewManifestV1:
  reviewer_kind: "user | named_human_reviewer | external_formal_source"
  reviewer_id: "..."
  created_outside_codex_run: true
  reviewed_task_ids: []
  review_statement: "The listed tasks are intentionally admitted as human/user curated formal geometry tasks."
  review_hash: "sha256:..."
```

Disallowed:

```text
- Codex-created local tasks marked user_reviewed_human_curated without ReviewManifestV1.
- Review manifests generated by the same Codex implementation step and not explicitly approved by user.
- Provenance notes such as "Codex-created formal Lean facade task" counted as curated.
```

If no valid review manifest exists, Codex must label those tasks as `synthetic_generated`.

### 12.5 Engine output must be semantic, not proof text

No release-critical engine output may include Lean proof text, tactic scripts, proof-region replacement text, benchmark-specific proof templates, or benchmark dispatch fields.

Forbidden fields or semantic equivalents in engine outputs:

```text
proof_text
tactic_script
lean_patch
proof_region_replacement_text
exact_lemma_application
benchmark_template_id
theorem_family_dispatch
task_id_dispatch
theorem_name_dispatch
```

Allowed engine outputs:

```text
normalized geometric facts
trace steps with rule ids
construction candidates
side-condition reports
case split / coverage reports
algebraic or inequality certificates
metric/angle normalization certificates
measured-failure diagnostics
```

The compiler, not the engine, creates `LeanPatchCandidateFull2D`, and the compiler may do so only from normalized engine artifacts and RuleRegistry contracts.

### 12.6 Compiler input isolation

Release compilers may consume only:

```text
GeometryFull2DClaimSpec
EngineOutputFull2D artifacts
RuleRegistryFull2D
SideConditionCalculusFull2D
Lean theorem target hash / allowed edit region
```

Release compilers must not consume:

```text
template_id
theorem_family
provenance label
difficulty_tier
benchmark task_id except as opaque run identifier
```

A checker must scan release compiler code and runtime traces for this isolation boundary.

### 12.7 Baseline comparability

Advantage claims are valid only if baseline runs are comparable. B1, B5, B6, B7, and B8 must use:

```text
same corpus
same source theorem files
same ProofWorker capability
same FinalVerifyGate
same model provider set, except for the explicitly disabled component
same resource class unless the ablation spec explicitly varies resources and records it
```

A baseline may disable only the named component. It must not be crippled by removing final verification, proof worker patch application, Lean library access, or source theorem visibility.

If B1 can solve a direct-lemma task without the geometry solver, that success must be counted for B1. This prevents easy template tasks from inflating B2 advantage.

### 12.8 Causal-chain hash

`ActualTaskPipelineRunV1` must include a `causal_chain_hash` computed from ordered hashes of:

```text
source theorem artifact
LeanExtractionReportFull2D
GeometryFull2DClaimSpec
ProviderRunManifestFull2D
EngineOutputFull2D artifacts listed in engine_output_refs
CompilerResultFull2D artifacts
LeanPatchCandidateFull2D
ProofWorkerResultFull2D
FinalVerifyReport
SolverBackedProofCertificateFull2D
```

The release checker must recompute this chain and fail on mismatch.

### 12.9 Anti-v0.4.2 regression fixture

The repository must include a negative regression fixture reproducing the bad v0.4.2 path:

```text
template_id -> proof replacement -> fabricated solver ref -> FinalVerifyGate -> overlay metric success
```

The v0.4.3 release checker must reject this fixture and record the failure reason under `anti_v042_regression_status=passed`.

## 13. Anti-gaming release blockers

Final release must fail if any of the following occur:

```text
K-001: release report metrics_summary / advantage_summary / engine_usage_summary / used_rule_coverage_summary is empty.
K-002: any open DebtLedger entry remains.
K-003: counted final theorem lacks ActualTaskPipelineRunV1.
K-004: counted final theorem lacks provider_run_manifest_ref from actual provider.solve run.
K-005: normalized solver artifact ref is fabricated from task_id/template_id/theorem_name.
K-006: proof patch selected from template_id or theorem_family rather than compiler output.
K-007: matrix success computed from overlay without matching replay-valid ActualTaskPipelineRunV1.
K-008: extraction checker only validates a smoke theorem.
K-009: Codex-generated local corpus counted as human curated without explicit review manifest.
K-010: engine real_integration_flag has no independent evidence artifact.
K-011: source theorem is already proved before proof-worker patch and counted as solver-backed success.
K-012: rule registry count passes but used-rule coverage is below thresholds.
K-013: engine role appears in used_engine_roles by label but no counted certificate references its engine output.
K-014: release corpus full-file or per-theorem Lean compile evidence missing for counted tasks.
K-015: release checker ignores any of K-001..K-014.
K-016: substantive benchmark floors missing or below threshold.
K-017: direct lemma success fraction exceeds allowed ceiling.
K-018: curated provenance is self-certified by Codex.
K-019: engine output contains proof text or benchmark dispatch fields.
K-020: compiler reads benchmark labels to decide proof text.
K-021: baseline comparability violated.
K-022: ActualTaskPipelineRunV1 causal_chain_hash missing or invalid.
K-023: v0.4.2 failure regression is not present or does not fail.
K-024: release checker does not enforce K-016..K-023.
```

## 14. Continue-on-debt policy

Codex must continue independent implementation when it sees ReleaseBlocker or WorkDebt. It may stop only for HardBlockers:

```text
HB-01 active approved specs conflict
HB-02 requirement would require changing this Base Spec
HB-03 destructive action outside explicit refactor scope
HB-04 license/terms violation
HB-05 required private credential with no allowed substitute
HB-06 unspecified incompatible mathematical semantics
HB-07 unavoidable unsound proof-use path
HB-08 Lean cannot run at all after bootstrap
HB-09 Guardian authority corruption
```

All other failures must be recorded in the debt ledger and implementation must continue where possible.

## 15. Final release acceptance

Final release acceptance command:

```bash
python scripts/check_release_acceptance_v0_4_3.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_3/evidence/release_acceptance_report.json
```

Release passes only if:

```text
hard_blockers = []
release_blockers = []
work_debt_open = []
all anti-gaming checks pass
all extraction/engine/compiler/proof/certificate checks pass
all corpus floors pass
all performance thresholds pass
all advantage thresholds pass
all counted successes have valid ActualTaskPipelineRunV1
substantive_corpus_summary / review_manifest_summary / baseline_comparability_summary / causal_chain_summary / anti_v042_regression_status / engine_semantic_output_summary / compiler_input_isolation_summary are present and non-empty
closure claim does not exceed evidence
```
