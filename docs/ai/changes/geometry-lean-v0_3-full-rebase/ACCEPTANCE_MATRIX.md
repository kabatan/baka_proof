---
title: "Acceptance Matrix — geometry × Lean v0.3 full rebase"
version: "v0.3-full-rebase"
spec_id: "MARP-GEOLEAN-BASE-004"
plan_id: "MARP-GEOLEAN-PLAN-004"
status: "USER_APPROVED_ACTIVE_WITH_V0_3A_PATCH"
created: "2026-06-12"
---

# Acceptance Matrix

This matrix gives Codex and reviewers a concise way to check that Base Spec requirements are implemented.

| Area | Required evidence | Required command |
|---|---|---|
| Approved Guardian docs | BASE_SPEC, PLAN, SOURCE_MAP, REFACTOR_DIRECTIVE, ACCEPTANCE_MATRIX installed under change folder | `test -f docs/ai/changes/geometry-lean-v0_3-full-rebase/BASE_SPEC.md` |
| Old specs removed | root old draft specs gone, hash index exists | `python scripts/check_old_specs_removed.py` |
| Package layout | canonical `src/math_auto_research` only | `python scripts/check_package_layout.py` |
| Base/plugin separation | Base has no geometry imports or engine names | `python scripts/check_domain_contamination.py` |
| No loose options | no AgentC/D core modes, scalar SelectedImplementations | `python scripts/check_no_loose_options.py` |
| Models injectable | ModelProviderSet slots, no hard-coded GPT/Codex/DeepResearch | `python scripts/check_model_hardcode.py && make smoke-model-provider-set` |
| Resource governance | ResourceGovernor, ProcessRunner, semaphores, timeout | `make smoke-resource-governor && python scripts/check_resource_bypass.py` |
| Dependency bootstrap | DependencyResolutionReport emitted | `make smoke-env-bootstrap` |
| LeanGeo target | TargetLibraryManifest exactly LeanGeoSubsetV1 | `python -m math_auto_research.cli.report_target_library_status` |
| ProofStateDAG | Obligation/Derivation/EvidenceRef, GraphPatch-only mutation | `make test-unit TEST_FILTER=proof_state` |
| FinalVerifyGate | protected theorem hash, no sorry, no forbidden axioms | `make smoke-geometry-final-verify` |
| Extraction | semantic extraction, safe reject, relation classification | `make smoke-geometry-extraction && make test-mutation TEST_FILTER=extraction` |
| Real Newclid | Newclid-compatible adapter smoke, real report | `make smoke-real-newclid` |
| Real GenesisGeo | construction proposer smoke, raw rationale non-proof | `make smoke-real-genesisgeo` |
| Real TongGeometry | heavy search smoke, resource gated | `make smoke-real-tonggeometry` |
| GeoTrace/RuleRegistry | side-condition calculus and fixtures | `make test-mutation TEST_FILTER=rule_registry` |
| TraceCompiler | unsupported/malformed trace blockers | `make smoke-geometry-trace` |
| ConstructionCompiler | side-condition obligations and blockers | `make smoke-geometry-construction` |
| Trust safety | raw model/provider/DSL cannot close proof | `make test-regression TEST_FILTER=raw` |
| Fixture misuse | no fixture provider in release config | `python scripts/check_no_fixture_release.py` |
| Level2 pilot | B0-B5 matrix runs and produces metrics | `make smoke-level2-pilot` |
| Replay | reproducibility report generated | `python scripts/generate_repro_report.py --run-dir runs/<RUN_ID>` |
| Release acceptance | all blockers checked | `python scripts/check_release_acceptance.py --config configs/benchmark_runs/geometry_level2_pilot.yaml` |

## Claim matrix

| Claim | Required conditions |
|---|---|
| `schemas/contracts implemented` | schema tests pass |
| `real Newclid integrated` | dependency report installed/vendored + `make smoke-real-newclid` |
| `real GenesisGeo integrated` | dependency report installed/vendored + `make smoke-real-genesisgeo` |
| `real TongGeometry integrated` | dependency report installed/vendored + `make smoke-real-tonggeometry` |
| `specific Lean theorem proved` | FinalVerifyReport for that theorem |
| `V0.3_FULL_IMPLEMENTED_EXPERIMENT_READY` | all release blockers absent + Level2 pilot run/replay |
| `Level2 advantage observed` | metrics show improvement; not implied by experiment-ready |
| `arbitrary LeanGeo support` | disallowed by this spec |
| `open problem solved` | disallowed by this spec |
