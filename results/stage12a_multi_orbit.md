# Stage 12A Result — Multi-Orbit Constrained Carrier and Explicit Gauge-Flow Representatives

Status: **Stage 12A implementation closes criteria 11–16, subject to the repository regression on the current PR head.**

## Implemented finite family

Common constraint:

`C = p_T + p^2/2 = 0`.

Canonical physical-orbit data:

| orbit | Q_D | P_D |
| --- | ---: | ---: |
| `omega_alpha` | -0.35 | 1.25 |
| `omega_beta` | 0.40 | 1.25 |
| `omega_gamma` | -0.35 | 0.75 |
| `omega_delta` | 0.20 | 1.75 |

The family deliberately contains a same-`P_D`/different-`Q_D` pair and a same-`Q_D`/different-`P_D` pair. Their discrimination is exercised explicitly in Stage 12B/F; Stage 12A only establishes the carrier and prevents cross-orbit `Phi_s` construction.

## Gauge representative sample

Per physical orbit:

`s = (-1.0,-0.5,0.0,0.5,1.0)`.

Seed representative law:

`T=s`,

`q=Q_D+P_D T`,

`p=P_D`,

`p_T=-P_D^2/2`.

Counts asserted by the Stage 12A diagnostics/tests:

- physical orbits: **4**;
- representatives per orbit: **5**;
- representatives total: **20**;
- ordered non-identity same-orbit gauge transports: **80**.

Every licensed `Phi_s` checks the finite Hamiltonian-flow equations

`T' = T + Delta s`,

`q' = q + p Delta s`,

`p' = p`,

`p_T' = p_T`,

plus constraint residual and `Q_D,P_D` drift.

A transport between distinct `omega` values raises an explicit error and is not represented as a licensed positive gauge path.

## External parameterization carry-over

Every canonical physical orbit is represented in the four Stage 11 positive external parameterizations:

`identity`, `affine`, `cubic`, `hyperbolic`.

Counts:

- external parameterization views: **16**;
- Stage 11 parameterized event entries carried across those views: **208**.

Each view checks:

- positive lapse;
- the Stage 11 lapse/Jacobian chain rule;
- common constraint satisfaction;
- orbit-specific `Q_D,P_D` preservation.

The implementation keeps

`constraint_generated_gauge_flow`

and

`external_reparameterization`

as distinct transformation types.

## Typed provenance

Stage 12A explicitly records physical-orbit id, representative id, relational-event id/role, gauge chart, gauge parameter `s`, transformation type, external parameterization id, raw external labels, and provenance.

The seed chart uses `T=s` numerically, but this is not a type identification:

`clock coordinate T != gauge-flow parameter s by type`.

Likewise,

`constraint-generated gauge flow != external reparameterization by definition`.

## Criteria 11–16

11. Four canonical distinct physical orbits on a common constraint surface — **satisfied by implementation/test target**.
12. Multiple explicit gauge-flow representatives per orbit — **satisfied by implementation/test target**.
13. Constraint residual tolerance over all positive representatives — **satisfied by implementation/test target**.
14. `Q_D,P_D` invariance over all licensed positive gauge paths — **satisfied by implementation/test target**.
15. Stage 11 positive external parameterization family on every orbit — **satisfied by implementation/test target**.
16. Explicit typed orbit/gauge/event provenance — **satisfied by implementation/test target**.

Repository CI is the external code-regression check for the current head; it is not new scientific evidence.

## What Stage 12A does not establish

Stage 12A does not yet establish the full quotient partition, relational-observable descent, orbit-sensitive future-measurement behavior, or clock × reparameterization × gauge compatibility. Those remain Stage 12B–E tasks.

In particular:

`Dirac-invariant orbit data != timeless ontology by definition`.

`gauge quotient != elimination of physical change`.

`constraint-generated gauge flow != ontological becoming`.

`different physical orbit != later event on one orbit`.

`multi-orbit constrained carrier != general covariance`.

`finite gauge atlas precursor != diffeomorphism invariance`.

`single Hamiltonian constraint != hypersurface-deformation algebra`.

`constraint-generated gauge precursor != general relativity`.
