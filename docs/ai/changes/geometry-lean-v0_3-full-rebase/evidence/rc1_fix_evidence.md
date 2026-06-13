# RC-1 Fix Evidence

Scope: Fixes requested by the initial RC-1 Guardian boundary review.

## Fixes

- Added Base trust package:
  - `src/math_auto_research/base/trust/__init__.py`
  - `src/math_auto_research/base/trust/guard.py`
- Added `TrustGuard` classification for:
  - raw sources as `not_allowed`;
  - Lean patch candidates as non-final;
  - final theorem only through final verification references.
- Converted proof-state records to schema-backed Pydantic records with `schema_version`, while preserving existing positional constructor compatibility.
- Added proof-state records:
  - `GraphPatchCommitResult`
  - `DAGSnapshot`
  - `StateReaderSummary`
- Strengthened `DAGWriter` validation:
  - unknown rule IDs rejected;
  - evidence status checked by rule family;
  - invalid status transitions rejected;
  - Base-owned payload mutation flag rejected;
  - final proof-use still requires `final_verify_gate` and final-proof evidence.
- Moved target-library status implementation into the geometry plugin and left a generic top-level delegating shim.
- Moved artifact-to-schema filename routing into `schemas/artifact_schema_map.json`.
- Broadened `scripts/check_domain_contamination.py` to scan all of `src/math_auto_research`.

## Commands

```powershell
make test-unit TEST_FILTER=schema
```

Result:

```text
Ran 7 tests
OK
```

```powershell
make test-unit TEST_FILTER=proof_state
```

Result:

```text
Ran 10 tests
OK
```

```powershell
make test-unit TEST_FILTER=trust
```

Result:

```text
Ran 6 tests
OK
```

```powershell
python scripts\check_domain_contamination.py
```

Result:

```text
domain contamination check passed
```

```powershell
python scripts\check_package_layout.py
```

Result:

```text
package layout check passed: C:\Users\bakat\work\AI_math_research\src\math_auto_research\__init__.py
```

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
make test-regression TEST_FILTER=dag_raw_log_not_node
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

```powershell
make test-unit TEST_FILTER=artifact
make test-unit TEST_FILTER=run_logger
make test-unit TEST_FILTER=diagnostic
python -m unittest tests.unit.test_target_library_status
```

Result:

```text
artifact: Ran 4 tests, OK
run_logger: Ran 4 tests, OK
diagnostic: Ran 2 tests, OK
target_library_status: Ran 1 test, OK
```

## Claim

These fixes address the initial RC-1 reviewer findings. RC-1 PASS is not claimed until a follow-up Guardian boundary review passes.
