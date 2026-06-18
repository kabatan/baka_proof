# Codex Handoff — GeometryFull2D v0.4.4 Reviewed

You are implementing `MARP-GEOLEAN-BASE-009` reviewed revision in `kabatan/baka_proof`.

## Read first

1. `docs/ai/changes/geometry-full2d-v0_4_4/BASE_SPEC.md`
2. `docs/ai/changes/geometry-full2d-v0_4_4/PLAN.md`
3. `docs/ai/changes/geometry-full2d-v0_4_4/ACCEPTANCE.md`
4. `docs/ai/changes/geometry-full2d-v0_4_4/REAL_PIPELINE_INVARIANTS.md`
5. `docs/ai/changes/geometry-full2d-v0_4_4/REFACTOR_DIRECTIVE.md`

## Do not do these

```text
Do not implement a projection-corpus pipeline again.
Do not select proof text from task_id/template_id/theorem_family/grammar_family/difficulty_tier/provenance/source_ref.
Do not fabricate solver refs from task id or theorem name.
Do not count a theorem unless it has ActualTaskPipelineRunV2 and SolverCausalityReportV1.
Do not count ExternalGoalPreserved unless GoalPreservationReportV1 proves exact/formal/structural goal preservation.
Do not require user-reviewed tasks as a release blocker; they are optional unless present.
Do not require B8 unless a model provider is enabled.
Do not close from v0.4.3 evidence.
```

## Expected behavior

Release acceptance should fail for much of implementation. This is normal. Log ReleaseBlockers and WorkDebt, then continue independent work. Stop only for HardBlockers.

## Final command

```bash
python scripts/check_release_acceptance_v0_4_4.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_4.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_4/evidence/release_acceptance_report.json
```

Final closure is allowed only if this command returns 0 with no blockers and `closure_allowed=true`.


Claim target: `V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY`
