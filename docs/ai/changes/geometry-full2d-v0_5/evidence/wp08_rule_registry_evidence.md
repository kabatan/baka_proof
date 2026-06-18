# WP-08 RuleRegistry Evidence

Status: implemented locally for `MARP-GEOLEAN-PLAN-011` WP-08.

Scope:

- Updated `plugins/geometry_full2d/rule_registry.py` so `RuleRegistryFull2D` emits v0.5 rule contracts.
- Added `scripts/check_full2d_rule_registry_v0_5.py`.
- Strengthened `scripts/geometry_full2d_v0_5_schemas.py` for counted RuleRegistry contracts.

Implemented contract:

- 150 counted non-identity rules across 30 counted rule families.
- 2 non-counted helper rules for direct identity/direct facade cases.
- Every counted rule has input patterns, output pattern, required side conditions, generated obligations, Lean template id, independent checker, positive fixtures, negative fixtures, and mutation fixtures.
- Counted rules reject output-equals-input identity patterns and target-goal output patterns.

WP-08 acceptance command:

```powershell
python scripts/check_full2d_rule_registry_v0_5.py --self-test
```

Result: passed.

Negative cases covered by the self-test:

- counted identity/direct-facade rule registry is rejected;
- counted naked-target rule registry is rejected;
- counted rule missing mutation fixtures is rejected.

Additional verification:

```powershell
python -m py_compile plugins\geometry_full2d\rule_registry.py scripts\check_full2d_rule_registry_v0_5.py scripts\geometry_full2d_v0_5_schemas.py
python scripts/check_schema_validators_v0_5.py --self-test
python -m unittest tests.unit.test_geometry_full2d_rule_registry
python scripts/check_full2d_rule_registry.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
```

Result: all passed.

Fail-closed release check:

```powershell
python scripts/check_release_acceptance_v0_5.py --config configs\benchmark_runs\geometry_full2d_v0_5.yaml --output docs\ai\changes\geometry-full2d-v0_5\evidence\release_acceptance_report.json --fresh-run
```

Result: failed as expected on later incomplete release gates, including used-rule coverage and solver causality. The generated incomplete release report and temporary release run directory were deleted and are not used as success evidence.

Claim ceiling after WP-08:

- WP-01 through WP-08 implementation gates have local evidence.
- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`, `ACCEPTANCE_COMPLETE`, and `SOURCE_FAITHFUL` are still not claimed.
