---
title: "Refactor Directive — GeometryFull2D v0.4.5"
base_spec: "MARP-GEOLEAN-BASE-010"
---

# Refactor Directive — v0.4.5

The following current or historical paths are forbidden in v0.4.5 release entrypoints and may remain only as regression fixtures:

```text
scripts/generate_full2d_v0_4_4_corpus.py
scripts/run_full2d_actual_task_v0_4_4.py
scripts/check_solver_causality_reports_v0_4_4.py
scripts/generate_full2d_external_projection_corpus.py
scripts/run_full2d_matrix_v0_4_3.py
scripts/run_full2d_matrix.py
scripts/build_full2d_proof_artifact_batch.py
```

Release entrypoints must be v0.4.5-specific and must not import v0.4.4/v0.4.3 release logic.

Forbidden release code patterns:

```text
_proof_from_shape
_proof_from_source
target_expr.startswith
baseline == "B2" leading to success
family == "Construction450" leading to B5 failure
solver_causal_necessity = final_status == "final_theorem"
mutation_sensitive = final_status == "final_theorem"
normalized_output_ref derived from task_id/theorem_name/template_id/used_rules selected by compiler
```

Required replacement architecture:

```text
provider/engine -> EngineOutputFull2D -> SelectedSolverDerivationV1 -> compiler -> patch -> proof worker -> FinalVerifyGate -> certificate -> destructive reruns
```

Any shortcut found after implementation must be treated as ReleaseBlocker, not silently grandfathered.
