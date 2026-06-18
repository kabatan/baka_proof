# GeometryFull2D v0.5 Guardian Authority

Status: active user-approved correction track.

This directory contains the active Guardian authority set for the v0.5 reviewed-strict GeometryFull2D real solver-causal full pipeline recovery.

Read first:

- `BASE_SPEC.md`
- `PLAN.md`
- `ACCEPTANCE.md`
- `RED_CASE_SUITE.md`
- `REAL_PIPELINE_INVARIANTS.md`
- `REFACTOR_DIRECTIVE.md`
- `CODEX_HANDOFF.md`
- `FAILURE_ANALYSIS.md`

The v0.4.5 closure is invalidated as a false-positive closure and retained only as negative evidence.

Review evidence:

- `evidence/v0_5_bundle_import.md`
- `evidence/v0_5_post_admission_review_loop.md`
- `evidence/wp01_wp02_redcase_acceptance_harness.md`
- `evidence/wp03_schema_validator_evidence.md`
- `evidence/wp04_corpus_system_evidence.md`

First checks:

```bash
python scripts/check_active_guardian_spec_v0_5.py
python scripts/check_v0_5_spec_plan_consistency.py docs/ai/changes/geometry-full2d-v0_5
```
