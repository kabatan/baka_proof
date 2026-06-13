# RC-4 Guardian boundary review

Reviewer: guardian_boundary_reviewer

Result: FAIL_FIXABLE

Reviewed commit:

```text
930ae50 V03 full rebase complete T20 extraction mutations
```

Blocking findings:

```text
1. T17 Plan-path mismatch: Plan requires
   lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/Grammar.lean, but the repo
   only had MathAutoResearch/Geometry/LeanGeoSubsetV1/Grammar.lean.
2. T17 mapping/manifest content incomplete: TargetLibraryManifest lacks
   source_dependency, commit/version, and hash refs; construction mapping lacks
   construction ID, Lean template ID, existence conditions, uniqueness
   requirements, and generated obligations.
3. T18 corpus manifests too small for R-EVAL-001: real smoke requires at least
   12 tasks and pilot requires at least 25 tasks with category coverage.
4. T19 extractor does not enforce only Lean goals: raw text with a nonempty
   anchor can produce an accepted claim.
5. T19 provenance is not source-faithful: protected_statement_hash and target
   library manifest hash refs are placeholders rather than preserved hashes.
6. T20 raw DSL mutation coverage only rejects empty-anchor raw DSL and misses
   raw/non-Lean text with a nonempty anchor.
```

Forbidden claims preserved:

```text
No RC-4 PASS claim.
No T17/T18/T19 full Base/Plan satisfaction claim.
No SOURCE_FAITHFUL / ACCEPTANCE_COMPLETE / V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY claim.
No R-ID is VERIFIED.
```
