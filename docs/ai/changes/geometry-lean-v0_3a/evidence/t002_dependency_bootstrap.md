---
title: T-002 Dependency Bootstrap Verification
date: 2026-06-12
task: T-002 — Implement dependency bootstrap and probe
status: passed_for_bootstrap_attempt
authority: Task evidence only; does not expand claim ceiling or mark R-IDs VERIFIED.
---

# T-002 Dependency Bootstrap Verification

Supports:

- `R-ENV-REAL-001`
- `R-ENV-REAL-002`

## Implemented Scope

- Added `scripts/bootstrap_geometry_engines.py`.
- Added `scripts/probe_geometry_dependencies.py`.
- Added shared helper `scripts/geometry_dependency_common.py`.
- Generated `configs/local_resource_profile.yaml`.
- Added optional Python package pins for `newclid[yuclid]==3.0.1` and `py-yuclid==3.0.0`.
- Registered GenesisGeo and TongGeometry source clones as git submodules.
- Added `configs/dependencies/geometry_engines.json`.
- Added top-level dependency evidence at `docs/ai/evidence/dependency_resolution.md`.

## Verification Commands

```text
python -m py_compile scripts\geometry_dependency_common.py scripts\probe_geometry_dependencies.py scripts\bootstrap_geometry_engines.py
```

Result: passed.

```text
python scripts\bootstrap_geometry_engines.py --dry-run --run-id v03a_t002_dry_run_latest
```

Result: passed.

```text
python scripts\bootstrap_geometry_engines.py --apply --run-id v03a_t002_apply_latest
```

Result: passed.

Observed bootstrap results:

- Newclid-compatible: `newclid[yuclid]` pip installation passed; observed `newclid==3.0.1`.
- GenesisGeo-compatible: source clone passed; observed commit `e8c4337e782548a4d54e6839558a32965a5a764e`.
- TongGeometry-compatible: source clone passed; observed commit `d00925f07dc3174f91326386cb8e785e539a91a1`.

```text
python scripts\probe_geometry_dependencies.py --json --run-id v03a_t002_probe_latest --output runs\v03a_t002_probe_latest\dependency_probe.json
```

Result: passed.

```text
python scripts\probe_local_resources.py --json
```

Result: passed.

```text
cmd /c make test-unit
```

Result: passed.

```text
Ran 88 tests in 8.743s
OK
```

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 71 tests in 12.950s
OK
```

## Claim Ceiling

T-002 records dependency bootstrap, source pinning, and local resource profile generation.

T-002 does not establish real provider runs, real integration acceptance, arbitrary LeanGeo theorem support, real Level 2 advantage, or v0.3 completion.
