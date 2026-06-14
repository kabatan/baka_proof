---
title: T56 solver-backed certificate and trust evidence
status: complete_rc_b3_pass
task: T56
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T56 Solver-Backed Certificate and Trust Evidence

## Scope

Implemented SolverBackedProofCertificate generation and certificate-aware TrustGuard behavior:

- `plugins/geometry_synthetic/proof/certificate_builder.py`
- `plugins/geometry_synthetic/proof/__init__.py`
- `plugins/geometry_synthetic/bridge/__init__.py`
- `tests/unit/test_solver_backed_proof_certificate.py`
- `tests/unit/test_solver_backed_laundering.py`

The certificate builder requires:

- FinalVerifyGate `proof_use_status = final_theorem`
- `solver_backed_proof_status = passed`
- unchanged theorem hash
- `proof_region_diff_hash`
- generated candidate file ref
- patch-applied WorkerResult
- normalized solver artifact dependency

TrustGuard rejects solver-backed final theorem closure without a passed certificate.

## Verification

```text
make test-unit TEST_FILTER=solver_backed_proof_certificate
Result: PASS
Ran 4 tests in 0.001s
```

```text
make test-regression TEST_FILTER=solver_backed_laundering
Result: PASS
Ran 4 tests in 0.001s
domain contamination check passed
no loose options check passed
```

```text
make test-unit TEST_FILTER=geometry_bridge
Result: PASS
Ran 9 tests in 0.001s
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## RC-B3 Fixes

The first RC-B3 review returned `FAIL_FIXABLE`. T56-related fixes:

- Certificate builder now requires `protected_statement_hash` to match `FinalVerifyReport.theorem_statement_hash`.
- TrustGuard now accepts `solver_backed_required=True` and enforces a passed certificate even if the FinalVerifyReport is otherwise marked `not_applicable` for solver-backed status.
- Regression tests cover theorem hash mismatch and provider-backed/solver-backed final theorem requests without certificates.

## RC-B3 Review

Guardian boundary reviewer rerun result:

```text
RESULT: PASS
Concrete blockers: none for the RC-B3 T55/T56 packet.
```

## Claim Ceiling

Allowed after T56:

```text
SolverBackedProofCertificate builder and certificate-aware TrustGuard behavior are implemented and locally verified.
```

Not allowed after T56:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
provider-backed final theorem success in standard loop/release matrix
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
