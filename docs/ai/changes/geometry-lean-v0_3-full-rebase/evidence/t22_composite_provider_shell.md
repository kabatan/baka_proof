# T22 CompositeSyntheticGeometryProvider shell evidence

Task: T22 — CompositeSyntheticGeometryProvider shell.

Supports:

```text
R-SOLVER-001
R-SOLVER-002
R-BASE-*
```

Implemented files:

```text
plugins/geometry_synthetic/providers/provider_api.py
plugins/geometry_synthetic/providers/composite_provider.py
plugins/geometry_synthetic/providers/provider_run_manifest.py
```

Notes:

```text
Plan-path provider modules re-export the existing composite provider
implementation while preserving the single Base-visible provider boundary.
```

Commands run:

```text
make smoke-geometry-provider
make test-unit TEST_FILTER=composite_provider
make test-regression TEST_FILTER=provider_not_base_branching
python -m compileall -q plugins tests
```

Observed results:

```text
smoke-geometry-provider passed and emitted ProviderRunManifest/ResourceUsageReport output
composite_provider unit tests: 14 tests OK
provider_not_base_branching regression: 1 test OK; domain/no-loose checks passed
compileall passed
```
