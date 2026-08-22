# Stage 9D Notes — Continuation-Aware Clock Transport

Status: **completed; criteria 31–36 satisfied.**

## Purpose

Stage 9A–9C established a constrained continuation family with nontrivial `V_extension`, continuation-independent positive `R_direction`, and selected-vs-unselected modal underdetermination in the A/e1 public interface. Stage 9D asks whether those structures survive **genuine changes of physical clock perspective** rather than only one preferred A-clock description.

The Stage 9 carrier contains:

`QExt(e1)={h_L,h_R}`

with continuation-specific constrained physical spaces. Therefore Stage 9D does not reuse one inherited clock-change matrix for both continuations. For each continuation `h` and chart `(X,j)`, it re-derives:

`C_{h,X,j}` — local support coordinates,

`G_{h,X,j}=C_{h,X,j}^{-dagger} C_{h,X,j}^{-1}` — the induced physical metric,

and

`S^h_{Y,k<-X,j}=C_{h,Y,k} C_{h,X,j}^{-1}` — the genuine continuation-aware clock change.

## 1. Re-derived atlas

For each of h_L and h_R:

- clocks: A/B/C;
- readings: 0/1/2;
- charts per continuation: 9;
- total charts: 18;
- every reduction rank: 14.

The two continuations are treated independently when their atlases are built.

## 2. State and metric transport

Across all ordered distinct-clock pairs and all source/target readings:

- 108 genuine distinct-clock state transports are tested;
- inverse/round-trip consistency is tested;
- induced-metric covariance is tested;
- 324 three-clock compositions are tested.

All required residuals remain within the Stage 9D tolerance.

The maps are not assumed to be Euclidean-unitary. The invariant structure is the physical metric:

`S^dagger G_target S = G_source`.

## 3. Directional record observable typing

Stage 9D does not transport an untyped bare matrix.

The record semantics are anchored at the declared A/e1 current event. The lower/upper target projectors and memory projectors are first converted into continuation-specific physical-coordinate operators, then represented in each chart by:

`O_{h,X,j}=C_{h,X,j} O_phys^h C_{h,X,j}^{-1}`.

Each typed record observable stores:

- continuation id;
- clock;
- clock reading;
- event anchor;
- relational target;
- register semantics;
- coordinate-basis declaration;
- matrix representation.

This explicitly preserves the Stage 8E guard:

`covariance of a wrongly typed observable != semantic correctness`.

## 4. Directional record covariance

For every h_L/h_R chart under the orientation-preserving event correspondence:

`A_R=+1`

`A_acc=+0.5`

with lower-index orientation.

Under the explicit orientation-reversing event correspondence e0<->e2:

`A_R=-1`

`A_acc=-0.5`.

Thus a physical clock change does not itself reverse temporal record orientation. The sign changes only when the relational-event correspondence is explicitly reversed.

`perspective change != temporal-direction reversal`.

A deliberately swapped event correspondence that is falsely declared preserving is rejected.

## 5. Continuation class and weight transport

Stage 9D separately declares continuation-class correspondence.

The positive correspondence is:

- `h_L -> h_L`;
- `h_R -> h_R`;
- current relational event e1 preserved.

Controls reject:

- swapped h_L/h_R class correspondence;
- a correspondence that misdeclares terminal e2 as the current e1 event.

Matched epistemic and ontic-extension local views remain equal at all nine clock nodes, and changing only the hidden epistemic h* remains invisible in those public transported views. Continuation weights are preserved under the declared class correspondence.

This extends Stage 9C operational underdetermination from A/e1 to the full declared local clock atlas.

## 6. Negative controls

Stage 9D contains three important typing/map controls.

### Wrong continuation map

Using an h_L-derived clock map on h_R does not reproduce the h_R target state. The continuation-specific atlases are genuinely distinct; one h-independent map is not silently substituted.

### Bare observable reuse

Using the same local observable matrix in a different chart without the required similarity transport fails. The correctly transported observable differs from the bare source-chart matrix.

### Wrong event/class correspondence

Swapped continuation classes and a reversed event map falsely declared preserving are rejected.

These controls matter because numerical covariance without the right physical typing would be a false positive.

## 7. Scope boundary: future-signature measurement family

Stage 9D establishes transport of:

- continuation-specific states;
- induced metrics;
- directional record observables;
- relational-event typing;
- continuation classes;
- continuation weights;
- matched modal local views.

It does **not** construct a single declared h-independent transport for the entire cross-continuation Stage 9C future-signature measurement family.

Therefore:

`full Stage 9C future-signature measurement covariance = not_established`.

This is kept separate from the positive state/record/class/weight covariance results.

## 8. Interpretation

Stage 9D strengthens the Stage 9 integration result. The coexistence and separation seen in A/e1 are not artifacts of one preferred clock description: within the declared finite atlas, `P`, directional `R`, and the transported `V_extension/V_weights` carrier can be represented consistently across genuine physical clock changes.

This does not imply:

- `P=R`;
- `P=V`;
- directional R determines `V_semantics`;
- the future is ontically open;
- one hidden future is physically selected;
- finite clock covariance is general covariance.

## Validation

Stage 9D scientific validation, GitHub Actions run #1013:

**`733 passed in 372.31s`**.

A later test-only optimization reuses the same deterministic full-atlas diagnostic rather than recomputing it repeatedly; it changes no scientific condition.

## Next

**Stage 9E — P/O/R_direction/V compatibility matrix**: classify the now-executable pairwise and joint relations among direction, continuation multiplicity, weights, semantics, accessibility, perspective transport, and order using the frozen evidence vocabulary.