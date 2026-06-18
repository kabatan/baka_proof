---
title: "Active Context Seed — GeometryFull2D v0.4.4 Reviewed"
base_spec: "MARP-GEOLEAN-BASE-009"
revision: "reviewed-2026-06-18"
---

claim_target: "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY"

# Active Context Seed — GeometryFull2D v0.4.4 Reviewed

The v0.4.3 implementation is not accepted as full pipeline completion. It created useful infrastructure but failed the intended meaning because it used external-looking projection obligations and fixed facade lemma proof generation.

## Current objective

Implement v0.4.4 real solver-causal full pipeline. Do not rewrite the claim. Do not close with projection-corpus results.

## Most important constraints

```text
- Projection-only tasks do not count.
- User-reviewed tasks are optional; do not block solely on their absence.
- Source theorem must be sorry-only before pipeline.
- External source goal must be preserved.
- Solver artifacts must be necessary, not merely referenced.
- Compiler must not read benchmark labels for proof decisions.
- Engine output must be semantic artifact, not proof text.
- B8 is conditional on model provider use.
```

## Stop policy

Stop only for HardBlockers. For ReleaseBlockers, log debt and continue unblocked work.
