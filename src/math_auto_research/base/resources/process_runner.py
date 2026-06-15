from __future__ import annotations

import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRequest
from math_auto_research.base.resources.resource_governor import ResourceGovernor


def run_guarded_process(
    command: list[str],
    request: ResourceRequest,
    governor: ResourceGovernor,
    *,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    started_at = time.time()
    start_monotonic = time.monotonic()
    with governor.admit(request):
        process_report = run_process_group(command, timeout_sec=request.timeout_sec, env=env)
    ended_at = time.time()
    wall = time.monotonic() - start_monotonic
    exit_status = "killed" if process_report["timed_out"] else "completed" if process_report["returncode"] == 0 else "failed"
    return {
        "schema_version": "1.0.0",
        "report_id": f"resource_usage:{time.time_ns()}",
        "run_id": "local_smoke",
        "role": request.engine_role if request.engine_role != "none" else request.component,
        "engine_role": request.engine_role,
        "admission_status": "admitted",
        "started_at": str(started_at),
        "ended_at": str(ended_at),
        "exit_status": exit_status,
        "component": request.component,
        "budget": request.budget,
        "queue_wait_sec": 0,
        "wall_time_sec": round(wall, 6),
        "cpu_time_sec": 0,
        "peak_rss_mb": 0,
        "gpu_vram_peak_mb": None,
        "timeout_status": process_report["timeout_status"],
        "hard_kill_executed": process_report["hard_kill_executed"],
        "heartbeat_count": process_report["heartbeat_count"],
        "process_id": str(process_report["pid"]),
        "orphan_check_passed": process_report["orphan_check_passed"],
        "logs_ref": "inline",
        "stdout_tail": process_report["stdout"][-2000:],
        "stderr_tail": process_report["stderr"][-2000:],
    }


def run_process_group(
    command: list[str],
    timeout_sec: float,
    hard_timeout_sec: float = 1.0,
    heartbeat_interval_sec: float = 0.05,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(
        command,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=creationflags,
        start_new_session=(os.name != "nt"),
        env=env,
    )
    heartbeat_count = 0
    deadline = time.monotonic() + timeout_sec
    while process.poll() is None and time.monotonic() < deadline:
        heartbeat_count += 1
        time.sleep(min(heartbeat_interval_sec, max(0.001, deadline - time.monotonic())))

    if process.poll() is None:
        _terminate_process_tree(process)
        hard_kill_executed = False
        try:
            stdout, stderr = process.communicate(timeout=hard_timeout_sec)
        except subprocess.TimeoutExpired:
            _kill_process_tree(process)
            hard_kill_executed = True
            stdout, stderr = process.communicate(timeout=hard_timeout_sec)
        orphan_check_passed = process.poll() is not None and not _pid_is_running(process.pid)
        timeout_status = (
            "hard_killed"
            if hard_kill_executed and orphan_check_passed
            else "soft_terminated_no_orphan"
            if orphan_check_passed
            else "kill_incomplete"
        )
        return {
            "pid": process.pid,
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": True,
            "timeout_status": timeout_status,
            "hard_kill_executed": hard_kill_executed,
            "heartbeat_count": max(heartbeat_count, 1),
            "orphan_check_passed": orphan_check_passed,
        }

    stdout, stderr = process.communicate(timeout=hard_timeout_sec)
    return {
        "pid": process.pid,
        "returncode": process.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "timed_out": False,
        "timeout_status": "none",
        "hard_kill_executed": False,
        "heartbeat_count": max(heartbeat_count, 1),
        "orphan_check_passed": process.poll() is not None,
    }


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T"], capture_output=True, text=True, check=False)
    else:
        os.killpg(process.pid, signal.SIGTERM)


def _kill_process_tree(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, text=True, check=False)
    else:
        os.killpg(process.pid, signal.SIGKILL)


def _pid_is_running(pid: int) -> bool:
    if os.name == "nt":
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"Get-Process -Id {pid} -ErrorAction SilentlyContinue"],
            capture_output=True,
            text=True,
            check=False,
        )
        return completed.returncode == 0 and bool(completed.stdout.strip())
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
