---
title: v0.3B proof-repair gap audit
task: T48
status: COMPLETE
created: 2026-06-14
authority: Evidence record only; does not implement v0.3B and does not mark R-IDs VERIFIED.
---

# v0.3B Proof-Repair Gap Audit

## Scope

This audit records the current repository gaps against:

```text
MARP-GEOLEAN-BASE-004B
MARP-GEOLEAN-PLAN-004B
MARP-GEOLEAN-ACCEPTANCE-004B
```

T47 installed the v0.3B authority documents. T48 is evidence-only. No
implementation code is changed by this audit.

## Current Summary

The repository is ready to begin v0.3B implementation, but the solver-backed
proof-repair path is not implemented.

Current status:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: v0.3A harness-ready/core experiment-ready passed, v0.3B solver-backed proof repair pending
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: not claimed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked
```

## 1. Provider-Backed Final Theorem Block

File:

```text
plugins/geometry_synthetic/standard_loop.py
```

Current behavior:

```python
if geometry_stage_required and final_verify_status == "final_theorem" and chain_satisfied:
    blockers.append("geometry_chain_diagnostic_only_no_proof_repair_claim")
```

This was valid for v0.3A safety hardening, but it is the direct blocker for
`R-LOOP-B001`. Provider-backed geometry tasks cannot become final theorem
successes even when provider, compiler, worker placeholder, and FinalVerifyGate
artifacts exist.

Required v0.3B change:

```text
StandardGeometryProofLoop.run_task must allow proof_use_status=final_theorem
only when FinalVerifyGate passes and SolverBackedProofCertificate.status=passed.
```

## 2. TaskRunResult Fields

File:

```text
plugins/geometry_synthetic/standard_loop.py
```

Current `TaskRunResult` fields:

```text
schema_version
run_id
task_entry_id
baseline_id
status
theorem_file_path
theorem_name
stage_statuses
artifact_index
blockers
proof_use_status
```

Missing v0.3B fields from `R-SCHEMA-B003`:

```text
solver_backed_final_theorem
solver_backed_proof_certificate_ref
proof_repair_patch_applied
proof_region_diff_hash
generated_candidate_file_ref
solver_dependency_kind
original_problem_compile_status
final_verify_report_ref
```

## 3. LeanPatchCandidateV1 Schema Missing

Expected files from `R-SCHEMA-B001`:

```text
plugins/geometry_synthetic/patching/lean_patch_candidate_v1.py
schemas/geometry/lean_patch_candidate_v1.schema.json
```

Current state:

```text
missing
```

Current compiler results contain only:

```text
lean_patch_candidate_ref
lean_patch
```

They do not contain or reference a content-addressed `LeanPatchCandidateV1`
record with protected theorem hash, proof-region replacement, allowed edit
region, deterministic patch id, and solver dependency refs.

## 4. SolverBackedProofCertificate Schema Missing

Expected files from `R-SCHEMA-B002`:

```text
plugins/geometry_synthetic/proof/solver_backed_proof_certificate.py
schemas/geometry/solver_backed_proof_certificate.schema.json
```

Current state:

```text
missing
```

No artifact named `solver_backed_proof_certificate.json` is emitted by the
standard loop, and TrustGuard has no certificate-based provider-backed final
theorem path.

## 5. TraceCompiler Gap

File:

```text
plugins/geometry_synthetic/trace_compiler.py
```

Current behavior:

```text
TraceCompilationResult.status = compiled
TraceCompilationResult.lean_patch_candidate_ref = lean_patch_candidate:<hash>
TraceCompilationResult.lean_patch = fixture theorem text
```

Current `_lean_patch_for_trace` emits a standalone fixture namespace theorem:

```text
MathAutoResearch.GeometryTraceFixture.compiled_trace_fixture
```

Gap:

```text
TraceCompiler does not emit a concrete LeanPatchCandidateV1 targeted at a
source problem proof region. It also does not implement the v0.3B template floor:
trace.coll_self_left.v1, trace.coll_self_right.v1,
trace.collinear_or_left.v1, trace.collinear_and_intro.v1.
```

## 6. ConstructionCompiler Gap

File:

```text
plugins/geometry_synthetic/construction/__init__.py
```

Current behavior:

```text
ConstructionCompilationResult.status = compiled
ConstructionCompilationResult.lean_patch_candidate_ref = lean_patch_candidate:<hash>
ConstructionCompilationResult.lean_patch = fixture theorem text
```

Current `_lean_patch_for_candidate` emits a standalone fixture namespace theorem:

```text
MathAutoResearch.GeometryConstructionFixture.compiled_construction_fixture
```

Gap:

```text
ConstructionCompiler does not emit a concrete LeanPatchCandidateV1 targeted at
a source problem proof region. It also does not implement the v0.3B construction
template floor:
construction.exists_existing_line_witness.v1,
construction.distinct_points_on_line_pack.v1,
construction.exists_point_collinear_self.v1.
```

## 7. ProofWorker Gap

File:

```text
src/math_auto_research/model_api/proof_worker.py
```

Current behavior:

```text
DummyProofWorker.execute_work_order returns WorkerResult(status="patch_candidate")
WorkerResult cannot claim final theorem
```

This preserves the v0.3A safety boundary, but v0.3B requires:

```text
apply_lean_patch_candidate(source_problem_path, patch_candidate, output_dir, context)
```

Missing:

```text
proof-region marker parsing
source problem read
generated candidate file write
proof_region_diff_hash
generated_candidate_file_ref
solver_dependency_refs
patch_applied status
guard that original source is never edited in place
```

## 8. FinalVerifyGate Gap

File:

```text
src/math_auto_research/lean_integration/final_verify_gate.py
```

Current `FinalVerifyReport` fields:

```text
schema_version
report_id
target_obligation_id
theorem_statement_hash
protected_theorem_hash_unchanged
lean_status
forbidden_axiom_status
sorry_status
proof_use_status
lean_artifact_ref
proof_artifact_ref
```

Current provenance validation requires only:

```text
geometry_extraction_report_ref
goal_anchor_ref
protected_statement_hash
target_library_manifest_hash
```

Missing v0.3B fields/requirements:

```text
proof_use_provenance_status
solver_backed_proof_status
protected_statement_hash_source
checked_candidate_file_ref
proof_region_guard_status
provider manifest provenance
normalized solver artifact provenance
compiler result provenance
LeanPatchCandidateV1 provenance
WorkerResult provenance
solver-backed mode rejection on missing provenance
```

## 9. Corpus and Problem Source Gap

Expected files:

```text
benchmarks/geometry/solver_backed_proof_repair.jsonl
benchmarks/leangeo/SolverBackedProblems/README.md
benchmarks/leangeo/SolverBackedProblems/SolverBackedProofRepair.lean
configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
```

Current state:

```text
missing
```

Existing corpus files:

```text
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/leangeo/RealSmokeCorpus.lean
```

These are not the v0.3B `SolverBackedProofRepairCorpus` and do not satisfy the
10-task floor with repairable proof-region source files.

## 10. Evaluation and Metrics Gap

File:

```text
plugins/geometry_synthetic/evaluation.py
```

Current metrics include:

```text
final_theorem_count
proof_repair_success_count
trace_compile_success_count
construction_candidate_accepted_count
provider_success_rate_by_role
```

Missing v0.3B metrics:

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

Current matrix config validation is specific to B0-B5 and existing Level2 pilot
or ablation configs. It does not recognize
`geometry_solver_backed_proof_repair.yaml`.

## 11. Checker Script Gap

Required v0.3B scripts are missing:

```text
scripts/check_solver_backed_patch_schema.py
scripts/check_solver_backed_corpus.py
scripts/check_solver_backed_artifacts.py
scripts/check_solver_backed_metrics.py
scripts/check_no_original_proof_counted_as_solver_backed.py
scripts/check_no_fixture_solver_backed_release.py
```

Existing `scripts/check_matrix_artifact_derived.py` currently enforces a v0.3A
rule that B2/B4 provider-backed final theorem claims are errors:

```text
provider_task_claimed_final_theorem_in_release
```

This must be superseded or scoped so that v0.3B accepts provider-backed final
theorem only through SolverBackedProofCertificate.

## 12. Release Acceptance Gap

File:

```text
src/math_auto_research/workflow/release_acceptance.py
```

Current release acceptance:

```text
checks blockers 1-34
does not emit solver_backed_proof_repair_status
does not emit solver_backed_summary
does not check blockers 35-47
claim_ceiling remains core_experiment_ready_passed_no_tong_model_backed_claim
```

Required v0.3B behavior:

```text
checks blockers 1-47
emits solver_backed_proof_repair_status
blocks V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY until solver-backed floors pass
emits v0_3b_solver_backed_ready_no_tong_model_backed_claim when core and solver-backed pass while Tong model remains blocked
```

## 13. Release Fixture Risk

Current release standard loop uses real provider paths for v0.3A, but the codebase
still contains fixture-only helpers:

```text
StandardGeometryProofLoop.run_fixture
GEOMETRY_FINAL_VERIFY_FIXTURE
scripts/smoke_geometry_final_verify.py
```

v0.3B must retain these for tests only and must fail release if `run_fixture`,
`GEOMETRY_FINAL_VERIFY_FIXTURE`, or toy geometry definitions are used in the
solver-backed release path.

## 14. Task Mapping

| Gap | Plan task |
|---|---|
| LeanPatchCandidateV1 and SolverBackedProofCertificate missing | T49 |
| Problem-source proof-region guard missing | T50 |
| TraceCompiler concrete patch emission missing | T51 |
| ConstructionCompiler concrete patch emission missing | T52 |
| Compiler outputs not separated from proof evidence strongly enough | T53 |
| ProofWorker patch application missing | T54 |
| FinalVerifyGate solver-backed provenance missing | T55 |
| Certificate generation and TrustGuard integration missing | T56 |
| Standard loop remains diagnostic-only for provider-backed final theorem | T57 |
| Solver-backed corpus/config missing | T58 |
| Solver-backed metrics missing | T59 |
| Solver-backed checker scripts missing | T60 |
| Release acceptance blockers 35-47 missing | T61 |
| Focused smoke/mutation surfaces missing | T62 |
| Full v0.3B command pass and final closure missing | T63-T64 |

## T48 Conclusion

The current repo is correctly positioned for v0.3B implementation to begin at
T49 after this audit. The primary implementation risk is to accidentally relax
the v0.3A safety ban by counting provider artifacts directly. The required
solution is the stricter v0.3B chain:

```text
normalized solver artifact
  -> concrete LeanPatchCandidateV1
  -> ProofWorker patch_applied
  -> FinalVerifyGate final_theorem
  -> SolverBackedProofCertificate passed
  -> TaskRunResult.proof_use_status = final_theorem
```
