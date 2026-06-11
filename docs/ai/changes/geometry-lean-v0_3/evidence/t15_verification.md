---
title: T15 Verification Evidence
task: T15 — Composite GeometrySolverProvider shell
date: 2026-06-11
status: PASS_PENDING_RC3
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T15 Verification Evidence

## Implemented Scope

- `CompositeSyntheticGeometryProvider` shell.
- Provider-normalized `ProviderResult` with `proof_use_status = not_allowed`.
- `ProviderRunManifest` dataclass and concrete JSON Schema.
- Dummy engine role adapters for:
  - `symbolic_closure`;
  - `construction_proposer`;
  - `heavy_search`.
- ResourceGovernor admission for every planned engine step.
- ResourceUsageReport-shaped records for each admitted engine step.
- Manifest records adapter version, commit marker, config hash, checkpoint hash, seed, raw output hashes, normalized output refs, resource usage refs, unsupported rule count, and side-condition loss count.

## Verification

```powershell
python -m unittest tests.unit.test_composite_provider tests.unit.test_geometry_plugin_scaffold tests.unit.test_geometry_solver_policy
cmd /c make smoke-geometry-provider > docs\ai\changes\geometry-lean-v0_3\evidence\geometry_provider_smoke.json
cmd /c make test-regression TEST_FILTER=provider_not_base_branching
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
T15 focused tests: Ran 10 tests OK
smoke-geometry-provider: PASS
provider_not_base_branching regression: passed
Full unit suite: Ran 50 tests OK
Mutation target: Ran 12 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This completes the composite provider shell with dummy internal adapters. It does not claim real Newclid, GenesisGeo, or TongGeometry integration; solver/compiler integration; final theorem support; RC-3 PASS; or v0.3 completion.
