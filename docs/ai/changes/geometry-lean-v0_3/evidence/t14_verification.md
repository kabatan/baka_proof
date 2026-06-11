---
title: T14 Verification Evidence
task: T14 — GeometrySolverPolicy and resource-aware ExecutionPlan
date: 2026-06-11
status: PASS_PENDING_RC3
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T14 Verification Evidence

## Implemented Scope

- `GeometrySolverPolicy` with deterministic default routing:
  `symbolic_closure -> construction_proposer -> symbolic_closure retry -> heavy_search`.
- `GeometryExecutionPlan` dataclass and concrete JSON Schema.
- Budget rules for `tiny`, `small`, `medium`, `heavy`, and `extreme`.
- Reason codes for routing, construction fallback, symbolic retry, heavy search admission, and heavy search rejection.
- Resource semaphore requests per engine role using `ResourceRequest`.
- Heavy search is only planned under `heavy | extreme` budgets with explicit escalation/heavy request; lower budgets record a rejection reason instead of bypassing `ResourceGovernor`.

## Verification

```powershell
python -m unittest tests.unit.test_geometry_solver_policy tests.unit.test_resource_governor tests.unit.test_schema_validation
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
T14 focused set: Ran 12 tests OK
Full unit suite: Ran 46 tests OK
Mutation target: Ran 12 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This completes the T14 policy/planning scaffold only. It does not claim provider adapter execution, solver/compiler integration, final theorem support, RC-3 PASS, or v0.3 completion.
