# T34 Level2 pilot benchmark matrix evidence

Task: T34 — Level2 pilot benchmark matrix.

Supports:

```text
R-EVAL-001
R-EVAL-002
R-EVAL-003
R-EVAL-004
```

Implemented files:

```text
configs/benchmark_runs/geometry_level2_pilot.yaml
plugins/geometry_synthetic/evaluation.py
Makefile
tests/unit/test_evaluation_matrix.py
```

Notes:

```text
geometry_level2_pilot.yaml defines B0/B1/B2/B3/B4/B5 as evaluation
configuration entries, not runtime modes. B2 references the selected geometry
provider config. B5 disables construction only through evaluation config
metadata. run_level2_matrix now clears an existing run directory before writing
to avoid partial overwrite reads. The pilot matrix remains a fixture-level,
replayable matrix and does not claim Level2 advantage.
```

Commands run:

```text
make smoke-level2-pilot
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
make test-unit TEST_FILTER=evaluation_matrix
python scripts/check_no_fixture_release.py
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
smoke-level2-pilot passed and wrote runs/geometry_level2_pilot.
run_geometry_level2_matrix passed with B0-B5 and replay_status=restored.
evaluation_matrix unit tests: 3 tests OK.
check_no_fixture_release passed.
compileall passed.
```
