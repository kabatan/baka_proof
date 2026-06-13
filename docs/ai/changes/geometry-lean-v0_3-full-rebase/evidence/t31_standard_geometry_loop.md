# T31 Standard geometry proof loop evidence

Task: T31 — Standard geometry proof loop.

Supports:

```text
MECH-PROOF-001
```

Implemented files:

```text
src/math_auto_research/workflow/standard_geometry_loop.py
src/math_auto_research/workflow/__init__.py
tests/unit/test_geometry_standard_loop.py
tests/unit/test_standard_geometry_loop.py
```

Notes:

```text
Plan-path workflow/standard_geometry_loop.py exports the existing standard
geometry proof loop. The fixture loop covers LeanPort compile, GoalAnchor,
geometry extraction, geometry.solve, TraceCompiler, bridge gate, worker patch
candidate, FinalVerifyGate, DAG update, RunLogger, and structured feedback.
Target closure occurs only after FinalVerifyGate returns final_theorem.
```

Commands run:

```text
make smoke-geometry-final-verify
make test-integration TEST_FILTER=standard_geometry_loop
make test-unit TEST_FILTER=geometry_standard_loop
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
smoke-geometry-final-verify passed with final_verify proof_use_status=final_theorem and DAG final patch committed.
standard_geometry_loop integration tests: 7 tests OK.
geometry_standard_loop unit tests: 6 tests OK.
compileall passed.
```
