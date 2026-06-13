---
title: "Source Map — geometry × Lean v0.3 full rebase"
version: "v0.3-full-rebase"
spec_id: "MARP-GEOLEAN-BASE-004"
plan_id: "MARP-GEOLEAN-PLAN-004"
status: "USER_APPROVED_ACTIVE_WITH_V0_3A_PATCH"
created: "2026-06-12"
---

# Source Map

This file maps source decisions to the Base Spec and Plan.

## 1. Source hierarchy

1. User decisions in the current conversation are EXACT.
2. `docs/ai/changes/geometry-lean-v0_3-full-rebase/source/geometry_lean_pipeline_plan_v0_3.md` is a source architecture document, not implementation authority.
3. `v03_completion_blocker_report.md` is a blocker/evidence-ceiling report.
4. Guardian docs provide process style only; they do not define this project’s technical requirements.

The following filenames were present in the research-agent draft bundle text as background references, but the files are not currently present in this workspace and are not used as source-fidelity authority for this admission packet:

```text
fatal_risks_1_2_3_geometry_lean_review.md
math_auto_research_pipeline_final_repo_plan_v1_2.md
```

If those files are later supplied, they may be imported as additional non-authoritative source evidence only after a separate source-map update and Guardian boundary review.

## 2. Exact user decisions mapped to R-IDs

| User decision | R-IDs |
|---|---|
| v0.3 must be fully implemented, not fixture-level | `INV-009`, `R-TEST-003`, release blockers |
| Base Spec and Plan must leave no interpretation room | all R-IDs; especially `R-SCHEMA-*`, `R-TEST-*` |
| Drifted current repo specs should be deleted/refactored, not preserved | `R-REBASE-*` |
| Base pipeline and plugin must be separated | `INV-001`, `INV-003`, `R-BASE-*`, `R-SOLVER-*` |
| Environment setup should be done by Codex, not treated as a question | `R-ENV-*`, `MECH-BOOT-001` |
| Models must be externally swappable | `R-MODEL-*`, `MECH-MODEL-001` |
| Newclid/GenesisGeo/TongGeometry should be used as synthetic solvers | `R-SOLVER-002` to `R-SOLVER-006` |
| Local PC resources must be planned carefully | `R-RSRC-*`, `MECH-RSRC-001` |
| AgentC/D optional modes should not exist | `INV-002`, `R-REBASE-*`, release blockers |
| Target is geometry × Lean with LeanGeoSubsetV1 | `R-GEO-*`, `R-EXTRACT-*` |

## 3. Blocker report mapped to new requirements

The previous blocker report identified fixture-level ceiling and missing real integrations. This maps to:

| Blocker | New requirement |
|---|---|
| real Newclid unavailable | `R-SOLVER-003`, `make smoke-real-newclid`, release blocker 11 |
| real GenesisGeo unavailable | `R-SOLVER-004`, `make smoke-real-genesisgeo`, release blocker 11 |
| real TongGeometry unavailable | `R-SOLVER-005`, `make smoke-real-tonggeometry`, release blocker 11 |
| LeanGeo corpus absent | `R-EVAL-001`, `T18`, release blocker 23 |
| real Level2 advantage disallowed | `R-EVAL-004`: experiment-ready does not overclaim positive advantage |

## 4. Fatal risks mapped to new requirements

| Fatal risk | New requirement |
|---|---|
| Lean theorem to DSL extraction is semantic, not parser-only | `R-EXTRACT-*`, `T19`, `T20` |
| TraceCompiler is core research and must be deterministic | `R-RULE-*`, `R-TRACE-*`, `T26`, `T27` |
| Multiple target libraries are dangerous | `INV-008`, `R-GEO-001`, release blocker 4 |

## 5. v1.2 principles adapted

| v1.2 principle | Geometry adaptation |
|---|---|
| domain-neutral Base | `INV-001`, `R-BASE-*` |
| minimal ProofStateDAG | `R-DAG-*` |
| artifact separation | `R-BASE-001`, `R-DAG-*` |
| plugin GraphPatch-only mutation | `INV-004`, `R-DAG-005` |
| raw solver result not proof-use | `INV-005`, `R-TRUST-*` |
| Lean final verification authority | `INV-006`, `R-LEAN-004` |
| evaluation/reproducibility logs | `R-EVAL-*`, `T34`, `T35` |

## 6. Non-authoritative documents after approval

After approval, the following may be cited only as historical source/evidence, not as instructions:

```text
geometry_lean_guardian_BASE_SPEC_draft_v0_2.md
geometry_lean_guardian_PLAN_draft_v0_2.md
docs/ai/changes/geometry-lean-v0_3-full-rebase/source/geometry_lean_pipeline_plan_v0_3.md
previous CLOSURE.md files
previous fixture-level acceptance reports
```
