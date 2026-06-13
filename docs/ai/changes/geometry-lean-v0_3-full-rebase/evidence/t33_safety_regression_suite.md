# T33 Safety regression suite evidence

Task: T33 — Safety regression suite.

Supports:

```text
R-TEST-002
```

Implemented files:

```text
src/math_auto_research/workflow/__init__.py
src/math_auto_research/workflow/standard_geometry_loop.py
tests/unit/test_geometry_standard_loop.py
tests/unit/test_target_library_status.py
tests/unit/test_v03a_real_vs_fixture_integration.py
```

Notes:

```text
T33 full safety verification found and fixed a Base/plugin boundary issue:
src/math_auto_research/workflow/standard_geometry_loop.py imported
plugins.geometry_synthetic directly. The workflow module is now a Base-side
contract object with no geometry_synthetic plugin import. Regression tests
were also synchronized to current LeanGeoSubsetV1 target-library identity and
full-rebase claim ceiling wording.
```

Commands run:

```text
make test-regression
make test-mutation
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
test-regression passed: 114 tests OK; domain/no-loose checks passed.
test-mutation passed: 67 tests OK.
check_domain_contamination passed.
check_no_loose_options passed.
check_model_hardcode passed.
check_resource_bypass passed.
check_no_fixture_release passed.
compileall passed.
```
