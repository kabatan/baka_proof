---
title: T62 solver-backed smoke and mutation evidence
status: passed
created: 2026-06-14
authority: evidence
---

# T62 solver-backed smoke and mutation evidence

Commands run:

```text
make smoke-solver-backed-proof-repair
make smoke-solver-backed-geotrace-final
make smoke-solver-backed-construction-final
make test-regression TEST_FILTER=solver_backed
make test-mutation TEST_FILTER=solver_backed
```

Results:

```json
{
  "smoke_solver_backed_proof_repair": "passed",
  "smoke_solver_backed_geotrace_final": "passed",
  "smoke_solver_backed_construction_final": "passed",
  "solver_backed_regression_tests": {
    "status": "passed",
    "tests": 42
  },
  "solver_backed_mutation_tests": {
    "status": "passed",
    "tests": 42
  },
  "solver_backed_release_counts": {
    "B2": {
      "solver_backed_final_theorem_count": 10,
      "geotrace_solver_backed_final_theorem_count": 6,
      "construction_solver_backed_final_theorem_count": 3
    },
    "B4": {
      "solver_backed_final_theorem_count": 10
    }
  }
}
```

The smoke target checks include corpus validity, solver-backed metrics floors, counted artifact completeness, no original source theorem counted as solver-backed, and no fixture engine run in the certified solver artifact path.
