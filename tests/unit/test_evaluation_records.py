from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from math_auto_research.base.logging.run_trace import ControllerStrategyLog, ResearchContributionRecord
from math_auto_research.evaluation.metrics import REQUIRED_METRIC_KEYS
from math_auto_research.schema_validation import validate_artifact


class EvaluationRecordsTest(unittest.TestCase):
    def test_contribution_and_strategy_log_schemas_validate(self) -> None:
        contribution = ResearchContributionRecord(
            "1.0.0",
            "research_contribution:run:trace",
            "run:fixture",
            "geotrace:fixture",
            "used_in_search",
            "not final proof evidence",
        )
        strategy = ControllerStrategyLog(
            "1.0.0",
            "controller_strategy_log:run",
            "run:fixture",
            "controller:fixture",
            "sha256:controller",
            {"geometry_solve": True, "multi_agent": False},
            {"geometry_solve_requests": 1},
            "used_in_search",
            ("sha256:artifact",),
            "controller strategy is not proof evidence",
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            contribution_path = root / "research_contribution_record.json"
            strategy_path = root / "controller_strategy_log.json"
            contribution_path.write_text(json.dumps(contribution.to_dict()), encoding="utf-8")
            strategy_path.write_text(json.dumps(strategy.to_dict()), encoding="utf-8")
            self.assertEqual(validate_artifact(contribution_path).schema_id, "evaluation.research_contribution_record.v1")
            self.assertEqual(validate_artifact(strategy_path).schema_id, "evaluation.controller_strategy_log.v1")

    def test_required_metric_key_registry_is_complete(self) -> None:
        self.assertIn("final_theorem_rate", REQUIRED_METRIC_KEYS)
        self.assertIn("replay_success_rate", REQUIRED_METRIC_KEYS)
        self.assertEqual(len(REQUIRED_METRIC_KEYS), 12)


if __name__ == "__main__":
    unittest.main()
