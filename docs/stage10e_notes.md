# Stage 10E Notes — Weights, Modal Models, and Evidence-Update Covariance

Status: **Stage 10E completed; criteria 39–43 satisfied.**

## Purpose

Stage 10D established the fully typed future-signature measurement family at the per-continuation / pre-weighting level. Stage 10E restores the Stage 9C continuation weights and modal roles without changing their semantics, and asks whether the public weighted predictions and common evidence updates remain consistent across the full A/B/C clock atlas.

This stage reuses the Stage 9C model pair:

`M_E^QR=(QRCarrier,e1,h*,q_E)`

and

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`.

The Stage 10D chart-local per-continuation likelihoods replace only the old reference-node likelihood lookup. The epistemic/ontic typing and Bayes semantics are unchanged.

## Weighted prediction covariance

At each chart `(X,j)`, Stage 10E forms:

`P_{X,j}(o)=sum_h w_h p^h_{X,j}(o)`.

For matched `q_E=K=(0.5,0.5)`, the resulting weighted predictions are the same at all nine A/B/C chart nodes within tolerance.

The aggregation is performed only after Stage 10D has independently established each `p^h_{X,j}(o)`.

`weighted covariance != substitute for per-continuation covariance`.

## Matched epistemic / ontic-extension public measurement views

The Stage 10E public view combines the Stage 9D perspective-level public carrier data with the Stage 10 weighted future-measurement prediction.

With matched weights, the epistemic and ontic-extension views agree at every declared chart. Their privileged modal structures nevertheless remain distinct:

- the epistemic model retains one hidden selected continuation `h*`;
- the ontic-extension model contains no selected complete-continuation datum.

Therefore:

`matched public measurement views != modal/ontological identity`.

## Hidden h* swap

Keeping the same carrier and matched weights while changing the hidden epistemic selector from h_L to h_R leaves every Stage 10E public measurement view unchanged.

The public schema contains no field named or equivalent to:

- `selected_continuation`;
- `selected_continuation_id`;
- `selector`;
- `model_type` / `modal_type`;
- `belief_weights` / `extension_weights` as semantic model-role fields.

The weights themselves are exposed only as continuation weights in the public operational representation, not as evidence of the model's privileged modal interpretation.

`hidden h* swap invariance != selected-continuation observability`.

## Weight mismatch

The control `K=(0.75,0.25)` remains predictively distinct from the matched `(0.5,0.5)` case at every perspective because the Stage 10 future-signature likelihoods discriminate the two continuation classes.

The mismatch produces the same prediction difference at every corresponding chart within tolerance.

Thus Stage 10E establishes both:

- weight sensitivity;
- perspective-stable operational meaning of that sensitivity.

`weight sensitivity != selected-continuation observability`.

`control of V_weights != determination of V_semantics`.

## Common evidence conditioning

Stage 10E uses the externally supplied evidence:

`future_signature_left`.

At every chart it independently computes the likelihood vector from the Stage 10D typed measurement family and applies the same Bayes rule as Stage 9C.

The epistemic and ontic-extension posterior weights:

- are invariant across all nine charts;
- agree with each other for matched priors;
- reproduce the Stage 9C posterior values;
- preserve the hidden epistemic selected continuation;
- leave the updated ontic-extension state selector-free.

The Stage 9C update objects remain the semantic authority. A chart-local posterior that disagrees with the Stage 9C update semantics is rejected.

`evidence-update covariance != ontological becoming`.

`posterior equality != modal-semantic identity`.

## Criteria 39–43

39. Weighted future predictions are covariant under valid class/weight/outcome correspondence — **satisfied**.
40. Matched epistemic/ontic-extension public measurement views agree across all declared nodes — **satisfied**.
41. Hidden epistemic h* swaps remain outside the public typed measurement schema — **satisfied**.
42. Weight mismatch remains predictively visible with the same operational meaning across perspectives — **satisfied**.
43. Common evidence conditioning/posteriors are perspective-consistent and the ontic update remains selector-free — **satisfied**.

## Evidence status

Stage 10E upgrades the Stage 10D scope:

`weighted/modal/update operational covariance = established`

for the declared finite A/B/C measurement family.

This means the **operational transport and update behavior** of the matched epistemic and ontic-extension models is covariant. It does not collapse their privileged modal semantics.

The following guards remain active:

- `measurement covariance != modal/ontological identity`;
- `matched operational equality != matched probability semantics`;
- `weight covariance != selected-continuation observability`;
- `evidence-update covariance != ontological becoming`;
- `future-measurement covariance != future actuality`;
- `full finite-clock measurement covariance != general covariance`.

## Validation

Stage 10E scientific checkpoint, GitHub Actions run #1233:

**`834 passed in 455.24s (0:07:35)`**.

## Next

**Stage 10F — ablation / wrong-typing / false-positive controls.**
