# v0.3 Full Completion Blocker Report

Claim: BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY

Generated from current-state evidence after TongGeometry model-smoke hardening.

## Blocking Requirement

The admitted Base Spec and Plan require real provider smoke evidence and release
acceptance with no open release blockers before the project may claim:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

Relevant requirements:

```text
R-SOLVER-005
R-TEST-003
Base Spec Section 20 release blocker 11
Plan T25
Plan T36
Plan T37
```

## Current Machine Evidence

Latest release acceptance report:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Current status:

```text
status: blocked
open_blockers:
- release_blocker_11_real_provider_smoke_evidence
model_backed_errors:
- missing_model_checkpoint:tonggeometry_compatible
claim_ceiling: release_acceptance_blocked_no_v0_3_completion_claim
```

`docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance.json`
has been synchronized to the same report.

## What Is Implemented

TongGeometry integration is implemented up to the point that supplied model
artifacts can be verified:

```text
scripts/run_tonggeometry_probe.py
scripts/run_tonggeometry_model_smoke.py
plugins/geometry_synthetic/provider.py
tests/unit/test_tonggeometry_adapter.py
```

When all required paths exist, the probe computes an aggregate sha256 model
artifact hash and runs a local model-load smoke.

Required environment variables:

```text
TONGGEOMETRY_TOKENIZER
TONGGEOMETRY_LM_S
TONGGEOMETRY_LM_L
TONGGEOMETRY_CLS
```

## Why It Is Still Blocked

The current environment does not contain those four TongGeometry model artifact
paths, and public artifact discovery did not find trained TongGeometry
checkpoints:

```text
bigai-ai/tong-geometry GitHub release public / 1.0: assets=[]
bigai-ai/tong-geometry public tree: no checkpoint-like model artifact paths
vendored README checkpoint link: empty
Hugging Face searches: no public TongGeometry checkpoint repository found
```

Therefore the dependency probe reports:

```text
checkpoint_hash: null
family: tonggeometry_compatible
```

Release acceptance correctly refuses to pass.

## Commands Supporting This Report

```text
make test-unit TEST_FILTER=tonggeometry_adapter
make test-integration TEST_FILTER=tonggeometry_adapter
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
make smoke-real-tonggeometry
make test-unit TEST_FILTER=release_acceptance
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

All focused tests and smokes passed. The release acceptance command returned
nonzero because it is correctly blocked by the missing TongGeometry-compatible
model checkpoint.

## Required To Unblock

Provide admitted TongGeometry-compatible model artifacts for:

```text
tokenizer
lm_s
lm_l
cls
```

Then rerun:

```text
python scripts/run_tonggeometry_probe.py --request-id probe --claim-spec-json "{}"
python scripts/probe_dependencies.py --json
make smoke-real-tonggeometry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

The blocker can close only if dependency probing reports a non-null
`tonggeometry_compatible` checkpoint hash and TongGeometry probing reports
`model_inference_status=available`.
