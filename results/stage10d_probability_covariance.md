# Stage 10D Results — Per-Continuation Born / Completeness / Positivity Covariance

Status: **Stage 10D completed; criteria 32–38 satisfied.**

## Question

Does the fully typed continuation-specific future-signature measurement retain the same Born probabilities over the entire genuine A/B/C clock atlas, before continuation weights are restored?

## Executable answer

**Yes, in the declared finite per-continuation family.**

For each canonical continuation `h in {h_L,h_R}` and each of its nine A/B/C clock/readout charts, Stage 10D evaluates:

`p(o|h,X,j)=z^dagger F^X_{h,o} z / (z^dagger N^X_h z)`.

All corresponding chart probabilities agree within tolerance and reproduce the Stage 9C per-continuation future-signature likelihoods.

The comparison is performed before any branch-weight aggregation.

## Canonical evaluation count

- 2 continuations;
- 9 charts per continuation;
- 2 outcomes;
- **36 canonical outcome-probability evaluations**.

The canonical probabilities satisfy completeness and positivity at probability level:

- `sum_o p(o)=1` within tolerance;
- all tested `p(o)` remain in `[0,1]` within tolerance;
- normalization denominators remain positive.

## Outcome semantics control

The preserving correspondence retains:

`future_signature_left -> future_signature_left`

and

`future_signature_other -> future_signature_other`.

A swapped correspondence is rejected. The canonical likelihood family is numerically discriminating, so the swap is not hidden by a symmetric outcome distribution.

## Tomography-complete probe result

Stage 10D uses **196 valid constrained physical-coordinate probes**:

`14 + 2*C(14,2) = 196`.

The family contains all coordinate basis probes and both real and phase pair-superpositions. It is sufficient to distinguish Hermitian quadratic forms rather than only probing a small canonical subspace.

Total probe outcome evaluations:

`2 x 196 x 9 x 2 = 7056`.

The correctly transported Stage 10 measurement retains probability covariance, completeness, and positivity over this full probe family.

This strengthens the canonical result:

`canonical-state equality != tomography-complete covariance`.

## Normalization controls

### Fresh identity

A fresh numerical identity used independently as the denominator form in transported charts is rejected on the probe family.

### Pilot metric-control correction

The initial run #1209 used the correctly corresponding Stage 9D physical metric as if it had to be a numerically different normalization merely because its typing differs from the Stage 10 operational normalization. That premise was not justified.

Run #1209 therefore ended with:

**`818 passed / 4 failed`**.

The four failed assertions were consequences of the single assumption that the correctly corresponding physical metric itself must be rejected. The actual canonical/probe probability covariance and Stage 9C reference reproduction were already positive.

The corrected control uses a **misaligned chart metric**—a metric from a different chart without the required transport/correspondence. The 196-probe family detects the resulting wrong normalization.

This yields a useful refinement:

`typed-resource distinction != numerical inequality`.

The result does not collapse the Stage 9D physical metric and Stage 10 operational normalization into one semantic role. It only avoids treating distinct typing as proof of numerical difference.

## Criteria 32–38

32. Per-continuation probabilities invariant across all corresponding chart nodes — **satisfied**.
33. All transported charts reproduce Stage 9C reference likelihoods — **satisfied**.
34. Per-continuation covariance established before weighting — **satisfied**.
35. Swapped/misdeclared outcome correspondence detected — **satisfied**.
36. Fresh-identity and genuinely misaligned-metric errors detected — **satisfied**.
37. 196-state tomography-complete constrained family rules out accidental canonical equality — **satisfied**.
38. Evidence status assigned explicitly — **satisfied**.

## Evidence status

For the declared finite measurement family:

`full typed future-measurement covariance = established`

with the explicit scope:

**per-continuation / pre-weighting / typed A/B/C finite atlas**.

The following remain separate Stage 10E work:

`weighted/modal/update covariance = not_established`.

Thus:

`per-continuation measurement covariance established != modal/ontological identity`.

`per-continuation measurement covariance established != future actuality`.

`per-continuation measurement covariance established != ontic future openness`.

`full finite-clock measurement covariance != general covariance`.

## Validation

Corrected scientific checkpoint, GitHub Actions run #1213:

**`823 passed in 311.17s (0:05:11)`**.

## Next

**Stage 10E — weights, modal models, and evidence-update covariance.**
