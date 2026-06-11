---
title: RC-003A-4 Guardian Boundary Review
date: 2026-06-12
gate: RC-003A-4 corpus and real-vs-fixture tests
status: PASS
reviewer: guardian_boundary_reviewer
authority: Review record only; does not mark R-IDs VERIFIED or expand claim ceiling beyond the stated limited claims.
---

# RC-003A-4 Guardian Boundary Review

## Result

PASS.

The previous blocker is remediated. `scripts/check_real_smoke_corpus.py` directly runs `lake env lean benchmarks/leangeo/RealSmokeCorpus.lean` for the acceptance-eligible corpus entry, and `tests.unit.test_real_smoke_corpus` calls `validate_manifest()`, so `make test-regression` enforces the direct corpus final-verification path.

## Limited Admitted Claims

- `LeanGeoSubsetV1.RealSmokeCorpus` is declared as a limited one-entry smoke corpus with manifest fields for theorem path/name, statement hash, extraction class, supported predicates, coverage, expected final status, and acceptance eligibility.
- The admitted corpus entry `real_smoke:fixture_collinear` has recorded final verification evidence: `observed_final_verification_status = passed`.
- Regression coverage distinguishes fixture and real evidence boundaries, including Newclid non-fixture smoke evidence, mixed fixture/real whole-provider claim blocking, ResourceGovernor process reports, corpus check evidence, and claim-ceiling text.

## Explicit Non-Claims

- No R-IDs are VERIFIED.
- This does not admit v0.3A completion.
- This does not admit arbitrary or broad LeanGeo theorem/corpus support.
- This does not admit model-backed GenesisGeo/TongGeometry claims.
- This does not admit whole-provider real-integration claims from mixed fixture/real runs.
- This does not admit real Level 2 advantage.
- This does not admit SOURCE_FAITHFUL, ACCEPTANCE_COMPLETE, or PRODUCTION_SAFE.
