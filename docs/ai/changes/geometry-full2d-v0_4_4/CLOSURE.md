# GeometryFull2D v0.4.4 Closure

Status: closed after final release acceptance.

Allowed claim:

`V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY`

This closure does not claim external mathematical novelty, human-reviewed theorem quality beyond the governed corpus evidence, or production deployment outside this repository.

## Evidence

Final release command:

```powershell
python scripts\check_release_acceptance_v0_4_4.py --config configs\benchmark_runs\geometry_full2d_v0_4_4.yaml --output docs\ai\changes\geometry-full2d-v0_4_4\evidence\release_acceptance_report.json
```

Result:

- status: `passed`
- closure_allowed: `true`
- hard_blockers: `[]`
- release_blockers: `[]`
- work_debt_open: `[]`

Hashes:

- release report: `sha256:e24a5791048ea5ca50e48fabc60acd4b014ae65c2d20f4f90f6dfee45f3c18bf`
- corpus manifest file: `sha256:fdf955dcd89eb5307e0ac5badc9566a0264cc276e6161f7e464264b0b9d8ca07`
- benchmark config: `sha256:d96c3c8d4a124413f210f64c50bb879f8039ad52f14b6c29f17ba02c0d7c1da2`
- run records hash: `sha256:5b98e989c7c2fd902b3efe1979d804b5bab6362dde3c22ab7ebbaea3f83f3917`
- selected implementation hash in records: `sha256:ccb57681e6846e90398afc595365893df281cb51d9e860abc6f49a27d22ae702`
- git head used by final report: `391a7e3755d78663f6994a572c68fc9edbe0878a`

## Acceptance Summary

- counted positive tasks: 3350
- B2 final theorem successes: 3350
- B2 overall success rate: 1.0
- B2 solver causal success fraction: 1.0
- used concrete rules: 35
- used rule families: 27
- B8 status: `not_applicable_model_provider_not_used`

Baseline measured failures:

- B1: 2850
- B5: 450
- B6: 1550
- B7: 250

Advantage thresholds passed:

- B2 - B1 overall: 0.8507462686567164
- B2 - B5 construction subset: 1.0
- B2 - B6 algebraic/metric subset: 1.0
- B2 - B7 order/case subset: 1.0

## Non-Claims

The release evidence is repository-local and governed by `MARP-GEOLEAN-BASE-009`, `PLAN-009`, and `ACCEPTANCE-009`. It does not replace independent mathematical audit, external benchmark validation, or model-provider experiments.
