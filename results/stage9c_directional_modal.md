# Stage 9C Results — Typed Modal Models and Directional Operational Underdetermination

Status: **Stage 9C complete; criteria 24–30 satisfied.**

## Question

Does adding an explicit, accessible directional-record interface to the nontrivial Stage 9 continuation carrier determine whether Potentiality is epistemic — one complete continuation `h*` already selected but hidden — or ontic-extension-like — admissible continuations represented with no selected complete continuation datum?

## Executable answer

**No, not under the declared finite `O_QR` interface when the continuation weights are matched.**

Stage 9C places two type-distinct modal models on the exact same Stage 9A directional carrier:

`M_E^QR=(QRCarrier,e1,h*,q_E)`

and

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`.

The carrier contains the same two physically inequivalent continuations:

`QExt(e1)={h_L,h_R}`.

The epistemic model stores one hidden selected continuation. The ontic-extension model has no selected-continuation, selector, seed, precomputed branch, or arbitrary instance dictionary field.

## 1. Public directional interface

The Stage 9C ontology-neutral public projection is:

`O_QR=(current density,R_content,R_direction/R_access,Next_QR,future-signature probabilities,observed evidence)`.

The schema excludes:

- `selected_continuation`;
- `selected_history`;
- `selector`;
- `model_type`;
- `belief_weights` as a typed epistemic field;
- `extension_weights` as a typed ontic field.

The directional record interface is not branch-weighted. The implementation first verifies that every carrier continuation independently gives the same directional statistics, then exposes the common values:

`A_R=+1`

`A_acc=+0.5`

with lower-index orientation.

Thus the public arrow cannot be manufactured by selecting h_L, selecting h_R, or changing their mixture weights.

## 2. Matched modal comparison

With matched positive weights:

`q_E=K=(0.5,0.5)`,

the selected-`h_L` epistemic model and the no-selector ontic-extension model have equal `O_QR` views.

The privileged structural diagnostic still distinguishes them:

- epistemic: selected complete continuation present;
- ontic-extension: no selected complete continuation datum.

Therefore:

`operational directional equality != modal/ontological identity`.

This is an operational underdetermination result inside the declared finite model family.

## 3. Hidden-selector swap

Keeping the same carrier and weights while changing only the epistemic hidden selector:

`h*=h_L -> h*=h_R`

does not change the pre-update `O_QR` view.

The privileged test-only diagnostic detects the swap, but the public interface does not.

Therefore the directional record arrow does not expose the hidden selected continuation.

`hidden h* diagnostic != operational access to h*`.

## 4. Weight mismatch control

To ensure matched equality is not a vacuous consequence of an insensitive interface, Stage 9C changes only the ontic-extension weights:

`K=(0.75,0.25)`.

The current anchor, current density, current record joint distribution, current record information, and directional-record interface remain unchanged, while the future-signature prediction changes.

Thus `O_QR` is weight-sensitive where it should be, but the current directional arrow is not a disguised branch-weight aggregate.

`weight sensitivity != selected-continuation observability`.

`control of V_weights != determination of V_semantics`.

## 5. Future-signature measurement

Stage 9C derives the future measurement from the Stage 9 continuation-specific e2 states, not from the Stage 8 carrier.

The canonical measurement projects onto the h_L future ray and its orthogonal complement. The executable checks establish:

- completeness within tolerance;
- non-negative effects within tolerance;
- h_L/h_R future rays are operationally distinguishable (`overlap^2 < 1` within the declared tolerance).

The q_E/K values enter only as outer mixture weights over continuation-specific Born likelihoods.

## 6. Explicit evidence update

Stage 9C supplies explicit external evidence:

`future_signature_left`.

No branch is sampled internally.

Before update, matched epistemic and ontic-extension `O_QR` views are equal. Both models condition their weights on the same likelihoods. The epistemic model preserves its pre-existing hidden h*, while the ontic-extension update does not acquire a selected-continuation field.

With matched priors, the posterior weights match and the post-update public views remain equal. The anchor advances to terminal e2.

The terminal public view intentionally does not re-label the e1 directional diagnostic as a new e2 arrow: the pre-update `R_direction` interface is tied to its declared e1 anchor.

`explicit evidence update != ontological becoming`.

## Stage 9C criteria 24–30 assessment

24. Epistemic selected-`h*` and ontic no-selector models share the exact same nontrivial Stage 9 directional carrier — **satisfied**.
25. `O_QR` exposes current physical/record/directional/future-prediction data while excluding hidden selector and modal-type fields — **satisfied**.
26. With matched positive q_E/K weights, epistemic and ontic-extension `O_QR` views are equal while privileged modal structures remain distinct — **satisfied**.
27. Swapping only the hidden epistemic h* leaves the pre-update `O_QR` view unchanged while the privileged diagnostic detects the swap — **satisfied**.
28. Changing only continuation weights changes future prediction while preserving current density, record content, and directional data — **satisfied**.
29. Explicit common evidence conditions both models consistently, preserves the epistemic pre-existing h*, and does not create an ontic selected-continuation datum — **satisfied**.
30. The directional arrow remains present and continuation-independent before weighting, with underdetermination/becoming/weight-semantics guards explicit — **satisfied**.

## Scientific interpretation

Stage 8C showed selected-vs-unselected modal underdetermination on a carrier whose canonical continuation family did not itself carry a directional record arrow. Stage 9C strengthens that result by repeating the comparison **with a nonzero, accessible, continuation-independent `R_direction` explicitly included in the public interface**.

Within this declared finite model family:

`directional R + nontrivial V_extension + matched operational data`

still does not uniquely determine

`V_semantics`.

This is evidence for a structural separation between the presence of a directional record arrow and the selected-vs-unselected modal interpretation of Potentiality.

It is not a proof that nature admits both ontologies, that the future is ontically open, that one future is secretly fixed, or that becoming is fundamental.

## Guards

- `operational directional equality != modal/ontological identity`;
- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- `hidden h* diagnostic != operational access to h*`;
- `matched numerical q_E and K != matched probability semantics`;
- `explicit evidence update != ontological becoming`;
- `weight sensitivity != selected-continuation observability`;
- `control of V_weights != determination of V_semantics`;
- `underdetermined != ontically open`;
- `finite constrained-model success != empirical discovery`.

## Validation

Stage 9C implementation and focused modal tests passed in GitHub Actions run #995:

**`720 passed in 265.06s`**.

## Next

**Stage 9D — continuation-aware clock transport**: re-derive the A/B/C atlases on the Stage 9 directional carrier and test genuine cross-clock transport of states, directional record observables, event correspondences, continuation classes, and weights.