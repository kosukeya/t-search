# Stage 2C Design Notes — Ontic Extension Model

Status: **implemented**.

These notes explain implementation choices that should remain visible when Stage 2D compares the epistemic and ontic models.

## 1. Model state

The Stage 2C state is represented by:

`M_O(D) = (D, Ext_T(D), K)`.

The implementation stores:

- the neutral branching substrate `T`;
- current Actuality `D`;
- a typed `OnticPotentiality` containing every member of `Ext_T(D)`;
- normalized weights over those complete extensions.

There is no selected complete future field.

## 2. Why store complete-extension weights?

The Stage 2 protocol permits `K` either as immediate transition weights or as an equivalent normalized marginal over admissible extensions.

Stage 2C uses weights over complete live extensions because:

- the full admissible extension set is already central to the model semantics;
- immediate-next probabilities are then derived by marginalization;
- update after an observed event is implemented by filtering incompatible complete extensions and renormalizing;
- no extra hidden branch selector is needed.

This choice is only a representation of `K`; it is not a claim that physical chance fundamentally lives on complete histories.

## 3. Potentiality is type-distinct

`OnticPotentiality` is a different class from Stage 2B's `EpistemicPotentiality`.

This prevents identical carrier sets such as:

`{h_L,h_R}`

from silently erasing their different model roles.

- epistemic: hypotheses about an already-selected `h*`;
- ontic: admissible extensions with no selected `h*` in the model state.

## 4. No selected-future selector

The dataclass intentionally contains only:

`substrate, actuality, potentiality, extension_weights`.

Tests inspect the field names and require that `selected_history` / `hidden_history` are absent.

This cannot prove a metaphysical fact about reality. It only verifies that the software formalism follows the frozen Stage 2C specification rather than secretly reintroducing the Stage 2B semantics.

## 5. Update semantics

`update_ontic_model(model, observed_next)`:

1. checks that `observed_next` is an admissible immediate continuation of current Actuality;
2. extends `D` by that event;
3. removes complete extensions incompatible with the new prefix;
4. renormalizes surviving extension weights;
5. constructs a new ontic state with no selected future.

The function does not sample an event internally.

Thus:

`simulation update != evidence of ontic becoming`.

## 6. Left/right contrast with Stage 2B

At the canonical `D_0`, the ontic model has both left and right continuations as live extensions.

Therefore both explicit observations:

`l1`

and:

`r1`

can update the same initial ontic model when both carry positive weight.

By contrast, Stage 2B's baseline actual-run model has hidden `h*=h_L`; an actual observation `r1` is inconsistent with that model state and is rejected.

This formal contrast is useful, but Stage 2D should compare the models through the frozen ontology-neutral operational interface rather than privileged update consistency alone.

## 7. Zero-weight extensions

Structural admissibility and transition weight are kept separate.

An extension can appear in `OPot(D)` with weight zero. It remains allowed by the substrate but is impossible under the current `K` assignment.

Attempting to update into a zero-total-weight branch is rejected.

This distinction will be useful for the Stage 2F weight-mismatch control.

## 8. Validation limitation

The current execution environment cannot resolve `github.com`, so a clean checkout/full pytest run was unavailable during Stage 2C implementation.

A focused semantic harness passed 10 checks against the committed Stage 2C logic. The repository test file is committed and should be included in the next available full regression run before Stage 2 merge.

## 9. Next comparison

Stage 2D should introduce an ontology-neutral operational representation:

`O(G) = (A_now, Next(D), pi(next|D))`

and compare:

`O(G_E(D_0))`

with:

`O(G_O(D_0))`.

With the baseline matched weights, the expected result is operational equality despite the different internal selected-future semantics.
