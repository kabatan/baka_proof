---
title: T16 Verification Evidence
task: T16 — Newclid-compatible symbolic closure adapter
date: 2026-06-11
status: PASS_PENDING_RC3
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T16 Verification Evidence

## Implemented Scope

- Newclid-compatible symbolic closure fixture adapter.
- Input conversion from `GeometryClaimSpec` to a Newclid-compatible fixture shape:
  objects, known predicates, target, target raw expression, nondegeneracy assumptions, and orientation assumptions.
- Raw log capture through provider manifest raw output hashes.
- Output normalization remains `diagnostic_only` until `GeoTraceV1` and compiler contracts are implemented.
- Resource admission uses the `symbolic_closure` semaphore through `ResourceGovernor`.

## Verification

```powershell
cmd /c "set ENGINE_ROLE=symbolic_closure&& make smoke-geometry-provider" > docs\ai\changes\geometry-lean-v0_3\evidence\newclid_adapter_smoke.json
cmd /c make test-integration TEST_FILTER=newclid_adapter
cmd /c make test-regression TEST_FILTER=provider_not_base_branching
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
Newclid adapter smoke: PASS
Integration target: Ran 5 tests OK
Regression target: passed
Full unit suite: Ran 51 tests OK
Mutation target: Ran 12 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This is a Newclid-compatible fixture adapter, not real Newclid installation or integration. It does not claim normalized `GeoTraceV1`, solver/compiler integration, final theorem support, RC-3 PASS, or v0.3 completion.
