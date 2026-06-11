from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ENGINE_ROLES = [
    ("symbolic_closure", "newclid_compatible", "newclid"),
    ("construction_proposer", "genesisgeo_compatible", "genesisgeo"),
    ("heavy_search", "tonggeometry_compatible", "tonggeometry"),
]


def command_version(command: str, args: list[str]) -> tuple[str | None, str]:
    executable = shutil.which(command)
    if executable is None:
        return None, "unavailable"
    try:
        completed = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - defensive reporting
        return executable, f"failed: {exc}"
    output = (completed.stdout or completed.stderr).strip().splitlines()
    return executable, output[0] if output else f"exit {completed.returncode}"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def build_report() -> dict[str, Any]:
    lean_path, lean_version = command_version("lean", ["--version"])
    lake_path, lake_version = command_version("lake", ["--version"])
    packages = []
    for path in [Path("pyproject.toml"), Path("lakefile.lean")]:
        if path.exists():
            packages.append(
                {
                    "name": path.name,
                    "source": "local",
                    "version_or_commit": "workspace",
                    "lock_ref": file_hash(path),
                }
            )
    engines = []
    unresolved = []
    for role, family, command in ENGINE_ROLES:
        executable = shutil.which(command)
        install_status = "installed" if executable else "unavailable"
        engines.append(
            {
                "role": role,
                "family": family,
                "install_status": install_status,
                "version_or_commit": executable or "unavailable",
                "checkpoint_hash": None,
            }
        )
        if install_status != "installed":
            consequence = "blocks_heavy_search" if role == "heavy_search" else "blocks_real_final_theorem"
            unresolved.append({"component": family, "consequence": consequence})
    if lean_path is None or lake_path is None:
        unresolved.append({"component": "lean_lake_toolchain", "consequence": "blocks_real_final_theorem"})
    return {
        "schema_version": "1.0.0",
        "report_id": "dependency_resolution:" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
        "created_at": datetime.now(UTC).isoformat(),
        "os": platform.platform(),
        "python_version": sys.version.split()[0],
        "lean_version": lean_version,
        "lake_version": lake_version,
        "packages": packages,
        "engines": engines,
        "unresolved": unresolved,
        "evidence_refs": [file_hash(Path(__file__))],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    report = build_report()
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    if args.json or not args.output:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
