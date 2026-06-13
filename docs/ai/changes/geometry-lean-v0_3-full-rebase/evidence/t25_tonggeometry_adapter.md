# T25 TongGeometry-compatible real adapter evidence

Task: T25 — TongGeometry-compatible real adapter.

Supports:

```text
R-SOLVER-005
```

Implemented files:

```text
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
scripts/smoke_real_tonggeometry.py
tests/unit/test_tonggeometry_adapter.py
tests/unit/test_heavy_search_budget_gate.py
tests/unit/test_heavy_search_no_orphans.py
scripts/run_tonggeometry_probe.py
Makefile
```

Notes:

```text
Plan-path tonggeometry_adapter.py exposes the TongGeometry-compatible heavy
search adapter and a normalized-output selector. The provider path already
runs heavy search only under heavy/extreme policy admission and explicit
escalation, through ResourceGovernor and run_process_group. Raw TongGeometry
diagnostic output remains non-proof material.
```

Environment diagnostic:

```text
Vendored TongGeometry source is present at vendor/tong-geometry commit
d00925f07dc3174f91326386cb8e785e539a91a1. In this environment,
scripts/run_tonggeometry_probe.py reports python_import_status=available but
diagnostic blocker missing_tonggeometry_model_paths:tokenizer,lm_s,lm_l,cls.
Therefore the smoke establishes a real external diagnostic path and policy
gating, but does not establish model-backed TongGeometry heavy search.
```

Commands run:

```text
make smoke-real-tonggeometry
make test-integration TEST_FILTER=tonggeometry_adapter
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
python -m compileall -q plugins tests scripts
```

Observed results:

```text
smoke-real-tonggeometry passed. Medium budget did not schedule heavy_search.
Heavy budget with explicit escalation emitted heavy_search engine_family
tonggeometry_compatible, engine_version
tong-geometry@d00925f07dc3174f91326386cb8e785e539a91a1, fixture_flag=false,
real_integration_flag=true, and ResourceUsageReport.logs_ref=external_tonggeometry_stdout.
Provider result proof_use_status remained not_allowed.
tonggeometry_adapter integration tests: 4 tests OK.
heavy_search_budget_gate regression: 1 test OK; domain/no-loose checks passed.
heavy_search_no_orphans regression: 1 test OK; domain/no-loose checks passed.
compileall passed.
```
