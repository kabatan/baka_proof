---
title: T49 solver-backed schema patch evidence
status: complete
task: T49
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T49 Solver-Backed Schema Patch Evidence

## Scope

Implemented the v0.3B schema patch for `R-SCHEMA-B001` through `R-SCHEMA-B004`:

- `LeanPatchCandidateV1`
- `SolverBackedProofCertificate`
- `TaskRunResult` v0.3B extension fields
- `FinalVerifyReport` v0.3B extension fields
- `TraceCompilationResult`, `ConstructionCompilationResult`, and `WorkerResult` extension fields

This task does not claim solver-backed proof repair readiness. It only establishes the typed records, JSON schema files, deterministic identifiers, and negative validation behavior needed by later proof-repair tasks.

## Files

- `plugins/geometry_synthetic/patching/lean_patch_candidate_v1.py`
- `plugins/geometry_synthetic/proof/solver_backed_proof_certificate.py`
- `schemas/geometry/lean_patch_candidate_v1.schema.json`
- `schemas/geometry/solver_backed_proof_certificate.schema.json`
- `scripts/check_solver_backed_patch_schema.py`
- `tests/unit/test_solver_backed_schema.py`

Existing record/schema contracts were patched for:

- `TaskRunResult`
- `FinalVerifyReport`
- `TraceCompilationResult`
- `ConstructionCompilationResult`
- `WorkerResult`

## Verification

```text
make test-unit TEST_FILTER=solver_backed_schema
Result: PASS
Ran 6 tests in 0.001s
```

```text
python scripts/check_solver_backed_patch_schema.py
Result: PASS
status=passed
checks=schema_loaded for both new schema files; negative_validation_cases_passed
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

Additional regression checks:

```text
make test-unit TEST_FILTER=schema_validation
Result: PASS
Ran 9 tests in 0.076s
```

```text
make test-unit TEST_FILTER=trace_compiler
Result: PASS
Ran 8 tests in 0.006s
```

```text
make test-unit TEST_FILTER=construction
Result: PASS
Ran 9 tests in 0.014s
```

```text
make test-unit TEST_FILTER=proof_worker
Result: PASS
Ran 2 tests in 0.000s
```

```text
make test-unit TEST_FILTER=final_verify
Result: PASS
Ran 8 tests in 37.326s
```

## Claim Ceiling

Allowed after T49:

```text
T49 schema patch is implemented and locally verified.
```

Not allowed after T49:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
v0_3b_solver_backed_ready_no_tong_model_backed_claim
provider-backed final theorem success
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
