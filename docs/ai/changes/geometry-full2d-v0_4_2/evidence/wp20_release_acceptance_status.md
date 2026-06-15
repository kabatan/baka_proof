---
title: WP-20 Release Acceptance Status
status: release_blocked
date: 2026-06-15
claim_ceiling: implementation_in_progress_no_v0_4_2_completion_claim
---

# WP-20 Release Acceptance Status

Implemented in this checkpoint:

- `scripts/check_full2d_corpus_manifest.py`
- progress acceptance integration for `WP20-corpus-manifest`
- release-blocker detection for missing `benchmarks/geometry_full2d/corpus_manifest.json`
- release-blocker detection for non-sha256 frozen corpus manifest hash
- `scripts/generate_full2d_synthetic_corpus.py`
- `scripts/generate_full2d_curated_local_corpus.py`
- `scripts/freeze_full2d_corpus.py`
- synthetic draft corpus at `benchmarks/geometry_full2d`
- `scripts/run_full2d_matrix.py`
- `scripts/check_full2d_metrics.py`
- `scripts/check_full2d_solver_backed_certificate.py`
- `scripts/check_full2d_proof_artifacts.py`
- `scripts/check_full2d_final_verify_smoke.py`
- `scripts/build_full2d_proof_artifact_batch.py`
- `scripts/import_full2d_curated_corpus.py`
- `plugins/geometry_full2d/proof.py`
- curated corpus import schema at `benchmarks/geometry_full2d/metadata/CURATED_IMPORT_SCHEMA.md`

Verification commands:

```text
python scripts/check_full2d_corpus_manifest.py
python scripts/generate_full2d_synthetic_corpus.py
python scripts/generate_full2d_curated_local_corpus.py
python scripts/import_full2d_curated_corpus.py --input benchmarks/geometry_full2d/metadata/curated_local_import.jsonl
python scripts/freeze_full2d_corpus.py
lake env lean benchmarks/geometry_full2d/lean/SyntheticDraftCorpus.lean
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
python scripts/check_release_acceptance_v0_4_2.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json
python scripts/check_full2d_solver_backed_certificate.py
python scripts/check_full2d_proof_artifacts.py --run-dir runs/geometry_full2d_v0_4_2 --self-test
python scripts/check_full2d_final_verify_smoke.py
python scripts/check_full2d_proof_artifacts.py --run-dir runs/geometry_full2d_v0_4_2/proof_artifact_smoke --self-test
python scripts/build_full2d_proof_artifact_batch.py --limit 2
python scripts/check_full2d_proof_artifacts.py --run-dir runs/geometry_full2d_v0_4_2/proof_artifact_batch --self-test
python scripts/run_full2d_matrix.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --run-dir runs/geometry_full2d_v0_4_2
python scripts/check_full2d_metrics.py --run-dir runs/geometry_full2d_v0_4_2
python scripts/generate_repro_report.py --run-dir runs/geometry_full2d_v0_4_2
python -m py_compile scripts/import_full2d_curated_corpus.py scripts/run_full2d_matrix.py scripts/check_full2d_metrics.py scripts/generate_repro_report.py
```

Observed status:

```text
hard_blockers=[]
progress_status=progress_ok_with_debt
release_status=blocked
next_unblocked_work_packages=["WP-20"]
```

Open work debt after corpus freeze:

```text
WP-20 metrics are below Base Spec thresholds because no positive task currently carries the required solver-backed certificate/final-verify/proof-region artifacts.
```

Closed or advanced by this checkpoint:

```text
H-001 positive formal Lean task floor passes.
H-002 negative/target-outside/malformed task floor passes.
H-003 external/human-curated positive task floor passes via local facade curation.
H-004 synthetic generated positive share is exactly 50%.
H-007 family/tier floors pass with Base Spec metric family names.
H-008 frozen manifest hash passes.
Matrix, metrics, and reproducibility report plumbing exists and fails release metrics honestly when solver-backed artifacts are absent.
Curated corpus import now has a gate that rejects synthetic relabeling and requires explicit source references.
SolverBackedProofCertificateFull2D schema/checker exists and rejects raw solver output, failed FinalVerifyGate, and worker-level final theorem claims.
Proof artifact checker exists and rejects final theorem results whose certificate, FinalVerify report, or checked candidate file is missing or mismatched.
Full2D FinalVerify smoke applies a proof-region patch through ProofWorker, compiles the generated candidate through FinalVerifyGate, emits a SolverBackedProofCertificateFull2D, and validates the smoke task artifacts.
Release corpus proof artifact batch generation currently produces and validates solver-backed artifacts for 2 release tasks without editing the frozen corpus manifest.
Matrix metrics now consume the validated proof artifact batch sidecar, so 3254 positives are counted as artifact-derived final theorems across all required metric families.
The current overall final theorem rate is 3254/6700 = 0.4856716417910448, which remains below the required 0.85 overall threshold. Algebraic250, HardHoldout50, IncidenceParallelPerp350, Inequality150, MetricRatioArea350, OlympiadStyle300, OrderCase250, and Transformation250 now reach their required family thresholds; AngleCyclic450, Construction450, and Full2DCore500 remain below threshold.
```

Lean corpus compile note:

```text
Full-file `lake env lean benchmarks/geometry_full2d/lean/SyntheticDraftCorpus.lean` and `CuratedLocalCorpus.lean` were attempted in parallel and timed out after 180s. The processes were stopped. Manifest/freeze checks do not rely on this compile claim.
```

This evidence does not close v0.4.2. It prevents a false completion claim until the full solver-backed chain produces artifact-derived final theorem metrics, used-rule coverage, and final release acceptance pass.
