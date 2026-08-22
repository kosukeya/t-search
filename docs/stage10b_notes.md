# Stage 10B Notes — Continuation-Specific Measurement Lift / Normalization Choice

Status: **Stage 10B completed; criteria 17–23 satisfied.**

## Purpose

Stage 10B independently lifts the Stage 10A / Stage 9C reference future-signature measurement into each canonical continuation's own A/e2 QR-support and constrained physical coordinates, then selects the normalization representation that Stage 10C will transport.

This stage does **not** yet establish cross-clock measurement covariance.

## Continuation-specific pullback

For each `h in {h_L,h_R}`, let

`R_h = stage9_clock_reduction_matrix(h,"A",e2)`

be the continuation-specific reference reduction.

The Stage 9C ambient reference effect `E_o` is pulled back to physical coordinates as:

`F_{h,o}=R_h^dagger E_o R_h`.

The Stage 9C reduced-state norm is pulled back at the same time:

`N_h=R_h^dagger R_h`.

Hence the physical-coordinate probability rule is:

`p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

Because the Stage 9C reference effects satisfy `sum_o E_o=I`, the lifted forms satisfy:

`sum_o F_{h,o}=N_h`.

The lift is independently re-derived for h_L and h_R. No universal h-independent measurement lift is assumed.

## Reference QR-support representation

Writing the A/e2 reduction as

`R_h=Q_h C_h`,

Stage 10B also constructs the local QR-support effects:

`E^sup_{h,o}=Q_h^dagger E_o Q_h`.

At the A/e2 reference node the support normalization is the identity, so this is an ordinary local POVM and gives the same Stage 9C Born probabilities.

The physical effect form is the pullback of that local POVM:

`F_{h,o}=C_h^dagger E^sup_{h,o} C_h`,

`N_h=C_h^dagger C_h`.

The ambient-reduction and QR derivations are checked against one another.

## Normalization choice

Both the local reference POVM and the physical effect-form representation reproduce the Stage 9C reference likelihoods at A/e2.

However, Stage 9D genuine clock maps are generally non-Euclidean-unitary. For a genuine map `z_Y=S z_X`, the identity normalization transported as the same quadratic form is:

`I_Y=S^{-dagger} I_X S^{-1}`,

which is generally not the numerical identity matrix.

Therefore Stage 10B does **not** adopt the rule:

> normalize with a fresh identity matrix independently in every chart.

That would change the normalization object rather than transport it.

The retained Stage 10 transport representation is therefore:

**reference-induced physical-coordinate effect form with reference-induced operational normalization form**.

The chart-local POVM remains a correct reference-chart representation of the same object; it is not promoted to an identity-reset cross-chart convention.

`reference-chart identity normalization != identity normalization in every transported chart`.

## Distinction from the Stage 9D physical metric

Stage 9D's induced support metric tracks the norm of physical coordinates under clock change. Stage 10B's operational normalization instead tracks the Stage 9C normalized reduced-state Born rule.

These are kept as different typed resources.

Stage 10B does not infer:

`Stage 9D physical metric = Stage 10 operational normalization`.

Their relationship can be compared mathematically, but numerical or conceptual identity is not assumed.

## Correspondence typing

Each lift carries an explicit preserving continuation-class correspondence:

`h_L -> h_L`, `h_R -> h_R`,

and an explicit preserving outcome correspondence:

- `future_signature_left -> future_signature_left`;
- `future_signature_other -> future_signature_other`.

Continuation identity is checked before evaluating a lifted measurement. Applying an h_L lift to h_R, or vice versa, is rejected even though both coordinate arrays have dimension 14.

`same coordinate dimension != same continuation-specific measurement representation`.

## Criteria 17–23

17. Each continuation has an independently derived support/physical measurement representation — **satisfied**.
18. No universal h-independent measurement lift is assumed — **satisfied**.
19. Support effects, physical effect forms, and normalization forms are well-defined, positive in the declared form sense, and complete (`sum F=N`) — **satisfied**.
20. The retained normalization representation is selected by exact Stage 9C reference equivalence together with the nonunitary clock-map constraint, not by convenience — **satisfied**.
21. Both canonical continuations reproduce their Stage 9C reference likelihoods under the retained effect-form rule — **satisfied**.
22. Continuation-class and outcome correspondences are explicit — **satisfied**.
23. Wrong-continuation lift use is rejected — **satisfied**.

## Scope boundary

Stage 10B does not yet establish:

- valid measurement representations at every A/B/C chart;
- all genuine distinct-clock measurement transports;
- three-clock effect-form composition;
- transported completeness/positivity;
- per-continuation probability covariance across the full atlas;
- weighted/modal/update covariance;
- full Stage 10 future-measurement covariance.

Those begin in Stage 10C/D.

`normalization representation selected != measurement covariance established`.

`continuation-specific lift != hidden branch selection`.

`future-measurement representation != future actuality`.

`full finite-clock measurement covariance != general covariance`.

## Validation

Stage 10B scientific checkpoint: GitHub Actions run #1163:

**`795 passed in 462.74s (0:07:42)`**.

## Next

**Stage 10C — continuation-aware A/B/C measurement transport.**
