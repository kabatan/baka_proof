---
title: "Guardian Red Case Suite — GeometryFull2D v0.5 Reviewed Strict"
---

# Red Case Suite v0.5

The red-case suite describes failure classes, not one historical implementation. Each fixture must be generated in at least two variants: static-code variant and artifact-run variant. Final release acceptance must reject every variant.

## Required red cases

| Red case | Minimal forbidden behavior | Expected blocker |
|---|---|---|
| TargetFactProvider | Engine emits final target as premise-free fact | K-004/K-005 |
| NakedTargetAssertion | Selected derivation has only final target assertion | K-005 |
| IdentityRuleRegistry | Counted rule input == output | K-006 |
| ProofFromShapeCompiler | Compiler branches on target expr / target shape | K-007 |
| RuleListArtifactSynthesis | Engine output built from compiler selected rules | K-008 |
| ReportOnlyCausality | Reports failed_as_expected without rerun commands | K-011/K-012 |
| FamilyCodedBaseline | Baseline final status from family/category | K-023 |
| ProjectionCorpusCounted | Projection task counted as positive | K-013/K-016 |
| EngineOutputContainsProofText | Engine output contains exact/tactic/proof snippet | K-009 |
| CheckerOmission | K requirement missing from final coverage matrix | K-002 |
| CheckerWhitelist | Checker detects shortcut then suppresses by filename | K-030 |
| DirectLemmaWrappedAsIntermediate | have h := by exact lemma; exact h counted as substantive | K-020/K-021 |
| SealedChallengeImportsCompiler | Holdout generator imports compiler/provider/rules | K-015 |
| StaleEvidenceReplay | Old run records accepted after code hash changes | K-026 |
| TargetShapeMenuCorpus | Corpus has fixed target menu with low skeleton diversity | K-014/K-029 |
| GoalPreservationSelfAttestation | Generator self-declares goal preservation | K-016 |
| ProviderImportsCompiler | Provider imports compiler/proof modules | K-031 |
| B8SilentlyOmitted | Conditional B8 is omitted without checked not-applicable evidence | K-024/K-033 |
| ClosureOverclaimsReadiness | Closure claims natural-language fidelity, open-problem solving, model-backed readiness, production safety, or out-of-target correctness | K-028 |

A red case is considered rejected only when the production release checker fails it for the expected blocker. Separate toy validators do not count.
