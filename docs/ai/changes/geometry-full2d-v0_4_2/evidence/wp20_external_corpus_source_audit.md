---
title: WP-20 External Corpus Source Audit
status: release_blocked
date: 2026-06-15
claim_ceiling: implementation_in_progress_no_v0_4_2_completion_claim
---

# WP-20 External Corpus Source Audit

Purpose: record why the current workspace cannot honestly close H-003/H-004 by relabeling the synthetic draft corpus.

Checked sources:

- LeanEuclid: `https://github.com/loganrjmurphy/LeanEuclid`
  - Repository README describes 173 Euclidean geometry problems manually formalized into Lean.
  - The formal system is LeanEuclid/System E, not `GeometryFull2DTarget:1.0.0`.
  - Useful as an external source candidate, but insufficient alone for the H-003 floor of 900 external/human-curated positives.
- LeanGeo paper/index: `https://huggingface.co/papers/2508.14644`
  - Describes LeanGeo-Bench as a Lean geometry benchmark.
  - Search snippet reports 122 benchmark problems.
  - Useful as an external source candidate, but insufficient alone for the H-003 floor and requires target-language adaptation before release admission.
- TongGeometry repository: `https://github.com/bigai-ai/tong-geometry`
  - Python geometry project, not a ready Lean `GeometryFull2DTarget:1.0.0` formal corpus.
  - Not release-critical under the active v0.4.2 context.

Current conclusion:

```text
Do not count the existing generated draft tasks as external_formal or human_curated_formal.
Do not set corpus status to release_frozen until the curated/external floor and synthetic share checks pass.
```

Remaining WP-20 work:

```text
Acquire or create and admit at least 900 genuinely external_formal or human_curated_formal positive tasks in the GeometryFull2D facade.
Keep synthetic_generated positives <=50% of all positive tasks.
Run scripts/import_full2d_curated_corpus.py with source references and Lean checks.
Run scripts/freeze_full2d_corpus.py after manifest checks pass.
Run the full matrix and metrics acceptance after release freeze.
```
