# Failure Analysis — Why v0.4.5 exists

v0.4.4 improved the record/certificate scaffolding but still failed the intended meaning because:

1. Corpus generation used fixed theorem templates by family.
2. Proof generation used target-shape dispatch to direct Lean lemmas.
3. Engine artifacts were synthesized from selected rule lists rather than produced by independent solver computations.
4. Causality reports assigned boolean fields instead of executing destructive reruns.
5. Baseline outcomes were family-coded.
6. External source anchoring was not the same as preserving the external source goal.

v0.4.5 makes each of these release blockers.

Additional reviewed failure mode: an engine can fake causality by emitting the target fact as a solver artifact. v0.4.5 now requires independent checker evidence for every consumed fact/construction/certificate and rejects naked target assertions.
