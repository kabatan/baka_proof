# GeometryFull2D Curated Corpus Import Schema

Status: active import contract for v0.4.3 WP-11/WP-15.

`scripts/import_full2d_curated_corpus.py` admits only positive in-target formal Lean tasks with honest provenance:

- `external_formal`
- `user_reviewed_human_curated`

The importer rejects records labeled `synthetic_generated` or `human_curated_formal`, records without `source_ref`, duplicate task ids, duplicate theorem names, missing Lean files, and optional Lean compiler failures when `--check-lean` is used.

Additional v0.4.3 provenance requirements:

- `external_formal` records must include `license_or_provenance_ref`.
- `user_reviewed_human_curated` records must include `review_manifest_ref`.
- every imported positive record must include `SubstantiveTaskProfileV1` as `substantive_profile`.
- Codex-created local facade tasks cannot be imported as curated or external provenance.

Required fields per record:

```json
{
  "task_id": "full2d-curated-0001",
  "target_status": "in_target_positive",
  "theorem_name": "full2d_curated_0001",
  "theorem_family": "Full2DCore500",
  "grammar_family": "incidence",
  "difficulty_tier": "tier_2_multistep",
  "provenance": "external_formal",
  "lean_file": "benchmarks/geometry_full2d/lean/CuratedBatch001.lean",
  "template_id": "curated_incidence_unique_0001",
  "source_ref": "external-source:batch001:problem0001",
  "license_or_provenance_ref": "external-source:license:batch001",
  "near_duplicate_group": null,
  "substantive_profile": {
    "schema_version": "1.0.0",
    "task_id": "full2d-curated-0001",
    "source_kind": "external_formal",
    "theorem_family": "Full2DCore500",
    "geometry_features": ["incidence"],
    "required_reasoning_depth": 2,
    "requires_construction": false,
    "requires_side_condition_discharge": false,
    "requires_case_split_or_order_reasoning": false,
    "requires_nontrivial_metric_or_algebraic_reasoning": false,
    "direct_lean_lemma_baseline_expected": false,
    "review_manifest_ref": null
  }
}
```

`source_statement_hash`, `canonical_statement_hash`, `near_duplicate_group`, and `expected_outcome` are filled when absent. Importing curated tasks changes the manifest status to `draft_curated_merge_not_release_frozen`; `scripts/freeze_full2d_corpus.py` must still be run before final acceptance.
