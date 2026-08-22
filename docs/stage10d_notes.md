# Stage 10D Notes — Per-Continuation Born / Completeness / Positivity Covariance

Status: **Stage 10D completed; criteria 32–38 satisfied.**

## Purpose

Stage 10C established covariance of the typed measurement **representation**. Stage 10D evaluates the corresponding Born probabilities themselves before any continuation-weight aggregation.

For each continuation `h`, chart `(X,j)`, and outcome `o`, the declared rule is:

`p(o|h,X,j)=z^dagger F^X_{h,o} z / (z^dagger N^X_h z)`.

The canonical continuation states must agree at all A/B/C nodes and reproduce the unchanged Stage 9C future-signature likelihoods. Additional valid constrained inputs are then used to exclude accidental canonical-state equality and to make wrong-normalization controls discriminating.

## Canonical per-continuation covariance

The evaluation is performed separately for `h_L` and `h_R` over all nine A/B/C clock/readout charts per continuation.

Thus the canonical measurement check contains:

- 2 continuations;
- 9 charts per continuation;
- 2 outcomes per chart;
- 36 canonical outcome-probability evaluations.

All declared corresponding nodes agree within tolerance, and every node reproduces the Stage 9C reference likelihood for the same continuation/outcome.

No continuation weights are used in this comparison.

`per-continuation covariance != weighted covariance by definition`.

## Probability-level completeness and positivity

Stage 10D does not rely only on the Stage 10C matrix-level result. For canonical and probe inputs it independently checks:

- positive normalization denominator;
- `sum_o p(o)=1` within tolerance;
- each outcome probability lies in `[0,1]` within tolerance.

This supplies an operational probability-level check of the retained effect/normalization representation.

## Swapped-outcome control

The preserving outcome correspondence remains:

- `future_signature_left -> future_signature_left`;
- `future_signature_other -> future_signature_other`.

A swapped outcome correspondence is rejected semantically, and the canonical measurement is numerically discriminating rather than a symmetric `0.5/0.5` case that would hide the swap.

`same two outcome labels != same outcome correspondence`.

## Tomography-complete constrained probe family

The first Stage 10D implementation used 41 probe states. The final implementation strengthens this to a **196-state Hermitian-tomography-complete physical-coordinate family**:

- 14 coordinate-basis probes `e_i`;
- for every `i<j`, `(e_i+e_j)/sqrt(2)`;
- for every `i<j`, `(e_i+i e_j)/sqrt(2)`.

These probes determine all diagonal, real off-diagonal, and imaginary off-diagonal components of a Hermitian quadratic form. Each probe is interpreted in the continuation-specific 14D physical basis and is therefore a valid constrained input in the declared finite construction.

The full probe check covers:

`2 continuations x 196 probes x 9 charts x 2 outcomes = 7056`

probe outcome-probability evaluations.

Correctly transported measurement forms remain probability-covariant over this family.

`canonical-state equality != tomography-complete covariance`.

## Normalization / metric controls

### Fresh identity normalization

Using a fresh numerical identity matrix as the denominator form in every chart is rejected on the discriminating probe family.

This is the direct operational counterpart of the Stage 10B nonunitarity warning:

`reference-chart identity normalization != identity normalization in every transported chart`.

### Stage 9D physical metric and the pilot correction

The pilot Stage 10D run (#1209) required the correctly corresponding Stage 9D physical metric itself to produce different probabilities from the Stage 10 operational normalization. That requirement was too strong.

The Stage 9D physical metric and Stage 10 operational normalization remain **differently typed resources**, but different typing does not entail numerical inequality on a particular finite carrier or state family.

The pilot therefore produced:

**`818 passed / 4 failed`**

with the substantive covariance checks passing and the failure cascading from the overly strong `correct physical metric must be rejected` control.

The corrected criterion uses a genuinely wrong **misaligned-chart metric**: a metric from a different clock chart is applied without the required correspondence/transport. A tomography-complete probe family detects this mismatch.

`typed-resource distinction != numerical inequality`.

`correct physical metric != wrong metric merely because its semantic role differs`.

`misaligned chart metric != transported operational normalization`.

## Criterion 37 and accidental equality

Accidental canonical equality is ruled out by the combination of:

1. covariance on the 196-state tomography-complete constrained probe family;
2. rejection of fresh-identity normalization;
3. rejection of a genuinely misaligned chart metric;
4. explicit swapped-outcome rejection.

Thus the positive result is not supported only by the two canonical continuation states.

## Evidence status

Stage 10D assigns:

`full typed future-measurement covariance = established`

**for the declared per-continuation, pre-weighting finite measurement family**.

This status includes:

- typed representation covariance from Stage 10C;
- per-continuation probability covariance;
- Stage 9C reference-likelihood reproduction;
- completeness/positivity at the probability level;
- outcome correspondence;
- normalization controls;
- tomography-complete discriminating probes.

It does **not** yet include the Stage 10E layer:

- continuation-weight aggregation;
- matched epistemic/ontic-extension public measurement views;
- hidden epistemic `h*` swap checks across charts;
- weight-mismatch transport;
- common evidence conditioning/posteriors.

Therefore the remaining Stage 10E boundary is explicitly:

`weighted/modal/update covariance = not_established`.

And:

`per-continuation measurement covariance established != weighted/modal/update covariance established`.

## Criteria 32–38

32. Per-continuation outcome probabilities invariant across all declared corresponding nodes — **satisfied**.
33. Every chart reproduces Stage 9C reference likelihoods for each continuation/outcome — **satisfied**.
34. Likelihood covariance established before branch-weight aggregation — **satisfied**.
35. Swapped/misdeclared outcome correspondence detected — **satisfied**.
36. Fresh-identity and genuinely misaligned-metric normalization errors detected on a discriminating family — **satisfied**.
37. Accidental canonical-state equality ruled out with 196 tomography-complete valid constrained probes — **satisfied**.
38. Scoped full typed future-measurement covariance status explicitly assigned `established` — **satisfied**.

## Validation

Pilot diagnostic run #1209: **`818 passed / 4 failed`**. The four failures traced to one overly strong negative-control premise; canonical/probe covariance itself passed.

Corrected Stage 10D scientific checkpoint, GitHub Actions run #1213:

**`823 passed in 311.17s (0:05:11)`**.

## Next

**Stage 10E — weights, modal models, and evidence-update covariance.**
