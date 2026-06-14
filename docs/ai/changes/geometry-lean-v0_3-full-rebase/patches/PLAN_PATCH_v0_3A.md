---
title: "Guardian Plan Patch — geometry × Lean v0.3A completion hardening"
patch_id: "MARP-GEOLEAN-PLAN-004A"
base_patch: "MARP-GEOLEAN-BASE-004A"
base_plan: "MARP-GEOLEAN-PLAN-004"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-007"
target_repo: "kabatan/baka_proof"
created: "2026-06-13"
installed: "2026-06-13"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md"
---

# Guardian Plan Patch — geometry × Lean v0.3A completion hardening

## 0. Authority

After approval, this Plan Patch amends `MARP-GEOLEAN-PLAN-004`. It adds tasks T38–T49 and modifies T25/T34/T36/T37 acceptance behavior.

The Base Spec plus `MARP-GEOLEAN-BASE-004A` remain authoritative. If this Plan Patch conflicts with the Base Patch, the Base Patch wins.

## 1. Patch execution rules for Codex

Codex must treat the current repository as partially implemented but not v0.3 complete.

Codex must not focus only on the missing TongGeometry checkpoint. It must also repair corpus, matrix, standard-loop, dependency-report, and acceptance blind spots.

Codex must preserve these constraints:

```text
- no AgentC/D core mode restoration
- no second target library
- no raw provider/model/DSL proof-use
- no fixture provider selected in release config
- no local toy geometry as release target
- no unmanaged provider process
- no model hard-code inside controller/worker
```

## 2. Modified stop conditions

Dependency failure is still not a stop condition. Codex must attempt install/vendor/pin. If TongGeometry model checkpoints remain unavailable after public discovery, Codex must:

```text
1. mark model_artifact_status = admitted_unavailable_external_artifact;
2. mark claim_impact = blocks_model_backed_tonggeometry_claim;
3. keep V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY blocked;
4. continue toward V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY if all other blockers can pass.
```

Codex must stop and report only if it would need to:

```text
- trust raw Tong output as proof;
- replace LeanGeoSubsetV1 with a toy/local target;
- fabricate model checkpoint evidence;
- satisfy corpus nontriviality by metadata labels only;
- satisfy matrix acceptance without per-task artifacts;
- weaken any patch blocker.
```

## 3. Task additions

### T38 — Install patch authority and record current deviation audit

Supports: `R-CLAIM-*`, `R-DEP-*`, `R-EVAL-*`, `R-LOOP-REAL-001`, `R-REFACTOR-010`.

Deliverables:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_deviation_audit.md
```

The deviation audit must explicitly check:

```text
- TongGeometry checkpoint status
- current corpus identity-hypothesis ratio
- whether run_geometry_level2_matrix uses per-task runs or metadata formulas
- whether StandardGeometryProofLoop release path uses real LeanGeo theorem files
- whether provider.py is facade-only
- whether dependency report has model_artifact_status / claim_impact fields
```

Verification:

```bash
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_deviation_audit.md
```

### T39 — Dependency claim-profile schema and probe update

Supports: `R-DEP-010`, `R-DEP-011`, patch blockers 26–28.

Deliverables:

```text
schemas/base/dependency_resolution_report.schema.json
scripts/probe_dependencies.py
scripts/check_dependency_claim_profile.py
scripts/check_dependency_report_model_status.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_discovery_report.md
```

Implementation details:

```text
- Split code_install_status from model_artifact_status.
- Add model_inference_status and claim_impact.
- GenesisGeo model checkpoint remains required for core experiment readiness.
- TongGeometry model checkpoint may be admitted_unavailable_external_artifact if public discovery fails.
- Missing Tong model must block only V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY, not core v0.3.
```

Verification:

```bash
python scripts/probe_dependencies.py --json --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
python scripts/check_dependency_claim_profile.py
python scripts/check_dependency_report_model_status.py
```

### T40 — Provider module layout refactor

Supports: `R-REFACTOR-010`.

Deliverables:

```text
plugins/geometry_synthetic/providers/provider_api.py
plugins/geometry_synthetic/providers/composite_provider.py
plugins/geometry_synthetic/providers/provider_run_manifest.py
plugins/geometry_synthetic/providers/newclid_adapter.py
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
plugins/geometry_synthetic/provider.py       # facade only
scripts/check_provider_layout.py
```

Implementation details:

```text
- Move implementation classes out of provider.py.
- provider.py may import and re-export names only.
- Preserve public import compatibility by re-exporting CompositeSyntheticGeometryProvider.
- No Base module may import provider internals by engine family.
```

Verification:

```bash
python scripts/check_provider_layout.py
python -m compileall -q plugins src scripts tests
make test-unit TEST_FILTER=composite_provider
make test-integration TEST_FILTER=newclid_adapter
make test-integration TEST_FILTER=genesisgeo_adapter
make test-integration TEST_FILTER=tonggeometry_adapter
```

### T41 — TongGeometry claim-profile smoke hardening

Supports: `R-SOLVER-005A`, `R-SOLVER-005B`, patch blockers 27–28.

Deliverables:

```text
scripts/run_tonggeometry_probe.py
scripts/run_tonggeometry_model_smoke.py
scripts/smoke_real_tonggeometry.py
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_smoke.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_backed_status.json
```

Acceptance behavior:

```text
Case 1: model artifacts present
  - aggregate checkpoint hash is non-null
  - model_inference_status=available
  - V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY may pass if other checks pass

Case 2: model artifacts unavailable but code-backed diagnostic path works
  - model_artifact_status=admitted_unavailable_external_artifact
  - model_inference_status=unavailable
  - claim_impact=blocks_model_backed_tonggeometry_claim
  - V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY may still pass
  - model-backed claim remains blocked
```

Verification:

```bash
make smoke-real-tonggeometry
make test-unit TEST_FILTER=tonggeometry_adapter
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
python scripts/check_dependency_claim_profile.py
```

### T42 — Nontrivial LeanGeoSubsetV1 corpus replacement

Supports: `R-EVAL-005`, `R-EVAL-005B`, patch blocker 29.

Deliverables:

```text
benchmarks/leangeo/RealSmokeCorpus.lean
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/rejected_by_extraction.jsonl
scripts/check_level2_corpus_nontrivial.py
```

Required corpus content:

```text
- At most 5 identity-hypothesis tasks.
- At least 10 nonidentity symbolic-closure tasks.
- At least 5 auxiliary-construction tasks.
- At least 5 proof-worker-only baseline tasks.
- At least 5 safe-reject/blocker tasks.
- No normalized goal signature appears more than 3 times.
- All release tasks import real LeanGeo-compatible definitions.
- No local toy Point/Coll target definitions in release corpus.
```

Implementation note:

If LeanGeo has limited theorem APIs, Codex may write synthetic theorems using real LeanGeo definitions, but the statements must not be merely repeated identity hypotheses. Metadata labels alone do not satisfy this task.

Verification:

```bash
python scripts/check_level2_corpus_nontrivial.py
python -m math_auto_research.cli.validate_artifact benchmarks/geometry/geometry_level2_pilot.jsonl
make lean-build
```

### T43 — Real task standard geometry loop

Supports: `R-LOOP-REAL-001`, patch blockers 31–32.

Deliverables:

```text
src/math_auto_research/workflow/standard_geometry_loop.py
# or the current plugin loop refactored so release code imports only the real-task API
plugins/geometry_synthetic/standard_loop.py
scripts/check_no_fixture_standard_loop_release.py
```

Required API:

```python
run_task(task, baseline, selected, run_root) -> TaskRunResult
```

Required behavior:

```text
- Use actual theorem_file_path and theorem_name.
- Create GoalAnchor from the real theorem.
- Run extraction on real Lean context or emit safe-reject.
- Run provider only when the baseline permits geometry.solve.
- Run compiler only on normalized outputs.
- Run FinalVerifyGate on actual theorem candidate.
- Emit per-task artifacts.
```

Forbidden in release path:

```text
- run_fixture()
- build_fixture_run()
- GEOMETRY_FINAL_VERIFY_FIXTURE
- local toy Point/Coll definitions
- `def Coll := True` target semantics
```

Verification:

```bash
python scripts/check_no_fixture_standard_loop_release.py
make test-integration TEST_FILTER=standard_geometry_loop
make smoke-geometry-final-verify
```

### T44 — Artifact-derived Level2 matrix

Supports: `R-EVAL-006`, patch blocker 30.

Deliverables:

```text
scripts/run_geometry_level2_matrix.py
plugins/geometry_synthetic/evaluation.py
src/math_auto_research/evaluation/metrics.py
runs/<run_id>/matrix_task_runs/**
scripts/check_matrix_artifact_derived.py
```

Implementation details:

```text
- Execute every benchmark task under B0/B1/B2/B3/B4/B5.
- For 25 tasks, produce 150 per-task run results.
- Compute metrics from TaskRunResult artifacts, not labels.
- Write per_task_artifact_index.json.
- Set artifact_derived_metrics=true and fixture_run_used=false.
- B2 and B4 must use real provider config.
- B5 may disable auxiliary construction only by evaluation config.
```

Verification:

```bash
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
python scripts/check_matrix_artifact_derived.py --run-dir runs/geometry_level2_pilot
python scripts/generate_repro_report.py --run-dir runs/geometry_level2_pilot
```

### T45 — Release acceptance hardening

Supports: `R-TEST-003`, patch blockers 26–34.

Deliverables:

```text
scripts/check_release_acceptance.py
src/math_auto_research/workflow/release_acceptance.py
scripts/check_dependency_claim_profile.py
scripts/check_dependency_report_model_status.py
scripts/check_level2_corpus_nontrivial.py
scripts/check_matrix_artifact_derived.py
scripts/check_no_fixture_standard_loop_release.py
scripts/check_provider_layout.py
```

Required new release checks:

```text
release_blocker_26_dependency_model_status_schema
release_blocker_27_tong_model_artifact_status_classified
release_blocker_28_no_tong_model_backed_overclaim
release_blocker_29_level2_corpus_nontrivial_floor
release_blocker_30_matrix_artifact_derived
release_blocker_31_no_fixture_standard_loop_release
release_blocker_32_real_task_standard_loop_available
release_blocker_33_provider_layout_facade_only
release_blocker_34_release_acceptance_patch_checks_present
```

Verification:

```bash
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
make test-unit TEST_FILTER=release_acceptance
```

### T46 — Replay and closure claim update

Supports: final closure requirements.

Deliverables:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_final_command_log.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
```

Closure rules:

```text
If all original and patch release blockers pass:
  may claim V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY.

If Tong model artifacts are unavailable but admitted unavailable:
  must explicitly state V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY is blocked.

If any per-task matrix, corpus, or standard-loop patch blocker remains:
  must state BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY.
```

Verification:

```bash
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

Review checkpoint: RC-9 after T46.

## 4. Modified existing task notes

### Patch to T25

T25 should no longer be read as requiring non-public TongGeometry checkpoints for core v0.3. It requires code-backed heavy_search diagnostics for core v0.3 and model-backed smoke for the separate Tong model-backed claim.

### Patch to T34

T34 must not generate matrix metrics from category labels. It must run per-task artifacts.

### Patch to T36

T36 must include release blockers 26–34 and call the new check scripts.

### Patch to T37

T37 closure must report both claim profiles independently:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY
```
