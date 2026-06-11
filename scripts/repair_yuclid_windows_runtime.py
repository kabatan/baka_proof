from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


BOOST_DLL_ALIASES = {
    "boost_log_setup.dll": "boost_log_setup-vc143-mt-x64-1_88.dll",
    "boost_log.dll": "boost_log-vc143-mt-x64-1_88.dll",
    "boost_thread.dll": "boost_thread-vc143-mt-x64-1_88.dll",
    "boost_json.dll": "boost_json-vc143-mt-x64-1_88.dll",
    "boost_program_options.dll": "boost_program_options-vc143-mt-x64-1_88.dll",
}


def main() -> int:
    if sys.platform != "win32":
        print(json.dumps({"status": "skipped", "reason": "non_windows"}, indent=2, sort_keys=True))
        return 0

    env_root = Path(sys.executable).resolve().parent
    source_dir = env_root / "Library" / "bin"
    target_dir = env_root / "Scripts"
    results = []
    for source_name, target_name in BOOST_DLL_ALIASES.items():
        source = source_dir / source_name
        target = target_dir / target_name
        if not source.exists():
            results.append({"source": str(source), "target": str(target), "status": "missing_source"})
            continue
        if target.exists():
            results.append({"source": str(source), "target": str(target), "status": "already_present"})
            continue
        shutil.copy2(source, target)
        results.append({"source": str(source), "target": str(target), "status": "copied"})

    status = "passed" if all(item["status"] != "missing_source" for item in results) else "failed"
    print(json.dumps({"status": status, "results": results}, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
