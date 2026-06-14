---
title: WP-02 Lean facade evidence
status: PASSED
created: 2026-06-15
purpose: Record evidence for the GeometryFull2D Lean facade work package.
authority: Evidence only; does not claim v0.4.2 release completion or full semantic coverage.
---

# WP-02 Lean Facade Evidence

## Scope

WP-02 added the Lean namespace:

```text
MathAutoResearch.GeometryFull2D
```

Implemented modules:

```text
Basic
Incidence
Angle
Metric
Circle
Triangle
Construction
Transformation
Order
Inequality
Tactics
```

The facade imports LeanGeo and aliases core primitives to LeanGeo objects. It does not introduce new `axiom`, `sorry`, `admit`, `unsafe`, `Point := Unit`, or `Coll := True` definitions.

## Verification

```text
python scripts/check_geometry_full2d_facade.py
```

Result:

```text
passed
```

This checker now materializes the local GeometryFull2D Lean modules with `lean -o` before passing, so API mismatches such as nonexistent LeanGeo symbols are caught by WP-02 evidence.

```text
python -m pytest tests/unit/test_geometry_full2d_facade.py -q
```

Result:

```text
1 passed
```

```text
make lean-no-sorry
```

Result:

```text
lean no-sorry check passed
```

```text
make lean-build
```

Result:

```text
Build completed successfully
```

## Claim Ceiling

This closes WP-02 facade setup only. It does not yet satisfy structured extraction, corpus, performance, solver portfolio, proof-use, or release acceptance requirements.
