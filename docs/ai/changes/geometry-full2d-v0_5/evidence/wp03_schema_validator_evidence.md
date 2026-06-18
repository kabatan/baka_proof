# WP-03 Schema Validator Evidence

Date: 2026-06-18

Status: WP-03 schema validator self-test implemented. This is not release completion evidence.

## Commands

```text
python scripts/check_schema_validators_v0_5.py --self-test
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_v0_5_spec_plan_consistency.py docs/ai/changes/geometry-full2d-v0_5
```

## Results

```text
check_schema_validators_v0_5.py --self-test: passed.
run_red_cases_v0_5.py --expect-failure: passed.
check_no_checker_whitelist_v0_5.py: passed.
check_v0_5_spec_plan_consistency.py: passed.
```

The self-test includes positive fixtures for:

```text
ActualTaskPipelineRunV4
LeanExtractionReportFull2D
GeometryFull2DClaimSpec
ProviderRunManifestFull2D
EngineOutputFull2D
IndependentCheckerReportFull2D
SelectedSolverDerivationV2
CompilerResultFull2D
LeanPatchCandidateFull2D
ProofWorkerResultFull2D
FinalVerifyReportFull2D
SolverCausalityReportV3
SolverBackedProofCertificateFull2D
GoalPreservationReportV2
RuleRegistryFull2D
StageFailureReportV1
DisabledStageReportV1
```

Negative fixtures reject target fact without derivation, naked target assertion, proof text in engine output, report-only causality, hash mismatch, stale artifact, and identity-rule counted success.

## Claim Ceiling

Allowed:

```text
WP-03 schemas and artifact validators have a passing self-test.
```

Not allowed:

```text
V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
SOURCE_FAITHFUL
ACCEPTANCE_COMPLETE
PRODUCTION_SAFE
R-ID VERIFIED
```
