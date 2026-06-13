# T11 Evidence — LeanGeo Dependency and TargetLibraryManifest

Task: `T11 — LeanGeo dependency and TargetLibraryManifest`

Supports:
- `R-ENV-*`
- `R-GEO-001`

## Changes

- Confirmed Lean/lake build works with the pinned LeanGeo-compatible dependency in `lakefile.lean`.
- Extended `configs/target_libraries/leangeo_subset_v1.yaml` into the Base Spec `TargetLibraryManifest` shape:
  - `target_library_id`
  - `source_dependency`
  - `version_or_commit`
  - namespace / grammar / predicate / construction / relation mapping refs
- Extended `schemas/geometry/target_library_manifest.schema.json`.
- Extended target library status reporting to include manifest refs and dependency metadata.
- Added `scripts/check_no_fixture_release.py` as an initial release-config fixture misuse guard.
- Wrote target-library status evidence to `target_library_status.json`.

## Commands

```powershell
python -m math_auto_research.cli.validate_artifact configs\target_libraries\leangeo_subset_v1.yaml
```

Result:

```json
{"schema": "geometry.target_library_manifest.v1", "status": "ok"}
```

```powershell
make lean-build
```

Result:

```text
Build completed successfully.
```

Lake emitted warnings that `.lake/packages/UnicodeBasic` and `.lake/packages/batteries` have local changes. The build still completed successfully.

```powershell
python -m math_auto_research.cli.report_target_library_status > docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\target_library_status.json
python -m math_auto_research.cli.validate_artifact docs\ai\changes\geometry-lean-v0_3-full-rebase\evidence\target_library_status.json
```

Result:

```json
{"schema": "geometry.target_library_status_report.v1", "status": "ok"}
```

```powershell
python scripts\check_no_fixture_release.py
```

Result:

```text
no fixture release check passed
```

## Claim

T11 acceptance is satisfied for the pinned LeanGeo-compatible lake dependency, TargetLibraryManifest shape, namespace/theorem status report generation, and initial no-fixture release guard. This does not verify the full LeanGeoSubsetV1 grammar/mappings, real corpus, extraction, provider integration, or release readiness.
