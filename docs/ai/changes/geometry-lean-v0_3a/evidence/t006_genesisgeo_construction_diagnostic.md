---
title: T-006 GenesisGeo-Compatible Construction Diagnostic Verification
date: 2026-06-12
task: T-006 — GenesisGeo-compatible construction proposer integration
status: passed_with_diagnostic_blocker
authority: Task evidence only; does not mark R-IDs VERIFIED or establish GenesisGeo model inference.
---

# T-006 GenesisGeo-Compatible Construction Diagnostic Verification

Supports:

- `R-REAL-GENESISGEO-001`
- `R-PROVIDER-REAL-002`
- `R-RESOURCE-REAL-001`

## Implemented Scope

- Added a real GenesisGeo-compatible construction proposer diagnostic path behind `use_real_genesisgeo` / `USE_REAL_GENESISGEO`.
- The provider launches `scripts/run_genesisgeo_probe.py` as an external process through Base `run_process_group` while inside `ResourceGovernor.admit`.
- The diagnostic records vendored GenesisGeo source path, commit, Python requirement, current Python version, model checkpoint status, and blocker reasons.
- Raw GenesisGeo diagnostic output remains `proof_use_status = not_allowed`.
- `ProviderRunManifest.engine_runs` records `engine_family = genesisgeo_compatible`, `engine_version = GenesisGeo@e8c4337e782548a4d54e6839558a32965a5a764e`, `fixture_flag = false`, and `real_integration_flag = true` for the construction proposer diagnostic run.
- `smoke-geometry-construction` still verifies the existing `AuxiliaryConstructionCandidateV1 -> ConstructionCompiler -> Lean patch` path and now also includes the GenesisGeo diagnostic provider run.

## Diagnostic Blocker

The vendored GenesisGeo source is present, but model inference is not admitted as complete in this environment.

Observed diagnostic blockers:

- GenesisGeo `pyproject.toml` requires Python `==3.10.*`;
- current Python is `3.12.11`;
- no `GENESISGEO_MODEL_PATH` / `GENESISGEO_CHECKPOINT` is configured.

Therefore T-006 records a genuine external-process Diagnostic, not a non-fixture construction candidate from GenesisGeo model inference.

## Verification Commands

```text
python -m py_compile plugins\geometry_synthetic\provider.py scripts\run_genesisgeo_probe.py scripts\smoke_geometry_construction.py scripts\smoke_geometry_provider.py
```

Result: passed.

```text
python scripts\run_genesisgeo_probe.py --request-id geometry_request:probe --claim-spec-json <smoke-json>
```

Result: passed. Output status was `diagnostic_only` with blocker reasons `python_runtime_required:==3.10.*:actual:3.12.11` and `missing_genesisgeo_model_checkpoint`.

```text
python scripts\probe_geometry_dependencies.py --engine genesisgeo_compatible --json
```

Result: passed. Vendored GenesisGeo commit was detected.

```text
python -m unittest tests.unit.test_composite_provider
```

Result: passed.

```text
Ran 12 tests in 12.783s
OK
```

```text
cmd /c make smoke-geometry-construction
```

Result: passed. The emitted provider run recorded `proof_use_status = not_allowed`, `logs_ref = external_genesisgeo_stdout`, `orphan_check_passed = true`, and GenesisGeo commit `e8c4337e782548a4d54e6839558a32965a5a764e`.

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 78 tests in 27.485s
OK
```

```text
cmd /c make test-unit
```

Result: passed.

```text
Ran 95 tests in 26.245s
OK
```

## Run Artifacts

- `runs/v03a_t006_genesisgeo_latest/dependency_probe.json`
- `runs/v03a_t006_genesisgeo_latest/construction_smoke.json`

## Claim Ceiling

T-006 establishes a ResourceGovernor-managed real external diagnostic path against the vendored GenesisGeo source and records why model-backed construction proposal is blocked in this environment.

T-006 does not establish GenesisGeo model inference, non-fixture GenesisGeo construction candidate generation, real TongGeometry integration, arbitrary LeanGeo theorem support, final Lean theorem verification, real Level 2 advantage, or v0.3A completion.
