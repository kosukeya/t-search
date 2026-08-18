# Stage 2D — Operational Equivalence

Status: **completed**.

## Purpose

Stage 2B and Stage 2C now provide two formally different model structures:

- epistemic-history: `M_E = (T,h*,q_E)`;
- ontic-extension: `M_O(D) = (D,Ext_T(D),K)`.

Stage 2D asks whether the difference remains visible after both typed modal views are mapped to the ontology-neutral operational interface fixed by the Stage 2 protocol:

`O(G) = (A_now, Next(D), pi(next|D))`.

The operational interface is deliberately not allowed to inspect Python model classes, `h*`, or the semantic type of Potentiality.

## Typed modal views remain formally different

Before operational erasure, the two local descriptions remain type-distinct:

- epistemic local view: `EpistemicLocalView`;
- ontic local view: `OnticLocalView`;
- epistemic Potentiality: `EpistemicPotentiality`;
- ontic Potentiality: `OnticPotentiality`.

Thus Stage 2D does not obtain equality by claiming the typed model structures are literally the same object.

## Operational interface

Stage 2D introduces:

`OperationalView`

with exactly three fields:

- `actuality`;
- `next_events`;
- `next_probabilities`.

There is no:

- `potentiality` semantic tag;
- `selected_history` field;
- epistemic/ontic model-type field.

The map therefore compares only the observables declared in advance by the protocol.

## Matched baseline

Use the shared current Actuality:

`D_0 = (p,n)`.

Epistemic baseline:

`q_E(h_L)=q_E(h_R)=1/2`.

Ontic baseline:

`K(h_L)=K(h_R)=1/2`.

The epistemic operational view is:

`O(G_E(D_0)) = ((p,n), {l1,r1}, {l1:1/2,r1:1/2})`.

The ontic operational view is:

`O(G_O(D_0)) = ((p,n), {l1,r1}, {l1:1/2,r1:1/2})`.

Therefore:

`O(G_E(D_0)) = O(G_O(D_0))`.

Component-wise:

- Actuality: equal;
- immediate next alternatives: equal;
- immediate-next probabilities: equal.

The correct Stage 2D conclusion is:

**operationally indistinguishable under the tested observables and matched baseline weights**.

This is not ontological equivalence.

## Hidden-history swap control

Replace only the epistemic hidden selected history:

`h*=h_L -> h*=h_R`

while keeping `T`, `D_0`, and `q_E` fixed.

Stage 2B already established that the epistemic local projection does not reveal this swap. Stage 2D confirms that the ontology-neutral operational view is also unchanged.

Thus the operational interface contains no indirect `h*` leakage.

## Weight-mismatch negative control

Operational equality is not a theorem that follows from the words "epistemic" and "ontic".

Change only the epistemic numerical weights to:

`q_E(h_L)=3/4`

`q_E(h_R)=1/4`

while keeping the ontic baseline at:

`K(h_L)=K(h_R)=1/2`.

Then:

- Actuality remains equal;
- the set of immediate next alternatives remains equal;
- the probability component differs;
- full operational equality fails.

An analogous mismatch can be produced by changing only `K`.

Therefore the matched baseline equality depends on the controlled numerical condition:

`pi_E(next|D_0)=pi_O(next|D_0)`.

It should not be attributed to the metaphysical interpretation itself.

## What is erased and what survives

### Erased by `O`

- epistemic versus ontic Potentiality type;
- the epistemic selected complete history `h*`;
- the distinction between "selected-future information exists but is hidden" and "selected-future information is absent";
- complete-extension semantic interpretation beyond its immediate operational consequences.

### Survives in the baseline

- current actual prefix `D_0`;
- immediate admissible alternatives `{l1,r1}`;
- matched predictive distribution `{1/2,1/2}`.

These are operationally shared structures under this deliberately restricted interface. They are not yet strict physical invariants.

## Interpretation

Stage 2D demonstrates a concrete separation between:

`formal/internal distinguishability`

and:

`operational distinguishability under a specified interface`.

For the matched baseline, the models are internally different but operationally equal under `O`.

The strongest justified statement is:

`M_E != M_O` internally,

while:

`O(G_E(D_0)) = O(G_O(D_0))`.

This does not show that the two ontologies are physically equivalent. It shows only that the selected local observables do not discriminate them in this toy setup.

## Validation scope

The committed Stage 2D test file contains 8 focused tests covering:

1. typed modal/Potentiality distinction before erasure;
2. matched baseline operational equality;
3. expected baseline operational contents;
4. hidden-`h*` swap invisibility;
5. epistemic weight-mismatch negative control;
6. ontic weight-mismatch negative control;
7. absence of Potentiality/selected-history semantics from `OperationalView`;
8. interface validation that probability keys match immediate alternatives.

As with Stage 2C, a full repository regression remains required before Stage 2 merge review if the execution environment still cannot obtain a clean checkout.

## Next step

Stage 2E will compare the two models after the same explicit observation, initially:

`l1`.

It will ask whether operational agreement persists after update while privileged internal diagnostics continue to distinguish:

- epistemic: unchanged preselected `h*` plus conditioned beliefs;
- ontic: longer Actuality plus pruned extensions and no selected future.
