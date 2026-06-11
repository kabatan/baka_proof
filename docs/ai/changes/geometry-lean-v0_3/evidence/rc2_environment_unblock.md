---
title: RC-2 Environment Unblock Evidence
task: RC-2 — target subset and extraction
date: 2026-06-11
status: PASS_PENDING_REVIEW
authority: Evidence record only; does not override Base Spec, Plan, or reviewer decisions.
---

# RC-2 Environment Unblock Evidence

## User Authorization

The user explicitly authorized environment changes, including Lean install/update/downgrade/uninstall if needed, to reach the simplest working setup for v0.3.

## Toolchain

- Repository toolchain pinned in `lean-toolchain`: `leanprover/lean4:v4.15.0`.
- Windows Elan installed and used by `make.bat` when `%USERPROFILE%\.elan\bin\lean.exe` exists.
- WSL Ubuntu-24.04 Elan installed with `leanprover/lean4:v4.15.0`.
- `lakefile.lean` now pins LeanGeo from `https://github.com/project-numina/LeanGeo.git` at commit `9212b89ef0cb08adb049b32f6332a1f2b9e551ab`.
- `lake-manifest.json` records LeanGeo package name `lib` and transitive dependencies.

## Evidence

- `wsl_lake_update_leangeo.log`: WSL `lake update` completed under Lean 4.15.
- `wsl_lake_build_leangeo_target.log`: full `lake build LeanGeo` progressed through `SystemE` and `LeanGeo.Abbre` before the long build was stopped; no RC-2 claim depends on full LeanGeo theorem corpus build.
- `wsl_leangeo_fixture_check.log`: `lake env lean .tmp/LeanGeoFixture.lean` passed for a minimal fixture importing `LeanGeo.Abbre` and elaborating `Point`, `Line`, `Coll`, `MidPoint`, `Cyclic`, and line intersection negation.
- `wsl_leangeo_check_output.log`: WSL `lake env lean` emitted a real Lean `#check` signature for a LeanGeo.Abbre theorem fixture.
- `leangeo_extraction_smoke.json`: `make smoke-geometry-extraction` produced `GeometryClaimSpec` from the real Lean `#check` signature, not from a manually populated context.

## Native Windows Limitation

Native Windows full LeanGeo dependency build is not currently the primary path because LeanGeo's transitive `lean-cvc5` release used by this pin provides Linux/macOS static archives but no Windows static archive. Windows remains usable for the repository's own Lean root build through Elan 4.15.

## Claim Ceiling

This evidence supports re-review of RC-2 semantic extraction from a real LeanGeo.Abbre elaborated `#check` signature. It does not claim full LeanGeo theorem-corpus build, solver integration, RC-2 PASS, or v0.3 completion without reviewer acceptance.
