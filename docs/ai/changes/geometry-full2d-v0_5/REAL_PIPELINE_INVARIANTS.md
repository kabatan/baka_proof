# Real Pipeline Invariants v0.5 Reviewed Strict

1. Provider before compiler. Provider artifacts must exist before compiler execution and provider cannot import downstream proof modules.
2. Semantic engine outputs only. No Lean proof text or proof templates in engine outputs.
3. No naked target fact. A final target fact must be derived from non-target selected artifacts or independently checked certificates.
4. Compiler consumes SelectedSolverDerivationV2 only. It cannot branch on target shape or benchmark labels.
5. Final theorem status is granted only by FinalVerifyGate report, never by matrix or baseline logic.
6. Solver causality is live destructive rerun evidence, never a boolean field.
7. Matrix contains all counted tasks for every required baseline.
8. Corpus is independent of proof implementation and meets statement diversity floors.
9. All K requirements are executed in final release acceptance.
10. Red-case rejection is a prerequisite to any green release report.
