---
title: Closure — geometry x Lean v0.3A real integration recovery
version: v0.3A-release-candidate
status: FINAL_REVIEWS_PENDING
created: 2026-06-12
base_spec: MARP-GEOLEAN-BASE-003A
plan: MARP-GEOLEAN-PLAN-003A
authority: Evidence-bound closure candidate; final claim requires final spec, quality, and Guardian boundary review.
---

# Closure — geometry x Lean v0.3A

## Scope

Recovery target: `V0.3A_REAL_INTEGRATION_RECOVERY`.

This closure candidate covers the admitted v0.3A recovery tasks T-001 through T-010 and the recorded RC-003A review gates.

This closure does not mark any R-ID `VERIFIED`.

## Evidence

Primary evidence:

- `evidence/t001_fixture_preservation.md`
- `evidence/t002_dependency_bootstrap.md`
- `evidence/t003_resource_governor_enforcement.md`
- `evidence/t004_composite_provider_v1.md`
- `evidence/t005_real_newclid_symbolic_closure.md`
- `evidence/t006_genesisgeo_construction_diagnostic.md`
- `evidence/t007_tonggeometry_heavy_search_diagnostic.md`
- `evidence/t008_real_smoke_corpus.md`
- `evidence/t009_real_vs_fixture_integration_tests.md`
- `evidence/t010_release_acceptance.md`
- `evidence/v03a_release_acceptance_report.json`

Review artifacts:

- `evidence/guardian_boundary_review.md`
- `evidence/rc003a_1_guardian_boundary_review.md`
- `evidence/rc003a_2_guardian_boundary_review.md`
- `evidence/rc003a_3_guardian_boundary_review.md`
- `evidence/rc003a_4_guardian_boundary_review.md`

Run artifacts:

- `runs/v03a_t002_apply_latest/dependency_probe.json`
- `runs/v03a_t002_apply_latest/dependency_resolution_report.json`
- `runs/v03a_t005_newclid_latest/real_newclid_provider_smoke.json`
- `runs/v03a_t006_genesisgeo_latest/construction_smoke.json`
- `runs/v03a_t007_tonggeometry_latest/heavy_search_smoke.json`
- `runs/v03a_t008_real_smoke_corpus_latest/corpus_check.json`

## Acceptance Evidence

The v0.3A acceptance checker passed:

```text
python scripts\check_v03a_release_acceptance.py
```

The inherited v0.3 release acceptance command also passed:

```text
python scripts\check_release_acceptance.py --config configs\benchmark_runs\geometry_level2_smoke.yaml
```

## Current Pre-Final Claim Ceiling

Until final reviews pass, this closure candidate says:

```text
The track has fixture-level release acceptance only.
Real Newclid / GenesisGeo / TongGeometry integration remains unverified.
Real LeanGeo corpus support remains unverified.
Real Level 2 advantage remains unverified and out of scope for this recovery target.
```

## Supported Claim After Final Review

If final reviews pass, the maximum supported claim is:

```text
The geometry x Lean pipeline has real-integration evidence for the selected provider roles and limited LeanGeoSubsetV1.RealSmokeCorpus under the recorded trust boundary.
```

Details:

- Newclid-compatible symbolic closure has a non-fixture real smoke path with raw output normalized to `GeoTraceV1 | Diagnostic`, `ProviderRunManifest`, and `ResourceUsageReport`.
- GenesisGeo-compatible construction proposal has an external diagnostic engine-run path, but model-backed construction proposal remains unproven.
- TongGeometry-compatible heavy search has an external diagnostic engine-run path under the heavy-search policy, but model-backed heavy search remains unproven.
- `LeanGeoSubsetV1.RealSmokeCorpus` is a limited one-entry smoke corpus with direct Lean final-verification evidence for the admitted entry.
- Fixture adapters and fixture tests remain as regressions.

## Explicit Non-Claims

This closure does not support:

- arbitrary LeanGeo theorem support;
- broad geometry automation;
- open-problem solving;
- real Level 2 advantage;
- model-backed GenesisGeo construction proposal;
- model-backed TongGeometry heavy search;
- whole-provider real-integration claims from mixed fixture/real runs;
- production safety;
- `SOURCE_FAITHFUL`;
- `ACCEPTANCE_COMPLETE`;
- any R-ID `VERIFIED` status.

## Closure Statement

This is a release-candidate closure pending final reviews. It becomes the v0.3A final closure only if spec verifier, quality reviewer, and Guardian boundary final review pass under the claim ceiling above.
