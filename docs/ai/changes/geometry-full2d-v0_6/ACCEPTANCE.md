---
title: "Guardian Acceptance — GeometryFull2D v0.6 Execution-Locked Full Pipeline Reviewed Strict"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-012"
base_spec: "MARP-GEOLEAN-BASE-012"
plan: "MARP-GEOLEAN-PLAN-012"
status: "USER_APPROVED_ACTIVE"
revision: "reviewed-strict-2026-06-20"
---

# Guardian Acceptance — GeometryFull2D v0.6

Final claim target: `V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`

## Final release command

```bash
python scripts/check_release_acceptance_v0_6.py   --config configs/benchmark_runs/geometry_full2d_v0_6.yaml   --fresh-run   --fail-on-stale   --no-skip   --all-baselines   --live-mutations   --output docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json
```

This command must return 0 only if all K requirements below pass. A checker warning is not enough; any failed K requirement becomes a release blocker.

## Required report fields

The release report must include nonempty:

```text
checked_rids
freshness_summary
red_case_summary
acceptance_coverage_summary
schema_contract_summary
extraction_summary
claimspec_summary
provider_isolation_summary
engine_output_not_from_compiler_rules_summary
solver_artifact_check_summary
selected_derivation_summary
derivation_target_matcher_summary
compiler_input_lock_summary
rule_registry_summary
proof_worker_final_verify_summary
live_causality_summary
corpus_independence_summary
statement_diversity_summary
all_baseline_matrix_summary
metrics_summary
advantage_summary
used_rule_coverage_summary
engine_contribution_summary
measured_failure_summary
closure_claim_ceiling_summary
K_to_checker_evidence_map
```

Empty placeholder fields fail `K-001`.

## K requirements

### K-001 Active authority
Exactly one active GeometryFull2D Base Spec: `MARP-GEOLEAN-BASE-012`.

### K-002 Old closure invalidation
v0.4.x, draft v0.5, and prior v0.5 closures/release artifacts are historical evidence only and cannot be release evidence.

### K-003 Red-case suite must run first
`check_red_case_suite_v0_6.py --all` must run and reject all generalized red-case classes with positive controls.

### K-004 Acceptance coverage
Every K requirement must map to an executed checker and evidence field. Missing mapping fails.

### K-005 No checker whitelist
If a forbidden shortcut is detected in a release entrypoint, release fails. Filename, role, comment, or directory based suppression is forbidden for release files.

### K-006 Fresh run evidence
Final release must use a fresh run directory created by final release command. Closure mode disallows stale replay by default.

### K-007 No target-fact provider
Any selected provider/engine output whose only selected fact is the final target with empty premises and no checked derivation fails.

### K-008 Provider isolation
Provider/engine imports downstream proof modules or corpus/matrix/release modules => fail.

### K-009 Engine artifacts independently checked
Every selected fact/construction/certificate must have `IndependentSolverArtifactCheckV1(status=passed)` from a checker independent of provider and compiler.

### K-010 No proof text in engine output
Engine output containing Lean proof text, tactic script, Lean lemma template id, proof replacement text, or final target proof text fails.

### K-011 No rule-list artifact synthesis
Engine output derived from compiler-selected `used_rules`, rule registry output, or proof plan fails.

### K-012 Rule registry semantic integrity
Counted registry must have >=35 non-alias semantic rules across >=15 families. Identity/direct/facade rules cannot count. Rule-level negative fixtures must fail.

### K-013 Selected derivation non-target requirement
Every B2 counted success must have a selected semantic non-target intermediate or checked construction/certificate/case split. Alpha-renamed target equivalents, target-hash intermediates, trivial target wrappers, reflexivity/symmetry-equivalent targets, direct-facade target intermediates, and intermediates that normalize to the target without checked solver construction/certificate/side-condition/case-split evidence do not count.

### K-014 Derivation target matcher isolation
Target matching must be a separate stage and must not output proof text, target expression strings, strategy labels, rule ids, or corpus labels.

### K-015 Compiler input lock
Compiler must accept only TheoremAnchor, SelectedSolverDerivation, RuleRegistrySnapshot, and side-condition reports. It cannot branch on target shape/corpus metadata.

### K-016 No proof-from-shape
Static and dynamic taint tests must prove target shape / theorem family / task id / target_shape_id / source_ref / category / theorem name / statement hash / proof-region identity / binder-map identity / any `TheoremAnchorV1` identifier field do not determine proof text, rule plan, rule selection, lemma selection, derivation-step ordering, or proof strategy.

### K-017 ProofWorker/final verify strictness
ProofWorker cannot claim final theorem; FinalVerifyGate must compile candidate and reject sorry/admit/axiom/unsafe/toy target/protected theorem mutation/stale candidate.

### K-018 Live destructive causality
Every B2 counted final theorem success must have live causality reruns. Field-only causality fails.

### K-019 Mutation sensitivity
For every B2 counted success, removing/corrupting selected solver artifact, unsupported rule mutation, side-condition mutation, checker transcript removal, or certificate corruption must prevent the same counted final theorem.

### K-020 Corpus categories
Counted positives may only be ExternalGoalPreserved, SealedAdversarialHoldout, UserReviewedGoal. Projection tasks are non-counted fixtures.

### K-021 Goal preservation
ExternalGoalPreserved requires machine-checkable goal preservation or formal equivalence. Source_ref-only or point/predicate reuse fails.

### K-022 Sealed challenge independence
Sealed generator must be post-freeze and cannot import/read provider/compiler/rule-registry/proof/final/matrix/release code or proof labels.

### K-023 Corpus diversity floors
Pass only if:

```text
counted positives >= 1200
negative/malformed/target-outside >= 200
unique normalized target ASTs >= 900
unique hypothesis-target dependency signatures >= 700
near duplicate fraction <= 0.05
direct/facade lemma eligible fraction <= 0.05
construction/case/certificate-required tasks >= 600
multi-step derivation required tasks >= 800
no family > 20% counted positives
no target predicate family > 30% counted positives
```

### K-024 All-baseline matrix
All counted tasks must have B1/B2/B5/B6/B7 and conditional B8 records from actual pipeline execution. B2-only matrix fails.

### K-025 No family-coded baseline
Baseline outcome cannot depend on theorem family/category/target type labels. It must arise from actual disabled artifacts/stages.

### K-026 Metrics from actual records only
Metrics and advantages must be computed from `ActualTaskPipelineRunV4` and `SolverCausalityLiveRunV1`, not corpus labels or summaries.

### K-027 Success thresholds
Release requires all Base Spec minimum metrics.

### K-028 Engine contribution
Every release-critical engine role from the exact `ReleaseCriticalEngineRoleV1` list in Base Spec DR-012-015 that is enabled for an enabled corpus subset must contribute to at least one counted B2 final theorem success in its mapped subset. The enabled role set must be derived from corpus metadata and config before provider execution. A measured unavailability/debt report may explain a measured failure or ReleaseBlocker, but it cannot satisfy the final release metric for an enabled release-critical engine role. Cosmetic, post-hoc, or narrowly redefined engine roles fail.

### K-029 Used rule coverage
Used rule count/family thresholds must be certificate-bound, compiler-consumed, mutation-sensitive, and final-theorem successful.

### K-030 Measured failures honest
Measured failures must be actual stage failures or disabled-stage reports, not label-coded failures.

### K-031 Stale evidence
No stale v0.4.x / draft v0.5 / prior v0.5 / previous v0.6 evidence may be used in closure mode. Closure mode requires fresh run by default.

### K-032 Closure ceiling
Closure claim must be generated from release report. Manual closure claim or claim beyond report fails.

### K-033 Nonessential blocker discipline
External source unavailability, model B8 absence, and performance failures are ReleaseBlockers/MeasuredFailures, not HardBlockers, unless they create unsound proof-use.


### K-034 Checker cannot fabricate pipeline evidence

Release checker and helper checkers must not fabricate provider, engine, compiler, FinalVerify, matrix, or causality success artifacts. They may only validate or execute the pipeline. Any checker-generated success artifact that is not a red-case fixture is a release blocker.

### K-035 Release checker invokes all required checkers

`check_release_acceptance_v0_6.py` must invoke every checker listed in this Acceptance document and must fail if any required checker is absent from the release report, returns nonzero, emits an empty report, or lacks an evidence ref.

## Required checkers

The final release checker must invoke at least:

```text
check_active_guardian_spec_v0_6.py
check_red_case_suite_v0_6.py --all
check_acceptance_coverage_v0_6.py
check_no_old_release_dependency_v0_6.py
check_schema_contracts_v0_6.py --self-test --red-cases
check_full2d_extraction_corpus_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --run-dir <fresh>
check_full2d_claimspec_v0_6.py --run-dir <fresh> --self-test
check_provider_isolation_v0_6.py --run-dir <fresh> --red-cases
check_engine_output_not_from_compiler_rules_v0_6.py --run-dir <fresh> --red-cases
check_independent_solver_artifacts_v0_6.py --all --red-cases
check_rule_registry_v0_6.py --release --red-cases
check_selected_derivation_v0_6.py --run-dir <fresh> --red-cases
check_derivation_target_matcher_v0_6.py --run-dir <fresh> --red-cases
check_compiler_input_lock_v0_6.py --self-test --red-cases --dynamic-taint
check_proof_worker_final_verify_v0_6.py --self-test --red-cases
check_corpus_independence_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --red-cases
check_statement_diversity_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6
run_full2d_matrix_v0_6.py --config ... --run-dir <fresh> --execute-all --all-baselines --no-skip
check_all_baseline_matrix_v0_6.py --run-dir <fresh> --red-cases
run_solver_causality_live_v0_6.py --run-dir <fresh> --all-b2-successes
check_solver_causality_live_v0_6.py --run-dir <fresh> --red-cases
check_full2d_metrics_v0_6.py --run-dir <fresh>
check_used_rule_coverage_v0_6.py --run-dir <fresh> --red-cases
check_engine_contribution_v0_6.py --run-dir <fresh> --red-cases
check_closure_claim_ceiling_v0_6.py
```

`check_release_acceptance_v0_6.py` must fail if any K requirement is not represented in the K-to-checker evidence map.


## Mandatory final release flags

The final closure release command must include all of these flags exactly in closure mode:

```text
--fresh-run
--fail-on-stale
--no-skip
--all-baselines
--live-mutations
```

A release command that omits any of these flags is a release blocker.
