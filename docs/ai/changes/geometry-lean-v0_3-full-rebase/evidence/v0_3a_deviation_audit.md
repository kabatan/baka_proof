---
title: v0.3A deviation audit
status: ACTIVE_DEVIATION_AUDIT
created: 2026-06-13
purpose: Record current repository deviations against MARP-GEOLEAN-BASE-004A and MARP-GEOLEAN-PLAN-004A before implementation resumes.
authority: Evidence record only; does not weaken Base/Plan requirements or mark R-IDs verified.
---

# v0.3A Deviation Audit

## Summary

The v0.3A patch is installed, but the repository is not yet v0.3A complete.
The current implementation still violates the patch requirements in dependency
claim-profile reporting, corpus nontriviality, matrix artifact derivation,
standard-loop release path separation, and provider module layout.

## TongGeometry Checkpoint Status

Current release acceptance status:

```text
status: blocked
open_blockers:
- release_blocker_11_real_provider_smoke_evidence
model_backed_errors:
- missing_model_checkpoint:tonggeometry_compatible
claim_ceiling: release_acceptance_blocked_no_v0_3_completion_claim
```

Under `BASE_SPEC_PATCH_v0_3A.md`, this blocker must be reclassified into the
split claim profile:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY:
  may proceed if TongGeometry code-backed diagnostics work and model artifacts
  are admitted_unavailable_external_artifact.

V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY:
  remains blocked until tokenizer/lm_s/lm_l/cls exist and model smoke passes.
```

Current dependency report still has the old shape:

```text
install_status
version_or_commit
checkpoint_hash
```

It does not yet expose:

```text
code_install_status
model_artifact_status
model_inference_status
claim_impact
public_discovery_evidence_ref
```

## Corpus Nontriviality

Current `benchmarks/geometry/geometry_level2_pilot.jsonl` audit:

```text
task_count: 25
task_categories:
  simple_symbolic_closure: 10
  auxiliary_construction: 5
  proof_worker_only_baseline: 5
  safe_reject_blocker: 5
is_identity_hypothesis field: missing for all 25 entries
source_lean_mode field: missing for all 25 entries
normalized_goal_signature field: missing for all 25 entries
```

This fails `R-EVAL-005` because the patch requires explicit identity flags,
normalized goal signatures, real LeanGeo source mode, duplicate-signature
limits, and nontrivial category floors.

## Matrix Derivation

Current matrix/evaluation code still uses fixture and metadata-derived paths:

```text
plugins/geometry_synthetic/evaluation.py imports build_fixture_run
plugins/geometry_synthetic/evaluation.py computes metrics from task_category counts
plugins/geometry_synthetic/run_trace.py defines build_fixture_run
```

No current evidence shows:

```text
artifact_derived_metrics=true
fixture_run_used=false
per_task_run_count=150
per_task_artifact_index.json
matrix_task_runs/** per task/baseline artifacts
```

This fails `R-EVAL-006`.

## Standard Loop Release Path

Current standard-loop code still contains fixture-only local toy definitions:

```text
plugins/geometry_synthetic/standard_loop.py:
  GEOMETRY_FINAL_VERIFY_FIXTURE = "def Point := Unit ..."
  def run_fixture(...)
```

Current release/matrix-adjacent code still imports fixture helpers:

```text
plugins/geometry_synthetic/evaluation.py imports build_fixture_run
scripts/smoke_geometry_final_verify.py calls StandardGeometryProofLoop().run_fixture()
```

`run_fixture()` may remain for tests, but release matrix and release acceptance
must not use it. The release-path `run_task(...)` API required by
`R-LOOP-REAL-001` is not yet implemented.

## Provider Layout

Current provider implementation remains monolithic:

```text
plugins/geometry_synthetic/provider.py defines:
  ProviderRunManifest
  DummyEngineAdapter
  NewclidCompatibleSymbolicClosureAdapter
  GenesisGeoCompatibleConstructionProposerAdapter
  TongGeometryCompatibleHeavySearchAdapter
  CompositeSyntheticGeometryProviderV1
```

This fails `R-REFACTOR-010`, which requires implementation classes under:

```text
plugins/geometry_synthetic/providers/**
```

with `plugins/geometry_synthetic/provider.py` reduced to a compatibility
facade.

## Missing Patch Checkers

The following required v0.3A checker scripts are not yet implemented:

```text
scripts/check_dependency_claim_profile.py
scripts/check_dependency_report_model_status.py
scripts/check_level2_corpus_nontrivial.py
scripts/check_matrix_artifact_derived.py
scripts/check_no_fixture_standard_loop_release.py
scripts/check_provider_layout.py
```

Release acceptance does not yet include blockers 26-34.

## Next Task

Implementation should resume at:

```text
T39 — Dependency claim-profile schema and probe update
```

after this T38 patch-install audit is committed.
