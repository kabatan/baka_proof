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
5. Grammar manifest field names are aligned with the v0.3 contract index (`allowed_hypothesis_forms`, `rejected_hypothesis_forms`, `allowed_target_forms`, `rejected_target_forms`).
6. Extraction tests now cover every accepted grammar form with LeanGeo-style theorem/proposition syntax, using declarations observed in LeanGeo/SystemE source such as `Point`, `Line`, `Circle`, `Coll`, `Cyclic`, `MidPoint`, `PerpLine`, `Foot`, `line_from_points`, `circle_from_points`, and `intersection_lines`.
7. Relation classification no longer depends on synthetic markers embedded in the theorem text; it requires `RelationEvidence(source = goal_anchor)`.
8. Plan verification commands now include `make lean-build` and `make test-mutation TEST_FILTER=extraction`.

## Explicit Blocker

Full Lean elaboration against real LeanGeo namespaces remains blocked by T11 dependency status: local Lean is 4.30.0 while LeanGeo pins `leanprover/lean4:v4.15.0` and requires solver tools. No alternate target library was introduced.

## Verification

```powershell
python -m unittest tests.unit.test_target_subset tests.unit.test_geometry_extraction tests.unit.test_schema_validation
cmd /c make smoke-geometry-extraction > docs\ai\changes\geometry-lean-v0_3\evidence\geometry_extraction_smoke.json
cmd /c make lean-build
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make test-unit
python scripts/check_domain_contamination.py
```

Results:

```text
Ran 13 tests in 0.019s
OK
Build completed successfully (0 jobs).
Ran 8 tests in 0.007s
OK
Ran 38 tests in 1.635s
OK
domain contamination check passed
```

## Claim Ceiling

Do not claim full semantic extraction, real LeanGeo integration, solver/compiler integration, RC-2 PASS, or final theorem support. Current state is RC-2 blocked on real LeanGeo elaboration/toolchain setup.
