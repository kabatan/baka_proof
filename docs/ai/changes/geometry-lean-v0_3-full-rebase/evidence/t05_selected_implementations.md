# T05 Evidence — SelectedImplementations and Configs

Task: `T05 — SelectedImplementations and configs`

Supports:
- `INV-002`
- `R-SCHEMA-002`
- `R-SCHEMA-004`
- `R-SCHEMA-005`

## Changes

- Kept the canonical default config at `configs/selected_implementations/geometry_default.yaml`.
- Validated the default config through the Pydantic-backed `SelectedImplementations` schema.
- Strengthened `scripts/check_no_loose_options.py` so it checks both:
  - the JSON schema field definitions are scalar, not arrays;
  - every YAML config under `configs/selected_implementations/` validates as scalar `SelectedImplementations`.
- Recorded the canonical selected implementation hash in `selected_implementations_hash.txt`.

## SelectedImplementations Hash

```text
sha256:c04cf7261c67fd036c3e56a3b72177a0355b614730426254d0bbb72a8a5d76bf
```

The hash was computed from the Pydantic canonical JSON serialization of `configs/selected_implementations/geometry_default.yaml`.

## Commands

```powershell
python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml
```

Result:

```json
{"schema": "base.selected_implementations.v1", "status": "ok"}
```

```powershell
python scripts\check_no_loose_options.py
```

Result:

```text
no loose options check passed
```

```powershell
python -c "from pathlib import Path; from math_auto_research.schema_validation import load_artifact; from math_auto_research.base.schemas import SelectedImplementations; r=SelectedImplementations.model_validate(load_artifact(Path('configs/selected_implementations/geometry_default.yaml'))); print(r.deterministic_hash())"
```

Result:

```text
sha256:c04cf7261c67fd036c3e56a3b72177a0355b614730426254d0bbb72a8a5d76bf
```

## Claim

T05 acceptance is satisfied for scalar selected implementation config validation and hash evidence. This does not verify later plugin registry loading, model-provider slot implementation, geometry provider integration, or release readiness.
