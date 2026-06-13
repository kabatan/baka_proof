# T21 GeometrySolverPolicy and GeometryExecutionPlan evidence

Task: T21 — GeometrySolverPolicy and GeometryExecutionPlan.

Supports:

```text
R-SOLVER-006
R-RSRC-*
```

Implemented files:

```text
plugins/geometry_synthetic/solver_policy/geometry_solver_policy.py
plugins/geometry_synthetic/solver_policy/geometry_solver_policy_v1.yaml
plugins/geometry_synthetic/solver_policy/execution_plan.py
configs/solver_policies/geometry_synthetic_v1.yaml
```

Notes:

```text
The Plan-path modules re-export the existing policy implementation while
preserving established imports from plugins.geometry_synthetic.policy.
```

Commands run:

```text
make test-unit TEST_FILTER=geometry_solver_policy
make test-unit TEST_FILTER=resource_budget
python -m compileall -q plugins tests
```

Observed results:

```text
geometry_solver_policy unit tests: 5 tests OK
resource_budget unit tests: 3 tests OK
compileall passed
```
