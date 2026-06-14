---
title: WP-03 structured extraction evidence
status: PASSED
created: 2026-06-15
purpose: Record evidence for the GeometryFull2D structured Lean extraction work package.
authority: Evidence only; does not claim v0.4.2 release completion.
---

# WP-03 Structured Extraction Evidence

## Scope

WP-03 added a Lean-side `CanonicalGeometryStatementV1` smoke extractor and a Python wrapper that runs Lean elaboration, captures the emitted JSON payload, and validates the required canonical fields, hashes, side-condition buckets, and exact-goal relation.

The release extraction checker rejects regex-only classifier tokens in the wrapper and requires Lean elaboration output from:

```text
lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean
```

## Verification

```text
python scripts/check_structured_extraction_v0_4_2.py
```

Result:

```text
passed
```

```text
python -m pytest tests/unit/test_geometry_full2d_extraction.py -q
```

Result:

```text
2 passed
```

```text
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Result:

```text
hard_blockers=[]
completed_work_packages includes WP-03:structured-extraction-checker-passed
next_unblocked_work_packages starts with WP-04
```

## Claim Ceiling

This closes the WP-03 structured extraction smoke and checker only. It does not yet satisfy ClaimSpec canonical bridging, provider run manifests, engine implementation, corpus, performance, or final release acceptance.
