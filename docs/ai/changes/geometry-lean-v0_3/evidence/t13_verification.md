---
title: T13 Verification Evidence
task: T13 — GeometryExtractionContract
date: 2026-06-11
status: SUPERSEDED_BY_RC2_LEAN_OUTPUT_EVIDENCE
authority: Evidence record only; does not override Base Spec or Plan.
---

# T13 Verification Evidence

## Scope

Implemented GeometryExtractionContract scaffold and RC-2 remediation. This evidence record has been superseded for RC-2 semantic extraction by:

- `rc2_environment_unblock.md`
- `rc2_pre_review_verification.md`
- `wsl_leangeo_check_output.log`
- `leangeo_extraction_smoke.json`

Retained historical scope:

- `GeometryExtractionReport` schema;
- `GeometryClaimSpec` schema;
- safe-rejecting `GeometryExtractor`;
- relation classifier scaffold: `exact`, direction-checked `sufficient`, safe-rejected `related`, and `none`;
- raw DSL path guard: missing `goal_anchor_ref` safe-rejects and cannot create a claim spec;
- accepted extraction emits `result_level = extracted_claim` and `proof_use_status = not_allowed`; it does not emit `lean_patch_candidate`;
- extractor tests cover every accepted grammar form with LeanGeo-style theorem/proposition syntax;
- initial smoke command and evidence file, later replaced by the Lean-backed `make smoke-geometry-extraction` target.

## Historical Commands

```powershell
python -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset tests.unit.test_schema_validation
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

The original manual-context smoke output was removed and must not be used as RC-2 semantic extraction evidence.

Current RC-2 semantic extraction command:

```powershell
cmd /c make smoke-geometry-extraction
```

Current evidence files:

- `wsl_leangeo_check_output.log`
- `leangeo_extraction_smoke.json`

Results:

```text
target/extraction/schema tests: Ran 13 tests OK
smoke-geometry-extraction: PASS, superseded by Lean-backed `leangeo_extraction_smoke.json`
Ran 38 tests in 1.635s
OK
domain contamination check passed
```

## Claim Ceiling

This historical record does not support current RC-2 PASS by itself. Current RC-2 support is the Lean-backed smoke output in `leangeo_extraction_smoke.json` plus `wsl_leangeo_check_output.log`. This task does not claim solver integration, full LeanGeo theorem-corpus build, or final theorem support.
