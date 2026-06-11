---
title: T19 Verification Evidence
task: T19 — GeoTraceV1 and RuleRegistryV1
date: 2026-06-11
status: PASS_PENDING_RC4
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T19 Verification Evidence

## Implemented Scope

- `GeoTraceV1` dataclass and JSON Schema.
- `RuleRegistryV1`, `GeometryRuleContract`, and `SideConditionReport` dataclasses and JSON Schemas.
- Initial LeanGeoSubsetV1 supported rule subset:
  - `collinearity_propagation`;
  - `parallel_perpendicular_transfer`;
  - `midpoint_basic_consequences`;
  - `concyclicity_basic_consequences`;
  - `equal_length_transfer`;
  - `angle_transfer`;
  - `construction_introduction`.
- Rule registry validator fails missing side conditions, missing fixtures, duplicate rule IDs, missing Lean template, and wrong target library.
- Side-condition calculus turns missing side conditions into generated obligations, not silent assumptions.

## Verification

```powershell
python -m unittest tests.unit.test_geotrace_rule_registry tests.unit.test_schema_validation
cmd /c make test-mutation TEST_FILTER=rule_registry
cmd /c make test-unit
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
T19 focused tests: Ran 8 tests OK
Mutation target: Ran 12 tests OK
Full unit suite: Ran 58 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This completes T19 registry/trace schemas and fixture validation only. It does not claim TraceCompiler, ConstructionCompiler, Lean patch generation, final theorem support, RC-4 PASS, or v0.3 completion.
