# WP-09 Evidence: Compiler Input Isolation and Taint Gates

Status: local WP-09 gates passed. This is not final v0.5 release evidence.

## Scope

WP-09 implements the release compiler entry point and checks for DR-011-003:

- compiler CLI accepts ClaimSpec ref, SelectedSolverDerivationV2 ref, RuleRegistry ref, and side-condition checker refs;
- proof-decision behavior is driven by SelectedSolverDerivationV2 plus RuleRegistry contracts;
- forbidden corpus/task/family/template/shape metadata is rejected by static scan or shown not to affect the compiler output by taint mutation;
- the compiler rejects naked target derivations and rule-list-only synthesis patterns;
- the compiler result cites solver facts, constructions, certificates, generated obligations, RuleRegistry contracts, and derivation steps.

## Implemented Files

- `plugins/geometry_full2d/compiler_v0_5.py`
- `scripts/geometry_full2d_v0_5_compiler_fixtures.py`
- `scripts/check_compiler_input_isolation_v0_5.py`
- `scripts/check_compiler_taint_v0_5.py`

## Evidence Commands

```powershell
python -m py_compile plugins\geometry_full2d\compiler_v0_5.py scripts\geometry_full2d_v0_5_compiler_fixtures.py scripts\check_compiler_input_isolation_v0_5.py scripts\check_compiler_taint_v0_5.py
```

Result: passed.

```powershell
python scripts/check_compiler_input_isolation_v0_5.py --run-dir runs\geometry_full2d_v0_5 --self-test
```

Result: passed.

Observed checks:

- positive compiler fixture passed;
- static bad fixture containing `target_expr.startswith(...)` failed with `target_expr_startswith`;
- naked target derivation failed with `naked_target_assertion` and `target_step_missing_inputs:0`.

```powershell
python scripts/check_compiler_taint_v0_5.py --run-dir runs\geometry_full2d_v0_5
```

Result: passed.

Observed checks:

- forbidden ClaimSpec metadata mutation did not change the proof-decision view;
- selected derivation mutation changed the proof-decision view.

```powershell
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_schema_validators_v0_5.py --self-test
```

Result: all passed.

Observed red-case coverage:

- `ProofFromShapeCompiler` rejected with K-007 present;
- `RuleListArtifactSynthesis` rejected with K-008 present;
- all 19 v0.5 red cases rejected.

## Release Harness Probe

The fail-closed release command was also probed after WP-09:

```powershell
python scripts/check_release_acceptance_v0_5.py --config configs\benchmark_runs\geometry_full2d_v0_5.yaml --output docs\ai\changes\geometry-full2d-v0_5\evidence\release_acceptance_report.json --fresh-run
```

Result: failed closed, as expected before later WPs. The generated incomplete `release_acceptance_report.json` and its fresh release run directory were deleted and are not release evidence.

Known remaining failures are for later work packages, including used-rule coverage and solver causality checkers that are not implemented at WP-09.

## Claim Ceiling After WP-09

Allowed: WP-09 compiler input isolation and taint gates have local evidence.

Not allowed:

- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`
- `SOURCE_FAITHFUL`
- `ACCEPTANCE_COMPLETE`
- `PRODUCTION_SAFE`
- R-ID `VERIFIED`
