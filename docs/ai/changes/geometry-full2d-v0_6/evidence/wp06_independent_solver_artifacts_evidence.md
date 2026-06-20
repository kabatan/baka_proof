# WP06 Independent Solver Artifact Checker Evidence

Status: MECH evidence regenerated after Guardian review BLOCK; pending re-review.

Command executed:

```bash
python scripts/check_independent_solver_artifacts_v0_6.py --all --red-cases --output docs/ai/changes/geometry-full2d-v0_6/evidence/wp06_independent_solver_artifacts_report.json
```

Observed result:

- `status=passed`
- evidence `git_head=f765471bb8f5ee2fec3c2f95925bb4dd3e43b22d`
- `engine_output_count=21`
- `check_count=21`
- every checked `EngineOutputFull2D` has `independent_checker_refs` bound to the emitted `IndependentSolverArtifactCheckV1` records
- checker imports contain no provider, compiler, rule registry, proof worker, final verify, matrix, release, corpus, prior release, or proof-template modules
- all seven checker roles observed:
  - `synthetic_trace_checker`
  - `construction_checker`
  - `algebraic_metric_certificate_checker`
  - `order_case_checker`
  - `inequality_checker`
  - `lean_search_certificate_checker`
  - `external_solver_trace_normalizer_checker`
- red/local negative cases reject naked final target facts, target-as-certificate, proof text, missing premises, missing side conditions, and schema-only certificates.
- reviewer-requested bypass regressions are covered:
  - unbound `non_target_intermediate:*` conclusion is rejected with `conclusion_not_verified`
  - arbitrary solver-context side-condition hash is rejected with `side_conditions_not_verified`
  - certificates embedding the actual target hash or a target-hash field are rejected with `target_as_certificate`
  - extra unbound `solver_context:*` premises are rejected with `premises_not_exactly_bound_to_claim` and `unverified_premise:*`

Corrective changes after initial review block:

- `verify_conclusion` recomputes the exact expected non-target conclusion and conclusion hash from ClaimSpec plus engine role.
- `verify_side_conditions` recomputes the exact expected side-condition records from ClaimSpec plus engine role.
- premise verification now requires the full artifact premise set to equal the ClaimSpec-derived expected premise for that role.
- certificate validation walks nested certificate fields and rejects actual target hashes, target fields, target expressions, schema-normalized target certificates, and schema-only certificates.
- local red cases now include bogus unbound conclusion, target-hash embedded certificate, target-hash field certificate, schema-normalized target certificate, arbitrary side-condition hash, and extra unbound solver-context premise.

Scope note:

WP06 checks provider-stage selected artifacts and emits `IndependentSolverArtifactCheckV1` records. It does not claim selected derivation, target matching, compiler correctness, live causality, matrix metrics, or final release readiness.
