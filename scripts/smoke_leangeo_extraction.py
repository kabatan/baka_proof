from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from plugins.geometry_synthetic.extraction import GeometryExtractor


LEAN_FIXTURE = r"""import LeanGeo.Abbre

open LeanGeo
namespace MathAutoResearch.GeometryFixture

theorem fixture_collinear (A B C : Point) (h : Coll A B C) : Coll A B C := by
  exact h

#check MathAutoResearch.GeometryFixture.fixture_collinear

end MathAutoResearch.GeometryFixture
"""


def _wsl_workspace_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    suffix = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{suffix}"


def _run_lean_check() -> tuple[int, str]:
    tmp_dir = ROOT / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    fixture_path = tmp_dir / "LeanGeoExtractionSmoke.lean"
    fixture_path.write_text(LEAN_FIXTURE, encoding="utf-8")
    local_lake = Path.home() / ".elan" / "bin" / ("lake.exe" if sys.platform == "win32" else "lake")
    lake = local_lake if local_lake.exists() else Path("lake")
    if shutil.which(str(lake)) is not None or local_lake.exists():
        completed = subprocess.run(
            [str(lake), "env", "lean", str(fixture_path.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        return completed.returncode, completed.stdout
    if shutil.which("wsl") is None:
        return 2, "wsl command not found; LeanGeo extraction smoke requires WSL.\n"
    workspace = _wsl_workspace_path(ROOT)
    command = (
        f"cd {workspace} && "
        'export PATH="$HOME/.elan/bin:$PATH" && '
        "lake env lean .tmp/LeanGeoExtractionSmoke.lean"
    )
    try:
        completed = subprocess.run(
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
        return 124, output + "\nTIMEOUT after 600 seconds\n"
    return completed.returncode, completed.stdout


def main() -> int:
    evidence_dir = ROOT / "docs" / "ai" / "changes" / "geometry-lean-v0_3-full-rebase" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    lean_log = evidence_dir / "wsl_leangeo_check_output.log"
    smoke_json = evidence_dir / "leangeo_extraction_smoke.json"

    returncode, output = _run_lean_check()
    lean_log.write_text(output, encoding="utf-8")
    if returncode != 0:
        print(output, end="")
        print(f"LeanGeo extraction smoke failed before extraction; see {lean_log}", file=sys.stderr)
        return returncode

    report, claim = GeometryExtractor().extract_lean_check_output(
        output,
        source_goal_ref="lean-check:MathAutoResearch.GeometryFixture.fixture_collinear",
        elaboration_report_ref=str(lean_log.relative_to(ROOT)).replace("\\", "/"),
    )
    payload = {"lean_output": output, "report": report.to_dict(), "claim": claim.to_dict() if claim else None}
    smoke_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if report.status != "accepted" or claim is None:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
