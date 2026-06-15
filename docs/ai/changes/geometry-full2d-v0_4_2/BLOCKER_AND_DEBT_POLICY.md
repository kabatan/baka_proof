<!--
Generated for kabatan/baka_proof Guardian/Codex handoff.
Created: 2026-06-14
Status: SUPERSEDED_BY_MARP-GEOLEAN-BASE-008
-->
---
title: "Guardian Blocker and Debt Policy — GeometryFull2D v0.4.2"
policy_id: "MARP-GEOLEAN-BLOCKER-POLICY-007"
base_spec: "MARP-GEOLEAN-BASE-007"
status: "SUPERSEDED_BY_MARP-GEOLEAN-BASE-008"
created: "2026-06-14"
---

# Guardian Blocker and Debt Policy — GeometryFull2D v0.4.2

## 0. Purpose

This policy prevents two failure modes:

```text
1. Codex weakens the specification or makes arbitrary design decisions.
2. Codex stops too often and waits for user input for repairable implementation issues.
```

The policy is mandatory for all v0.4.2 work.

## 1. Severity ladder

### HardBlocker

Stop immediately. Write `docs/ai/changes/geometry-full2d-v0_4_2/evidence/hard_blocker_<id>.md`.

Allowed only for:

```text
HB-01 spec conflict with no precedence rule
HB-02 requirement change needed
HB-03 destructive repo/user-data action outside refactor scope
HB-04 license/terms prohibit required use
HB-05 required secret/private artifact unavailable and no allowed substitute exists
HB-06 unspecified incompatible mathematical semantics choice
HB-07 unavoidable unsound proof-use path
HB-08 Lean/lake cannot run at all after bootstrap
HB-09 Guardian authority state corrupt
```

### ReleaseBlocker

Do not stop. Record in DebtLedger and continue. Blocks final release only.

Examples:

```text
threshold not met
engine underperforms
corpus family insufficient
rule coverage insufficient
one benchmark family failing
one compiler family incomplete
external backend unavailable but an allowed substitute exists
release acceptance blocked
```

### WorkDebt

Do not stop. Record if needed. Must be closed before release if acceptance requires it.

Examples:

```text
refactor cleanup pending
test coverage incomplete
performance optimization needed
one engine lacks enough counted successes
one proof template missing
```

### MeasuredFailure

A task failed honestly. Count in metrics. Not a blocker unless aggregate thresholds fail.

### Informational

No release impact.

## 2. Default decisions table

Codex must apply these defaults without asking the user.

| Situation | Required action |
|---|---|
| LeanGeo dependency missing | install/vendor reproducibly; continue. |
| LeanGeo API name mismatch | create GeometryFull2D facade wrapper and mapping evidence; continue. |
| Newclid unavailable | implement admitted local synthetic closure plus record WorkDebt; continue. |
| GenesisGeo unavailable | implement deterministic construction search; record WorkDebt if neural proposer absent; continue. |
| TongGeometry model missing | ignore for v0.4.2 release path; do not block. |
| Sage unavailable | use SymPy exact / Lean tactics / custom checker alternative; continue. |
| One engine cannot solve a task | mark measured_failure; continue corpus run. |
| Corpus threshold below floor | ReleaseBlocker; continue adding tasks. |
| Solve-rate below threshold | ReleaseBlocker; continue engine/rule/corpus repair. |
| A rule has missing side condition | WorkDebt or ReleaseBlocker depending on used-rule path; continue unrelated rules. |
| FinalVerifyGate fails for a task | measured_failure; continue. |
| A checker script fails | ReleaseBlocker unless it reveals unsound proof-use. |
| Unsound proof-use path detected | HardBlocker HB-07 if cannot isolate; otherwise immediately quarantine path and continue. |

## 3. DebtLedger schema

Path:

```text
docs/ai/changes/geometry-full2d-v0_4_2/debt/debt_ledger.jsonl
```

Schema:

```json
{
  "schema_version": "1.0.0",
  "debt_id": "debt:...",
  "severity": "ReleaseBlocker | WorkDebt",
  "created_at": "...",
  "affected_rids": [],
  "affected_work_packages": [],
  "summary": "...",
  "evidence_ref": "...",
  "unblock_plan": [],
  "status": "open | in_progress | closed",
  "closure_evidence_ref": null
}
```

A debt entry may not alter Base Spec requirements.

## 4. Blocker report requirements

A HardBlocker report must include:

```text
hard_blocker_id
triggering R-ID / Plan task
exact evidence
why no default decision applies
why continuing would be unsafe or arbitrary
options requiring user decision
recommended option
```

A ReleaseBlocker report must not ask the user to decide unless it also triggers a HardBlocker condition.

## 5. Guardian workflow rule

Codex must never treat `release_acceptance_status=blocked` as automatic stop. It must inspect `hard_blockers`.

```text
if hard_blockers != []:
  stop and report.
else:
  continue next_unblocked_work_packages.
```
