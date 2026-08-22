# Stage 9D Results — Continuation-Aware Clock Transport

Status: **Stage 9D complete; criteria 31–36 satisfied.**

## Question

Do the Stage 9 directional-record / nontrivial-Potentiality results survive genuine changes of physical clock perspective when each continuation receives its own re-derived constrained atlas and all record/event/class typing remains explicit?

## Executable answer

**Yes for continuation-specific state, metric, directional-record observable, continuation-class, weight, and matched modal-view transport in the declared finite Stage 9D atlas.**

The full cross-continuation Stage 9C future-signature measurement-family covariance remains separately `not_established`.

## 1. Continuation-specific atlas

The canonical carrier remains:

`QExt(e1)={h_L,h_R}`.

For every continuation h and clock node `(X,j)`, Stage 9D re-derives:

`C_{h,X,j}`

`G_{h,X,j}=C_{h,X,j}^{-dagger}C_{h,X,j}^{-1}`

`S^h_{Y,k<-X,j}=C_{h,Y,k}C_{h,X,j}^{-1}`.

Results:

- 9 A/B/C charts per continuation;
- 18 charts total;
- minimum chart rank = `14`;
- 108 genuine ordered distinct-clock state transports;
- 324 three-clock compositions;
- state, inverse, induced-metric, and composition residuals all within the declared tolerance.

The h_L and h_R atlases do not collapse into one universal h-independent map. A control that applies an h_L map to h_R is rejected.

## 2. Typed directional record transport

The e0/e2 record-target observables and memory projectors are anchored to the declared A/e1 semantics, lifted to each continuation's physical coordinates, and represented in each clock chart.

For every h_L/h_R chart under preserving relational-event correspondence:

`(A_R,A_acc)=(+1,+0.5)`.

For the explicitly reversing correspondence:

`(A_R,A_acc)=(-1,-0.5)`.

The observable-transport, induced-metric self-adjointness, projector, and target-memory commutator checks all pass within tolerance.

Thus:

`perspective change != temporal-direction reversal`.

The record arrow is covariant under the preserving atlas transformation and reverses only when event correspondence reverses.

## 3. Event correspondence

Stage 9D explicitly distinguishes event labels from numerical clock readings.

Positive correspondence:

`e0 -> e0`

`e1 -> e1`

`e2 -> e2`.

Reversing correspondence:

`e0 -> e2`

`e1 -> e1`

`e2 -> e0`.

A reversed event map falsely declared orientation-preserving fails the directional covariance test.

`equal numeric clock readings != event identity`.

## 4. Continuation-class and weight covariance

The valid class correspondence preserves:

`h_L -> h_L`

`h_R -> h_R`

at the common e1 current event.

Swapped-class and terminal-current controls are rejected.

With matched q_E/K weights:

- epistemic and ontic-extension transported public views agree at all 9 clock nodes;
- hidden epistemic h* swap remains public-view invariant at all nodes;
- continuation weights are preserved;
- the public transported view exposes no selected-continuation/model-type field.

This extends the Stage 9C operational underdetermination result through the declared clock atlas.

## 5. Wrong-map and wrong-observable controls

Two important false-positive routes are rejected.

1. **Wrong continuation map:** using h_L's atlas map for h_R fails to reproduce the h_R target state.
2. **Bare observable reuse:** copying a source-chart record matrix into another chart without the required coordinate transport disagrees with the correctly represented target observable.

Therefore:

`covariance of a wrongly typed observable != semantic correctness`.

and

`continuation-aware transport != one universal h-independent map`.

## 6. Stage 9C future-signature measurement boundary

Stage 9D does not infer a transport for the entire Stage 9C cross-continuation future-signature measurement merely from successful continuation-specific state and record transport.

Result:

`full Stage 9C future-signature measurement covariance = not_established`.

This is a scope boundary, not a negative result about the already established state/record/class/weight transport.

`not_established != false`.

## Stage 9D criteria 31–36 assessment

31. Eighteen continuation-specific A/B/C charts are re-derived and every declared chart has rank 14 — **satisfied**.
32. 108 genuine distinct-clock state/inverse/metric transports and 324 three-clock compositions satisfy covariance within tolerance — **satisfied**.
33. Typed directional record observables transport consistently; preserving correspondence retains `(+1,+0.5)` and reversing correspondence gives `(-1,-0.5)` — **satisfied**.
34. Continuation classes and weights transport under explicit correspondence; matched epistemic/ontic views and hidden-h* swap invariance hold at every local node — **satisfied**.
35. Wrong class, wrong event, wrong continuation-map, and bare-observable controls are rejected — **satisfied**.
36. Full Stage 9C future-signature measurement-family covariance is reported separately as `not_established`, rather than inferred from the positive transport results — **satisfied**.

## Scientific interpretation

Stage 9D shows that the Stage 9 directional-R/V construction is not confined to a preferred A-clock representation. In the declared finite constrained family, continuation-specific perspective transport, directional-record semantics, continuation classes, and weights form a mutually compatible local atlas when the required event/class/observable typing is supplied.

The strongest statement supported here is:

`genuine P transport + directional R + nontrivial V_extension/V_weights = compatible in the declared typed finite atlas`.

This does **not** establish that `P`, `R`, and `V` are identical, that `V_semantics` is fixed, that future openness or becoming is ontological, or that finite clock covariance is gravitational/general covariance.

## Guards

- `equal numeric clock readings != event identity`;
- `covariance of a wrongly typed observable != semantic correctness`;
- `continuation-aware transport != one universal h-independent map`;
- `branch-specific perspective map != hidden branch selection`;
- `directional record covariance != P=R`;
- `P-R_direction-V covariance != ontic openness`;
- `class/weight covariance != V_semantics identity`;
- `full Stage 9C future-measurement covariance remains not_established`;
- `not_established != false`;
- `finite clock covariance != general covariance`;
- `finite constrained-model success != empirical discovery`.

## Validation

GitHub Actions run #1013:

**`733 passed in 372.31s`**.

This run includes the full Stage 9D scientific transport and negative-control tests before the later test-only reuse optimization.

## Next

**Stage 9E — P/O/R_direction/V compatibility matrix**.