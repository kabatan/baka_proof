---
title: T60 solver-backed checker evidence
status: checker_implemented_current_fixture_blocker_detected
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
```

Results:

```json
{
  "solver_backed_checkers_unit": "passed",
  "check_solver_backed_patch_schema": "passed",
  "check_solver_backed_corpus": "passed",
  "check_no_fixture_solver_backed_release": {
    "status": "failed",
    "checked": 20,
    "expected_for_current_run": true
  }
}
```

Interpretation:

- T60 checker implementation is present and unit-covered.
- `check_no_fixture_solver_backed_release.py` correctly detects that the current solver-backed matrix success path still uses fixture provider manifests and fixture adapter versions.
- This leaves release blocker 46 open until B2/B4 solver-backed counted successes run through real provider integration artifacts.
