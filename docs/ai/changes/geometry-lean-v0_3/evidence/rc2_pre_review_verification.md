---
title: RC-2 Pre-Review Verification
task: RC-2 — target subset and extraction
date: 2026-06-11
status: PASS_PENDING_REVIEW
authority: Evidence record only; reviewers decide RC-2 status.
---

# RC-2 Pre-Review Verification

## Commands

```powershell
python -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset tests.unit.test_schema_validation tests.unit.test_target_library_status
cmd /c make smoke-leangeo-fixture
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make smoke-geometry-extraction > docs\ai\changes\geometry-lean-v0_3\evidence\geometry_extraction_smoke.json
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

## Results

- Focused RC-2 unit set: `Ran 17 tests ... OK`.
- LeanGeo fixture: `PASS: LeanGeo.Abbre fixture elaborated with lake env lean`; warning only for unknown upstream `supportInterpreter` package field.
- Full unit suite: `Ran 41 tests ... OK`.
- Mutation target: `Ran 11 tests ... OK`.
- Geometry extraction smoke: passed and regenerated `geometry_extraction_smoke.json`.
- Lean root build: `Build completed successfully`; warnings only from transitive package metadata/local dependency cache state.
- Lean no-sorry check: passed.
- Domain contamination check: passed.

## Claim Ceiling

This supports RC-2 re-review only. It does not claim full LeanGeo theorem-corpus build, solver/compiler integration, RC-2 PASS, or v0.3 completion.
