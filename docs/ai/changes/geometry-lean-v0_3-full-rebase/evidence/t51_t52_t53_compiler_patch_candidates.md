---
title: T51-T53 compiler patch candidate evidence
status: complete_rc_b2_pass
tasks: T51,T52,T53
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T51-T53 Compiler Patch Candidate Evidence

## Scope

Implemented the v0.3B compiler patch-candidate floor:

- `TraceCompiler` emits `LeanPatchCandidateV1` for the required trace template floor:
  - `trace.coll_self_left.v1`
  - `trace.coll_self_right.v1`
  - `trace.collinear_or_left.v1`
  - `trace.collinear_and_intro.v1`
- `ConstructionCompiler` emits `LeanPatchCandidateV1` for the required construction template floor:
  - `construction.exists_existing_line_witness.v1`
  - `construction.distinct_points_on_line_pack.v1`
  - `construction.exists_point_collinear_self.v1`
- Unsupported compiler inputs remain blocked.
- Compiler outputs remain `lean_patch_candidate`; they do not claim final theorem status.
- Raw provider output flagged as proof material is rejected by `LeanPatchCandidateV1`.

This task does not claim solver-backed proof repair readiness.

## Verification

```text
make test-unit TEST_FILTER=trace_compiler_solver_backed_patch
Result: PASS
Ran 3 tests in 0.001s
```

```text
make test-mutation TEST_FILTER=trace_compiler_solver_backed
Result: PASS
Ran 4 tests in 0.002s
```

```text
make test-unit TEST_FILTER=construction_compiler_solver_backed_patch
Result: PASS
Ran 2 tests in 0.001s
```

```text
make test-mutation TEST_FILTER=construction_compiler_solver_backed
Result: PASS
Ran 3 tests in 0.001s
```

```text
make test-regression TEST_FILTER=compiler_patch_candidate
Result: PASS
Ran 3 tests in 0.001s
domain contamination check passed
no loose options check passed
```

Additional regression:

```text
make test-unit TEST_FILTER=trace_compiler
Result: PASS
Ran 12 tests in 0.023s
```

```text
make test-unit TEST_FILTER=construction
Result: PASS
Ran 12 tests in 0.030s
```

```text
make test-unit TEST_FILTER=solver_backed_schema
Result: PASS
Ran 8 tests in 0.001s
```

```text
make test-unit TEST_FILTER=schema_validation
Result: PASS
Ran 9 tests in 0.080s
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## Boundary Note

During T53 verification, `check_domain_contamination.py` found a Base-layer import of the geometry plugin in `proof_worker.py`. The implementation was corrected so the Base `apply_lean_patch_candidate` interface uses structural access to patch-candidate fields and no longer imports plugin modules.

## RC-B2 Review

Guardian boundary reviewer result:

```text
RESULT: PASS
Blockers: none for RC-B2 scope T51, T52, T53 against R-COMPILER-B001, R-COMPILER-B002, R-COMPILER-B003.
```

Reviewer cautions:

```text
Do not claim V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY.
Do not claim provider-backed final theorem success.
Do not claim SOURCE_FAITHFUL, ACCEPTANCE_COMPLETE, or any R-ID VERIFIED.
```

## Claim Ceiling

Allowed after T51-T53:

```text
Compiler patch-candidate floor is implemented and locally verified.
```

Not allowed after T51-T53:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
provider-backed final theorem success
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
