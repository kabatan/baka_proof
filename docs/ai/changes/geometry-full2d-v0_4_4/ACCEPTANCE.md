---
title: "Guardian Acceptance — GeometryFull2D v0.4.4 Real Solver-Causal Pipeline Reviewed"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-009"
base_spec: "MARP-GEOLEAN-BASE-009"
plan: "MARP-GEOLEAN-PLAN-009"
revision: "reviewed-2026-06-18"
status: "USER_APPROVED_ACTIVE"
---

# Guardian Acceptance — GeometryFull2D v0.4.4 Reviewed

## 0. Final acceptance command

```bash
python scripts/check_release_acceptance_v0_4_4.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_4/evidence/release_acceptance_report.json
```

The command must return 0 only when all acceptance requirements pass.

## 1. Required nonempty release report fields

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

Empty placeholder fields fail `K-001`.

`checked_rids` must be populated only with concrete requirement identifiers from `MARP-GEOLEAN-BASE-009 / PLAN-009 / ACCEPTANCE-009`, including applicable `DR-009-*`, `I-*`, `K-*`, and Plan work-package acceptance gates.

`freshness_summary` must prove that reused checker, matrix, corpus, and report outputs are bound to the current repository tree or selected implementation hash, corpus hash, config hash, run directory hash, and checker code hash as applicable.

`family_floor_summary` must report every positive family floor from Base Spec section 4.2 and fail if any family is below its floor.

## 2. Blocker list

### K-001 — Empty summaries

Fail if any required summary is empty, missing, or contains only placeholder values.

### K-002 — Open debt

Fail if any DebtLedger entry has `status != closed`.

### K-003 — Missing ActualTaskPipelineRunV2

Fail if any counted positive final theorem lacks a valid ActualTaskPipelineRunV2.

### K-004 — Projection-only counted success

Fail if any counted positive task has category `ProjectionNonCounted`, preservation kind `projection_not_counted`, or goal-preservation evidence showing target simplification.

### K-005 — Template proof selection

Fail if compiler, proof worker, or proof candidate generator selects proof text from `task_id`, `theorem_name`, `template_id`, `theorem_family`, `grammar_family`, `difficulty_tier`, `provenance`, `source_ref`, or generator-private labels.

### K-006 — Fabricated solver reference

Fail if any normalized solver ref or engine output ref is derived from `task_id`, theorem name, template id, benchmark label, or a non-engine payload.

### K-007 — Sidecar / overlay matrix

Fail if matrix success can be computed without executing or replaying valid ActualTaskPipelineRunV2 records.

### K-008 — Smoke-only extraction

Fail if extraction evidence comes from a fixed smoke theorem, hand-written JSON not tied to the source theorem hash, stale extraction cache, or Python semantic classification.

### K-009 — Corpus floors insufficient

Fail if corpus floors are not met:

```text
positive formal Lean tasks >= 3350
negative / target-outside / malformed >= 500
ExternalGoalPreserved positives >= 700
SealedSolverChallenge positives >= 1200
ProjectionNonCounted positives counted as release positives = 0
near duplicate positives <= 10%
exact target-shape duplicate max per theorem family <= 5
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

`UserReviewedGoal` has no fixed floor. If present, every UserReviewedGoal must pass ReviewManifest validation.

### K-010 — External goal not preserved

Fail if an ExternalGoalPreserved task lacks a passing GoalPreservationReportV1 with preservation kind in:

```text
exact_same_formal_goal
structurally_preserved_by_reviewed_translator
formally_equivalent
```

Fail if the source has no explicit goal, if goal predicate family is changed without formal equivalence, or if an easier projection target is counted.

### K-011 — Source theorem pre-proved

Fail if any counted positive source theorem has a non-sorry proof before pipeline execution.

### K-012 — Used-rule coverage insufficient

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

### K-013 — Engine contribution insufficient

Fail if any release-critical engine role is never consumed in counted B2 final theorem certificates and solver-causality reports.

### K-014 — Engine output proof text

Fail if engine output contains Lean proof text, tactic scripts, theorem-specific proof replacement text, or target theorem names used for proof generation.

### K-015 — Compiler input isolation violated

Fail if compiler release path reads any Base-forbidden proof-decision field, including `task_id`, `theorem_name` except for patch anchoring, `theorem_family`, `grammar_family`, `difficulty_tier`, `template_id`, `provenance`, `source_ref` except for artifact bookkeeping, benchmark labels, corpus generator private labels, or proof text embedded in corpus metadata.

### K-016 — Solver causality missing

Fail if any B2 counted final theorem success lacks a passing SolverCausalityReportV1.

### K-017 — Solver causality mutation failure

Fail if removing or corrupting the selected normalized solver artifact still produces the same counted patch and final theorem.

### K-018 — Direct/wrapped facade lemma dominance

Fail if B2 counted successes exceed:

```text
direct_or_wrapped_facade_lemma_success_fraction <= 0.10
```

Direct/wrapped includes `exact lemma`, direct `have` wrapper around exact lemma, field-evidence projection, and one-step facade theorem matching target. A direct lemma can count only if it is solver-causal and under the ceiling.

### K-019 — Insufficient solver-causal successes

Fail if:

```text
solver_causal_success_fraction < 1.00
non_target_intermediate_fact_success_fraction < 0.50
construction_or_case_or_certificate_success_fraction < 0.50
ExternalGoalPreserved_success_count < 500
SealedSolverChallenge_success_count < 700
```

### K-020 — Baseline comparability violated

Fail if baselines differ except for the declared disabled component. Fail if B8 is required but missing, or if B8 is required when no model provider is enabled.

### K-021 — Advantage thresholds fail

Fail if:

```text
B2 - B1 overall < 0.25
B2 - B5 construction subset < 0.15
B2 - B6 algebraic/metric subset < 0.15
B2 - B7 order/case subset < 0.10
B2 - B8 model-disabled olympiad subset < 0.05, only when B8 is required
```

If no model provider is enabled, B8 threshold is not applicable and the report must explicitly say `not_applicable_model_provider_not_used`.

### K-022 — Final theorem thresholds fail

Fail if any family or overall final theorem rate in Base Spec falls below threshold.

### K-023 — Challenge suite insufficient

Fail if any engine challenge suite is missing, dominated by reflexivity/symmetry/direct lemma tasks, or below its pass floor.

### K-024 — Regression failure suite missing

Fail if regression tests do not prove v0.4.2/v0.4.3 shortcuts and v0.4.4 bypasses fail.

### K-025 — Closure exceeds evidence

Fail if closure claims more than release report supports.

### K-026 — Stale or hash-unbound evidence

Fail if release acceptance relies on stale v0.4.2/v0.4.3 evidence, stale v0.4.4 checker or matrix outputs, or any reused output not bound to the current repository tree or selected implementation hash, corpus hash, config hash, run directory hash, and checker code hash as applicable.

### K-027 — Renamed old release path

Fail if a renamed, wrapped, copied, shimmed, or substantially equivalent v0.4.2/v0.4.3 release path is accepted as a v0.4.4 release path instead of being treated as a regression fixture that fails acceptance.

## 3. Required checker commands

The final release checker must invoke or verify outputs from:

```bash
python scripts/check_active_guardian_spec_v0_4_4.py
python scripts/check_no_projection_release_path_v0_4_4.py
python scripts/check_anti_v043_projection_regression.py
python scripts/check_full2d_corpus_manifest_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_goal_preservation_reports.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_review_manifest_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_sealed_challenge_manifest.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_positive_source_theorems_sorry_only.py --corpus-root benchmarks/geometry_full2d_v0_4_4
python scripts/check_full2d_extraction_corpus_v0_4_4.py --corpus-root benchmarks/geometry_full2d_v0_4_4 --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_full2d_claimspec_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_engine_challenge_suite_v0_4_4.py --all-engines
python scripts/check_full2d_engine_real_execution_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_engine_no_proof_text_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_compiler_input_isolation_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_compiler_evidence_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_solver_causality_reports_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_proof_worker_hardening_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_full2d_final_verify_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/check_actual_task_pipeline_runs_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4 --self-test
python scripts/run_full2d_matrix_v0_4_4.py --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml --run-dir runs/geometry_full2d_v0_4_4 --execute-all
python scripts/check_full2d_matrix_evidence_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_full2d_metrics_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_full2d_used_rule_coverage_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_full2d_engine_contribution_v0_4_4.py --run-dir runs/geometry_full2d_v0_4_4
python scripts/check_v0_4_4_regression_failures.py
```

## 4. Required report shape

```yaml
ReleaseAcceptanceReportV0_4_4:
  schema_version: "1.0.0"
  status: "passed | failed"
  claim_ceiling: "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY | blocked"
  hard_blockers: []
  release_blockers: []
  work_debt_open: []
  checked_rids: []
  freshness_summary: {}
  family_floor_summary: {}
  corpus_summary: {}
  corpus_goal_preservation_summary: {}
  metrics_summary: {}
  advantage_summary: {}
  used_rule_coverage_summary: {}
  engine_usage_summary: {}
  engine_contribution_summary: {}
  solver_causality_summary: {}
  actual_pipeline_run_summary: {}
  measured_failure_summary: {}
  challenge_suite_summary: {}
  regression_failure_summary: {}
  baseline_comparability_summary: {}
  debt_ledger_summary: {}
  b8_applicability: "required | not_applicable_model_provider_not_used"
  closure_allowed: true | false
```

## 5. Acceptance-negative tests

Each checker must include self-tests proving it fails on:

```text
v0.4.2 overlay success
v0.4.3 projection corpus counted as external
compiler using template_id
compiler using task_id
compiler using theorem_family
compiler using grammar_family
compiler using provenance/source_ref/generator-private labels
engine proof text leakage
missing solver causality report
stale ActualTaskPipelineRunV2 record
mutated solver artifact still producing same patch
renamed/shimmed v0.4.3 release path accepted as v0.4.4
stale checker, matrix, corpus, or release output accepted without current hash binding
direct lemma wrapper counted as solver intermediate
open DebtLedger entry ignored
source theorem already proved
smoke extraction reused across tasks
UserReviewedGoal without review manifest
B8 omitted when model provider is enabled
B8 required when no model provider is enabled
```
