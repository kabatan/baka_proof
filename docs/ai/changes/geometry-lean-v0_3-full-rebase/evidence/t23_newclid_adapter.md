# T23 Newclid-compatible real adapter evidence

Task: T23 — Newclid-compatible real adapter.

Supports:

```text
R-SOLVER-003
```

Implemented files:

```text
plugins/geometry_synthetic/providers/newclid_adapter.py
scripts/smoke_real_newclid.py
tests/unit/test_newclid_adapter.py
Makefile
```

Notes:

```text
Plan-path newclid_adapter.py exposes the Newclid-compatible adapter and
conversion helpers. The real path runs python -m newclid through the
ResourceGovernor-managed external process path, normalizes accepted output to
a geotrace: ref, emits ProviderRunManifest and ResourceUsageReport data, and
returns unsupported translations as diagnostic blockers. The smoke target
fails if a fixture path is selected for the real Newclid smoke run.
```

Commands run:

```text
make smoke-real-newclid
make test-integration TEST_FILTER=newclid_adapter
python scripts/check_no_fixture_release.py
python -m compileall -q plugins tests scripts
```

Observed results:

```text
smoke-real-newclid passed with newclid==3.0.1;py-yuclid==3.0.0;yuclid==dc40a72767c15a90.
The smoke emitted geotrace:geometry_request:real_newclid_smoke:symbolic_closure:newclid_real,
ProviderRunManifest.fixture_flag=false, ProviderRunManifest.real_integration_flag=true,
and ResourceUsageReport.logs_ref=external_newclid_stdout.
newclid_adapter integration tests: 3 tests OK.
check_no_fixture_release passed.
compileall passed.
```
