# Codex Handoff — GeometryFull2D v0.6 Reviewed Strict

Use only this v0.6 reviewed strict authority set:

```text
MARP-GEOLEAN-BASE-012
MARP-GEOLEAN-PLAN-012
MARP-GEOLEAN-ACCEPTANCE-012
```

Do not try to make the release checker green first. First make the generalized red cases fail. The final release claim is forbidden until the fresh execution-locked command passes:

```bash
python scripts/check_release_acceptance_v0_6.py \
  --config configs/benchmark_runs/geometry_full2d_v0_6.yaml \
  --fresh-run \
  --fail-on-stale \
  --no-skip \
  --all-baselines \
  --live-mutations \
  --output docs/ai/changes/geometry-full2d-v0_6/evidence/release_acceptance_report.json
```

Critical prohibitions:

```text
No target-fact provider.
No identity/direct counted rule.
No proof-from-shape compiler.
No rule-list artifact synthesis.
No field-only causality.
No B2-only matrix.
No family-coded baseline.
No projection corpus counted as positive.
No checker whitelist for release files.
No checker-created pipeline artifacts.
No stale evidence closure.
```

Release checker failure is expected until the actual full pipeline is implemented. Record ReleaseBlockers and continue with unblocked work packages.


## Authority identifiers

```text
MARP-GEOLEAN-BASE-012
MARP-GEOLEAN-PLAN-012
MARP-GEOLEAN-ACCEPTANCE-012
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```
