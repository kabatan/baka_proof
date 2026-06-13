# T32 Run trace and contribution records evidence

Task: T32 — Run trace and contribution records.

Supports:

```text
R-BASE-002
R-SCHEMA-006
R-EVAL-*
```

Implemented files:

```text
src/math_auto_research/evaluation/evaluation_funnel.py
src/math_auto_research/evaluation/metrics.py
src/math_auto_research/evaluation/reproducibility_report.py
src/math_auto_research/evaluation/__init__.py
schemas/evaluation/research_contribution_record.schema.json
schemas/evaluation/controller_strategy_log.schema.json
schemas/artifact_schema_map.json
tests/unit/test_evaluation_records.py
tests/unit/test_contribution_tracking.py
```

Notes:

```text
Evaluation public modules expose EvaluationFunnel, MetricsReport,
ReproducibilityReport, ControllerStrategyLog, and ResearchContributionRecord.
Research contribution records distinguish search contribution, final proof
evidence, and diagnostic-only artifacts. Required metric key registry records
the R-EVAL metric surface without making positive advantage claims.
```

Commands run:

```text
python -m json.tool schemas/artifact_schema_map.json
make test-unit TEST_FILTER=evaluation_records
make test-unit TEST_FILTER=contribution_tracking
make test-unit TEST_FILTER=run_trace
make test-unit TEST_FILTER=evaluation_matrix
python -m compileall -q src plugins tests scripts
```

Observed results:

```text
artifact_schema_map JSON parsed.
evaluation_records unit tests: 2 tests OK.
contribution_tracking unit tests: 1 test OK.
run_trace unit tests: 3 tests OK.
evaluation_matrix unit tests: 2 tests OK.
compileall passed.
```
