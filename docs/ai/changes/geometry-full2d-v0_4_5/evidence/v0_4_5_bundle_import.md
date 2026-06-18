---
title: "Evidence — v0.4.5 Reviewed No-Shortcuts Guardian Bundle Import"
status: "EVIDENCE"
created: "2026-06-18"
base_spec: "MARP-GEOLEAN-BASE-010"
plan: "MARP-GEOLEAN-PLAN-010"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-010"
---

# Evidence — v0.4.5 Reviewed No-Shortcuts Guardian Bundle Import

## Source

The user supplied the research-agent bundle:

```text
C:/Users/bakat/.codex/codex-remote-attachments/019eb4d0-2577-77d1-b921-799c63e3c5bd/F7F94352-D234-4279-B09A-CF1D28A17622/1-guardian_geometry_lean_v0_4_5_reviewed_no_shortcuts_bundle.zip
```

Bundle SHA-256:

```text
58C9A559A5C554AFAB5A92817586CF8EA100504CB7DD379EE4A7D86D7158C593
```

It was extracted to:

```text
.tmp/v0_4_5_bundle_import/v0_4_5_real_solver_causal_no_shortcuts_reviewed
```

## Hash Verification

The bundle manifest `geometry_lean_guardian_v0_4_5_sha256sums.txt` was checked against the extracted files before installation. All listed files matched their expected SHA-256 values.

The original manifest is retained at:

```text
docs/ai/changes/geometry-full2d-v0_4_5/evidence/bundle_sha256sums.txt
```

The bundle's self-consistency checker also passed:

```bash
python .tmp/v0_4_5_bundle_import/v0_4_5_real_solver_causal_no_shortcuts_reviewed/geometry_lean_guardian_v0_4_5_consistency_check.py .tmp/v0_4_5_bundle_import/v0_4_5_real_solver_causal_no_shortcuts_reviewed
```

## Installed Mapping

```text
geometry_lean_guardian_BASE_SPEC_v0_4_5_real_solver_causal_full_pipeline.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/BASE_SPEC.md

geometry_lean_guardian_PLAN_v0_4_5_real_solver_causal_full_pipeline.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/PLAN.md

geometry_lean_guardian_ACCEPTANCE_v0_4_5_real_solver_causal_full_pipeline.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/ACCEPTANCE.md

geometry_lean_guardian_REAL_PIPELINE_INVARIANTS_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/REAL_PIPELINE_INVARIANTS.md

geometry_lean_guardian_REFACTOR_DIRECTIVE_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/REFACTOR_DIRECTIVE.md

geometry_lean_guardian_SOURCE_MAP_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/SOURCE_MAP.md

geometry_lean_guardian_ACTIVE_CONTEXT_seed_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/ACTIVE_CONTEXT.md

geometry_lean_guardian_CODEX_HANDOFF_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/CODEX_HANDOFF.md

geometry_lean_guardian_SELF_REVIEW_LOG_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/SELF_REVIEW_LOG.md

geometry_lean_guardian_FAILURE_ANALYSIS_v0_4_5.md
  -> docs/ai/changes/geometry-full2d-v0_4_5/FAILURE_ANALYSIS.md
```

The root navigation files were updated:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/INDEX.md
```

The active-authority checker was added and the generic wrapper now points to it:

```text
scripts/check_active_guardian_spec_v0_4_5.py
scripts/check_active_guardian_spec.py
```

## Status Changes

The imported v0.4.5 authority files were installed as `USER_APPROVED_ACTIVE` under the current user request.

The v0.4.4 authority files were marked:

```text
SUPERSEDED_BY_MARP-GEOLEAN-BASE-010
SUPERSEDED_BY_MARP-GEOLEAN-PLAN-010
SUPERSEDED_BY_MARP-GEOLEAN-ACCEPTANCE-010
```

The v0.4.4 files remain in place as historical evidence, negative evidence, and regression sources. They are not active v0.4.5 release authority and cannot support the v0.4.5 completion claim.

## Claim Ceiling

Allowed after this import:

```text
MARP-GEOLEAN-BASE-010 / PLAN-010 / ACCEPTANCE-010 are installed as the active v0.4.5 Guardian authority set.
Implementation can resume from WP-00/WP-01 under the v0.4.5 plan.
```

Not allowed after this import:

```text
V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```

No implementation work beyond Guardian authority installation is claimed by this evidence file.
