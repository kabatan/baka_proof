---
title: WP-08 AlgebraicGeometryEngine Evidence
status: implementation_smoke_passed
date: 2026-06-15
claim_ceiling: implementation_in_progress_no_v0_4_2_completion_claim
---

# WP-08 AlgebraicGeometryEngine Evidence

Implemented:

- `plugins/geometry_full2d/engines/algebraic_geometry.py`
- `AlgebraicCertificateFull2D` normalized output for repeated-point collinearity smoke targets.
- Exact local checker for the duplicate-row determinant certificate.
- Measured failure for missing or unsupported ClaimSpec targets.
- Smoke harness and progress acceptance coverage for `algebraic_geometry`.

Verification commands:

```text
python scripts/smoke_full2d_engine.py --engine algebraic_geometry
python -m pytest tests/unit/test_geometry_full2d_algebraic_geometry.py -q
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Expected status after verification:

```text
hard_blockers=[]
completed_work_packages includes WP-08:algebraic-geometry-smoke-passed
next_unblocked_work_packages starts at WP-09
```

Remaining release blocker:

```text
Release acceptance is still blocked until the governed corpus and final release acceptance artifacts are complete.
```
