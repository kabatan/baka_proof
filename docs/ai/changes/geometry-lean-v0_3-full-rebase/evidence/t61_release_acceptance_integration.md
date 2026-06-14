---
title: T61 release acceptance integration evidence
status: passed
created: 2026-06-14
authority: evidence
---

# T61 release acceptance integration evidence

Commands run:

```text
make test-unit TEST_FILTER=release_acceptance
make test-unit TEST_FILTER=release_acceptance_solver_backed
python -m compileall -q src plugins scripts tests
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_solver_backed_proof_repair.yaml --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/release_acceptance_report.json
```

Result:

```json
{
  "status": "passed",
  "core_experiment_ready_status": "passed",
  "solver_backed_proof_repair_status": "passed",
  "tonggeometry_model_backed_status": "blocked",
  "claim_ceiling": "v0_3b_solver_backed_ready_no_tong_model_backed_claim",
  "open_blockers": [],
  "blocked_claims": [
    "V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY"
  ],
  "solver_backed_summary": {
    "b2_solver_backed_final_theorem_count": 10,
    "b2_geotrace_solver_backed_final_theorem_count": 6,
    "b2_construction_solver_backed_final_theorem_count": 3,
    "b4_solver_backed_final_theorem_count": 10
  }
}
```

Implementation notes:

- Release acceptance keeps blockers 1-34 on the Level2 pilot core config and evaluates blockers 35-47 on `runs/geometry_solver_backed_proof_repair`.
- `MARP_REFRESH_RELEASE_MATRICES=1` forces matrix regeneration; otherwise acceptance verifies existing run artifacts and checker outputs.
- The optional ablation command surface is skipped unless `MARP_RUN_ABLATION_ACCEPTANCE=1`; it is not one of blockers 1-47.
