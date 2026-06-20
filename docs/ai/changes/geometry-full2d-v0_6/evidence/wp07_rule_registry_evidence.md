# WP07 Rule Registry Evidence

Status: passed for WP07 registry-contract acceptance.

Commands run from `C:\Users\bakat\work\AI_math_research`:

```powershell
lake env lean lean\MathAutoResearch\GeometryFull2D\RuleLemmas.lean
python -m py_compile scripts\geometry_full2d_v0_6_rule_checkers.py scripts\geometry_full2d_v0_6_rule_registry.py scripts\check_rule_registry_v0_6.py
python scripts\check_rule_registry_v0_6.py --release --red-cases --output docs\ai\changes\geometry-full2d-v0_6\evidence\wp07_rule_registry_report.json --registry-output docs\ai\changes\geometry-full2d-v0_6\evidence\rule_registry_full2d_v0_6.json
```

Observed result:

- `check_rule_registry_v0_6.py` status: `passed`
- counted rule contracts: 36
- counted rule families: 21
- helper rules: 3
- Lean rule lemma elaboration: `passed`
- executable independent rule fixture suite: `passed`
- executable rule fixtures evaluated: 288
- positive rule fixtures passed: 72
- negative / unsupported / mutation rule fixtures failed as expected: 216
- rule checker import isolation: `passed`
- red cases: `passed`
- registry hash: `sha256:0e557d332b5f9452f4a2be1ba777688ebda5d4b76a500fc229147a9b0a04ebef`

Evidence artifacts:

- `docs/ai/changes/geometry-full2d-v0_6/evidence/wp07_rule_registry_report.json`
- `docs/ai/changes/geometry-full2d-v0_6/evidence/rule_registry_full2d_v0_6.json`

Claim ceiling:

WP07 establishes the semantic rule-registry contract floor: Lean lemmas elaborate, lemma type hashes are bound, identity/direct/facade counted rules are rejected, alias inflation is rejected, and executable independent rule fixtures run for every counted rule. Positive fixtures pass; negative, unsupported, and mutation fixtures fail as expected.

WP07 does not claim final release rule coverage. Under Base Spec DR-012-006 and Acceptance K-029, a rule is release-counted only when later WP09/WP13/WP14 records prove it was consumed by the compiler, present in a solver-backed certificate, mutation-sensitive, and used in a successful B2 final theorem. Those checks remain mandatory release evidence.
