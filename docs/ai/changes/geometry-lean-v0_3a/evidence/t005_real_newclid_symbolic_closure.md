---
title: T-005 Real Newclid-Compatible Symbolic Closure Verification
date: 2026-06-12
task: T-005 — Newclid-compatible symbolic closure integration
status: passed
authority: Task evidence only; does not mark R-IDs VERIFIED or establish full v0.3 completion.
---

# T-005 Real Newclid-Compatible Symbolic Closure Verification

Supports:

- `R-REAL-NEWCLID-001`
- `R-PROVIDER-REAL-002`
- `R-RESOURCE-REAL-001`

## Implemented Scope

- Added a real Newclid-compatible symbolic closure path behind `use_real_newclid` / `USE_REAL_NEWCLID`.
- Kept default fixture behavior intact for fixture preservation.
- Translates the current smoke `GeometryClaimSpec` collinearity target into a minimal Newclid JGEX problem.
- Launches real Newclid through Base `run_process_group` while inside `ResourceGovernor.admit`.
- Normalizes successful real output to a `GeoTraceV1` reference and failed/unsupported translation to Diagnostic.
- Keeps `ProviderResult.proof_use_status = not_allowed`; raw Newclid output is not proof evidence.
- Records real engine version evidence in `ProviderRunManifest.engine_runs`.

## Environment Resolution

Initial real Newclid execution failed because `yuclid.exe` exited with `-1073741515` / `3221225781`.

Observed dependency issue:

- `yuclid.exe` imported Boost DLL names such as `boost_log-vc143-mt-x64-1_88.dll`.
- The conda environment had no matching Boost runtime DLLs before repair.

Applied repair:

```text
conda install -y -c conda-forge libboost=1.88.0
```

Result: passed.

```text
python scripts\repair_yuclid_windows_runtime.py
```

Result: passed. The required Boost DLL aliases were present under the Python environment `Scripts` directory.

Health check:

```text
yuclid --help
```

Result: passed.

Manual real Newclid smoke:

```text
newclid --output-dir runs\newclid_probe_coll --saturate --seed 0 --log-level ERROR jgex --problem "a b = segment a b; c = on_line c a b ? coll a b c"
```

Result: passed. `run_infos.json` reported `success = true`.

## Verification Commands

```text
python -m py_compile plugins\geometry_synthetic\provider.py scripts\geometry_dependency_common.py scripts\smoke_geometry_provider.py scripts\repair_yuclid_windows_runtime.py
```

Result: passed.

```text
python -m unittest tests.unit.test_composite_provider
```

Result: passed.

```text
Ran 11 tests in 11.678s
OK
```

```text
python scripts\probe_geometry_dependencies.py --engine newclid_compatible --json
```

Result: passed. `newclid`, `yuclid`, and Python import checks were available.

```text
$env:ENGINE_ROLE='symbolic_closure'; $env:USE_REAL_NEWCLID='1'; cmd /c make smoke-geometry-provider
```

Result: passed. The emitted manifest recorded:

- `fixture_flag = false`;
- `real_integration_flag = true`;
- `engine_family = newclid_compatible`;
- `engine_version = newclid==3.0.1;py-yuclid==3.0.0;yuclid==dc40a72767c15a90`;
- `logs_ref = external_newclid_stdout`;
- `proof_use_status = not_allowed`.

```text
cmd /c make smoke-geometry-provider
```

Result: passed for default fixture-preservation path.

```text
python -m unittest tests.unit.test_schema_validation
```

Result: passed.

```text
Ran 5 tests in 0.025s
OK
```

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 77 tests in 26.557s
OK
```

```text
cmd /c make test-unit
```

Result: passed.

```text
Ran 94 tests in 25.369s
OK
```

## Run Artifacts

- `runs/v03a_t005_newclid_latest/dependency_probe.json`
- `runs/v03a_t005_newclid_latest/real_newclid_provider_smoke.json`

## Claim Ceiling

T-005 establishes a real Newclid-compatible symbolic closure smoke path for the admitted smoke `GeometryClaimSpec` shape, with manifest/resource accounting and proof-use blocking.

T-005 does not establish real GenesisGeo or TongGeometry integration, broad Newclid theorem coverage, arbitrary LeanGeo theorem support, final Lean theorem verification, real Level 2 advantage, or v0.3A completion.
