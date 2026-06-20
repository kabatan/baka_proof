---
title: "WP02 Acceptance Coverage Evidence"
base_spec: "MARP-GEOLEAN-BASE-012"
plan: "MARP-GEOLEAN-PLAN-012"
status: "MECH_WP02_LOCAL_PASS"
---

# WP02 Acceptance Coverage Evidence

Command:

```bash
python scripts/check_acceptance_coverage_v0_6.py --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp02_acceptance_coverage_report.json
```

Result:

```text
status=passed
covered_K=K-001..K-035
errors=[]
red_case_suite_status=passed
```

Scope:

- Implements WP02 only.
- Adds `docs/ai/changes/geometry-full2d-v0_6/evidence/acceptance_coverage_map.json`.
- Adds `scripts/check_acceptance_coverage_v0_6.py`.
- Checks that every mapped checker appears in the v0.6 Acceptance required-checker list.
- Checks that `RC-009 RedCase_CheckerOmission` and `RC-010 RedCase_CheckerWhitelist` are rejected by the v0.6 red-case suite.

Claim ceiling:

WP02 local acceptance passed. This is not a release checker implementation claim and does not prove downstream stage checkers exist or pass.
