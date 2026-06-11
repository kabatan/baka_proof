---
title: DR-GEO-005 — Auxiliary Construction Contract
decision_id: DR-GEO-005
status: ACCEPTED
created: 2026-06-11
purpose: Record the v0.3 decision to standardize auxiliary construction candidates.
authority: Decision record; Base Spec R-AUX-* and R-V03-AUX-001 are authoritative.
---

# DR-GEO-005 — Auxiliary Construction Contract

Decision: Auxiliary construction proposals are typed `AuxiliaryConstructionCandidateV1` artifacts, not natural-language proof evidence.

Supported v0.3 proof-use construction kinds are deliberately restricted and must pass `ConstructionCompiler`, `ProofWorker`, and `FinalVerifyGate`.
