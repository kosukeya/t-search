# Stage 11A Notes — Minimal Parametrized Constrained Carrier

Status: **Stage 11A implementation complete; criteria 11–16 are satisfied by the executable diagnostics. Stage 11B is the next scientific checkpoint.**

## Purpose

Stage 11A implements only the carrier frozen in Stage 11.0. It does not yet claim the full Stage 11 reparameterization-covariance result. The purpose is to make the external parameter visibly representational while keeping one nontrivial constrained relational orbit fixed.

The central separation remains:

`parameter label != physical event identity`.

`internal clock reading != external parameter label`.

## Minimal constrained seed

The implemented classical precursor uses

`C = p_T + p^2/2 = 0`

with canonical momentum seed `p=1.25` and therefore `p_T=-p^2/2`.

The identity-chart source labels sample 13 explicit events on `[-1.5,1.5]`. The positive nonconstant lapse-like seed is

`N(lambda)=1+lambda^2/4`

and the corresponding internal clock coordinate is

`T(lambda)=lambda+lambda^3/12`.

The physical configuration seed is

`q(T)=-0.35+1.25 T`.

Thus the carrier is nonstatic and the raw parameter rates can change without changing the physical relational orbit.

`classical parametrized precursor != fundamental classical ontology`.

## Frozen positive family implemented

The exact Stage 11.0 minimum family is present:

1. `f_id(lambda)=lambda`;
2. `f_aff(lambda)=2 lambda + 1`;
3. `f_cub(lambda)=lambda + lambda^3/4`;
4. `f_sinh(lambda)=sinh(lambda)`.

For each representation, the lapse is transformed by

`N'(lambda')=N(lambda)/f'(lambda)`.

All four implemented positive representations are explicitly marked admissible, orientation-preserving, and injective on the tested domain.

## Explicit physical-event correspondence

Every sampled point carries an event id `orbit_event_00` through `orbit_event_12`. Correspondence is constructed from these explicit event identities together with equal physical `T` and `q`, not by matching equal raw parameter values.

Across the three non-identity charts there are **36 corresponding event pairs with different raw parameter values**.

This is the first anti-triviality witness required by the protocol:

`same numerical parameter value != same physical event`.

## Chain-rule and orbit diagnostics

The canonical executable diagnostics report:

- event count: **13**;
- admissible positive parameterizations: **4**;
- minimum transformed positive lapse: **0.5**;
- maximum constraint residual: **0.0**;
- maximum lapse chain-rule residual: **0.0**;
- maximum `T`, `q`, `p`, and `p_T` orbit residual across the positive family: **0.0**;
- corresponding event pairs with different raw parameter labels: **36**;
- nonlinear-map sample points with different raw `dq/dlambda` rates: **24**.

The 24 raw-rate differences are recorded now as an anti-triviality witness but Stage 11B, not Stage 11A, is responsible for closing the relational-derivative criteria.

`raw parameter derivative equality != reparameterization covariance criterion`.

## Boundary controls

Two Stage 11.0 controls are implemented as explicit non-admissible specifications:

- `f_rev(lambda)=-lambda` — injective but orientation reversing;
- `f_noninj(lambda)=lambda^2` on a domain containing both signs — non-injective.

The canonical positive-trajectory constructor rejects both rather than silently treating them as gauge-equivalent positive reparameterizations.

`orientation-preserving reparameterization != time reversal`.

`non-injective relabeling != admissible reparameterization`.

## Criterion closure

11. Minimal constrained parametrized trajectory implemented with positive lapse-like rate — **satisfied**.
12. Frozen identity/affine/cubic/hyperbolic positive parameterizations implemented — **satisfied**.
13. Corresponding physical events carry different raw parameter values where expected — **satisfied**.
14. Chain-rule lapse transformation numerically verified — **satisfied**.
15. Constraint orbit / relational trajectory preserved across the positive family — **satisfied**.
16. Orientation-reversing and non-injective maps kept outside the positive admissible family — **satisfied**.

## What Stage 11A does not establish

Stage 11A does not yet establish:

- the Stage 11B relational observable/derivative criteria;
- O/P/R/V/Xi covariance;
- Stage 10 measurement covariance under reparameterization;
- clock-change × reparameterization commutation;
- general covariance;
- general relativity;
- any conclusion for blockness or ontological becoming.

Guards:

`same constraint orbit != established general covariance`.

`absence of preferred external parameterization != absence of ontological becoming`.

`finite typed parametrized covariance != general covariance`.

`finite-model success != empirical discovery`.
