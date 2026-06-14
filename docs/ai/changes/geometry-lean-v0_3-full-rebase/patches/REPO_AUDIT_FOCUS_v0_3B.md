---
title: "Repo Audit Focus — v0.3B solver-backed proof repair gap"
status: "ACTIVE_AUDIT_FOCUS"
target_repo: "kabatan/baka_proof"
created: "2026-06-14"
installed: "2026-06-14"
authority: "Focused audit guidance only; does not override Base Spec, Plan, or patch requirements."
---

# Repo Audit Focus — v0.3B solver-backed proof repair gap

This document is the focused audit note for the v0.3B patch. It is not a full repository audit. Its purpose is to tell Codex exactly what gap must be closed.

## 1. Current passed state

The current repo has passed v0.3A core experiment readiness with:

```text
core_experiment_ready_status = passed
tonggeometry_model_backed_status = blocked
claim_ceiling = core_experiment_ready_passed_no_tong_model_backed_claim
```

That is acceptable for v0.3A.

## 2. Current fatal gap for v0.3B

The current implementation prevents provider-backed geometry tasks from becoming final theorem success.

The relevant pattern observed in the current code is:

```python
if geometry_stage_required and final_verify_status == "final_theorem" and chain_satisfied:
    blockers.append("geometry_chain_diagnostic_only_no_proof_repair_claim")
```

This was correct as a temporary safety measure. It is now the main blocker.

## 3. Required change

Provider-backed geometry tasks must be allowed to become `proof_use_status = final_theorem` when and only when:

```text
1. extraction accepted the LeanGeoSubsetV1 problem source;
2. a real provider path produced normalized GeoTraceV1 or AuxiliaryConstructionCandidateV1;
3. TraceCompiler or ConstructionCompiler emitted a concrete LeanPatchCandidateV1;
4. ProofWorker applied the patch to a generated candidate file;
5. FinalVerifyGate verified the generated candidate file;
6. SolverBackedProofCertificate.status = passed.
```

## 4. What must not happen

Codex must not satisfy v0.3B by:

```text
1. counting already-proved Lean examples as solver-backed success;
2. using run_fixture in the release matrix;
3. counting provider diagnostics as proof repair;
4. marking TraceCompilationResult alone as final theorem;
5. weakening FinalVerifyGate;
6. using toy definitions in release problem sources;
7. treating TongGeometry model availability as part of this patch.
```

## 5. Evidence to collect during implementation

Codex must produce evidence files for:

```text
v0_3b_proof_repair_gap_audit.md
t49_solver_backed_schema.md
t50_problem_source_region_guard.md
t51_trace_compiler_patch.md
t52_construction_compiler_patch.md
t54_proof_worker_patch_application.md
t55_final_verify_solver_backed.md
t56_solver_backed_certificate.md
t57_standard_loop_solver_backed.md
t58_solver_backed_corpus.md
t59_solver_backed_matrix.md
t63_v0_3b_final_command_log.md
release_acceptance_v0_3b_report.json
```
