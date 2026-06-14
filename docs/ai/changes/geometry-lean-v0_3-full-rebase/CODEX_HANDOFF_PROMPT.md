# Codex handoff prompt — geometry × Lean v0.3B solver-backed proof repair

Use Guardian Lane.

You are working in `kabatan/baka_proof`.

The repository has passed the v0.3A harness-ready/core experiment-ready closure. It has not yet passed v0.3B solver-backed proof repair.

## Read first

Read these files in order:

1. `docs/ai/ACTIVE_CONTEXT.md`
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md`
3. `docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md`
4. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md`
5. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md`
6. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md`
7. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md`
8. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md`
9. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md`
10. `docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/REPO_AUDIT_FOCUS_v0_3B.md`

## Mission

Implement v0.3B so that normalized geometry solver artifacts can become concrete Lean proof repairs and pass FinalVerifyGate.

Required successful chain:

```text
LeanGeoSubsetV1 problem theorem with proof-region marker
  -> GeometryExtractionContract
  -> GeometryClaimSpec
  -> real provider path
  -> GeoTraceV1 or AuxiliaryConstructionCandidateV1
  -> TraceCompiler or ConstructionCompiler
  -> LeanPatchCandidateV1
  -> ProofWorker applies patch
  -> generated candidate Lean file
  -> FinalVerifyGate
  -> SolverBackedProofCertificate
  -> TaskRunResult.solver_backed_final_theorem = true
```

## Current task

Begin at:

```text
T48 — Audit current proof-repair gap
```

T47 is complete: v0.3B patch documents are installed.

## Forbidden shortcuts

- Counting raw provider output as proof.
- Counting TraceCompilationResult or ConstructionCompilationResult alone as proof.
- Counting an unchanged already-proved Lean theorem as solver-backed success.
- Keeping provider-backed tasks diagnostic-only while adjusting metrics.
- Using `run_fixture` in release matrix.
- Using toy geometry definitions in release corpus.
- Removing FinalVerifyGate checks.
- Modifying protected theorem statements.
- Requiring TongGeometry trained checkpoints for v0.3B.

## Final acceptance command

The final release command must pass:

```bash
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Expected passing claim ceiling if TongGeometry model checkpoints remain unavailable:

```text
v0_3b_solver_backed_ready_no_tong_model_backed_claim
```
