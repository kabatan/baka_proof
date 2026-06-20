# GeometryFull2D v0.6 Guardian Authority

Status: active user-approved execution-locked correction track.

This directory contains the active Guardian authority set for the v0.6 reviewed-strict GeometryFull2D real solver-causal full pipeline recovery.

Authority identifiers:

```text
MARP-GEOLEAN-BASE-012
MARP-GEOLEAN-PLAN-012
MARP-GEOLEAN-ACCEPTANCE-012
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```

Read first:

- `BASE_SPEC.md`
- `PLAN.md`
- `ACCEPTANCE.md`
- `RED_CASE_SUITE.md`
- `REAL_PIPELINE_INVARIANTS.md`
- `REFACTOR_DIRECTIVE.md`
- `CODEX_HANDOFF.md`
- `FAILURE_ANALYSIS.md`
- `SOURCE_MAP.md`

The v0.5 and v0.4.x tracks are superseded and retained only as historical evidence, regression sources, and failure-analysis context. They are not active v0.6 release authority.

Review evidence:

- `evidence/v0_6_bundle_import.md`
- `evidence/v0_6_post_admission_review_loop.md`
- `evidence/WP14_ZERO_B2_SUCCESS_BLOCKER_REPORT.md`
- `evidence/bundle_sha256sums.txt`
- `evidence/bundle_original_sha256sums.txt`
- `evidence/bundle_actual_sha256sums.txt`
- `evidence/bundle_consistency_result.json`
- `evidence/bundle_consistency_check.py`

First checks:

```bash
python scripts/check_active_guardian_spec_v0_6.py
python scripts/check_v0_6_spec_plan_consistency.py
```

No implementation completion is claimed by this authority import.
