---
title: Guardian Active Context Seed — geometry × Lean v0.3 implementation revised draft
context_id: MARP-GEOLEAN-ACTIVE-CONTEXT-002
version: v0.2-draft
status: DRAFT_FOR_USER_REVIEW
created: 2026-06-10
base_spec: MARP-GEOLEAN-BASE-002
plan: MARP-GEOLEAN-PLAN-002
---

# Guardian Active Context Seed — geometry × Lean v0.3 implementation revised draft

## Current status

Implementation permission: **missing until user explicitly approves Base Spec and Plan**.

Codex may review and refine these documents. Codex must not implement repository code until approval is recorded in the change evidence directory.

## Current objective

Implement the geometry × Lean initial target of the mathematical automatic research pipeline under Guardian Lane, using:

- Domain-neutral Base pipeline.
- Minimal ProofStateDAG.
- `LeanGeoSubsetV1` as the single target library.
- Base-level `ModelProviderSet` for model replacement.
- `ResearchControllerPlugin` and `ProofWorkerPlugin` as model consumers.
- `geometry_synthetic` plugin.
- Composite `GeometrySolverProvider` with internal Newclid-compatible, GenesisGeo-compatible, and TongGeometry-compatible roles.
- Deterministic `ResourceGovernor` for local PC resource usage.
- Lean final verification as the only authority for `final_theorem`.

## Non-negotiable decisions

1. No AgentC/AgentD core modes or A/B/C/D taxonomy.
2. No loose optional target libraries, providers, trace compilers, or trust bypasses.
3. Exactly one selected implementation per public boundary per run.
4. Codex may bootstrap dependencies, but must log reproducible dependency changes and must not silently substitute target library.
5. Models are not owned by controller/worker plugins; models are injected through `ModelProviderSet`.
6. Base must not know geometry concepts or Newclid/GenesisGeo/TongGeometry names except via generic artifact logs where allowed by schemas.
7. Newclid is the standard symbolic closure role.
8. GenesisGeo is auxiliary construction proposer role.
9. TongGeometry is heavy/exreme search oracle role.
10. All provider engines run through `ResourceGovernor`.
11. Raw model/provider/trace output is never proof evidence.
12. Final theorem requires FinalVerifyGate.

## Read first when implementing

1. `docs/ai/changes/geometry-lean-v0_3/BASE_SPEC.md`
2. `docs/ai/changes/geometry-lean-v0_3/PLAN.md`
3. `docs/ai/changes/geometry-lean-v0_3/source_map.md`
4. Current task section in Plan.
5. Relevant R-IDs and MECHs.

## Current task pointer

Next task after approval: `T00 — Guardian setup and implementation approval gate`.

## Global stop conditions

Stop and request decision if:

- A Base Spec R-ID appears impossible without weakening.
- A second target library seems necessary.
- AgentC/D core modes seem necessary.
- A model must be hard-coded into controller/worker.
- Provider execution cannot be routed through ResourceGovernor.
- Raw provider output must be trusted to pass a task.
- Closure evidence cannot be produced.

## Evidence directory

Default evidence path:

```text
docs/ai/changes/geometry-lean-v0_3/evidence/
```

Long command logs, dependency reports, resource profiles, run reports, and closure evidence should be stored there or under a run-specific evidence directory linked from there.
