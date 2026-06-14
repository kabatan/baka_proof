---
title: WP-12 InequalityEngine Evidence
status: implementation_smoke_passed
date: 2026-06-15
claim_ceiling: implementation_in_progress_no_v0_4_2_completion_claim
---

# WP-12 InequalityEngine Evidence

Implemented:

- `plugins/geometry_full2d/engines/inequality.py`
- `InequalityCertificateFull2D` normalized output for exact domain side-condition certificates.
- Nondegeneracy-to-positive-squared-distance normalization.
- Exact certificate checker for the local domain certificate path.
- Measured failure for missing domain constraints.
- Smoke harness and progress acceptance coverage for `inequality`.

Verification commands:

```text
python scripts/smoke_full2d_engine.py --engine inequality
python -m pytest tests/unit/test_geometry_full2d_inequality.py -q
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Expected status after verification:

```text
hard_blockers=[]
completed_work_packages includes WP-12:inequality-smoke-passed
next_unblocked_work_packages starts at WP-13
```

Remaining release blocker:

```text
Release acceptance is still blocked until the governed corpus and final release acceptance artifacts are complete.
```
