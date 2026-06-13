from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from plugins.geometry_synthetic.run_trace import build_fixture_run


class ContributionTrackingTest(unittest.TestCase):
    def test_fixture_run_records_search_final_and_diagnostic_contributions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "fixture_run"
            build_fixture_run(run_dir)
            payload = json.loads((run_dir / "research_contribution_records.json").read_text(encoding="utf-8"))
        statuses = {record["contribution_status"] for record in payload["records"]}
        self.assertIn("used_in_search", statuses)
        self.assertIn("used_in_final_proof", statuses)
        self.assertIn("diagnostic_only", statuses)


if __name__ == "__main__":
    unittest.main()
