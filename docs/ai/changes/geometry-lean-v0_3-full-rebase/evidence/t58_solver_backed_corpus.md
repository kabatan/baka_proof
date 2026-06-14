---
title: T58 solver-backed corpus evidence
status: complete
task: T58
plan: MARP-GEOLEAN-PLAN-004B
date: 2026-06-14
authority: evidence
---

# T58 Solver-Backed Corpus Evidence

## Scope

Added the solver-backed proof repair corpus:

- `benchmarks/geometry/solver_backed_proof_repair.jsonl`
- `benchmarks/leangeo/SolverBackedProblems/SolverBackedProofRepair.lean`
- `configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml`
- `scripts/check_solver_backed_corpus.py`

Corpus floor:

- total tasks: 10
- geotrace-to-Lean tasks: 6
- construction-to-Lean tasks: 3
- hybrid/side-condition tasks: 1

The source problem file imports `LeanGeo.Abbre`, contains MARP proof regions with `sorry`, and is not imported by the normal `lake build` root.

## Verification

```text
python scripts/check_solver_backed_corpus.py
Result: PASS
status=passed
```

```text
make lean-build
Result: PASS
Build completed successfully.
Notes: Lake emitted dependency-local-change warnings for UnicodeBasic and batteries.
```

```text
make lean-no-sorry
Result: PASS
lean no-sorry check passed
```

```text
python -m compileall -q plugins src scripts tests
Result: PASS
```

## Claim Ceiling

Allowed after T58:

```text
Solver-backed proof repair corpus is implemented and locally verified.
```

Not allowed after T58:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
full solver-backed release matrix completion
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
R-ID VERIFIED
```
