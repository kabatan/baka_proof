# T18 real corpus manifests evidence

Task: T18 — real corpus manifests.

Supports:

```text
R-EVAL-001
```

Implemented files:

```text
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/rejected_by_extraction.jsonl
schemas/geometry/geometry_corpus_jsonl.schema.json
```

Notes:

```text
The JSONL entries reference Lean files importing LeanGeo.Abbre and target only
LeanGeoSubsetV1:1.0.0. The rejected-by-extraction manifest is explicitly not
acceptance eligible.
```

Commands run:

```text
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\leangeo_real_smoke.jsonl
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\geometry_level2_pilot.jsonl
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\rejected_by_extraction.jsonl
python scripts\check_no_fixture_release.py
make test-unit TEST_FILTER=geometry_corpus
make lean-build
make lean-no-sorry
python -m compileall -q src tests scripts
make test-unit TEST_FILTER=real_smoke_corpus
```

Observed results:

```text
all three JSONL manifests validated against geometry.geometry_corpus_jsonl.v1
no fixture release check passed
geometry_corpus unit tests: 3 tests OK
lake build: Build completed successfully
lean no-sorry check passed
compileall passed
real_smoke_corpus unit tests: 5 tests OK
```

Known warning:

```text
make lean-build emitted existing .lake dependency local-change warnings for
UnicodeBasic and batteries; build completed successfully.
```
