---
title: "Red Case Suite — GeometryFull2D v0.6 Reviewed Strict"
base_spec: "MARP-GEOLEAN-BASE-012"
status: "USER_APPROVED_ACTIVE"
---

# Red Case Suite v0.6

The red-case suite defines failure classes, not historical filenames. Each red case must include an executable fixture under `tests/red_cases/geometry_full2d_v0_6/` and must be rejected by `scripts/check_red_case_suite_v0_6.py --all`.

Required red cases:

1. `RC-001 RedCase_TargetFactProvider` (`Target-fact provider`): provider emits final target as selected fact with empty premises.
2. `RC-002 RedCase_NakedTargetAssertion` (`Naked target assertion`): selected derivation has only final target.
3. `RC-003 RedCase_IdentityDirectRuleRegistry` (`Identity/direct-rule registry`): counted rule is identity, reflexivity, pure symmetry, direct facade lemma, alias inflation, or an output equal to its input modulo renaming.
4. `RC-004 RedCase_ProofFromShapeCompiler` (`Proof-from-shape compiler`): compiler chooses proof text or rule plan from target shape, theorem family, task id, source ref, target_shape_id, grammar family, corpus category, source_ref, template_id, difficulty tier, baseline, theorem name, statement hash, proof-region identity, binder-map identity, or any `TheoremAnchorV1` identifier field.
5. `RC-005 RedCase_RuleListArtifactSynthesis` (`Rule-list artifact synthesis`): engine artifact is derived from downstream `used_rules`, compiler decisions, proof text, rule registry output, or any proof-generation object.
6. `RC-006 RedCase_ReportOnlyCausality` (`Report-only causality`): causality report contains status fields but no live compiler, proof worker, and FinalVerifyGate rerun logs.
7. `RC-007 RedCase_FamilyCodedBaseline` (`Family-coded baseline`): baseline result is computed from family/category labels, target type, or hard-coded baseline id.
8. `RC-008 RedCase_ProjectionBenchmark` (`Projection benchmark`): projection task is counted as ExternalGoalPreserved or as a release positive.
9. `RC-009 RedCase_CheckerOmission` (`Checker omission`): a Base Spec or Acceptance requirement lacks release checker enforcement.
10. `RC-010 RedCase_CheckerWhitelist` (`Checker whitelist`): checker suppresses a detected forbidden shortcut due to filename, directory, file role, comment, fixture tag, or role.
11. `RC-011 RedCase_SealedChallengeCollusion` (`Sealed challenge collusion`): holdout generator imports or reads implementation code, selected implementation artifacts, run records, or emits expected proof/rule/engine labels.
12. `RC-012 RedCase_StaleEvidenceReplay` (`Stale evidence replay`): stale run records pass without binding to current git head, selected implementation hash, corpus hash, config hash, checker hash set, and fresh run directory hash.
13. `RC-013 RedCase_RuleHack` (`Rule hack`): rule registry uses fake broad families, aliases, unchecked rules, or rule checkers that do not verify premises, side conditions, and conclusion independently.
14. `RC-014 RedCase_TargetAsCertificate` (`Target-as-certificate`): certificate payload is just the target statement, target hash, target expression, or schema-normalized target with a checker name.
15. `RC-015 RedCase_CheckerGeneratedSuccessArtifacts` (`Checker-generated success artifacts`): checker creates counted success artifacts instead of executing provider, engine, compiler, proof worker, final verifier, matrix, or causality stages.
16. `RC-016 RedCase_StaticOnlyGreenRelease` (`Static-only green release`): final release passes from static scans, pre-existing reports, or summary fields without live execution.
17. `RC-017 RedCase_B2OnlyMatrix` (`B2-only matrix`): matrix executes B2 records only or materializes non-B2 baselines from summaries, labels, or cached B2 results.
18. `RC-018 RedCase_DirectLemmaWrappedAsIntermediate` (`Direct lemma wrapped as intermediate`): a direct facade lemma is wrapped as an intermediate and counted as solver-causal reasoning.
19. `RC-019 RedCase_ProviderImportsCompiler` (`Provider imports compiler`): provider or engine imports compiler, rule registry templates, proof generation, proof worker, final verifier, matrix, release checker, or corpus generator modules.

The suite passes only when each fixture fails release acceptance for the expected semantic reason.

Required non-RC K-level fixture:

- `K-010 EngineOutputContainsProofText`: engine output contains Lean proof text, tactic script, Lean lemma template id, proof replacement text, or final target proof text. This fixture enforces Acceptance K-010 and does not replace any Base Spec RC identifier.
- `K-013 TargetEquivalentIntermediate`: selected derivation uses an alpha-renamed target, target-hash intermediate, trivial target wrapper, reflexivity/symmetry-equivalent target, or direct-facade target lemma as its alleged non-target intermediate.
- `K-028 NarrowEngineRoleSet`: implementation defines release-critical engine roles after observing provider success or omits an enabled Base Spec `ReleaseCriticalEngineRoleV1` role from contribution accounting.


## Authority identifiers

```text
MARP-GEOLEAN-BASE-012
MARP-GEOLEAN-PLAN-012
MARP-GEOLEAN-ACCEPTANCE-012
V0.6_GEOMETRY_FULL2D_EXECUTION_LOCKED_REAL_SOLVER_CAUSAL_FULL_PIPELINE_READY
```
