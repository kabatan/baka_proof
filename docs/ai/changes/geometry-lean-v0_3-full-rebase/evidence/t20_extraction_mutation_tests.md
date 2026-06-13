# T20 extraction mutation tests evidence

Task: T20 — extraction mutation tests.

Supports:

```text
R-EXTRACT-*
R-TEST-002
```

Mutation fixtures added:

```text
local notation ambiguity
missing nondegeneracy
unsupported orientation
related-only target
raw DSL claim
```

Commands run:

```text
make test-mutation TEST_FILTER=extraction
make test-mutation
make test-unit TEST_FILTER=extraction
python -m compileall -q plugins tests
python scripts\check_domain_contamination.py
```

Observed results:

```text
filtered extraction mutation tests: 16 tests OK
full mutation target: 56 tests OK
extraction unit tests: 16 tests OK
compileall passed
domain contamination check passed
```
