---
title: "Real Pipeline Invariants — GeometryFull2D v0.6 Reviewed Strict"
base_spec: "MARP-GEOLEAN-BASE-012"
status: "USER_APPROVED_ACTIVE"
---

# Real Pipeline Invariants v0.6

1. Solver artifacts are generated before compiler artifacts and cannot import downstream proof-generation code.
2. SelectedSolverDerivationV3 must contain at least one checked non-target intermediate, construction, certificate, or case split for every counted B2 success.
3. Compiler proof text is derived only from selected derivation steps and rule contracts, not target shape or corpus metadata.
4. FinalVerifyGate alone authorizes final theorem status.
5. SolverCausalityLiveRunV1 requires live destructive reruns with command logs and fresh temp dirs.
6. Matrix requires all counted tasks across B1/B2/B5/B6/B7 and conditional B8, not B2-only records.
7. Metrics are computed only from ActualTaskPipelineRunV4 and SolverCausalityLiveRunV1 records.
8. Checkers may not fabricate provider/engine/compiler/final artifacts.
9. Red-case failure classes are release blockers even if implemented under different names.
10. Closure is generated only by release acceptance and cannot be manually granted.


## Authority identifiers

```text
MARP-GEOLEAN-BASE-012
MARP-GEOLEAN-PLAN-012
MARP-GEOLEAN-ACCEPTANCE-012
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```
