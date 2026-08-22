# Stage 10F Results — Ablation / Wrong-Typing / False-Positive Controls

Status: **Stage 10F completed; criteria 44–47 satisfied.**

## Executable classification matrix

| ablation | numerical payload | typed identification | measurement/probability covariance |
| --- | --- | --- | --- |
| remove event correspondence | `preserved` | `lost` | `not_established` |
| remove continuation-class correspondence | `preserved` | `lost` | `not_established` |
| remove outcome correspondence | `preserved` | `lost` | `not_established` |
| remove normalization semantics | `reconstructible` | `underdetermined` | `not_established` |
| fresh numerical identity normalization | `preserved` | `lost` | `refuted` |
| bare-effect reuse | `preserved` | `lost` | `refuted` |
| weight/class misalignment | `preserved` | `lost` | `refuted` |

The first three rows are deliberate false-positive cases: unchanged stored matrices/numbers do not authorize a fully typed covariance claim after their correspondence resource has been removed.

`numerical reconstructibility != typed operational identification`.

## Explicit control witnesses

The Stage 10F diagnostics expose the following executable residual/rejection fields:

- `bare_effect_residual > tolerance` and `bare_effect_rejected=True`;
- `wrong_continuation_form_residual > tolerance` and cross-continuation use is rejected;
- `wrong_outcome_probability_residual > tolerance` and swapped outcome correspondence is rejected;
- `wrong_event_rejected=True` for the misdeclared-preserving event map;
- `weight_misalignment_prediction_residual > tolerance` and misaligned weights are rejected;
- `fresh_identity_probe_residual > tolerance` and fresh-identity normalization is rejected on the tomography-complete probe family.

These witnesses close the loophole that a wrong typing could pass only because one canonical state or one convenient coordinate representation happened to give the same number.

## Correspondence result

Removing event, class, or outcome correspondence leaves the matrices directly present but removes the formal resource needed to say that source and target refer to the same event role, continuation class, or outcome identity.

Therefore:

`preserved numerical payload + missing chi != preserved typed measurement identity`.

This is classified as `lost` at the typed-identification level and `not_established` at the fully typed covariance level.

## Normalization result

Two distinct cases are separated.

1. **Semantics removed, matrix retained**: the form can still be reconstructed/read numerically, but its operational denominator role is underdetermined; covariance is `not_established`.
2. **Fresh identity substituted**: the rule makes different predictions on the valid Stage 10D tomography family; covariance is `refuted` for that corrupted rule.

`missing semantics != refuted numerical rule`.

## Weight alignment result

For the deliberately mismatched ontic weights `(0.75,0.25)`, Stage 10E correctly preserves their predictive effect across perspectives. Stage 10F then swaps their continuation-class alignment to `(0.25,0.75)` while retaining the same likelihood rows.

The weighted prediction changes by a nonzero residual above tolerance. Hence weight values without class alignment are insufficient to define the same weighted future prediction.

`same weight multiset != same continuation-weight assignment`.

## Criteria 44–47 assessment

44. Removing event/class/outcome correspondence classifies typed identifications using the project status vocabulary — **satisfied**.
45. Removing/corrupting normalization semantics classifies probability covariance as warranted — **satisfied**.
46. Bare-effect, wrong-continuation, wrong-outcome, wrong-event, and weight-misalignment controls receive explicit witnesses/residuals — **satisfied**.
47. Reconstruction/ablation results avoid metaphysical promotion — **satisfied**.

## Scientific interpretation

Stage 10F strengthens the positive Stage 10A–E result in a specific way: the measurement-covariance claim is not merely a consequence of carrying around numerically compatible matrices. Explicit correspondence and normalization semantics do functional work in defining the typed operational family.

This remains a finite formal conclusion only.

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`wrong-typing failure != ontological becoming`.

`finite-model ablation != fundamental ontology`.

## Validation

GitHub Actions run #1249:

**`843 passed in 575.02s (0:09:35)`**.

## Next

**Stage 10G — synthesis and evidence-selected next gate.**
