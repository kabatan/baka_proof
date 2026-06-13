---
title: "Guardian Plan — geometry × Lean v0.3 full rebase implementation"
plan_id: "MARP-GEOLEAN-PLAN-004"
version: "v0.3-full-rebase"
status: "USER_APPROVED_ACTIVE_WITH_V0_3A_PATCH"
created: "2026-06-12"
base_spec: "MARP-GEOLEAN-BASE-004"
active_patches:
  - "MARP-GEOLEAN-PLAN-004A"
target_repo: "https://github.com/kabatan/baka_proof"
---

# Guardian Plan — geometry × Lean v0.3 full rebase implementation

## 0. Plan authority

This Plan defines how Codex agents must implement `MARP-GEOLEAN-BASE-004`.

The Base Spec wins over this Plan if there is a conflict. This Plan must not add requirements, remove requirements, weaken requirements, or reinterpret requirements. Each task maps to explicit R-IDs and MECHs from the Base Spec.

This Plan is amended by `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md`. The Plan Patch adds T38-T46/T49-class hardening work and modifies T25/T34/T36/T37 acceptance behavior. If the Plan Patch conflicts with `BASE_SPEC_PATCH_v0_3A.md`, the Base Patch wins.

Implementation must not start until the user approves both:

```text
MARP-GEOLEAN-BASE-004
MARP-GEOLEAN-PLAN-004
```

## 1. Codex execution rules

For each task:

1. Read `docs/ai/ACTIVE_CONTEXT.md`.
2. Read the current task in this Plan.
3. Read all referenced Base Spec R-IDs and MECHs.
4. Inspect existing repo files before editing.
5. Remove or refactor conflicting implementation instead of preserving it.
6. Implement only the task scope.
7. Run verification commands.
8. Store evidence under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

9. Update Active Context with:
   - completed task
   - files changed
   - commands run
   - evidence refs
   - blockers
10. Stop at review checkpoints.

## 2. Global stop conditions

Codex must stop and request a user/reviewer decision if it needs to:

1. weaken any R-ID.
2. keep old root-level specs as active guidance.
3. use a second target library.
4. add AgentC/AgentD core modes.
5. hard-code GPT-Pro, Codex, DeepResearch, or any model endpoint into controller/worker code.
6. put Newclid/GenesisGeo/TongGeometry logic in Base.
7. use fixture adapters for release config.
8. trust raw provider/model output as proof.
9. bypass ResourceGovernor.
10. mutate protected theorem statement.
11. claim full experiment-ready without real integration evidence.
12. make a completion claim without fresh command evidence.

Dependency failure is not a stop condition by itself. Codex must attempt install/vendor/pin, emit `DependencyResolutionReport`, and mark dependent claims blocked if unresolved.

## 3. Global verification command set

By final release, the following commands must exist and pass:

```bash
make fmt
make lint
make typecheck
make test
make test-unit
make test-integration
make test-regression
make test-mutation
make lean-build
make lean-no-sorry

make smoke-env-bootstrap
make smoke-resource-governor
make smoke-model-provider-set
make smoke-geometry-extraction
make smoke-real-newclid
make smoke-real-genesisgeo
make smoke-real-tonggeometry
make smoke-geometry-provider
make smoke-geometry-trace
make smoke-geometry-construction
make smoke-geometry-final-verify
make smoke-level2-pilot

python scripts/check_old_specs_removed.py
python scripts/check_package_layout.py
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_ablation.yaml
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
```

Early tasks may create commands incrementally, but final acceptance requires the whole set.

## 4. Review checkpoints

```text
RC-0: after T02, repo rebase and old-spec deletion.
RC-1: after T07, Base schemas, package layout, and Base/plugin boundary.
RC-2: after T12, resource governance and dependency bootstrap.
RC-3: after T15, model provider and Lean verification boundary.
RC-4: after T20, target subset and extraction.
RC-5: after T25, real provider integration.
RC-6: after T29, compiler and construction path.
RC-7: after T33, standard loop and trust/bridge safety.
RC-8: after T37, evaluation pilot and release acceptance.
```

At every checkpoint, Codex must run the relevant Guardian reviewers if available and record reviewer outputs under evidence.

## 5. Task dependency graph

```text
T00 approve spec/plan
 -> T01 repo audit
 -> T02 cleanup superseded specs and duplicate layout
 -> T03 establish canonical repo skeleton
 -> T04 stable schema framework
 -> T05 SelectedImplementations and configs
 -> T06 ArtifactStore, RunLogger, DiagnosticBundle
 -> T07 ProofStateDAG core
 -> T08 plugin registry and manifest loader
 -> T09 ResourceGovernor and ProcessRunner
 -> T10 dependency bootstrap
 -> T11 LeanGeo dependency and TargetLibraryManifest
 -> T12 resource/dependency smoke evidence
 -> T13 ModelProviderSet
 -> T14 ResearchControllerPlugin and ProofWorkerPlugin contracts
 -> T15 LeanPort, ProofRegionGuard, FinalVerifyGate
 -> T16 geometry_synthetic plugin scaffold
 -> T17 LeanGeoSubsetV1 theorem grammar and mappings
 -> T18 real corpus manifests
 -> T19 GeometryExtractionContract
 -> T20 extraction mutation tests
 -> T21 GeometrySolverPolicy and GeometryExecutionPlan
 -> T22 CompositeSyntheticGeometryProvider shell
 -> T23 Newclid-compatible real adapter
 -> T24 GenesisGeo-compatible real adapter
 -> T25 TongGeometry-compatible real adapter
 -> T26 GeoTraceV1 and RuleRegistryV1
 -> T27 TraceCompiler
 -> T28 AuxiliaryConstructionCandidateV1
 -> T29 ConstructionCompiler
 -> T30 GeometryBridgeGate and TrustGuard
 -> T31 Standard geometry proof loop
 -> T32 run trace and contribution records
 -> T33 safety regression suite
 -> T34 Level2 pilot benchmark matrix
 -> T35 reproducibility and replay
 -> T36 release acceptance script
 -> T37 final evidence, reviews, closure
```

---

## 6. Tasks

### T00 — Approval gate

Supports: `R-REBASE-001`, `R-TEST-003`, all R-IDs through the approval and release-blocker gate.

Deliverables:

- User approval record under `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md`.
- Approved Base Spec copied to `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`.
- Approved Plan copied to `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`.

Verification:

```bash
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/user_approval.md
```

Stop condition:

- Stop if approval is missing.

### T01 — Current repo audit

Supports: `R-REBASE-001` to `R-REBASE-005`.

Purpose: produce a factual audit of current files before deleting/refactoring.

Deliverables:

- `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_audit.md`
- machine-readable file inventory:
  `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_file_inventory.json`
- list of superseded specs to delete.
- list of duplicate package paths.
- list of fixture-only production paths.
- list of current Makefile commands.

Implementation notes:

- Do not edit implementation code in T01.
- Include hashes for old root spec files before deletion.

Verification:

```bash
python - <<'PY'
from pathlib import Path
assert Path("docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_audit.md").exists()
assert Path("docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/repo_file_inventory.json").exists()
PY
```

### T02 — Cleanup superseded specs and ambiguous root guidance

Supports: `R-REBASE-001`, `R-REBASE-002`, `R-REBASE-003`.

Deliverables:

- Delete root-level superseded Guardian drafts.
- Move or delete `geometry_lean_pipeline_plan_v0_3.md` from root. If kept, place under `docs/ai/changes/geometry-lean-v0_3-full-rebase/source/` with non-authoritative header.
- Add `scripts/check_old_specs_removed.py`.
- Add `docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/superseded_spec_index.md`.

Implementation notes:

- Do not keep old spec files in root.
- Do not create multiple active spec folders for this change.

Verification:

```bash
python scripts/check_old_specs_removed.py
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/superseded_spec_index.md
```

Review checkpoint RC-0.

### T03 — Canonical package and repo skeleton

Supports: `R-REBASE-004`, `R-REBASE-005`, repo anatomy.

Deliverables:

- canonical directories from Base Spec Section 4.
- package root under `src/math_auto_research`.
- delete or neutralize top-level `math_auto_research` duplicate package if present.
- add `scripts/check_package_layout.py`.

Verification:

```bash
python scripts/check_package_layout.py
python -c "import math_auto_research, pathlib; print(pathlib.Path(math_auto_research.__file__).as_posix())"
```

### T04 — Stable schema framework

Supports: `R-SCHEMA-001` to `R-SCHEMA-006`.

Deliverables:

- schema framework using Pydantic v2 or equivalent.
- schema versioning.
- JSON schema export.
- CLI:

```bash
python -m math_auto_research.cli.validate_schema <file>
python -m math_auto_research.cli.validate_artifact <file>
```

Required files:

```text
src/math_auto_research/base/schemas.py
src/math_auto_research/cli/validate_schema.py
src/math_auto_research/cli/validate_artifact.py
schemas/base/
schemas/proof_state/
schemas/model/
schemas/resources/
schemas/geometry/
schemas/evaluation/
```

Verification:

```bash
make test-unit TEST_FILTER=schema
python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml || true
```

### T05 — SelectedImplementations and configs

Supports: `INV-002`, `R-SCHEMA-002`, `R-SCHEMA-004`, `R-SCHEMA-005`.

Deliverables:

- `SelectedImplementations` schema.
- `configs/selected_implementations/geometry_default.yaml`.
- exactly scalar fields.
- selected implementation hash.

Verification:

```bash
python -m math_auto_research.cli.validate_schema configs/selected_implementations/geometry_default.yaml
python scripts/check_no_loose_options.py
```

### T06 — ArtifactStore, RunLogger, DiagnosticBundle

Supports: `R-BASE-001` to `R-BASE-004`.

Deliverables:

```text
src/math_auto_research/base/artifacts/
src/math_auto_research/base/logging/
src/math_auto_research/base/diagnostics/
src/math_auto_research/base/trust/
```

Implement:

- immutable content-addressed artifacts.
- RunRecord.
- TrustReport.
- DiagnosticBundle.
- release evidence link support.

Verification:

```bash
make test-unit TEST_FILTER=artifact
make test-unit TEST_FILTER=run_logger
make test-unit TEST_FILTER=diagnostic
make test-unit TEST_FILTER=trust
```

### T07 — ProofStateDAG core

Supports: `R-DAG-001` to `R-DAG-005`.

Deliverables:

```text
src/math_auto_research/proof_state/dag_core.py
src/math_auto_research/proof_state/graph_patch.py
src/math_auto_research/proof_state/dag_writer.py
src/math_auto_research/proof_state/closure_engine.py
src/math_auto_research/proof_state/invalidation.py
src/math_auto_research/proof_state/state_reader.py
```

Implementation details:

- core node types only: Obligation, Derivation, EvidenceRef.
- acyclicity on proof-use graph.
- search-context not participating in closure.
- invalidation on proof-critical hash changes.
- GraphPatch-only mutation.

Verification:

```bash
make test-unit TEST_FILTER=proof_state
make test-regression TEST_FILTER=dag_raw_log_not_node
python scripts/check_domain_contamination.py
```

Review checkpoint RC-1.

### T08 — Plugin registry and manifest loader

Supports: `INV-001`, `INV-003`, `R-SOLVER-001`.

Deliverables:

```text
src/math_auto_research/plugin_api/
src/math_auto_research/base/registry/
plugins/geometry_synthetic/plugin.yaml
```

Implementation details:

- Base loads plugin by manifest.
- Base does not import plugin modules directly except through loader boundary.
- capability card for `geometry.solve`.

Verification:

```bash
make test-unit TEST_FILTER=plugin_registry
python scripts/check_domain_contamination.py
```

### T09 — ResourceGovernor and ProcessRunner

Supports: `R-RSRC-001` to `R-RSRC-005`, `MECH-RSRC-001`.

Deliverables:

```text
src/math_auto_research/base/resources/local_resource_profile.py
src/math_auto_research/base/resources/resource_budget.py
src/math_auto_research/base/resources/resource_governor.py
src/math_auto_research/base/resources/process_runner.py
scripts/probe_local_resources.py
configs/resource/default_local.yaml
configs/resource/local.example.yaml
```

Implementation details:

- named semaphores.
- process group management.
- soft/hard timeout.
- orphan cleanup.
- ResourceUsageReport.
- priority: final_verify > lean_build > proof_worker > symbolic_closure > construction_proposer > heavy_search.

Verification:

```bash
make smoke-resource-governor
python scripts/probe_local_resources.py --json > docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/local_resource_profile.json
make test-unit TEST_FILTER=resource
make test-regression TEST_FILTER=resource_bypass
```

### T10 — Dependency bootstrap

Supports: `R-ENV-001` to `R-ENV-003`, `MECH-BOOT-001`.

Deliverables:

```text
scripts/bootstrap_env.sh
scripts/probe_dependencies.py
configs/dependencies/
DependencyResolutionReport schema
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.md
```

Implementation details:

- Codex must attempt install/vendor/pin, not stop at missing dependency.
- record commands and versions.
- no target substitution.

Verification:

```bash
make smoke-env-bootstrap
python scripts/probe_dependencies.py --json > docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_probe.json
python -m math_auto_research.cli.validate_artifact docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_probe.json
```

### T11 — LeanGeo dependency and TargetLibraryManifest

Supports: `R-ENV-*`, `R-GEO-001`.

Deliverables:

- add/pin LeanGeo-compatible dependency.
- `TargetLibraryManifest`.
- namespace/theorem discovery report.
- no local toy target.

Verification:

```bash
make lean-build
python -m math_auto_research.cli.report_target_library_status > docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/target_library_status.json
python scripts/check_no_fixture_release.py
```

### T12 — Resource/dependency smoke evidence

Supports: `R-ENV-*`, `R-RSRC-*`.

Deliverables:

- resource profile evidence.
- dependency resolution evidence.
- make commands pass.

Verification:

```bash
make smoke-env-bootstrap
make smoke-resource-governor
```

Review checkpoint RC-2.

### T13 — ModelProviderSet

Supports: `R-MODEL-001` to `R-MODEL-003`, `MECH-MODEL-001`.

Deliverables:

```text
src/math_auto_research/base/model_provider/
schemas/model/model_provider_set.schema.json
configs/model_provider_sets/default.example.yaml
```

Implementation details:

- slot invocation interface.
- no hard-coded model names in code.
- dummy/local fixture model allowed only for tests and example config.

Verification:

```bash
make smoke-model-provider-set
make test-unit TEST_FILTER=model_provider
python scripts/check_model_hardcode.py
```

### T14 — ResearchControllerPlugin and ProofWorkerPlugin contracts

Supports: `R-MODEL-004`, `R-MODEL-005`.

Deliverables:

```text
src/math_auto_research/model_api/research_controller.py
src/math_auto_research/model_api/proof_worker.py
src/math_auto_research/model_api/action_plan.py
src/math_auto_research/model_api/work_order.py
src/math_auto_research/model_api/state_pack.py
```

Implementation details:

- plugins consume model slots.
- `ActionPlan` cannot close obligations.
- `WorkerResult` cannot claim final theorem; only FinalVerifyGate can.

Verification:

```bash
make test-unit TEST_FILTER=controller_plugin
make test-unit TEST_FILTER=proof_worker_plugin
make test-regression TEST_FILTER=model_output_not_proof
```

### T15 — LeanPort, ProofRegionGuard, FinalVerifyGate

Supports: `R-LEAN-001` to `R-LEAN-004`, `INV-006`.

Deliverables:

```text
src/math_auto_research/lean_integration/lean_port.py
src/math_auto_research/lean_integration/goal_anchor.py
src/math_auto_research/lean_integration/final_verify_gate.py
src/math_auto_research/lean_integration/proof_region_guard.py
src/math_auto_research/lean_integration/lean_error_summary.py
lean/MathAutoResearch/Base/
```

Verification:

```bash
make lean-build
make lean-no-sorry
make test-unit TEST_FILTER=final_verify
make test-regression TEST_FILTER=theorem_statement_hash
make test-regression TEST_FILTER=no_sorry
```

Review checkpoint RC-3.

### T16 — geometry_synthetic plugin scaffold

Supports: `INV-003`, `R-SOLVER-001`.

Deliverables:

```text
plugins/geometry_synthetic/plugin.yaml
plugins/geometry_synthetic/README.md
plugins/geometry_synthetic/solver_policy/
plugins/geometry_synthetic/providers/
plugins/geometry_synthetic/target_subset/
plugins/geometry_synthetic/extraction/
plugins/geometry_synthetic/trace/
plugins/geometry_synthetic/construction/
plugins/geometry_synthetic/bridge/
```

Verification:

```bash
make test-unit TEST_FILTER=geometry_plugin_scaffold
python scripts/check_domain_contamination.py
```

### T17 — LeanGeoSubsetV1 theorem grammar and mappings

Supports: `R-GEO-001` to `R-GEO-003`.

Deliverables:

```text
plugins/geometry_synthetic/target_subset/leangeo_subset_v1.yaml
plugins/geometry_synthetic/target_subset/predicate_mapping.yaml
plugins/geometry_synthetic/target_subset/construction_mapping.yaml
plugins/geometry_synthetic/target_subset/relation_mapping.yaml
lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/Grammar.lean
```

Acceptance details:

- target library exactly one.
- each grammar entry has fixtures.
- relation mapping classifies exact/sufficient/related/none.

Verification:

```bash
make test-unit TEST_FILTER=target_subset
make lean-build
```

### T18 — Real corpus manifests

Supports: `R-EVAL-001`.

Deliverables:

```text
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/rejected_by_extraction.jsonl
```

Implementation details:

- real corpus must import LeanGeo-compatible dependency.
- no local toy target.
- synthetic theorem files are allowed only if they use real LeanGeo definitions.

Verification:

```bash
python -m math_auto_research.cli.validate_artifact benchmarks/geometry/leangeo_real_smoke.jsonl
python -m math_auto_research.cli.validate_artifact benchmarks/geometry/geometry_level2_pilot.jsonl
python scripts/check_no_fixture_release.py
```

### T19 — GeometryExtractionContract

Supports: `R-EXTRACT-001` to `R-EXTRACT-003`.

Deliverables:

```text
plugins/geometry_synthetic/extraction/extraction_contract.py
plugins/geometry_synthetic/extraction/extraction_report.py
plugins/geometry_synthetic/extraction/claim_spec.py
```

Implementation details:

- semantic extraction.
- canonicalization.
- nondegeneracy/orientation/diagram assumption extraction where supported.
- safe reject.
- GeometryClaimSpec provenance.

Verification:

```bash
make smoke-geometry-extraction
make test-unit TEST_FILTER=geometry_extraction
make test-mutation TEST_FILTER=extraction
```

### T20 — Extraction mutation tests

Supports: `R-EXTRACT-*`, `R-TEST-002`.

Deliverables:

- mutation fixtures:
  - local notation ambiguity.
  - missing nondegeneracy.
  - unsupported orientation.
  - related-only target.
  - raw DSL claim.

Verification:

```bash
make test-mutation TEST_FILTER=extraction
```

Review checkpoint RC-4.

### T21 — GeometrySolverPolicy and GeometryExecutionPlan

Supports: `R-SOLVER-006`, `R-RSRC-*`.

Deliverables:

```text
plugins/geometry_synthetic/solver_policy/geometry_solver_policy.py
plugins/geometry_synthetic/solver_policy/geometry_solver_policy_v1.yaml
plugins/geometry_synthetic/solver_policy/execution_plan.py
configs/solver_policies/geometry_synthetic_v1.yaml
```

Verification:

```bash
make test-unit TEST_FILTER=geometry_solver_policy
make test-unit TEST_FILTER=resource_budget
```

### T22 — CompositeSyntheticGeometryProvider shell

Supports: `R-SOLVER-001`, `R-SOLVER-002`, `R-BASE-*`.

Deliverables:

```text
plugins/geometry_synthetic/providers/provider_api.py
plugins/geometry_synthetic/providers/composite_provider.py
plugins/geometry_synthetic/providers/provider_run_manifest.py
```

Implementation details:

- Base sees one provider.
- internal adapters communicate only through normalized records.
- ResourceGovernor integrated.

Verification:

```bash
make smoke-geometry-provider
make test-unit TEST_FILTER=composite_provider
make test-regression TEST_FILTER=provider_not_base_branching
```

### T23 — Newclid-compatible real adapter

Supports: `R-SOLVER-003`.

Deliverables:

```text
plugins/geometry_synthetic/providers/newclid_adapter.py
```

Implementation details:

- real dependency path.
- input conversion.
- output normalization to GeoTraceV1 or diagnostic.
- fail if fixture selected for release.

Verification:

```bash
make smoke-real-newclid
make test-integration TEST_FILTER=newclid_adapter
python scripts/check_no_fixture_release.py
```

### T24 — GenesisGeo-compatible real adapter

Supports: `R-SOLVER-004`, `R-AUX-001`.

Deliverables:

```text
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
```

Implementation details:

- output normalized to AuxiliaryConstructionCandidateV1.
- raw rationale non-proof.
- GPU/CPU guarded.

Verification:

```bash
make smoke-real-genesisgeo
make test-integration TEST_FILTER=genesisgeo_adapter
make test-regression TEST_FILTER=genesis_output_not_proof
```

### T25 — TongGeometry-compatible real adapter

Supports: `R-SOLVER-005`.

Deliverables:

```text
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
```

Implementation details:

- heavy/extreme budget only.
- exclusive semaphore.
- timeout/heartbeat/kill.
- normalized output only.

Verification:

```bash
make smoke-real-tonggeometry
make test-integration TEST_FILTER=tonggeometry_adapter
make test-regression TEST_FILTER=heavy_search_budget_gate
make test-regression TEST_FILTER=heavy_search_no_orphans
```

Review checkpoint RC-5.

### T26 — GeoTraceV1 and RuleRegistryV1

Supports: `R-RULE-001`, `R-TRACE-001`.

Deliverables:

```text
plugins/geometry_synthetic/trace/geotrace_v1.py
plugins/geometry_synthetic/trace/rule_registry_v1.py
plugins/geometry_synthetic/trace/side_condition_calculus.py
schemas/geometry/geotrace_v1.schema.json
schemas/geometry/rule_registry_v1.schema.json
```

Implementation details:

- at least an initial supported rule subset for real corpus.
- each rule has side conditions and fixtures.
- unsupported provider rules are blockers.

Verification:

```bash
make test-unit TEST_FILTER=geotrace
make test-unit TEST_FILTER=rule_registry
make test-mutation TEST_FILTER=rule_registry
```

### T27 — TraceCompiler

Supports: `R-TRACE-002`.

Deliverables:

```text
plugins/geometry_synthetic/trace/trace_compiler.py
lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/RuleTemplates.lean
```

Verification:

```bash
make smoke-geometry-trace
make test-unit TEST_FILTER=trace_compiler
make test-mutation TEST_FILTER=trace_compiler
make lean-build
```

### T28 — AuxiliaryConstructionCandidateV1

Supports: `R-AUX-001`.

Deliverables:

```text
plugins/geometry_synthetic/construction/auxiliary_construction_candidate_v1.py
schemas/geometry/auxiliary_construction_candidate_v1.schema.json
```

Verification:

```bash
make test-unit TEST_FILTER=auxiliary_construction_candidate
make test-regression TEST_FILTER=aux_rationale_not_proof
```

### T29 — ConstructionCompiler

Supports: `R-AUX-002`.

Deliverables:

```text
plugins/geometry_synthetic/construction/construction_compiler.py
lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/ConstructionTemplates.lean
```

Verification:

```bash
make smoke-geometry-construction
make test-unit TEST_FILTER=construction_compiler
make test-mutation TEST_FILTER=construction_compiler
make lean-build
```

Review checkpoint RC-6.

### T30 — GeometryBridgeGate and TrustGuard

Supports: `R-BRIDGE-001`, `R-TRUST-001`, `R-TRUST-002`.

Deliverables:

```text
plugins/geometry_synthetic/bridge/geometry_bridge_report.py
plugins/geometry_synthetic/bridge/relation_to_goal.py
src/math_auto_research/base/trust/
```

Verification:

```bash
make test-unit TEST_FILTER=geometry_bridge
make test-regression TEST_FILTER=raw_dsl_not_proof
make test-regression TEST_FILTER=raw_provider_not_proof
```

### T31 — Standard geometry proof loop

Supports: `MECH-PROOF-001`.

Deliverables:

```text
src/math_auto_research/workflow/standard_geometry_loop.py
```

Workflow:

```text
LeanPort -> GoalAnchor -> extraction -> geometry.solve -> compiler -> worker -> LeanPort -> FinalVerifyGate -> DAG update -> RunLogger
```

Verification:

```bash
make smoke-geometry-final-verify
make test-integration TEST_FILTER=standard_geometry_loop
```

### T32 — Run trace and contribution records

Supports: `R-BASE-002`, `R-SCHEMA-006`, `R-EVAL-*`.

Deliverables:

```text
src/math_auto_research/evaluation/evaluation_funnel.py
src/math_auto_research/evaluation/metrics.py
src/math_auto_research/evaluation/reproducibility_report.py
ResearchContributionRecord schema
ControllerStrategyLog schema
```

Verification:

```bash
make test-unit TEST_FILTER=evaluation_records
make test-unit TEST_FILTER=contribution_tracking
```

### T33 — Safety regression suite

Supports: `R-TEST-002`.

Deliverables:

- all required regression families.
- all required mutation families.
- scripts:
  - `check_domain_contamination.py`
  - `check_no_loose_options.py`
  - `check_model_hardcode.py`
  - `check_resource_bypass.py`
  - `check_no_fixture_release.py`

Verification:

```bash
make test-regression
make test-mutation
python scripts/check_domain_contamination.py
python scripts/check_no_loose_options.py
python scripts/check_model_hardcode.py
python scripts/check_resource_bypass.py
python scripts/check_no_fixture_release.py
```

Review checkpoint RC-7 begins after T33 if standard loop also passes.

### T34 — Level2 pilot benchmark matrix

Supports: `R-EVAL-001` to `R-EVAL-004`.

Deliverables:

```text
configs/benchmark_runs/geometry_level2_pilot.yaml
configs/benchmark_runs/geometry_level2_ablation.yaml
scripts/run_geometry_level2_matrix.py
```

Implementation details:

- B0/B1/B2/B3/B4/B5 are evaluation configs, not runtime modes.
- B2 must use real provider config.
- B5 disables auxiliary construction only by evaluation config, not by runtime optional mode.

Verification:

```bash
make smoke-level2-pilot
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

### T35 — Replay and reproducibility

Supports: `R-BASE-002`, `R-EVAL-*`.

Deliverables:

```text
src/math_auto_research/workflow/replay.py
scripts/generate_repro_report.py
```

Verification:

```bash
python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>
make test-integration TEST_FILTER=replay
```

### T36 — Release acceptance script

Supports: `R-TEST-003`, Release blockers.

Deliverables:

```text
scripts/check_release_acceptance.py
src/math_auto_research/workflow/release_acceptance.py
```

The script must check all release blockers in Base Spec Section 20.

Verification:

```bash
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```

### T37 — Final evidence, review, and closure

Supports: `R-TEST-003`, Base Spec Section 20 release blockers, and Base Spec Section 21 final closure requirements.

Deliverables:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/final_command_log.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance.json
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/reproducibility_report.md
```

Verification:

Run all global verification commands and cite evidence.

Allowed closure only if no release blockers remain:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

If any real dependency remains unresolved, closure must instead state:

```text
BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

and list exact blockers.

Review checkpoint RC-8.

---

## 7. Refactoring rules for Codex

### 7.1 Delete rather than preserve incompatible implementation

If existing code conflicts with Base Spec, Codex must remove or rewrite it. Do not keep compatibility shims unless they are explicitly required by this Plan.

Examples:

- Delete AgentC/D core modes.
- Delete Base branches on engine family names.
- Delete fixture provider from release configs.
- Delete root spec drafts.
- Delete duplicate package roots.
- Delete local toy geometry target from production paths.

### 7.2 Fixtures stay as tests only

Fixture code is allowed only if:

- path contains `tests/fixtures` or `Fixtures`.
- config name contains `fixture`.
- `proof_use_status` cannot reach `final_theorem`.
- release acceptance rejects it for experiment-ready.

### 7.3 Do not postpone required contracts

Codex must not replace required implementations with TODOs, NotImplemented, stub return values, or placeholder reports in final tasks.

Allowed temporarily before dependent task completion:

- scaffold class with explicit failing tests.
- fixture implementation for unit tests only.
- blocker diagnostic with evidence.

Forbidden in final release:

- placeholder BridgeGate.
- placeholder Coverage/Resource/Trust report.
- fixture-only provider selected by release config.
- dummy LeanGeo target.

---

## 8. Evidence naming convention

All evidence files must be under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

Suggested names:

```text
repo_audit.md
repo_file_inventory.json
superseded_spec_index.md
dependency_resolution.md
dependency_probe.json
local_resource_profile.json
selected_implementations_hash.txt
target_library_status.json
newclid_smoke.json
genesisgeo_smoke.json
tonggeometry_smoke.json
leangeo_real_smoke_report.json
level2_pilot_metrics.json
release_acceptance.json
final_command_log.md
reproducibility_report.md
```

---

## 9. Completion claim template

Use this only if all release blockers are absent:

```markdown
# CLOSURE — geometry × Lean v0.3 full rebase

Claim: V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY

Evidence:
- Spec: ...
- Plan: ...
- Commit: ...
- Repo audit: ...
- DependencyResolutionReport: ...
- LocalResourceProfile: ...
- TargetLibraryManifest: ...
- Real Newclid smoke: ...
- Real GenesisGeo smoke: ...
- Real TongGeometry smoke: ...
- LeanGeoSubsetV1 corpus: ...
- FinalVerifyGate report: ...
- Level2 pilot metrics: ...
- Release acceptance: ...
- Reproducibility: ...

Disallowed claims:
- open-problem solving
- arbitrary LeanGeo/Mathlib support
- Level2 advantage unless metrics show it
```

If blocked:

```markdown
# CLOSURE — blocked

Claim: BLOCKED_FOR_V0_3_FULL_IMPLEMENTED_EXPERIMENT_READY

Blocking R-IDs:
- ...

Evidence:
- ...

Allowed current claim:
- ...
```
