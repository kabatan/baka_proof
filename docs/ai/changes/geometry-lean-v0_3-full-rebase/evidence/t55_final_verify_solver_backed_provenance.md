---
title: T55 final verify solver-backed provenance evidence
status: complete
task: T55
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T55 FinalVerifyGate Solver-Backed Provenance Evidence

## Scope

Implemented solver-backed provenance gating in `FinalVerifyGate`.

When `proof_use_provenance["solver_backed_mode"]` is true, FinalVerifyGate now requires:

- geometry extraction report ref
- goal anchor ref
- protected statement hash
- target library manifest hash
- provider run manifest ref
- normalized solver artifact ref
- compiler result ref
- LeanPatchCandidateV1 ref
- WorkerResult ref
- proof region diff hash
- generated candidate file ref

It records:

- `checked_candidate_file_ref`
- `solver_backed_proof_status`
- `proof_use_provenance_status`
- `proof_region_guard_status`
- `protected_statement_hash_source`

## Verification

```text
make test-unit TEST_FILTER=final_verify_solver_backed
Result: PASS
Ran 4 tests in 24.766s
```

```text
make test-regression TEST_FILTER=final_verify_solver_backed
Result: PASS
Ran 4 tests in 24.769s
domain contamination check passed
no loose options check passed
```

```text
make test-unit TEST_FILTER=final_verify
Result: PASS
Ran 13 tests in 51.284s
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## Claim Ceiling

Allowed after T55:

```text
FinalVerifyGate solver-backed provenance checks are implemented and locally verified.
```

Not allowed after T55:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
provider-backed final theorem success without SolverBackedProofCertificate
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
