# T40 Provider Module Layout Evidence

Task: T40 — Provider module layout refactor.

## Changed Files

```text
plugins/geometry_synthetic/provider.py
plugins/geometry_synthetic/providers/composite_provider.py
plugins/geometry_synthetic/providers/provider_api.py
plugins/geometry_synthetic/providers/provider_run_manifest.py
plugins/geometry_synthetic/providers/newclid_adapter.py
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
scripts/check_provider_layout.py
```

## Result

`plugins/geometry_synthetic/provider.py` is now a backward-compatible facade
with import/re-export statements only. Provider implementation classes and
helper functions were moved to `plugins/geometry_synthetic/providers/**`.

The checker verifies:

```text
- required providers/** files exist
- provider.py defines no classes or implementation functions
- provider internals do not import back from provider.py
- Base src/ does not import engine-family provider internals
```

## Verification

```text
python scripts/check_provider_layout.py
status: passed

python -m compileall -q plugins src scripts tests
status: passed

make test-unit TEST_FILTER=composite_provider
status: passed, 14 tests

make test-integration TEST_FILTER=newclid_adapter
status: passed, 5 tests

make test-integration TEST_FILTER=genesisgeo_adapter
status: passed, 3 tests, 1 skipped

make test-integration TEST_FILTER=tonggeometry_adapter
status: passed, 6 tests

git diff --check
status: passed, CRLF warnings only
```

## Claim Ceiling

T40 is complete. No provider implementation remains in `provider.py`, but no
v0.3 completion claim is made.
