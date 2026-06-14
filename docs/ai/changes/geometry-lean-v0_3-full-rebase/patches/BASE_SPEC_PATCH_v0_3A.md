---
title: "Guardian Base Spec Patch — geometry × Lean v0.3A experiment-readiness hardening"
patch_id: "MARP-GEOLEAN-BASE-004A"
base_spec: "MARP-GEOLEAN-BASE-004"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-007"
target_repo: "kabatan/baka_proof"
created: "2026-06-13"
installed: "2026-06-13"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md"
---

# Guardian Base Spec Patch — geometry × Lean v0.3A experiment-readiness hardening

## 0. Authority

After user approval, this patch amends:

```text
MARP-GEOLEAN-BASE-004
```

It does not replace the full Base Spec. It supersedes only the clauses explicitly listed below.

If this patch conflicts with the unpatched `BASE-004`, this patch wins for the patched R-IDs, release blockers, and claim profiles. All other `BASE-004` invariants remain in force.

Codex must not implement convenience shortcuts that satisfy the old release checker while bypassing this patch.

## 1. Purpose of this patch

This patch addresses two classes of problems discovered after the v0.3 full-rebase implementation pass:

```text
Class A — external artifact blocker:
  TongGeometry source code can be vendored and run as a resource-governed diagnostic path,
  but trained model checkpoints may be unavailable or non-public.

Class B — experiment-readiness blind spots:
  the current Level2 corpus and matrix can pass structural checks while remaining too trivial
  or fixture-derived to support meaningful experiment launch.
```

The patch therefore does **not** merely weaken the TongGeometry requirement. It strengthens the corpus, matrix, standard-loop, dependency-report, and release-acceptance requirements.

## 2. Claim profiles

### R-CLAIM-001 — Split core experiment readiness from model-backed TongGeometry readiness

The following claim profiles are now distinct.

```yaml
ClaimProfiles:
  V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY:
    meaning: >
      The repo can launch and replay non-fixture geometry × Lean v0.3 experiments
      over the approved LeanGeoSubsetV1 pilot corpus, with real Newclid-compatible
      symbolic closure, real GenesisGeo-compatible construction proposal, a
      resource-governed TongGeometry-compatible heavy_search role, artifact-derived
      Level2 matrix metrics, and all proof-use safety gates.
    requires_tonggeometry_model_checkpoint: false
    requires_tonggeometry_code_backed_heavy_search: true
    allows_tonggeometry_model_artifact_status:
      - available
      - admitted_unavailable_external_artifact

  V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY:
    meaning: >
      The TongGeometry-compatible heavy_search role is backed by local tokenizer,
      small language model, large language model, and classifier artifacts and can
      pass model-load / model-inference smoke.
    requires_tonggeometry_model_checkpoint: true
    required_environment_variables:
      - TONGGEOMETRY_TOKENIZER
      - TONGGEOMETRY_LM_S
      - TONGGEOMETRY_LM_L
      - TONGGEOMETRY_CLS
```

The repo may claim `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` without the second claim only if the missing TongGeometry model artifacts are recorded as `admitted_unavailable_external_artifact` with public-discovery evidence and all other v0.3A release blockers pass.

The repo must not claim model-backed TongGeometry heavy search unless `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY` passes.

### R-CLAIM-002 — No implied advantage claim

`V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` still does not imply a positive Level2 advantage. It means that the non-fixture Level2 experiment can be run and replayed. Any advantage claim must be separately supported by metrics.

## 3. Dependency and model artifact requirements

### R-DEP-010 — Enhanced DependencyResolutionReport

`DependencyResolutionReport.engines[*]` must use the following fields for model-backed roles:

```yaml
EngineDependencyStatus:
  role: "symbolic_closure | construction_proposer | heavy_search"
  family: "newclid_compatible | genesisgeo_compatible | tonggeometry_compatible"

  code_install_status: "installed | vendored | unavailable | failed"
  code_version_or_commit: "..."
  code_source: "pypi | git | local_vendor | system_path | release | unknown"

  model_artifact_expected: true
  model_artifact_status: "available | admitted_unavailable_external_artifact | unavailable | failed | not_applicable"
  model_checkpoint_hash: "sha256:... | null"
  model_inference_status: "available | unavailable | failed | not_applicable"

  public_discovery_evidence_ref: "sha256:... | null"
  claim_impact: "none | blocks_core_experiment_ready | blocks_model_backed_tonggeometry_claim | blocks_provider_role"
  evidence_refs: []
```

For `newclid_compatible`, `model_artifact_expected` may be false and `model_artifact_status=not_applicable`.

For `genesisgeo_compatible`, if the design uses a neural proposer, model checkpoint availability is required for core experiment readiness.

For `tonggeometry_compatible`, if public checkpoint discovery fails but code is vendored/importable and heavy_search diagnostic smoke passes, the dependency report may set:

```yaml
model_artifact_status: "admitted_unavailable_external_artifact"
model_inference_status: "unavailable"
claim_impact: "blocks_model_backed_tonggeometry_claim"
```

This does not block `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY`, but it blocks `V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY`.

### R-DEP-011 — Public discovery evidence for admitted-unavailable model artifacts

If Codex marks TongGeometry model artifacts as `admitted_unavailable_external_artifact`, it must emit:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/tonggeometry_model_discovery_report.md
```

The report must include:

```text
- vendored repository path and commit
- import status
- release / asset discovery attempts
- Hugging Face or equivalent model artifact search attempts
- README / documentation checkpoint-link status
- reason why the artifact cannot be installed automatically
- explicit statement that model-backed TongGeometry heavy search remains blocked
```

## 4. TongGeometry-compatible provider requirements

### R-SOLVER-005A — TongGeometry role claim levels

Patch `R-SOLVER-005` as follows.

TongGeometry-compatible adapter must support two claim levels:

```yaml
TongGeometryHeavySearchClaimLevel:
  code_backed_diagnostic:
    required_for: "V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY"
    must_have:
      - vendored or installed TongGeometry-compatible source
      - import or runnable probe status
      - ResourceGovernor-managed heavy_search execution
      - heavy/extreme budget gate
      - timeout / heartbeat / process cleanup
      - ProviderRunManifest
      - ResourceUsageReport
      - raw output proof_use_status = not_allowed
      - model_artifact_status either available or admitted_unavailable_external_artifact

  model_backed_heavy_search:
    required_for: "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"
    must_have:
      - TONGGEOMETRY_TOKENIZER
      - TONGGEOMETRY_LM_S
      - TONGGEOMETRY_LM_L
      - TONGGEOMETRY_CLS
      - aggregate checkpoint hash
      - model_inference_status = available
      - model smoke report
```

Even in `model_backed_heavy_search`, raw Tong output is not proof evidence. Proof-use still requires normalization to `GeoTraceV1` or `AuxiliaryConstructionCandidateV1`, compilation, ProofWorker, LeanPort, and FinalVerifyGate.

### R-SOLVER-005B — Tong normalized output requirement

If model-backed TongGeometry emits a proof plan, construction proposal, or trace-like output, the provider must either:

```text
1. normalize it to GeoTraceV1 or AuxiliaryConstructionCandidateV1;
2. or return a diagnostic blocker explaining unsupported normalization.
```

It must never mark a raw Tong output as `lean_patch_candidate`, `goal_level_allowed`, or `final_theorem`.

## 5. Corpus hardening requirements

### R-EVAL-005 — Nontrivial LeanGeoSubsetV1 corpus floor

Patch `R-EVAL-001` with the following stricter conditions.

`GeometryLevel2PilotCorpus` must contain at least 25 tasks and must satisfy all of the following:

```yaml
GeometryLevel2PilotCorpusFloor:
  total_tasks_min: 25

  identity_hypothesis_tasks_max: 5

  nonidentity_symbolic_closure_tasks_min: 10
  auxiliary_construction_tasks_min: 5
  proof_worker_only_baseline_tasks_min: 5
  safe_reject_or_blocker_tasks_min: 5

  duplicate_normalized_goal_signature_max_per_signature: 3

  each_task_requires:
    - entry_id
    - theorem_file_path
    - theorem_name
    - target_library = "LeanGeoSubsetV1:1.0.0"
    - task_category
    - normalized_goal_signature
    - is_identity_hypothesis: boolean
    - expected_required_stages
    - acceptance_eligible: boolean
    - source_lean_mode: "real_leangeo_dependency"
```

Allowed task categories:

```text
nonidentity_symbolic_closure
auxiliary_construction
proof_worker_only_baseline
safe_reject_or_blocker
identity_hypothesis_smoke
```

The old categories `simple_symbolic_closure` and `auxiliary_construction` may remain only if their metadata satisfies the new nontriviality fields. A task labelled `auxiliary_construction` but proving `h : P ⊢ P` is invalid.

A task is `is_identity_hypothesis=true` if its target proposition is syntactically equal, after canonicalization, to one of its assumptions.

A release corpus must fail if more than 5 tasks are identity hypotheses, regardless of category labels.

### R-EVAL-005B — Corpus Lean source restrictions

Release corpus Lean files must import a LeanGeo-compatible dependency and must not define local toy substitutes for target semantics.

Forbidden in release corpus Lean files:

```lean
def Point := Unit
def Coll ... := True
axiom Point : Type
axiom Coll : ...
```

A release corpus theorem may be synthetic, but it must use real LeanGeo-compatible definitions and must be capable of exercising at least one of:

```text
semantic extraction,
RuleRegistry non-identity rule,
auxiliary construction proposal,
ConstructionCompiler side-condition generation,
safe-reject diagnostic,
FinalVerifyGate.
```

## 6. Matrix and standard-loop requirements

### R-LOOP-REAL-001 — Real task standard loop

`StandardGeometryProofLoop` must expose a release-path method:

```python
run_task(task: BenchmarkTask, baseline: BaselineConfig, selected: SelectedImplementations, run_root: Path) -> TaskRunResult
```

Required behavior:

```text
1. Read the actual theorem file from task.theorem_file_path.
2. Build GoalAnchor from the actual theorem_name and protected theorem statement.
3. Run GeometryExtractionContract on the actual Lean goal/context or emit safe-reject diagnostic.
4. If baseline permits geometry.solve, call CompositeSyntheticGeometryProvider through GeometrySolverPolicy.
5. Run TraceCompiler or ConstructionCompiler only on normalized outputs.
6. Run ProofWorkerPlugin where the baseline permits worker repair.
7. Run FinalVerifyGate against the actual theorem file or admitted generated copy.
8. Emit TaskRunResult, FinalVerifyReport or blocker diagnostic, and per-task artifact index.
```

`run_fixture()` may remain only for unit/regression tests. It must not be imported or called from release matrix, release acceptance, or non-fixture benchmark scripts.

### R-EVAL-006 — Artifact-derived Level2 matrix

`run_geometry_level2_matrix.py` must execute every selected benchmark task under every selected baseline and aggregate metrics from per-task artifacts.

For `GeometryLevel2PilotCorpus` with 25 tasks and B0–B5 baselines:

```yaml
expected_per_task_run_count: 150
```

The matrix report must include:

```yaml
artifact_derived_metrics: true
fixture_run_used: false
per_task_run_count: 150
expected_per_task_run_count: 150
per_task_artifact_index_ref: "sha256:..."
metrics_source: "per_task_task_run_results"
```

For each task/baseline pair, the run directory must contain:

```text
task_result.json
artifact_index.json
selected_implementations.json
controller_strategy_log.json        # if controller used
extraction_report.json              # if extraction attempted
provider_run_manifest.json          # if geometry.solve used
trace_compilation_result.json       # if trace attempted
construction_compilation_result.json# if construction attempted
final_verify_report.json            # if final verification attempted
resource_usage_report_*.json        # if external process/model/Lean build used
```

Metrics must be derived from these files. Hard-coded formulas based only on corpus category labels are forbidden.

## 7. Provider module layout requirement

### R-REFACTOR-010 — Provider implementation layout

`plugins/geometry_synthetic/provider.py` may remain as a backward-compatible facade only. It must not contain implementation classes for Newclid, GenesisGeo, TongGeometry, composite provider orchestration, or provider manifests.

Required layout:

```text
plugins/geometry_synthetic/providers/provider_api.py
plugins/geometry_synthetic/providers/composite_provider.py
plugins/geometry_synthetic/providers/provider_run_manifest.py
plugins/geometry_synthetic/providers/newclid_adapter.py
plugins/geometry_synthetic/providers/genesisgeo_adapter.py
plugins/geometry_synthetic/providers/tonggeometry_adapter.py
```

Allowed facade content in `provider.py`:

```python
from plugins.geometry_synthetic.providers.composite_provider import CompositeSyntheticGeometryProvider
from plugins.geometry_synthetic.providers.provider_run_manifest import ProviderRunManifest
```

Release acceptance must fail if `provider.py` defines classes matching:

```text
Newclid*Adapter
GenesisGeo*Adapter
TongGeometry*Adapter
CompositeSyntheticGeometryProvider*
ProviderRunManifest
```

## 8. Release blocker additions

Append the following blockers to Base Spec Section 20.

```text
26. Dependency report lacks code/model artifact status split or claim-impact classification.
27. TongGeometry model checkpoint is missing but not classified as either available or admitted_unavailable_external_artifact.
28. TongGeometry model-backed claim is made without tokenizer/lm_s/lm_l/cls and model_inference_status=available.
29. Level2 pilot corpus fails the nontrivial corpus floor.
30. Release matrix metrics are not artifact-derived from per-task runs.
31. Release matrix uses run_fixture/build_fixture_run or local toy geometry standard loop.
32. StandardGeometryProofLoop release path cannot run real benchmark tasks.
33. Provider implementation remains monolithic in provider.py instead of providers/** with facade-only provider.py.
34. Release acceptance lacks checks for blockers 26–33.
```

## 9. Required new checker scripts

The final repo must include and wire into release acceptance:

```text
scripts/check_dependency_claim_profile.py
scripts/check_dependency_report_model_status.py
scripts/check_level2_corpus_nontrivial.py
scripts/check_matrix_artifact_derived.py
scripts/check_no_fixture_standard_loop_release.py
scripts/check_provider_layout.py
```

Each script must return nonzero on violation and must be called by `scripts/check_release_acceptance.py`.

## 10. Closure claims after this patch

Allowed closure claims:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

only if all original Base Spec release blockers and patch blockers 26–34 pass.

Allowed additional claim:

```text
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY
```

only if all four TongGeometry model artifact paths exist, aggregate checkpoint hash is non-null, and model inference smoke passes.

If patch blockers pass except TongGeometry model-backed readiness, closure must explicitly say:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked by unavailable TongGeometry checkpoint artifacts
```
