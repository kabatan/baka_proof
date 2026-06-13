# T04 Evidence — Stable Schema Framework

Task: `T04 — Stable schema framework`

Supports:
- `R-SCHEMA-001`
- `R-SCHEMA-002`
- `R-SCHEMA-003`
- `R-SCHEMA-004`
- `R-SCHEMA-005`
- `R-SCHEMA-006`

## Changes

- Added `src/math_auto_research/base/schemas.py` with a Pydantic v2 schema framework.
- Added `SchemaRecord` with:
  - required `schema_version` serialization;
  - forbidden unknown fields for registered proof-critical records;
  - deterministic canonical JSON hashing;
  - schema hashing;
  - JSON Schema export for registered records.
- Registered initial Base/resource records required by T04:
  - `ArtifactRef`
  - `RunConfig`
  - `RunRecord`
  - `SelectedImplementations`
  - `TrustReport`
  - `DiagnosticBundle`
  - `DependencyResolutionReport`
  - `LocalResourceProfile`
  - `ResourceBudgetProfile`
  - `ResourceUsageReport`
  - `FinalVerifyReport`
  - `ReleaseAcceptanceReport`
- Updated `src/math_auto_research/schema_validation.py` so known schema paths validate through the Pydantic models while preserving the existing CLI interface.
- Added `schemas/model/.gitkeep` so the required `schemas/model/` directory exists separately from the older `schemas/model_api/` directory.
- Updated `Makefile` so `make test-unit TEST_FILTER=schema` actually runs the schema-focused unit tests instead of the full unit suite.

## Environment Note

`make` was not initially present on PATH. Chocolatey install was attempted and failed because the non-elevated shell could not access Chocolatey package locks/directories. A user-local shim was then added at:

```text
C:\Users\bakat\.local\bin\make.cmd
```

The shim delegates to the existing:

```text
C:\msys64\ucrt64\bin\mingw32-make.exe
```

Result:

```text
GNU Make 4.4.1
```

## Commands

```powershell
make test-unit TEST_FILTER=schema
```

Result:

```text
python -m unittest discover -s tests/unit -p "*schema*.py"
.......
Ran 7 tests in 0.079s
OK
```

```powershell
python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml
```

Result:

```json
{"schema": "base.selected_implementations.v1", "status": "ok"}
```

```powershell
python -m math_auto_research.cli.validate_artifact configs/selected_implementations/geometry_default.yaml
```

Result:

```json
{"schema": "base.selected_implementations.v1", "status": "ok"}
```

## Claim

T04 schema-framework acceptance is satisfied for the registered Base/resource schema layer and existing schema validation CLI surface. This does not verify T05 selected implementation hashing, later model-provider contracts, geometry extraction, provider integration, or release readiness.
