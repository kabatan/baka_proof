# RC-3 Fix Evidence

Scope: Fixes requested by the initial RC-3 Guardian boundary review.

## Fixes

- Resolved Plan checkpoint ambiguity by aligning the checkpoint table to `RC-3: after T15`, matching the T15 task body.
- Added T13 required paths:
  - `src/math_auto_research/base/model_provider/`
  - `schemas/model/model_provider_set.schema.json`
- Extended `ModelInvocationRecord` with:
  - `provider_set_hash`
  - `request_hash`
  - `response_hash`
  - `usage_metadata`
  - `redacted_transcript_artifact_ref`
- Added Base-required T14 method signatures:
  - `DummyResearchController.plan_next_actions(state, models, context)`
  - `DummyProofWorker.execute_work_order(work_order, models, lean_port, resource_governor)`
- Extended `FinalVerifyGate` checks for:
  - admitted imports;
  - local toy target substitution markers;
  - proof-use provenance fields when provenance is supplied.
- Recorded initial RC-3 failure in `rc3_guardian_boundary_review_fail.md`.

## Commands

```powershell
make smoke-model-provider-set
make test-unit TEST_FILTER=model_provider
make test-unit TEST_FILTER=controller_plugin
make test-unit TEST_FILTER=proof_worker_plugin
make test-regression TEST_FILTER=model_output_not_proof
make test-unit TEST_FILTER=final_verify
python scripts\check_model_hardcode.py
python -m math_auto_research.cli.validate_schema configs\model_provider_sets\default.example.yaml
make lean-build
make lean-no-sorry
```

Results:

```text
model provider set smoke passed
model_provider: Ran 4 tests, OK
controller_plugin: Ran 2 tests, OK
proof_worker_plugin: Ran 2 tests, OK
model_output_not_proof: Ran 1 test, OK
final_verify: Ran 7 tests, OK
model hardcode check passed
model provider set config validated
Lean build completed successfully
lean no-sorry check passed
```

Lake emitted warnings that `.lake/packages/UnicodeBasic` and `.lake/packages/batteries` have local changes. The build still completed successfully.

## Claim

The specific RC-3 reviewer findings have been addressed. RC-3 PASS is not claimed until follow-up Guardian review passes.
