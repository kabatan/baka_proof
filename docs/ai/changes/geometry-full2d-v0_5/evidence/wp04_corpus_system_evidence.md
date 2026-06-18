---
title: "WP-04 Evidence — Corpus System Without Proof Coupling"
status: "WP-04_IMPLEMENTED"
created: 2026-06-18
base_spec: "MARP-GEOLEAN-BASE-011"
plan: "MARP-GEOLEAN-PLAN-011"
acceptance: "MARP-GEOLEAN-ACCEPTANCE-011"
claim_ceiling: "WP-04 corpus tooling and guards implemented; counted corpus release evidence is not claimed before WP-10A freeze."
---

# WP-04 Evidence — Corpus System Without Proof Coupling

## Implemented Files

- `scripts/geometry_full2d_v0_5_corpus.py`
- `scripts/discover_external_goal_sources_v0_5.py`
- `scripts/import_external_goal_preserved_v0_5.py`
- `scripts/generate_sealed_adversarial_holdout_v0_5.py`
- `scripts/check_corpus_independence_v0_5.py`
- `scripts/check_corpus_statement_diversity_v0_5.py`
- `scripts/check_goal_preservation_reports_v0_5.py`

## Enforced WP-04 Properties

- Counted SealedAdversarialHoldout generation fails without a freeze manifest.
- Pre-freeze sealed generation emits only non-counted preview tasks.
- Corpus independence checker rejects forbidden proof-coupled keys recursively, including rule ids, engine roles, proof labels, target shape ids, compiler rules, templates, proof text, and solver hints.
- Corpus independence checker scans the sealed generator entrypoint and generator function for forbidden downstream proof imports and unadmitted reads.
- Sealed holdout counted tasks must carry seed, generator hash, grammar hash, freeze hash, and challenge manifest hash.
- ExternalGoalPreserved import accepts only exact formal-goal preservation in this WP and writes content-addressed source, translated, mapping, and checker witness artifacts.
- GoalPreservation checker resolves those refs and recomputes exact preservation instead of trusting report fields.
- Statement diversity checker enforces v0.5 floors for skeleton count, duplicate cap, relation-family count, construction/case/certificate requirements, and non-target-intermediate requirements.

## Verification Commands

```text
python scripts/check_corpus_independence_v0_5.py --self-test
python scripts/check_corpus_statement_diversity_v0_5.py --self-test
python scripts/check_goal_preservation_reports_v0_5.py --self-test
python scripts/generate_sealed_adversarial_holdout_v0_5.py --output-root .tmp/v05_wp04_preview --count 5 --seed 1
python scripts/generate_sealed_adversarial_holdout_v0_5.py --output-root .tmp/v05_wp04_counted_no_freeze --count 5 --seed 1 --counted
python scripts/check_corpus_independence_v0_5.py --corpus-root .tmp/v05_wp04_preview
python scripts/import_external_goal_preserved_v0_5.py --registry .tmp/v05_wp04_external_fixture/metadata/external_goal_sources.json --corpus-root .tmp/v05_wp04_external_fixture
python scripts/check_goal_preservation_reports_v0_5.py --corpus-root .tmp/v05_wp04_external_fixture
python scripts/check_corpus_independence_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/check_corpus_statement_diversity_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/check_goal_preservation_reports_v0_5.py --corpus-root benchmarks/geometry_full2d_v0_5
python scripts/run_red_cases_v0_5.py --expect-failure
python scripts/check_acceptance_coverage_v0_5.py
python scripts/check_no_checker_whitelist_v0_5.py
python scripts/check_release_acceptance_v0_5.py --config configs/benchmark_runs/geometry_full2d_v0_5.yaml --output docs/ai/changes/geometry-full2d-v0_5/evidence/release_acceptance_report.json --fresh-run
git diff --check
```

## Observed Results

- Corpus checker self-tests passed.
- Missing counted corpus fails independence, diversity, and goal-preservation checks.
- Pre-freeze sealed preview generation passed and the preview corpus passed independence checks.
- Counted sealed generation without freeze manifest failed with `counted_generation_requires_freeze_manifest`.
- Exact ExternalGoalPreserved fixture imported successfully and passed goal-preservation replay checks.
- Red cases remain fully rejected: 19/19.
- Acceptance K coverage remains complete for K-001..K-033.
- No checker filename/role suppression was detected.
- Final release command still fails closed because later WP-05+ executable pipeline components and counted corpus are not yet implemented. The generated incomplete `release_acceptance_report.json` was intentionally deleted and is not release evidence.

## Non-Claims

- No counted v0.5 corpus has been materialized.
- No WP-10A freeze manifest exists.
- No release acceptance completion is claimed.
- `V0.5_GEOMETRY_FULL2D_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY` is not claimed.
