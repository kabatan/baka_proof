---
title: "GeometryFull2D v0.4.4 Real Pipeline Invariants — Reviewed"
base_spec: "MARP-GEOLEAN-BASE-009"
revision: "reviewed-2026-06-18"
---

claim_target: "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY"

# GeometryFull2D v0.4.4 Real Pipeline Invariants

These invariants are release-critical. A release checker must fail if any invariant is violated.

## I-001 — Source-theorem invariant

Counted positive source theorem files contain theorem statements with only a MARP proof region containing `sorry`. A counted source theorem may not already contain a proof.

## I-002 — Non-projection corpus invariant

External formal tasks count only if the source goal is preserved exactly, structurally through a reviewed translator, or by formal equivalence. Projection obligations are non-counted.

## I-003 — Optional user-review invariant

UserReviewedGoal tasks count only with ReviewManifestV1. Missing user-reviewed tasks do not block release if other corpus floors pass.

## I-004 — Per-theorem extraction invariant

Every counted task has Lean-side, per-theorem structured extraction tied to source statement hash. Smoke extraction is not release evidence.

## I-005 — Solver-causality invariant

Every B2 counted success has SolverCausalityReportV1. Removing or corrupting the selected normalized solver artifact prevents the same counted proof patch from being accepted.

## I-006 — Compiler isolation invariant

Compiler proof decisions are independent of task id, theorem name, theorem family, grammar family, difficulty tier, provenance, source ref, template id, and generator private labels.

## I-007 — Engine semantic-artifact invariant

Engine outputs are semantic artifacts. They contain no Lean proof text, tactic script, or proof-region replacement text.

## I-008 — Shallow proof ceiling invariant

Direct or wrapped facade lemma applications may not exceed the release ceiling and may not be relabeled as solver-intermediate.

## I-009 — Baseline comparability invariant

Baselines differ only by declared disabled solver components. B8 is conditional on model-provider use.

## I-010 — Replay invariant

Replay is allowed only if corpus hash, config hash, selected implementation hash, repo/code hash, and artifact hashes match.

## I-011 — Report integrity invariant

Release report summaries are nonempty and artifact-derived. Empty summary fields, stale reports, or open debt entries block closure.

## I-012 — Old-path alias invariant

Renamed, wrapped, copied, shimmed, or substantially equivalent v0.4.2/v0.4.3 release paths are old paths. They may exist only as regression fixtures that v0.4.4 checks prove fail acceptance.
