---
title: DR-GEO-002 — No AgentC/AgentD Core Modes
decision_id: DR-GEO-002
status: ACCEPTED
created: 2026-06-11
purpose: Record the v0.3 decision to remove AgentC/AgentD taxonomy from core.
authority: Decision record; Base Spec R-NOOPT-002 is authoritative.
---

# DR-GEO-002 — No AgentC/AgentD Core Modes

Decision: AgentC/AgentD and A/B/C/D runtime taxonomies are not core architecture modes.

Controller internals may use multi-agent orchestration, population search, rater loops, or deep planning, but core sees only the `ResearchControllerPlugin` boundary.
