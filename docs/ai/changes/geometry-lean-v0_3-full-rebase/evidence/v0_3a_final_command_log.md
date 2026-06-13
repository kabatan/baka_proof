---
title: v0.3A final command log
task: T46
status: COMPLETE
created: 2026-06-13
---

# v0.3A final command log

All commands were run from:

```text
C:\Users\bakat\work\AI_math_research
```

## Commands

This final command pass includes the post-review hardening that:

```text
1. rejects fixture adapter-version tokens in B2/B4 release provider manifests;
2. prevents provider-backed geometry tasks from being counted as final theorem/proof repair success;
3. keeps remaining B2/B4 final theorem counts limited to tasks where geometry_provider is not_required_for_task.
```

```text
make test
```

Result:

```text
PASS
Unit: Ran 214 tests, OK (skipped=1)
Regression: Ran 118 tests, OK
Mutation: Ran 68 tests, OK
Integration: Ran 35 tests, OK (skipped=1)
```

```text
make test-regression
```

Result:

```text
PASS
Ran 118 tests, OK
domain contamination check passed
no loose options check passed
```

```text
make test-mutation
```

Result:

```text
PASS
Ran 68 tests, OK
```

```text
make lean-build
```

Result:

```text
PASS
Build completed successfully.
```

Observed warnings:

```text
UnicodeBasic and batteries package repositories under .lake reported local changes.
```

```text
make lean-no-sorry
```

Result:

```text
PASS
lean no-sorry check passed
```

```text
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Result:

```text
PASS
status=passed
core_experiment_ready_status=passed
tonggeometry_model_backed_status=blocked
claim_ceiling=core_experiment_ready_passed_no_tong_model_backed_claim
open_blockers=[]
blocked_claims=["V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"]
checked_blockers=1-34
release_blocker_24_level2_matrix_run_replay=passed
release_blocker_25_closure_claims_do_not_exceed_evidence=passed with open_blockers_before_closure=[]
release_blocker_30_matrix_artifact_derived=passed
B2/B4 provider manifests contain no fixture adapter-version tokens
B2/B4 tasks with provider_run_manifest.json do not claim proof_use_status=final_theorem
```

## Claim impact

The final verification suite supports `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed`.

The suite does not support `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: passed`; that claim remains blocked by unavailable TongGeometry model checkpoint artifacts.
