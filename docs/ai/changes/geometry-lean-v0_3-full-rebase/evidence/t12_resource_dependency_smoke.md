# T12 Evidence — Resource and Dependency Smoke

Task: `T12 — Resource/dependency smoke evidence`

Supports:
- `R-ENV-*`
- `R-RSRC-*`

## Commands

```powershell
make smoke-env-bootstrap
```

Result:

```text
dependency report emitted successfully
```

Observed dependency state:

- Lean/lake available at Lean 4.15.0.
- Newclid-compatible role installed.
- GenesisGeo-compatible role vendored at pinned commit `e8c4337e782548a4d54e6839558a32965a5a764e`.
- TongGeometry-compatible role vendored at pinned commit `d00925f07dc3174f91326386cb8e785e539a91a1`.
- `unresolved: []` in the dependency probe.

```powershell
make smoke-resource-governor
```

Result:

```text
local resource profile emitted successfully
```

```powershell
python scripts\probe_dependencies.py --json > docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_probe.json
python scripts\probe_local_resources.py --json > docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\local_resource_profile.json
python -m math_auto_research.cli.validate_artifact docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_probe.json
```

Result:

```json
{"schema": "resources.dependency_resolution_report.v1", "status": "ok"}
```

## Claim

T12 acceptance is satisfied for fresh dependency and local resource smoke evidence. This does not verify real provider smoke behavior, model-provider slots, Lean final verification, or release readiness.
