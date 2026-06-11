from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = r"""import LeanGeo.Abbre

open LeanGeo
namespace MathAutoResearch.GeometryFixture

example (A B C : Point) (h : Coll A B C) : Coll A B C := by
  exact h

example (L M : Line) (h : ¬ L.intersectsLine M) : ¬ L.intersectsLine M := by
  exact h

example (A P B : Point) (h : MidPoint A P B) : MidPoint A P B := by
  exact h

example (A B C D : Point) (h : Cyclic A B C D) : Cyclic A B C D := by
  exact h

end MathAutoResearch.GeometryFixture
"""


def _wsl_workspace_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    suffix = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def main() -> int:
    if shutil.which("wsl") is None:
        print("wsl command not found; LeanGeo fixture check requires WSL.", file=sys.stderr)
        return 2

    tmp_dir = ROOT / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    fixture_path = tmp_dir / "LeanGeoFixture.lean"
    fixture_path.write_text(FIXTURE, encoding="utf-8")

    evidence_dir = ROOT / "docs" / "ai" / "changes" / "geometry-lean-v0_3" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    log_path = evidence_dir / "wsl_leangeo_fixture_check.log"

    workspace = _wsl_workspace_path(ROOT)
    command = (
        f"cd {workspace} && "
        'export PATH="$HOME/.elan/bin:$PATH" && '
        "lake env lean .tmp/LeanGeoFixture.lean"
    )
    try:
        result = subprocess.run(
            ["wsl", "-d", "Ubuntu-24.04", "--", "bash", "-lc", command],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=600,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        log_path.write_text(output + "\nTIMEOUT after 600 seconds\n", encoding="utf-8")
        print(output, end="")
        print(f"LeanGeo fixture check timed out; see {log_path}", file=sys.stderr)
        return 124

    output = result.stdout
    if result.returncode == 0:
        output += "PASS: LeanGeo.Abbre fixture elaborated with lake env lean.\n"
    log_path.write_text(output, encoding="utf-8")
    print(output, end="")
    if result.returncode != 0:
        print(f"LeanGeo fixture check failed; see {log_path}", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
