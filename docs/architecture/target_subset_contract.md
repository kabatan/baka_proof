---
title: TargetSubsetContract — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for the v0.3 TargetSubsetContract.
authority: Derived documentation; Base Spec R-V03-TARGET-001 is authoritative.
---

# TargetSubsetContract — geometry × Lean v0.3

This document tracks the target-subset architecture required by `R-V03-TARGET-001`.

Required components:

- `LeanGeoSubsetV1TheoremGrammar`
- predicate, construction, and relation mappings
- `GeometryExtractionContract`
- `GeometryExtractionReport`
- `GeometryClaimSpec`
- fixtures and safe-reject policy

Implementation must preserve the proof-use rule that `GeometryClaimSpec` cannot exist in a proof-use path without accepted `GeometryExtractionReport` provenance.
