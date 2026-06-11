from __future__ import annotations

import subprocess
import time
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRequest
from math_auto_research.base.resources.resource_governor import ResourceGovernor


def run_guarded_process(command: list[str], request: ResourceRequest, governor: ResourceGovernor) -> dict[str, Any]:
    started_at = time.time()
    start_monotonic = time.monotonic()
    with governor.admit(request):
        completed = subprocess.run(command, capture_output=True, text=True, timeout=request.timeout_sec, check=False)
    ended_at = time.time()
    wall = time.monotonic() - start_monotonic
    return {
        "schema_version": "1.0.0",
        "report_id": f"resource_usage:{time.time_ns()}",
        "run_id": "local_smoke",
        "role": request.engine_role if request.engine_role != "none" else request.component,
        "admission_status": "admitted",
        "started_at": str(started_at),
        "ended_at": str(ended_at),
        "exit_status": "completed" if completed.returncode == 0 else "failed",
        "component": request.component,
        "budget": request.budget,
        "queue_wait_sec": 0,
        "wall_time_sec": round(wall, 6),
        "cpu_time_sec": 0,
        "peak_rss_mb": 0,
        "gpu_vram_peak_mb": None,
        "logs_ref": "inline",
    }
