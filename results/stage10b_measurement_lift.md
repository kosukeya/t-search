# Stage 10B Results — Continuation-Specific Measurement Lift / Normalization Choice

Status: **Stage 10B completed; criteria 17–23 satisfied.**

## Question

Can the Stage 9C future-signature measurement be independently lifted into each h_L/h_R constrained coordinate system without changing the reference likelihoods, and which normalization object should be retained for later genuine clock transport?

## Executable answer

**Yes.**

For each canonical continuation `h`, Stage 10B independently derives:

`F_{h,o}=R_h^dagger E_o R_h`

and

`N_h=R_h^dagger R_h`,

where `R_h` is that continuation's own A/e2 reduction and `E_o` is the unchanged Stage 9C reference effect.

The resulting effect forms satisfy:

`sum_o F_{h,o}=N_h`,

and reproduce the Stage 9C per-continuation reference likelihoods under:

`p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

## Support/physical equivalence

The continuation-specific QR factorization `R_h=Q_h C_h` gives an ordinary reference support POVM:

`E^sup_{h,o}=Q_h^dagger E_o Q_h`,

with identity normalization at A/e2.

The physical form is independently checked against:

`F_{h,o}=C_h^dagger E^sup_{h,o} C_h`,

`N_h=C_h^dagger C_h`.

Both the support POVM calculation and physical effect-form calculation reproduce the same Stage 9C reference probabilities for h_L and h_R within tolerance.

## Evidence-selected normalization representation

The reference-chart local POVM is valid, but it is not selected as an `I in every chart` transport convention.

Stage 9D genuine clock-change matrices are non-Euclidean-unitary in the declared atlas. Consequently, transporting the reference identity normalization as the same quadratic form yields:

`S^{-dagger} I S^{-1}`,

which is not generally `I`.

The executable nonunitarity and transported-identity controls are nonzero above tolerance.

Therefore the retained representation for Stage 10C is:

**reference-induced physical-coordinate effect form + reference-induced operational normalization form**.

The local A/e2 POVM is retained as a representation of this object at the reference chart, not as permission to reset normalization independently after clock change.

`local POVM validity != cross-chart identity-reset validity`.

## Typed-resource separation

The Stage 10 operational normalization is not identified with the Stage 9D physical-norm metric.

- Stage 9D metric: tracks physical-coordinate norm under perspective change.
- Stage 10B normalization: pulls back the Stage 9C reduced-state normalization used by the future-signature Born rule.

`physical metric != operational normalization by definition`.

## Wrong-continuation control

The h_L and h_R lifts are separately typed. A lift belonging to one continuation cannot be evaluated as if it belonged to the other continuation; such cross-use is rejected.

This prevents a numerically shape-compatible 14D matrix from silently becoming a universal h-independent measurement object.

`same shape != same typed measurement`.

## Criteria 17–23 assessment

17. Independent h_L/h_R support/physical lifts — **satisfied**.
18. No universal h-independent measurement map assumed — **satisfied**.
19. Effect/effect-form and normalization objects mathematically valid — **satisfied**.
20. Retained normalization selected from Stage 9C equivalence plus genuine-map nonunitarity, not convenience — **satisfied**.
21. Reference-node probabilities agree with Stage 9C for both continuations — **satisfied**.
22. Class and outcome correspondences explicit — **satisfied**.
23. Wrong-continuation lift rejected — **satisfied**.

## Scientific interpretation

Stage 10B closes a representation ambiguity left open by Stage 10.0.

The Stage 9C future question can be encoded as a continuation-specific quadratic-form pair `(F,N)` without changing the reference probabilities. This supplies a single object whose numerator and denominator can both be represented in later clock charts.

What has **not** yet been shown is that this object actually remains valid and probability-covariant over every h_L/h_R A/B/C chart. That is the Stage 10C/D question.

`effect-form lift exists != full measurement-family covariance`.

`normalization transport candidate selected != normalization transport validated over the atlas`.

`measurement representation != modal/ontological identity`.

## Validation

GitHub Actions run #1163:

**`795 passed in 462.74s (0:07:42)`**.

## Next

**Stage 10C — continuation-aware A/B/C measurement transport.**
