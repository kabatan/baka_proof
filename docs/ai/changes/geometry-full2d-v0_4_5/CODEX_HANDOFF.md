# Codex Handoff — GeometryFull2D v0.4.5

Claim target: `V0.4.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`

Use only these active authorities:

```text
MARP-GEOLEAN-BASE-010
MARP-GEOLEAN-PLAN-010
MARP-GEOLEAN-ACCEPTANCE-010
```

Do not reuse v0.4.4 as a release path. v0.4.4 is a regression target.

Your objective is not to pass the checker by synthesizing records. Your objective is to implement a real solver-causal pipeline where solver artifacts are necessary for proof generation and destructive mutation reruns prove that necessity.

You must not implement:

```text
projection corpus counted as external goal preserved
target-shape-to-proof menu
family-coded baseline outcomes
boolean-only causality reports
engine outputs that contain proof text
compiler proof text generated before solver artifacts
```

If a release blocker appears, record it in DebtLedger and continue other unblocked work. Stop only on HardBlocker.

Final closure is forbidden until:

```text
check_release_acceptance_v0_4_5.py returns 0
all destructive causality reruns pass
all required summaries are nonempty
all regression shortcuts fail as expected
```

Additional v0.4.5 reviewed hardening:

```text
Every consumed solver fact/construction/certificate must have independent checker evidence.
A naked target assertion is not a solver artifact.
Provider/engine modules must not import release compiler or proof-generation modules.
```
