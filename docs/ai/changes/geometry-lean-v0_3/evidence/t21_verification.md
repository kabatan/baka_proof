---
title: T21 Verification Evidence
task: T21 — AuxiliaryConstructionCandidateV1 and ConstructionCompiler
date: 2026-06-11
status: PASS_PENDING_RC4
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T21 Verification Evidence

## Implemented Scope

- `AuxiliaryConstructionCandidateV1`, `ConstructionCheckResult`, and `ConstructionCompilationResult` dataclasses and JSON Schemas.
- `ConstructionCompiler` accepts only the v0.3 construction kind set.
- Unsupported construction kinds are blocked.
- Missing side conditions are blocked.
- Accepted construction candidates generate side-condition obligations and Lean introduction patch candidates.
- Lean compile fixture checks generated patch syntax with `lean`; it does not claim final theorem support.

## Verification

```powershell
python -m unittest tests.unit.test_construction_compiler tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry
cmd /c make smoke-geometry-construction > docs\ai\changes\geometry-lean-v0_3\evidence\construction_compiler_smoke.json
cmd /c make test-mutation TEST_FILTER=construction_compiler
cmd /c make test-unit
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
T21 focused tests: Ran 9 tests OK
Construction compiler smoke: PASS
Mutation target: Ran 12 tests OK
Full unit suite: Ran 64 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This completes T21 construction candidate and construction compiler scaffold. It does not claim final theorem support, protected theorem patch insertion, RC-4 PASS, or v0.3 completion.
