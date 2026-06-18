---
title: "Refactor Directive — GeometryFull2D v0.4.4 Reviewed"
base_spec: "MARP-GEOLEAN-BASE-009"
revision: "reviewed-2026-06-18"
---

claim_target: "V0.4.4_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_PIPELINE_READY"

# Refactor Directive — GeometryFull2D v0.4.4 Reviewed

## 1. Purpose

The current v0.4.3 repository contains useful infrastructure but also release paths that allowed projection-corpus and direct-lemma success to pass. v0.4.4 must remove or quarantine those paths.

## 2. Quarantine from release path

The following must not be used by v0.4.4 release commands:

```text
scripts/build_full2d_proof_artifact_batch.py
scripts/run_full2d_matrix.py
scripts/run_full2d_matrix_v0_4_3.py
scripts/generate_full2d_external_projection_corpus.py as a counted positive generator
v0.4.2/v0.4.3 release_acceptance_report.json as closure evidence
v0.4.3 projection corpus files as release positives
any proof artifact overlay sidecar as a success source
any compiler path selecting proof from template_id/theorem_family/grammar_family
renamed, wrapped, copied, shimmed, or substantially equivalent versions of these release paths
```

They may remain under `legacy/` or `regression_fixtures/` only if v0.4.4 tests prove they fail release acceptance.

## 3. Replace with v0.4.4 release path

Required release path:

```text
source theorem with sorry-only proof region
  -> per-theorem Lean extraction
  -> ClaimSpecV2
  -> provider actual run
  -> semantic engine artifacts
  -> compiler from normalized artifacts
  -> SolverCausalityReportV1
  -> LeanPatchCandidate
  -> ProofWorker
  -> FinalVerifyGate
  -> SolverBackedProofCertificate
  -> ActualTaskPipelineRunV2
  -> matrix/metrics
```

## 4. Corpus replacement

Replace projection corpus release positives with:

```text
ExternalGoalPreserved tasks with GoalPreservationReportV1
SealedSolverChallenge tasks with SealedChallengeManifestV1
UserReviewedGoal tasks only when review manifests exist
```

Projection tasks become `ProjectionNonCounted` or regression fixtures.

## 5. Release evidence reset

Release evidence must be regenerated under v0.4.4. v0.4.3 reports are stale and not closure evidence.
