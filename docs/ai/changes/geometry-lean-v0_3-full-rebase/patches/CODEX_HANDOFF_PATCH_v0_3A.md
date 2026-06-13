---
title: "Codex handoff prompt — apply v0.3A patch"
patch_id: "MARP-GEOLEAN-CODEX-HANDOFF-004A"
status: "USER_APPROVED_HANDOFF_GUIDANCE"
created: "2026-06-13"
installed: "2026-06-13"
approval_evidence: "docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/v0_3a_patch_import.md"
---

# Codex handoff prompt — apply v0.3A patch

Use this as the next Codex task prompt after user approval.

```text
You are working in kabatan/baka_proof under Guardian governance.

Authority:
- Existing authority: docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md
- Existing plan: docs/ai/changes/geometry-lean-v0_3-full-rebase/PLAN.md
- New approved patch: docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/BASE_SPEC_PATCH_v0_3A.md
- New approved plan patch: docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/PLAN_PATCH_v0_3A.md
- New acceptance patch: docs/ai/changes/geometry-lean-v0_3-full-rebase/patches/ACCEPTANCE_PATCH_v0_3A.md

Task:
Implement v0.3A patch completely. Do not only resolve the TongGeometry checkpoint blocker. The current repo also has an inadequate corpus, a fixture-derived matrix, and a fixture standard loop that must not satisfy release acceptance.

Mandatory implementation order:
1. Install patch docs and record v0_3a_deviation_audit.md.
2. Update dependency report schema and probe scripts with code/model status split and claim impact.
3. Refactor provider implementation into plugins/geometry_synthetic/providers/** with provider.py facade only.
4. Harden TongGeometry smoke and claim profile:
   - code-backed diagnostic path is required for core v0.3;
   - model-backed claim requires tokenizer/lm_s/lm_l/cls and model_inference_status=available;
   - if checkpoints are unavailable after public discovery, mark admitted_unavailable_external_artifact and continue core v0.3 work.
5. Replace the Level2 corpus with a nontrivial LeanGeoSubsetV1 corpus satisfying R-EVAL-005.
6. Implement run_task(...) release path for real benchmark tasks. run_fixture/build_fixture_run must not appear in release matrix path.
7. Rewrite Level2 matrix so it executes all task/baseline pairs and derives metrics from per-task artifacts.
8. Harden release acceptance with blockers 26–34.
9. Run all verification commands.
10. Produce closure that separately reports:
    - V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY
    - V0.3_TONGGEOMETRY_MODEL_BACKED_HEAVY_SEARCH_READY

Non-negotiable constraints:
- Do not reintroduce AgentC/D core modes.
- Do not add a second target library.
- Do not use local toy geometry as release target.
- Do not trust raw Newclid/GenesisGeo/TongGeometry output as proof.
- Do not satisfy the corpus floor by metadata labels alone.
- Do not satisfy the matrix by formula metrics.
- Do not fabricate Tong checkpoints.
- Do not stop merely because Tong checkpoints are unavailable; record admitted-unavailable external artifact status and continue core experiment-ready work.

Expected new files:
- scripts/check_dependency_claim_profile.py
- scripts/check_dependency_report_model_status.py
- scripts/check_level2_corpus_nontrivial.py
- scripts/check_matrix_artifact_derived.py
- scripts/check_no_fixture_standard_loop_release.py
- scripts/check_provider_layout.py

Expected updated files:
- scripts/probe_dependencies.py
- scripts/run_tonggeometry_probe.py
- scripts/check_release_acceptance.py
- src/math_auto_research/workflow/release_acceptance.py
- plugins/geometry_synthetic/evaluation.py
- plugins/geometry_synthetic/standard_loop.py or src/math_auto_research/workflow/standard_geometry_loop.py
- benchmarks/leangeo/RealSmokeCorpus.lean
- benchmarks/geometry/geometry_level2_pilot.jsonl

Final commands:
make test
make test-regression
make test-mutation
make lean-build
make lean-no-sorry
python scripts/probe_dependencies.py --json --output docs/ai/changes/geometry-lean-v0_3-full-rebase/evidence/dependency_resolution.json
python scripts/check_dependency_claim_profile.py
python scripts/check_level2_corpus_nontrivial.py
python scripts/run_geometry_level2_matrix.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
python scripts/check_matrix_artifact_derived.py --run-dir runs/geometry_level2_pilot
python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml
```
