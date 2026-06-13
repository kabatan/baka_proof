# T44 Artifact-Derived Level2 Matrix Evidence

Task: T44 — Artifact-derived Level2 matrix.

## Changed Files

```text
plugins/geometry_synthetic/evaluation.py
src/math_auto_research/lean_integration/lean_port.py
scripts/check_matrix_artifact_derived.py
```

Generated local run artifacts:

```text
runs/geometry_level2_pilot/
```

`runs/` is intentionally gitignored; the command evidence below records the
local generated artifact state.

## Result

`scripts/run_geometry_level2_matrix.py` now executes each selected benchmark
task under each B0-B5 baseline through `StandardGeometryProofLoop.run_task`.
For the 25-task pilot corpus this produced:

```text
per_task_run_count: 150
expected_per_task_run_count: 150
artifact_derived_metrics: true
fixture_run_used: false
metrics_source: per_task_task_run_results
per_task_artifact_index_ref: per_task_artifact_index.json
```

Metrics are computed from `TaskRunResult` artifacts and the per-task artifact
index, not from task category labels alone.

## Verification

```text
make test-unit TEST_FILTER=evaluation_matrix
status: passed, 4 tests

python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
status: passed

python scripts/check_matrix_artifact_derived.py --run-dir runs/geometry_level2_pilot
status: passed

python scripts/generate_repro_report.py --run-dir runs/geometry_level2_pilot
status: passed

python -m compileall -q plugins src scripts tests
status: passed

git diff --check
status: passed, CRLF warnings only
```

## Claim Ceiling

T44 is complete. No Level2 advantage claim is made; the matrix report remains a
pilot-count experiment-readiness artifact.
