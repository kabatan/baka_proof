---
title: T57 standard loop solver-backed path evidence
status: complete_rc_b4_pass
task: T57
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T57 Standard Loop Solver-Backed Path Evidence

## Scope

Implemented the solver-backed release path in `StandardGeometryProofLoop.run_task`:

```text
extraction -> provider -> compiler -> ProofWorker.apply_lean_patch_candidate
-> FinalVerifyGate -> SolverBackedProofCertificate -> TaskRunResult final_theorem
```

The previous unconditional `geometry_chain_diagnostic_only_no_proof_repair_claim` blocker is no longer applied when a passed solver-backed certificate is present.

Artifacts written for solver-backed success include:

- `source_problem_ref.json`
- `generated_candidate_file_ref.json`
- `extraction_report.json`
- `provider_run_manifest.json`
- `provider_result.json`
- `trace_compilation_result.json` or `construction_compilation_result.json`
- `lean_patch_candidate.json`
- `worker_result.json`
- `final_verify_report.json`
- `solver_backed_proof_certificate.json`
- `task_result.json`
- `artifact_index.json`

## Verification

```text
make test-integration TEST_FILTER=standard_geometry_loop_solver_backed
Result: PASS
Ran 1 test in 59.899s
```

```text
make test-regression TEST_FILTER=standard_loop_no_unconditional_provider_block
Result: PASS
Ran 1 test in 59.836s
domain contamination check passed
no loose options check passed
```

```text
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair
Result: FAIL as expected before T58/T59/T60
Reason: script not yet present in this repo at T57.
```

Additional regression:

```text
make test-unit TEST_FILTER=geometry_standard_loop
Result: PASS
Ran 7 tests in 36.151s
```

```text
make test-unit TEST_FILTER=solver_backed_proof_region
Result: PASS
Ran 7 tests in 0.033s
```

```text
make test-unit TEST_FILTER=final_verify
Result: PASS
Ran 14 tests in 45.391s
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## RC-B4 Fixes

The first RC-B4 review returned `FAIL_FIXABLE`. Fix applied:

- `StandardGeometryProofLoop.run_task` now writes explicit `source_problem_ref.json` and `generated_candidate_file_ref.json` per-task artifacts and includes both in `artifact_index.json`.
- The solver-backed integration test asserts both artifact files and confirms the certificate refs match them.

## RC-B4 Review

Guardian boundary reviewer rerun result:

```text
RESULT: PASS
Blockers: none for the scoped RC-B4/T57 packet.
```

## Claim Ceiling

Allowed after T57:

```text
StandardGeometryProofLoop solver-backed release path is implemented and locally verified.
```

Not allowed after T57:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
full solver-backed release matrix completion
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
