---
title: "Evidence — v0.4.3 Integrated Guardian Bundle Import"
status: "EVIDENCE"
created: "2026-06-15"
base_spec: "MARP-GEOLEAN-BASE-008"
plan: "MARP-GEOLEAN-PLAN-008"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-008"
---

# Evidence — v0.4.3 Integrated Guardian Bundle Import

## Source

The user supplied the research-agent bundle:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_4_3_integrated_bundle.zip
```

It was extracted to:

```text
C:/Users/bakat/AppData/Local/Temp/guardian_geometry_lean_v0_4_3_integrated_bundle/v0_4_3_integrated
```

## Hash Verification

The bundle manifest `geometry_lean_guardian_v0_4_3_integrated_sha256sums.txt` was verified before installation. All listed files matched their expected SHA-256 values.

The original manifest is retained at:

```text
docs/ai/changes/geometry-full2d-v0_4_3/evidence/bundle_sha256sums.txt
```

## Installed Mapping

```text
README_v0_4_3_integrated.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/README.md

geometry_lean_guardian_BASE_SPEC_v0_4_3_real_full2d_recovery.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/BASE_SPEC.md

geometry_lean_guardian_PLAN_v0_4_3_real_full2d_recovery.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/PLAN.md

geometry_lean_guardian_ACCEPTANCE_v0_4_3_real_full2d_recovery.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/ACCEPTANCE.md

geometry_lean_guardian_REAL_PIPELINE_INVARIANTS_v0_4_3.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/REAL_PIPELINE_INVARIANTS.md

geometry_lean_guardian_REFACTOR_DIRECTIVE_v0_4_3.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/REFACTOR_DIRECTIVE.md

geometry_lean_guardian_SOURCE_MAP_v0_4_3.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/SOURCE_MAP.md

geometry_lean_guardian_ACTIVE_CONTEXT_seed_v0_4_3.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/ACTIVE_CONTEXT.md

geometry_lean_guardian_CODEX_HANDOFF_v0_4_3.md
  -> docs/ai/changes/geometry-full2d-v0_4_3/CODEX_HANDOFF.md
```

The root navigation files were updated:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/INDEX.md
```

The active-authority checker was added:

```text
scripts/check_active_guardian_spec_v0_4_3.py
```

## Status Changes

The imported v0.4.3 authority files were installed as `USER_APPROVED_ACTIVE` under the current user request.

The v0.4.2 authority files were marked:

```text
SUPERSEDED_BY_MARP-GEOLEAN-BASE-008
```

The v0.4.2 files remain in place as historical evidence, negative evidence, and regression sources. They are not active v0.4.3 release authority and cannot support the v0.4.3 completion claim.

## Claim Ceiling

Allowed after this import:

```text
MARP-GEOLEAN-BASE-008 / PLAN-008 / ACCEPTANCE-008 are installed as the active v0.4.3 Guardian authority set.
Implementation can resume from WP-00 under the v0.4.3 plan.
```

Not allowed after this import:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
ACCEPTANCE_COMPLETE
SOURCE_FAITHFUL
PRODUCTION_SAFE
```

No implementation work beyond Guardian authority installation is claimed by this evidence file.
