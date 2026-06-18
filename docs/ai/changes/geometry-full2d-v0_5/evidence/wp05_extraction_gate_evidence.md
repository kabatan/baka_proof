---
title: "WP-05 Evidence — Structured Lean Extraction Per Theorem"
status: "WP-05_IMPLEMENTED"
created: 2026-06-18
base_spec: "MARP-GEOLEAN-BASE-011"
plan: "MARP-GEOLEAN-PLAN-011"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-011"
claim_ceiling: "WP-05 extraction builder/checker implemented; counted-corpus extraction completion is not claimed before WP-10A corpus materialization."
---

# WP-05 Evidence — Structured Lean Extraction Per Theorem

## Implemented Files

- `scripts/geometry_full2d_v0_5_extraction.py`
- `scripts/build_full2d_extraction_corpus_v0_5.py`
- `scripts/check_full2d_extraction_corpus_v0_5.py`
- `scripts/geometry_full2d_v0_5_schemas.py` tightened `LeanExtractionReportFull2D`.

## Enforced WP-05 Properties

- v0.5 extraction reports are normalized to `LeanExtractionReportFull2D`.
- Reports bind source file hash, theorem statement hash, elaborated expression hash, and Lean-side target classification.
- Python may locate theorem source and theorem name, but semantic classification must come from `lean_elaborator_structured_theorem`.
- Reports with Python semantic classification, regex semantic classification, handwritten markers, stale source hashes, stale theorem hashes, stale extraction index corpus hashes, pre-proved source theorem status, or incomplete/smoke-only report coverage are rejected.
- The builder writes one extraction report per required task and a corpus-bound extraction index.

## Verification Commands

```text
python scripts/check_schema_validators_v0_5.py --self-test
python scripts/check_full2d_extraction_corpus_v0_5.py --self-test
python scripts/check_full2d_extraction_corpus_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5 --run-dir runs/geometry_full2d_v0_5
python scripts/extract_geometry_full2d_theorem.py --lean-file lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean --theorem-name full2d_smoke_collinear_refl --output .tmp/v05_wp05_smoke_extraction.json
python scripts/build_full2d_extraction_corpus_v0_5.py --corpus-root .tmp/v05_wp05_corpus_fixture --run-dir .tmp/v05_wp05_run_fixture
python scripts/check_full2d_extraction_corpus_v0_5.py --corpus-root .tmp/v05_wp05_corpus_fixture --run-dir .tmp/v05_wp05_run_fixture
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_release_acceptance_v0_5.py --config configs/benchmark_runs/geometry_full2d_v0_5.yaml --output docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json --fresh-run
git diff --check
```

## Observed Results

- Schema validator self-test passed after tightening extraction report requirements.
- Extraction checker self-test passed:
  - positive fixture accepted;
  - incomplete/smoke-only fixture rejected;
  - handwritten JSON fixture rejected;
  - stale source/cache fixture rejected;
  - Python semantic classification fixture rejected.
- Current real release corpus path fails extraction checking because the counted v0.5 corpus and extraction index do not exist yet.
- Existing Lean-side smoke theorem extraction succeeded through the structured elaborator extractor. That theorem is pre-proved and is not counted release evidence.
- A temporary sorry-only one-task corpus passed v0.5 extraction builder and checker.
- Red cases remain fully rejected: 19/19.
- Acceptance K coverage remains complete for K-001..K-033.
- No checker filename/role suppression was detected.
- Final release command still fails closed because WP-06+ provider, checker, registry, compiler, proof worker, matrix, causality, metrics, corpus freeze, and closure gates are not complete. The generated incomplete `release_acceptance_report.json` was intentionally deleted and is not release evidence.

## Non-Claims

- No counted v0.5 corpus has been extracted.
- No WP-10A freeze manifest exists.
- No release acceptance completion is claimed.
- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` is not claimed.
