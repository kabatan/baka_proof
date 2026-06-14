# Solver-Backed Problem Sources

This directory is for v0.3B solver-backed proof-repair source problems.

Problem sources may contain `sorry` only inside exact MARP proof-region markers:

```lean
theorem task_name : TARGET := by
  -- MARP_PROOF_REGION_START:task_name
  sorry
  -- MARP_PROOF_REGION_END:task_name
```

These files are inputs to the proof-repair pipeline. They must not be imported by
the normal `lake build` root. Generated solved candidates are written under
`lean/MathAutoResearch/Geometry/Generated/` or an equivalent run artifact
directory and must contain no `sorry`.
