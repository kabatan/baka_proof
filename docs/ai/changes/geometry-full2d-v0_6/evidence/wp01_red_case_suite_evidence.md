---
title: "WP01 Red Case Suite Evidence"
base_spec: "MARP-GEOLEAN-BASE-012"
plan: "MARP-GEOLEAN-PLAN-012"
status: "MECH_WP01_LOCAL_PASS"
---

# WP01 Red Case Suite Evidence

Command:

```bash
python scripts/check_red_case_suite_v0_6.py --all --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp01_red_case_suite_report.json
```

Result:

```text
status=passed
all_rejected=true
red_case_count=22
expected_red_case_count=22
errors=[]
evidence_ref=sha256:d041739bcce5fcaa6091373a6be1d01e728b25281a1c399c25342475131890f4
```

Scope:

- Implements WP01 only.
- Fixes v0.6 red-case and K-level fixtures under `tests/red_cases/geometry_full2d_v0_6/`.
- Adds `scripts/check_red_case_suite_v0_6.py --all`.
- Does not implement provider, compiler, rule registry, matrix, corpus expansion, or release acceptance.

Claim ceiling:

WP01 local acceptance passed. This is not a full-pipeline completion claim.
