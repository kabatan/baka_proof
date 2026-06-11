---
title: T17 Verification Evidence
task: T17 — GenesisGeo-compatible construction proposer adapter
date: 2026-06-11
status: PASS_PENDING_RC3
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# T17 Verification Evidence

## Implemented Scope

- GenesisGeo-compatible construction proposer fixture adapter.
- Output normalization to an `AuxiliaryConstructionCandidateV1`-shaped candidate ref.
- Candidate records include construction kind, source provenance, introduced objects, dependencies, intended use, side conditions, and `proof_use_status = not_allowed`.
- Raw rationale remains raw provider output and is captured only through manifest raw output hash.
- Resource admission uses the `construction_proposer` semaphore through `ResourceGovernor`.

## Verification

```powershell
cmd /c "set ENGINE_ROLE=construction_proposer&& make smoke-geometry-provider" > docs\ai\changes\geometry-lean-v0_3\evidence\genesis_adapter_smoke.json
cmd /c make test-regression TEST_FILTER=genesis_output_not_proof
cmd /c make test-unit
cmd /c make test-mutation TEST_FILTER=extraction
cmd /c make lean-build
cmd /c make lean-no-sorry
python scripts/check_domain_contamination.py
```

Results:

```text
Genesis adapter smoke: PASS
Regression target: passed
Full unit suite: Ran 52 tests OK
Mutation target: Ran 12 tests OK
Lean root build: Build completed successfully
Lean no-sorry: passed
Domain contamination: passed
```

## Claim Ceiling

This is a GenesisGeo-compatible fixture adapter, not real GenesisGeo installation or integration. Raw rationale and construction candidates are not proof evidence. This does not claim construction compilation, final theorem support, RC-3 PASS, or v0.3 completion.
