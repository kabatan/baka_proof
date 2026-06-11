from __future__ import annotations

import subprocess
import time
from typing import Any

from math_auto_research.base.resources.resource_budget import ResourceRequest
from math_auto_research.base.resources.resource_governor import ResourceGovernor


def run_guarded_process(command: list[str], request: ResourceRequest, governor: ResourceGovernor) -> dict[str, Any]:
    start = time.monotonic()
    with governor.admit(request):
        completed = subprocess.run(command, capture_output=True, text=True, timeout=request.timeout_sec, check=False)
    wall = time.monotonic() - start
    return {
        "schema_version": "1.0.0",
        "report_id": f"resource_usage:{time.time_ns()}",
        "run_id": "local_smoke",
        "component": request.component,
        "engine_role": request.engine_role,
        "budget": request.budget,
        "admitted": True,
        "queue_wait_sec": 0,
        "wall_time_sec": round(wall, 6),
        "cpu_time_sec": 0,
        "peak_rss_mb": 0,
        "gpu_vram_peak_mb": None,
        "exit_status": "success" if completed.returncode == 0 else "failed",
        "logs_ref": "inline",
    }
