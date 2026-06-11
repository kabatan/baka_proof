---
title: RC-003A-2 Guardian Boundary Review
date: 2026-06-12
gate: RC-003A-2 provider/resource boundary
status: PASS
reviewer: guardian_boundary_reviewer
authority: Review record only; does not mark R-IDs VERIFIED or expand claim ceiling beyond the stated limited claim.
---

# RC-003A-2 Guardian Boundary Review

## Result

PASS.

RC-003A-2 provider/resource boundary is admitted within the fixture-level claim ceiling.

## Reviewed Scope

- `plugins/geometry_synthetic/provider.py`
- `schemas/geometry/provider_run_manifest.schema.json`
- `schemas/geometry/v03_contract_index.schema.json`
- `tests/unit/test_composite_provider.py`
- `docs/ai/changes/geometry-lean-v0_3a/evidence/t004_composite_provider_v1.md`
- `docs/ai/changes/geometry-lean-v0_3a/evidence/INDEX.md`
- `docs/ai/ACTIVE_CONTEXT.md`

## Blocker Remediation Confirmed

- `ProviderResult.status` now uses admitted `failed` plus `fixture_only_real_required` diagnostic marker.
- `ProviderRunManifest.required_fields` in `v03_contract_index` now includes `engine_runs`.
- Per-engine `engine_family` now records actual family labels: `newclid_compatible`, `genesisgeo_compatible`, `tonggeometry_compatible`, with schema enum and unit assertions.

## Limited Admitted Claim

T-004 establishes the `CompositeSyntheticGeometryProviderV1` provider boundary and ProviderRunManifest accounting for fixture-vs-real separation, including explicit fixture/real flags and actual internal engine-family labels. Fixture-only provider configuration is blocked from satisfying a real-integration requirement.

## Explicit Non-Claims

- No R-IDs are VERIFIED.
- This does not admit real Newclid/GenesisGeo/TongGeometry integration.
- This does not admit real provider acceptance.
- This does not admit v0.3A completion.
- This does not admit real Level 2 advantage.
