# RC8 guardian boundary review result

Status: FAIL_FIXABLE

Reviewer: guardian_boundary_reviewer

## Findings

```text
Level2 matrix evidence was not sufficient for full v0.3 readiness because the
pilot/ablation configuration did not yet prove a 25-task Level2 corpus run and
the matrix claim ceiling still allowed fixture-level interpretation.
```

```text
Release acceptance was too weak: it checked command success and text surfaces
but did not reject fixture-level matrix evidence, missing required evaluation
metrics, or over-strong closure claims.
```

```text
GenesisGeo-compatible and TongGeometry-compatible evidence did not establish
model-backed inference. The evidence documents record missing
GenesisGeo checkpoint/runtime requirements and missing TongGeometry model paths.
```

## Remediation Status

```text
The Level2 corpus/matrix checks were strengthened to require 25 benchmark
entries, non-fixture corpus/config text, replay restoration, and the required
evaluation metric set.

Closure is now blocked rather than full-ready.

Release acceptance now blocks on missing model-backed GenesisGeo/TongGeometry
evidence.
```
