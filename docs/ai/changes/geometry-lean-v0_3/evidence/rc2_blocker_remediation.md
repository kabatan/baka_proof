---
title: RC-2 Blocker Remediation Evidence
task: RC-2 — target subset and extraction
date: 2026-06-11
status: PASS_PENDING_REVIEW
authority: Evidence record only; does not override Base Spec or Plan.
---

# RC-2 Blocker Remediation Evidence

## Addressed Items

1. Fixture coverage now checks every declared grammar entry across object declarations, hypothesis forms, target forms, and construction mappings.
2. Extraction no longer emits `lean_patch_candidate`; accepted extraction emits `result_level = extracted_claim` and `proof_use_status = not_allowed`.
3. Relation gating now covers:
   - `exact`: accepted;
   - `sufficient`: accepted only when `direction_needed == direction_available`;
   - `related`: safe-rejected for goal-level proof-use;
   - `none`: safe-rejected.
4. Raw DSL / missing goal anchor remains safe-rejected.

## Explicit Blocker

Full semantic Lean expression canonicalization against real LeanGeo namespaces remains blocked by T11 dependency status: local Lean is 4.30.0 while the checked LeanGeo README states Lean 4.15 support/requirement. No alternate target library was introduced.

## Verification

```powershell
python -m unittest tests.unit.test_target_subset tests.unit.test_geometry_extraction tests.unit.test_schema_validation
cmd /c make smoke-geometry-extraction > docs\ai\changes\geometry-lean-v0_3\evidence\geometry_extraction_smoke.json
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

Results:

```text
Ran 12 tests in 0.026s
OK
Ran 37 tests in 1.626s
OK
domain contamination check passed
```

## Claim Ceiling

Do not claim full semantic extraction, real LeanGeo integration, solver/compiler integration, RC-2 PASS, or final theorem support until Guardian review passes.
