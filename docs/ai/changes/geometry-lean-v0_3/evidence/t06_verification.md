---
title: T06 Verification Evidence
task: T06 — ProofStateDAG core
date: 2026-06-11
status: PASS
authority: Evidence record only; does not override Base Spec or Plan.
---

# T06 Verification Evidence

## Scope

Implemented the Base ProofStateDAG core:

- core node records: `Obligation`, `Derivation`, and `EvidenceRef`;
- `GraphPatch` as the only mutation input;
- `DAGWriter` validation for patch schema, duplicate IDs, references, final theorem trust preconditions, invalidation, and acyclicity;
- `StateReader` closure summaries;
- regression coverage that diagnostic/provider-style output cannot close a target obligation;
- source scan coverage that the ProofStateDAG core has no geometry-specific terms.

## Commands

```powershell
python -m unittest tests.unit.test_proof_state_dag tests.unit.test_domain_contamination
```

Result:

```text
Ran 6 tests in 0.002s
OK
```

```powershell
python -m unittest discover -s tests/unit -p "test_*.py"
```

Result:

```text
Ran 15 tests in 0.171s
OK
```

```powershell
cmd /c make test-unit
```

Result:

```text
Ran 15 tests in 0.157s
OK
```

## Notes

The Plan's filtered commands (`make test-unit TEST_FILTER=proof_state` and `make test-regression TEST_FILTER=domain_contamination`) are not yet separately implemented by the repository-local `make.bat`; the current unit suite includes equivalent T06 tests.

This task does not claim Lean verification, geometry extraction, provider correctness, or release completion.
