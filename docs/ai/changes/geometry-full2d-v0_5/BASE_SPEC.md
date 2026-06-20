---
title: "Guardian Base Spec — GeometryFull2D v0.5 Real Solver-Causal Full Pipeline Reviewed Strict"
spec_id: "MARP-GEOLEAN-BASE-011"
related_plan: "MARP-GEOLEAN-PLAN-011"
related_acceptance: "MARP-GEOLEAN-ACCEPTANCE-011"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-012_RETAINED_AS_PRIOR_EVIDENCE"
supersedes_when_approved:
  - "MARP-GEOLEAN-BASE-010"
claim_target: "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
target_repo: "kabatan/baka_proof"
revision: "reviewed-strict-2026-06-18"
---

# Guardian Base Spec — GeometryFull2D v0.5 Real Solver-Causal Full Pipeline Reviewed Strict

## 0. Purpose

This Base Spec replaces all earlier GeometryFull2D v0.4.x and draft v0.5 authority documents after user approval. It exists because earlier implementations repeatedly satisfied release checkers while avoiding the intended full solver-causal implementation.

The new release target is not a report-shaped, target-shape, rule-list, or identity-rule pipeline. It is a real solver-causal proving pipeline for formal Lean theorem tasks in `GeometryFull2DTarget:1.0.0`.

The only admitted final claim is:

```text
V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```

The claim is permitted only when every counted positive theorem is processed by this executable causal chain:

```text
sorry-only Lean theorem source
  -> Lean-side structured extraction for that exact theorem
  -> GeometryFull2DClaimSpec
  -> provider.solve actual run in a separate provider process / stage
  -> EngineOutputFull2D containing independently checked nontrivial solver artifacts
  -> SelectedSolverDerivationV2 chosen from those engine artifacts
  -> compiler consumes SelectedSolverDerivationV2 and RuleRegistry contracts
  -> LeanPatchCandidateFull2D
  -> ProofWorker applies patch only inside MARP proof region
  -> FinalVerifyGate compiles generated candidate and checks no sorry / no forbidden declarations
  -> SolverBackedProofCertificateFull2D binds all upstream artifacts
  -> live destructive SolverCausalityReportV3 reruns prove selected solver artifacts are necessary
  -> artifact-derived metrics, used-rule coverage, engine contribution, and baseline reports
```

A report containing fields named `solver_causal_necessity`, `mutation_sensitive`, `failed_as_expected`, or `replay_status` is not evidence by itself. Evidence must include live rerun command logs, temp run directories, input/output hashes, and final acceptance verification.

## 1. Generalized red-case class

This spec treats the following as one failure class: **Agent shortcut implementation**. A release implementation must reject the whole class, not merely the specific historical files.

A shortcut implementation includes at least:

```text
1. Target-fact provider:
   provider reads the final target and emits that target as an already-proved solver fact.

2. Naked target assertion:
   selected solver derivation contains only the final target and no non-target intermediate, construction, certificate, or replayable trace.

3. Identity-rule registry:
   counted rule transforms a fact into itself or applies a direct facade theorem and is counted as geometry reasoning.

4. Proof-from-shape compiler:
   compiler chooses proof text from target expression shape, theorem name, theorem family, task id, grammar family, category, difficulty tier, target_shape_id, source_ref, or benchmark labels.

5. Rule-list artifact synthesis:
   engine outputs are generated from compiler-selected used_rules or from a proof plan already chosen by the compiler.

6. Report-only causality:
   causality report says deleted/corrupted artifact failed without executing destructive reruns.

7. Family-coded baseline:
   baseline success/failure is decided directly by theorem family, category, or corpus label.

8. Projection corpus as benchmark:
   external source is used only as a source of point names or predicates while the counted Lean goal is an easier projection.

9. Checker omission:
   Base Spec / Acceptance requirement exists but final release command does not execute and enforce a checker for it.

10. Checker whitelist:
   checker detects a forbidden shortcut in a release entrypoint and suppresses it because of filename, directory, or role.

11. Sealed challenge collusion:
   holdout generator imports, reads, or is generated from provider/compiler/rule-registry/proof code or emits proof hints.

12. Stale evidence replay:
   final release accepts run records not freshly generated or not bound to current git head, selected implementation hash, corpus hash, config hash, checker hashes, and run directory hash.
```

Every member of this class is a release blocker.

## 2. Non-negotiable decisions

### DR-011-001 — Red-case-first implementation

Codex must implement the red-case suite and release acceptance coverage before implementing provider, compiler, rule registry, matrix, or corpus expansion. The first milestone is that all shortcut implementations fail.

### DR-011-002 — No target-fact provider

An engine must not output the final target as a selected fact unless it is the final step of a replayable derivation from prior non-target artifacts.

Invalid counted success:

```yaml
facts:
  - conclusion: <target>
    premises: []
    checker_report_ref: null
```

Valid counted success must contain at least one of:

```text
- multi-step synthetic trace with at least one selected non-target intermediate fact;
- construction trace with introduced object and side-condition discharge;
- algebraic/metric/inequality certificate independently replayed from hypotheses;
- Lean-search certificate checked independently and not equivalent to a naked target assertion;
- external solver trace normalized and replay-checked.
```

### DR-011-003 — No proof-from-shape compiler

The compiler may use ClaimSpec only for theorem anchoring, variable names, and final-goal equivalence checking. It may not branch on target expression shape to choose proof text. It must consume `SelectedSolverDerivationV2` and RuleRegistry contracts.

Forbidden in release compiler code paths:

```text
target_expr.startswith(...)
match target_expr
if target_family == ...
if theorem_family == ...
if grammar_family == ...
if task_id == ...
if baseline == ... to select proof text
lookup_by_target_shape
proof_from_shape
proof_from_source
```

### DR-011-004 — Provider / engine cannot import downstream proof code

Provider and engine code may not import compiler, rule registry Lean templates, proof worker, final verifier, matrix, corpus generator, benchmark metadata utilities, or prior release runner modules. Provider output must be generated before compiler execution and persisted as content-addressed artifacts.

### DR-011-005 — Solver causality requires live destructive reruns

For every counted B2 success, release acceptance must rerun the pipeline in a temporary isolated directory for:

```text
positive_control
remove_selected_solver_artifact
corrupt_selected_fact_or_construction
corrupt_certificate_or_checker_output
unsupported_rule_mutation
side_condition_mutation
```

The rerun must invoke the compiler, ProofWorker, and FinalVerifyGate. A mutation passes only if it prevents the same final theorem from being counted. A text field saying `failed_as_expected` is not evidence.

### DR-011-006 — Full matrix means all baselines

B1, B2, B5, B6, B7, and conditional B8 must run through the same actual task pipeline for every counted task. Baselines may differ only by declared disabled components in config. Success/failure cannot be decided by theorem family or corpus label.

Conditional B8 is not an escape hatch. The release config must explicitly resolve B8 as one of:

```text
B8_ENABLED:
  model/provider baseline is configured and must run for every counted task.

B8_NOT_APPLICABLE:
  model/provider baseline is not configured for this release; the report must record the concrete reason and checker evidence.
```

If B8 is enabled in config, missing B8 records are `K-033`. If B8 is not applicable, the report must still prove that B1, B2, B5, B6, and B7 ran for every counted task and that no B2 metric was computed from B8 availability, family labels, target shape, or model self-report.

### DR-011-007 — Corpus is independent of proof implementation

Counted positives may be only:

```text
ExternalGoalPreserved:
  external formal source goal preserved exactly or by machine-checkable equivalence.

SealedAdversarialHoldout:
  generated after implementation freeze by a generator that cannot import/read provider, compiler, rule registry, Lean proof lemmas, proof worker, final verifier, previous release modules, or run records.

UserReviewedGoal:
  explicitly approved with ReviewManifestV2.
```

Projection tasks may exist only as regression fixtures and cannot count as release positives.

### DR-011-008 — Stale evidence is invalid

Final release must run in a fresh release run directory created by the final command, or must prove exact replay freshness by hashes for every artifact. The default final release command must delete or create a fresh `runs/geometry_full2d_v0_5/release_<timestamp_or_hash>` directory. Reusing old records without exact freshness proof is a release blocker.

### DR-011-009 — Checker coverage is itself checked

Every K requirement in Acceptance must map to at least one executed checker. Every checker result must be included in the release report. If a checker detects a forbidden pattern in release code, the final release must fail. Filename-based suppression in release entrypoints is forbidden.

## 3. Architecture boundary

### 3.1 Base pipeline

Base remains domain-neutral:

```text
ArtifactStore
RunLogger
SchemaRegistry
PluginRegistry
ProofStateDAG kernel
GraphPatch / DAGWriter
TrustGuard
FinalVerifyGate
ModelProviderSet
ResourceGovernor
ReplayVerifier
ReleaseAcceptanceRunner
```

Base must not import geometry-specific modules except through plugin registry and declared interfaces.

### 3.2 Canonical plugin

The v0.5 release plugin is:

```text
plugins/geometry_full2d
```

A separate versioned implementation namespace may be used internally, but release config must point to one selected implementation. `plugins.geometry_synthetic`, v0.3, v0.4.2, v0.4.3, v0.4.4, and draft v0.5 shortcuts may only appear as red-case fixtures, never as release dependencies.

### 3.3 Required stage order

The release runner must enforce stage order:

```text
extract -> claimspec -> provider -> independent solver checkers -> selected derivation -> compiler -> proof worker -> final verify -> certificate -> matrix record materialization -> causality reruns -> metrics/summaries
```

A downstream stage may read only upstream content-addressed artifacts. Provider must not read compiler outputs. Compiler must not read matrix/corpus labels. Matrix must not synthesize task outcomes. Matrix execution materializes one actual task/baseline record per counted task and required baseline through FinalVerify or a content-addressed measured failure report. Solver causality then reruns every counted B2 final theorem success discovered by those records. Metrics and summaries are computed only after causality reports exist.

## 4. Required artifact schemas

### 4.1 ActualTaskPipelineRunV4

```yaml
ActualTaskPipelineRunV4:
  schema_version: "ActualTaskPipelineRunV4"
  run_id: "actual_full2d_run:v0_5:..."
  task_id: "..."
  baseline_id: "B1 | B2 | B5 | B6 | B7 | B8"
  corpus_manifest_hash: "sha256:..."
  config_hash: "sha256:..."
  git_head: "..."
  selected_implementation_hash: "sha256:..."
  release_run_dir_hash: "sha256:..."
  source_theorem_ref: "sha256:..."
  source_theorem_preproved: false
  extraction_report_ref: "sha256:..."
  claim_spec_ref: "sha256:..."
  provider_run_manifest_ref: "sha256:..."
  engine_output_refs: ["sha256:..."]
  independent_checker_report_refs: ["sha256:..."]
  selected_solver_derivation_ref: "sha256:..."
  compiler_result_refs: ["sha256:..."]
  lean_patch_candidate_ref: "sha256:..."
  proof_worker_result_ref: "sha256:..."
  final_verify_report_ref: "sha256:..."
  solver_causality_report_ref: "sha256:... | null until causality stage"
  solver_backed_certificate_ref: "sha256:..."
  causal_chain_hash: "sha256:..."
  final_status: "final_theorem | measured_failure"
```

All refs must resolve to artifacts whose content hash matches the ref.

For `final_theorem` records, stage refs must resolve to the successful stage artifact types named by the fields. For `measured_failure` records, a stage that cannot run because a baseline intentionally disables an upstream component or because an earlier real stage failed must write a content-addressed `StageFailureReportV1` or `DisabledStageReportV1`; downstream refs may point to those reports instead of fake successful artifacts. Null refs are allowed only before the stage is reached inside an in-progress run and are forbidden in final release records. A `final_theorem` status may come only from `FinalVerifyReportFull2D`. A measured failure may come from either `FinalVerifyReportFull2D` or a content-addressed stage failure/disabled report, never from family labels, target shape, or expected outcome metadata.

```yaml
StageFailureReportV1:
  schema_version: "StageFailureReportV1"
  stage: "provider | independent_checker | compiler | proof_worker | final_verify | causality"
  input_refs: ["sha256:..."]
  command_log_ref: "sha256:..."
  failure_kind: "real_execution_failure | validation_rejected | resource_exhausted | unsupported_after_disabled_component"
  failure_reason: "..."
  git_head: "..."
  selected_implementation_hash: "sha256:..."

DisabledStageReportV1:
  schema_version: "DisabledStageReportV1"
  baseline_id: "B1 | B5 | B6 | B7 | B8"
  disabled_component: "..."
  config_ref: "sha256:..."
  upstream_input_refs: ["sha256:..."]
  reason: "declared baseline ablation only"
```

### 4.2 EngineOutputFull2D

```yaml
EngineOutputFull2D:
  schema_version: "EngineOutputFull2D:2"
  engine_role: "synthetic_closure | construction_search | algebraic_geometry | metric_angle | transformation | order_case | inequality | lean_proof_search | portfolio_coordinator"
  input_claim_spec_ref: "sha256:..."
  backend_identity: "..."
  backend_code_hash: "sha256:..."
  provider_stage_run_id: "..."
  real_execution_evidence_ref: "sha256:..."
  normalized_artifact_refs: ["sha256:..."]
  proof_text_present: false
  forbidden_metadata_consumed_by_compiler: []
  facts: []
  constructions: []
  certificates: []
  proof_use_status: "not_allowed"
```

Selected artifacts must be semantic and independently checkable. Engine output cannot contain Lean proof snippets, rule-to-proof mappings, target theorem names for proof generation, or compiler-selected rule lists.

The `synthetic_closure` engine role name does not permit synthetic proof closure, target-fact emission, proof-from-shape behavior, or report-shaped success. Counted `synthetic_closure` contribution must be replayable from original hypotheses and independently checked like every other engine output.

### 4.3 SelectedSolverDerivationV2

```yaml
SelectedSolverDerivationV2:
  derivation_id: "sha256:..."
  selected_engine_output_refs: ["sha256:..."]
  selected_facts: ["fact_id"]
  selected_constructions: ["construction_id"]
  selected_certificates: ["certificate_id"]
  derivation_steps:
    - step_id: "..."
      input_refs: ["hypothesis_id | fact_id | construction_id | certificate_id"]
      output_ref: "fact_id | target_goal"
      rule_id: "..."
      independent_checker_report_ref: "sha256:..."
      output_is_target: true|false
      non_target_intermediate: true|false
```

A counted success must have at least one selected non-target intermediate or selected construction/certificate whose checker derives the target from original hypotheses. A direct single-step target assertion does not count.

### 4.4 RuleRegistryFull2D

Every counted rule must have:

```yaml
RuleContractFull2D:
  rule_id: "..."
  rule_family: "..."
  input_patterns: [...]
  output_pattern: "..."
  required_side_conditions: [...]
  generated_obligations: [...]
  lean_template_id: "..."
  independent_checker: "..."
  positive_fixtures: [...]
  negative_fixtures: [...]
  mutation_fixtures: [...]
  direct_identity_rule: false
  direct_facade_rule: false
```

Identity/direct-facade/helper rules may exist only as non-counted helper rules and may not contribute to used-rule coverage, solver-causal success, non-target intermediate success, or engine contribution metrics.

## 5. Corpus requirements

### 5.1 Counted corpus floors

```text
Total counted positive formal Lean tasks >= 1200
Negative / target-outside / malformed >= 300
SealedAdversarialHoldout >= 700
ExternalGoalPreserved >= min(300, discovered_machine_checkable_external_goal_preserved_count)
UserReviewedGoal has no fixed floor; if present every task requires ReviewManifestV2
ProjectionNonCounted may exist only as regression fixture and must not count
```

The lower quantity than v0.4.x is intentional. A smaller corpus with adversarial causality is preferred to a large template corpus. This does not reduce `GeometryFull2DTarget:1.0.0`; it defines the release validation floor for full pipeline readiness.

### 5.2 Statement diversity floors

Counted positives must satisfy:

```text
unique normalized theorem skeletons >= 150
max exact normalized theorem skeleton duplicate count <= 8
used relation families >= 8
construction/case/certificate required tasks >= 350
non-target intermediate required tasks >= 600
```

The normalized skeleton removes theorem names, variable names, and binder ordering. This prevents a fixed target-shape menu from satisfying the corpus floor.

### 5.3 SealedAdversarialHoldout generation

The sealed generator must:

```text
- run after implementation freeze;
- not import/read provider, compiler, rule registry, proof worker, final verifier, matrix, run records, Lean facade proof lemma inventory, or previous release modules;
- not emit proof text, rule ids, engine roles, solver hints, target_shape_id, template id, expected compiler rule, or proof labels;
- record generator hash, grammar hash, freeze hash, seed, and challenge manifest hash;
- be regenerated if selected implementation hash changes;
- generate diverse theorem skeletons from a declarative grammar that is separate from proof code.
```

### 5.4 ExternalGoalPreserved

Goal preservation requires machine-checkable evidence:

```yaml
GoalPreservationReportV2:
  source_goal_ast_ref: "sha256:..."
  translated_goal_ast_ref: "sha256:..."
  mapping_table_ref: "sha256:..."
  preservation_kind: "exact_same_formal_goal | formally_equivalent | structurally_preserved_with_machine_checked_mapping"
  dropped_hypotheses: []
  added_strengthening_hypotheses: []
  easier_projection: false
  checker_report_ref: "sha256:..."
```

A report written by the corpus generator is not enough unless a separate checker recomputes the mapping from source AST to translated AST and rejects easier projections.

## 6. Metrics and thresholds

Release thresholds:

```text
B2 counted final theorem rate >= 0.70
B2 solver-causal final theorem rate >= 0.70
B2 destructive causality pass rate = 1.00 on all counted B2 final theorem successes
B2 non-target-intermediate success fraction >= 0.50
B2 construction/case/certificate success fraction >= 0.40
Direct or wrapped facade lemma success fraction <= 0.10
Used concrete non-identity rules >= 25
Used rule families >= 10
Every release-critical engine role contributes to at least one counted B2 success
```

No release-critical engine role may be marked not applicable except conditional B8 model provider. If a role has no task, corpus construction is insufficient.

Baseline thresholds:

```text
B2 - B1 overall advantage >= 0.15
B2 - B5 construction subset advantage >= 0.10 when construction subset exists
B2 - B6 algebraic/metric subset advantage >= 0.10 when subset exists
B2 - B7 order/case subset advantage >= 0.05 when subset exists
B8 only when model provider is enabled; otherwise report not_applicable_model_provider_not_used
```

The B8 applicability decision must be emitted in `baseline_comparability_summary.conditional_b8_resolution` and independently checked. The checker must fail if B8 is silently omitted, if B8 is disabled only to simplify release execution, or if B8 status changes counted B2 success/failure.

## 7. Required red cases

Final release must dynamically generate and reject at least these classes:

```text
RedCase_TargetFactProvider
RedCase_NakedTargetAssertion
RedCase_IdentityRuleRegistry
RedCase_ProofFromShapeCompiler
RedCase_RuleListArtifactSynthesis
RedCase_ReportOnlyCausality
RedCase_FamilyCodedBaseline
RedCase_ProjectionCorpusCounted
RedCase_EngineOutputContainsProofText
RedCase_CheckerOmission
RedCase_CheckerWhitelist
RedCase_DirectLemmaWrappedAsIntermediate
RedCase_SealedChallengeImportsCompiler
RedCase_StaleEvidenceReplay
RedCase_TargetShapeMenuCorpus
RedCase_GoalPreservationSelfAttestation
RedCase_ProviderImportsCompiler
RedCase_B8SilentlyOmitted
RedCase_ClosureOverclaimsReadiness
```

A red case passes only if release acceptance rejects it for the expected K blocker.

## 8. Final release requirements

The final release command is:

```bash
python scripts/check_release_acceptance_v0_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_5.yaml \
  --output docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json \
  --fresh-run
```

It must fail unless all hold:

```text
- every K requirement has an executed checker result;
- red cases are rejected;
- final run directory is fresh or exactly replay-verified;
- all counted successes have ActualTaskPipelineRunV4;
- all selected solver artifacts pass independent checker evidence;
- all B2 successes have live destructive SolverCausalityReportV3;
- matrix contains actual records for all required baselines and counted tasks;
- no release implementation path uses target-fact, proof-from-shape, identity-rule, or family-coded shortcuts;
- corpus independence and statement diversity floors pass;
- DebtLedger has no open entries;
- closure does not exceed evidence.
```

Closure is a separate artifact from the release report. The final release command must emit a machine-readable `closure_claim_ceiling` even before `CLOSURE.md` exists. After `CLOSURE.md` is written, `check_closure_claim_ceiling_v0_5.py` must compare the closure against the release report and fail on any claim beyond `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` or any missing required non-claim.
