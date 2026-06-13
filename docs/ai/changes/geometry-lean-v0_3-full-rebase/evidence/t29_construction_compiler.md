# T29 ConstructionCompiler evidence

Task: T29 — ConstructionCompiler.

Supports:

```text
R-AUX-002
```

Implemented files:

```text
plugins/geometry_synthetic/construction/construction_compiler.py
plugins/geometry_synthetic/construction/__init__.py
lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/ConstructionTemplates.lean
lean/MathAutoResearch.lean
tests/unit/test_construction_compiler.py
```

Notes:

```text
Plan-path construction_compiler.py exports ConstructionCompiler and result
types. ConstructionCompiler now blocks missing dependency refs and missing
nondegeneracy side conditions, while continuing to generate Lean patch
candidates and side-condition obligations. ConstructionTemplates.lean is
imported by the Lean root so lean-build checks it.
```

Commands run:

```text
make smoke-geometry-construction
make test-unit TEST_FILTER=construction_compiler
make test-mutation TEST_FILTER=construction_compiler
make lean-build
make test-unit TEST_FILTER=schema_validation
python -m compileall -q plugins tests scripts
```

Observed results:

```text
smoke-geometry-construction passed and the emitted construction Lean patch checked with lean_exit_code=0.
construction_compiler unit tests: 5 tests OK.
construction_compiler mutation tests: 5 tests OK.
lean-build completed successfully.
lean-build warning: .lake package repositories UnicodeBasic and batteries report local changes in the dependency cache.
schema_validation unit tests: 9 tests OK.
compileall passed.
```
