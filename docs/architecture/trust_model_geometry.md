---
title: Trust Model — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for v0.3 geometry trust levels and BridgeGate rules.
authority: Derived documentation; Base Spec R-V03-TRUST-001 is authoritative.
---

# Trust Model — geometry × Lean v0.3

Trust levels:

- `diagnostic_only`
- `extracted_claim`
- `raw_provider_result`
- `checked_trace`
- `construction_candidate_checked`
- `lean_patch_candidate`
- `lean_compiled`
- `final_theorem`

Only `final_theorem` from `FinalVerifyGate` may close a target theorem.
