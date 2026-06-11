---
title: ProofStateDAG — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for the domain-neutral ProofStateDAG integration.
authority: Derived documentation; Base Spec R-DAG-* and R-V03-DAG-001 are authoritative.
---

# ProofStateDAG — geometry × Lean v0.3

Core node types remain:

- `Obligation`
- `Derivation`
- `EvidenceRef`

Plugins mutate DAG state only through `GraphPatch` and `DAGWriter`.

A target theorem obligation closes only through a proof-use derivation with `proof_use_status = final_theorem`, closed side conditions, valid `FinalVerifyReport`, and unchanged protected theorem statement hash.
