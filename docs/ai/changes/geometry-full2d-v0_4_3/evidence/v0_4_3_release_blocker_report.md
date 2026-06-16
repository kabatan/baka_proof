---
title: "Release Blocker Report — GeometryFull2D v0.4.3 Strict Spec Verification"
report_id: "MARP-GEOLEAN-V043-RELEASE-BLOCKER-2026-06-16"
status: "RELEASE_BLOCKED"
base_spec: "MARP-GEOLEAN-BASE-008"
plan: "MARP-GEOLEAN-PLAN-008"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-008"
created: "2026-06-16"
authority: "Evidence report; does not change Base Spec or Plan requirements."
---

# Release Blocker Report — GeometryFull2D v0.4.3

## Summary

The implementation cannot be claimed as `V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY`.

The earlier `release_acceptance_report.json` PASS was invalidated by stricter checks for:

- `R-CORPUS-005`: near-duplicate positives must be <= 10%.
- `R-CORPUS-006`: exact template duplicate max per theorem family must be <= 5.
- `K-017` / Base Spec section 12.3: more than 20% of counted positive final-theorem successes may not be single direct facade lemma applications with no solver-generated intermediate evidence.
- `K-024`: release acceptance must enforce the above blockers.

This is not a Lean bootstrap blocker and not a browser/environment blocker. It is a release-content blocker: the current corpus and successful B2 proof patches do not meet the active Base Spec's anti-template and substantive-success requirements.

## Blocking Evidence

Strict corpus checker:

```text
path: runs/geometry_full2d_v0_4_3/check_reports/corpus_manifest_strict_after_specfail.json
status: failed
errors:
- exact_template_duplicate_max_gt_5:
  Full2DCore500 collinear_refl_left = 500
  IncidenceParallelPerp350 between_collinear = 350
  AngleCyclic450 directed_angle_eq_symm = 450
  Construction450 buckets = 112..113
  MetricRatioArea350 equal_length_symm = 350
  Transformation250 rotation_preserves_collinear = 250
  OrderCase250 between_collinear = 250
- near_duplicate_positive_fraction_gt_0_1: 3350/3350
```

Strict metrics checker:

```text
path: runs/geometry_full2d_v0_4_3/check_reports/metrics_strict_after_specfail.json
status: failed
errors:
- direct_lemma_success_fraction_gt_0_20: 1.0
```

Observed proof-patch profile for B2 positive final-theorem successes:

```text
3350 / 3350 successful B2 positive final theorem patches are single `exact ...` proofs.
```

Representative examples:

```lean
exact collinear_refl_left A B
exact between_collinear A B C h
exact directed_angle_eq_symm D E F A B C h
```

## Why This Blocks Completion

The current frozen manifest has 3350 positive tasks, but all positives are structurally grouped into repeated template families. Appending counters to `template_id` does not satisfy `R-CORPUS-006`; the normalized template identity still repeats far above the ceiling.

The current B2 solver-backed path produces valid Lean patches, but the counted successes are still direct facade lemma applications. Under `BASE_SPEC.md` section 12.3, those successes exceed the 20% ceiling because they lack solver-generated intermediate facts, construction evidence, side-condition reports, case/order evidence, algebraic certificates, metric/angle certificates, or inequality certificates in the final successful proof path.

## Required To Unblock

1. Rebuild the v0.4.3 release corpus so that counted positives satisfy:
   - positives >= 3000;
   - negatives / target-outside / malformed >= 500;
   - external_formal or user_reviewed_human_curated positives >= 900;
   - synthetic positives <= 50%;
   - near-duplicate positives <= 10%;
   - exact template duplicate max per theorem family <= 5.

2. Replace the current facade-lemma dominated B2 proof path with substantive compiler/proof generation so that at most 20% of counted positive final-theorem successes are single direct facade lemma applications.

3. Regenerate the frozen corpus hash, Lean extraction cache, full B1/B2/B5/B6/B7/B8 matrix, metrics, and release evidence.

4. Rerun the release command only after the strict corpus and metrics gates pass:

```bash
python scripts/check_release_acceptance_v0_4_3.py --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml --output docs/ai/changes/geometry-full2d-v0_4_3/evidence/release_acceptance_report.json
```

5. Run Guardian closure review only after release acceptance passes under the strict gates.

## Current Claim Ceiling

Allowed claim:

```text
The v0.4.3 implementation contains substantial real-pipeline hardening, Lean elaborator extraction, matrix-run infrastructure, and strict blocker checkers, but release closure is blocked by corpus duplicate and direct-lemma success ceilings.
```

Forbidden claims:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```
