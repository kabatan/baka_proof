---
title: "Guardian Acceptance — GeometryFull2D v0.4.5 Real Solver-Causal Full Pipeline"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-010"
base_spec: "MARP-GEOLEAN-BASE-010"
plan: "MARP-GEOLEAN-PLAN-010"
status: "USER_APPROVED_ACTIVE"
revision: "reviewed-2026-06-18-no-shortcuts"
---

# Guardian Acceptance — GeometryFull2D v0.4.5

Claim target: `V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`

## 0. Final command

```bash
python scripts/check_release_acceptance_v0_4_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_5/evidence/release_acceptance_report.json
```

The command must return 0 only when all acceptance requirements pass.

## 1. Required report fields

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

Empty placeholder fields fail K-001.

## 2. Blockers

### K-001 — Empty summaries

Fail if any required summary is empty, missing, stale, or contains only placeholder values.

### K-002 — Open debt

Fail if any DebtLedger entry has `status != closed`.

### K-003 — Missing ActualTaskPipelineRunV3

Fail if any counted positive final theorem lacks a valid ActualTaskPipelineRunV3 with all required artifact refs.

### K-004 — Counted projection

Fail if any counted positive task has category `ProjectionNonCounted`, preservation kind `projection_not_counted`, point/predicate pool reuse without goal preservation, or goal-preservation evidence showing target simplification.

### K-005 — Proof selected from metadata or target-shape menu

Fail if compiler, proof worker, provider, engine, or proof candidate generator selects proof text from:

```text
task_id, theorem_name except patch anchoring, template_id, theorem_family,
grammar_family, difficulty_tier, category, provenance, source_ref,
projection_kind, target_shape_id, raw target expression alone, fixed target-shape menu.
```

Static patterns such as `_proof_from_shape`, `_proof_from_source`, `target_expr.startswith`, `proof_text_for_template`, and target-shape-to-lemma dispatch in release paths fail. Dynamic taint tests must also fail if target metadata is sufficient to produce the same proof patch without solver facts.

### K-006 — Fabricated solver artifact

Fail if any normalized solver artifact, selected derivation, engine output ref, or solver fact is derived from task id, theorem name, template id, benchmark label, compiler-selected rule list, or non-engine payload rather than actual engine output.

### K-007 — Engine output lacks real execution

Fail if an engine output sets `real_integration_flag=true` without a valid `real_integration_evidence_ref`, deterministic replay, code hash, input hash, output hash, and non-template challenge transcript.

### K-008 — Engine output contains proof text

Fail if engine output contains Lean proof text, tactic scripts, theorem-specific proof replacement text, target theorem names used for proof generation, or expected proof labels.

### K-009 — Compiler consumed no solver facts

Fail if a counted final theorem's compiler result lacks consumed solver fact, construction, or certificate ids from selected solver artifacts.

### K-010 — Missing SelectedSolverDerivationV1

Fail if a counted final theorem lacks `SelectedSolverDerivationV1`, or if the derivation can be constructed from ClaimSpec alone.

### K-011 — Solver causality missing

Fail if any counted B2 final theorem success lacks a passing SolverCausalityReportV2 with destructive rerun artifacts.

### K-012 — Solver causality destructive test missing or ineffective

Fail if deleting or corrupting selected solver artifacts still produces the same counted patch and final theorem. Fail if the causality checker only reads boolean fields.

### K-013 — Proof-from-shape survived mutation

Fail if the compiler can still produce the counted proof patch when selected solver artifacts are absent, irrelevant, corrupted, or replaced by unsupported rules.

### K-014 — Baseline outcome is label-coded

Fail if baseline outcome is computed from baseline id, theorem family, grammar family, task category, or label instead of actual missing artifacts caused by the disabled component.

### K-015 — External goal not preserved

Fail if ExternalGoalPreserved lacks GoalPreservationReportV2 with exact, formally equivalent, or machine-checked structure-preserving mapping. Fail if checker evidence is created by the same generator without independent validation. Fail if source goal predicate family, arity, or hypotheses are changed without a formal equivalence artifact.

### K-016 — Corpus floors fail

Fail if corpus floors are not met:

```text
positive formal Lean tasks >= 3350
negative / target-outside / malformed >= 500
ExternalGoalPreserved positives >= min(700, available_external_goal_preserved_count_after_discovery)
SealedPostImplementationChallenge positives >= 1200 + external_goal_preserved_deficit
ProjectionNonCounted counted positives = 0
near duplicate positives <= 10%
exact target-shape duplicate max per theorem family <= 5
logical proof-schema duplicate max per theorem family <= 5
one-step facade-lemma theorem fraction <= 0.05
```

UserReviewedGoal has no fixed floor. If present, each UserReviewedGoal must pass ReviewManifest validation.

Definitions used by this checker:

```text
admitted_external_goal_preserved_count = number of counted ExternalGoalPreserved positives accepted by GoalPreservationReportV2.
external_goal_preserved_deficit = max(0, 700 - admitted_external_goal_preserved_count).
admitted_external_goal_preserved_success_count = B2 final theorem successes among admitted ExternalGoalPreserved tasks.
external_success_deficit = max(0, min(500, admitted_external_goal_preserved_count) - admitted_external_goal_preserved_success_count).
```

### K-017 — Source theorem pre-proved

Fail if any counted positive source theorem has a non-sorry proof before pipeline execution.

### K-018 — Sealed challenge invalid or stale

Fail if sealed challenges are generated before implementation freeze, generated by importing provider/compiler/rule registry/proof worker/matrix/release checker, include proof hints, or are stale after implementation code changes.

### K-019 — Direct/wrapped facade lemma dominance

Fail if B2 counted successes exceed:

```text
direct_or_wrapped_facade_lemma_success_fraction <= 0.05
```

Direct/wrapped includes exact lemma, direct `have` wrapper around exact lemma, field-evidence projection, and one-step facade theorem matching target. A direct lemma can count only if solver-causal and under the ceiling.

### K-020 — Solver-causal success thresholds fail

Fail if:

```text
solver_causal_success_fraction < 1.00
destructive_rerun_success_fraction < 1.00
non_target_intermediate_fact_success_fraction < 0.50
construction_or_case_or_certificate_success_fraction < 0.50
ExternalGoalPreserved_success_count < min(500, admitted_external_goal_preserved_count)
SealedPostImplementationChallenge_success_count < 700 + external_success_deficit
```

### K-021 — Rule coverage insufficient

Fail if B2 counted successes do not meet:

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

### K-022 — Engine contribution insufficient

Fail if any release-critical engine role is never consumed in counted B2 final theorem certificates and solver-causality reports.

### K-023 — Compiler input isolation violated

Fail if compiler release path reads any Base-forbidden proof-decision field or can decide proof text from target shape without selected solver derivation.

### K-024 — Baseline comparability violated

Fail if baselines differ except for the declared disabled component. Fail if B8 is required but missing, or if B8 is required when no model provider is enabled.

### K-025 — Advantage thresholds fail

Fail if:

```text
B2 - B1 overall < 0.25
B2 - B5 construction subset < 0.15
B2 - B6 algebraic/metric subset < 0.15
B2 - B7 order/case subset < 0.10
B2 - B8 model-disabled olympiad subset < 0.05, only when B8 is required
```

If no model provider is enabled, B8 threshold is not applicable and the report must explicitly say `not_applicable_model_provider_not_used`.

### K-026 — Final theorem thresholds fail

Fail if any family or overall final theorem rate in Base Spec falls below threshold.

### K-027 — Challenge suite insufficient

Fail if any engine challenge suite is missing, dominated by reflexivity/symmetry/direct lemma tasks, or below its pass floor.

### K-028 — Regression failure suite missing

Fail if regression tests do not prove v0.4.2/v0.4.3/v0.4.4 shortcuts and v0.4.5 bypasses fail.

### K-029 — Closure exceeds evidence

Fail if closure claims more than release report supports.

### K-030 — Stale or hash-unbound evidence

Fail if release acceptance relies on stale v0.4.2/v0.4.3/v0.4.4 evidence, stale v0.4.5 checker or matrix outputs, or any reused output not bound to current repository tree / selected implementation hash / corpus hash / config hash / run directory hash / checker code hash.

### K-031 — Renamed old release path

Fail if a renamed, wrapped, copied, shimmed, or substantially equivalent v0.4.2/v0.4.3/v0.4.4 release path is accepted as v0.4.5 release path instead of regression fixture.

### K-032 — Unchecked solver fact or compiler-generated engine artifact

Fail if a consumed solver fact/construction/certificate lacks independent checker evidence, if an engine emits a naked target assertion with no checked trace/certificate, or if provider/engine code imports release compiler/proof-generation modules.

## 3. Required checker commands

The final release checker must invoke or verify outputs from:

```bash
python scripts/check_active_guardian_spec_v0_4_5.py
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py
python scripts/check_full2d_corpus_manifest_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_goal_preservation_reports_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_external_source_availability_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_sealed_challenge_manifest_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_counted_sources_sorry_only_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_corpus_no_proof_coupling_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5
python scripts/check_full2d_extraction_corpus_v0_4_5.py --corpus-root benchmarks/geometry_full2d_v0_4_5 --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_claimspec_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_full2d_engine_challenge_suite_v0_4_5.py --all-engines
python scripts/check_full2d_engine_real_execution_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_full2d_engine_no_proof_text_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_engine_output_not_from_compiler_rules_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_solver_fact_independent_checkers_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_full2d_compiler_input_isolation_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_compiler_taint_v0_4_5.py
python scripts/check_full2d_compiler_evidence_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_selected_solver_derivation_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/check_actual_task_pipeline_runs_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/run_solver_causality_mutations_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --all-b2-successes
python scripts/check_solver_causality_reports_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5 --self-test
python scripts/run_full2d_matrix_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5 --execute-all
python scripts/check_full2d_baseline_comparability_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_no_family_coded_baseline_v0_4_5.py
python scripts/check_full2d_matrix_evidence_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_metrics_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_used_rule_coverage_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_full2d_engine_contribution_v0_4_5.py --run-dir runs/geometry_full2d_v0_4_5
python scripts/check_v0_4_5_regression_failures.py
```

## 4. Closure

Create `CLOSURE.md` only after final release acceptance passes. Closure must not claim natural-language source fidelity, open-problem solving, TongGeometry model-backed readiness, or production safety.
