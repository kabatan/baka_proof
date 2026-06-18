#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--change-dir", required=False)
    args = parser.parse_args()
    ledger = Path(args.change_dir or ".") / "debt" / "debt_ledger.jsonl"
    open_entries = []
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("status") != "closed":
                open_entries.append(item.get("id", "unknown"))
    report = {
        "schema_version": "DebtLedgerCheckV05",
        "status": "passed" if not open_entries else "failed",
        "errors": [] if not open_entries else ["open_debt_entries"],
        "open_entries": open_entries,
        "change_dir": args.change_dir,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
