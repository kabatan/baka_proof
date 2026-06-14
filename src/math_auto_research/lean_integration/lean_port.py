from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from math_auto_research.base.resources.process_runner import run_guarded_process
from math_auto_research.base.resources.resource_budget import ResourceRequest
from math_auto_research.base.resources.resource_governor import ResourceGovernor
from math_auto_research.lean_integration.goal_anchor import GoalAnchor, goal_anchor_for_text
from math_auto_research.lean_integration.lean_error_summary import LeanErrorSummary

_PROJECT_BUILD_CACHE: LeanCompileResult | None = None
_FILE_COMPILE_CACHE: dict[tuple[str, int, int], LeanCompileResult] = {}


@dataclass(frozen=True)
class LeanCompileResult:
    status: str
    stdout: str
    stderr: str
    returncode: int
    resource_usage_report: dict


class LeanPort:
    def __init__(
        self,
        lean_executable: str = "lean",
        lake_executable: str = "lake",
        governor: ResourceGovernor | None = None,
    ) -> None:
        self.lean_executable = shutil.which(lean_executable) or lean_executable
        self.lake_executable = shutil.which(lake_executable) or lake_executable
        self.governor = governor or ResourceGovernor()

    def compile_file(self, path: Path, budget: ResourceRequest | None = None) -> LeanCompileResult:
        resolved_path = Path(path).resolve()
        try:
            stat = resolved_path.stat()
            cache_key = (str(resolved_path), int(stat.st_mtime_ns), int(stat.st_size))
        except FileNotFoundError:
            cache_key = None
        if cache_key is not None and cache_key in _FILE_COMPILE_CACHE:
            return _FILE_COMPILE_CACHE[cache_key]
        request = budget or ResourceRequest(component="lean_file", engine_role="lean_build", budget="tiny", timeout_sec=120)
        if Path("lakefile.lean").exists():
            command = [self.lake_executable, "env", "lean", str(path)]
        else:
            command = [self.lean_executable, str(path)]
        report = run_guarded_process(command, request, self.governor)
        result = self._compile_result(report)
        if cache_key is not None:
            _FILE_COMPILE_CACHE[cache_key] = result
        return result

    def check_file(self, path: Path) -> LeanCompileResult:
        return self.compile_file(path)

    def build_project(self, budget: ResourceRequest | None = None) -> LeanCompileResult:
        global _PROJECT_BUILD_CACHE
        if _PROJECT_BUILD_CACHE is not None:
            return _PROJECT_BUILD_CACHE
        request = budget or ResourceRequest(component="lean_build", engine_role="lean_build", budget="small", timeout_sec=120)
        report = run_guarded_process([self.lake_executable, "build"], request, self.governor)
        _PROJECT_BUILD_CACHE = self._compile_result(report)
        return _PROJECT_BUILD_CACHE

    def extract_goals(self, path: Path, theorem_name: str) -> list[GoalAnchor]:
        text = path.read_text(encoding="utf-8")
        return [goal_anchor_for_text(text, theorem_name, path)]

    def summarize_errors(self, result: LeanCompileResult) -> LeanErrorSummary:
        return LeanErrorSummary(status=result.status, stderr_tail=result.stderr[-2000:], stdout_tail=result.stdout[-2000:])

    def _compile_result(self, report: dict) -> LeanCompileResult:
        return LeanCompileResult(
            status="passed" if report["exit_status"] == "completed" else "failed",
            stdout=report.get("stdout_tail", ""),
            stderr=report.get("stderr_tail", ""),
            returncode=0 if report["exit_status"] == "completed" else 1,
            resource_usage_report=report,
        )


def _is_within_workspace(path: Path) -> bool:
    try:
        path.resolve().relative_to(Path.cwd().resolve())
        return True
    except ValueError:
        return False
