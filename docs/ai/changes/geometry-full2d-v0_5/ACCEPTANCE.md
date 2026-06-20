---
title: "Guardian Acceptance — GeometryFull2D v0.5 Real Solver-Causal Full Pipeline Reviewed Strict"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-011"
base_spec: "MARP-GEOLEAN-BASE-011"
plan: "MARP-GEOLEAN-PLAN-011"
claim_target: "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
status: "SUPERSEDED_BY_MARP-GEOLEAN-ACCEPTANCE-012_RETAINED_AS_PRIOR_EVIDENCE"
revision: "reviewed-strict-2026-06-18"
---

# Guardian Acceptance — GeometryFull2D v0.5 Reviewed Strict

## 0. Final command

```bash
python scripts/check_release_acceptance_v0_5.py \
  --config configs/benchmark_runs/geometry_full2d_v0_5.yaml \
  --output docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json \
  --fresh-run
```

The command returns 0 only when all K blockers are absent. It must create or validate a fresh release run directory. It must not accept stale records unless exact replay freshness is proven.

## 1. Required nonempty report fields

```text
checked_requirements
checker_coverage_matrix
red_case_summary
corpus_summary
corpus_statement_diversity_summary
extraction_summary
provider_stage_boundary_summary
engine_output_summary
independent_checker_summary
rule_registry_summary
compiler_isolation_summary
actual_pipeline_run_summary
solver_causality_summary
final_verify_summary
metrics_summary
used_rule_coverage_summary
engine_contribution_summary
baseline_comparability_summary
measured_failure_summary
debt_ledger_summary
freshness_summary
closure_claim_ceiling
closure_claim_ceiling_summary
```

## 2. K blockers

```text
K-001 Empty or placeholder summary
K-002 Checker coverage incomplete
K-003 Red case accepted
K-004 Target-fact provider
K-005 Naked target assertion
K-006 Identity/direct-facade rule counted
K-007 Proof-from-shape compiler
K-008 Engine output from compiler-selected rules
K-009 Proof text in engine output
K-010 Missing independent checker evidence
K-011 Causality report not live rerun
K-012 Destructive causality failure
K-013 Projection counted as positive
K-014 Corpus coupled to proof implementation
K-015 Sealed challenge not independent
K-016 Weak/self-attested goal preservation
K-017 Source theorem pre-proved
K-018 Engine contribution insufficient
K-019 Used-rule coverage insufficient
K-020 Direct/wrapped facade lemma dominance
K-021 Non-target intermediate insufficient
K-022 Construction/case/certificate evidence insufficient
K-023 Family-coded baseline
K-024 Baseline comparability violated
K-025 Metrics below threshold
K-026 Stale evidence
K-027 Open debt
K-028 Closure exceeds evidence
K-029 Statement diversity insufficient
K-030 Checker whitelist or suppression
K-031 Provider imports downstream proof code
K-032 Final status not from FinalVerifyReport
K-033 Matrix not all-baselines
```

Every K blocker must map to at least one executed checker in `checker_coverage_matrix`.

Existing K blockers must enforce the corresponding Base Spec floors verbatim. In particular, K-019 covers used concrete non-identity rules and used rule families, K-022 covers construction/case/certificate evidence and required-task floors, K-025 covers all release and baseline threshold failures, and K-029 covers all corpus count and statement-diversity floors. A checker that only enforces the subset listed in this Acceptance file is incomplete under K-002.

## 3. Required checker commands

The final release checker must execute or directly invoke equivalent library functions for all of:

```bash
python scripts/check_active_guardian_spec_v0_5.py
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_corpus_independence_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/check_corpus_statement_diversity_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/check_goal_preservation_reports_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/check_full2d_extraction_corpus_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5 --run-dir runs/geometry_full2d_v0_5
python scripts/check_provider_stage_boundary_v0_5.py --self-test
python scripts/check_engine_outputs_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_independent_solver_checkers_v0_5.py --run-dir runs/geometry_full2d_v0_5 --self-test
python scripts/check_full2d_rule_registry_v0_5.py --self-test
python scripts/check_compiler_input_isolation_v0_5.py --run-dir runs/geometry_full2d_v0_5 --self-test
python scripts/check_compiler_taint_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_proof_worker_final_verify_v0_5.py --run-dir runs/geometry_full2d_v0_5 --self-test
python scripts/run_full2d_matrix_v0_5.py --config configs/benchmark_runs/geometry_full2d_v0_5.yaml --run-dir runs/geometry_full2d_v0_5 --execute-all-baselines --fresh-run
python scripts/run_solver_causality_mutations_v0_5.py --run-dir runs/geometry_full2d_v0_5 --all-b2-successes --fresh-reruns
python scripts/check_solver_causality_reports_v0_5.py --run-dir runs/geometry_full2d_v0_5 --self-test
python scripts/check_full2d_baseline_comparability_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_full2d_metrics_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_full2d_used_rule_coverage_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_full2d_engine_contribution_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_debt_ledger_v0_5.py --change-dir docs/ai/changes/geometry-full2d-v0_5
python scripts/check_closure_claim_ceiling_v0_5.py --change-dir docs/ai/changes/geometry-full2d-v0_5 --release-report docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json --closure docs/ai/changes/geometry-full2d-v0_5/CLOSURE.md --allow-missing-closure
```

The final checker must fail if any command is omitted, returns nonzero, emits stale evidence, or is not represented in the release report.

## 4. Minimum report decision checks

The final checker must explicitly enforce:

```text
- red_case_summary.all_rejected == true
- checker_coverage_matrix covers K-001..K-033
- corpus_summary.counted_positive_formal_lean_tasks >= 1200
- corpus_summary.negative_target_outside_malformed_tasks >= 300
- corpus_summary.sealed_adversarial_holdout_count >= 700
- corpus_summary.external_goal_preserved_count >= min(300, corpus_summary.discovered_machine_checkable_external_goal_preserved_count)
- corpus_summary.user_reviewed_goal_without_review_manifest_count == 0
- corpus_summary.projection_non_counted_positive_count == 0
- corpus_statement_diversity_summary.unique_normalized_theorem_skeletons >= 150
- corpus_statement_diversity_summary.max_exact_skeleton_duplicate <= 8
- corpus_statement_diversity_summary.used_relation_families >= 8
- corpus_statement_diversity_summary.construction_case_certificate_required_tasks >= 350
- corpus_statement_diversity_summary.non_target_intermediate_required_tasks >= 600
- actual_pipeline_run_summary has every counted task x every required baseline
- solver_causality_summary.live_destructive_rerun_fraction == 1.0
- solver_causality_summary.precomputed_report_fraction == 0
- metrics_summary.B2_final_theorem_rate >= 0.70
- metrics_summary.B2_solver_causal_rate >= 0.70
- metrics_summary.B2_destructive_causality_pass_rate == 1.0
- metrics_summary.direct_wrapped_facade_fraction <= 0.10
- metrics_summary.non_target_intermediate_fraction >= 0.50
- metrics_summary.construction_case_certificate_success_fraction >= 0.40
- used_rule_coverage_summary.used_concrete_non_identity_rules >= 25
- used_rule_coverage_summary.used_rule_families >= 10
- engine_contribution_summary.every_release_engine_role_contributed == true
- baseline_comparability_summary.B2_minus_B1_overall_advantage >= 0.15
- baseline_comparability_summary.B2_minus_B5_construction_subset_advantage >= 0.10 when construction subset exists
- baseline_comparability_summary.B2_minus_B6_algebraic_metric_subset_advantage >= 0.10 when algebraic/metric subset exists
- baseline_comparability_summary.B2_minus_B7_order_case_subset_advantage >= 0.05 when order/case subset exists
- baseline_comparability_summary.conditional_b8_resolution_valid == true
- freshness_summary.current_git_head_bound == true
- debt_ledger_summary.open_entries == []
- closure_claim_ceiling.allowed_final_claim == "V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY"
- closure_claim_ceiling.forbidden_claims_present == []
```

After `CLOSURE.md` is written, `check_closure_claim_ceiling_v0_5.py` must be rerun without `--allow-missing-closure`. A closure that omits required non-claims or exceeds the release report evidence is K-028.
