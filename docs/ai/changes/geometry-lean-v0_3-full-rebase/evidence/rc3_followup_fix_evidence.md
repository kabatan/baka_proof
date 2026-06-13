# RC-3 follow-up fix evidence

Status: ready for Guardian boundary re-review.

Prior review findings addressed:

- `ModelInvocationRecord` schemas now include runtime provenance/logging fields:
  `provider_set_hash`, `request_hash`, `response_hash`,
  `redacted_transcript_artifact_ref`, `usage_metadata`, and
  `proof_use_status: not_allowed`.
- `DummyResearchController.plan_next_actions` now exposes the Base-required
  typed interface and returns `ActionPlan`.
- `DummyProofWorker.execute_work_order` now exposes the Base-required typed
  interface and returns `WorkerResult`.
- `FinalVerifyGate` now rejects a `final_theorem` result when proof-use
  provenance is missing or incomplete.

Commands run:

```text
make smoke-model-provider-set
make test-unit TEST_FILTER=model_provider
make test-unit TEST_FILTER=controller_plugin
make test-unit TEST_FILTER=proof_worker_plugin
make test-regression TEST_FILTER=model_output_not_proof
make test-unit TEST_FILTER=final_verify
python scripts\check_model_hardcode.py
python -m math_auto_research.cli.validate_schema configs\model_provider_sets\default.example.yaml
python -m compileall -q src tests scripts
make lean-build
make lean-no-sorry
make test-regression TEST_FILTER=theorem_statement_hash
```

Observed results:

```text
model provider set smoke passed
model_provider unit tests: 4 tests OK
controller_plugin unit tests: 2 tests OK
proof_worker_plugin unit tests: 2 tests OK
model_output_not_proof regression: 1 test OK; domain/no-loose checks passed
final_verify unit tests: 8 tests OK
model hardcode check passed
model_provider_sets/default.example.yaml schema validation status: ok
compileall passed
lake build: Build completed successfully
lean no-sorry check passed
theorem_statement_hash regression: 1 test OK; domain/no-loose checks passed
```

Notes:

- `make lean-build` emitted warnings about local changes inside `.lake`
  dependency repositories. The build itself completed successfully.
- Untracked `lib/` remains present and was not modified by this fix.
