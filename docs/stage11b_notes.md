# Stage 11B Notes — Relational Observables and Relational Derivatives

Status: **Stage 11B implementation checkpoint; criteria 17–23 targeted.**

Stage 11A established one finite sampled constraint orbit represented in four admissible positive external parameterizations. Stage 11B asks whether the relational quantities frozen in the Stage 11.0 protocol are actually independent of that external parameterization on the declared family.

Stage 11A repository-level baseline: GitHub Actions run #1309 passed **`883 passed in 630.96s (0:10:30)`**.

## 1. Relational observable

The Stage 11B observable is

`q(T=tau)`.

A relational observation is located by a unique internal-clock reading `T=tau` and retains:

- physical event id;
- parameterization id;
- raw external parameter value;
- internal-clock value;
- q value.

The lookup does not use equality of raw external parameter labels. Cross-parameterization comparison first calls the explicit Stage 11A physical-event correspondence and then reconstructs the observation at the common internal-clock reading.

`equal raw lambda != physical-event correspondence`.

## 2. Relational derivative

The tested relational derivative is

`dq/dT = (dq/dlambda)/(dT/dlambda)`.

Since the Stage 11A carrier obeys

`dq/dlambda = N(lambda) p`

and

`dT/dlambda = N(lambda)`,

the relational derivative should reconstruct `p=1.25` in every admissible parameterization even though the raw derivative changes under nonlinear reparameterization.

The positive family contains 4 parameterizations × 13 events = **52 relational-derivative evaluations**.

## 3. Anti-triviality witness

The nonlinear cubic and hyperbolic charts are compared directly with the identity chart. The raw `dq/dlambda` rates differ at **24 sampled chart-event points in total** (12 cubic + 12 hyperbolic; the central source point has unit Jacobian and therefore coincides).

Thus Stage 11B does not infer covariance merely from unchanged discrete event labels.

`raw parameter derivative equality != reparameterization covariance criterion`.

## 4. Explicit anchor/target typing

Stage 11B keeps two physical event roles explicit on the classical precursor:

- prediction anchor: `orbit_event_06`;
- measurement target: `orbit_event_10`.

Each role is represented in all four parameterizations, giving **8 typed anchor/target views**. The physical event ids and internal-clock readings are fixed while raw parameter values are allowed to differ.

These classical precursor roles do not replace the Stage 10 `e1 -> e2` quantum measurement typing; Stage 11D will perform that lift.

## 5. Equal-raw-parameter false comparison

The identity and affine parameterizations provide a direct false-matching control.

There are **7** pairs with the same numerical raw parameter value. Only **1** pair is also the same explicit physical event. The remaining **6** equal-raw-lambda pairs correspond to different event ids and different internal-clock readings.

The executable control therefore classifies raw-equal-parameter event matching as

`invalid_equal_raw_parameter_event_rule`.

This is a bounded logical result: equal numerical parameter values are insufficient as an event-identification rule in the declared family. It is not a claim that every possible coordinate coincidence must fail.

## 6. Criteria 17–23

Stage 11B closes only if the executable diagnostics establish:

17. `q(T=tau)` is constructed at corresponding physical events;
18. relational observable values agree across all four positive parameterizations;
19. relational derivatives agree across the positive family;
20. at least one nonlinear map demonstrably changes raw parameter derivatives;
21. anchor/target physical-event typing remains explicit;
22. equal raw parameter labels are not used as event identity;
23. the raw-parameter false comparison is rejected/classified as invalid.

No Stage 11C–G criterion is claimed here.

## Interpretation guards

- `parameter label != internal clock reading`;
- `parameter label != event identity`;
- `equal raw lambda != physical-event correspondence`;
- `relational observable covariance != full O/P/R/V covariance`;
- `relational derivative covariance != measurement covariance`;
- `relational covariance on one finite orbit != general covariance`;
- `absence of preferred external parameterization != absence of ontological becoming`;
- `parametrized covariance precursor != general relativity`;
- `finite-model success != empirical discovery`.

Next checkpoint after successful validation: **Stage 11C — typed O/P/R/V/Xi lift.**
