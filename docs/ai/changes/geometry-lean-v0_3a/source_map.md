---
title: Guardian Source Map — geometry x Lean v0.3A
source_map_id: MARP-GEOLEAN-SOURCEMAP-003A
version: v0.3A-recovery-admitted
status: SUPERSEDED_BY_MARP-GEOLEAN-BASE-007
created: 2026-06-12
base_spec: MARP-GEOLEAN-BASE-003A
plan: MARP-GEOLEAN-PLAN-003A
purpose: Map v0.3A amendment requirements to the user recovery instruction and v0.3 blocker evidence.
authority: Non-authoritative traceability aid.
---

# Guardian Source Map — geometry x Lean v0.3A

## Source Inventory

| ID | Source | Kind | Availability | Notes |
|---|---|---|---|---|
| A1 | `C:/Users/bakat/Downloads/v03_completion_blocker_response_instructions.md` | user recovery instruction | present | Defines `V0.3A_REAL_INTEGRATION_RECOVERY`, scope, Base Spec amendment, Plan amendment, resource policy, claim rules, and acceptance checklist. |
| A2 | `docs/ai/changes/geometry-lean-v0_3/evidence/v03_completion_blocker_report.md` | blocker report | present | Defines completion blockers accepted by A1 as claim-ceiling report. |
| A3 | `docs/ai/changes/geometry-lean-v0_3/CLOSURE.md` | fixture closure | present | Records current fixture-level claim ceiling and blocked real integrations. |
| A4 | `docs/ai/archive/geometry_pre_v0_4_2/specs/MARP-GEOLEAN-BASE-003A.md` | candidate Base amendment | present after this prep | Correctness authority after admission. |
| A5 | `docs/ai/archive/geometry_pre_v0_4_2/plans/MARP-GEOLEAN-PLAN-003A.md` | candidate Plan amendment | present after this prep | Execution contract after admission. |

## Requirement Mapping

| Requirement | Sources | Mapping note |
|---|---|---|
| `R-ENV-REAL-001` | A1 | Agent-owned reproducible dependency bootstrap and required evidence. |
| `R-ENV-REAL-002` | A1, A2 | Missing dependency is a completion blocker, not a recovery-work stop condition. |
| `R-PROVIDER-REAL-001` | A1 | Single Base-visible provider boundary and internal engine roles. |
| `R-PROVIDER-REAL-002` | A1 | Mandatory ProviderRunManifest and fixture/real flags. |
| `R-RESOURCE-REAL-001` | A1 | ResourceGovernor required for all real provider processes. |
| `R-CORPUS-REAL-001` | A1, A2, A3 | Limited `LeanGeoSubsetV1.RealSmokeCorpus`, not arbitrary LeanGeo support. |
| `R-CLAIM-REAL-001` | A1, A2, A3 | Claim ceiling discipline before and after v0.3A. |
| `R-REAL-NEWCLID-001` | A1, A2, A3 | Real Newclid-compatible symbolic closure recovery. |
| `R-REAL-GENESISGEO-001` | A1, A2, A3 | Real GenesisGeo-compatible construction proposer recovery. |
| `R-REAL-TONGGEOMETRY-001` | A1, A2, A3 | Real TongGeometry-compatible heavy-search recovery. |

## Explicit Scope Decisions

| Blocker | v0.3A decision |
|---|---|
| `B-V03-REAL-NEWCLID` | In scope. |
| `B-V03-REAL-GENESISGEO` | In scope. |
| `B-V03-REAL-TONGGEOMETRY` | In scope with strict resource control. |
| `B-V03-LEANGEO-CORPUS` | Partially in scope as limited `LeanGeoSubsetV1.RealSmokeCorpus`. |
| `B-V03-LEVEL2-REAL-ADVANTAGE` | Out of scope; later evaluation target. |
