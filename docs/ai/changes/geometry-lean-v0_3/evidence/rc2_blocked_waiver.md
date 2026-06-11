---
title: RC-2 Blocked Waiver
task: RC-2 — target subset and extraction
date: 2026-06-11
status: BLOCKED
authority: Evidence-bound waiver; does not override Base Spec or Plan.
---

# RC-2 Blocked Waiver

RC-2 cannot be claimed PASS under the current admitted Base Spec and Plan.

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

One of the following is required before RC-2 PASS can be claimed:

- install/pin a LeanGeo-compatible Lean 4.15 toolchain and solver dependencies, then implement real Lean elaboration-backed extraction; or
- obtain an admitted Base/Plan revision that explicitly lowers RC-2 from semantic extraction to scaffold-only.
