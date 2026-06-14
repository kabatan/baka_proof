---
title: "Guardian Base Spec Patch — geometry × Lean v0.3B solver-backed proof repair"
patch_id: "MARP-GEOLEAN-BASE-004B"
base_spec: "MARP-GEOLEAN-BASE-004"
prior_patches:
  - "MARP-GEOLEAN-BASE-004A"
status: "USER_APPROVED_ACTIVE_AMENDMENT"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
installed: "2026-06-14"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md"
lane: "Guardian Lane"
---

# Guardian Base Spec Patch — geometry × Lean v0.3B solver-backed proof repair

## 0. Authority

After user approval, this patch amends:

```text
MARP-GEOLEAN-BASE-004
MARP-GEOLEAN-BASE-004A
```

It does not replace the full Base Spec. It supersedes only the clauses explicitly listed below.

If this patch conflicts with BASE-004 or BASE-004A, this patch wins for the patched R-IDs, claim profiles, release blockers, and proof-repair requirements.

Codex must not implement a shortcut that merely passes the existing v0.3A release checker while leaving provider-backed geometry tasks as diagnostic-only. This patch exists because v0.3A deliberately prevented provider-backed geometry tasks from being counted as final theorem success. That safety restriction is now replaced by a stricter positive requirement: solver-backed geometry artifacts must be able to drive Lean proof repair and pass FinalVerifyGate.

## 1. Purpose

The current v0.3A state is allowed to claim:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked
```

However, in the current design, geometry provider-backed tasks are intentionally prevented from being counted as final theorem success. This makes the system experiment-ready as a harness but not yet a solver-backed proof-repair pipeline.

This patch defines the next required claim:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
```

The goal is not broad geometry automation. The goal is a narrow, explicit, non-ambiguous proof-use path:

```text
LeanGeoSubsetV1 problem theorem
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> real Newclid-compatible GeoTraceV1
      or real GenesisGeo-compatible AuxiliaryConstructionCandidateV1
  -> TraceCompiler or ConstructionCompiler
  -> concrete LeanPatchCandidateV1
  -> ProofWorkerPlugin applies the patch to an admitted generated proof file
  -> FinalVerifyGate verifies the patched theorem
  -> SolverBackedProofCertificate records solver-backed attribution
  -> TaskRunResult.proof_use_status = final_theorem
```

TongGeometry model-backed heavy search remains out of scope for this patch. TongGeometry may continue as code-backed diagnostic heavy_search. This patch must not reintroduce a requirement for unavailable TongGeometry trained checkpoints.

## 2. Claim profiles

### R-CLAIM-010 — New claim profile

Add the following claim profile:

```yaml
ClaimProfiles:
  V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY:
    meaning: >
      The repo can run and replay a non-fixture LeanGeoSubsetV1 benchmark slice
      in which normalized geometry solver artifacts are compiled into Lean proof
      patches, applied by the proof worker, and admitted as final theorem evidence
      by FinalVerifyGate.
    requires_tonggeometry_model_checkpoint: false
    requires_real_newclid: true
    requires_real_genesisgeo: true
    requires_solver_backed_final_theorem_successes: true
    allows_tonggeometry_model_artifact_status:
      - available
      - admitted_unavailable_external_artifact
```

### R-CLAIM-011 — Updated completion meaning

After this patch is approved, a future closure may claim:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
```

only if it also reports the status of:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
```

Allowed combinations:

```yaml
allowed_closure_profiles:
  - core_experiment_ready: passed
    solver_backed_proof_repair: passed
    tonggeometry_model_backed: blocked
    claim_ceiling: "v0_3b_solver_backed_ready_no_tong_model_backed_claim"

  - core_experiment_ready: passed
    solver_backed_proof_repair: blocked
    tonggeometry_model_backed: blocked
    claim_ceiling: "v0_3a_harness_ready_but_solver_backed_proof_repair_blocked"
```

The second profile is not final for v0.3B.

## 3. Non-negotiable v0.3B invariants

### INV-B001 — Solver-backed final theorem is allowed but only through the strict path

BASE-004A prevented provider tasks from claiming final theorem status. Replace that blanket prohibition with this rule:

```text
Provider-backed geometry tasks may produce proof_use_status = final_theorem
only if SolverBackedProofCertificate.status = passed and FinalVerifyGate.proof_use_status = final_theorem.
```

A provider-backed task without a valid `SolverBackedProofCertificate` remains `not_allowed`.

### INV-B002 — FinalVerifyGate remains the only final theorem authority

Solver-backed attribution does not replace Lean final verification.

```text
GeoTraceV1, AuxiliaryConstructionCandidateV1, TraceCompilationResult,
ConstructionCompilationResult, LeanPatchCandidateV1, WorkerResult,
and SolverBackedProofCertificate are not final theorem evidence alone.
```

Only `FinalVerifyGate` may emit:

```text
result_level = lean_theorem
proof_use_status = final_theorem
```

### INV-B003 — Raw provider output is still never proof

Raw Newclid / GenesisGeo / TongGeometry output remains non-proof. v0.3B admits only normalized solver artifacts that pass compilers and FinalVerifyGate.

### INV-B004 — The proof patch must be concrete and replayable

A compiler result that only stores an abstract reference such as `lean_patch_candidate_ref = "patch:..."` is insufficient.

A proof-use compiler result must contain or reference a content-addressed `LeanPatchCandidateV1` with concrete patch material.

### INV-B005 — Original already-proved theorem cannot count as solver-backed success

A task must not be counted as solver-backed final theorem if:

```text
1. the original problem source already compiles without repair; and
2. no proof-region diff is applied; or
3. the final proof has no SolverBackedProofCertificate linking it to normalized solver artifacts.
```

Existing fully proved smoke theorems may remain for unit tests and lean-build, but they must not satisfy the v0.3B solver-backed proof-repair floor.

### INV-B006 — Solver-backed proof-repair tasks use problem sources, not ordinary built examples

Release solver-backed tasks must use admitted problem sources with protected theorem statements and repairable proof regions.

Allowed problem-source pattern:

```lean
import LeanGeo.Abbre

open LeanGeo
namespace MathAutoResearch.SolverBackedProblems

theorem task_name ... : TARGET := by
  -- MARP_PROOF_REGION_START:task_name
  sorry
  -- MARP_PROOF_REGION_END:task_name

end MathAutoResearch.SolverBackedProblems
```

These problem-source files may contain `sorry` and must not be imported by the normal `lake build` target. They are inputs to the proof-repair pipeline, not closure artifacts.

Generated solved files must contain no `sorry` and must pass FinalVerifyGate.

## 4. Required records

### R-SCHEMA-B001 — LeanPatchCandidateV1

Add a geometry schema and implementation for:

```yaml
LeanPatchCandidateV1:
  schema_version: "1.0.0"
  patch_id: "lean_patch:<hash>"
  source_task_run_id: "task_run:..."
  target_theorem_name: "..."
  target_file_path: "..."
  target_protected_statement_hash: "sha256:..."
  patch_kind: "replace_proof_region | add_helper_lemma_and_replace_proof_region"
  allowed_edit_region:
    region_id: "..."
    start_marker: "-- MARP_PROOF_REGION_START:<theorem>"
    end_marker: "-- MARP_PROOF_REGION_END:<theorem>"
  required_imports: []
  helper_lemmas:
    - name: "optional"
      text_ref: "sha256:..."
      proof_origin: "trace_compiler | construction_compiler | proof_worker"
  proof_region_replacement:
    text_ref: "sha256:..."
    text_hash: "sha256:..."
  solver_dependency_refs:
    - "provider_run_manifest:<hash>"
    - "geotrace:<hash> | aux_construction_candidate:<hash>"
    - "trace_compilation:<hash> | construction_compilation:<hash>"
  proof_template_id: "..."
  proof_origin: "trace_compiler | construction_compiler | hybrid"
  raw_provider_output_used_as_proof: false
  created_by: "TraceCompiler | ConstructionCompiler"
```

Requirements:

```text
1. Unknown fields are rejected.
2. patch_id is deterministic from theorem statement hash + proof replacement hash + solver_dependency_refs.
3. proof_region_replacement.text_ref must be content-addressed.
4. solver_dependency_refs must include at least one normalized solver artifact and the provider manifest.
5. raw provider output cannot appear in proof_region_replacement unless quoted only in comments and proof_use_status remains not_allowed.
```

### R-SCHEMA-B002 — SolverBackedProofCertificate

Add a geometry/evaluation schema and implementation for:

```yaml
SolverBackedProofCertificate:
  schema_version: "1.0.0"
  certificate_id: "solver_backed_proof:<hash>"
  task_run_id: "task_run:..."
  benchmark_entry_id: "..."
  baseline_id: "B2 | B4 | other"
  source_problem_ref: "sha256:..."
  generated_candidate_file_ref: "sha256:..."
  theorem_name: "..."
  protected_statement_hash: "sha256:..."

  extraction_report_ref: "geometry_extraction:<hash>"
  goal_anchor_ref: "goal:<hash>"
  provider_run_manifest_ref: "provider_run_manifest:<hash>"

  normalized_solver_artifact:
    kind: "geotrace | auxiliary_construction | hybrid"
    ref: "geotrace:<hash> | aux_construction_candidate:<hash>"
    source_engine_role: "symbolic_closure | construction_proposer | heavy_search"

  compiler_result_ref: "trace_compilation:<hash> | construction_compilation:<hash>"
  lean_patch_candidate_ref: "lean_patch:<hash>"
  worker_result_ref: "worker_result:<hash>"
  final_verify_report_ref: "final_verify:<hash>"

  proof_region_diff_hash: "sha256:..."
  solver_dependency_status: "passed | failed"
  theorem_hash_unchanged: true
  no_sorry: true
  no_forbidden_axioms: true
  final_verify_status: "final_theorem"
  status: "passed | failed"
  failure_reason: null
```

A task may claim `solver_backed_final_theorem = true` only if this certificate has `status = passed`.

### R-SCHEMA-B003 — TaskRunResult extensions

Patch `TaskRunResult` to include:

```yaml
TaskRunResult:
  solver_backed_final_theorem: true | false
  solver_backed_proof_certificate_ref: "solver_backed_proof:<hash> | null"
  proof_repair_patch_applied: true | false
  proof_region_diff_hash: "sha256:... | null"
  generated_candidate_file_ref: "sha256:... | null"
  solver_dependency_kind: "none | geotrace | auxiliary_construction | hybrid"
  original_problem_compile_status: "passed | failed | skipped_problem_source"
  final_verify_report_ref: "final_verify:<hash> | null"
```

### R-SCHEMA-B004 — FinalVerifyReport extensions

Patch `FinalVerifyReport` to include or guarantee equivalent fields:

```yaml
FinalVerifyReport:
  proof_use_provenance_status: "passed | failed"
  solver_backed_proof_status: "not_applicable | passed | failed"
  protected_statement_hash_source: "source_problem | original_file | generated_file"
  checked_candidate_file_ref: "sha256:..."
  proof_region_guard_status: "passed | failed"
```

## 5. Compiler requirements

### R-COMPILER-B001 — TraceCompiler must emit concrete LeanPatchCandidateV1

For supported `GeoTraceV1` steps, TraceCompiler must produce:

```text
TraceCompilationResult.status = compiled
TraceCompilationResult.lean_patch_candidate_ref != null
TraceCompilationResult.lean_patch_candidate.kind = LeanPatchCandidateV1
```

Minimum supported v0.3B trace-to-Lean templates:

```yaml
TraceToLeanTemplateFloor:
  - template_id: "trace.coll_self_left.v1"
    target_shape: "Coll A A B"
    expected_proof_contains:
      - "simp [Coll]"
    required_solver_artifact: "GeoTraceV1"
  - template_id: "trace.coll_self_right.v1"
    target_shape: "Coll A B B"
    expected_proof_contains:
      - "simp [Coll]"
    required_solver_artifact: "GeoTraceV1"
  - template_id: "trace.collinear_or_left.v1"
    target_shape: "P ∨ Q"
    expected_proof_contains:
      - "Or.inl"
    required_solver_artifact: "GeoTraceV1"
  - template_id: "trace.collinear_and_intro.v1"
    target_shape: "P ∧ Q"
    expected_proof_contains:
      - "And.intro"
    required_solver_artifact: "GeoTraceV1"
```

These are intentionally narrow. They are enough to prove the wiring from solver trace to Lean proof patch. They are not a claim of broad Newclid trace translation.

### R-COMPILER-B002 — ConstructionCompiler must emit concrete LeanPatchCandidateV1

For supported `AuxiliaryConstructionCandidateV1`, ConstructionCompiler must produce concrete proof patches.

Minimum supported v0.3B construction-to-Lean templates:

```yaml
ConstructionToLeanTemplateFloor:
  - template_id: "construction.exists_existing_line_witness.v1"
    target_shape: "∃ M : Line, A.onLine M"
    proof_pattern: "exact ⟨L, h⟩"
    required_solver_artifact: "AuxiliaryConstructionCandidateV1"
  - template_id: "construction.distinct_points_on_line_pack.v1"
    target_shape: "distinctPointsOnLine A B L"
    proof_pattern: "And.intro hA (And.intro hB hne)"
    required_solver_artifact: "AuxiliaryConstructionCandidateV1"
  - template_id: "construction.exists_point_collinear_self.v1"
    target_shape: "∃ P : Point, Coll P A A"
    proof_pattern: "exact ⟨A, by simp [Coll]⟩"
    required_solver_artifact: "AuxiliaryConstructionCandidateV1"
```

If a construction candidate does not match a supported template, ConstructionCompiler must produce a blocker, not a proof success.

### R-COMPILER-B003 — Compiler output must be differentiated from proof evidence

`TraceCompilationResult` and `ConstructionCompilationResult` remain `lean_patch_candidate`, not final theorem. They may be proof-use dependencies only after ProofWorker and FinalVerifyGate.

## 6. ProofWorker requirements

### R-WORKER-B001 — ProofWorker applies compiler patch

ProofWorker must implement:

```python
apply_lean_patch_candidate(
    source_problem_path: Path,
    patch_candidate: LeanPatchCandidateV1,
    output_dir: Path,
    context: RunContext,
) -> WorkerResult
```

Required behavior:

```text
1. read source_problem_path.
2. locate exact MARP_PROOF_REGION_START/END markers for target theorem.
3. replace only the admitted proof region.
4. add helper lemmas only under admitted generated helper region or generated file.
5. write generated candidate file under:
   lean/MathAutoResearch/Geometry/Generated/<run_id>/<task_id>.lean
   or an equivalent run artifact directory.
6. record proof_region_diff_hash.
7. record solver_dependency_refs.
8. set WorkerResult.status = patch_applied only after file write and region guard pass.
```

ProofWorker must not edit the original problem source in place.

### R-WORKER-B002 — ProofWorker cannot self-claim final theorem

WorkerResult may say `patch_applied`. It may not set `proof_use_status = final_theorem`.

## 7. FinalVerifyGate and trust requirements

### R-FINAL-B001 — FinalVerifyGate must verify generated candidate file

For solver-backed proof repair, FinalVerifyGate must compare:

```text
source problem theorem statement
generated candidate theorem statement
```

and must accept only if:

```text
1. protected theorem statement hash unchanged.
2. candidate file compiles.
3. no sorry in candidate file.
4. no forbidden axiom/admit/unsafe.
5. proof region guard passed.
6. admitted imports only.
7. proof_use_provenance contains:
   - GeometryExtractionReport
   - GoalAnchor
   - protected_statement_hash
   - TargetLibraryManifest
   - ProviderRunManifest
   - normalized solver artifact ref
   - TraceCompilationResult or ConstructionCompilationResult
   - LeanPatchCandidateV1
   - WorkerResult
```

### R-TRUST-B001 — SolverBackedProofCertificate generation

After FinalVerifyGate passes, the standard loop must generate `SolverBackedProofCertificate`.

TrustGuard may allow a provider-backed task to close with `proof_use_status = final_theorem` only if:

```text
FinalVerifyReport.proof_use_status = final_theorem
SolverBackedProofCertificate.status = passed
```

### R-TRUST-B002 — No raw-output laundering

Release acceptance must fail if a task has `solver_backed_final_theorem=true` but any of the following is true:

```text
1. normalized solver artifact missing.
2. compiler result missing.
3. LeanPatchCandidateV1 missing.
4. WorkerResult.patch_applied is false.
5. FinalVerifyReport missing.
6. SolverBackedProofCertificate missing.
7. provider raw output is the only solver reference.
8. source problem theorem statement changed.
```

## 8. Corpus requirements

### R-EVAL-B001 — SolverBackedProofRepairCorpus

Add a release corpus:

```text
benchmarks/geometry/solver_backed_proof_repair.jsonl
```

and source problem files under:

```text
benchmarks/leangeo/SolverBackedProblems/*.lean
```

Minimum corpus floor:

```yaml
SolverBackedProofRepairCorpusFloor:
  total_tasks_min: 10

  geotrace_to_lean_tasks_min: 6
  construction_to_lean_tasks_min: 3
  hybrid_or_side_condition_task_min: 1

  each_task_requires:
    - entry_id
    - theorem_file_path
    - theorem_name
    - target_library = "LeanGeoSubsetV1:1.0.0"
    - task_category:
        "solver_backed_geotrace_final"
        "solver_backed_construction_final"
        "solver_backed_hybrid_or_side_condition"
    - source_problem_kind = "repairable_problem_source"
    - source_lean_mode = "real_leangeo_dependency"
    - starts_with_unproved_region = true
    - expected_solver_dependency_kind = "geotrace | auxiliary_construction | hybrid"
    - expected_required_stages includes:
        "extraction"
        "provider"
        "compiler"
        "proof_worker_patch"
        "final_verify"
        "solver_backed_proof_certificate"
```

Forbidden:

```text
1. task source has a complete proof outside admitted proof region.
2. task source defines toy Point/Coll/Line semantics.
3. task is counted as solver-backed if it is solved by verifying the original file unchanged.
4. task is counted as solver-backed if B0/B1 solves it but B2 never applies a solver patch.
```

### R-EVAL-B002 — Updated Level2 pilot

The existing `GeometryLevel2PilotCorpus` may remain. However, after this patch the release matrix must also include the solver-backed proof-repair corpus or a superset of it.

## 9. Evaluation requirements

### R-EVAL-B010 — New metrics

Add required metrics:

```text
solver_backed_final_theorem_count
solver_backed_final_theorem_rate
solver_backed_geotrace_final_count
solver_backed_construction_final_count
proof_repair_patch_applied_count
lean_patch_candidate_count
solver_backed_certificate_count
solver_backed_final_verify_failure_count
solver_backed_blocker_kind_counts
```

### R-EVAL-B011 — Minimum acceptance floor

Release acceptance for v0.3B must fail unless:

```yaml
minimum_solver_backed_acceptance:
  B2_full_geometry_enabled:
    solver_backed_final_theorem_count_min: 8
    geotrace_solver_backed_final_theorem_count_min: 5
    construction_solver_backed_final_theorem_count_min: 2

  B4_lower_model_geometry_enabled:
    solver_backed_final_theorem_count_min: 5

  all_solver_backed_successes:
    final_verify_report_required: true
    solver_backed_proof_certificate_required: true
    proof_region_diff_hash_required: true
    source_problem_ref_required: true
```

These floors are not an advantage claim. They only establish that the solver-backed proof-repair path works.

### R-EVAL-B012 — B0/B1/B3 interpretation

B0/B1/B3 may solve some tasks without geometry.solve. That is allowed. However, they must not contribute to `solver_backed_final_theorem_count` unless they use the strict solver-backed chain. Usually they will have zero solver-backed successes.

## 10. Standard loop patch

### R-LOOP-B001 — Replace diagnostic-only provider handling

Patch `StandardGeometryProofLoop.run_task` so that provider-backed geometry tasks are no longer automatically blocked after FinalVerifyGate.

Old behavior to remove:

```text
if geometry_stage_required and final_verify_status == "final_theorem" and chain_satisfied:
    blockers.append("geometry_chain_diagnostic_only_no_proof_repair_claim")
```

New behavior:

```text
if geometry_stage_required:
    if final_verify_status == "final_theorem" and solver_backed_certificate.status == "passed":
        proof_use_status = "final_theorem"
        solver_backed_final_theorem = true
        status = "verified"
    else:
        proof_use_status = "not_allowed"
        solver_backed_final_theorem = false
        status = "blocked"
```

### R-LOOP-B002 — Real proof repair path

`run_task` must do the following for solver-backed tasks:

```text
1. read source problem file with proof-region markers.
2. create GoalAnchor from protected theorem statement.
3. run extraction.
4. call provider if geometry enabled and expected.
5. compile normalized artifact into LeanPatchCandidateV1.
6. call ProofWorker to apply the patch.
7. run FinalVerifyGate on generated candidate file.
8. create SolverBackedProofCertificate if FinalVerifyGate passes.
9. set TaskRunResult.solver_backed_final_theorem accordingly.
10. write all artifacts into the per-task artifact index.
```

### R-LOOP-B003 — Existing run_fixture remains test-only

`run_fixture()` may remain, but release matrix and v0.3B acceptance must fail if `run_fixture()` or `GEOMETRY_FINAL_VERIFY_FIXTURE` is used by any release run.

## 11. Release blockers

Append these blockers after BASE-004A blocker 34.

```text
35. LeanPatchCandidateV1 schema or concrete patch material missing.
36. SolverBackedProofCertificate schema missing.
37. TraceCompiler or ConstructionCompiler does not emit concrete LeanPatchCandidateV1.
38. ProofWorker does not apply solver-produced patch to an admitted generated candidate file.
39. FinalVerifyGate does not validate solver-backed provenance.
40. StandardGeometryProofLoop still blocks provider-backed final theorem success unconditionally.
41. SolverBackedProofRepairCorpus missing or below floor.
42. B2 solver_backed_final_theorem_count below floor.
43. B4 solver_backed_final_theorem_count below floor.
44. solver-backed success lacks proof_region_diff_hash, final_verify_report, or solver_backed_certificate.
45. release metrics count original already-proved theorem as solver-backed final theorem.
46. release matrix uses run_fixture or toy geometry path for solver-backed proof repair.
47. release acceptance lacks checks for blockers 35–46.
```

## 12. Required checker scripts

Add and wire into release acceptance:

```text
scripts/check_solver_backed_patch_schema.py
scripts/check_solver_backed_corpus.py
scripts/check_solver_backed_artifacts.py
scripts/check_solver_backed_metrics.py
scripts/check_no_original_proof_counted_as_solver_backed.py
scripts/check_no_fixture_solver_backed_release.py
```

Each script must return nonzero on violation and must be called by `scripts/check_release_acceptance.py`.

## 13. Closure claims after this patch

Allowed only if all original blockers, v0.3A blockers, and v0.3B blockers pass:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
```

A valid closure after this patch must report:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked or passed
```

If TongGeometry model artifacts remain unavailable, the correct closure is:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked by unavailable TongGeometry checkpoint artifacts
```

## 14. Explicit non-goals

This patch does not require:

```text
1. arbitrary Newclid trace translation.
2. arbitrary GenesisGeo construction translation.
3. TongGeometry model-backed inference.
4. positive Level2 advantage.
5. arbitrary LeanGeo theorem support.
6. natural-language to Lean formalization.
7. open-problem solving.
```

It requires only the narrow but decisive proof-use capability that was missing from v0.3A: normalized solver artifacts can become concrete Lean proof repairs that FinalVerifyGate accepts and the run matrix counts as solver-backed final theorem success.
