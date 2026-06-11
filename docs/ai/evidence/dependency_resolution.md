---
title: Dependency Resolution Evidence
date: 2026-06-12
status: V03A_T002_BOOTSTRAP_ATTEMPT_RECORDED
authority: Dependency evidence only; does not support real provider run or completion claims.
---

# Dependency Resolution Evidence

This file records the v0.3A T-002 dependency bootstrap attempt.

## Source References

- Newclid source: `https://github.com/Newclid/Newclid`
- GenesisGeo source: `https://github.com/ZJUVAI/GenesisGeo`
- TongGeometry source: `https://github.com/bigai-ai/tong-geometry`
- LeanGeo source remains pinned by `lakefile.lean`.

## Commands Run

```text
python scripts\bootstrap_geometry_engines.py --dry-run --run-id v03a_t002_dry_run_latest
```

Result: passed. Planned Newclid pip installation and GenesisGeo/TongGeometry vendor clone actions were recorded without executing them.

```text
python scripts\bootstrap_geometry_engines.py --apply --run-id v03a_t002_apply_latest
```

Result: passed.

Recorded action results:

- `newclid[yuclid]` installed by pip.
- `vendor/GenesisGeo` cloned from `https://github.com/ZJUVAI/GenesisGeo.git`.
- `vendor/tong-geometry` cloned from `https://github.com/bigai-ai/tong-geometry.git`.

```text
python scripts\probe_geometry_dependencies.py --json --run-id v03a_t002_probe_latest --output runs\v03a_t002_probe_latest\dependency_probe.json
```

Result: passed.

```text
python scripts\probe_local_resources.py --json
```

Result: passed.

## Pinned State

- `pyproject.toml` declares optional `geometry-engines` pins for `newclid[yuclid]==3.0.1` and `py-yuclid==3.0.0`.
- `configs/dependencies/geometry_engines.json` records `libboost==1.88.0` from conda-forge as the Windows runtime required by `yuclid.exe`.
- `scripts/repair_yuclid_windows_runtime.py` records the local Windows DLL alias repair for `yuclid.exe` Boost imports.
- `.gitmodules` pins external source locations for GenesisGeo and TongGeometry as submodules.
- `configs/dependencies/geometry_engines.json` records the dependency set and observed commits.
- `configs/local_resource_profile.yaml` records the local resource profile required by BASE-003A.

## T-005 Newclid Runtime Update

The first real Newclid smoke attempt reached `newclid==3.0.1` but failed when `yuclid.exe` exited with Windows code `3221225781` / `-1073741515`.

Resolution performed on 2026-06-12:

```text
conda install -y -c conda-forge libboost=1.88.0
python scripts\repair_yuclid_windows_runtime.py
```

After this repair:

- `yuclid --help` passed;
- `newclid --output-dir runs\newclid_probe_coll --saturate --seed 0 --log-level ERROR jgex --problem "a b = segment a b; c = on_line c a b ? coll a b c"` passed;
- `python scripts\probe_geometry_dependencies.py --engine newclid_compatible --json` reported `newclid` and `yuclid` command checks as available.

## Run Artifacts

- `runs/v03a_t002_dry_run_latest/dependency_probe.json`
- `runs/v03a_t002_dry_run_latest/dependency_resolution_report.json`
- `runs/v03a_t002_apply_latest/dependency_probe.json`
- `runs/v03a_t002_apply_latest/dependency_resolution_report.json`
- `runs/v03a_t002_probe_latest/dependency_probe.json`
- `runs/v03a_t005_newclid_latest/dependency_probe.json`
- `runs/v03a_t005_newclid_latest/real_newclid_provider_smoke.json`

## Claim Ceiling

This evidence records dependency bootstrap, source availability, and the T-005 Newclid runtime repair.

The T-005 Newclid smoke evidence is limited to the explicitly recorded smoke `GeometryClaimSpec` shape and does not establish:

- broad real provider behavior;
- real GenesisGeo / TongGeometry integration;
- arbitrary LeanGeo theorem support;
- real Level 2 advantage;
- v0.3 completion.
