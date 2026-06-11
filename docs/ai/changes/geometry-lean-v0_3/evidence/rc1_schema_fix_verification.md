---
title: RC-1 Schema Stability Fix Verification
task: RC-1 blocker remediation
date: 2026-06-11
status: PASS_PENDING_REVIEW
authority: Evidence record only; does not override Base Spec or Plan.
---

# RC-1 Schema Stability Fix Verification

## Blocker Addressed

The first RC-1 Guardian boundary review blocked because public contract schemas were placeholders and tests only checked file existence. This remediation replaces placeholder public contract schemas with contract-index definitions that record, per v0.3 public contract:

- required fields;
- provenance/ref fields;
- status fields;
- proof-use fields;
- allowed status/proof-use values where constrained by v0.3.

The schema tests now fail if an inventory contract lacks a concrete contract definition, lacks `schema_version` where required for serialized public records, lacks provenance/status/proof-use metadata, or allows final theorem proof-use through geometry provider/trace/construction outputs.

## Commands

```powershell
python -m unittest tests.unit.test_schema_validation
```

Result:

```text
Ran 5 tests in 0.059s
OK
```

```powershell
cmd /c make test-unit
```

Result:

```text
Ran 19 tests in 0.220s
OK
```

```powershell
python scripts/check_domain_contamination.py
```

Result:

```text
domain contamination check passed
```

```powershell
python scripts/check_no_loose_options.py
```

Result:

```text
no loose options check passed
```

## Claim Ceiling

This evidence supports re-review of RC-1 schema stability only. It does not claim implementation of later task behavior, Lean verification, real provider integration, or v0.3 release completion.
