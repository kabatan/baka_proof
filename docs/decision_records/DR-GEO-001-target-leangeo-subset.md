---
title: DR-GEO-001 — Target LeanGeoSubsetV1
decision_id: DR-GEO-001
status: ACCEPTED
created: 2026-06-11
purpose: Record the v0.3 decision to target LeanGeoSubsetV1.
authority: Decision record; Base Spec R-GEO-001 and R-V03-TARGET-001 are authoritative.
---

# DR-GEO-001 — Target LeanGeoSubsetV1

Decision: The initial geometry target library is exactly `LeanGeoSubsetV1`.

Consequences:

- Mathlib may be a dependency, not a second geometry target.
- Local geometry micro-libraries are not proof targets.
- Release acceptance fails if a theorem is satisfied only by an unmapped toy target.
