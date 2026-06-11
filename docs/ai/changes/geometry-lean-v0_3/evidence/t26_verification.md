---
title: T26 Verification
task: T26 — EvaluationFunnel and Level 2 matrix
date: 2026-06-11
status: passed
authority: Implementation evidence; does not mark R-IDs VERIFIED.
---

# T26 Verification

Supports R-IDs: `R-EVAL-001`, `R-RUN-002`, `R-RUN-003`, `R-CLAIM-001`, `R-V03-EVAL-001`.

## Implemented Scope

- Added `configs/benchmark_runs/geometry_level2_smoke.yaml`.
- Added `configs/benchmark_runs/geometry_level2_ablation.yaml`.
- Added B0-B5 baseline matrix records:
  - B0 proof-worker-only fixture;
  - B1 controller + worker without `geometry.solve`;
  - B2 full geometry-enabled fixture;
  - B3 strong-model without `geometry.solve`;
  - B4 lower-model + `geometry.solve`;
  - B5 geometry-enabled with auxiliary construction disabled.
- Added matrix runner `scripts/run_geometry_level2_matrix.py`.
- Added metrics collector in `plugins/geometry_synthetic/evaluation.py`.
- Extended reproducibility reporting to restore matrix run records when `level2_matrix_report.json` is present.
- Added `tests/unit/test_evaluation_matrix.py`.

## Verification Commands

```text
python -m unittest tests.unit.test_evaluation_matrix tests.unit.test_run_trace
```

Result: passed, 5 tests.

```text
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
```

Result: passed. Output included:

- fixed `benchmark_pool = ["sample_target_fixture"]`;
- B0 through B5 baseline entries;
- `geometry_enabled_minus_controller_no_geometry_final_count = 1`;
- `claim_ceiling = fixture_level_matrix_not_level2_advantage_claim`;
- reproducibility report `run_id = geometry_level2_smoke`.

```text
python scripts/generate_repro_report.py --run-dir runs/geometry_level2_smoke
```

Result: passed. Output included:

- `replay_status = restored`;
- `missing_components = []`;
- restored components include `evaluation_funnel` and `level2_run_matrix`.

```text
cmd /c make test-unit
```

Result: passed, 84 tests.

```text
cmd /c make test-regression
```

Result: passed; domain contamination and no-loose-options checks passed; 69 regression tests passed.

```text
python scripts/check_domain_contamination.py
```

Result: passed.

## Claim Ceiling

- T26 implements fixture-level Level 2 evaluation matrix plumbing.
- The reported comparison is a fixture count only.
- T26 does not claim real Level 2 advantage, benchmark validity beyond the fixed smoke pool, v0.3 completion, or any R-ID as VERIFIED.
