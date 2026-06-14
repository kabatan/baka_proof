---
title: v0.4.2 import-stage repo audit
status: INITIAL_AUDIT_FOR_WP00
created: 2026-06-15
purpose: Record the repository state observed while installing the v0.4.2 Guardian authority documents.
authority: Evidence only; does not satisfy implementation acceptance or release acceptance.
---

# v0.4.2 Import-Stage Repo Audit

## Git State Before Import

Observed before installing the v0.4.2 documents:

```text
?? lib/
```

`lib/` was already untracked and unrelated to this import. It was not modified.

## Bundle State

The v0.4.2 bundle was present at:

```text
C:/Users/bakat/Downloads/guardian_geometry_lean_v0_4_2_governed_full2d_bundle.zip
```

Bundle SHA-256:

```text
CC771F50B6A32A14E2D2DF87DB6B6C7223980D09250F74212014EBEBA7A6B727
```

The bundle-provided per-file hashes passed verification.

## Existing Geometry Tracks

Existing v0.3-family Guardian tracks remain in the repository as historical evidence:

```text
docs/ai/changes/geometry-lean-v0_3/
docs/ai/changes/geometry-lean-v0_3a/
docs/ai/changes/geometry-lean-v0_3-full-rebase/
docs/ai/changes/geometry-lean_v0_3/
docs/ai/specs/MARP-GEOLEAN-BASE-003A.md
docs/ai/plans/MARP-GEOLEAN-PLAN-003A.md
```

The v0.4.2 Refactor Directive requires older active geometry authority to be archived. During import, those files were not physically moved because existing repository code still references older evidence paths, including:

```text
src/math_auto_research/workflow/release_acceptance.py
scripts/check_dependency_report_model_status.py
scripts/check_dependency_claim_profile.py
scripts/check_old_specs_removed.py
scripts/check_release_acceptance.py
scripts/check_v03a_release_acceptance.py
scripts/probe_dependencies.py
scripts/smoke_real_tonggeometry.py
scripts/smoke_leangeo_extraction.py
tests/unit/test_geometry_extraction.py
```

Physical archival and reference repair are therefore WP-00 implementation work, not a safe pre-implementation file move.

## Installed v0.4.2 Track

Installed active track:

```text
docs/ai/changes/geometry-full2d-v0_4_2/
```

The root navigation files now point to v0.4.2:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/INDEX.md
```

## Immediate WP-00 Work Remaining

```text
1. implement/run scripts/check_active_guardian_spec.py;
2. archive old active geometry authority only after updating stale path references;
3. create the v0.4.2 release-path status evidence files from real checks, not placeholders;
4. keep claim ceiling at implementation-in-progress until release acceptance passes.
```
