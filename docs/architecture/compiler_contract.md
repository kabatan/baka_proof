---
title: CompilerContract — geometry × Lean v0.3
version: v0.3
status: SCAFFOLD_IMPLEMENTATION_APPROVED
created: 2026-06-11
purpose: Architecture home for the v0.3 CompilerContract.
authority: Derived documentation; Base Spec R-V03-COMPILER-001 and R-V03-AUX-001 are authoritative.
---

# CompilerContract — geometry × Lean v0.3

This document tracks the compiler architecture required by `R-V03-COMPILER-001` and `R-V03-AUX-001`.

Required components:

- `GeoTraceV1`
- `TraceCheckerResult`
- `RuleRegistryV1`
- `GeometryRuleContract`
- `SideConditionReport`
- `TraceCompiler`
- `TraceCompilationResult`
- `AuxiliaryConstructionCandidateV1`
- `ConstructionCheckResult`
- `ConstructionCompiler`
- `ConstructionCompilationResult`
- mutation tests

Trace schema validity and construction schema validity are not proof evidence. Only `FinalVerifyGate` may produce `final_theorem`.
