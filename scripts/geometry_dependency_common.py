from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ENGINE_SPECS = {
    "newclid_compatible": {
        "role": "symbolic_closure",
        "commands": ["newclid"],
        "python_imports": ["newclid"],
        "install_plan": "python -m pip install 'newclid[yuclid]'",
        "source_url": "https://github.com/Newclid/Newclid",
        "completion_blocker": "blocks_real_final_theorem",
    },
    "genesisgeo_compatible": {
        "role": "construction_proposer",
        "commands": ["genesisgeo"],
        "python_imports": [],
        "install_plan": "git clone https://github.com/ZJUVAI/GenesisGeo.git vendor/GenesisGeo",
        "source_url": "https://github.com/ZJUVAI/GenesisGeo",
        "completion_blocker": "blocks_real_final_theorem",
    },
    "tonggeometry_compatible": {
        "role": "heavy_search",
        "commands": ["tonggeometry", "tong-geometry"],
        "python_imports": [],
        "install_plan": "git clone https://github.com/bigai-ai/tong-geometry.git vendor/tong-geometry",
        "source_url": "https://github.com/bigai-ai/tong-geometry",
        "completion_blocker": "blocks_heavy_search",
    },
}


def now_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def command_version(command: str, args: list[str] | None = None, timeout: int = 10) -> dict[str, Any]:
    args = args or ["--version"]
    executable = shutil.which(command)
    if executable is None:
        return {"command": command, "path": None, "status": "unavailable", "version": "unavailable"}
    try:
        completed = subprocess.run(
            [executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive reporting
        return {"command": command, "path": executable, "status": "failed", "version": f"failed: {exc}"}
    output = (completed.stdout or completed.stderr).strip().splitlines()
    version = output[0] if output else f"exit {completed.returncode}"
    status = "available" if completed.returncode == 0 else "failed"
    return {"command": command, "path": executable, "status": status, "version": version}


def python_import_status(module: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import importlib.util, json; "
                f"spec = importlib.util.find_spec({module!r}); "
                "print(json.dumps({'available': spec is not None, 'origin': None if spec is None else spec.origin}))"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {"module": module, "status": "failed", "origin": completed.stderr.strip()}
    data = json.loads(completed.stdout)
    version = _distribution_version(module)
    return {
        "module": module,
        "status": "available" if data["available"] else "unavailable",
        "origin": data["origin"],
        "version": version,
    }


def git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    completed = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def local_resource_profile() -> dict[str, Any]:
    logical = os.cpu_count() or 1
    total_gb = round(_total_ram_bytes() / (1024**3), 3) if _total_ram_bytes() else None
    disk_free_gb = round(shutil.disk_usage(ROOT).free / (1024**3), 3)
    max_provider_workers = max(1, logical - 2)
    max_provider_memory_gb = None if total_gb is None else max(1, int(total_gb - 4))
    return {
        "cpu": {
            "logical_cores": logical,
            "reserved_for_lean_and_os": 2,
            "max_provider_workers": max_provider_workers,
        },
        "memory": {
            "total_gb": total_gb,
            "reserve_gb": 4,
            "max_provider_memory_gb": max_provider_memory_gb,
        },
        "gpu": {
            "available": False,
            "device_count": 0,
            "vram_gb": None,
            "allow_genesisgeo_gpu": True,
            "allow_tonggeometry_gpu": False,
        },
        "disk": {
            "artifact_cache_limit_gb": max(1, min(10, int(disk_free_gb * 0.05))),
            "checkpoint_cache_limit_gb": max(1, min(20, int(disk_free_gb * 0.10))),
            "raw_log_limit_gb": max(1, min(5, int(disk_free_gb * 0.02))),
        },
        "process_policy": {
            "use_process_groups": True,
            "kill_on_timeout": True,
            "heartbeat_interval_sec": 30,
        },
        "budget_profiles": {
            "tiny": {"timeout_sec": 30, "max_parallel_engines": 1, "allowed_roles": ["symbolic_closure"]},
            "small": {"timeout_sec": 120, "max_parallel_engines": 1, "allowed_roles": ["symbolic_closure"]},
            "medium": {
                "timeout_sec": 600,
                "max_parallel_engines": 2,
                "allowed_roles": ["symbolic_closure", "construction_proposer"],
            },
            "heavy": {
                "timeout_sec": 3600,
                "max_parallel_engines": 2,
                "allowed_roles": ["symbolic_closure", "construction_proposer", "heavy_search"],
                "heavy_search_exclusive": True,
            },
            "extreme": {
                "timeout_sec": 14400,
                "max_parallel_engines": 1,
                "allowed_roles": ["heavy_search"],
                "heavy_search_exclusive": True,
                "requires_explicit_run_label": True,
            },
        },
    }


def write_simple_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_yaml_lines(data) + "\n", encoding="utf-8")


def build_dependency_probe(run_id: str, bootstrap_mode: str = "probe") -> dict[str, Any]:
    lean = command_version("lean", ["--version"])
    lake = command_version("lake", ["--version"])
    engines = []
    unresolved = []
    for family, spec in ENGINE_SPECS.items():
        command_checks = [command_version(command) for command in spec["commands"]]
        import_checks = [python_import_status(module) for module in spec["python_imports"]]
        vendor_path = ROOT / "vendor" / _vendor_name(family)
        vendor_commit = git_head(vendor_path)
        available = any(check["status"] == "available" for check in command_checks + import_checks) or vendor_commit is not None
        install_status = "installed" if available else "unavailable"
        engines.append(
            {
                "role": spec["role"],
                "family": family,
                "install_status": install_status,
                "version_or_commit": _version_or_commit(command_checks, import_checks, vendor_commit),
                "checkpoint_hash": None,
                "source_url": spec["source_url"],
                "install_plan": spec["install_plan"],
                "command_checks": command_checks,
                "python_import_checks": import_checks,
                "vendor_path": str(vendor_path.relative_to(ROOT)),
            }
        )
        if install_status != "installed":
            unresolved.append({"component": family, "consequence": spec["completion_blocker"]})
    if lean["status"] != "available" or lake["status"] != "available":
        unresolved.append({"component": "lean_lake_toolchain", "consequence": "blocks_real_final_theorem"})
    packages = []
    for path in [ROOT / "pyproject.toml", ROOT / "lakefile.lean", ROOT / "lake-manifest.json"]:
        if path.exists():
            packages.append({"name": path.name, "source": "local", "version_or_commit": "workspace", "lock_ref": file_hash(path)})
    return {
        "schema_version": "1.0.0",
        "report_id": f"dependency_probe:{run_id}",
        "created_at": datetime.now(UTC).isoformat(),
        "run_id": run_id,
        "bootstrap_mode": bootstrap_mode,
        "os": platform.platform(),
        "python_version": sys.version.split()[0],
        "lean_version": lean["version"],
        "lake_version": lake["version"],
        "packages": packages,
        "engines": engines,
        "unresolved": unresolved,
        "evidence_refs": [file_hash(ROOT / "scripts" / "geometry_dependency_common.py")],
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_command(command: list[str], timeout: int = 600) -> dict[str, Any]:
    started = time.time()
    try:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout, check=False)
        status = "passed" if completed.returncode == 0 else "failed"
        return {
            "command": command,
            "status": status,
            "returncode": completed.returncode,
            "duration_sec": round(time.time() - started, 3),
            "stdout_tail": completed.stdout[-2000:],
            "stderr_tail": completed.stderr[-2000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "status": "timeout",
            "returncode": None,
            "duration_sec": round(time.time() - started, 3),
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }


def _version_or_commit(command_checks: list[dict[str, Any]], import_checks: list[dict[str, Any]], vendor_commit: str | None) -> str:
    for check in command_checks:
        if check["status"] == "available":
            return check["version"]
    for check in import_checks:
        if check["status"] == "available":
            version = check.get("version")
            return f"{check['module']}=={version}" if version else str(check["origin"])
    return vendor_commit or "unavailable"


def _vendor_name(family: str) -> str:
    return {
        "newclid_compatible": "Newclid",
        "genesisgeo_compatible": "GenesisGeo",
        "tonggeometry_compatible": "tong-geometry",
    }[family]


def _distribution_version(module: str) -> str | None:
    candidates = [module, module.replace("_", "-")]
    if module == "newclid":
        candidates.append("py-yuclid")
    for candidate in candidates:
        try:
            return importlib.metadata.version(candidate)
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def _total_ram_bytes() -> int:
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
            return int(status.ullTotalPhys)
        except Exception:
            return 0
    return 0


def _yaml_lines(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(_yaml_lines(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(_yaml_lines(item, indent + 2))
            else:
                lines.append(f"{prefix}- {_yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{prefix}{_yaml_scalar(value)}"


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_yaml_scalar(item) for item in value) + "]"
    return json.dumps(str(value))
