from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LeanResult:
    status: str
    stdout: str
    stderr: str
    returncode: int


class LeanPort:
    def __init__(self, lean_executable: str = "lean", lake_executable: str = "lake") -> None:
        self.lean_executable = lean_executable
        self.lake_executable = lake_executable

    def check_file(self, path: Path) -> LeanResult:
        completed = subprocess.run(
            [self.lean_executable, str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        return LeanResult(
            status="passed" if completed.returncode == 0 else "failed",
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
        )

    def build_project(self) -> LeanResult:
        completed = subprocess.run(
            [self.lake_executable, "build"],
            capture_output=True,
            text=True,
            check=False,
        )
        return LeanResult(
            status="passed" if completed.returncode == 0 else "failed",
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
        )
