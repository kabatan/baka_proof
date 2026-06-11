---
title: v0.3 Completion Blocker Report
date: 2026-06-12
status: BLOCKED_FOR_FULL_V0_3_COMPLETION
base_spec: MARP-GEOLEAN-BASE-003
plan: MARP-GEOLEAN-PLAN-003
authority: Blocker report; does not mark R-IDs VERIFIED and does not expand the final claim ceiling.
---

# v0.3 Completion Blocker Report

## Summary

The geometry x Lean v0.3 Guardian track is blocked from a full v0.3 completion claim.

The admitted final state is fixture-level release acceptance only:

- final release acceptance passed for the recorded fixture scope;
- final spec verifier, quality reviewer, and Guardian boundary reviewer passed within that claim ceiling;
- real Newclid/GenesisGeo/TongGeometry integrations remain unavailable;
- arbitrary LeanGeo theorem support, real Level 2 advantage, `SOURCE_FAITHFUL`, `ACCEPTANCE_COMPLETE`, `PRODUCTION_SAFE`, v0.3 completion, and R-ID VERIFIED claims remain disallowed.

## Blocker Classification

Blocker type: external integration and evidence ceiling.

Severity: completion-blocking for any full v0.3 claim.

Current admitted status: `FINAL_REVIEW_PASSED_FIXTURE_LEVEL`.

Not blocked: fixture-level schemas/contracts, extraction fixtures, provider/resource fixtures, compiler/construction fixtures, bridge/trust guards, worker-applied standard-loop final-verification fixture, run trace/replay fixture, and Level 2 smoke matrix fixture.

Blocked: full v0.3 completion claim and real-integration claims.

## Blocking Items

### B-V03-REAL-NEWCLID

Component: `newclid_compatible`

Evidence:

- `dependency_probe.json`: `install_status = unavailable`
- `dependency_probe.json`: unresolved consequence `blocks_real_final_theorem`
- `CLOSURE.md`: blocks real final theorem support beyond the Newclid-compatible symbolic fixture adapter

Impact:

- The pipeline cannot claim real Newclid-backed symbolic closure.
- The pipeline cannot claim real final theorem support through Newclid-compatible integration.

Exit criteria:

- Install or vendor a supported Newclid-compatible engine.
- Record version/commit/checkpoint hash in dependency evidence.
- Replace fixture-only adapter path with real integration evidence.
- Add tests that fail without the real integration path and pass with it.
- Re-run release acceptance and Guardian/spec/quality reviews.

### B-V03-REAL-GENESISGEO

Component: `genesisgeo_compatible`

Evidence:

- `dependency_probe.json`: `install_status = unavailable`
- `dependency_probe.json`: unresolved consequence `blocks_real_final_theorem`
- `CLOSURE.md`: blocks real final theorem support beyond the GenesisGeo-compatible construction fixture adapter

Impact:

- The pipeline cannot claim real GenesisGeo-backed construction proposal.
- The pipeline cannot claim real final theorem support through GenesisGeo-compatible integration.

Exit criteria:

- Install or vendor a supported GenesisGeo-compatible component.
- Record version/commit/checkpoint hash in dependency evidence.
- Replace fixture-only construction proposal path with real integration evidence.
- Add tests that fail without the real integration path and pass with it.
- Re-run release acceptance and Guardian/spec/quality reviews.

### B-V03-REAL-TONGGEOMETRY

Component: `tonggeometry_compatible`

Evidence:

- `dependency_probe.json`: `install_status = unavailable`
- `dependency_probe.json`: unresolved consequence `blocks_heavy_search`
- `CLOSURE.md`: blocks real heavy-search support beyond the TongGeometry-compatible fixture adapter

Impact:

- The pipeline cannot claim real TongGeometry-backed heavy search.
- The pipeline cannot claim real Level 2 search behavior beyond fixture counts.

Exit criteria:

- Install or vendor a supported TongGeometry-compatible heavy-search component.
- Record version/commit/checkpoint hash in dependency evidence.
- Replace fixture-only heavy-search path with real integration evidence.
- Add tests and benchmark evidence that fail without the real search path and pass with it.
- Re-run release acceptance and Guardian/spec/quality reviews.

### B-V03-LEANGEO-CORPUS

Component: LeanGeo theorem corpus support

Evidence:

- `CLOSURE.md`: full LeanGeo theorem-corpus support remains outside the current evidence ceiling.
- `final_guardian_boundary_review.md`: arbitrary LeanGeo theorem support is a forbidden overclaim.

Impact:

- The pipeline cannot claim arbitrary LeanGeo theorem support.
- Current Lean evidence is limited to LeanGeo.Abbre extraction fixtures and one local worker-applied final-verification fixture.

Exit criteria:

- Define the supported LeanGeo theorem corpus/subset as an approved Base Spec amendment or new Base Spec.
- Add extraction, compilation, and final-verification evidence across that subset.
- Add regression/mutation tests covering corpus-level failure modes.
- Re-run source-fidelity, spec, quality, and Guardian boundary reviews.

### B-V03-LEVEL2-REAL-ADVANTAGE

Component: real Level 2 advantage claim

Evidence:

- `CLOSURE.md`: real Level 2 advantage beyond fixture counts is disallowed.
- `final_guardian_boundary_review.md`: real Level 2 advantage beyond fixture counts is a forbidden overclaim.

Impact:

- The Level 2 smoke matrix can support fixture-level accounting only.
- It cannot support a real benchmark advantage or research-performance claim.

Exit criteria:

- Define the benchmark population and statistical acceptance criteria.
- Run non-fixture benchmark evaluations with reproducible artifacts.
- Show replayable counts and failure accounting.
- Re-run release acceptance and final reviews under the expanded claim target.

## Required Recovery Path

1. Decide whether full v0.3 completion means real engine integration, LeanGeo corpus support, real Level 2 advantage, or all of these.
2. Update or supersede the approved Base Spec and Plan before implementation.
3. Resolve the dependency blockers with concrete installed/vendored components and recorded versions/hashes.
4. Replace fixture-only paths with real integration paths while preserving fixture tests.
5. Add tests and benchmarks that can distinguish fixture behavior from real integration behavior.
6. Re-run release acceptance.
7. Re-run spec verifier, quality reviewer, and Guardian boundary reviewer.

## Current Claim Ceiling

Allowed:

- The geometry x Lean v0.3 Guardian track passed fixture-level release acceptance and final reviews for the recorded fixture scope.

Not allowed:

- full v0.3 completion;
- real Newclid/GenesisGeo/TongGeometry integration;
- arbitrary LeanGeo theorem support;
- broad geometry automation or open-problem solving;
- real Level 2 advantage beyond fixture counts;
- `SOURCE_FAITHFUL`, `ACCEPTANCE_COMPLETE`, `PRODUCTION_SAFE`, or R-ID VERIFIED claims.
