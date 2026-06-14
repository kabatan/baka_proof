---
title: "Guardian Plan Patch — geometry × Lean v0.3B solver-backed proof repair"
plan_patch_id: "MARP-GEOLEAN-PLAN-004B"
base_patch: "MARP-GEOLEAN-BASE-004B"
base_spec: "MARP-GEOLEAN-BASE-004"
prior_plan: "MARP-GEOLEAN-PLAN-004"
prior_patches:
  - "MARP-GEOLEAN-PLAN-004A"
status: "USER_APPROVED_ACTIVE_AMENDMENT"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
installed: "2026-06-14"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md"
---

# Guardian Plan Patch — geometry × Lean v0.3B solver-backed proof repair

## 0. Plan authority

This Plan Patch defines how Codex must implement `MARP-GEOLEAN-BASE-004B`.

The Base Spec and Base Spec Patch win over this Plan Patch if there is a conflict. This Plan Patch must not weaken requirements. It is intentionally explicit so that Codex can implement without inventing a simpler architecture.

Implementation must not start until the user approves:

```text
MARP-GEOLEAN-BASE-004B
MARP-GEOLEAN-PLAN-004B
MARP-GEOLEAN-ACCEPTANCE-004B
```

## 1. Current-state diagnosis that this patch fixes

The current repo state is acceptable as v0.3A core experiment-ready but not acceptable as solver-backed proof repair.

Codex must treat the following current behavior as a defect for v0.3B:

```text
1. Provider-backed geometry tasks are not allowed to become final theorem success.
2. The release matrix can exercise providers and compilers without counting solver-backed final theorem successes.
3. Existing final theorem successes mostly come from proof-worker-only or already-proved Lean files.
4. StandardGeometryProofLoop contains release behavior that keeps provider chains diagnostic-only.
```

The desired v0.3B state is:

```text
A provider-backed geometry task can be final_theorem
iff
  normalized solver artifact
  + compiler-generated concrete Lean patch
  + ProofWorker patch application
  + FinalVerifyGate
  + SolverBackedProofCertificate
all pass.
```

TongGeometry trained model artifacts remain out of scope for this patch.

## 2. Global stop conditions

Codex must stop and report instead of continuing if it needs to:

```text
1. weaken any BASE-004B R-ID.
2. count raw provider output as proof.
3. count a task as solver-backed without SolverBackedProofCertificate.
4. count the unchanged original theorem as solver-backed final theorem.
5. modify protected theorem statements.
6. use local toy Point/Coll/Line definitions in release solver-backed corpus.
7. remove FinalVerifyGate from the proof-use path.
8. reintroduce the v0.3A blanket ban by keeping provider-backed tasks unable to reach final_theorem.
9. make TongGeometry model-backed inference a required blocker for this patch.
10. implement only a test double while claiming v0.3B release success.
```

Dependency failure for TongGeometry model artifacts is not a stop condition.

## 3. Review checkpoints

```text
RC-B0: after T47, patch docs installed and old closure claim downgraded to v0.3A-only.
RC-B1: after T50, schemas and problem-source format implemented.
RC-B2: after T53, compilers emit concrete LeanPatchCandidateV1.
RC-B3: after T56, ProofWorker and FinalVerifyGate solver-backed path implemented.
RC-B4: after T58, standard loop counts solver-backed final theorem only under certificate.
RC-B5: after T61, solver-backed corpus and release matrix pass.
RC-B6: after T64, release acceptance and closure.
```

At every checkpoint, Codex must store evidence under:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/
```

## 4. Global verification command surface after v0.3B

By the final task, these commands must exist and pass:

```bash
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry

make smoke-solver-backed-proof-repair
make smoke-solver-backed-geotrace-final
make smoke-solver-backed-construction-final

python scripts/check_solver_backed_patch_schema.py
python scripts/check_solver_backed_corpus.py
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
```

## 5. Task dependency graph

```text
T47 install v0.3B authority docs
 -> T48 audit current proof-repair gap
 -> T49 schema patch: LeanPatchCandidateV1, SolverBackedProofCertificate, TaskRunResult extensions
 -> T50 problem-source format and proof-region guard
 -> T51 TraceCompiler concrete patch emission
 -> T52 ConstructionCompiler concrete patch emission
 -> T53 compiler artifact tests
 -> T54 ProofWorker patch application
 -> T55 FinalVerifyGate solver-backed provenance
 -> T56 TrustGuard / SolverBackedProofCertificate generation
 -> T57 StandardGeometryProofLoop solver-backed release path
 -> T58 solver-backed corpus and generated problem sources
 -> T59 evaluation matrix and metrics update
 -> T60 checker scripts
 -> T61 release acceptance integration
 -> T62 focused smoke and mutation tests
 -> T63 full test / release acceptance run
 -> T64 closure update
```

## 6. Tasks

### T47 — Install v0.3B authority docs

Supports: `R-CLAIM-010`, `R-CLAIM-011`.

Deliverables:

```text
docs/ai/changes/geometry-lean_v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
docs/ai/changes/geometry-lean_v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
docs/ai/changes/geometry-lean_v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md
```

If the repo uses `geometry-lean-v0_3-full-rebase` with a hyphen, use that exact existing folder. Do not create a second active change folder because of typo differences.

Update:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
```

so that the old closure is explicitly v0.3A-only until v0.3B passes.

Verification:

```bash
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
```

Evidence:

```text
evidence/v0_3b_patch_import.md
```

Review checkpoint RC-B0.

### T48 — Audit current proof-repair gap

Supports: all v0.3B purpose clauses.

Deliverables:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_proof_repair_gap_audit.md
```

Audit must identify:

```text
1. all places where provider-backed tasks are prevented from final theorem success.
2. current TaskRunResult fields.
3. current TraceCompilationResult and ConstructionCompilationResult patch material.
4. current FinalVerifyGate provenance fields.
5. current evaluation metric derivation.
6. current checker scripts that must change.
```

Do not edit implementation in T48 except for evidence files.

Verification:

```bash
python - <<'PY'
from pathlib import Path
p = Path("docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_proof_repair_gap_audit.md")
assert p.exists()
text = p.read_text(encoding="utf-8")
for token in ["StandardGeometryProofLoop", "provider-backed", "final_theorem", "TraceCompiler", "ConstructionCompiler"]:
    assert token in text
PY
```

### T49 — Schema patch

Supports: `R-SCHEMA-B001` to `R-SCHEMA-B004`.

Deliverables:

```text
plugins/geometry_synthetic/patching/lean_patch_candidate_v1.py
plugins/geometry_synthetic/proof/solver_backed_proof_certificate.py
schemas/geometry/lean_patch_candidate_v1.schema.json
schemas/geometry/solver_backed_proof_certificate.schema.json
```

Patch existing records:

```text
TaskRunResult
FinalVerifyReport
TraceCompilationResult
ConstructionCompilationResult
WorkerResult
```

Implementation details:

```text
1. Use typed schema implementation consistent with repo style.
2. Unknown fields rejected for proof-critical records.
3. Deterministic hashes.
4. Include to_dict/from_dict or equivalent serialization.
5. Include unit tests for missing solver_dependency_refs, missing proof_region_diff_hash, and raw output laundering.
```

Verification:

```bash
make test-unit TEST_FILTER=solver_backed_schema
python scripts/check_solver_backed_patch_schema.py
python -m compileall -q plugins src scripts tests
```

Review checkpoint RC-B1 may wait until T50.

### T50 — Problem-source format and proof-region guard

Supports: `INV-B006`, `R-WORKER-B001`.

Deliverables:

```text
benchmarks/leangeo/SolverBackedProblems/README.md
lean/MathAutoResearch/Geometry/Generated/.gitkeep
plugins/geometry_synthetic/patching/proof_region.py
tests/unit/test_solver_backed_proof_region.py
```

Required behavior:

```text
1. Source problem files may contain sorry only inside MARP proof-region markers.
2. Source problem files are not imported by normal lake build.
3. Generated candidate files must contain no sorry.
4. Region guard rejects theorem statement edits.
5. Region guard rejects edits outside admitted proof/helper regions.
```

Verification:

```bash
make test-unit TEST_FILTER=solver_backed_proof_region
make lean-build
make lean-no-sorry
```

Review checkpoint RC-B1.

### T51 — TraceCompiler emits concrete LeanPatchCandidateV1

Supports: `R-COMPILER-B001`.

Deliverables:

```text
plugins/geometry_synthetic/trace/trace_compiler.py
plugins/geometry_synthetic/patching/lean_patch_candidate_v1.py
tests/unit/test_trace_compiler_solver_backed_patch.py
tests/mutation/test_trace_compiler_solver_backed_mutation.py
```

Implementation details:

```text
1. For supported trace templates, emit LeanPatchCandidateV1.
2. The patch candidate must include concrete proof replacement text.
3. The patch candidate must include provider manifest ref and geotrace ref.
4. Unsupported trace still returns blocker, never patch success.
5. Missing side condition returns blocker, never patch success.
```

Minimum templates:

```text
trace.coll_self_left.v1
trace.coll_self_right.v1
trace.collinear_or_left.v1
trace.collinear_and_intro.v1
```

Verification:

```bash
make test-unit TEST_FILTER=trace_compiler_solver_backed_patch
make test-mutation TEST_FILTER=trace_compiler_solver_backed
```

### T52 — ConstructionCompiler emits concrete LeanPatchCandidateV1

Supports: `R-COMPILER-B002`.

Deliverables:

```text
plugins/geometry_synthetic/construction/construction_compiler.py
tests/unit/test_construction_compiler_solver_backed_patch.py
tests/mutation/test_construction_compiler_solver_backed_mutation.py
```

Implementation details:

```text
1. For supported construction templates, emit LeanPatchCandidateV1.
2. The patch candidate must include concrete proof replacement text.
3. The patch candidate must include provider manifest ref and auxiliary construction ref.
4. Missing existence/nondegeneracy conditions return blocker unless the template explicitly discharges them.
```

Minimum templates:

```text
construction.exists_existing_line_witness.v1
construction.distinct_points_on_line_pack.v1
construction.exists_point_collinear_self.v1
```

Verification:

```bash
make test-unit TEST_FILTER=construction_compiler_solver_backed_patch
make test-mutation TEST_FILTER=construction_compiler_solver_backed
```

### T53 — Compiler artifact tests

Supports: `R-COMPILER-B003`.

Deliverables:

```text
tests/regression/test_compiler_patch_candidate_not_final_proof.py
tests/regression/test_raw_provider_output_not_patch_material.py
```

Acceptance:

```text
1. TraceCompilationResult alone cannot close task.
2. ConstructionCompilationResult alone cannot close task.
3. LeanPatchCandidateV1 without FinalVerifyGate cannot close task.
4. raw provider output cannot be proof_region_replacement.
```

Verification:

```bash
make test-regression TEST_FILTER=compiler_patch_candidate
```

Review checkpoint RC-B2.

### T54 — ProofWorker patch application

Supports: `R-WORKER-B001`, `R-WORKER-B002`.

Deliverables:

```text
src/math_auto_research/model_api/proof_worker.py
plugins/geometry_synthetic/patching/apply_patch.py
tests/unit/test_proof_worker_solver_patch_application.py
```

Implementation details:

```text
1. Add apply_lean_patch_candidate interface.
2. Write generated candidate file, never mutate source problem.
3. Store generated candidate file ref.
4. Store proof_region_diff_hash.
5. Record solver_dependency_refs.
6. WorkerResult.status = patch_applied only after region guard pass.
7. WorkerResult cannot set final_theorem.
```

Verification:

```bash
make test-unit TEST_FILTER=proof_worker_solver_patch
make test-regression TEST_FILTER=worker_cannot_claim_final
```

### T55 — FinalVerifyGate solver-backed provenance

Supports: `R-FINAL-B001`.

Deliverables:

```text
src/math_auto_research/lean_integration/final_verify_gate.py
tests/unit/test_final_verify_solver_backed_provenance.py
tests/regression/test_final_verify_rejects_missing_solver_backed_provenance.py
```

Implementation details:

```text
1. Accept source_problem_text and generated_candidate_path.
2. Compare source theorem statement hash against candidate theorem statement hash.
3. Reject candidate with sorry.
4. Reject forbidden axioms/admit/unsafe.
5. Reject missing solver-backed provenance when solver_backed mode requested.
6. Record checked_candidate_file_ref.
7. Record solver_backed_proof_status.
```

Verification:

```bash
make test-unit TEST_FILTER=final_verify_solver_backed
make test-regression TEST_FILTER=final_verify_solver_backed
```

### T56 — TrustGuard and SolverBackedProofCertificate generation

Supports: `R-TRUST-B001`, `R-TRUST-B002`.

Deliverables:

```text
plugins/geometry_synthetic/proof/solver_backed_proof_certificate.py
plugins/geometry_synthetic/proof/certificate_builder.py
src/math_auto_research/base/trust/
tests/unit/test_solver_backed_proof_certificate.py
tests/regression/test_solver_backed_laundering.py
```

Implementation details:

```text
1. Build SolverBackedProofCertificate only after FinalVerifyGate final_theorem.
2. Verify all refs are present.
3. Verify theorem hash unchanged.
4. Verify proof_region_diff_hash present.
5. Verify normalized solver artifact kind.
6. Verify raw provider output is not the only solver ref.
7. TrustGuard allows provider-backed final theorem only with passed certificate.
```

Verification:

```bash
make test-unit TEST_FILTER=solver_backed_proof_certificate
make test-regression TEST_FILTER=solver_backed_laundering
```

Review checkpoint RC-B3.

### T57 — StandardGeometryProofLoop solver-backed release path

Supports: `R-LOOP-B001`, `R-LOOP-B002`, `R-LOOP-B003`.

Deliverables:

```text
plugins/geometry_synthetic/standard_loop.py
tests/integration/test_standard_geometry_loop_solver_backed.py
tests/regression/test_standard_loop_no_unconditional_provider_block.py
```

Required code changes:

```text
1. Remove unconditional geometry_chain_diagnostic_only_no_proof_repair_claim blocker.
2. Add solver-backed path:
   extraction -> provider -> compiler -> ProofWorker.apply_lean_patch_candidate
   -> FinalVerifyGate -> SolverBackedProofCertificate -> TaskRunResult final_theorem.
3. Keep run_fixture test-only.
4. Release path must use run_task, never run_fixture.
5. Write per-task artifacts:
   - source_problem_ref
   - generated_candidate_file_ref
   - extraction_report.json
   - provider_run_manifest.json
   - provider_result.json
   - trace_compilation_result.json or construction_compilation_result.json
   - lean_patch_candidate.json
   - worker_result.json
   - final_verify_report.json
   - solver_backed_proof_certificate.json
   - task_result.json
   - artifact_index.json
```

Verification:

```bash
make test-integration TEST_FILTER=standard_geometry_loop_solver_backed
make test-regression TEST_FILTER=standard_loop_no_unconditional_provider_block
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair || true
```

The last command may fail before T58/T59 because the run does not yet exist.

Review checkpoint RC-B4.

### T58 — Solver-backed corpus

Supports: `R-EVAL-B001`, `R-EVAL-B002`.

Deliverables:

```text
benchmarks/geometry/solver_backed_proof_repair.jsonl
benchmarks/leangeo/SolverBackedProblems/SolverBackedProofRepair.lean
configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
```

Corpus floor:

```text
at least 10 tasks:
  >= 6 geotrace-to-Lean tasks
  >= 3 construction-to-Lean tasks
  >= 1 hybrid or side-condition task
```

Problem source requirements:

```text
1. import LeanGeo.Abbre.
2. use real LeanGeo names, not toy definitions.
3. theorem statement protected by hash.
4. proof region contains sorry or failing placeholder before repair.
5. source file is not imported by normal build.
```

Verification:

```bash
python scripts/check_solver_backed_corpus.py
make lean-build
make lean-no-sorry
```

### T59 — Evaluation matrix and metrics update

Supports: `R-EVAL-B010`, `R-EVAL-B011`, `R-EVAL-B012`.

Deliverables:

```text
plugins/geometry_synthetic/evaluation.py
scripts/run_geometry_level2_matrix.py
scripts/check_solver_backed_metrics.py
```

Required behavior:

```text
1. Run every solver-backed corpus task under B0-B5 or the configured solver-backed matrix.
2. B2 must use real Newclid and real GenesisGeo where task requires them.
3. B4 may use lower model + geometry; Tong model-backed remains optional/blocked.
4. Metrics are derived from per-task artifacts.
5. B2 solver_backed_final_theorem_count >= 8.
6. B2 geotrace_solver_backed_final_theorem_count >= 5.
7. B2 construction_solver_backed_final_theorem_count >= 2.
8. B4 solver_backed_final_theorem_count >= 5.
9. No task is counted if original problem compiled unchanged.
10. No task is counted without solver_backed_proof_certificate.json.
```

Verification:

```bash
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
```

Review checkpoint RC-B5 may wait until T61.

### T60 — Checker scripts

Supports: release blockers 35–47.

Deliverables:

```text
scripts/check_solver_backed_patch_schema.py
scripts/check_solver_backed_corpus.py
scripts/check_solver_backed_artifacts.py
scripts/check_solver_backed_metrics.py
scripts/check_no_original_proof_counted_as_solver_backed.py
scripts/check_no_fixture_solver_backed_release.py
```

Each checker must:

```text
1. be deterministic.
2. print JSON status.
3. return nonzero on violation.
4. be unit tested or covered by release acceptance tests.
```

Verification:

```bash
make test-unit TEST_FILTER=solver_backed_checkers
python scripts/check_solver_backed_patch_schema.py
python scripts/check_solver_backed_corpus.py
```

### T61 — Release acceptance integration

Supports: release blocker 47.

Deliverables:

```text
src/math_auto_research/workflow/release_acceptance.py
scripts/check_release_acceptance.py
tests/unit/test_release_acceptance_solver_backed.py
```

Required behavior:

```text
1. Add blockers 35–47.
2. Keep blockers 1–34.
3. Do not re-block core v0.3B on TongGeometry model-backed artifact unavailability.
4. Block V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY if solver-backed counts fail.
5. Continue blocking V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY when model artifacts unavailable.
6. Emit claim_ceiling:
   - v0_3b_solver_backed_ready_no_tong_model_backed_claim
   when core + solver-backed pass and Tong model is blocked.
```

Verification:

```bash
make test-unit TEST_FILTER=release_acceptance_solver_backed
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml
```

Review checkpoint RC-B5.

### T62 — Focused smoke and mutation tests

Supports: all v0.3B blockers.

Deliverables:

```text
make smoke-solver-backed-proof-repair
make smoke-solver-backed-geotrace-final
make smoke-solver-backed-construction-final
```

Add tests:

```text
1. missing LeanPatchCandidateV1 -> release fail.
2. missing WorkerResult.patch_applied -> release fail.
3. missing SolverBackedProofCertificate -> release fail.
4. theorem statement mutation -> fail.
5. raw provider output as solver dependency only -> fail.
6. original already-proved theorem counted as solver-backed -> fail.
7. run_fixture used in solver-backed release -> fail.
8. unsupported trace counted as solver-backed -> fail.
9. construction rationale counted as proof -> fail.
10. FinalVerifyGate success without solver provenance -> not solver-backed.
```

Verification:

```bash
make smoke-solver-backed-proof-repair
make test-regression TEST_FILTER=solver_backed
make test-mutation TEST_FILTER=solver_backed
```

### T63 — Full command pass

Supports final acceptance.

Run:

```bash
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Evidence:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_final_command_log.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Review checkpoint RC-B6 begins after this task.

### T64 — Closure update

Supports closure after all checks pass.

Deliverables:

```text
docs/ai/changes/geometry-lean-v0_3-full-rebase/CLOSURE.md
docs/ai/ACTIVE_CONTEXT.md
```

Allowed closure only if release acceptance passes:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked by unavailable TongGeometry checkpoint artifacts
```

If solver-backed proof repair remains blocked, closure must say:

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: blocked
```

and must not imply that v0.3 is complete in the intended solver-backed sense.
