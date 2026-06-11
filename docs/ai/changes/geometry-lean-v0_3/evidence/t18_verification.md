---
title: T18 Verification Evidence
task: T18 — TongGeometry-compatible heavy-search adapter
date: 2026-06-11
status: PASS_PENDING_RC3
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T18 Verification Evidence

## Implemented Scope

- TongGeometry-compatible heavy-search fixture adapter.
- Heavy search appears in plans only under `heavy | extreme` budget with explicit escalation/heavy request.
- Resource admission uses the `heavy_search` semaphore through `ResourceGovernor`.
- Heavy search resource usage records include timeout budget and completion status.
- Raw heavy-search trace is recorded only as raw output hash and diagnostic; it is not proof evidence.
- ProviderResult remains `proof_use_status = not_allowed`.

## Verification

```powershell
cmd /c "set ENGINE_ROLE=heavy_search&& set BUDGET=heavy&& make smoke-geometry-provider" > docs\ai\changes\geometry-lean-v0_3\evidence\tong_adapter_smoke.json
cmd /c make test-regression TEST_FILTER=heavy_search_budget_gate
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
Tong adapter smoke: PASS
Regression target: passed
Full unit suite: Ran 52 tests OK
Mutation target: Ran 12 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This is a TongGeometry-compatible fixture adapter, not real TongGeometry installation or integration. It does not claim real heavy-search discovery, solver/compiler integration, final theorem support, RC-3 PASS, or v0.3 completion.
