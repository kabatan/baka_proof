---
title: "Refactor Directive — GeometryFull2D v0.4.3 Real Pipeline Recovery"
status: "USER_APPROVED_ACTIVE"
base_spec: "MARP-GEOLEAN-BASE-008"
---

# Refactor Directive — v0.4.3

## 1. Delete, archive, or remove from release path

The following v0.4.2 patterns must not remain in release path:

```text
- template_id -> proof replacement mapping;
- theorem_family -> proof replacement mapping;
- task_id -> normalized solver ref generation;
- proof artifact overlay without ActualTaskPipelineRunV1;
- smoke-only extraction as release evidence;
- Codex-generated curated corpus counted as human-curated;
- generated RuleRegistry count used as capability evidence without used-rule certificate coverage;
- release report with empty summaries.
```

Existing files may remain only if renamed or guarded as non-release compatibility utilities.

## 2. Specific files requiring rewrite or quarantine

Codex must audit and either rewrite or quarantine:

```text
scripts/build_full2d_proof_artifact_batch.py
scripts/run_full2d_matrix.py
scripts/check_full2d_metrics.py
scripts/check_release_acceptance_v0_4_2.py
scripts/check_v0_4_2_progress_acceptance.py
scripts/extract_geometry_full2d_statement.py
scripts/check_structured_extraction_v0_4_2.py
benchmarks/geometry_full2d/corpus_manifest.json
plugins/geometry_full2d/engines/*.py
plugins/geometry_full2d/rule_registry.py
```

## 3. Replacement release files

Required v0.4.3 release files:

```text
scripts/check_release_acceptance_v0_4_3.py
scripts/run_full2d_matrix_v0_4_3.py
scripts/check_no_v042_template_release_path.py
scripts/check_actual_task_pipeline_runs.py
scripts/check_full2d_engine_real_execution.py
scripts/check_full2d_extraction_corpus.py
scripts/check_full2d_claimspec_v0_4_3.py
scripts/check_full2d_compiler_evidence.py
scripts/check_full2d_certificate_binding.py
scripts/check_full2d_used_rule_coverage.py
scripts/check_full2d_matrix_evidence.py
scripts/check_full2d_metrics_v0_4_3.py
plugins/geometry_full2d/run_records.py
plugins/geometry_full2d/extraction_pipeline.py
plugins/geometry_full2d/claim_spec_v0_4_3.py
plugins/geometry_full2d/provider_v0_4_3.py
plugins/geometry_full2d/compilers/
plugins/geometry_full2d/engines/
```

## 4. Refactor acceptance

```bash
python scripts/check_no_v042_template_release_path.py
python scripts/check_release_acceptance_v0_4_3.py --config configs/benchmark_runs/geometry_full2d_v0_4_3.yaml
```

Release must fail until all real pipeline requirements are satisfied.



## 5. Additional integrated anti-gaming refactors

The following must also be removed from release paths or rewritten before release:

```text
- any engine output schema that permits proof_text, tactic_script, lean_patch, proof_region_replacement_text, exact_lemma_application, template dispatch fields, theorem-family dispatch fields, or task-id dispatch fields;
- any compiler code path that reads template_id, theorem_family, difficulty_tier, provenance, or benchmark labels to choose proof text;
- any corpus importer that lets Codex self-certify tasks as user_reviewed_human_curated;
- any baseline config that disables FinalVerifyGate, ProofWorker, source theorem visibility, or Lean library access except where that is the explicitly named ablation;
- any ActualTaskPipelineRunV1 implementation without causal_chain_hash recomputation;
- any release acceptance path that omits K-016..K-024.
```

These are not patch requirements; they are part of the v0.4.3 release refactor itself.
