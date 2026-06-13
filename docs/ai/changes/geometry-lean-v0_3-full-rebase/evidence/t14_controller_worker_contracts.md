# T14 Evidence — ResearchControllerPlugin and ProofWorkerPlugin Contracts

Task: `T14 — ResearchControllerPlugin and ProofWorkerPlugin contracts`

Supports:
- `R-MODEL-004`
- `R-MODEL-005`

## Changes

- Added Plan-required `src/math_auto_research/model_api/` modules:
  - `research_controller.py`
  - `proof_worker.py`
  - `action_plan.py`
  - `work_order.py`
  - `state_pack.py`
- Kept `src/math_auto_research/base/model_consumers.py` as compatibility re-exports.
- Added `ActionPlan` validation that prevents controller output from claiming final theorem closure.
- Added `WorkerResult` validation that prevents worker/model output from claiming `final_theorem` or `lean_theorem`.
- Added focused unit/regression tests for controller, worker, and model-output non-proof boundaries.

## Commands

```powershell
make test-unit TEST_FILTER=controller_plugin
```

Result:

```text
Ran 1 test
OK
```

```powershell
make test-unit TEST_FILTER=proof_worker_plugin
```

Result:

```text
Ran 1 test
OK
```

```powershell
make test-regression TEST_FILTER=model_output_not_proof
```

Result:

```text
Ran 1 test
OK
domain contamination check passed
no loose options check passed
```

```powershell
make test-unit TEST_FILTER=model_provider
```

Result:

```text
Ran 4 tests
OK
```

## Claim

T14 acceptance is satisfied for model-consuming controller/worker contract placement and non-proof model output boundaries. This does not verify ProofRegionGuard, LeanPort, FinalVerifyGate, real model providers, or release readiness.
