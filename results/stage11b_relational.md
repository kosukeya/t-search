# Stage 11B Results — Relational Observables and Relational Derivatives

Status: **criteria 17–23 satisfied by the Stage 11B executable diagnostics, pending final current-head repository regression.**

Stage 11A repository baseline: run #1309 — **`883 passed in 630.96s (0:10:30)`**.

## Carrier and positive family

Stage 11B reuses the Stage 11A constrained precursor without changing the physical orbit:

`C = p_T + p^2/2 = 0`

with four positive admissible external parameterizations and 13 explicit physical events.

## Relational observable result

The executable observable is

`q(T=tau)`.

Across 4 parameterizations × 13 events:

- relational-observable evaluations: **52**;
- maximum corresponding-event `q(T=tau)` residual: **0.0** within the deterministic carrier;
- physical event identity is supplied by explicit correspondence plus the common internal-clock reading, not by equal raw external parameter values.

Bounded result:

`Stage 11B q(T=tau) covariance on the frozen positive family = established`.

## Relational derivative result

The executable derivative is

`dq/dT=(dq/dlambda)/(dT/dlambda)`.

Across 4 parameterizations × 13 events:

- relational-derivative evaluations: **52**;
- reference `dq/dT`: **1.25**;
- maximum cross-parameterization relational-derivative residual: **0.0** within numerical tolerance;
- maximum residual against the canonical momentum `p`: **0.0** within numerical tolerance.

At the same time, the cubic and hyperbolic parameterizations change the raw `dq/dlambda` rate at **24** sampled chart-event points in total. The largest raw-rate difference in the frozen family is approximately **1.2263808139534884**.

Thus the positive result is not based on equality of raw parameter derivatives.

Bounded result:

`Stage 11B relational derivative covariance on the frozen positive family = established`.

## Explicit anchor and target typing

Stage 11B keeps the precursor roles explicit:

- prediction anchor: `orbit_event_06`;
- measurement target: `orbit_event_10`;
- typed anchor/target views: **8** across the four parameterizations.

The event ids and internal-clock readings are preserved while the raw external parameter values may differ.

## Raw-equal-parameter false comparison

Identity versus affine provides the frozen false-matching witness:

- equal numerical raw-parameter overlaps: **7**;
- overlaps that are actually different physical events: **6**;
- coincident overlap that is also the same event: **1**.

Therefore equal raw parameter value is not a sufficient event-identification rule. The executable classification is

`invalid_equal_raw_parameter_event_rule`.

This specifically establishes an insufficiency result, not a universal prohibition on numerical coordinate coincidences.

## Criteria 17–23

17. Relational observables `q(T=tau)` constructed at corresponding physical events — **satisfied**.
18. Relational observable values agree across the full frozen positive family — **satisfied**.
19. Relational derivatives agree across the positive family — **satisfied**.
20. Nonlinear maps demonstrably change raw parameter derivatives — **satisfied**.
21. Anchor/target physical-event typing remains explicit — **satisfied**.
22. Equal raw parameter labels are not used as event identity — **satisfied**.
23. Raw-parameter false comparison is classified as invalid — **satisfied**.

## Bounded Stage 11B checkpoint

`Stage 11B relational observable/derivative covariance on the frozen positive family = established`.

This is deliberately narrower than the eventual Stage 11 synthesis. In particular:

`relational observable covariance != full O/P/R/V covariance`.

`relational derivative covariance != future-measurement covariance`.

`relational covariance on one finite orbit != general covariance`.

`absence of preferred external parameterization != absence of ontological becoming`.

`parametrized covariance precursor != general relativity`.

`finite-model success != empirical discovery`.

Next checkpoint: **Stage 11C — typed O/P/R/V/Xi lift.**
