---
title: "Real Pipeline Invariants — GeometryFull2D v0.4.5"
spec_id: "MARP-GEOLEAN-INVARIANTS-010"
base_spec: "MARP-GEOLEAN-BASE-010"
---

# Real Pipeline Invariants — v0.4.5

These invariants are release-critical.

## I-010-001 — Solver-before-proof

No proof text may be generated before provider/engine artifacts and `SelectedSolverDerivationV1` exist.

## I-010-002 — Solver fact dependency

A counted proof patch must depend on at least one solver fact, construction, or certificate. Compiler output without consumed solver artifacts is not counted.

## I-010-003 — Destructive rerun causality

Every counted B2 success must pass destructive reruns. Boolean-only causality reports are invalid.

## I-010-004 — No target-shape proof menus

Release code must not contain target-shape-to-proof menus such as `_proof_from_shape`, target-prefix dispatch, or theorem-family proof selection.

## I-010-005 — No family-coded baselines

Baseline outcomes must arise from disabled artifacts in the actual pipeline, not from theorem-family labels.

## I-010-006 — Non-projection corpus

External sources may not be counted by projecting them to easier obligations. Sealed challenges must be independent of provider/compiler/rule-registry/proof-worker code.

## I-010-007 — Hash-bound evidence

All counted artifacts must be content-addressed and bound to corpus hash, config hash, selected implementation hash, and repository tree hash.

## I-010-008 — Full target maintained

The release target remains GeometryFull2DTarget:1.0.0. The pipeline may report measured failures during development, but final closure requires the specified thresholds.
