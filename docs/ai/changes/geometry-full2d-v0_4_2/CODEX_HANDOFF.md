<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: USER_APPROVED_ACTIVE
-->
---
title: "Codex Handoff — GeometryFull2D v0.4.2 Governed Full Implementation"
status: "USER_APPROVED_ACTIVE"
created: "2026-06-14"
---

# Codex Handoff — GeometryFull2D v0.4.2

You are implementing `V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY` in `kabatan/baka_proof`.

## Read first

```text
docs/ai/changes/geometry-full2d-v0_4_2/BASE_SPEC.md
docs/ai/changes/geometry-full2d-v0_4_2/PLAN.md
docs/ai/changes/geometry-full2d-v0_4_2/ACCEPTANCE.md
docs/ai/changes/geometry-full2d-v0_4_2/ENGINE_CONTRACTS.md
docs/ai/changes/geometry-full2d-v0_4_2/BLOCKER_AND_DEBT_POLICY.md
docs/ai/changes/geometry-full2d-v0_4_2/REFACTOR_DIRECTIVE.md
```

These documents are the authority. Do not use older geometry specs to weaken this work.

## Non-negotiable

```text
Do not implement a smaller v0.3B-like track.
Do not close with experiment-ready only.
Do not lower thresholds.
Do not mark in-target positive tasks as safe-reject success.
Do not use geometry_synthetic in release path.
Do not use toy geometry semantics.
Do not use raw solver or raw model output as proof.
Do not stop for ReleaseBlockers or WorkDebt.
Stop only for HardBlockers HB-01..HB-09.
```

## First commands / tasks

```text
1. Install these docs under docs/ai/changes/geometry-full2d-v0_4_2/.
2. Initialize debt/debt_ledger.jsonl.
3. Run repo audit.
4. Create plugins/geometry_full2d.
5. Create Lean facade MathAutoResearch.GeometryFull2D.
6. Implement progress acceptance before full release acceptance.
```

## Stop policy

If a test fails, do not stop. Classify it.

```text
HardBlocker: stop and report.
ReleaseBlocker: write debt ledger entry, continue.
WorkDebt: write debt ledger entry if needed, continue.
MeasuredFailure: count in metrics, continue.
```

## Closure

Do not write closure claiming `V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY` until final release acceptance passes with:

```text
hard_blockers=[]
release_blockers=[]
work_debt_open=[]
all thresholds passed
```
