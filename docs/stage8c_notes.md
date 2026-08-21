# Stage 8C Notes — Operational Underdetermination and Explicit Update

Status: **implementation in progress; final full-regression validation recorded in the Stage 8C result checkpoint.**

## Question

Can the two type-distinct Stage 8B models on the same executable continuation carrier remain operationally indistinguishable under one fully specified ontology-neutral quantum interface when their continuation weights are matched, while an explicit common piece of evidence updates them according to different internal semantics?

Stage 8C targets Stage 8 exit criteria **22–29** only. Genuine clock-perspective transport remains Stage 8D.

## Full ontology-neutral interface O_Q

Stage 8C freezes the executable interface:

`O_Q = (D, rho_now, R_now, Next_Q(D), pi_Q(next|D), observed_outcome)`.

The concrete `QuantumOperationalView` contains:

- current relational anchor;
- normalized current reduced density matrix;
- current target-memory joint readout distribution;
- current target-memory mutual information;
- physically defined next measurement outcomes;
- their predicted probabilities;
- the observed outcome after update, if any.

It deliberately excludes:

- `h*`;
- selected-history / selector data;
- model type names;
- typed Potentiality objects;
- raw epistemic `q_E` weights;
- raw ontic `K` weights.

The prediction layer therefore compares physical output rather than exposing modal bookkeeping.

## Physical future-signature measurement

The Stage 8A canonical `e2` reduced states of `h_L` and `h_R` are orthogonal. Stage 8C uses that physical fact to define a fixed projective measurement on the A-clock reduced ambient space.

The first two effects project onto the two orthogonal future-state rays. A third remainder projector closes the measurement on the ambient space.

For the canonical retained continuation family:

- `h_L` gives `future_signature_0` with probability one;
- `h_R` gives `future_signature_1` with probability one;
- the remainder outcome has zero probability for both canonical continuations.

The first two physically supported outcomes therefore form `Next_Q(e1)`.

The measurement is a diagnostic of physical future differences already established in Stage 8A. Its outcome labels are operational measurement labels, not a declaration that continuation labels themselves are observables.

## Prediction rule

For each continuation `h`, Stage 8C computes the Born likelihood:

`p(y|h,D)`.

The epistemic prediction is:

`pi_E(y|D) = sum_h q_E(h|D) p(y|h,D)`.

The ontic-extension prediction is:

`pi_O(y|D) = sum_h K(h|D) p(y|h,D)`.

The hidden epistemic `h*` is not read by the operational projection.

With canonical matched weights:

`q_E = K = (1/2,1/2)`,

both model types predict:

`pi(future_signature_0)=1/2`,

`pi(future_signature_1)=1/2`.

Thus matched operational equality, if the tests pass, is produced by one common physical measurement and matched predictive weights, not by comparing model-type labels.

## Privileged distinction

A separate privileged diagnostic remains available for test purposes.

For the epistemic model it reports that a selected continuation exists and reveals its continuation id.

For the ontic-extension model it reports that no selected complete continuation datum exists in the declared model schema.

This privileged diagnostic is deliberately outside `O_Q`.

Therefore Stage 8C tests:

`operational equality != modal/ontological identity`.

## Hidden-selected-continuation swap

With carrier and weights fixed, Stage 8C repeats the Stage 8B swap control at the full `O_Q` level:

`h*=h_L -> h*=h_R`.

The privileged diagnostic changes, while the full operational projection should remain unchanged.

This directly checks that `h*` does not leak into the pre-evidence operational prediction.

## Weight-mismatch control

Stage 8C changes only the ontic continuation weights to:

`K=(0.75,0.25)`

while leaving the current constrained Actuality and continuation carrier unchanged.

Because the future-signature measurement distinguishes the two continuation states, the predicted next-outcome probabilities become `(0.75,0.25)` rather than `(0.5,0.5)`.

This is the required positive control showing that `O_Q` is capable of detecting an operationally meaningful mismatch rather than being hard-coded to equality.

## Explicit evidence update

The update API accepts an explicit `QuantumEvidence(outcome)` object. It does not sample a branch or choose a continuation internally.

The canonical common update uses:

`future_signature_0`.

### Epistemic update

The pre-existing selected continuation `h*` is retained.

The epistemic weights are conditioned by the Born likelihood of the explicit evidence:

`q_E'(h) proportional to q_E(h) p(evidence|h)`.

In the canonical `h*=h_L` run the posterior becomes:

`q_E'=(1,0)`.

Evidence with zero likelihood under the hidden selected continuation is rejected rather than silently replacing `h*`.

### Ontic-extension update

The ontic weights are conditioned by the same physical likelihood:

`K'(h) proportional to K(h) p(evidence|h)`.

The canonical posterior also becomes:

`K'=(1,0)`.

The updated ontic object stores the source carrier, terminal current anchor, explicit observed outcome, and posterior weights. Its frozen/slots schema contains no selected-continuation, selector, seed, or singleton `QuantumContinuation` field.

The finite canonical update advances to terminal `e2`, so the declared future extension set after the update is:

`QExt(e2)=empty`.

The singleton posterior support is evidence-conditioned public information about the completed continuation, not a hidden selector that existed before the evidence.

## Operational equality after the common update

For the canonical deterministic signature evidence, the matched epistemic and ontic posteriors coincide. Their evidence-conditioned current reduced density matrices and record interfaces therefore coincide at `e2`, and both have no further canonical `Next_Q` outcomes.

Stage 8C tests operational equality both before and after this explicit common update.

## Superposition and density/Born controls

The common current `e1` reduced state contains multiple coherent amplitudes. The same current density matrix and the same next-outcome Born-mixture prediction occur in both modal model types while their privileged structures remain different.

Therefore, within this declared finite family:

- presence of superposition does not select the ontic-extension semantics;
- the current density matrix does not uniquely determine selected-vs-unselected modal structure;
- the matched Born prediction does not uniquely determine selected-vs-unselected modal structure.

These are underdetermination results inside the declared model family, not a theorem that quantum states can never constrain modal interpretation in other theories.

## Interpretation boundary

Stage 8C does **not** establish:

- ontic openness of the real future;
- a hidden pre-existing future in nature;
- collapse as physical becoming;
- sampling as actualization;
- phenomenal passage;
- P-V covariance across genuine clock changes;
- V independence from P/O/R.

Frozen guards:

- `operational quantum equality != modal/ontological identity`;
- `matched numerical q_E and K != matched probability semantics`;
- `explicit evidence update != ontological becoming`;
- `random sampling != ontic actualization evidence`;
- `superposition != ontic Potentiality by definition`;
- `same density/Born data != unique modal semantics in this family`;
- `evidence-conditioned singleton support != pre-existing hidden selector`.

## Exit-criteria target

Stage 8C is designed to satisfy criteria **22–29**:

22. matched baseline operational views agree;
23. privileged diagnostics distinguish the modal structures;
24. weight mismatch changes operational prediction;
25. explicit common evidence changes Actuality consistently;
26. epistemic update retains `h*` and conditions beliefs;
27. ontic-extension update prunes support without adding a hidden complete future;
28. superposition/Born randomness alone is insufficient to choose ontic-extension semantics in the canonical family;
29. state/density representation alone does not silently decide the modal semantics in the canonical family.

Criteria 30–50 remain Stage 8D–G work.

## Next

Stage 8D — genuine clock-change modal transport.
