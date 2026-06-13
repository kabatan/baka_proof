# T16 geometry_synthetic plugin scaffold evidence

Task: T16 — geometry_synthetic plugin scaffold.

Supports:

```text
INV-003
R-SOLVER-001
```

Implemented scaffold paths:

```text
plugins/geometry_synthetic/plugin.yaml
plugins/geometry_synthetic/README.md
plugins/geometry_synthetic/solver_policy/
plugins/geometry_synthetic/providers/
plugins/geometry_synthetic/target_subset/
plugins/geometry_synthetic/extraction/
plugins/geometry_synthetic/trace/
plugins/geometry_synthetic/construction/
plugins/geometry_synthetic/bridge/
```

Compatibility note:

```text
Existing module imports such as plugins.geometry_synthetic.bridge are preserved
by converting conflicting single-file modules into packages with __init__.py.
No Base runtime domain branch was added.
```

Commands run:

```text
make test-unit TEST_FILTER=geometry_plugin_scaffold
python scripts\check_domain_contamination.py
python -m compileall -q plugins tests
make test-unit TEST_FILTER=geometry
```

Observed results:

```text
geometry_plugin_scaffold unit tests: 3 tests OK
domain contamination check passed
compileall passed
geometry unit tests: 30 tests OK
```

Follow-up compatibility fix:

```text
plugins/geometry_synthetic/standard_loop.py now uses GoalAnchor.protected_statement_hash
and passes proof-use provenance into FinalVerifyGate, matching the RC-3
FinalVerify provenance contract.
```
