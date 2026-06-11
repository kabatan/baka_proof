---
title: T13 Verification Evidence
task: T13 — GeometryExtractionContract
date: 2026-06-11
status: PASS_PENDING_RC2_REVIEW_AFTER_FIXES
authority: Evidence record only; does not override Base Spec or Plan.
---

# T13 Verification Evidence

## Scope

Implemented GeometryExtractionContract scaffold and RC-2 remediation:

- `GeometryExtractionReport` schema;
- `GeometryClaimSpec` schema;
- safe-rejecting `GeometryExtractor`;
- relation classifier scaffold: `exact`, direction-checked `sufficient`, safe-rejected `related`, and `none`;
- raw DSL path guard: missing `goal_anchor_ref` safe-rejects and cannot create a claim spec;
- accepted extraction emits `result_level = extracted_claim` and `proof_use_status = not_allowed`; it does not emit `lean_patch_candidate`;
- smoke command and evidence file.

## Commands

```powershell
python -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset tests.unit.test_schema_validation
cmd /c make smoke-geometry-extraction > docs\ai\changes\geometry-lean-v0_3\evidence\geometry_extraction_smoke.json
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

Results:

```text
target/extraction/schema tests: Ran 12 tests OK
smoke-geometry-extraction: PASS
Ran 37 tests in 1.626s
OK
domain contamination check passed
```

## Claim Ceiling

This is extraction-contract scaffold with safe-reject behavior and direction-aware relation gating. Full semantic Lean expression canonicalization remains blocked by unresolved real LeanGeo dependency; this task does not claim solver integration or final theorem support.
