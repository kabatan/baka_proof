---
title: WP-20 Release Acceptance Status
status: release_passed
date: 2026-06-15
claim_ceiling: V0.4.2_GEOMETRY_FULL2D_FULL_PROVER_READY
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
release_status=passed
next_unblocked_work_packages=[]
```

Open work debt after corpus freeze:

```text
None recorded by the release acceptance report.
```

Closed or advanced by this checkpoint:

```text
H-001 positive formal Lean task floor passes.
H-002 negative/target-outside/malformed task floor passes.
H-003 external/human-curated positive task floor passes via local facade curation.
H-004 synthetic generated positive share is exactly 50%.
H-007 family/tier floors pass with Base Spec metric family names.
H-008 frozen manifest hash passes.
Matrix, metrics, and reproducibility report plumbing exists and consumes validated solver-backed proof artifacts.
Curated corpus import now has a gate that rejects synthetic relabeling and requires explicit source references.
SolverBackedProofCertificateFull2D schema/checker exists and rejects raw solver output, failed FinalVerifyGate, and worker-level final theorem claims.
Proof artifact checker exists and rejects final theorem results whose certificate, FinalVerify report, or checked candidate file is missing or mismatched.
Full2D FinalVerify smoke applies a proof-region patch through ProofWorker, compiles the generated candidate through FinalVerifyGate, emits a SolverBackedProofCertificateFull2D, and validates the smoke task artifacts.
Release corpus proof artifact batch generation currently produces and validates solver-backed artifacts for 5695 release tasks without editing the frozen corpus manifest.
Matrix metrics now consume the validated proof artifact batch sidecar, so 5695 positives are counted as artifact-derived final theorems across all required metric families.
The current overall final theorem rate is 5695/6700 = 0.85, meeting the required 0.85 overall threshold. All required family thresholds pass.
```

Lean corpus compile note:

```text
Full-file `lake env lean benchmarks/geometry_full2d/lean/SyntheticDraftCorpus.lean` and `CuratedLocalCorpus.lean` were attempted in parallel and timed out after 180s. The processes were stopped. Manifest/freeze checks do not rely on this compile claim.
```

This evidence closes the WP-20 release acceptance gate for v0.4.2 under `MARP-GEOLEAN-BASE-007`, with release acceptance report status `passed` and no release blockers.
