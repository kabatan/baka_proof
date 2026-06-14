---
title: "Guardian Acceptance Patch — geometry × Lean v0.3B solver-backed proof repair"
acceptance_patch_id: "MARP-GEOLEAN-ACCEPTANCE-004B"
base_patch: "MARP-GEOLEAN-BASE-004B"
plan_patch: "MARP-GEOLEAN-PLAN-004B"
status: "USER_APPROVED_ACTIVE_AMENDMENT"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
installed: "2026-06-14"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3b_patch_import.md"
---

# Guardian Acceptance Patch — geometry × Lean v0.3B solver-backed proof repair

## 0. Purpose

This patch changes release acceptance from:

```text
the system can run a real integration harness
```

to:

```text
the system can produce replayable solver-backed Lean final theorem successes.
```

It keeps all previous v0.3 and v0.3A blockers. It adds blockers 35–47.

## 1. Release acceptance output fields

`ReleaseAcceptanceReport` must include:

```yaml
status: "passed | blocked | failed"
core_experiment_ready_status: "passed | blocked | failed"
solver_backed_proof_repair_status: "passed | blocked | failed"
tonggeometry_model_backed_status: "passed | blocked | failed"

claim_ceiling: "..."
blocked_claims: []
checked_blockers: []
open_blockers: []
solver_backed_summary:
  run_dir: "runs/geometry_solver_backed_proof_repair"
  b2_solver_backed_final_theorem_count: 0
  b2_geotrace_solver_backed_final_theorem_count: 0
  b2_construction_solver_backed_final_theorem_count: 0
  b4_solver_backed_final_theorem_count: 0
```

## 2. New claim ceiling logic

```python
if core_status == "passed" and solver_backed_status == "passed" and tong_model_status == "passed":
    claim_ceiling = "v0_3b_solver_backed_ready_and_tong_model_backed_ready"
elif core_status == "passed" and solver_backed_status == "passed":
    claim_ceiling = "v0_3b_solver_backed_ready_no_tong_model_backed_claim"
elif core_status == "passed":
    claim_ceiling = "v0_3a_harness_ready_but_solver_backed_proof_repair_blocked"
elif core_status == "blocked":
    claim_ceiling = "release_acceptance_blocked_no_v0_3_completion_claim"
else:
    claim_ceiling = "release_acceptance_failed_no_v0_3_completion_claim"
```

Blocked claims:

```python
if core_status != "passed":
    blocked_claims.append("V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY")
if solver_backed_status != "passed":
    blocked_claims.append("V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY")
if tong_model_status != "passed":
    blocked_claims.append("V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY")
```

## 3. New blockers

### Blocker 35 — LeanPatchCandidateV1 schema and concrete patch material

Fail if:

```text
1. schema file missing.
2. implementation missing.
3. TraceCompilationResult or ConstructionCompilationResult can report compiled without a LeanPatchCandidateV1.
4. LeanPatchCandidateV1 lacks proof_region_replacement text hash.
5. LeanPatchCandidateV1 lacks solver_dependency_refs.
```

Command:

```bash
python scripts/check_solver_backed_patch_schema.py
```

### Blocker 36 — SolverBackedProofCertificate schema

Fail if:

```text
1. schema missing.
2. implementation missing.
3. certificate can pass without FinalVerifyReport.
4. certificate can pass without provider_run_manifest_ref.
5. certificate can pass without normalized solver artifact ref.
```

Command:

```bash
python scripts/check_solver_backed_patch_schema.py
```

### Blocker 37 — Compiler concrete patch emission

Fail if supported trace/construction tasks do not produce concrete LeanPatchCandidateV1.

Evidence required:

```text
trace_compilation_result.json
construction_compilation_result.json
lean_patch_candidate.json
```

Command:

```bash
make test-unit TEST_FILTER=trace_compiler_solver_backed_patch
make test-unit TEST_FILTER=construction_compiler_solver_backed_patch
```

### Blocker 38 — ProofWorker patch application

Fail if:

```text
1. worker does not write generated candidate file.
2. proof_region_diff_hash missing.
3. source problem file edited in place.
4. WorkerResult claims final theorem.
```

Command:

```bash
make test-unit TEST_FILTER=proof_worker_solver_patch
```

### Blocker 39 — FinalVerifyGate solver-backed provenance

Fail if FinalVerifyGate can emit solver-backed final theorem without:

```text
extraction report
goal anchor
provider manifest
normalized solver artifact
compiler result
LeanPatchCandidateV1
WorkerResult
protected statement hash
```

Command:

```bash
make test-unit TEST_FILTER=final_verify_solver_backed
make test-regression TEST_FILTER=final_verify_solver_backed
```

### Blocker 40 — Standard loop no longer unconditionally blocks provider-backed final theorem

Fail if release path still contains or exhibits:

```text
geometry_chain_diagnostic_only_no_proof_repair_claim
```

for a task that otherwise has a passed SolverBackedProofCertificate.

Command:

```bash
make test-integration TEST_FILTER=standard_geometry_loop_solver_backed
make test-regression TEST_FILTER=standard_loop_no_unconditional_provider_block
```

### Blocker 41 — SolverBackedProofRepairCorpus

Fail if:

```text
benchmarks/geometry/solver_backed_proof_repair.jsonl missing
or total tasks < 10
or geotrace tasks < 6
or construction tasks < 3
or hybrid/side-condition tasks < 1
or release source files use toy definitions
or source files are already fully proved outside repair region
```

Command:

```bash
python scripts/check_solver_backed_corpus.py
```

### Blocker 42 — B2 solver-backed final theorem floor

Fail if B2 has:

```text
solver_backed_final_theorem_count < 8
geotrace_solver_backed_final_theorem_count < 5
construction_solver_backed_final_theorem_count < 2
```

Command:

```bash
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
```

### Blocker 43 — B4 solver-backed final theorem floor

Fail if B4 has:

```text
solver_backed_final_theorem_count < 5
```

Command:

```bash
python scripts/check_solver_backed_metrics.py --run-dir runs/geometry_solver_backed_proof_repair
```

### Blocker 44 — Solver-backed artifact completeness

Fail if any solver-backed final theorem task lacks:

```text
task_result.json
source_problem_ref
generated_candidate_file_ref
extraction_report.json
provider_run_manifest.json
provider_result.json
trace_compilation_result.json or construction_compilation_result.json
lean_patch_candidate.json
worker_result.json
final_verify_report.json
solver_backed_proof_certificate.json
proof_region_diff_hash
artifact_index.json
```

Command:

```bash
python scripts/check_solver_backed_artifacts.py --run-dir runs/geometry_solver_backed_proof_repair
```

### Blocker 45 — Original theorem not counted as solver-backed

Fail if:

```text
1. original problem source compiles without patch and is counted as solver-backed.
2. proof_region_diff_hash is null.
3. generated candidate hash equals source problem hash.
4. final proof has no solver dependency refs.
```

Command:

```bash
python scripts/check_no_original_proof_counted_as_solver_backed.py --run-dir runs/geometry_solver_backed_proof_repair
```

### Blocker 46 — No fixture solver-backed release

Fail if solver-backed release path uses:

```text
run_fixture
GEOMETRY_FINAL_VERIFY_FIXTURE
def Point := Unit
def Coll ... := True
fixture adapter versions in B2/B4 solver-backed success path
```

Command:

```bash
python scripts/check_no_fixture_solver_backed_release.py --run-dir runs/geometry_solver_backed_proof_repair
```

### Blocker 47 — Release acceptance patch checks present

Fail if blockers 35–46 are not wired into:

```text
src/math_auto_research/workflow/release_acceptance.py
scripts/check_release_acceptance.py
```

## 4. Metrics checks

`check_solver_backed_metrics.py` must compute metrics from per-task artifacts, not from labels.

Required metric fields:

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

## 5. Valid passing state

The passing v0.3B release acceptance state is:

```json
{
  "status": "passed",
  "core_experiment_ready_status": "passed",
  "solver_backed_proof_repair_status": "passed",
  "tonggeometry_model_backed_status": "blocked",
  "claim_ceiling": "v0_3b_solver_backed_ready_no_tong_model_backed_claim",
  "blocked_claims": [
    "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"
  ],
  "open_blockers": []
}
```

If TongGeometry model artifacts later become available, the final field may become:

```text
tonggeometry_model_backed_status = passed
```

but this is not required for v0.3B.
