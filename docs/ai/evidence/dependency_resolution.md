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
- `.gitmodules` pins external source locations for GenesisGeo and TongGeometry as submodules.
- `configs/dependencies/geometry_engines.json` records the dependency set and observed commits.
- `configs/local_resource_profile.yaml` records the local resource profile required by BASE-003A.

## Run Artifacts

- `runs/v03a_t002_dry_run_latest/dependency_probe.json`
- `runs/v03a_t002_dry_run_latest/dependency_resolution_report.json`
- `runs/v03a_t002_apply_latest/dependency_probe.json`
- `runs/v03a_t002_apply_latest/dependency_resolution_report.json`
- `runs/v03a_t002_probe_latest/dependency_probe.json`

## Claim Ceiling

This evidence records dependency bootstrap and source availability only.

It does not establish:

- real provider behavior;
- real Newclid / GenesisGeo / TongGeometry integration;
- arbitrary LeanGeo theorem support;
- real Level 2 advantage;
- v0.3 completion.
