---
title: "Codex Handoff — GeometryFull2D v0.4.3 Real Pipeline Recovery"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-009"
base_spec: "MARP-GEOLEAN-BASE-008"
---

# Codex Handoff — GeometryFull2D v0.4.3 Real Pipeline Recovery

This handoff is historical. Do not use it as active implementation authority for v0.4.4 work.

You are implementing `MARP-GEOLEAN-BASE-008` and `MARP-GEOLEAN-PLAN-008` in `kabatan/baka_proof`.

## Absolute rules

```text
1. Do not weaken the Base Spec.
2. Do not lower thresholds.
3. Do not mark v0.4.2 passed status as v0.4.3 completion.
4. Do not use template_id/theorem_family/task_id to select proof text in release path.
5. Do not fabricate solver refs.
6. Do not count proof artifacts unless they belong to valid ActualTaskPipelineRunV1.
7. Do not count Codex-generated tasks as human curated unless a user/reviewer manifest is present.
8. Do not claim release while debt ledger has open entries.
9. Do not generate many shallow formal theorems and treat that as full prover performance.
10. Do not let engines output proof snippets, tactic scripts, or benchmark dispatch fields.
11. Do not let compilers read benchmark labels to choose proof text.
12. Do not weaken baselines to create artificial advantage.
13. Do not omit causal_chain_hash or anti-v0.4.2 regression evidence.
```

## Continue-on-debt policy

If you encounter a ReleaseBlocker or WorkDebt, record it and continue independent work. Stop only for HardBlockers in the Base Spec.

## Required first commands

After installing docs, run:

```bash
python scripts/check_active_guardian_spec_v0_4_3.py
python scripts/check_no_v042_template_release_path.py
```

Expect release acceptance to fail until the real pipeline is implemented. A failing release checker is not a reason to stop; it is guidance.

## Required final command

```bash
python scripts/check_release_acceptance_v0_4_3.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_3/evidence/release_acceptance_report.json
```

Release is valid only if this passes with no hard blockers, no release blockers, no open work debt, non-empty summaries, and validated actual pipeline runs.



## Integrated anti-gaming work

The following are mandatory v0.4.3 work, not a later patch:

```text
1. Implement substantive corpus profile checker.
2. Implement ReviewManifestV1 checker.
3. Enforce engine semantic-output guard.
4. Enforce compiler input isolation.
5. Enforce baseline comparability.
6. Add causal_chain_hash to ActualTaskPipelineRunV1.
7. Add anti-v0.4.2 template-overlay regression fixture.
8. Wire K-016..K-024 into final release acceptance.
```

Continue-on-debt remains active: record ReleaseBlockers and continue independent work. Do not close release until every v0.4.3 acceptance check passes.
