---
title: "Source Map Patch — v0.3B solver-backed proof repair"
status: "USER_APPROVED_TRACEABILITY_PATCH"
created: "2026-06-14"
installed: "2026-06-14"
authority: "Non-authoritative traceability aid; Base Spec and Base Spec patches define correctness authority."
---

# Source Map Patch — v0.3B solver-backed proof repair

## Authoritative sources

The approved authority after user approval must be:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md
```

## Source observations that motivated v0.3B

```text
OBS-001:
  v0.3A closure correctly says core experiment-ready passed but TongGeometry model-backed heavy search is blocked.

OBS-002:
  v0.3A final command log states that provider-backed geometry tasks are not counted as final theorem/proof repair success.

OBS-003:
  StandardGeometryProofLoop release path uses provider artifacts but sets provider-backed geometry tasks to blocked rather than final_theorem.

OBS-004:
  The release corpus and matrix now exist and are artifact-derived, but they do not yet establish solver-backed proof repair success.

OBS-005:
  TongGeometry model checkpoints are externally unavailable; this is not the target of v0.3B.
```

## Requirement mapping

```text
OBS-002, OBS-003 -> R-LOOP-B001, R-LOOP-B002
OBS-004 -> R-EVAL-B001, R-EVAL-B010, R-EVAL-B011
OBS-005 -> R-CLAIM-010, explicit non-goals
```
