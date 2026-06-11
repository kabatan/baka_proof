---
title: LeanGeo Source Inspection Evidence
task: RC-2 dependency/source inspection
date: 2026-06-11
status: OBSERVED
authority: Evidence record only; does not override Base Spec or Plan.
---

# LeanGeo Source Inspection Evidence

Inspected upstream repository:

- `https://github.com/project-numina/LeanGeo`
- observed HEAD: `9212b89ef0cb08adb049b32f6332a1f2b9e551ab`

Observed dependency/toolchain:

- `lean-toolchain`: `leanprover/lean4:v4.15.0`
- `lakefile.lean` requires pinned `mathlib`, `lean-smt`, `checkdecls`, and `doc-gen4`
- `lakefile.lean` check script requires external `smt-portfolio`, `z3`, and `cvc5`

Observed LeanGeo/SystemE names used to ground the current extractor fixtures:

- primitive sorts: `Point`, `Line`, `Circle`
- relations/abbreviations: `Coll`, `Cyclic`, `MidPoint`, `PerpLine`, `Foot`
- constructions: `line_from_points`, `circle_from_points`, `intersection_lines`
- metric/angle notations present in source/readme: `|(A─B)|`, `∠ A:B:C`

Claim ceiling:

- This inspection grounds scaffold fixtures in upstream names.
- It does not prove LeanGeo builds locally or that Lean elaboration is integrated.
