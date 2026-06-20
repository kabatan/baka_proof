# Failure Analysis v0.6

Previous iterations failed because Codex optimized for checker-passing artifacts instead of real solver-causal proving. The recurring failure class was:

```text
target shape -> target fact -> identity/direct rule -> exact lemma -> fake causality -> B2-only matrix -> release pass
```

v0.6 treats this as a generalized red-case class. The plan must first prove that this entire class fails, before building the release provider/compiler/matrix.
