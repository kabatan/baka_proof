# WP-10 Evidence: ProofWorker and FinalVerifyGate

Status: local WP-10 gates passed. This is not final v0.5 release evidence.

## Scope

WP-10 implements the v0.5 ProofWorker and FinalVerifyGate path:

- ProofWorker applies `LeanPatchCandidateFull2D` only inside the MARP proof region.
- Source theorem proof region must be exactly sorry-only before patching.
- FinalVerifyGate runs `lake env lean` on the generated candidate.
- FinalVerifyGate checks theorem statement unchanged, no sorry, no forbidden declarations, no toy target definitions, admitted imports only, proof-region guard, and provenance refs.
- Worker output cannot claim final theorem; final theorem status comes only from `FinalVerifyReportFull2D`.

## Implemented Files

- `plugins/geometry_full2d/proof_worker_v0_5.py`
- `scripts/check_proof_worker_final_verify_v0_5.py`
- `scripts/geometry_full2d_v0_5_contracts.py`

## Evidence Commands

```powershell
python -m py_compile plugins\geometry_full2d\proof_worker_v0_5.py scripts\check_proof_worker_final_verify_v0_5.py scripts\geometry_full2d_v0_5_contracts.py
```

Result: passed.

```powershell
python scripts/check_proof_worker_final_verify_v0_5.py --run-dir runs\geometry_full2d_v0_5 --self-test
```

Result: passed.

Observed positive fixture:

- ProofWorker accepted a sorry-only source theorem and produced a patched candidate only inside the MARP proof region.
- FinalVerifyGate executed `lake env lean <candidate>` and got return code 0.
- FinalVerifyGate reported theorem statement unchanged, no sorry, no forbidden declarations, no toy target definitions, admitted imports only, and `proof_use_status: final_theorem`.

Observed negative fixtures:

- pre-proved source rejected with `source_theorem_not_sorry_only`;
- non-proof-region-only patch rejected with `patch_not_proof_region_only`;
- changed theorem statement rejected with `theorem_statement_changed`;
- candidate with sorry rejected with `sorry_present`;
- forbidden declaration rejected with `forbidden_declarations`;
- toy target definition rejected with `toy_target_definitions`;
- non-admitted import rejected with `non_admitted_imports`.

```powershell
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_schema_validators_v0_5.py --self-test
python scripts/run_red_cases_v0_5.py --expect-failure
```

Result: all passed.

## Release Harness Probe

The fail-closed release command was probed after WP-10:

```powershell
python scripts/check_release_acceptance_v0_5.py --config configs\benchmark_runs\geometry_full2d_v0_5.yaml --output docs\ai\changes\geometry-full2d-v0_5\evidence\release_acceptance_report.json --fresh-run
```

Result: failed closed, as expected before later WPs. The generated incomplete report and fresh release run directory were deleted and are not release evidence.

Observed summary statuses in the temporary report before deletion:

- `final_verify_summary.status == passed`
- `compiler_isolation_summary.status == passed`
- `independent_checker_summary.status == passed`
- `rule_registry_summary.status == passed`

K-032 was not present in the remaining release blockers. Remaining blockers are for later work packages, including corpus materialization, causality, used-rule coverage, matrix/baseline execution, metrics, debt closure, and final closure.

## Claim Ceiling After WP-10

Allowed: WP-10 ProofWorker and FinalVerifyGate gates have local evidence.

Not allowed:

- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY`
- `SOURCE_FAITHFUL`
- `ACCEPTANCE_COMPLETE`
- `PRODUCTION_SAFE`
- R-ID `VERIFIED`
