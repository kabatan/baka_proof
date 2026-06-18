---
title: "Active Context Seed — GeometryFull2D v0.4.3"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-009"
---

# Active Context Seed — v0.4.3

## Current mission

Recover from the v0.4.2 scaffold/template acceptance failure and implement a real solver-backed Full2D geometry pipeline.

## Active claim target

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
```

## What must not happen again

```text
- Do not pass release using synthetic template corpus only.
- Do not pass release using template_id -> proof text.
- Do not pass release using fabricated solver refs.
- Do not pass release using smoke-only extraction.
- Do not pass release with empty metrics/advantage/engine/rule summaries.
- Do not ignore open debt ledger entries.
```

## Implementation style

```text
Continue on ReleaseBlocker/WorkDebt.
Stop only on HardBlocker.
Do not weaken Base Spec.
Do not lower thresholds.
Do not relabel synthetic as curated.
```

## First tasks for Codex

```text
1. Install v0.4.3 Guardian docs.
2. Quarantine v0.4.2 template release path.
3. Implement ActualTaskPipelineRunV1.
4. Implement per-theorem extraction.
5. Implement real provider/engine evidence coupling.
6. Rebuild matrix to execute/replay actual runs only.
```



## Integrated anti-gaming requirements

This v0.4.3 context already includes the anti-gaming hardening. Codex must not expect or install a separate addendum. The implementation must enforce substantive corpus floors, review manifest gates, engine semantic-output guards, compiler input isolation, baseline comparability, causal-chain hashes, and anti-v0.4.2 regression checks before release.
