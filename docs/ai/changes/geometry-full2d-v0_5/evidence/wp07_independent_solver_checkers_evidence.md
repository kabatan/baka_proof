# WP-07 Independent Solver Checkers Evidence

Status: implemented locally for `MARP-GEOLEAN-PLAN-011` WP-07.

Scope:

- Added `scripts/geometry_full2d_v0_5_independent_checkers.py`.
- Added `scripts/check_independent_solver_checkers_v0_5.py`.
- Updated `plugins/geometry_full2d/provider_cli.py` to write content-addressed ClaimSpec and normalized semantic artifacts for checker replay.
- Updated `plugins/geometry_full2d/engines/synthetic_closure.py` so repeated-collinearity success uses a non-target support fact before the target step.
- Strengthened `scripts/geometry_full2d_v0_5_schemas.py` so `IndependentCheckerReportFull2D` rejects self-certified, engine-boolean-trusting, or target-conclusion-trusting reports.

WP-07 acceptance command:

```powershell
python scripts/check_independent_solver_checkers_v0_5.py --run-dir runs\geometry_full2d_v0_5 --self-test
```

Result: passed.

Negative cases covered by the self-test:

- mutated target facts are rejected;
- target steps with missing premises are rejected;
- naked target traces without non-target support are rejected;
- self-certified checker reports are rejected.

Additional verification:

```powershell
python -m py_compile scripts\geometry_full2d_v0_5_independent_checkers.py scripts\check_independent_solver_checkers_v0_5.py scripts\geometry_full2d_v0_5_schemas.py plugins\geometry_full2d\provider_cli.py plugins\geometry_full2d\engines\synthetic_closure.py
python scripts/check_schema_validators_v0_5.py --self-test
python scripts/check_provider_stage_boundary_v0_5.py --self-test
python scripts/check_engine_outputs_v0_5.py --self-test
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python -m unittest tests.unit.test_geometry_full2d_provider
```

Result: all passed.

Fail-closed checks:

```powershell
python scripts/check_independent_solver_checkers_v0_5.py --run-dir runs\geometry_full2d_v0_5
```

Result: failed as expected with `missing_provider_cli_summary` because no actual v0.5 provider-stage run exists in that run directory yet.

```powershell
python scripts/check_release_acceptance_v0_5.py --config configs\benchmark_runs\geometry_full2d_v0_5.yaml --output docs\ai\changes\geometry-full2d-v0_5\evidence\release_acceptance_report.json --fresh-run
```

Result: failed as expected because later WP release checkers and full release artifacts are still incomplete. The generated incomplete release report and temporary release run directory were deleted and are not used as success evidence.

Claim ceiling after WP-07:

- WP-01 through WP-07 implementation gates have local evidence.
- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`, `ACCEPTANCE_COMPLETE`, and `SOURCE_FAITHFUL` are still not claimed.
