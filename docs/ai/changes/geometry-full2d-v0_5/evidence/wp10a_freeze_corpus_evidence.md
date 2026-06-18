# WP-10A Evidence: Implementation Freeze and Counted Corpus Materialization

Status: local WP-10A gates passed. This is not final v0.5 release evidence.

## Scope

WP-10A created an implementation freeze manifest and then generated counted corpus material after that freeze:

- freeze manifest binds implementation git head, selected implementation file hashes, checker hashes, config hash, corpus-tool hashes, and admitted release entrypoints;
- counted `SealedAdversarialHoldout` tasks are generated only after a valid freeze manifest exists;
- sealed tasks carry generator hash, grammar hash, freeze hash, seed, and challenge manifest hash;
- corpus checker validates current file hashes against the freeze manifest;
- statement diversity floors are enforced on the counted corpus;
- external goal preservation checker passes with zero external imported tasks and no self-attested reports.

This freeze is valid for the current implementation hash. Later changes to provider, compiler, rule registry, proof worker, final verifier, matrix runner, release checker, corpus generator, or checker code require regenerating the freeze manifest and holdout corpus.

## Implemented / Materialized Files

- `scripts/create_freeze_manifest_v0_5.py`
- `scripts/geometry_full2d_v0_5_corpus.py`
- `scripts/generate_sealed_adversarial_holdout_v0_5.py`
- `scripts/check_corpus_independence_v0_5.py`
- fail-closed release entrypoints for later WPs:
  - `scripts/run_full2d_matrix_v0_5.py`
  - `scripts/run_solver_causality_mutations_v0_5.py`
  - `scripts/check_solver_causality_reports_v0_5.py`
  - `scripts/check_full2d_baseline_comparability_v0_5.py`
  - `scripts/check_full2d_metrics_v0_5.py`
  - `scripts/check_full2d_used_rule_coverage_v0_5.py`
  - `scripts/check_full2d_engine_contribution_v0_5.py`
  - `scripts/check_debt_ledger_v0_5.py`
  - `scripts/check_closure_claim_ceiling_v0_5.py`
- `benchmarks/geometry_full2d_v0_5/freeze_manifest.json`
- `benchmarks/geometry_full2d_v0_5/corpus_manifest.json`

## Evidence Commands

```powershell
python -m py_compile scripts\geometry_full2d_v0_5_corpus.py scripts\generate_sealed_adversarial_holdout_v0_5.py scripts\check_corpus_independence_v0_5.py scripts\create_freeze_manifest_v0_5.py scripts\run_full2d_matrix_v0_5.py scripts\run_solver_causality_mutations_v0_5.py scripts\check_solver_causality_reports_v0_5.py scripts\check_full2d_baseline_comparability_v0_5.py scripts\check_full2d_metrics_v0_5.py scripts\check_full2d_used_rule_coverage_v0_5.py scripts\check_full2d_engine_contribution_v0_5.py scripts\check_debt_ledger_v0_5.py scripts\check_closure_claim_ceiling_v0_5.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_corpus_independence_v0_5.py --self-test
```

Result: all passed.

```powershell
python scripts/create_freeze_manifest_v0_5.py --output benchmarks\geometry_full2d_v0_5\freeze_manifest.json
```

Result: passed.

Observed freeze creation:

- checker file count: 26
- corpus tool file count: 5
- implementation file count: 9
- implementation git head: `db3d093117b413877b91cb804b2a3874a3d4352d`

```powershell
python scripts/generate_sealed_adversarial_holdout_v0_5.py --output-root benchmarks\geometry_full2d_v0_5 --count 1200 --negative-count 300 --seed 500 --freeze-manifest benchmarks\geometry_full2d_v0_5\freeze_manifest.json --counted
```

Result: passed.

Observed corpus materialization:

- sealed counted tasks: 1200
- negative target-outside/malformed tasks: 300
- total tasks: 1500

```powershell
python scripts/check_corpus_independence_v0_5.py --corpus-root benchmarks\geometry_full2d_v0_5 --freeze-manifest benchmarks\geometry_full2d_v0_5\freeze_manifest.json
python scripts/check_corpus_statement_diversity_v0_5.py --corpus-root benchmarks\geometry_full2d_v0_5
python scripts/check_goal_preservation_reports_v0_5.py --corpus-root benchmarks\geometry_full2d_v0_5
python scripts/run_red_cases_v0_5.py --expect-failure
```

Result: all passed.

Observed diversity summary:

- counted positive count: 1200
- unique normalized theorem skeletons: 288
- max exact skeleton duplicate: 8
- used relation families: 12
- construction/case/certificate required tasks: 400
- non-target intermediate required tasks: 600

## Release Harness Probe

The fail-closed release command was probed after WP-10A. It failed closed as expected before WP-11 and later WPs. The generated incomplete report and fresh run directory were deleted.

Observed summary statuses in the temporary report before deletion:

- `corpus_summary.status == passed`
- `corpus_summary.counted_positive_formal_lean_tasks == 1200`
- `corpus_summary.negative_target_outside_malformed_tasks == 300`
- `corpus_summary.sealed_adversarial_holdout_count == 1200`
- `corpus_statement_diversity_summary.status == passed`
- `final_verify_summary.status == passed`

Remaining release blockers were limited to later work packages: causality, engine contribution, used-rule coverage, metrics, baseline/matrix execution, debt/closure, and extraction/matrix command failures.

## Claim Ceiling After WP-10A

Allowed: WP-10A freeze and counted corpus gates have local evidence for the current implementation hash.

Not allowed:

- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`
- `SOURCE_FAITHFUL`
- `ACCEPTANCE_COMPLETE`
- `PRODUCTION_SAFE`
- R-ID `VERIFIED`
