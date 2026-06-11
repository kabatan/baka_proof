---
title: T20 Verification Evidence
task: T20 — TraceCompiler
date: 2026-06-11
status: PASS_PENDING_RC4
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T20 Verification Evidence

## Implemented Scope

- `TraceCompiler` compiles only supported `GeoTraceV1` rule subset.
- `TraceCompilationResult` dataclass and JSON Schema.
- Unsupported rules return blockers.
- Malformed/empty traces and missing side-condition refs are rejected fail-safe.
- Supported trace fixture compiles to a Lean patch candidate with `proof_use_status = lean_patch_candidate`.
- Lean compile fixture checks generated patch syntax with `lean`; it does not claim final theorem support.

## Verification

```powershell
python -m unittest tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry
cmd /c make smoke-geometry-trace > docs\ai\changes\geometry-lean-v0_3\evidence\trace_compiler_smoke.json
cmd /c make test-mutation TEST_FILTER=trace_compiler
cmd /c make test-unit
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
T20 focused tests: Ran 6 tests OK
Trace compiler smoke: PASS
Mutation target: Ran 12 tests OK
Full unit suite: Ran 61 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This completes T20 TraceCompiler scaffold for supported fixture traces. It does not claim arbitrary provider trace translation, construction compilation, final theorem support, RC-4 PASS, or v0.3 completion.
