---
title: T03 Verification
created: 2026-06-11
status: PASS_WITH_UNRESOLVED_PROVIDER_ENGINES
purpose: Verify dependency bootstrap reporting and DependencyResolutionReport schema.
authority: Evidence only.
---

# T03 Verification

Commands:

- `python scripts/probe_dependencies.py --json --output docs\\ai\\changes\\geometry-lean-v0_3\\evidence\\dependency_probe.json` -> PASS.
- `cmd /c make smoke-env-bootstrap` -> PASS.
- `python -m math_auto_research.cli.validate_artifact docs\\ai\\changes\\geometry-lean-v0_3\\evidence\\dependency_probe.json` -> PASS.

Detected toolchain:

- Python: 3.12.11
- Lean: Lean (version 4.30.0, x86_64-w64-windows-gnu, commit d024af099ca4bf2c86f649261ebf59565dc8c622, Release)
- Lake: Lake version 5.0.0-src+d024af0 (Lean version 4.30.0)

Unresolved components:

- newclid_compatible: blocks_real_final_theorem
- genesisgeo_compatible: blocks_real_final_theorem
- tonggeometry_compatible: blocks_heavy_search

No target-library substitution was made. Real provider integration claims remain blocked where unresolved components require them.
