---
title: WP-09 MetricAngleEngine Evidence
status: implementation_smoke_passed
date: 2026-06-15
claim_ceiling: implementation_in_progress_no_v0_4_2_completion_claim
---

# WP-09 MetricAngleEngine Evidence

Implemented:

- `plugins/geometry_full2d/engines/metric_angle.py`
- `MetricAngleTraceFull2D` normalized output for the repeated-endpoint collinearity smoke target.
- Explicit `directed_angle_mod_pi` normalization policy.
- Local checker for zero-angle modulo pi trace shape and required nondegeneracy condition.
- Measured failure for missing side conditions or unsupported targets.
- Smoke harness and progress acceptance coverage for `metric_angle`.

Verification commands:

```text
python scripts/smoke_full2d_engine.py --engine metric_angle
python -m pytest tests/unit/test_geometry_full2d_metric_angle.py -q
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Expected status after verification:

```text
hard_blockers=[]
completed_work_packages includes WP-09:metric-angle-smoke-passed
next_unblocked_work_packages starts at WP-10
```

Remaining release blocker:

```text
Release acceptance is still blocked until the governed corpus and final release acceptance artifacts are complete.
```
