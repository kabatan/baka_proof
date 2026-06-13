# T41 TongGeometry Claim-Profile Smoke Evidence

Task: T41 — TongGeometry claim-profile smoke hardening.

## Changed Files

```text
scripts/run_tonggeometry_probe.py
scripts/smoke_real_tonggeometry.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_smoke.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_backed_status.json
```

## Result

TongGeometry has two explicit claim levels.

```text
code_backed_diagnostic:
  status: available
  evidence: tonggeometry_smoke.json
  proof_use_status: not_allowed
  heavy_search_resource_governed: true
  orphan_check_passed: true

model_backed_heavy_search:
  status: blocked
  model_artifact_status: admitted_unavailable_external_artifact
  model_inference_status: unavailable
  claim_impact: blocks_model_backed_tonggeometry_claim
  missing artifacts: tokenizer, lm_s, lm_l, cls
```

The heavy-search provider path remains diagnostic-only and does not produce a
proof-use artifact.

## Verification

```text
make smoke-real-tonggeometry
status: passed

make test-unit TEST_FILTER=tonggeometry_adapter
status: passed, 6 tests

make test-regression TEST_FILTER=heavy_search_budget_gate
status: passed, 1 test plus domain/no-loose checks

make test-regression TEST_FILTER=heavy_search_no_orphans
status: passed, 1 test plus domain/no-loose checks

python scripts/check_dependency_claim_profile.py
status: passed

python scripts/check_dependency_report_model_status.py
status: passed

git diff --check
status: passed, CRLF warnings only
```

## Claim Ceiling

T41 is complete. `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY` remains
blocked. This task does not claim `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`
because corpus, matrix, standard-loop, release-acceptance, and closure tasks
remain.
