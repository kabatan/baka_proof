---
title: T-009 Real-vs-Fixture Integration Tests Verification
date: 2026-06-12
task: T-009 — Add real-vs-fixture integration tests
status: passed
authority: Task evidence only; does not mark R-IDs VERIFIED or establish v0.3A completion.
---

# T-009 Real-vs-Fixture Integration Tests Verification

Supports: all v0.3A R-IDs as regression coverage only.

## Implemented Scope

Added `tests/unit/test_v03a_real_vs_fixture_integration.py` covering:

- dependency evidence for Newclid, GenesisGeo, and TongGeometry paths;
- provider manifest fixture/real flags;
- real Newclid output normalization and proof-use blocking;
- mixed fixture/real top-level manifest rejection for whole-provider real claims;
- ResourceGovernor process report fields for external provider paths;
- corpus check evidence;
- corpus final-verification evidence recorded by `scripts/check_real_smoke_corpus.py`;
- claim ceiling text for no broad/full claims.

Updated `Makefile` so `test-regression` explicitly includes the T-009 integration test.

## Verification Commands

```text
python -m unittest tests.unit.test_v03a_real_vs_fixture_integration
```

Result: passed.

```text
Ran 5 tests in 0.002s
OK
```

```text
cmd /c make test
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 106 tests in 55.357s
Ran 79 tests in 21.897s
Ran 45 tests in 2.809s
Ran 18 tests in 15.898s
OK
```

## Claim Ceiling

T-009 adds regression coverage for evidence separation only.

T-009 does not establish v0.3A completion, R-ID VERIFIED status, broad theorem support, model-backed GenesisGeo/TongGeometry behavior, or real Level 2 advantage.
