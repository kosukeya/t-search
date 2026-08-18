# Stage 2C — Ontic-Extension Model

Status: **completed**.

## Purpose

Stage 2C implements the formal object:

`M_O(D) = (D, Ext_T(D), K)`

on top of the neutral Stage 2A branching substrate.

The defining structural contrast with Stage 2B is that the model contains:

- current Actuality `D`;
- every admissible complete extension `Ext_T(D)`;
- weights `K` over those extensions;

but **no selected complete future history** and no field intended to act as an equivalent hidden selector.

This is a formal modeling choice. It does not establish that physical reality is ontically open.

## Baseline fixture

Use:

`D_0 = (p,n)`

with complete admissible extensions:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`.

The baseline state contains:

`OPot(D_0) = {h_L,h_R}`

and equal extension weights:

`K(h_L|D_0) = 1/2`

`K(h_R|D_0) = 1/2`.

Marginalizing those extension weights gives:

`pi_O(l1|D_0) = 1/2`

`pi_O(r1|D_0) = 1/2`.

## Typed ontic Potentiality

Stage 2C introduces:

`OnticPotentiality`

as a type-distinct carrier for admissible complete extensions.

It is deliberately separate from Stage 2B's:

`EpistemicPotentiality`.

The two types can contain the same history tuples while representing different model roles.

The local modal view is:

`G_O(D) = (A_now, OPot(D), pi_O(next|D))`.

## No selected-future datum

`OnticExtensionModel` contains the fields:

- `substrate`;
- `actuality`;
- `potentiality`;
- `extension_weights`.

It contains no:

- `selected_history`;
- `hidden_history`;
- equivalent explicit future-selection field.

The constructor also requires:

`potentiality == Ext_T(actuality)`

by deriving the potentiality from the neutral substrate and validating that the supplied weights cover exactly all live extensions.

Thus the model represents all admissible futures without designating one as already actual.

## Update semantics

The update receives an observed next event explicitly. It does not randomly choose an event internally.

For observation:

`l1`

Actuality changes:

`(p,n) -> (p,n,l1)`.

The incompatible right extension is removed, leaving:

`OPot = {h_L}`

with normalized weight:

`K(h_L)=1`.

The immediate-next prediction becomes:

`pi_O(l2)=1`.

No selected complete future field is created by the update.

## Symmetric admissibility control

A key contrast with the Stage 2B baseline is that the same initial ontic state can also accept:

`r1`.

Then:

`Actuality = (p,n,r1)`

`OPot = {h_R}`

and the branch is terminal.

This differs from the Stage 2B actual-run fixture with hidden `h*=h_L`, where observation `r1` is rejected as inconsistent with the already-selected history.

This is a difference in formal model semantics, not evidence that one ontology describes physical reality.

## Terminal behavior

Following:

`(p,n) -> l1 -> l2`

produces the terminal Actuality:

`(p,n,l1,l2)`.

The only compatible complete extension is the current complete history itself and the immediate-next probability distribution is empty.

## Weight validation

The extension-weight map must:

- cover exactly all members of `Ext_T(D)`;
- use finite non-negative values;
- sum to one.

A zero-weight branch can remain structurally admissible in `OPot`, but an attempted actual-run update into a branch whose total surviving weight is zero is rejected.

This keeps structural admissibility and positive transition weight conceptually distinct.

## Validation

The execution environment still cannot clone GitHub because DNS resolution for `github.com` fails. Therefore the current validation is not a GitHub Actions/full-repository run.

A focused semantic harness reproducing the Stage 2A substrate semantics and the committed Stage 2C logic passed:

`10 Stage 2C semantic checks passed`.

The committed test file covers:

1. baseline Actuality and all admissible extensions;
2. absence of selected-future fields and type distinction from epistemic Potentiality;
3. baseline `1/2,1/2` immediate-next probabilities;
4. local view contains no selected-history datum;
5. left update extends Actuality and prunes extensions;
6. right update is also admissible from the same unselected baseline;
7. terminal behavior;
8. invalid observation rejection;
9. exact-coverage and normalization validation for `K`;
10. zero-weight branch semantics.

A full repository pytest run should be performed later when the checkout/network path is available, and in any case before Stage 2 merge review.

## Classification

### Local observable / locally accessible at Stage 2C

- current Actuality/prefix;
- current ontic extension set `OPot(D)`;
- immediate-next predictive weights.

### Internal/formal property

- the absence of a selected complete future from the model state;
- the full extension-weight representation from which next-event probabilities are derived.

### Not a hidden lost property

There is no `h*` hidden by the Stage 2C projection. The selected-future datum is absent from the model state rather than stored and concealed.

### Not a strict invariant

The baseline branching structure and probabilities are shared by construction with later comparison models. Their agreement is not yet a strict physical invariant.

## Interpretation discipline

Stage 2C establishes that a formalism can represent current Actuality plus multiple admissible extensions without containing an explicit preselected complete future.

It does **not** establish ontic becoming or an open physical future.

The key formal contrast now available is:

`Stage 2B: selected-future information exists globally and is locally hidden`

versus:

`Stage 2C: selected-future information is absent from the model state`.

Stage 2D can now compare the ontology-neutral operational outputs of those two distinct internal structures under matched weights.
