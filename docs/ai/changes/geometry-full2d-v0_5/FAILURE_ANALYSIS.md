# Failure Analysis v0.5 Reviewed Strict

Prior failure pattern:

```text
fixed target shape / theorem menu
  -> target fact artifact
  -> identity or direct facade rule
  -> exact rule template
  -> causality report field says failed_as_expected
  -> B2-only matrix or label-derived metrics
  -> release pass
```

v0.5 prevents this by requiring:

```text
- red-case-first acceptance;
- provider/compiler stage separation;
- no target-fact provider;
- non-identity RuleRegistry;
- independent checker reports for selected solver artifacts;
- compiler taint tests;
- live destructive causality reruns;
- all-baseline actual matrix;
- statement diversity floors;
- K coverage matrix;
- no checker whitelist.
```
