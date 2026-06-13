# T17 LeanGeoSubsetV1 theorem grammar and mappings evidence

Task: T17 — LeanGeoSubsetV1 theorem grammar and mappings.

Supports:

```text
R-GEO-001
R-GEO-002
R-GEO-003
```

Implemented files:

```text
plugins/geometry_synthetic/target_subset/leangeo_subset_v1.yaml
plugins/geometry_synthetic/target_subset/predicate_mapping.yaml
plugins/geometry_synthetic/target_subset/construction_mapping.yaml
plugins/geometry_synthetic/target_subset/relation_mapping.yaml
MathAutoResearch/Geometry/LeanGeoSubsetV1/Grammar.lean
```

Notes:

```text
The .yaml files use JSON-compatible YAML syntax so the existing lightweight
artifact reader can consume them without adding a new parser dependency.
Existing grammar JSON remains for backward-compatible tests and extraction.
```

Commands run:

```text
make test-unit TEST_FILTER=target_subset
make lean-build
python -m compileall -q plugins tests
make lean-no-sorry
python scripts\check_domain_contamination.py
```

Observed results:

```text
target_subset unit tests: 4 tests OK
lake build: Build completed successfully
compileall passed
lean no-sorry check passed
domain contamination check passed
```

Known warning:

```text
make lean-build emitted existing .lake dependency local-change warnings for
UnicodeBasic and batteries; build completed successfully.
```
