---
title: T-007 TongGeometry-Compatible Heavy-Search Diagnostic Verification
date: 2026-06-12
task: T-007 — TongGeometry-compatible heavy-search integration
status: passed_with_diagnostic_blocker
authority: Task evidence only; does not mark R-IDs VERIFIED or establish TongGeometry model search.
---

# T-007 TongGeometry-Compatible Heavy-Search Diagnostic Verification

Supports:

- `R-REAL-TONGGEOMETRY-001`
- `R-RESOURCE-REAL-001`

## Implemented Scope

- Added a real TongGeometry-compatible heavy-search diagnostic path behind `use_real_tonggeometry` / `USE_REAL_TONGGEOMETRY`.
- Preserved the policy gate: heavy search is not scheduled for `medium` budget even when requested; it runs only under admitted heavy policy.
- The provider launches `scripts/run_tonggeometry_probe.py` as an external process through Base `run_process_group` while inside `ResourceGovernor.admit`.
- The diagnostic records vendored TongGeometry source path, commit, Python import status, model path status, and blocker reasons.
- Raw TongGeometry diagnostic output remains `proof_use_status = not_allowed`.
- `ProviderRunManifest.engine_runs` records `engine_family = tonggeometry_compatible`, `engine_version = tong-geometry@d00925f07dc3174f91326386cb8e785e539a91a1`, `fixture_flag = false`, and `real_integration_flag = true` for the heavy-search diagnostic run.

## Diagnostic Blocker

The vendored TongGeometry source is present and importable from `vendor/tong-geometry`, but model-backed heavy search is not admitted as complete in this environment.

Observed diagnostic blocker:

- no `TONGGEOMETRY_TOKENIZER`, `TONGGEOMETRY_LM_S`, `TONGGEOMETRY_LM_L`, or `TONGGEOMETRY_CLS` model paths are configured.

Therefore T-007 records a genuine external-process Diagnostic, not a model-backed heavy-search result.

## Verification Commands

```text
python -m py_compile plugins\geometry_synthetic\provider.py scripts\run_tonggeometry_probe.py scripts\smoke_geometry_provider.py
```

Result: passed.

```text
python scripts\run_tonggeometry_probe.py --request-id geometry_request:tong-probe --claim-spec-json <smoke-json>
```

Result: passed. Output status was `diagnostic_only` with blocker reason `missing_tonggeometry_model_paths:tokenizer,lm_s,lm_l,cls`.

```text
python scripts\probe_geometry_dependencies.py --engine tonggeometry_compatible --json
```

Result: passed. Vendored TongGeometry commit was detected.

```text
python -m unittest tests.unit.test_composite_provider
```

Result: passed.

```text
Ran 13 tests in 12.287s
OK
```

```text
$env:ENGINE_ROLE='heavy_search'; $env:BUDGET='heavy'; $env:USE_REAL_TONGGEOMETRY='1'; cmd /c make smoke-geometry-provider
```

Result: passed. The emitted provider run recorded `proof_use_status = not_allowed`, `logs_ref = external_tonggeometry_stdout`, `orphan_check_passed = true`, and TongGeometry commit `d00925f07dc3174f91326386cb8e785e539a91a1`.

```text
cmd /c make smoke-geometry-provider
```

Result: passed for default fixture-preservation path.

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 79 tests in 27.432s
OK
```

```text
cmd /c make test-unit
```

Result: passed.

```text
Ran 96 tests in 25.739s
OK
```

## Run Artifacts

- `runs/v03a_t007_tonggeometry_latest/dependency_probe.json`
- `runs/v03a_t007_tonggeometry_latest/heavy_search_smoke.json`

## Claim Ceiling

T-007 establishes a ResourceGovernor-managed, policy-gated real external diagnostic path against the vendored TongGeometry source and records why model-backed heavy search is blocked in this environment.

T-007 does not establish TongGeometry model inference/search, arbitrary LeanGeo theorem support, final Lean theorem verification, real Level 2 advantage, or v0.3A completion.
