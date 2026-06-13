# T08 Evidence — Plugin Registry and Manifest Loader

Task: `T08 — Plugin registry and manifest loader`

Supports:
- `INV-001`
- `INV-003`
- `R-SOLVER-001`

## Changes

- Added Plan-required public plugin API package:
  - `src/math_auto_research/plugin_api/manifest.py`
  - `src/math_auto_research/plugin_api/capability.py`
  - `src/math_auto_research/plugin_api/schemas.py`
- Added Plan-required Base registry package:
  - `src/math_auto_research/base/registry/loader.py`
  - `src/math_auto_research/base/registry/registry.py`
- Kept `src/math_auto_research/base/plugins/**` as compatibility re-exports only.
- `PluginLoader` loads `plugins/geometry_synthetic/plugin.yaml`, registers the `geometry.solve` capability, and registers schema files from the manifest `schema_root`.
- Loader records manifest component paths as data only; the registry test asserts it does not import `plugins.geometry_synthetic.facade`.

## Commands

```powershell
make test-unit TEST_FILTER=plugin_registry
```

Result:

```text
Ran 2 tests
OK
```

```powershell
python scripts\check_domain_contamination.py
```

Result:

```text
domain contamination check passed
```

## Claim

T08 acceptance is satisfied for manifest loading, capability/schema registration, and Base/plugin import boundary at the registry layer. This does not verify resource governance, dependency bootstrap, model-provider slots, real provider integration, or release readiness.
