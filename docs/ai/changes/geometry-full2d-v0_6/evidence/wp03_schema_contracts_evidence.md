---
title: "WP03 Schema Contracts Evidence"
base_spec: "MARP-GEOLEAN-BASE-012"
plan: "MARP-GEOLEAN-PLAN-012"
status: "MECH_WP03_LOCAL_PASS"
---

# WP03 Schema Contracts Evidence

Command:

```bash
python scripts/check_schema_contracts_v0_6.py --self-test --red-cases --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp03_schema_contracts_report.json
```

Result:

```text
status=passed
self_test.status=passed
red_cases.status=passed
errors=[]
```

Scope:

- Implements WP03 only.
- Adds validators for the 16 schema records named in `MARP-GEOLEAN-PLAN-012`.
- Positive fixtures pass for all 16 schema records.
- Negative fixtures reject target-fact provider, naked/target-equivalent derivation, proof text in engine output, provider downstream import, forbidden compiler input, weak final verify, target-as-certificate, report-only causality, label-coded status, stale evidence, and schema-only markers.
- `--red-cases` confirms schema-managed payloads from WP01 red cases are rejected.

Claim ceiling:

WP03 local schema-contract acceptance passed. This is not a claim that downstream pipeline stages exist or pass.
