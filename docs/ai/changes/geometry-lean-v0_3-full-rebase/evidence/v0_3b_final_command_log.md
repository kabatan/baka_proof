---
title: v0.3B final command log
status: passed_by_split_suite
created: 2026-06-14
authority: evidence
---

# v0.3B final command log

Commands passed:

```text
make test-unit
make test-regression
make test-mutation
make test-integration
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Post-review fix verification commands passed:

```text
python -m unittest tests.unit.test_final_verify_solver_backed_provenance tests.unit.test_solver_backed_checkers tests.unit.test_standard_geometry_loop_solver_backed tests.unit.test_geometry_standard_loop
python -m compileall -q src plugins scripts tests
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
make test-unit TEST_FILTER=solver_backed
make test-unit TEST_FILTER=final_verify_solver_backed
make test-regression TEST_FILTER=solver_backed
make test-mutation TEST_FILTER=solver_backed
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Command attempted but not used as pass evidence:

```text
make test
```

The monolithic `make test` command timed out in the Codex tool after 20 minutes. Its component commands were run separately and passed.

Results:

```json
{
  "make_test": {
    "status": "tool_timeout_after_20_minutes",
    "claim_use": "not_used_as_pass_evidence"
  },
  "make_test_unit": {
    "status": "passed",
    "tests": "267 passed, 1 skipped"
  },
  "make_test_regression": {
    "status": "passed",
    "tests": 118
  },
  "make_test_mutation": {
    "status": "passed",
    "tests": 68
  },
  "make_test_integration": {
    "status": "passed",
    "tests": "35 passed, 1 skipped"
  },
  "make_lean_build": "passed",
  "make_lean_no_sorry": "passed",
  "release_acceptance_v0_3b_report": {
    "status": "passed",
    "core_experiment_ready_status": "passed",
    "solver_backed_proof_repair_status": "passed",
    "tonggeometry_model_backed_status": "blocked",
    "claim_ceiling": "v0_3b_solver_backed_ready_no_tong_model_backed_claim",
    "open_blockers": []
  },
  "post_review_fix_verification": {
    "focused_unittest": "passed, 17 tests",
    "compileall": "passed",
    "solver_backed_matrix_rerun": "passed",
    "solver_backed_artifact_checker": "passed",
    "solver_backed_metrics_checker": "passed",
    "no_fixture_solver_backed_checker": "passed",
    "no_original_proof_checker": "passed",
    "test_unit_solver_backed": "passed, 56 tests",
    "test_unit_final_verify_solver_backed": "passed, 6 tests",
    "test_regression_solver_backed": "passed, 56 tests plus regression guards",
    "test_mutation_solver_backed": "passed, 56 tests",
    "lean_no_sorry": "passed"
  }
}
```

Known non-completion claim:

```text
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY remains blocked by admitted unavailable TongGeometry checkpoint artifacts.
```
