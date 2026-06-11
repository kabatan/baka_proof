---
title: RC-2 Blocked Waiver
task: RC-2 — target subset and extraction
date: 2026-06-11
status: SUPERSEDED_BY_RC2_ENVIRONMENT_UNBLOCK
authority: Evidence-bound waiver; does not override Base Spec or Plan.
---

# RC-2 Blocked Waiver

This historical waiver recorded the RC-2 blocker before the user authorized environment changes. It is superseded by:

- `rc2_environment_unblock.md`
- `rc2_pre_review_verification.md`
- `wsl_leangeo_check_output.log`
- `leangeo_extraction_smoke.json`

Do not use this waiver as current RC-2 status.

## Blocking Condition

The Plan requires RC-2 to verify semantic extraction from Lean goal/context. The current environment cannot elaborate LeanGeo goals because:

- LeanGeo upstream pins `leanprover/lean4:v4.15.0`;
- local Lean is 4.30.0;
- `elan` is not installed, so local toolchain switching is unavailable;
- LeanGeo also requires external solver tooling (`smt-portfolio`, `z3`, `cvc5`) for its check script.

## Completed Non-Blocked Work

- Grammar/schema/fixture scaffold is aligned to v0.3 field names.
- Extractor uses LeanGeo-style theorem/proposition syntax and upstream-observed names.
- Extractor tests cover every accepted grammar form.
- Raw DSL and missing goal anchor are safe-rejected.
- Extraction outputs `extracted_claim` with `proof_use_status = not_allowed`, never `lean_patch_candidate`.
- `sufficient` relation requires goal-anchor relation evidence with matching direction.

## Verification

```powershell
python -m unittest tests.unit.test_target_subset tests.unit.test_geometry_extraction tests.unit.test_schema_validation
cmd /c make smoke-geometry-extraction
cmd /c make lean-build
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

All commands passed locally after remediation.

## Required Unblock

At the time this waiver was written, one of the following was required before RC-2 PASS could be claimed:

- install/pin a LeanGeo-compatible Lean 4.15 toolchain and solver dependencies, then implement real Lean elaboration-backed extraction; or
- obtain an admitted Base/Plan revision that explicitly lowers RC-2 from semantic extraction to scaffold-only.

The first path was later implemented for RC-2 subset evidence using Elan Lean 4.15, WSL Lean 4.15, and LeanGeo.Abbre `#check` output extraction. RC-2 still requires Guardian review before PASS may be claimed.
