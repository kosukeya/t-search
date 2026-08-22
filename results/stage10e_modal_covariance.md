# Stage 10E Results — Weights, Modal Models, and Evidence-Update Covariance

Status: **Stage 10E completed; criteria 39–43 satisfied.**

## Question

After Stage 10D establishes per-continuation future-measurement covariance, do continuation-weight aggregation, matched epistemic/ontic-extension public views, hidden-selector invariance, weight sensitivity, and common evidence conditioning retain the same operational meaning across the full A/B/C clock atlas?

## Executable answer

**Yes, in the declared finite operational family.**

Stage 10E leaves the Stage 9C modal semantics unchanged and uses the Stage 10D per-continuation chart likelihoods as the likelihood table for weighting and conditioning.

## Weighted predictions

For each chart `(X,j)`:

`P_{X,j}(o)=sum_h w_h p^h_{X,j}(o)`.

With matched `q_E=K=(0.5,0.5)`, the weighted prediction is invariant over all nine declared A/B/C nodes within tolerance.

Because Stage 10D already established per-continuation covariance, this result is not produced by a cancellation between incorrectly transported branch likelihoods.

`weighted equality != substitute for branchwise covariance`.

## Matched public views

The Stage 10E public measurement view contains the transported public perspective data plus the typed future outcomes and weighted outcome probabilities.

For matched priors, the epistemic and ontic-extension public views agree at every chart, while their privileged structures remain distinct:

- epistemic: hidden selected complete continuation present;
- ontic extension: no selected complete continuation datum.

`operational equality != modal/ontological identity`.

## Hidden h* swap

Changing the hidden epistemic selected continuation from h_L to h_R while keeping the same public carrier and weights leaves every Stage 10E public view unchanged.

The public view schema contains no hidden selector or modal-model-type field.

`hidden h* diagnostic != operational access to h*`.

## Weight mismatch

The control `K=(0.75,0.25)` changes the future-signature prediction relative to the matched `(0.5,0.5)` case at every chart.

The mismatch effect itself is perspective-covariant: the mismatched prediction is the same operational prediction at every corresponding node within tolerance.

Thus:

`weight sensitivity = preserved`

while:

`selected-continuation observability = not implied`.

## Evidence update

Common evidence `future_signature_left` is conditioned independently at every chart using the transported typed likelihoods.

The resulting posterior weights:

- are chart-invariant;
- match between the epistemic and ontic-extension models for matched priors;
- reproduce the Stage 9C posterior values;
- preserve the epistemic hidden selection;
- do not introduce a selected complete continuation into the ontic-extension update.

Therefore:

`evidence-update covariance = established`

in the declared finite operational family.

This remains an explicit Bayesian/evidential update result:

`evidence-update covariance != ontological becoming`.

## Criteria 39–43 assessment

39. Weighted future predictions covariant under valid class/weight/outcome correspondence — **satisfied**.
40. Matched epistemic/ontic-extension public measurement views agree across all declared nodes — **satisfied**.
41. Hidden epistemic h* swaps remain absent from the public typed measurement schema — **satisfied**.
42. Weight mismatch remains predictively visible with perspective-stable operational meaning — **satisfied**.
43. Common evidence posteriors are perspective-consistent and ontic update remains selector-free — **satisfied**.

## Evidence status

After Stage 10E:

`weighted/modal/update operational covariance = established`

for the declared typed finite A/B/C future-measurement family.

This upgrades the Stage 10D pre-weighting result to the declared public weighted and update layer, but it does **not** establish modal-semantic identity, ontic future openness, future actuality, or ontological becoming.

`matched public equality != modal-semantic identity`.

`weight covariance != V_semantics identity`.

`future-measurement covariance != future actuality`.

`full finite-clock measurement covariance != general covariance`.

## Validation

GitHub Actions run #1233:

**`834 passed in 455.24s (0:07:35)`**.

## Next

**Stage 10F — ablation / wrong-typing / false-positive controls.**
