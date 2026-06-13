# T42 Nontrivial LeanGeoSubsetV1 Corpus Evidence

Task: T42 — Nontrivial LeanGeoSubsetV1 corpus replacement.

## Changed Files

```text
benchmarks/leangeo/RealSmokeCorpus.lean
benchmarks/geometry/leangeo_real_smoke.jsonl
benchmarks/geometry/geometry_level2_pilot.jsonl
benchmarks/geometry/rejected_by_extraction.jsonl
scripts/check_level2_corpus_nontrivial.py
tests/unit/test_geometry_corpus_manifests.py
```

## Result

The Level2 pilot corpus now satisfies the v0.3A nontrivial floor:

```text
total tasks: 25
nonidentity_symbolic_closure: 10
auxiliary_construction: 5
proof_worker_only_baseline: 5
safe_reject_or_blocker: 5
identity_hypothesis tasks: 0
source_lean_mode: real_leangeo_dependency for all release tasks
```

Every release task has:

```text
normalized_goal_signature
is_identity_hypothesis
expected_required_stages
source_lean_mode
```

`RealSmokeCorpus.lean` imports `LeanGeo.Abbre` and does not define local toy
`Point` or `Coll` substitutes.

## Verification

```text
python scripts/check_level2_corpus_nontrivial.py
status: passed

python -m math_auto_research.cli.validate_artifact benchmarks/geometry/geometry_level2_pilot.jsonl
status: passed

make test-unit TEST_FILTER=geometry_corpus_manifests
status: passed, 6 tests

make test-unit TEST_FILTER=real_smoke_corpus
status: passed, 5 tests

make lean-build
status: passed

git diff --check
status: passed, CRLF warnings only
```

## Claim Ceiling

T42 is complete. No v0.3 completion claim is made because the standard loop,
artifact-derived matrix, release acceptance, and closure tasks remain.
