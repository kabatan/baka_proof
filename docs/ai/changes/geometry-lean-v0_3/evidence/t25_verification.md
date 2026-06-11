---
title: T25 Verification
task: T25 — Regression and mutation suite
date: 2026-06-11
status: passed
authority: Implementation evidence; does not mark R-IDs VERIFIED.
---

# T25 Verification

Supports R-IDs: `R-TEST-001`, `R-V03-TEST-001`, and safety R-IDs covered by the regression families.

## Implemented Scope

- Expanded `make test-regression` and `make.bat test-regression` to run the required safety families:
  domain contamination, schema/public contract checks, dependency/target substitution checks, resource governor/provider timeout checks, extraction, RuleRegistry/TraceCompiler, ConstructionCompiler, trust/final verification, model/provider non-proof-use, standard loop, and run trace/replay.
- Expanded `make test-mutation` and `make.bat test-mutation` to include extraction/target mutations, TraceCompiler/RuleRegistry side-condition mutations, ConstructionCompiler mutations, TrustGuard/BridgeGate laundering checks, and FinalVerifyGate misuse checks.

## Verification Commands

```text
cmd /c make test-regression
```

Result: passed; domain contamination and no-loose-options checks passed; 62 regression tests passed.

```text
cmd /c make test-mutation
```

Result: passed, 34 tests.

```text
cmd /c make test-unit
```

Result: passed, 80 tests.

```text
cmd /c make lean-build
```

Result: passed. Warnings remain for local changes under `.lake/packages/UnicodeBasic` and `.lake/packages/batteries`.

```text
cmd /c make lean-no-sorry
```

Result: passed.

## Claim Ceiling

- T25 confirms the configured regression and mutation targets run the required fixture-level safety families.
- T25 does not claim exhaustive mutation testing or v0.3 completion.
- No R-ID is marked VERIFIED.
