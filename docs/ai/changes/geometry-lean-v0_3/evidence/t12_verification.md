---
title: T12 Verification Evidence
task: T12 — LeanGeoSubsetV1 theorem grammar
date: 2026-06-11
status: PASS
authority: Evidence record only; does not override Base Spec or Plan.
---

# T12 Verification Evidence

## Scope

Implemented the LeanGeoSubsetV1 grammar scaffold:

- grammar schema and manifest;
- predicate, construction, and relation mappings;
- positive, negative, ambiguous, safe-reject, and mutation fixtures;
- target subset validator;
- relation-to-goal checks that block `related` and `none` from goal-level proof-use.

## Commands

```powershell
python -m unittest tests.unit.test_target_subset
python -m math_auto_research.cli.validate_artifact plugins/geometry_synthetic/grammar/leangeo_subset_v1_grammar.json
python -m math_auto_research.cli.validate_artifact plugins/geometry_synthetic/grammar/fixtures.json
cmd /c make lean-build
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

Results:

```text
target subset tests: Ran 2 tests OK
grammar schema: ok
fixture schema: ok
Build completed successfully (0 jobs).
Ran 32 tests in 1.537s
OK
domain contamination check passed
```

## Claim Ceiling

This is grammar/schema/fixture scaffold. It does not claim semantic Lean extraction, real LeanGeo dependency availability, geometry solving, or final theorem support.
