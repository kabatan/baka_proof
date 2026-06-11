---
title: T-008 LeanGeoSubsetV1.RealSmokeCorpus Verification
date: 2026-06-12
task: T-008 — Define LeanGeoSubsetV1.RealSmokeCorpus
status: passed
authority: Task evidence only; does not mark R-IDs VERIFIED or establish arbitrary LeanGeo theorem support.
---

# T-008 LeanGeoSubsetV1.RealSmokeCorpus Verification

Supports:

- `R-CORPUS-REAL-001`
- `R-CLAIM-REAL-001`

## Implemented Scope

- Added `benchmarks/leangeo/real_smoke_corpus.yaml`.
- Added `benchmarks/leangeo/RealSmokeCorpus.lean`.
- The corpus manifest records theorem file path, theorem name, statement hash, extraction class, supported predicates, construction/rule coverage, expected final verification status, and acceptance eligibility.
- Added `scripts/check_real_smoke_corpus.py`.
- Added regression tests for:
  - manifest shape and statement hash;
  - extraction from the recorded theorem statement;
  - safe reject for unsupported expression;
  - statement mutation hash mismatch;
  - toy-library substitution rejection.
- Updated `Makefile` so `make lean-build` prefers `%USERPROFILE%/.elan/bin/lake.exe` when available, matching repo `lean-toolchain` instead of the unrelated winget Lean 4.30 executable.

## Verification Commands

```text
python -m py_compile scripts\check_real_smoke_corpus.py
```

Result: passed.

```text
python scripts\check_real_smoke_corpus.py
```

Result: passed.

```text
python -m unittest tests.unit.test_real_smoke_corpus
```

Result: passed.

```text
Ran 5 tests in 0.013s
OK
```

```text
cmd /c make lean-build
```

Result: passed.

```text
Build completed successfully.
```

```text
cmd /c make test-regression
```

Result: passed.

```text
domain contamination check passed
no loose options check passed
Ran 79 tests in 26.173s
OK
```

## Run Artifacts

- `runs/v03a_t008_real_smoke_corpus_latest/corpus_check.json`

## Claim Ceiling

T-008 defines and checks a limited `LeanGeoSubsetV1.RealSmokeCorpus` with one accepted smoke entry and explicit negative checks.

T-008 does not establish arbitrary LeanGeo theorem support, broad corpus support, final proof generation for new theorems, real Level 2 advantage, or v0.3A completion.
