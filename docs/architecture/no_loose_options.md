---
title: No Loose Options — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for no-loose-options and exactly-one-selected rules.
authority: Derived documentation; Base Spec R-NOOPT-* and R-V03-EXT-001 are authoritative.
---

# No Loose Options — geometry × Lean v0.3

The core runtime must not accumulate optional modes.

Each run records exactly one selected implementation for each public boundary:

- target library
- model provider set
- research controller plugin
- proof worker plugin
- geometry solver provider
- geometry solver policy
- rule registry
- resource policy
- trust boundary

AgentC/AgentD and A/B/C/D runtime taxonomies are not core modes.
