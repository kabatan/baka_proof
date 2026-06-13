# RC-4 fix evidence

Status: ready for RC-4 re-review.

Prior RC-4 findings addressed:

```text
1. Lean grammar path moved to lean/MathAutoResearch/Geometry/LeanGeoSubsetV1/Grammar.lean
   and lakefile.lean now builds the MathAutoResearch library from srcDir := "lean".
2. plugins/geometry_synthetic/target_subset/leangeo_subset_v1.yaml is now a
   TargetLibraryManifest with source dependency, commit, and hash refs.
   Predicate and construction mappings now include the Base-required policy,
   template, existence, uniqueness, and generated-obligation fields.
3. benchmarks/geometry/leangeo_real_smoke.jsonl has 12 tasks with required
   categories, and geometry_level2_pilot.jsonl has 25 tasks with required
   category counts.
4. GeometryExtractor.extract no longer creates claims from raw/non-elaborated
   text. Accepted claims come from extract_context or extract_lean_check_output.
5. GeometryClaimSpec now carries sha256 protected_statement_hash and
   target_library_manifest_hash provenance, and its schema requires these fields.
6. Raw DSL mutation coverage now uses a nonempty anchor and verifies
   non_elaborated_lean_goal_required.
```

Commands run:

```text
make test-unit TEST_FILTER=target_subset
make test-unit TEST_FILTER=geometry_corpus
make test-unit TEST_FILTER=geometry_extraction
make test-mutation TEST_FILTER=extraction
python -m math_auto_research.cli.validate_schema plugins\geometry_synthetic\target_subset\leangeo_subset_v1.yaml
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\leangeo_real_smoke.jsonl
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\geometry_level2_pilot.jsonl
python -m math_auto_research.cli.validate_artifact benchmarks\geometry\rejected_by_extraction.jsonl
make lean-build
make lean-no-sorry
python scripts\check_domain_contamination.py
make smoke-geometry-extraction
make test-unit TEST_FILTER=real_smoke_corpus
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
target_subset unit tests: 4 tests OK
geometry_corpus unit tests: 5 tests OK
geometry_extraction unit tests: 12 tests OK
filtered extraction mutation tests: 17 tests OK
TargetLibraryManifest schema validation: ok
all three JSONL corpus manifests validated against geometry.geometry_corpus_jsonl.v1
lake build: Build completed successfully
lean no-sorry check passed
domain contamination check passed
smoke-geometry-extraction passed
real_smoke_corpus unit tests: 5 tests OK
compileall passed
```

Known warning:

```text
Lean commands emitted existing .lake dependency local-change warnings for
UnicodeBasic and batteries; builds and checks completed successfully.
```
