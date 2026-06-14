# ACTIVE_CONTEXT seed — v0.3B solver-backed proof repair

## Current approved baseline

The repo has v0.3A core experiment-ready status, but v0.3B is not yet implemented.

## Current task

Implement the approved v0.3B patch:

```text
MARP-GEOLEAN-BASE-004B
MARP-GEOLEAN-PLAN-004B
MARP-GEOLEAN-ACCEPTANCE-004B
```

## Primary objective

Make solver-backed geometry chains produce Lean final theorem successes through the strict path:

```text
normalized solver artifact
  -> compiler-generated LeanPatchCandidateV1
  -> ProofWorker patch application
  -> FinalVerifyGate
  -> SolverBackedProofCertificate
  -> TaskRunResult.proof_use_status = final_theorem
```

## Do not work on

```text
TongGeometry trained model discovery
open-problem solving
arbitrary LeanGeo theorem support
natural-language formalization
broad Newclid/Tong trace translation
```

## Must not claim

```text
V0.3B_SOLVER_BACKED_PROOF_REPAIR_READY
```

until release acceptance for `configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml` passes with blockers 1–47 absent.
