---
title: WP-07 ConstructionSearchEngine evidence
status: PASSED
created: 2026-06-15
purpose: Record evidence for the GeometryFull2D ConstructionSearchEngine work package.
authority: Evidence only; does not claim final release coverage.
---

# WP-07 ConstructionSearchEngine Evidence

## Scope

WP-07 replaced the construction-search diagnostic skeleton with a deterministic auxiliary construction backend:

```text
geometry_full2d.construction_search:deterministic_auxiliary_search:v0_4_2
```

For the structured smoke ClaimSpec, it introduces a line through two nondegenerate points and emits an `AuxiliaryConstructionFull2D` reference with side-condition obligations and a RuleRegistryFull2D source rule. Missing side conditions produce `measured_failure`.

## Verification

```text
python scripts/smoke_full2d_engine.py --engine construction_search
```

Result:

```text
passed
```

```text
python -m pytest tests/unit/test_geometry_full2d_construction_search.py tests/unit/test_geometry_full2d_provider.py -q
```

Result:

```text
6 passed
```

```text
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Result:

```text
completed_work_packages includes WP-07:construction-search-smoke-passed
next_unblocked_work_packages includes WP-08 through WP-14 and WP-20
```

## Claim Ceiling

This closes the WP-07 smoke path only. It does not yet satisfy algebraic, metric/angle, transformation, order/case, inequality, Lean proof search, corpus, or final release acceptance.
