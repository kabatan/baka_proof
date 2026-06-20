# WP11 Solver Causality Live Evidence

Status: MECH ready for review.

Implemented files:

- `scripts/run_solver_causality_live_v0_6.py`
- `scripts/check_solver_causality_live_v0_6.py`

Evidence commands:

```bash
python -m py_compile scripts\run_solver_causality_live_v0_6.py scripts\check_solver_causality_live_v0_6.py
python scripts\check_solver_causality_live_v0_6.py --self-test --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp11_solver_causality_live_report.json
python scripts\run_solver_causality_live_v0_6.py --run-dir runs\wp09_v0_6_fresh --all-b2-successes --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp11_solver_causality_live_run_report.json
python scripts\check_solver_causality_live_v0_6.py --run-dir runs\wp09_v0_6_fresh --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp11_solver_causality_live_check_report.json
```

Observed result:

- All commands exited 0.
- The self-test creates one B2 `ActualTaskPipelineRunV4` fixture whose positive control passes `lake env lean`.
- The self-test runs all seven required `SolverCausalityLiveRunV1` cases: `positive_control`, `remove_selected_artifact`, `corrupt_non_target_intermediate`, `corrupt_construction_or_certificate`, `unsupported_rule_mutation`, `side_condition_mutation`, and `remove_checker_transcript`.
- Every destructive mutation reaches FinalVerify with a command log and fails to reproduce the same final theorem.
- The checker rejects field-only/report-only causality, missing command logs, mutation-same-final-theorem, positive-control failure, and checker-generated success artifact fixtures.
- The checker verifies command log refs, isolated temp dirs, `lake env lean` command shape, input/output hashes, patch hashes, and FinalVerify report file hash/path consistency.
- Running WP11 on `runs\wp09_v0_6_fresh` produced zero causality reports because that run currently has zero B2 counted final theorem successes.

Claim ceiling:

WP11 establishes the live destructive causality runner/checker mechanism and red-case rejection. It does not claim full pipeline completion, release readiness, corpus theorem success, all-baseline matrix completion, or live causality for release-counted successes. The current fresh run has no B2 `final_theorem` records, so no release-counted causality success exists yet.
