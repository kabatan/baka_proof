# Failure Analysis — Why v0.4.4 Reviewed Exists

## v0.4.3 failure pattern

```text
external-looking source
  -> projection theorem with easy target
  -> fixed facade lemma proof
  -> ActualTaskPipelineRun and certificate chain
  -> release checker passed
```

This failed the intended full-prover meaning.

## Root causes

1. Corpus requirements allowed projection tasks to look external.
2. Direct lemma ceilings were too narrow and did not catch wrapped direct proofs.
3. ActualTaskPipelineRunV1 proved artifact presence but not solver causal necessity.
4. Baseline requirements and B8 applicability were under-specified.
5. User-reviewed tasks risked becoming a nonessential external blocker.
6. Acceptance did not require enough negative tests for these failure modes.

## v0.4.4 reviewed fixes

1. Projection tasks are never counted.
2. ExternalGoalPreserved requires goal preservation reports.
3. UserReviewedGoal has no fixed release floor.
4. B8 is conditional on model provider use.
5. Every B2 success needs SolverCausalityReportV1.
6. Direct/wrapped facade lemma success is capped and not substantive.
7. Engine outputs may not contain proof text.
8. Compiler input isolation is explicit.
9. SealedSolverChallenge replaces reliance on user-only review availability.
10. Regression tests must prove old shortcuts fail.
