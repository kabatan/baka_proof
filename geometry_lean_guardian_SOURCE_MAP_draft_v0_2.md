---
title: Guardian Source Map — geometry × Lean v0.3 implementation revised draft
source_map_id: MARP-GEOLEAN-SOURCEMAP-002
version: v0.2-draft
status: DRAFT_FOR_USER_REVIEW
created: 2026-06-10
base_spec: MARP-GEOLEAN-BASE-002
plan: MARP-GEOLEAN-PLAN-002
---

# Guardian Source Map — geometry × Lean v0.3 implementation revised draft

This file maps requirements in `MARP-GEOLEAN-BASE-002` to their sources. It is not the authority for correctness; the Base Spec is.

## Source inventory

| ID | Source | Kind | Notes |
|---|---|---|---|
| S1 | `geometry_lean_pipeline_plan_v0_3.md` | project design | v0.3 geometry × Lean architecture; TargetSubsetContract / CompilerContract / RunTraceContract. |
| S2 | `fatal_risks_1_2_3_geometry_lean_review.md` | red-team review | Semantic extraction, TraceCompiler side-condition calculus, one target library. |
| S3 | `geometry_lean_pipeline_review_v0_2_revised.md` | red-team review | AuxiliaryConstructionCandidateV1, RuleRegistryV1, theorem grammar, ProviderRunManifest, attribution logging. |
| S4 | `math_auto_research_pipeline_final_repo_plan_v1_2.md` | parent architecture | Domain-neutral Base, minimal ProofStateDAG, ArtifactStore separation, GraphPatch-only mutation, raw solver result not proof. |
| S5 | User decisions in conversation, 2026-06-10 | authoritative user decisions | Remove AgentC/D core taxonomy, enable dependency bootstrap by Codex, make model providers swappable, use Newclid/GenesisGeo/TongGeometry, plan local PC resources carefully. |
| S6 | `https://github.com/kabatan/guardian` | Guardian reference | Spec-driven planning, guarded execution, evidence-bound closure. |

## Requirement mapping

| R-ID | Sources | Mapping note |
|---|---|---|
| R-GUARD-001..003 | S6, S5 | Guardian Lane authority and approval flow. |
| R-ARCH-001..003 | S1, S4, S5 | Base/plugin separation adapted from parent architecture. |
| R-NOOPT-001..003 | S1, S5 | No loose optional components; exactly-one selected implementations. |
| R-ENV-001..003 | S5, S6 | User authorized reproducible dependency bootstrap; Guardian evidence required. |
| R-MODEL-001..003 | S5 | ModelProviderSet promoted to Base-level boundary. |
| R-RSRC-001..006 | S5 | Local PC resource planning for Newclid/GenesisGeo/TongGeometry composite solver. |
| R-DAG-001..003 | S1, S4 | Minimal DAG and GraphPatch-only mutation. |
| R-LEAN-001, R-VERIFY-001 | S1, S2 | Lean final verification and protected theorem statement. |
| R-GEO-001..002 | S1, S2, S3 | Single target library and theorem grammar. |
| R-EXTRACT-001..002 | S1, S2 | Extraction-first proof-use path and semantic extraction. |
| R-SOLVER-001..003 | S1, S5 | Composite solver provider, Base-visible single provider, deterministic policy. |
| R-ENGINE-001 | S5, prior research discussion | Newclid-compatible symbolic closure as primary integration target. |
| R-ENGINE-002 | S5, prior research discussion | GenesisGeo-compatible construction proposer. |
| R-ENGINE-003 | S5, prior research discussion | TongGeometry-compatible heavy-search oracle. |
| R-RULE-001, R-TRACE-001 | S2, S3 | RuleRegistry side-condition calculus and narrow TraceCompiler. |
| R-AUX-001..002 | S3 | AuxiliaryConstructionCandidateV1 and ConstructionCompiler. |
| R-TRUST-001..002 | S1, S4 | Raw output not proof; result levels. |
| R-BRIDGE-001 | S1, S2 | Lightweight but mandatory geometry BridgeGate. |
| R-RUN-001..003 | S3, S5 | ProviderRunManifest, controller strategy logging, resource usage. |
| R-EVAL-001 | S1, S3, S5 | Level 2 domain-tool advantage evaluation. |
| R-TEST-001 | S1, S2, S3, S4 | Regression/mutation tests. |
| R-CLAIM-001 | S6, S5 | Evidence-bound allowed claims. |

## Decisions explicitly changed from previous draft

| Previous draft item | New decision |
|---|---|
| `QD-001` blocks LeanGeo package absence | Retired. Codex may bootstrap dependencies; failure is recorded in `DependencyResolutionReport`. |
| GPT-Pro/Codex/DeepResearch hidden inside controller/worker plugin | Replaced by Base-level `ModelProviderSet`; controller/worker are model consumers. |
| Solver providers described mostly abstractly | Composite provider roles specified: Newclid symbolic closure, GenesisGeo construction proposer, TongGeometry heavy search. |
| Resource policy under-specified | `ResourceGovernor`, local resource probe, per-engine semaphores, timeout/kill policy, and resource reports are required. |
