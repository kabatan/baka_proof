---
title: "Closure — geometry x Lean v0.3 full rebase"
status: "V0_3A_CORE_EXPERIMENT_READY_PASSED_V0_3B_SOLVER_BACKED_PENDING"
created: "2026-06-13"
base_spec: "MARP-GEOLEAN-BASE-004"
plan: "MARP-GEOLEAN-PLAN-004"
patches:
  - "MARP-GEOLEAN-BASE-004A"
  - "MARP-GEOLEAN-PLAN-004A"
  - "MARP-GEOLEAN-ACCEPTANCE-004A"
  - "MARP-GEOLEAN-BASE-004B"
  - "MARP-GEOLEAN-PLAN-004B"
  - "MARP-GEOLEAN-ACCEPTANCE-004B"
---

# Closure — geometry x Lean v0.3 full rebase

## v0.3A closure claim statuses

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: not yet claimed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked
```

The prior v0.3A closure remains valid for the harness-ready/core experiment-ready claim under the approved Base Spec/Plan and v0.3A amendments. The separate TongGeometry model-backed heavy-search claim remains blocked because the tokenizer/lm_s/lm_l/cls checkpoint artifacts are not available and are classified as admitted unavailable external artifacts.

After installation of `MARP-GEOLEAN-BASE-004B`, `MARP-GEOLEAN-PLAN-004B`, and `MARP-GEOLEAN-ACCEPTANCE-004B`, this file is not a final v0.3B closure. v0.3B requires solver-backed proof repair to pass release blockers 35-47 before `V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY` may be claimed.

This closure does not claim:

```text
real Level2 advantage observed
arbitrary LeanGeo support
open-problem solving
PRODUCTION_SAFE
R-ID VERIFIED
```

## Authority

Approved authority documents:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md
```

Implementation approval:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md
```

## Release acceptance

Latest release acceptance evidence:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Required Base Spec §21 evidence references:

```text
repo audit:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_audit.md
dependency report:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
resource profile:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/local_resource_profile.json
selected implementations hash:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/selected_implementations_hash.txt
real provider smokes:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t23_newclid_adapter.md
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t24_genesisgeo_adapter.md
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t25_tonggeometry_adapter.md
target and corpus manifests:
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/target_library_status.json
  docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/t18_real_corpus_manifests.md
Level2 matrix report:
  runs/geometry_level2_pilot/level2_matrix_report.json
reproducibility report:
  runs/geometry_level2_pilot/reproducibility_report.json
```

Post-review hardening evidence:

```text
release blocker 24: replay_status=restored, missing_components=[]
release blocker 25: open_blockers_before_closure=[]
release blocker 30: artifact-derived metrics checker passed, including no fixture adapter versions in B2/B4 provider manifests and no provider task claiming final theorem.
```

Summary:

```json
{
  "status": "passed",
  "core_experiment_ready_status": "passed",
  "tonggeometry_model_backed_status": "blocked",
  "claim_ceiling": "core_experiment_ready_passed_no_tong_model_backed_claim",
  "open_blockers": [],
  "blocked_claims": [
    "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"
  ],
  "checked_blockers": "1-34"
}
```

## Final verification

Final command evidence:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_final_command_log.md
```

Commands passed:

```text
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

## Final commit

```text
implementation_closure_commit: e427015
```

## v0.3B resume state

```text
current_task: T48 — Audit current proof-repair gap
v0_3b_solver_backed_proof_repair_status: not_started
required_final_config: configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
required_final_report: docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Allowed future closure after v0.3B passes:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked by unavailable TongGeometry checkpoint artifacts
```

Git closure scope:

```text
All v0.3 full-rebase/v0.3A closure files are committed. The untracked top-level lib/ directory is outside this closure scope and was not staged or modified by this closure task.
```
