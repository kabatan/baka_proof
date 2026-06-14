# Codex Handoff Prompt — v0.3B solver-backed proof repair

You are implementing the v0.3B solver-backed proof repair patch in `kabatan/baka_proof`.

## Read first

Read these files in order:

```text
docs/ai/ACTIVE_CONTEXT.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3B.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3B.md
```

If v0.3B patch files are not installed yet, install the user-approved copies first.

## Mission

The current repo is not acceptable as solver-backed proof repair because provider-backed geometry tasks are not counted as final theorem successes. Implement v0.3B so that a normalized solver artifact can become a concrete Lean proof repair and pass FinalVerifyGate.

The required successful chain is:

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

## Do not solve this by weakening safety

Forbidden shortcuts:

```text
- Counting raw provider output as proof.
- Counting TraceCompilationResult alone as proof.
- Counting an unchanged already-proved Lean theorem as solver-backed success.
- Keeping provider-backed tasks diagnostic-only while adjusting metrics.
- Using run_fixture in release matrix.
- Using toy geometry definitions in release corpus.
- Removing FinalVerifyGate checks.
- Modifying protected theorem statements.
- Requiring TongGeometry trained checkpoints for this patch.
```

## Implement tasks

Follow PLAN_PATCH_v0_3B tasks T47 through T64 exactly.

## Final acceptance command

The final release command must pass:

```bash
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_v0_3b_report.json
```

Expected passing claim ceiling if TongGeometry model checkpoints remain unavailable:

```text
v0_3b_solver_backed_ready_no_tong_model_backed_claim
```

Expected allowed closure:

```text
V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY: passed
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY: passed
V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY: blocked by unavailable TongGeometry checkpoint artifacts
```
