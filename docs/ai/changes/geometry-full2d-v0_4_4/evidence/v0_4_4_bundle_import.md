---
title: "Evidence — v0.4.4 Reviewed Guardian Bundle Import"
status: "EVIDENCE"
created: "2026-06-18"
base_spec: "MARP-GEOLEAN-BASE-009"
plan: "MARP-GEOLEAN-PLAN-009"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-009"
---

# Evidence — v0.4.4 Reviewed Guardian Bundle Import

## Source

The user supplied the research-agent bundle:

```text
C:/Users/bakat/.codex/codex-remote-attachments/019eb4d0-2577-77d1-b921-799c63e3c5bd/B50123FB-6A29-4A24-BEB5-1452FEF3AB3E/1-guardian_geometry_lean_v0_4_4_reviewed_bundle.zip
```

Bundle SHA-256:

```text
8EB35B7FFBEB076DC8887D5848273A0998068285F0CB931C778396020B9F9F7B
```

It was extracted to:

```text
.tmp/v0_4_4_reviewed_bundle_import/v0_4_4_real_full2d_solver_causal_reviewed
```

## Hash Verification

The bundle manifest `geometry_lean_guardian_v0_4_4_reviewed_sha256sums.txt` was checked against the extracted files before installation. All listed files matched their expected SHA-256 values.

The original manifest is retained at:

```text
docs/ai/changes/geometry-full2d-v0_4_4/evidence/bundle_sha256sums.txt
```

The bundle's self-consistency checker also passed:

```bash
python .tmp/v0_4_4_reviewed_bundle_import/v0_4_4_real_full2d_solver_causal_reviewed/geometry_lean_guardian_v0_4_4_consistency_check.py
```

## Installed Mapping

```text
geometry_lean_guardian_BASE_SPEC_v0_4_4_real_full2d_solver_causal.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/BASE_SPEC.md

geometry_lean_guardian_PLAN_v0_4_4_real_full2d_solver_causal.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/PLAN.md

geometry_lean_guardian_ACCEPTANCE_v0_4_4_real_full2d_solver_causal.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/ACCEPTANCE.md

geometry_lean_guardian_REAL_PIPELINE_INVARIANTS_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/REAL_PIPELINE_INVARIANTS.md

geometry_lean_guardian_REFACTOR_DIRECTIVE_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/REFACTOR_DIRECTIVE.md

geometry_lean_guardian_SOURCE_MAP_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/SOURCE_MAP.md

geometry_lean_guardian_ACTIVE_CONTEXT_seed_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/ACTIVE_CONTEXT.md

geometry_lean_guardian_CODEX_HANDOFF_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/CODEX_HANDOFF.md

geometry_lean_guardian_SELF_REVIEW_LOG_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/SELF_REVIEW_LOG.md

geometry_lean_guardian_FAILURE_ANALYSIS_v0_4_4.md
  -> docs/ai/changes/geometry-full2d-v0_4_4/FAILURE_ANALYSIS.md
```

The root navigation files were updated:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/INDEX.md
```

The active-authority checker was added and the generic wrapper was moved to it:

```text
scripts/check_active_guardian_spec_v0_4_4.py
scripts/check_active_guardian_spec.py
```

## Status Changes

The imported v0.4.4 authority files were installed as `USER_APPROVED_ACTIVE` under the current user request.

The v0.4.3 authority files were marked:

```text
SUPERSEDED_BY_MARP-GEOLEAN-BASE-009
```

The v0.4.3 files remain in place as historical evidence, negative evidence, and regression sources. They are not active v0.4.4 release authority and cannot support the v0.4.4 completion claim.

## Claim Ceiling

Allowed after this import:

```text
MARP-GEOLEAN-BASE-009 / PLAN-009 / ACCEPTANCE-009 are installed as the active v0.4.4 Guardian authority set.
Implementation can resume from WP00/WP01 under the v0.4.4 plan.
```

Not allowed after this import:

```text
V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```

No implementation work beyond Guardian authority installation is claimed by this evidence file.
