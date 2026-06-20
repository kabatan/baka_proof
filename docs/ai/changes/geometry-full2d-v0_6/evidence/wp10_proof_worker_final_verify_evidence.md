# WP10 ProofWorker and FinalVerifyGate Evidence

Status: passed for WP10 ProofWorker/FinalVerifyGate self-test and red-case acceptance.

Commands run from `C:\Users\bakat\work\AI_math_research`:

```powershell
python -m py_compile scripts\geometry_full2d_v0_6_proof_worker.py scripts\check_proof_worker_final_verify_v0_6.py
python scripts\check_schema_contracts_v0_6.py --self-test --red-cases
python scripts\check_proof_worker_final_verify_v0_6.py --self-test --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp10_proof_worker_final_verify_report.json
```

Observed result:

- checker status: `passed`
- positive self-test ran `lake env lean` and returned code `0`
- ProofWorker result schema: `passed`
- FinalVerify report schema: `passed`
- ProofWorker `claim_final_theorem`: `false`
- FinalVerify `proof_use_status`: `final_theorem` only after Lean succeeded
- self-test certificate binding schema: `passed`
- run-dir failure fixture: invalid patch candidate produced `stage_status=failed`
- manifest red cases RC-015 and RC-016: `passed`
- local negative cases rejected: preproved source, patch outside MARP region, statement mutation, sorry, admit, axiom, unsafe, toy target definition, non-admitted import, stale candidate hash, worker final-theorem claim, and non-`lake env lean` verification command

WP10 stage properties:

- ProofWorker applies replacement text only between theorem-specific MARP markers.
- ProofWorker refuses pre-proved source theorem regions and does not claim final theorem status.
- FinalVerifyGate runs `lake env lean` on the generated candidate from scratch.
- FinalVerifyGate rejects changed theorem statement, outside-region changes, `sorry`, `admit`, `axiom`, `unsafe`, toy target definitions, non-admitted imports, stale/mismatched candidate hashes, and any ProofWorker final-theorem claim.
- Run-dir aggregation fails if any ProofWorker result is not `patch_applied`, any final verify report is missing/not run, or any FinalVerify status is not `passed`.
- The certificate binding builder produces a `SolverBackedProofCertificateFull2D` from explicit upstream refs plus the FinalVerify report ref. WP10 self-test uses fixture refs only; release-counted certificate refs are supplied by WP11/WP13 actual causality and actual task records.

Evidence artifact:

- `docs/ai/changes/geometry-full2d-v0_6/evidence/wp10_proof_worker_final_verify_report.json`

Claim ceiling:

WP10 establishes the ProofWorker/FinalVerifyGate mechanism, its negative checks, run-dir failure propagation, and certificate-binding helper. It does not claim that current WP09 compiler candidates close release corpus theorems, live causality, all-baseline matrix completion, corpus floors, release readiness, closure, or K-029 final used-rule coverage.
