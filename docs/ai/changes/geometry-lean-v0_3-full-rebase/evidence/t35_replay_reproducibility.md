# T35 Replay and reproducibility evidence

Task: T35 — Replay and reproducibility.

Supports:

```text
R-BASE-002
R-EVAL-001
R-EVAL-002
R-EVAL-003
R-EVAL-004
```

Implemented files:

```text
src/math_auto_research/workflow/replay.py
scripts/generate_repro_report.py
plugins/geometry_synthetic/run_trace.py
tests/unit/test_run_trace.py
tests/unit/test_replay.py
src/math_auto_research/workflow/__init__.py
```

Notes:

```text
Base workflow replay now inspects run directories without importing geometry
plugin code. It reconstructs replay-critical artifact presence, content hashes,
matrix metric artifacts, restored components, missing components, and writes a
ReproducibilityReport. The geometry plugin delegates its reproducibility report
builder to the Base workflow API. The CLI now replays an existing run directory
instead of silently creating fixture output for a missing run.
```

Commands run:

```text
make test-integration TEST_FILTER=replay
python scripts/generate_repro_report.py --run-dir runs/geometry_level2_pilot
make test-unit TEST_FILTER=run_trace
python -m compileall -q src plugins tests scripts
python scripts/check_domain_contamination.py
python scripts/check_no_fixture_release.py
make test-unit TEST_FILTER=replay
```

Observed results:

```text
test-integration replay: 3 tests OK.
generate_repro_report restored runs/geometry_level2_pilot with no missing components.
run_trace unit tests: 3 tests OK.
compileall passed.
domain contamination check passed.
no fixture release check passed.
replay unit tests: 3 tests OK.
```
