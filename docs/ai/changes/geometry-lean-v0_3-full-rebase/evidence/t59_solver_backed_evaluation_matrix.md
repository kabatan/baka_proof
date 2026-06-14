---
title: T59 solver-backed evaluation matrix evidence
status: passed
created: 2026-06-14
authority: evidence
---

# T59 solver-backed evaluation matrix evidence

Commands run:

```text
python scripts/check_solver_backed_corpus.py
python -m compileall -q plugins src scripts tests
python -m pytest tests/unit/test_proof_worker_solver_patch_application.py tests/unit/test_standard_geometry_loop_solver_backed.py tests/unit/test_final_verify_solver_backed_provenance.py -q
python -m pytest tests/unit/test_construction_compiler_solver_backed_patch.py tests/unit/test_standard_geometry_loop_solver_backed.py tests/unit/test_proof_worker_solver_patch_application.py -q
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
make lean-build
make lean-no-sorry
```

Observed solver-backed matrix metrics:

```json
{
  "B2": {
    "solver_backed_final_theorem_count": 10,
    "geotrace_solver_backed_final_theorem_count": 6,
    "construction_solver_backed_final_theorem_count": 3
  },
  "B4": {
    "solver_backed_final_theorem_count": 10
  }
}
```

Artifact gates:

```json
{
  "check_solver_backed_metrics": "passed",
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

Notes:

- Metrics are derived from per-task `task_result.json` artifacts and only count solver-backed final theorems with `solver_backed_proof_certificate.json`, patch application, generated candidate file refs, and FinalVerifyGate solver-backed status.
- The generated candidate compile path now uses `lake env lean <candidate>` rather than project build cache.
- Target-local `sorry` checks allow a multi-problem source file while still rejecting a target theorem whose repaired MARP proof region contains `sorry`.
- `python -m pytest tests/unit -q` was attempted after the T59 changes but did not complete within 10 minutes; focused T59 regression tests passed.
- `make lean-build` passed. `make lean-no-sorry` passed after excluding runtime output under `runs/` from the repository source no-sorry scan.
