---
title: T60 solver-backed checker evidence
status: checker_implemented_real_provider_path_passed
created: 2026-06-14
authority: evidence
---

# T60 solver-backed checker evidence

Commands run:

```text
make test-unit TEST_FILTER=solver_backed_checkers
python scripts/check_solver_backed_patch_schema.py
python scripts/check_solver_backed_corpus.py
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
```

Results:

```json
{
  "solver_backed_checkers_unit": "passed",
  "check_solver_backed_patch_schema": "passed",
  "check_solver_backed_corpus": "passed",
  "check_no_fixture_solver_backed_release": {
    "status": "passed",
    "checked": 20
  },
  "check_solver_backed_metrics": {
    "status": "passed",
    "B2": {
      "solver_backed_final_theorem_count": 10,
      "geotrace_solver_backed_final_theorem_count": 6,
      "construction_solver_backed_final_theorem_count": 3
    },
    "B4": {
      "solver_backed_final_theorem_count": 10
    }
  },
  "check_solver_backed_artifacts": {
    "status": "passed",
    "counted": 20
  },
  "check_no_original_proof_counted_as_solver_backed": {
    "status": "passed",
    "checked": 20
  }
}
```

Interpretation:

- T60 checker implementation is present and unit-covered.
- The regenerated solver-backed matrix has B2/B4 counted successes whose certified solver artifacts resolve to real Newclid/GenesisGeo engine runs.
- Release blockers 41-46 pass for `runs/geometry_solver_backed_proof_repair`; release acceptance wiring remains T61.
