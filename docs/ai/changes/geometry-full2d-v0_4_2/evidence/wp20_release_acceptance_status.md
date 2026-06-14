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
- `scripts/freeze_full2d_corpus.py`
- synthetic draft corpus at `benchmarks/geometry_full2d`
- `scripts/run_full2d_matrix.py`
- `scripts/check_full2d_metrics.py`
- `scripts/import_full2d_curated_corpus.py`
- curated corpus import schema at `benchmarks/geometry_full2d/metadata/CURATED_IMPORT_SCHEMA.md`

Verification commands:

```text
python scripts/check_full2d_corpus_manifest.py
python scripts/generate_full2d_synthetic_corpus.py
python scripts/freeze_full2d_corpus.py
lake env lean benchmarks/geometry_full2d/lean/SyntheticDraftCorpus.lean
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
python scripts/check_release_acceptance_v0_4_2.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/release_acceptance_report.json
python -m py_compile scripts/import_full2d_curated_corpus.py scripts/run_full2d_matrix.py scripts/check_full2d_metrics.py scripts/generate_repro_report.py
```

Observed status:

```text
hard_blockers=[]
progress_status=progress_ok_with_debt
release_status=blocked
next_unblocked_work_packages=["WP-20"]
```

Open release blockers after synthetic draft corpus generation:

```text
H-003: external/human-curated positive tasks < 900.
H-004: synthetic generated positives exceed 50% of positives.
H-008: corpus manifest status is draft_synthetic_not_release_complete, not release_frozen.
```

Closed or advanced by this checkpoint:

```text
H-001 positive formal Lean task floor is represented in the draft manifest.
H-002 negative/target-outside/malformed task floor is represented in the draft manifest.
H-007 family/tier floors are represented in the draft manifest.
The synthetic Lean corpus file compiles with `lake env lean`.
The frozen manifest hash is now a sha256 ref.
Matrix, metrics, and reproducibility report plumbing exists and fails release metrics honestly for the non-release-frozen draft corpus.
Curated corpus import now has a gate that rejects synthetic relabeling and requires explicit source references.
```

This evidence does not close v0.4.2. It prevents a false completion claim until the full governed corpus, external/human-curated share, matrix run, metrics, used-rule coverage, and final release acceptance are implemented.
