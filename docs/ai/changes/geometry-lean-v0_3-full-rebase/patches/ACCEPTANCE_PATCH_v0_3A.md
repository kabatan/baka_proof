---
title: "Acceptance Patch — v0.3A release checker requirements"
patch_id: "MARP-GEOLEAN-ACCEPTANCE-004A"
status: "USER_APPROVED_ACTIVE_ACCEPTANCE_AMENDMENT"
created: "2026-06-13"
installed: "2026-06-13"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md"
---

# Acceptance Patch — v0.3A release checker requirements

This document gives concrete release checker behavior required by `MARP-GEOLEAN-BASE-004A` and `MARP-GEOLEAN-PLAN-004A`.

## 1. Release acceptance status model

`ReleaseAcceptanceReport` must report three independent status fields:

```yaml
ReleaseAcceptanceReport:
  status: "passed | blocked | failed"
  core_experiment_ready_status: "passed | blocked | failed"
  tonggeometry_model_backed_status: "passed | blocked | failed | not_claimed"
  claim_ceiling: "..."
  open_blockers: []
  blocked_claims: []
```

Allowed claim ceiling examples:

```text
core_experiment_ready_passed_no_tong_model_backed_claim
core_experiment_ready_passed_and_tong_model_backed_ready
release_acceptance_blocked_no_v0_3_completion_claim
release_acceptance_failed_no_v0_3_completion_claim
```

## 2. Dependency check behavior

### 2.1 Newclid-compatible

Core v0.3 requires:

```yaml
family: newclid_compatible
code_install_status: "installed | vendored"
claim_impact: "none"
```

No model artifact is required.

### 2.2 GenesisGeo-compatible

Core v0.3 requires:

```yaml
family: genesisgeo_compatible
code_install_status: "installed | vendored"
model_artifact_status: "available"
model_checkpoint_hash: "sha256:..."
model_inference_status: "available"
claim_impact: "none"
```

### 2.3 TongGeometry-compatible

Core v0.3 accepts either:

```yaml
family: tonggeometry_compatible
code_install_status: "installed | vendored"
model_artifact_status: "available"
model_checkpoint_hash: "sha256:..."
model_inference_status: "available"
claim_impact: "none"
```

or:

```yaml
family: tonggeometry_compatible
code_install_status: "installed | vendored"
model_artifact_status: "admitted_unavailable_external_artifact"
model_checkpoint_hash: null
model_inference_status: "unavailable"
claim_impact: "blocks_model_backed_tonggeometry_claim"
public_discovery_evidence_ref: "sha256:..."
```

The second case passes only the core v0.3 claim and blocks the Tong model-backed claim.

## 3. Nontrivial corpus checker

`scripts/check_level2_corpus_nontrivial.py` must fail unless:

```text
- corpus file exists
- config benchmark_pool references exactly present corpus IDs
- corpus has at least 25 tasks
- identity_hypothesis tasks <= 5
- nonidentity_symbolic_closure tasks >= 10
- auxiliary_construction tasks >= 5
- proof_worker_only_baseline tasks >= 5
- safe_reject_or_blocker tasks >= 5
- each task has normalized_goal_signature
- no normalized_goal_signature appears more than 3 times
- all release tasks set source_lean_mode = real_leangeo_dependency
- no theorem_statement or theorem source contains local toy target definitions
```

The checker must not rely only on `task_category`; it must use `is_identity_hypothesis` and `normalized_goal_signature`.

## 4. Matrix artifact checker

`scripts/check_matrix_artifact_derived.py --run-dir runs/<RUN_ID>` must fail unless:

```text
- level2_matrix_report.json exists
- artifact_derived_metrics = true
- fixture_run_used = false
- per_task_run_count = expected_per_task_run_count
- expected_per_task_run_count = len(benchmark_pool) * len(baselines)
- per_task_artifact_index.json exists
- every task/baseline pair has task_result.json
- metrics_B*.json values are aggregated from task_result.json statuses
- no release path imports or calls build_fixture_run/run_fixture
```

## 5. Fixture standard loop checker

`scripts/check_no_fixture_standard_loop_release.py` must fail if any release or matrix code imports/calls:

```text
build_fixture_run
run_fixture
GEOMETRY_FINAL_VERIFY_FIXTURE
```

It must also fail if release task Lean files contain local toy target definitions:

```text
def Point := Unit
def Coll
axiom Point
axiom Coll
```

`run_fixture` may remain only under unit/regression tests.

## 6. Provider layout checker

`scripts/check_provider_layout.py` must fail if `plugins/geometry_synthetic/provider.py` defines implementation classes. It may only re-export from `plugins.geometry_synthetic.providers.*`.

Forbidden class definitions in `provider.py`:

```text
ProviderRunManifest
CompositeSyntheticGeometryProvider*
Newclid*Adapter
GenesisGeo*Adapter
TongGeometry*Adapter
DummyEngineAdapter
```

## 7. Release checker integration

`src/math_auto_research/workflow/release_acceptance.py` must include checks for blockers 26–34 and must expose their results in `checked_blockers`.

The release checker must fail if it sees `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` in `CLOSURE.md` while any original or patch blocker is open.

It must fail if it sees `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY` while Tong model artifacts are unavailable or admitted-unavailable.
