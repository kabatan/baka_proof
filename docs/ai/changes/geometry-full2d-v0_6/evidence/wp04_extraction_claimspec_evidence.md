---
title: "WP04 Extraction and ClaimSpec Evidence"
base_spec: "MARP-GEOLEAN-BASE-012"
plan: "MARP-GEOLEAN-PLAN-012"
status: "MECH_WP04_LOCAL_PASS"
---

# WP04 Extraction and ClaimSpec Evidence

Commands:

```bash
python scripts/check_full2d_extraction_corpus_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --run-dir runs/wp04_v0_6_fresh --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp04_extraction_report.json
python scripts/check_full2d_claimspec_v0_6.py --run-dir runs/wp04_v0_6_fresh --self-test --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp04_claimspec_report.json
```

Result:

```text
extraction.status=passed
extraction.report_count=3
extraction.self_test.status=passed
lean_semantic_extractor_cache_status=miss for all 3 generated extraction reports
claimspec.status=passed
claimspec.claim_spec_count=3
claimspec.self_test.status=passed
errors=[]
```

Scope:

- Implements WP04 only.
- Adds a v0.6 bootstrap extraction corpus for Lean extraction and ClaimSpec validation.
- Uses Lean-side structured extraction through `MathAutoResearch.GeometryFull2D.Extraction`.
- Binds extraction cache acceptance to theorem header hash, extractor hash, Lean context hash, and Lean version.
- Includes a stale-cache self-test that rejects a mismatched Lean context/toolchain cache payload.
- Normalizes extraction reports to `LeanExtractionReportFull2D`.
- Builds `GeometryFull2DClaimSpec` only from extraction reports.

Claim ceiling:

WP04 local extraction and ClaimSpec acceptance passed on the bootstrap corpus. This is not the WP12 release corpus/diversity claim and not full pipeline completion.
