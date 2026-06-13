# T15 Evidence — LeanPort, ProofRegionGuard, FinalVerifyGate

Task: `T15 — LeanPort, ProofRegionGuard, FinalVerifyGate`

Supports:
- `R-LEAN-001`
- `R-LEAN-002`
- `R-LEAN-003`
- `R-LEAN-004`
- `INV-006`

## Changes

- Added Plan-required Lean integration package:
  - `src/math_auto_research/lean_integration/lean_port.py`
  - `src/math_auto_research/lean_integration/goal_anchor.py`
  - `src/math_auto_research/lean_integration/final_verify_gate.py`
  - `src/math_auto_research/lean_integration/proof_region_guard.py`
  - `src/math_auto_research/lean_integration/lean_error_summary.py`
- Kept old Base import paths as compatibility re-exports.
- Updated `LeanPort` to execute Lean through `ResourceGovernor` / `ProcessRunner`.
- Added `GoalAnchor` with goal/protected-statement/context hashes.
- Added focused theorem statement hash and no-sorry regression tests.

## Commands

```powershell
make lean-build
```

Result:

```text
Build completed successfully.
```

Lake emitted warnings that `.lake/packages/UnicodeBasic` and `.lake/packages/batteries` have local changes. The build still completed successfully.

```powershell
make lean-no-sorry
```

Result:

```text
lean no-sorry check passed
```

```powershell
make test-unit TEST_FILTER=final_verify
```

Result:

```text
Ran 4 tests
OK
```

```powershell
make test-regression TEST_FILTER=theorem_statement_hash
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

```powershell
make test-regression TEST_FILTER=no_sorry
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

## Claim

T15 acceptance is satisfied for LeanPort, GoalAnchor, ProofRegionGuard, and FinalVerifyGate contract behavior on the current minimal Lean target. This does not verify geometry extraction, LeanGeoSubsetV1 grammar/mappings, real provider integration, or release readiness.
