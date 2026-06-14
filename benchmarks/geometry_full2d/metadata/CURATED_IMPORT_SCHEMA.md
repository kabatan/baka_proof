# GeometryFull2D Curated Corpus Import Schema

Status: active import contract for v0.4.2 WP-20.

`scripts/import_full2d_curated_corpus.py` admits only positive in-target formal Lean tasks with honest provenance:

- `external_formal`
- `human_curated_formal`

The importer rejects records labeled `synthetic_generated`, records without `source_ref`, duplicate task ids, duplicate theorem names, missing Lean files, and optional Lean compiler failures when `--check-lean` is used.

Required fields per record:

```json
{
  "task_id": "full2d-curated-0001",
  "target_status": "in_target_positive",
  "theorem_name": "full2d_curated_0001",
  "theorem_family": "Full2DCore500",
  "grammar_family": "incidence",
  "difficulty_tier": "tier_2_multistep",
  "provenance": "human_curated_formal",
  "lean_file": "benchmarks/geometry_full2d/lean/CuratedBatch001.lean",
  "template_id": "curated_incidence_unique_0001",
  "source_ref": "local-curation:batch001:problem0001",
  "near_duplicate_group": null
}
```

`source_statement_hash`, `canonical_statement_hash`, `near_duplicate_group`, and `expected_outcome` are filled when absent. Importing curated tasks changes the manifest status to `draft_curated_merge_not_release_frozen`; `scripts/freeze_full2d_corpus.py` must still be run before final acceptance.
