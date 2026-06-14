<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: USER_APPROVED_ACTIVE
-->
---
title: "Refactor Directive — GeometryFull2D v0.4.2"
directive_id: "MARP-GEOLEAN-REFACTOR-007"
status: "USER_APPROVED_ACTIVE"
created: "2026-06-14"
---

# Refactor Directive — GeometryFull2D v0.4.2

## 0. Goal

Refactor `kabatan/baka_proof` from the v0.3B solver-backed proof-repair implementation into the v0.4.2 full prover architecture without keeping confusing duplicate release paths.

## 1. Remove or archive obsolete authority

Move older active geometry specs to:

```text
docs/ai/archive/geometry_pre_v0_4_2/
```

Do not leave root-level or active change-dir documents that look like current authority.

## 2. Release plugin boundary

Required:

```text
plugins/geometry_full2d/
```

Legacy:

```text
plugins/geometry_synthetic/
```

Rules:

```text
1. geometry_full2d must not import geometry_synthetic.
2. release configs must not reference geometry_synthetic.
3. release acceptance must fail if legacy plugin appears in release path.
4. geometry_synthetic may remain only for historical tests or archive.
```

## 3. Directory target

```text
plugins/geometry_full2d/
  plugin.yaml
  facade/
  extraction/
  claims/
  provider/
  engines/
    synthetic_closure.py
    construction_search.py
    algebraic_geometry.py
    metric_angle.py
    transformation.py
    order_case.py
    inequality.py
    lean_proof_search.py
    portfolio_coordinator.py
  rules/
  side_conditions/
  compilers/
  proof/
  evaluation/
  tests/

lean/MathAutoResearch/GeometryFull2D/
  Basic.lean
  Incidence.lean
  Angle.lean
  Metric.lean
  Circle.lean
  Triangle.lean
  Construction.lean
  Transformation.lean
  Order.lean
  Inequality.lean
  Tactics.lean

schemas/geometry_full2d/
configs/benchmark_runs/geometry_full2d_v0_4_2.yaml
benchmarks/geometry_full2d/
scripts/check_release_acceptance_v0_4_2.py
scripts/check_v0_4_2_progress_acceptance.py
```

## 4. Do not delete safety foundations

Retain and adapt:

```text
LeanPatchCandidate
ProofWorker proof-region guard
FinalVerifyGate
SolverBackedProofCertificate
ResourceGovernor
ArtifactStore
RunLogger
ProofStateDAG
TrustGuard
ModelProviderSet
```

## 5. Delete or quarantine bad patterns

Release path must not contain:

```text
regex-only extraction
toy geometry definitions
fixture provider success
hard-coded theorem names
label-derived final theorem metrics
safe-reject-as-success for positive tasks
unverified raw solver proof-use
```
