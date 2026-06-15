---
title: "Guardian Acceptance Spec — Geometry × Lean Full2D Real Pipeline Recovery v0.4.3 Integrated"
acceptance_id: "MARP-GEOLEAN-ACCEPTANCE-008"
status: "USER_APPROVED_ACTIVE"
base_spec: "MARP-GEOLEAN-BASE-008"
plan: "MARP-GEOLEAN-PLAN-008"
created: "2026-06-15"
---

# Guardian Acceptance Spec — v0.4.3

## A. Final claim

Final release may claim only:

```text
V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY
```

No partial claim, experiment harness claim, synthetic-corpus claim, proof-plumbing claim, or v0.4.2 compatibility claim satisfies this acceptance spec.

## B. Required release command

```bash
python scripts/check_release_acceptance_v0_4_3.py \
  --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml \
  --output docs/ai/changes/geometry-full2d-v0_4_3/evidence/release_acceptance_report.json
```

The report must return exit code 0 and contain:

```json
{
  "status": "passed",
  "closure_allowed": true,
  "hard_blockers": [],
  "release_blockers": [],
  "work_debt_open": [],
  "claim_ceiling": "V0.4.3_GEOMETRY_FULL2D_REAL_PIPELINE_READY"
}
```


## C. Required non-empty release report summaries

The final release report must include non-empty values for all of:

```text
checked_rids
metrics_summary
advantage_summary
used_rule_coverage_summary
engine_usage_summary
measured_failure_summary
corpus_summary
actual_pipeline_run_summary
substantive_corpus_summary
review_manifest_summary
baseline_comparability_summary
causal_chain_summary
anti_v042_regression_status
engine_semantic_output_summary
compiler_input_isolation_summary
```

An empty dict, empty list, null, omitted field, or placeholder string is a ReleaseBlocker.

## D. Integrated hardening blockers

The final release checker must enforce all K-001..K-024 blockers. In particular:

```text
K-016 substantive benchmark floors missing or below threshold.
K-017 direct lemma success fraction exceeds 0.20.
K-018 curated provenance self-certified by Codex.
K-019 engine output contains proof text or benchmark dispatch fields.
K-020 compiler reads benchmark labels to decide proof text.
K-021 baseline comparability violated.
K-022 ActualTaskPipelineRunV1 causal_chain_hash missing or invalid.
K-023 v0.4.2 failure regression fixture is missing or not rejected.
K-024 release checker does not enforce K-016..K-023.
```

## E. Required hardening commands

All of the following commands are release-required:

```bash
python scripts/check_full2d_substantive_corpus.py --corpus-root benchmarks/geometry_full2d
python scripts/check_full2d_review_manifest.py --corpus-root benchmarks/geometry_full2d
python scripts/check_full2d_engine_no_proof_text.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_compiler_input_isolation.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_baseline_comparability.py --run-dir runs/geometry_full2d_v0_4_3
python scripts/check_actual_task_pipeline_runs.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_engine_real_execution.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_anti_v042_regression.py
```

Failure of any command is a ReleaseBlocker unless it exposes an unavoidable unsound proof-use path, in which case it is a HardBlocker.

## F. Release report non-empty summaries

The following report fields must be non-empty and computed from actual artifacts:

```text
checked_rids
metrics_summary
advantage_summary
used_rule_coverage_summary
engine_usage_summary
measured_failure_summary
corpus_summary
actual_pipeline_run_summary
```

Empty placeholder objects fail release.

## G. R-ID checklist

### R-AUTH

```text
R-AUTH-001 active Base Spec is MARP-GEOLEAN-BASE-008.
R-AUTH-002 v0.4.2 reports are not accepted as v0.4.3 release evidence.
R-AUTH-003 old specs are marked superseded for release claims.
```

### R-REFRACTOR

```text
R-REF-001 v0.4.2 template artifact path is not used by release matrix.
R-REF-002 no release script maps template_id/theorem_family to proof text.
R-REF-003 no release script fabricates solver refs from task_id/theorem_name/template_id.
R-REF-004 no release matrix applies sidecar overlay without replay-valid ActualTaskPipelineRunV1.
R-REF-005 no v0.4.3 release command imports plugins.geometry_synthetic.
```

### R-EXTRACT

```text
R-EXT-001 each counted success has LeanExtractionReportFull2D.
R-EXT-002 extraction report is theorem-specific and matches source theorem hash.
R-EXT-003 regex_used_for_semantics=false.
R-EXT-004 no fixed smokeStatement is used for counted tasks.
R-EXT-005 side conditions are preserved or reported as obligations/measured failures.
R-EXT-006 measured failures in sampled release metrics have extraction evidence or extraction-backed measured-failure reports.
R-EXT-007 target-outside / malformed negatives used for safe-reject metrics have extraction evidence.
```

### R-CLAIMSPEC

```text
R-CLAIM-001 each counted success has GeometryFull2DClaimSpec.
R-CLAIM-002 target classification is in_target_positive exact_goal.
R-CLAIM-003 nondegeneracy/orientation/order/existence fields are present.
```

### R-PROVIDER

```text
R-PROV-001 each counted success has actual provider.solve run manifest.
R-PROV-002 provider manifest is bound to task_id and claim_spec_ref.
R-PROV-003 engine outputs are content-addressed.
R-PROV-004 real_integration_flag is backed by evidence, not self-attestation.
```

### R-ENGINE

```text
R-ENG-001 every release-critical engine passes challenge suite.
R-ENG-002 every release-critical engine is used by at least one counted certificate.
R-ENG-003 engine output changes under challenge mutations when mathematically expected.
R-ENG-004 no engine branches on release theorem name/template_id.
```

### R-COMPILER

```text
R-COMP-001 compiler consumes actual engine output refs.
R-COMP-002 compiler result includes rule ids and side-condition report.
R-COMP-003 compiler does not read benchmark template_id/theorem_family.
R-COMP-004 LeanPatchCandidateFull2D is created from compiler result.
```

### R-PROOF

```text
R-PROOF-001 proof worker edits only MARP proof region.
R-PROOF-002 source problem proof region contains sorry before patch.
R-PROOF-003 generated candidate contains no sorry/axiom/admit/unsafe target semantics.
R-PROOF-004 FinalVerifyGate compiles generated candidate file.
R-PROOF-005 certificate binds extraction, claimspec, provider, engine, compiler, patch, worker, final verify.
```

### R-CORPUS

```text
R-CORPUS-001 positives >= 3000.
R-CORPUS-002 negatives/target-outside/malformed >= 500.
R-CORPUS-003 external_formal + user_reviewed_human_curated positives >= 900.
R-CORPUS-004 synthetic positives <= 50%.
R-CORPUS-005 near duplicate positives <= 10%.
R-CORPUS-006 exact template duplicate max per theorem family <= 5.
R-CORPUS-007 frozen manifest hash matches final run.
```

### R-METRICS

```text
R-MET-001 metrics are derived from ActualTaskPipelineRunV1 records.
R-MET-002 all family thresholds pass.
R-MET-003 overall final theorem rate >= 0.85.
R-MET-004 in-target positive safe-reject success count = 0.
R-MET-005 measured failures are counted honestly with reasons.
```

### R-ADVANTAGE

```text
R-ADV-001 B2-B1 >= 0.25 overall final theorem rate.
R-ADV-002 B2-B5 >= 0.15 on construction subset.
R-ADV-003 B2-B6 >= 0.15 on algebraic/metric subset.
R-ADV-004 B2-B7 >= 0.10 on order/case subset.
R-ADV-005 B2-B8 >= 0.05 on olympiad-style subset if model provider is used.
```

### R-DEBT

```text
R-DEBT-001 debt ledger exists.
R-DEBT-002 no open ReleaseBlocker entries.
R-DEBT-003 no open WorkDebt entries at closure.
R-DEBT-004 release report reads debt ledger and includes its hash.
```

## H. Anti-gaming tests

Release must run all anti-gaming tests:

```bash
python scripts/check_no_v042_template_release_path.py
python scripts/check_actual_task_pipeline_runs.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_engine_real_execution.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_extraction_corpus.py --corpus-root benchmarks/geometry_full2d --run-dir runs/geometry_full2d_v0_4_3
python scripts/check_full2d_compiler_evidence.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_certificate_binding.py --run-dir runs/geometry_full2d_v0_4_3 --self-test
python scripts/check_full2d_used_rule_coverage.py --run-dir runs/geometry_full2d_v0_4_3
python scripts/check_full2d_matrix_evidence.py --run-dir runs/geometry_full2d_v0_4_3
python scripts/check_full2d_metrics_v0_4_3.py --run-dir runs/geometry_full2d_v0_4_3
```

Any failure blocks release but should not stop unrelated implementation work.

## I. Required negative controls

The checker suite must include negative controls proving release fails when:

```text
1. proof artifact has final_theorem=true but no provider manifest;
2. solver ref is task_id-derived;
3. extraction report theorem_name mismatches task theorem;
4. source theorem is already proved;
5. patch edits outside MARP region;
6. final verify report refers to different candidate file;
7. engine real_integration_flag=true lacks evidence;
8. matrix summary is hand-written without task records;
9. debt ledger contains an open entry;
10. corpus marks Codex-generated tasks as curated without review manifest.
```
