# Dependency Resolution Report — T10

Task: `T10 — Dependency bootstrap`

Supports:
- `R-ENV-001`
- `R-ENV-002`
- `R-ENV-003`
- `MECH-BOOT-001`

## Actions

- Confirmed editable package install with geometry engine extras:

```powershell
python -m pip install -e ".[geometry-engines]"
```

Result:

```text
Successfully installed math-auto-research-0.0.0
newclid==3.0.1 already satisfied
py-yuclid==3.0.0 already satisfied
```

Pip continued to emit pre-existing local environment warnings about an invalid `~ip` distribution in `C:\Users\bakat\miniforge3\Lib\site-packages`; this did not block install.

- Confirmed vendored GenesisGeo repository:

```text
vendor/GenesisGeo
commit e8c4337e782548a4d54e6839558a32965a5a764e
remote https://github.com/ZJUVAI/GenesisGeo.git
```

- Provisioned the public GenesisGeo model checkpoint without opening a browser:

```text
source: https://huggingface.co/ZJUVAI/GenesisGeo
local path: models/GenesisGeo
model.safetensors sha256: 77406d21e84699b3d0d123653e40b7f48f3642beae10c0b608f58249223b8099
git status: excluded by /models/
```

- Created a dedicated GenesisGeo-compatible Python runtime:

```text
conda env: geolean-py310
python: 3.10.20
```

- Confirmed vendored TongGeometry repository:

```text
vendor/tong-geometry
commit d00925f07dc3174f91326386cb8e785e539a91a1
remote https://github.com/bigai-ai/tong-geometry.git
```

- Updated `scripts/probe_dependencies.py` so dependency reports recognize pinned vendored repositories from `configs/dependencies/geometry_engines.json`.
- Updated the Pydantic `DependencyResolutionReport` model to match the checked-in JSON Schema and emitted report shape.

## Commands

```powershell
make smoke-env-bootstrap
```

Result:

```text
dependency report emitted successfully
```

```powershell
python scripts\probe_dependencies.py --json > docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_probe.json
python -m math_auto_research.cli.validate_artifact docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_probe.json
```

Result:

```json
{"schema": "resources.dependency_resolution_report.v1", "status": "ok"}
```

```powershell
python scripts\probe_dependencies.py --output docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_resolution.json
python -m math_auto_research.cli.validate_artifact docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\dependency_resolution.json
```

Result:

```json
{"schema": "resources.dependency_resolution_report.v1", "status": "ok"}
```

## Current Dependency Status

The generated report currently records:

- Lean/lake available at Lean 4.15.0.
- Newclid-compatible role installed through `newclid.EXE`.
- GenesisGeo-compatible role vendored at the pinned commit with checkpoint_hash
  `sha256:77406d21e84699b3d0d123653e40b7f48f3642beae10c0b608f58249223b8099`.
- TongGeometry-compatible role vendored at the pinned commit.
- No unresolved entries in the T10 dependency-resolution report.

## Claim

T10 bootstrap acceptance is satisfied for installed/vendored dependency discovery and schema-backed dependency report generation. This does not verify LeanGeo target integration, real Newclid/GenesisGeo/TongGeometry smoke behavior, provider adapters, or release readiness.
