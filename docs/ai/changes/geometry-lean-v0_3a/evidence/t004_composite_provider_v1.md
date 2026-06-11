---
title: T-004 CompositeSyntheticGeometryProviderV1 Verification
date: 2026-06-12
task: T-004 — Implement CompositeSyntheticGeometryProviderV1
status: passed
authority: Task evidence only; does not expand claim ceiling or mark R-IDs VERIFIED.
---

# T-004 CompositeSyntheticGeometryProviderV1 Verification

Supports:

- `R-PROVIDER-REAL-001`
- `R-PROVIDER-REAL-002`

## Implemented Scope

- Added explicit `CompositeSyntheticGeometryProviderV1` provider boundary while preserving the existing compatibility alias.
- Extended `ProviderRunManifest` with:
  - `provider_class`;
  - `provider_version`;
  - top-level `fixture_flag`;
  - top-level `real_integration_flag`;
  - per-engine `engine_version`;
  - per-engine `fixture_flag`;
  - per-engine `real_integration_flag`;
  - per-engine `raw_log_artifact_hash`;
  - per-engine `normalized_output_hash`.
- Updated provider manifest schema and v0.3 contract index.
- Added tests showing fixture-only configuration cannot satisfy a real-integration requirement.
- Remediated RC-003A-2 pre-admission blocker findings:
  - fixture-only real-integration requests now use admitted `ProviderResult.status = failed` with a diagnostic marker instead of introducing an unadmitted status;
  - `ProviderRunManifest` is indexed with mandatory `engine_runs` in the v0.3 contract index;
  - per-engine `engine_family` records actual engine-family labels (`newclid_compatible`, `genesisgeo_compatible`, `tonggeometry_compatible`) instead of engine roles.
- Existing provider remains fixture-backed; this is boundary/manifest work, not real provider acceptance.

## Verification Commands

```text
python -m py_compile plugins\geometry_synthetic\provider.py
```

Result: passed.

```text
python -m unittest tests.unit.test_composite_provider
```

Result: passed.

```text
Ran 10 tests in 2.060s
OK
```

Post-review remediation rerun:

```text
Ran 10 tests in 1.847s
OK
```

```text
python -m unittest tests.unit.test_schema_validation
```

Result: passed.

```text
Ran 5 tests in 0.106s
OK
```

Post-review remediation rerun:

```text
Ran 5 tests in 0.027s
OK
```

```text
cmd /c make smoke-geometry-provider
```

Result: passed. The emitted manifest includes `provider_class = CompositeSyntheticGeometryProviderV1`, `fixture_flag = true`, and `real_integration_flag = false`.

Post-review remediation rerun: passed. The emitted manifest records actual `engine_family` values such as `newclid_compatible` and `genesisgeo_compatible`, and retains `fixture_flag = true`, `real_integration_flag = false`.

```text
python scripts\check_domain_contamination.py
```

Result: passed.

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 76 tests in 17.402s
OK
```

Post-review remediation rerun:

```text
domain contamination check passed
no loose options check passed
Ran 76 tests in 14.376s
OK
```

```text
cmd /c make test-unit
```

Result: passed after remediation.

```text
Ran 93 tests in 11.670s
OK
```

## Claim Ceiling

T-004 establishes manifest and provider-boundary accounting for fixture-vs-real separation.

T-004 does not establish real provider behavior, real Newclid/GenesisGeo/TongGeometry integration acceptance, arbitrary LeanGeo theorem support, real Level 2 advantage, or v0.3 completion.
