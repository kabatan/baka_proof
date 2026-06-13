# T13 Evidence — ModelProviderSet

Task: `T13 — ModelProviderSet`

Supports:
- `R-MODEL-001`
- `R-MODEL-002`
- `R-MODEL-003`
- `MECH-MODEL-001`

## Changes

- Added `scripts/smoke_model_provider_set.py`.
- Added `scripts/check_model_hardcode.py`.
- Adjusted model-output DAG regression to use an admitted non-final rule path while still rejecting final theorem closure without FinalVerifyGate.

## Commands

```powershell
make smoke-model-provider-set
```

Result:

```text
model provider set smoke passed
```

```powershell
make test-unit TEST_FILTER=model_provider
```

Result:

```text
Ran 4 tests
OK
```

```powershell
python scripts\check_model_hardcode.py
```

Result:

```text
model hardcode check passed
```

## Claim

T13 acceptance is satisfied for ModelProviderSet slot loading, slot invocation records, non-proof model output artifacts, and initial model-hardcode regression coverage. This does not verify controller/worker plugin contracts, real model providers, Lean final verification, or release readiness.
