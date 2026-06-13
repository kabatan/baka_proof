# T19 GeometryExtractionContract evidence

Task: T19 — GeometryExtractionContract.

Supports:

```text
R-EXTRACT-001
R-EXTRACT-002
R-EXTRACT-003
```

Implemented files:

```text
plugins/geometry_synthetic/extraction/extraction_contract.py
plugins/geometry_synthetic/extraction/extraction_report.py
plugins/geometry_synthetic/extraction/claim_spec.py
plugins/geometry_synthetic/extraction/__init__.py
```

Notes:

```text
Accepted GeometryClaimSpec records now include extraction_report_ref,
goal_anchor_ref, protected_statement_hash, target_library_manifest_hash, and
proof_use_status=not_allowed. Unsupported and ambiguous forms continue to
safe-reject without producing a claim.
```

Commands run:

```text
make test-unit TEST_FILTER=geometry_extraction
make test-mutation TEST_FILTER=extraction
make test-unit TEST_FILTER=geometry_standard_loop
python -m compileall -q plugins tests
python scripts\check_domain_contamination.py
make smoke-geometry-extraction
```

Observed results:

```text
geometry_extraction unit tests: 11 tests OK
extraction mutation suite: 56 tests OK
geometry_standard_loop unit tests: 5 tests OK
compileall passed
domain contamination check passed
smoke-geometry-extraction passed and emitted accepted extraction report
```

Smoke output:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/leangeo_extraction_smoke.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/wsl_leangeo_check_output.log
```

Known warning:

```text
The Lean smoke emitted existing .lake dependency local-change warnings for
UnicodeBasic and batteries; extraction still accepted the Lean #check output.
```
