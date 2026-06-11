---
title: Guardian Source Map — geometry × Lean v0.3
source_map_id: MARP-GEOLEAN-SOURCEMAP-003
version: v0.3-admission-candidate
status: SOURCE_FIDELITY_REVIEW_PASSED_PENDING_USER_IMPLEMENTATION_APPROVAL
created: 2026-06-10
last_updated: 2026-06-11
base_spec: MARP-GEOLEAN-BASE-003
plan: MARP-GEOLEAN-PLAN-003
purpose: Map Base Spec R-IDs to source units and record source availability.
authority: Non-authoritative traceability aid; the Base Spec is the correctness authority after admission and user approval.
---

# Guardian Source Map — geometry × Lean v0.3

This file maps requirements in `MARP-GEOLEAN-BASE-003` to their sources. It is not the authority for correctness; the Base Spec is.

## Source inventory

| ID | Source | Kind | Workspace availability | Notes |
|---|---|---|---|---|
| S1 | `geometry_lean_pipeline_plan_v0_3.md` | project design | present | v0.3 geometry × Lean architecture; TargetSubsetContract / CompilerContract / RunTraceContract. |
| S2 | `fatal_risks_1_2_3_geometry_lean_review.md` | red-team review | referenced by S1/drafts; not present | Semantic extraction, TraceCompiler side-condition calculus, one target library. Claims to S2 are inherited through S1/draft text unless the file is later supplied. |
| S3 | `geometry_lean_pipeline_review_v0_2_revised.md` | red-team review | referenced by S1/drafts; not present | AuxiliaryConstructionCandidateV1, RuleRegistryV1, theorem grammar, ProviderRunManifest, attribution logging. Claims to S3 are inherited through S1/draft text unless the file is later supplied. |
| S4 | `math_auto_research_pipeline_final_repo_plan_v1_2.md` | parent architecture | referenced by S1/drafts; not present | Domain-neutral Base, minimal ProofStateDAG, ArtifactStore separation, GraphPatch-only mutation, raw solver result not proof. Claims to S4 are inherited through S1/draft text unless the file is later supplied. |
| S5 | User decisions in conversation, 2026-06-10 and 2026-06-11 | authoritative user decisions | present in thread only | Remove AgentC/D core taxonomy, enable dependency bootstrap by Codex, make model providers swappable, use Newclid/GenesisGeo/TongGeometry, plan local PC resources carefully; 2026-06-11 request authorizes Guardian document completion/review but not code implementation. |
| S6 | `using-spec-guardian` skill and AGENTS instructions | Guardian reference | present in thread/local skill | Spec-driven planning, guarded execution, evidence-bound closure. |

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
| R-V03-DOC-001 | S1 | Exact v0.3 repository documentation and decision-record anatomy. |
| R-V03-SCHEMA-001 | S1 | Exact v0.3 public contract schema families and required field coverage. |
| R-V03-TARGET-001 | S1 | Exact TargetSubsetContract components, fixtures, mappings, extraction provenance, and relation-to-goal policy. |
| R-V03-MODEL-001 | S1 | Exact ResearchControllerPlugin, ProofWorkerPlugin, ActionPlan, WorkOrder, and WorkerResult boundaries. |
| R-V03-RUN-001 | S1 | Exact ControllerStrategyLog, ResearchContributionRecord, RunRecord, DAG/log separation, and replay requirements. |
| R-V03-SOLVER-001 | S1 | Exact GeometrySolveRequest, GeometrySolverPolicy, GeometryExecutionPlan, ProviderRunManifest, and ProviderResult details. |
| R-V03-COMPILER-001 | S1 | Exact GeoTraceV1, TraceChecker, RuleRegistryV1, SideConditionReport, TraceCompiler, and mutation requirements. |
| R-V03-AUX-001 | S1 | Exact v0.3 auxiliary construction kinds, candidate/check/compiler fields, and unsupported-kind policy. |
| R-V03-DAG-001 | S1 | Exact ProofStateDAG integration patterns and closure rule. |
| R-V03-TRUST-001 | S1 | Exact GeometryBridgeGate, GeometryBridgeReport, trust levels, and TrustGuard rules. |
| R-V03-WORKFLOW-001 | S1 | Exact 20-step standard proof loop and five main workflows. |
| R-V03-EVAL-001 | S1 | Exact Level 2 evaluation target, baseline matrix, metrics, EvaluationFunnel, and ReproducibilityReport. |
| R-V03-TEST-001 | S1 | Exact v0.3 CI, mutation, release blocker, and final checklist coverage. |
| R-V03-EXT-001 | S1, S5, S6 | Guardrail that local execution extensions must not alter v0.3 semantics. |

## Decisions explicitly changed from previous draft

| Previous draft item | New decision |
|---|---|
| `QD-001` blocks LeanGeo package absence | Retired. Codex may bootstrap dependencies; failure is recorded in `DependencyResolutionReport`. |
| GPT-Pro/Codex/DeepResearch hidden inside controller/worker plugin | Replaced by Base-level `ModelProviderSet`; controller/worker are model consumers. |
| Solver providers described mostly abstractly | Composite provider roles specified: Newclid symbolic closure, GenesisGeo construction proposer, TongGeometry heavy search. |
| Resource policy under-specified | `ResourceGovernor`, local resource probe, per-engine semaphores, timeout/kill policy, and resource reports are required. |
| Base Spec summarized v0.3 detailed contracts | Added `R-V03-*` source-fidelity overlay so schema fields, workflows, release blockers, and final checklist items from v0.3 remain required. |
