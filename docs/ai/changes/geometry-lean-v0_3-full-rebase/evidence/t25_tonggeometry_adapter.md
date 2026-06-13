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
diagnostic blocker for absent tokenizer/lm_s/lm_l/cls model paths.
The probe now records `model_checkpoint_hash`, `model_inference_status`, and
`model_inference_report` when all four model paths are supplied:
`TONGGEOMETRY_TOKENIZER`, `TONGGEOMETRY_LM_S`, `TONGGEOMETRY_LM_L`, and
`TONGGEOMETRY_CLS`. In the current environment those paths are absent, so
model_inference_status remains unavailable. Therefore the smoke establishes a
real external diagnostic path and policy gating, but does not establish
model-backed TongGeometry heavy search.
Additional resolution attempts are recorded in
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_resolution_attempt.md:
Hugging Face API search did not find public TongGeometry checkpoints, the
bigai-ai/tong-geometry GitHub pre-release has no assets, and the vendored README
still contains an empty checkpoint link.
```

Commands run:

```text
make smoke-real-tonggeometry
make test-integration TEST_FILTER=tonggeometry_adapter
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
python -m compileall -q plugins tests scripts
make test-unit TEST_FILTER=tonggeometry_adapter
python -m compileall -q scripts plugins src tests
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

Post-model-smoke hardening:

scripts/run_tonggeometry_model_smoke.py, scripts/run_tonggeometry_probe.py,
plugins/geometry_synthetic/provider.py, and tests/unit/test_tonggeometry_adapter.py
now support aggregate checkpoint hashing and optional model-load smoke evidence
when the tokenizer, small LM, large LM, and classifier checkpoint paths are
configured. Unit coverage verifies missing model paths remain unavailable,
configured paths produce a sha256 aggregate hash, a mocked passing model smoke
marks model_inference_status=available, and the provider adapter reports a
sha256 checkpoint_hash when all checkpoint paths are configured.

make test-unit TEST_FILTER=tonggeometry_adapter passed: 6 tests OK.
python -m compileall -q scripts plugins src tests passed.
```
