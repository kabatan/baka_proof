---
title: T50 solver-backed proof-region guard evidence
status: complete_rc_b1_pass
task: T50
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T50 Solver-Backed Proof-Region Guard Evidence

## Scope

Implemented the v0.3B problem-source and proof-region guard layer for `INV-B006` and `R-WORKER-B001`.

This task establishes:

- MARP proof-region markers as the admitted repair region for solver-backed source problems.
- Source problem policy: `sorry` may appear only inside `MARP_PROOF_REGION_START/END` regions.
- Generated candidate policy: no `sorry`.
- Region guard rejection for theorem statement edits and edits outside admitted proof/helper regions.
- Generated candidate output under a supplied output directory without mutating source problem files.
- `lean-no-sorry` treatment that keeps normal Lean build artifacts strict while validating solver-backed source problems separately.

This task does not claim end-to-end proof repair or solver-backed final theorem readiness.

## Files

- `benchmarks/leangeo/SolverBackedProblems/README.md`
- `lean/MathAutoResearch/Geometry/Generated/.gitkeep`
- `plugins/geometry_synthetic/patching/proof_region.py`
- `tests/unit/test_solver_backed_proof_region.py`
- `scripts/check_lean_no_sorry.py`

## Verification

```text
make test-unit TEST_FILTER=solver_backed_proof_region
Result: PASS
Ran 7 tests in 0.020s
```

```text
make lean-no-sorry
Result: PASS
lean no-sorry check passed
```

```text
make lean-build
Result: PASS
Build completed successfully.
Notes: Lake emitted warnings that dependency repositories under .lake/packages/UnicodeBasic and .lake/packages/batteries have local changes.
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

Additional regression after RC-B1 fixes:

```text
make test-unit TEST_FILTER=trace_compiler
Result: PASS
Ran 8 tests in 0.021s
```

```text
make test-unit TEST_FILTER=construction
Result: PASS
Ran 9 tests in 0.041s
```

```text
make test-unit TEST_FILTER=proof_worker
Result: PASS
Ran 2 tests in 0.000s
```

```text
make test-unit TEST_FILTER=schema_validation
Result: PASS
Ran 9 tests in 0.081s
```

## RC-B1 Fixes

The first RC-B1 review returned `FAIL_FIXABLE`. T50-related fixes applied:

- Added `apply_lean_patch_candidate(source_problem_path, patch_candidate, output_dir, context) -> WorkerResult`.
- The worker API records `patch_applied`, `generated_candidate_file_ref`, `proof_region_diff_hash`, and `solver_dependency_refs`.
- Patch application writes generated candidates under a run/task output directory and does not mutate source problem files.
- The proof-region guard uses the strict `proof_region_replacement_text` field from `LeanPatchCandidateV1`, not arbitrary metadata.

## RC-B1 Review

Guardian boundary reviewer rerun result:

```text
RESULT: PASS
Blockers: none found for T49/T50 packet scope.
```

Reviewer cautions:

```text
This does not support claiming full V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY.
This does not cover later T51+ compiler, FinalVerifyGate, TrustGuard, standard loop, corpus, metrics, or release acceptance work.
No R-ID is marked VERIFIED.
```

## Claim Ceiling

Allowed after T50:

```text
T50 proof-region guard behavior is implemented and locally verified.
```

Not allowed after T50:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
provider-backed final theorem success
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
