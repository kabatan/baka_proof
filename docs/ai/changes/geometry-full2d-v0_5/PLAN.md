---
title: "Guardian Plan — GeometryFull2D v0.5 Real Solver-Causal Full Pipeline Reviewed Strict"
plan_id: "MARP-GEOLEAN-PLAN-011"
base_spec: "MARP-GEOLEAN-BASE-011"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-011"
claim_target: "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
status: "SUPERSEDED_BY_MARP-GEOLEAN-PLAN-012_RETAINED_AS_PRIOR_EVIDENCE"
revision: "reviewed-strict-2026-06-18"
---

# Guardian Plan — GeometryFull2D v0.5 Real Solver-Causal Full Pipeline Reviewed Strict

## 0. Execution rule for Codex

Codex must execute work packages in order. It must not weaken Base Spec, remove checkers, lower thresholds, rename forbidden shortcuts, or close a blocker without fresh artifact evidence. ReleaseBlockers block closure but do not stop work. HardBlockers stop work only for repository safety, destructive ambiguity, or contradictory approved requirements.

The goal is not to produce a green report quickly. The goal is to produce a real solver-causal pipeline that passes adversarial acceptance.

No Plan acceptance item is sufficient by itself if a Base Spec or Acceptance requirement remains unchecked. When a Plan sentence is ambiguous, the stricter non-shortcut reading of `MARP-GEOLEAN-BASE-011` controls. Implementation discretion is limited to internal code organization and performance choices; it never permits mocks, self-attestation, report-only success, synthetic-only release artifacts, stale run reuse, family-coded outcomes, or checker suppression.

## 0.1 Base Spec to Plan coverage matrix

| Base Spec authority | Plan work package(s) | Required checker / evidence |
|---|---|---|
| DR-011-001 Red-case-first | WP-01, WP-02 | `run_red_cases_v0_5.py --expect-failure`, `check_acceptance_coverage_v0_5.py` |
| DR-011-002 No target-fact provider | WP-03, WP-06, WP-07 | schema validator, provider boundary, engine output, independent checker red cases |
| DR-011-003 No proof-from-shape compiler | WP-09 | `check_compiler_input_isolation_v0_5.py`, `check_compiler_taint_v0_5.py` |
| DR-011-004 Provider cannot import downstream proof code | WP-04, WP-06, WP-09 | corpus independence, provider boundary, compiler isolation |
| DR-011-005 Live destructive causality | WP-12, WP-14 | `run_solver_causality_mutations_v0_5.py`, `check_solver_causality_reports_v0_5.py` |
| DR-011-006 Full matrix / all baselines / B8 resolution | WP-11, WP-13 | matrix runner, baseline comparability, metrics, conditional B8 resolution evidence |
| DR-011-007 Corpus independent of proof implementation | WP-04, WP-10A | corpus independence, statement diversity, goal preservation, freeze manifest |
| DR-011-008 Stale evidence invalid | WP-02, WP-10A, WP-11, WP-12, WP-14 | freshness hashes, fresh run directory, stale evidence red case |
| DR-011-009 Checker coverage checked | WP-02, WP-14 | checker coverage matrix, no whitelist checker, final release report |
| Architecture stage order and schemas | WP-03, WP-05, WP-06, WP-07, WP-08, WP-09, WP-10, WP-11, WP-12 | artifact validators and per-stage boundary reports |
| Corpus floors and diversity | WP-04, WP-10A, WP-13 | counted corpus manifest, diversity and goal-preservation reports |
| Metrics and thresholds | WP-13, WP-14 | metrics, used-rule coverage, engine contribution, baseline advantage |
| Closure claim ceiling | WP-14 | `check_closure_claim_ceiling_v0_5.py` after release report and after closure writing |

If any row lacks executable evidence, the Plan is not complete even if a later release report is green.

## WP-00 — Install v0.5 authority and quarantine old paths

### Tasks

1. Copy v0.5 documents to `docs/ai/changes/geometry-full2d-v0_5/`.
2. Mark v0.4.2, v0.4.3, v0.4.4, v0.4.5 draft specs and closures as superseded evidence.
3. Move old shortcut-prone scripts into `tests/red_cases/legacy_shortcuts/` or keep them only as regression fixtures.
4. Release paths must not import superseded modules.

### Acceptance

`python scripts/check_active_guardian_spec_v0_5.py` reports only `MARP-GEOLEAN-BASE-011` as active.

## WP-01 — Red-case suite first

### Tasks

Implement `tests/red_cases/v0_5/` with executable fixtures for every RedCase in Base Spec section 7. Each fixture must be minimal but runnable. Each fixture must be rejected by the same validators used in final release.

Required fixtures:

```text
target_fact_provider
naked_target_assertion
identity_rule_registry
proof_from_shape_compiler
rule_list_artifact_synthesis
report_only_causality
family_coded_baseline
projection_corpus_counted
engine_output_contains_proof_text
checker_omission
checker_whitelist
direct_lemma_wrapped_as_intermediate
sealed_challenge_imports_compiler
stale_evidence_replay
target_shape_menu_corpus
goal_preservation_self_attestation
provider_imports_compiler
b8_silently_omitted
closure_overclaims_readiness
```

### Acceptance

`python scripts/run_red_cases_v0_5.py --expect-failure` returns 0 only when every fixture is rejected for its expected K blocker. A red-case detector may not whitelist release files by name.

## WP-02 — Acceptance harness and K coverage before implementation

### Tasks

1. Implement `scripts/check_release_acceptance_v0_5.py` with `--fresh-run` default behavior.
2. Implement `scripts/check_acceptance_coverage_v0_5.py` mapping every K blocker to executed checker(s).
3. Implement `scripts/check_no_checker_whitelist_v0_5.py` rejecting release checkers that detect-and-suppress forbidden patterns by filename.
4. Final checker must run WP-01 red cases every time.
5. Final checker must fail on missing checker, missing summary, stale artifact, empty report, or omitted K coverage.

### Acceptance

On the current shortcut implementation, release checker fails. On an empty repo, release checker fails. On red-case fixtures, release checker fails. It must not return 0 until real pipeline artifacts exist.

## WP-03 — Schemas and artifact validators

### Tasks

Implement schemas and validators for:

```text
ActualTaskPipelineRunV4
LeanExtractionReportFull2D
GeometryFull2DClaimSpec
ProviderRunManifestFull2D
EngineOutputFull2D
IndependentCheckerReportFull2D
SelectedSolverDerivationV2
CompilerResultFull2D
LeanPatchCandidateFull2D
ProofWorkerResultFull2D
FinalVerifyReportFull2D
SolverCausalityReportV3
SolverBackedProofCertificateFull2D
GoalPreservationReportV2
```

Every validator must have positive and negative tests. Negative tests must include target fact without derivation, naked target assertion, proof text in engine output, report-only causality, hash mismatch, stale artifact, and identity-rule counted success.

### Acceptance

`python scripts/check_schema_validators_v0_5.py --self-test` passes.

## WP-04 — Corpus system without proof coupling

### Tasks

1. Implement `discover_external_goal_sources_v0_5.py`.
2. Implement `import_external_goal_preserved_v0_5.py` with machine-checkable goal preservation.
3. Implement `generate_sealed_adversarial_holdout_v0_5.py`, but do not generate counted SealedAdversarialHoldout tasks before WP-10A implementation freeze.
4. The sealed generator must not import/read provider, compiler, rule registry, Lean facade proof lemmas, proof worker, final verifier, run records, matrix, previous releases, or proof labels.
5. The sealed generator must emit theorem statements and metadata only. It must not emit rule ids, engine roles, proof text, target_shape_id, template id, expected proof label, expected compiler rule, or solver hint.
6. Implement `check_corpus_independence_v0_5.py`, `check_corpus_statement_diversity_v0_5.py`, and `check_goal_preservation_reports_v0_5.py`.
7. Pre-freeze corpus tests may use fixtures only. Fixture success is not counted release evidence.

### Acceptance

The corpus checkers reject target-shape menus, proof labels, rule ids in metadata, engine role hints, projection positives, weak goal-preservation self-attestation, and insufficient skeleton diversity.

## WP-05 — Structured Lean extraction per theorem

### Tasks

1. Implement Lean-side extraction command for each theorem.
2. Python wrapper may locate theorem source but must not classify semantics.
3. Extraction report must bind source file hash, theorem statement hash, elaborated expression hash, and target classification.
4. Run extraction for 100% of counted positives and negative tasks used in metrics.

### Acceptance

`check_full2d_extraction_corpus_v0_5.py` passes and rejects smoke-only extraction, hand-written JSON, stale cache, and Python semantic classification fixtures.

## WP-06 — Provider / engine stage boundary

### Tasks

1. Implement provider CLI as a separate stage: `python -m plugins.geometry_full2d.provider_cli`.
2. Provider receives ClaimSpec refs and writes EngineOutput artifacts before compiler starts.
3. Provider and engines must not import compiler, rule registry Lean templates, proof worker, final verifier, matrix, corpus generator, run records, or prior release modules.
4. Engine outputs must contain semantic artifacts and independent checker refs.
5. A target fact with empty premises is never a counted success. A target output may count only as the final derivation step in `SelectedSolverDerivationV2` with selected non-target inputs, selected construction, or selected certificate.

Required engine roles:

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

### Acceptance

`check_provider_stage_boundary_v0_5.py --self-test` and `check_engine_outputs_v0_5.py --run-dir ...` pass. RedCase_TargetFactProvider, RedCase_NakedTargetAssertion, RedCase_ProviderImportsCompiler fail.

## WP-07 — Independent solver checkers

### Tasks

Implement independent checkers for:

```text
synthetic trace replay
construction existence / side-condition validation
algebraic certificate replay
metric/angle relation replay
order/case split validation
inequality certificate replay
Lean-search certificate check
external trace normalization replay
```

Checker must recompute from ClaimSpec and upstream artifacts. It may not trust engine booleans or target conclusions.

### Acceptance

`check_independent_solver_checkers_v0_5.py --run-dir ... --self-test` passes and rejects mutated facts, missing premises, naked targets, and self-certified checker reports.

## WP-08 — RuleRegistry with non-identity counted rules

### Tasks

1. Implement RuleRegistryFull2D with explicit contracts.
2. Identity/direct-facade rules may exist only as non-counted helpers.
3. Every counted rule must have input/output patterns, side conditions, Lean template, independent checker, positive fixtures, negative fixtures, mutation fixtures.
4. Used-rule coverage counts only certificate-bound, compiler-consumed, mutation-sensitive, final-theorem-successful non-identity rules.

### Acceptance

`check_full2d_rule_registry_v0_5.py --self-test` passes and rejects identity-rule registries and naked-target rule registries.

## WP-09 — Compiler from SelectedSolverDerivation only

### Tasks

1. Implement compiler CLI accepting only ClaimSpec ref, SelectedSolverDerivationV2 ref, RuleRegistry ref, and side-condition checker refs.
2. Compiler must not read corpus manifest, benchmark config, task id, theorem family, grammar family, difficulty tier, source ref, target_shape_id, template id, baseline id for proof decisions.
3. Compiler must not branch on target expression shape.
4. Compiler output proof must cite solver-derived facts / constructions / certificates and generated obligations.
5. Taint checker must mutate forbidden metadata; compiler output must be unchanged when only forbidden metadata changes and must change/fail when selected solver derivation changes.

### Acceptance

`check_compiler_input_isolation_v0_5.py --self-test` and `check_compiler_taint_v0_5.py --run-dir ...` pass. RedCase_ProofFromShapeCompiler and RedCase_RuleListArtifactSynthesis fail.

## WP-10 — ProofWorker and FinalVerifyGate

### Tasks

1. ProofWorker applies `LeanPatchCandidateFull2D` only inside MARP proof region.
2. Source theorem must be sorry-only before pipeline execution.
3. FinalVerifyGate runs `lake env lean` on generated candidate, checks theorem statement unchanged, no sorry, no forbidden declarations, no toy target definitions, admitted imports only.

### Acceptance

`check_proof_worker_final_verify_v0_5.py --run-dir ... --self-test` passes.

## WP-10A — Implementation freeze and counted corpus materialization

### Tasks

1. Create a freeze manifest binding current git head, selected implementation hash, checker hashes, config hash, corpus-tool hashes, and admitted release entrypoints.
2. After the freeze manifest exists, generate the counted SealedAdversarialHoldout corpus.
3. Import ExternalGoalPreserved tasks only with independent machine-checked GoalPreservationReportV2 evidence.
4. Re-run corpus independence, statement diversity, and goal preservation checkers against the counted corpus.
5. Any later change to provider, compiler, rule registry, proof worker, final verifier, matrix runner, release checker, corpus generator, or checker code invalidates the freeze manifest and requires regenerated holdout and fresh checker evidence.

### Acceptance

`check_corpus_independence_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5 --freeze-manifest ...`, `check_corpus_statement_diversity_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5`, and `check_goal_preservation_reports_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5` pass on the counted corpus. RedCase_SealedChallengeImportsCompiler, RedCase_TargetShapeMenuCorpus, RedCase_ProjectionCorpusCounted, and RedCase_GoalPreservationSelfAttestation fail for their expected K blockers.

## WP-11 — Actual matrix execution and baselines

### Tasks

1. Implement `run_full2d_matrix_v0_5.py` to execute all required baselines for every counted task through the same task pipeline.
2. B1/B2/B5/B6/B7/conditional B8 must all produce `ActualTaskPipelineRunV4` final release records.
3. Baseline differences are config-disabled components only.
4. Matrix must not compute outcomes from theorem family, corpus labels, or target shape.
5. `final_theorem` status must come from `FinalVerifyReportFull2D` per record.
6. `measured_failure` status must come from `FinalVerifyReportFull2D`, `StageFailureReportV1`, or `DisabledStageReportV1`; fake downstream success artifacts are forbidden.
7. Conditional B8 must be explicitly resolved in config and report. If B8 is enabled, it must run for every counted task. If it is not applicable, the report must include checked evidence for that status and B2 metrics must be independent of B8.

### Acceptance

`check_full2d_baseline_comparability_v0_5.py --run-dir ...` passes. RedCase_FamilyCodedBaseline and RedCase_B8SilentlyOmitted fail.

## WP-12 — Live destructive solver causality reruns

### Tasks

Implement `run_solver_causality_mutations_v0_5.py` after WP-11 matrix execution to run for every counted B2 `final_theorem` success:

```text
positive_control
remove_selected_solver_artifact
corrupt_selected_fact_or_construction
corrupt_certificate_or_checker_output
unsupported_rule_mutation
side_condition_mutation
```

Each mutation must create a fresh temp run directory, rerun compiler -> ProofWorker -> FinalVerifyGate, and record command logs, hashes, outputs, and failure reason. Precomputed reports are invalid.

### Acceptance

`check_solver_causality_reports_v0_5.py --run-dir ... --self-test` passes and rejects field-only, stale, no-rerun, and no-command-log reports.

## WP-13 — Metrics and summaries

### Tasks

Compute metrics from actual records and live causality reports only:

```text
B2 final theorem rate
B2 solver-causal final theorem rate
destructive causality pass rate
non-target-intermediate success fraction
construction/case/certificate success fraction
direct/wrapped facade lemma fraction
used-rule coverage
engine contribution
baseline advantage
measured failures
freshness / hash binding
```

### Acceptance

`check_full2d_metrics_v0_5.py --run-dir ...` passes and rejects label-derived, empty, stale, and B2-only metrics.

## WP-14 — Final release and closure

### Tasks

1. Run final release command with `--fresh-run`.
2. Ensure `release_blockers=[]`, `hard_blockers=[]`, `work_debt_open=[]`, `closure_allowed=true`.
3. Ensure every K requirement has an executed checker result.
4. Ensure `closure_claim_ceiling` is emitted by the release report and checked by `check_closure_claim_ceiling_v0_5.py --allow-missing-closure`.
5. Write closure only after final acceptance passes.
6. Re-run `check_closure_claim_ceiling_v0_5.py` without `--allow-missing-closure` after `CLOSURE.md` is written.

### Acceptance

`CLOSURE.md` may claim only `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` and must list non-claims for natural-language fidelity, open-problem solving, TongGeometry model-backed readiness, production safety, and correctness outside target.
