---
title: WP14 Zero B2 Success Blocker Report
status: ACTIVE_EVIDENCE
purpose: Document the execution blocker preventing v0.6 WP14 metrics and final release thresholds from passing.
authority: Evidence only. Does not modify BASE_SPEC, PLAN, or ACCEPTANCE.
created: 2026-06-20
---

# WP14 Zero B2 Success Blocker Report

## Summary

WP13 all-baseline matrix execution completed structurally, but B2 produced zero counted final theorem successes.

This is a release blocker for WP14 and later release readiness because Base Spec section 5 requires:

- B2 overall final theorem rate >= 0.70
- B2 solver-causal success fraction = 1.00
- B2 live destructive mutation pass fraction = 1.00
- B2 non-target intermediate success fraction >= 0.70
- B2 construction/case/certificate success fraction >= 0.50
- B2 used counted rule families >= 15
- every enabled release-critical engine role to contribute to at least one counted B2 final theorem success
- B2 baseline advantages over B1/B5/B6/B7

## Fresh Evidence

Run directory:

```text
runs/wp13_v0_6_full_matrix_3
```

WP13 matrix runner:

```bash
python scripts/run_full2d_matrix_v0_6.py --config configs/benchmark_runs/geometry_full2d_v0_6.yaml --run-dir runs/wp13_v0_6_full_matrix_3 --execute-all --all-baselines --no-skip
```

Result:

```text
status: passed
ActualTaskPipelineRunV4 records: 7200
B2 records: 1200
B2 final_theorem: 0
B2 measured_failure: 1200
DisabledStageReportV1 records: 6000
StageFailureReportV1 records: 1200
```

WP13 matrix checker:

```bash
python scripts/check_all_baseline_matrix_v0_6.py --run-dir runs/wp13_v0_6_full_matrix_3 --red-cases
```

Result:

```text
status: passed
record_count: 7200
by_baseline: B1=1200, B2=1200, B5=1200, B6=1200, B7=1200, B8=1200
red_cases: passed
```

WP14 metrics checker:

```bash
python scripts/check_full2d_metrics_v0_6.py --run-dir runs/wp13_v0_6_full_matrix_3 --thresholds-from docs/ai/changes/geometry-full2d-v0_6/BASE_SPEC.md
```

Result:

```text
status: failed
B2_final_theorem_rate: 0.0
B2_solver_causal_success_fraction: 0.0
B2_live_destructive_mutation_pass_fraction: 0.0
B2_non_target_intermediate_success_fraction: 0.0
B2_construction_case_certificate_success_fraction: 0.0
B2_minus_B1_overall: 0.0
B2_minus_B5_construction_subset: 0.0
B2_minus_B6_algebraic_metric_certificate_subset: 0.0
B2_minus_B7_order_case_subset: 0.0
```

WP14 used-rule coverage checker:

```bash
python scripts/check_used_rule_coverage_v0_6.py --run-dir runs/wp13_v0_6_full_matrix_3 --red-cases
```

Result:

```text
status: failed
no_b2_final_theorem_successes_for_rule_coverage
used_counted_rule_families_below_threshold:0<15
red_cases: passed
```

WP14 engine contribution checker:

```bash
python scripts/check_engine_contribution_v0_6.py --run-dir runs/wp13_v0_6_full_matrix_3 --red-cases
```

Result:

```text
status: failed
no_b2_final_theorem_successes_for_engine_contribution
enabled_role_without_counted_b2_success:synthetic_trace
enabled_role_without_counted_b2_success:construction
enabled_role_without_counted_b2_success:algebraic_metric_certificate
enabled_role_without_counted_b2_success:order_case
enabled_role_without_counted_b2_success:inequality
enabled_role_without_counted_b2_success:lean_search_certificate
enabled_role_without_counted_b2_success:external_solver_trace
red_cases: passed
```

## Root-Cause Hypothesis

The blocker is not missing matrix materialization. The all-baseline records exist and pass the matrix checker.

The blocker is semantic: generated B2 Lean proof candidates do not prove the actual theorem targets. The compiler currently emits a proof body whose final expression has type `True`, while the theorem target is a geometry proposition such as `between P23 P08 P25`, `isosceles P07 P06 P05`, or `concyclic P10 P23 P04 P17`.

Representative FinalVerify failure:

```text
type mismatch
  h_solver_derivation_trace_complete
has type
  True : Prop
but is expected to have type
  between P09 P04 P31 : Prop
```

Representative source theorem:

```lean
theorem v06_sealed_holdout_0338
    (P00 P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 P11 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P22 P23 P24 P25 P26 P27 P28 P29 P30 P31 : Point)
    (h00 : area_le P05 P20 P03 P18 P01 P16)
    (h01 : length_le P23 P25 P18 P11)
    (h02 : midpoint P03 P06 P09)
    : between P23 P08 P25 := by
```

The listed hypotheses do not provide a direct or rule-derived proof of the target under the current solver artifacts and compiler. Treating this as success would require a shortcut such as redefining geometry predicates as `True`, introducing an axiom, using a target-shaped provider artifact, or accepting a direct facade. Those are contrary to the v0.6 no-shortcut intent.

## Required Fix Direction

To resume Plan completion without rule hacking, the pipeline needs real B2 final theorem successes. At minimum this requires one of the following non-shortcut corrections:

1. Generate a sealed holdout corpus whose theorem targets are actually derivable from admitted hypotheses through non-target solver artifacts and counted rule lemmas.
2. Extend provider and selected derivation artifacts with structured, independently checked rule-application evidence that bridges hypotheses to the target without carrying proof text or target-shaped artifacts.
3. Extend compiler generation so it turns that structured derivation into Lean proof terms using the rule registry lemmas, while preserving the DR-012-004 compiler API lock and FinalVerifyGate.
4. Re-run WP12 independence checks after any corpus/generator or selected implementation change, then rerun WP13 and WP14.

Until this is done, WP14 metrics, used-rule coverage, engine contribution, live causality over B2 successes, and final release acceptance cannot pass honestly.

