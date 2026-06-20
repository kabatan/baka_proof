# WP05 Provider and Engine Isolation Evidence

Status: MECH evidence regenerated after Guardian review BLOCK; pending re-review.

Commands executed on a fresh run directory:

```bash
python scripts/check_full2d_extraction_corpus_v0_6.py --corpus-root benchmarks/geometry_full2d_v0_6 --run-dir runs/wp05_v0_6_fresh --self-test --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp05_extraction_prereq_report.json
python scripts/check_full2d_claimspec_v0_6.py --run-dir runs/wp05_v0_6_fresh --self-test --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp05_claimspec_prereq_report.json
python scripts/check_provider_isolation_v0_6.py --run-dir runs/wp05_v0_6_fresh --red-cases --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp05_provider_isolation_report.json
python scripts/check_engine_output_not_from_compiler_rules_v0_6.py --run-dir runs/wp05_v0_6_fresh --red-cases --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp05_engine_output_report.json
```

Observed results:

- Extraction prerequisite: `status=passed`, `required_task_count=3`, `report_count=3`.
- ClaimSpec prerequisite: `status=passed`, `claim_spec_count=3`.
- Provider isolation: `status=passed`, `provider_manifest_count=3`, `engine_output_count=21`, no forbidden provider imports.
- Engine output origin check: `status=passed`, all seven v0.6 engine roles observed, 21 engine output records checked.
- Red cases checked by WP05 gates: `RC-019`, `RC-001`, `RC-005`, `RC-014`, and `K-010`.
- Full red-case suite after RC-019 expansion: `status=passed`, `red_case_count=22`.
- Schema contracts after WP05 schema/checker changes: `status=passed`.

Corrective changes after initial review block:

- Provider artifacts no longer derive selected artifact content from `target_hash`; artifact seeds and payloads are bound to typed objects, normalized hypotheses, and side conditions.
- Each selected artifact now includes `algorithm`, `input_context`, `trace_steps`, and role-specific structured payload (`construction_payload`, `certificate_payload`, `cases`, `fact_payload`, or `trace_payload`).
- Provider import scanning now rejects compiler, rule registry, proof generation, proof worker, final verify, matrix, release, corpus, previous/prior release, proof template, and v0.4/v0.5 modules.
- `runs/wp05_v0_6_fresh/provider_stage_order_witness_v0_6.json` records provider output paths and proves no compiler-stage artifacts were present at provider completion in the WP05 fresh run.

Scope note:

WP05 produces provider-stage `EngineOutputFull2D` records before WP06 independent checkers run. Therefore `independent_checker_refs` is allowed to be empty at this stage only. WP06 must attach and validate `IndependentSolverArtifactCheckV1(status=passed)` for every selected solver artifact before any `SelectedSolverDerivationV3` can be built.
