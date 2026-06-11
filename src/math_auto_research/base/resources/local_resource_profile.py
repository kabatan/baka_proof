from __future__ import annotations

import json
import os
import platform
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def probe_local_resources() -> dict[str, Any]:
    logical = os.cpu_count() or 1
    total_ram_mb = _total_ram_mb()
    free_artifact = shutil.disk_usage(Path.cwd()).free // (1024 * 1024)
    profile = {
        "schema_version": "1.0.0",
        "profile_id": "local_resource_profile:unhashed",
        "created_at": datetime.now(UTC).isoformat(),
        "os": platform.platform(),
        "cpu_physical_cores": max(1, logical // 2),
        "cpu_logical_cores": logical,
        "total_ram_mb": total_ram_mb,
        "available_ram_mb_at_probe": total_ram_mb,
        "gpu_devices": [],
        "disk_free_mb": {
            "artifact_root": free_artifact,
            "temp_root": shutil.disk_usage(Path(os.environ.get("TEMP", str(Path.cwd())))).free // (1024 * 1024),
        },
        "lean_build_parallelism_default": max(1, logical - max(1, int(logical * 0.15))),
        "provider_engine_availability": {
            "symbolic_closure": "unavailable",
            "construction_proposer": "unavailable",
            "heavy_search": "unavailable",
        },
    }
    profile["profile_id"] = "sha256:" + _stable_hash(profile)
    return profile


def _total_ram_mb() -> int:
    if platform.system() == "Windows":
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MEMORYSTATUSEX()
            status.dwLength = ctypes.sizeof(status)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return int(status.ullTotalPhys // (1024 * 1024))
        except Exception:
            return 0
    return 0


def _stable_hash(value: dict[str, Any]) -> str:
    import hashlib

    copy = dict(value)
    copy["profile_id"] = ""
    payload = json.dumps(copy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
