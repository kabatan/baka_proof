---
title: "Real Pipeline Invariants — GeometryFull2D v0.4.3"
status: "USER_APPROVED_ACTIVE"
base_spec: "MARP-GEOLEAN-BASE-008"
---

# Real Pipeline Invariants — GeometryFull2D v0.4.3

This document exists to prevent a repeat of the v0.4.2 failure mode.

## Invariant 1 — Evidence must be causally coupled

For a counted theorem, each artifact must be causally downstream of the previous artifact:

```text
source theorem
  causes extraction report
  causes claim spec
  causes provider request
  causes engine output
  causes compiler result
  causes patch candidate
  causes worker result
  causes final verify report
  causes certificate
  causes metric inclusion
```

Hash references alone are not sufficient if they do not prove this causal relation.

## Invariant 2 — No label-to-proof path

The following path is invalid:

```text
template_id / theorem_family / task_id -> proof text
```

Valid proof text must come from compiler output derived from normalized solver artifact.

## Invariant 3 — No fabricated solver references

`normalized_solver_artifact_ref` must be the ref emitted by provider engine output. It must not be created by batch proof artifact code.

## Invariant 4 — No overlay-only matrix

A matrix may consume replay artifacts only if those artifacts are valid `ActualTaskPipelineRunV1` records matching the current frozen corpus and config.

## Invariant 5 — Real engine evidence is verified externally to engine output

Engine output cannot self-certify. Each engine run must have an independent real integration evidence artifact.

## Invariant 6 — Corpus provenance is proof-critical for performance claims

Codex-generated tasks are synthetic. They cannot be counted as human-curated unless a separate user/reviewer manifest exists.

## Invariant 7 — Smoke tests are not release tests

Engine smoke, extraction smoke, and final-verify smoke are necessary but insufficient. Release requires corpus-wide evidence.

## Invariant 8 — Empty summaries fail

Any release report with empty metrics, advantage, engine usage, measured failure, checked R-ID, or used-rule coverage summaries is invalid.

## Invariant 9 — Debt ledger is authoritative

Open debt blocks release. Release acceptance must parse the ledger, not rely on a separately generated report field.

## Invariant 10 — Final theorem count must be artifact-derived

A final theorem count is valid only if every counted task has a valid certificate and final verify report.



## Invariant 11 — Engine semantic outputs only

Release-critical engines must output semantic artifacts only: facts, trace steps, constructions, side-condition reports, case/coverage reports, algebraic/metric/inequality certificates, and diagnostics. They must not output Lean proof text, tactic scripts, proof-region replacement text, exact lemma applications, theorem-family dispatch, task-id dispatch, or benchmark-template dispatch.

## Invariant 12 — Compiler input isolation

Release compilers may not read benchmark labels. They may consume only ClaimSpec, engine artifacts, RuleRegistry, SideConditionCalculus, and the target hash/edit region. Any compiler path that reads `template_id`, `theorem_family`, `provenance`, `difficulty_tier`, or benchmark labels to decide proof text is invalid.

## Invariant 13 — Substantive corpus is required

A large corpus of shallow reflexivity/direct-lemma tasks is not sufficient. SubstantiveTaskProfileV1 and ReviewManifestV1 are release-critical. Direct-lemma successes may not exceed the release ceiling.

## Invariant 14 — Baseline comparability is proof of advantage

Advantage metrics are valid only when baselines differ by the named disabled component and not by weaker FinalVerifyGate, weaker ProofWorker, hidden source theorem access, or different model/provider/resource setup.

## Invariant 15 — Causal-chain hash binds the run

ActualTaskPipelineRunV1 must include a recomputable causal_chain_hash over the ordered source/extraction/claim/provider/engine/compiler/patch/worker/final-verify/certificate artifacts. Metrics may count only runs whose causal chain is valid.
