# v0.4.5 Shortcut Audit

Status: WP-01 evidence.

Authority: MARP-GEOLEAN-BASE-010 / PLAN-010 / ACCEPTANCE-010.

## Release-forbidden current paths

The following v0.4.4 paths are quarantined as regression/failure fixtures only:

- `scripts/generate_full2d_v0_4_4_corpus.py`
- `scripts/run_full2d_actual_task_v0_4_4.py`
- `scripts/check_solver_causality_reports_v0_4_4.py`

They may remain in the repository so that v0.4.5 regression checks can prove the old failure modes are rejected. They are not release success evidence for v0.4.5.

## Detected shortcut signatures

`scripts/run_full2d_actual_task_v0_4_4.py` contains release-forbidden target-shape proof construction:

- `_proof_from_shape`
- `_proof_from_source`
- `target_expr.startswith(...)` proof dispatch
- `_baseline_allows_success`
- `solver_causal_necessity = final_status == "final_theorem"`

`scripts/check_solver_causality_reports_v0_4_4.py` validates causality by reading fields such as `solver_causal_necessity` and `mutation_sensitive`; v0.4.5 requires destructive mutation rerun artifacts instead.

`scripts/generate_full2d_v0_4_4_corpus.py` writes goal-preservation metadata from the corpus generator path. v0.4.5 requires an independent checker against the external source registry.

## Implemented gate

The release-path checker is:

```bash
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py --static-only
```

Static mode scans v0.4.5 release entrypoints that exist, verifies that copied v0.4.4 shortcut fixtures are detected by self-tests, and records not-yet-created v0.4.5 entrypoints as pending rather than blocking WP-01.

Full mode is reserved for WP-13 and must inspect actual release run artifacts:

```bash
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py --config configs/benchmark_runs/geometry_full2d_v0_4_5.yaml --run-dir runs/geometry_full2d_v0_4_5
```

## WP-01 command evidence

Recorded command:

```bash
python scripts/check_release_path_forbidden_shortcuts_v0_4_5.py --static-only
```

Expected result for WP-01: pass if no current v0.4.5 release entrypoint imports or calls known shortcut paths, while v0.4.4 files are detected only as quarantined regression fixtures.
