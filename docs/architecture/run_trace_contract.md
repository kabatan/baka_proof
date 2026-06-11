---
title: RunTraceContract — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for v0.3 run trace, attribution, replay, and evaluation records.
authority: Derived documentation; Base Spec R-V03-RUN-001 and R-V03-EVAL-001 are authoritative.
---

# RunTraceContract — geometry × Lean v0.3

This document tracks the run trace architecture required by `R-V03-RUN-001` and `R-V03-EVAL-001`.

Required records:

- `RunRecord`
- `SelectedImplementations`
- `ProviderRunManifest`
- `ControllerStrategyLog`
- `ResearchContributionRecord`
- `EvaluationFunnel`
- `ReproducibilityReport`

No `mode A/B/C/D` field is allowed. Baselines are evaluation configurations, not runtime architecture modes.
