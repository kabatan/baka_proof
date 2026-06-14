---
title: T54 proof worker patch application evidence
status: complete
task: T54
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T54 ProofWorker Patch Application Evidence

## Scope

Implemented the plugin-facing patch application adapter:

- `plugins/geometry_synthetic/patching/apply_patch.py`
- `tests/unit/test_proof_worker_solver_patch_application.py`
- `tests/unit/test_worker_cannot_claim_final.py`

The Base interface `apply_lean_patch_candidate` was already added during the RC-B1 fix and remains implemented in `src/math_auto_research/model_api/proof_worker.py`.

The worker records:

- `patch_applied`
- `generated_candidate_file_ref`
- `proof_region_diff_hash`
- `solver_dependency_refs`

Worker output remains non-final proof evidence and cannot claim `final_theorem`.

## Verification

```text
make test-unit TEST_FILTER=proof_worker_solver_patch
Result: PASS
Ran 2 tests in 0.026s
```

```text
make test-regression TEST_FILTER=worker_cannot_claim_final
Result: PASS
Ran 2 tests in 0.000s
domain contamination check passed
no loose options check passed
```

```text
python scripts/check_domain_contamination.py
Result: PASS
domain contamination check passed
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## Claim Ceiling

Allowed after T54:

```text
ProofWorker patch application is implemented and locally verified.
```

Not allowed after T54:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
provider-backed final theorem success
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
