---
title: T02 Verification
created: 2026-06-11
status: PASS_WITH_WINDOWS_COMMAND_NOTE
purpose: Verify stable schemas, SelectedImplementations config, and schema validation CLI.
authority: Evidence only.
---

# T02 Verification

Commands:

- `python -m unittest discover -s tests/unit -p "test_*.py"` -> PASS, 3 tests.
- `python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml` -> PASS.
- `cmd /c make test-unit` -> PASS, 3 tests via repo-local `make.bat`.
- PowerShell direct `make test-unit` did not resolve because this Windows shell does not search the current directory for batch files by bare command name.

Deliverables:

- `schemas/base/**` present.
- `schemas/model_api/**` present.
- `schemas/resources/**` present.
- `schemas/geometry/**` present.
- `schemas/v03_contract_inventory.json` maps v0.3 public contracts to schema refs.
- `configs/selected_implementations/geometry_default.yaml` validates and uses scalar selected implementation fields.
- `python -m math_auto_research.cli.validate_schema` entrypoint works.
