from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PREFIX = "MARP_CANONICAL_GEOMETRY_STATEMENT_JSON="
LOCAL_LEAN_MODULES = [
    "MathAutoResearch.GeometryFull2D.Basic",
    "MathAutoResearch.GeometryFull2D.Incidence",
    "MathAutoResearch.GeometryFull2D.Angle",
    "MathAutoResearch.GeometryFull2D.Metric",
    "MathAutoResearch.GeometryFull2D.Circle",
    "MathAutoResearch.GeometryFull2D.Triangle",
    "MathAutoResearch.GeometryFull2D.Construction",
    "MathAutoResearch.GeometryFull2D.Transformation",
    "MathAutoResearch.GeometryFull2D.Order",
    "MathAutoResearch.GeometryFull2D.Inequality",
    "MathAutoResearch.GeometryFull2D.Tactics",
    "MathAutoResearch.GeometryFull2D.Extraction",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-file", default="lean/MathAutoResearch/GeometryFull2D/ExtractionSmoke.lean")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload = extract_statement(Path(args.lean_file))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def extract_statement(lean_file: Path) -> dict[str, Any]:
    lean_file = Path(lean_file)
    _ensure_local_lean_artifacts()
    command = [_lake(), "env", "lean", "-R", "lean", str(lean_file)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=_browser_suppressed_env(),
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Lean extraction command failed:\n"
            + completed.stdout[-2000:]
            + completed.stderr[-2000:]
        )
    for line in completed.stdout.splitlines():
        if line.startswith(JSON_PREFIX):
            return json.loads(line[len(JSON_PREFIX) :])
    raise RuntimeError("Lean extraction command did not emit CanonicalGeometryStatementV1 JSON")


def _ensure_local_lean_artifacts() -> None:
    for module_name in LOCAL_LEAN_MODULES:
        source = ROOT / "lean" / Path(*module_name.split(".")).with_suffix(".lean")
        olean = ROOT / ".lake" / "build" / "lib" / Path(*module_name.split(".")).with_suffix(".olean")
        ilean = ROOT / ".lake" / "build" / "lib" / Path(*module_name.split(".")).with_suffix(".ilean")
        if _artifact_is_current(source, olean):
            continue
        olean.parent.mkdir(parents=True, exist_ok=True)
        command = [_lake(), "env", "lean", "-R", "lean", str(source), "-o", str(olean), "-i", str(ilean)]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=_browser_suppressed_env(),
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Lean local artifact build failed for {module_name}:\n"
                + completed.stdout[-2000:]
                + completed.stderr[-2000:]
            )


def _artifact_is_current(source: Path, olean: Path) -> bool:
    return olean.exists() and olean.stat().st_mtime >= source.stat().st_mtime


def _lake() -> str:
    elan_lake = Path.home() / ".elan" / "bin" / ("lake.exe" if os.name == "nt" else "lake")
    if elan_lake.exists():
        return str(elan_lake)
    return shutil.which("lake") or "lake"


def _browser_suppressed_env() -> dict[str, str]:
    env = os.environ.copy()
    env["BROWSER"] = f"{sys.executable} -c \"import sys; sys.exit(0)\""
    no_browser_path = str((ROOT / "scripts" / "no_browser_sitecustomize").resolve())
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = no_browser_path if not existing_pythonpath else os.pathsep.join([no_browser_path, existing_pythonpath])
    return env


if __name__ == "__main__":
    raise SystemExit(main())
