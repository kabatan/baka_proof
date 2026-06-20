---
title: "Refactor Directive — GeometryFull2D v0.6 Reviewed Strict"
base_spec: "MARP-GEOLEAN-BASE-012"
status: "USER_APPROVED_ACTIVE"
---

# Refactor Directive v0.6

The v0.6 release path must supersede v0.4.x and draft v0.5 release paths. Old implementations remain only as red-case fixtures.

Remove or isolate from release path:

```text
run_full2d_actual_task_v0_4_*.py
run_full2d_matrix_v0_4_*.py
check_release_acceptance_v0_4_*.py
provider/engine implementations that emit target-as-fact
rule registries with counted identity/direct rules
causality scripts that write failed_as_expected without rerun
B2-only matrix scripts
corpus generators with proof/rule/engine labels
checker whitelist logic for release files
```

Release path must use only v0.6 scripts and plugin modules declared in the active selected implementation manifest.

Refactor order:
1. install v0.6 authority;
2. move old shortcuts into red-case fixtures;
3. implement red-case suite;
4. implement acceptance coverage;
5. implement fresh execution-locked stages;
6. run final fresh release.
