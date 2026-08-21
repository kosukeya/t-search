# Stage 8C Results — Operational Underdetermination and Explicit Update

Status: **implementation added; final numerical/CI checkpoint pending synchronized regression.**

## Scope

Stage 8C tests exit criteria **22–29** on the same canonical Stage 8A/8B continuation carrier:

`QExt(e1)={h_L,h_R}`.

No physical continuation schedule is changed to obtain the modal comparison.

## Operational interface

The executable `QuantumOperationalView` exposes only:

- current anchor;
- normalized current reduced density matrix;
- target-memory joint record distribution;
- target-memory mutual information;
- physically defined next outcomes;
- predicted next-outcome probabilities;
- explicit observed outcome after update.

It excludes `h*`, selector/model type, typed Potentiality, and raw `q_E` / `K` fields.

## Physical next-outcome measurement

A fixed projective future-signature measurement is constructed from the two orthogonal canonical `e2` states established by Stage 8A.

The first two projectors discriminate those physical future states; a remainder projector closes the measurement on the ambient reduced space.

Expected canonical Born signatures are deterministic:

- `h_L -> future_signature_0`;
- `h_R -> future_signature_1`;
- remainder probability zero for both retained continuations.

Measurement completeness, positivity, and projector orthogonality are executable tests rather than assumptions.

## Matched baseline

With:

`q_E=K=(0.5,0.5)`,

the two model types are expected to have the same full `O_Q` view and predicted next probabilities:

`(0.5,0.5)`.

The hidden selected continuation is not consulted by the operational projection.

A privileged structural diagnostic remains different between the model types and lies outside `O_Q`.

## Hidden-selected swap

Changing only:

`h*=h_L -> h*=h_R`

with the carrier and weights fixed must change the privileged diagnostic while leaving the full `O_Q` view unchanged.

## Weight-mismatch control

Changing only the ontic weights to:

`K=(0.75,0.25)`

must leave current Actuality fields unchanged while changing the physical next-outcome prediction to `(0.75,0.25)`.

This control demonstrates that the operational comparator can detect a real predictive mismatch.

## Explicit common update

The canonical explicit evidence is:

`QuantumEvidence("future_signature_0")`.

No internal sampling API selects a branch.

Expected epistemic result:

- current anchor advances `e1 -> e2`;
- pre-existing `h*=h_L` is preserved;
- posterior `q_E'=(1,0)`;
- contradictory deterministic evidence is rejected rather than replacing `h*`.

Expected ontic-extension result:

- current anchor advances `e1 -> e2`;
- posterior `K'=(1,0)`;
- updated frozen/slots schema contains no selected-continuation / selector / seed field;
- declared terminal future extension set is `QExt(e2)=empty`.

The evidence-conditioned singleton posterior support is public evidence-derived support for the completed continuation, not a hidden complete-future selector that existed before update.

## State / Born underdetermination controls

The common current `e1` state has multiple coherent amplitudes. The two model types nevertheless share the same current density matrix and matched next-outcome prediction while remaining distinguishable by a privileged modal diagnostic.

Thus, in the canonical family, neither superposition, the current density matrix, nor the matched Born-mixture output uniquely selects one of the two typed modal semantics.

## Exit criteria

If the focused tests and synchronized full regression pass, Stage 8C satisfies criteria **22–29** and leaves criteria **30–50** for Stage 8D–G.

## Validation

Focused tests:

`tests/test_stage8c_operational_update.py`

Full-regression counts and final head SHA are recorded after CI completes.

## Strongest bounded statement

**If the Stage 8C executable checks pass, the canonical finite constrained continuation family supports two privileged-structure-distinct modal models whose full declared ontology-neutral operational views agree under matched weights, disagree under a controlled weight mismatch, and remain operationally matched after one explicit deterministic common-evidence update that preserves the epistemic hidden selector while the ontic-extension schema adds no selector. The same superposed current state, density matrix, and matched Born prediction occur in both model types. This is finite-interface operational underdetermination and update compatibility, not proof of ontic openness, hidden futurity, collapse-as-becoming, or unique quantum modal semantics.**

## Next

Stage 8D — genuine clock-change modal transport.
