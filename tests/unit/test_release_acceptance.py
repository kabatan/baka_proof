from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_release_acceptance import _blocked_real_integrations, _validate_checklist_item


class ReleaseAcceptanceTest(unittest.TestCase):
    def test_missing_dependency_probe_fails_blocked_integration_accounting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = _blocked_real_integrations(Path(tmp) / "missing.json")
        self.assertEqual(result[0]["status"], "failed")

    def test_contradictory_dependency_probe_fails_blocked_integration_accounting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dependency_probe.json"
            path.write_text(
                json.dumps(
                    {
                        "engines": [{"family": "newclid_compatible", "install_status": "available"}],
                        "unresolved": [],
                    }
                ),
                encoding="utf-8",
            )
            result = _blocked_real_integrations(path)
        self.assertIn("failed", [item["status"] for item in result])

    def test_bogus_checklist_test_evidence_fails(self) -> None:
        result = _validate_checklist_item(
            "bogus_check",
            "test",
            "tests.unit.test_does_not_exist",
            [],
            [],
        )
        self.assertEqual(result["status"], "failed")


if __name__ == "__main__":
    unittest.main()
