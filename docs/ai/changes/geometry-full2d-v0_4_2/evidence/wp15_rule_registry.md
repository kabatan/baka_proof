---
title: WP-15 rule registry evidence
status: PASSED
created: 2026-06-15
purpose: Record evidence for the GeometryFull2D rule registry floor work package.
authority: Evidence only; does not claim final release coverage or counted-success rule usage.
---

# WP-15 Rule Registry Evidence

## Scope

WP-15 added `RuleRegistryFull2D` with:

```text
150 concrete rule contracts
30 rule families
30 construction templates
20 side-condition discharge procedures
```

Each counted registry rule declares input/output patterns, required side conditions, generated obligations, Lean template/lemma reference, proof template, unsupported variants, and positive/negative/mutation fixtures.

## Verification

```text
python scripts/check_full2d_rule_registry.py
```

Result:

```text
passed
rule_count=150
rule_family_count=30
construction_template_count=30
side_condition_procedure_count=20
```

```text
python -m pytest tests/unit/test_geometry_full2d_rule_registry.py -q
```

Result:

```text
3 passed
```

```text
python scripts/check_v0_4_2_progress_acceptance.py --config configs/benchmark_runs/geometry_full2d_v0_4_2.yaml --output docs/ai/changes/geometry-full2d-v0_4_2/evidence/progress_acceptance_report.json
```

Result:

```text
completed_work_packages includes WP-15:rule-registry-checker-passed
work_debt=[]
```

## Claim Ceiling

This closes the registry floor only. Counted-success usage floors still require WP-06 through WP-14 engine/compiler/final-verification artifacts and final release acceptance.
