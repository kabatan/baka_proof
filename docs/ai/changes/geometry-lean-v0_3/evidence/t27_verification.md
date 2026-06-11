---
title: T27 Verification
task: T27 — Release acceptance and closure
date: 2026-06-11
status: passed
authority: Implementation evidence; does not mark R-IDs VERIFIED or claim completion.
---

# T27 Verification

Supports R-IDs: all release-scope MUST R-IDs and `R-V03-*` R-IDs, especially `R-GUARD-002`, `R-CLAIM-001`, `R-V03-TEST-001`, and `R-V03-EXT-001`.

## Implemented Scope

- Added `scripts/check_release_acceptance.py`.
- Added `docs/ai/changes/geometry-lean-v0_3/CLOSURE.md`.
- Added `docs/ai/changes/geometry-lean-v0_3/evidence/INDEX.md`.
- Added `fmt`, `lint`, `typecheck`, and aggregate `test` targets to `Makefile` and `make.bat`.
- Generated `docs/ai/changes/geometry-lean-v0_3/evidence/release_acceptance_report.json`.

## Verification Commands

```text
cmd /c make fmt
```

Result: passed.

```text
cmd /c make lint
```

Result: passed; domain contamination and no-loose-options checks passed.

```text
cmd /c make typecheck
```

Result: passed, 5 schema validation tests.

```text
cmd /c make test
```

Result: passed:

- 84 unit tests;
- 69 regression tests plus domain/no-loose checks;
- 45 mutation tests;
- 12 integration tests.

```text
cmd /c make lean-build
```

Result: passed. Warnings remain for local changes under `.lake/packages/UnicodeBasic` and `.lake/packages/batteries`.

```text
cmd /c make lean-no-sorry
```

Result: passed.

```text
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_smoke.yaml
```

Result: passed after spec-verifier blocker remediation. The generated release acceptance report records:

- `status = passed`;
- all required review evidence files present through RC-5;
- release blocker and final checklist accounting present;
- real Newclid/GenesisGeo/TongGeometry integrations explicitly marked blocked with dependency evidence;
- domain contamination, no-loose-options, and schema validation checks passed;
- required release gate commands recorded;
- T27 gate commands rerun inside release acceptance: `make test`, `make test-regression`, `make test-mutation`, `make lean-build`, and `make lean-no-sorry`;
- Level 2 matrix check passed with six baselines;
- claim ceiling `fixture_level_release_acceptance_not_v0_3_completion_claim`.

## Claim Ceiling

- T27 supports fixture-level release acceptance only.
- T27 does not claim `SOURCE_FAITHFUL`, `ACCEPTANCE_COMPLETE`, `PRODUCTION_SAFE`, v0.3 completion, real Level 2 advantage, arbitrary LeanGeo theorem support, or any R-ID as VERIFIED.
- Final strong claims require required Guardian/spec/quality reviews.
