# T03 Evidence — Canonical Package Layout

Task: `T03 — Canonical package and repo skeleton`

Supports:
- `R-REBASE-004`
- `R-REBASE-005`
- Base Spec Section 4 repository anatomy

## Changes

- Removed the tracked top-level `math_auto_research/__init__.py` package shim so the root package no longer shadows `src/math_auto_research`.
- Added `scripts/check_package_layout.py` to fail if a duplicate top-level package exists or if `math_auto_research` imports outside the canonical `src/math_auto_research` tree.
- Added setuptools editable-install metadata in `pyproject.toml` so the canonical `src/` package can be imported by ordinary Python commands.
- Added `*.egg-info/` to `.gitignore` because editable-install metadata is generated.

## Commands

```powershell
python -m pip install -e .
```

Result:

```text
Successfully built math-auto-research
Successfully installed math-auto-research-0.0.0
```

Pip emitted pre-existing environment warnings about an invalid `~ip` distribution in `C:\Users\bakat\miniforge3\Lib\site-packages`; these did not block the editable install.

```powershell
python scripts\check_package_layout.py
```

Result:

```text
package layout check passed: C:\Users\bakat\work\AI_math_research\src\math_auto_research\__init__.py
```

```powershell
python -c "import math_auto_research, pathlib; print(pathlib.Path(math_auto_research.__file__).as_posix())"
```

Result:

```text
C:/Users/bakat/work/AI_math_research/src/math_auto_research/__init__.py
```

## Claim

T03 package-layout acceptance is satisfied. This does not verify any later v0.3 implementation tasks or release readiness.
