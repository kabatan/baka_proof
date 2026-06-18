---
title: "WP-06 Evidence — Provider / Engine Stage Boundary"
status: "WP-06_IMPLEMENTED"
created: 2026-06-18
base_spec: "MARP-GEOLEAN-BASE-011"
plan: "MARP-GEOLEAN-PLAN-011"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-011"
claim_ceiling: "WP-06 provider boundary and engine-output gates implemented; complete pipeline readiness is not claimed."
---

# WP-06 Evidence — Provider / Engine Stage Boundary

## Implemented Files

- `plugins/geometry_full2d/provider_cli.py`
- `scripts/check_provider_stage_boundary_v0_5.py`
- `scripts/check_engine_outputs_v0_5.py`
- `plugins/geometry_full2d/provider.py` no longer imports `run_records`.
- `plugins/geometry_full2d/engines/*.py` no longer import `rule_registry`.
- `plugins/geometry_full2d/engine_contracts.py` provides provider-stage independent checker refs.

## Enforced WP-06 Properties

- `python -m plugins.geometry_full2d.provider_cli` executes provider work as a separate CLI stage.
- Provider CLI reads a ClaimSpec JSON, computes/binds a ClaimSpec ref, runs all required engine roles, and writes v0.5 `ProviderRunManifestFull2D` and `EngineOutputFull2D:2` artifacts.
- Provider and engine release-path import scanning rejects downstream compiler, rule registry, proof, proof worker, final verifier, matrix, run record, and prior v0.4 implementation imports.
- Engine outputs bind backend code hashes, provider stage run id, real execution evidence refs, normalized artifact refs, independent checker refs, and `proof_use_status=not_allowed`.
- Engine output checker rejects proof text, target facts with empty premises, missing required engine roles, missing semantic artifacts for normalized successes, and missing independent checker refs.

## Verification Commands

```text
python scripts/check_provider_stage_boundary_v0_5.py --self-test
python scripts/check_engine_outputs_v0_5.py --self-test
python -m unittest tests.unit.test_geometry_full2d_provider
python scripts/check_provider_stage_boundary_v0_5.py
python scripts/check_engine_outputs_v0_5.py --run-dir runs/geometry_full2d_v0_5
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_schema_validators_v0_5.py --self-test
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_release_acceptance_v0_5.py --config configs/benchmark_runs/geometry_full2d_v0_5.yaml --output docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json --fresh-run
git diff --check
```

## Observed Results

- Provider boundary self-test passed, including a negative fixture importing `plugins.geometry_full2d.compiler`.
- Engine outputs self-test passed, including mutation rejection for proof text and empty-premise target fact.
- Existing provider unit tests passed.
- Provider/engine release-path static import scan passed.
- Real `runs/geometry_full2d_v0_5` engine-output check fails closed because no release provider-stage artifacts exist yet.
- Red cases remain fully rejected: 19/19.
- Acceptance K coverage remains complete for K-001..K-033.
- No checker filename/role suppression was detected.
- Final release command still fails closed because WP-07+ independent checkers, rule registry, compiler, proof worker, matrix, causality, metrics, corpus freeze, and closure gates are not complete. The generated incomplete `release_acceptance_report.json` was intentionally deleted and is not release evidence.

## Non-Claims

- No counted release provider run has been completed.
- No independent solver checker implementation is claimed before WP-07.
- No release acceptance completion is claimed.
- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` is not claimed.
