# WP12 Corpus And Holdout Evidence

Status: MECH ready for review.

Implemented/updated files:

- `scripts/generate_geometry_full2d_v0_6_corpus.py`
- `scripts/build_geometry_full2d_v0_6_freeze_manifest.py`
- `scripts/create_geometry_full2d_v0_6_release_seed.py`
- `scripts/check_corpus_independence_v0_6.py`
- `scripts/check_statement_diversity_v0_6.py`
- `benchmarks/geometry_full2d_v0_6/corpus_manifest.json`
- `benchmarks/geometry_full2d_v0_6/lean/GeneratedSealedHoldout.lean`
- `benchmarks/geometry_full2d_v0_6/lean/GeneratedTargetOutside.lean`
- `benchmarks/geometry_full2d_v0_6/metadata/*`

Generation:

```bash
python scripts\build_geometry_full2d_v0_6_freeze_manifest.py --output benchmarks\geometry_full2d_v0_6\metadata\implementation_freeze_manifest_v0_6.json
python scripts\create_geometry_full2d_v0_6_release_seed.py --implementation-freeze-manifest benchmarks\geometry_full2d_v0_6\metadata\implementation_freeze_manifest_v0_6.json --implementation-freeze-manifest-hash sha256:f937afebd9fff64dd42bec8723daeb8ab513b168f94610b3e1726b967b588008 --output benchmarks\geometry_full2d_v0_6\metadata\release_seed_transcript_v0_6.json
python scripts\generate_geometry_full2d_v0_6_corpus.py --corpus-root benchmarks\geometry_full2d_v0_6 --release-seed v0_6_release_acceptance_pre_run_seed_5169dd893286d0aef2f892d428cdabce1aed15e8095f3c23 --implementation-freeze-manifest benchmarks\geometry_full2d_v0_6\metadata\implementation_freeze_manifest_v0_6.json --implementation-freeze-manifest-hash sha256:f937afebd9fff64dd42bec8723daeb8ab513b168f94610b3e1726b967b588008 --release-seed-transcript benchmarks\geometry_full2d_v0_6\metadata\release_seed_transcript_v0_6.json --release-seed-transcript-hash sha256:f14095a05e03ff4f6305d954f85c2a9ec4274cc1bcde12f1804bef6d2c11ad63 --positive-count 1200 --negative-count 220
```

Observed generation result:

- Exit code 0.
- `positive_count`: 1200.
- `external_goal_preserved_count`: 0.
- `sealed_adversarial_holdout_count`: 1200.
- `negative_count`: 220.
- `git_head`: `d767432937def1bca5dc444dec2429d54b262c37`.
- `freeze_builder_manifest_hash`: `sha256:f937afebd9fff64dd42bec8723daeb8ab513b168f94610b3e1726b967b588008`.
- `release_seed`: `v0_6_release_acceptance_pre_run_seed_5169dd893286d0aef2f892d428cdabce1aed15e8095f3c23`.
- `release_seed_transcript_hash`: `sha256:f14095a05e03ff4f6305d954f85c2a9ec4274cc1bcde12f1804bef6d2c11ad63`.
- `corpus_manifest_hash`: `sha256:0c5aa6a5c7841ac894e46dbf12db7527e39e7dc530a530ef4d41e8ef4c312711`.
- `implementation_freeze_manifest_hash`: `sha256:f937afebd9fff64dd42bec8723daeb8ab513b168f94610b3e1726b967b588008`.
- `sealed_holdout_manifest_hash`: `sha256:1677431b98f8d7d37dbd3def7f9360cc4479c831f08b209b881431fcb88d5a47`.

Freeze coverage:

- The freeze manifest records `freeze_includes_provider_compiler_rule_registry: true`.
- The freeze manifest records `required_freeze_paths_checked_for_existence: true`; missing required paths now fail freeze building rather than being silently omitted.
- The sealed corpus generator no longer builds the freeze manifest and does not contain provider/compiler/rule-registry/proof-worker implementation path literals; it consumes the pre-existing freeze manifest path/hash only.
- The release seed is generated in a separate transcript after the freeze manifest and is hash-bound from both the corpus manifest and sealed holdout manifest.
- Rule registry freeze coverage includes `scripts/geometry_full2d_v0_6_rule_registry.py`, `scripts/geometry_full2d_v0_6_rule_checkers.py`, `scripts/check_rule_registry_v0_6.py`, `lean/MathAutoResearch/GeometryFull2D/RuleLemmas.lean`, and `docs/ai/changes/geometry-full2d-v0_6/evidence/rule_registry_full2d_v0_6.json`.

Acceptance commands:

```bash
python -m py_compile scripts\build_geometry_full2d_v0_6_freeze_manifest.py scripts\create_geometry_full2d_v0_6_release_seed.py scripts\generate_geometry_full2d_v0_6_corpus.py scripts\check_corpus_independence_v0_6.py scripts\check_statement_diversity_v0_6.py
python scripts\check_corpus_independence_v0_6.py --corpus-root benchmarks\geometry_full2d_v0_6 --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp12_corpus_independence_report.json
python scripts\check_statement_diversity_v0_6.py --corpus-root benchmarks\geometry_full2d_v0_6 --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp12_statement_diversity_report.json
lake env lean benchmarks\geometry_full2d_v0_6\lean\GeneratedSealedHoldout.lean
lake env lean benchmarks\geometry_full2d_v0_6\lean\GeneratedTargetOutside.lean
```

Observed acceptance result:

- All commands exited 0.
- `GeneratedSealedHoldout.lean` was rerun with command output redirected to a temp log because 1200 expected `sorry` warnings exceeded the interactive output timeout; the recorded Lean exit code was 0 and the first error scan found no `error:` lines.
- Lean emitted expected `sorry` warnings for source theorem statements; no Lean errors.
- Corpus independence check passed with red cases for projection counted positives, source-ref-only goal preservation, available external source without ExternalGoalPreserved tasks, forbidden sealed metadata, forbidden generator imports, forbidden generator implementation-file reads/path literals, manifest hash mismatch, sealed-to-freeze hash mismatch, per-task sealed manifest hash mismatch, release-seed transcript mismatch, and missing rule-registry freeze coverage.
- Statement diversity check passed:
  - counted positives: 1200
  - target-outside/malformed negatives: 220
  - unique normalized target ASTs: 1200
  - unique hypothesis-target dependency signatures: 1200
  - near duplicate fraction: 0.025833
  - direct/facade lemma eligible fraction: 0.0
  - construction/case/certificate required: 650
  - multi-step derivation required: 850
  - no target family exceeds the floor limits.

Claim ceiling:

WP12 establishes a release-counted v0.6 corpus and sealed holdout mechanism that satisfies the Base Spec corpus/diversity floors and independence checks under a hash-bound pre-run release seed transcript. It does not claim provider success, final theorem success, all-baseline matrix completion, live causality for release-counted B2 successes, metrics thresholds, release readiness, or closure. Final acceptance may still regenerate or revalidate with a final release command seed.
