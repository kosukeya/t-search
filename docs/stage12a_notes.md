# Stage 12A Notes — Multi-Orbit Constrained Carrier and Explicit Gauge-Flow Representatives

Status: **implementation complete; criteria 11–16 are intended to close after repository CI validates the new executable/test family.**

## Question

Stage 12A asks only whether the Stage 12.0 frozen carrier can be implemented as a finite family containing multiple physically distinct constraint orbits, multiple explicit representatives on each orbit, and the inherited Stage 11 positive external parameterization family.

It does **not** yet perform the full Stage 12B physical-orbit discrimination analysis, the Stage 12C quotient/groupoid descent, or the Stage 12D measurement lift.

## Implemented constrained carrier

The common constraint remains

`C = p_T + p^2/2 = 0`.

The four protocol-frozen physical orbits are implemented exactly as

- `omega_alpha: (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta: (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma: (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta: (Q_D,P_D)=(0.20,1.75)`.

All four therefore obey the same constraint law while carrying distinct frozen Dirac-data pairs.

## Explicit gauge representatives

For each physical orbit, Stage 12A samples

`s in {-1.0,-0.5,0.0,0.5,1.0}`.

In the seed chart,

`T=s`,

`q=Q_D+P_D T`,

`p=P_D`,

`p_T=-P_D^2/2`.

The numerical equality `T=s` is only a convenient chart choice. The implementation stores the clock coordinate `T` and the gauge-flow parameter `s` as separately typed fields.

This produces **5 representatives per orbit / 20 representatives total**.

For every ordered pair of distinct representatives within one orbit, the implementation constructs a typed constraint-generated gauge transport `Phi_s`. With five representatives this gives `5*4=20` non-identity ordered transports per orbit and **80 transports total**.

The transport checks

`T' = T + Delta s`,

`q' = q + p Delta s`,

`p' = p`,

`p_T' = p_T`,

and monitors both constraint residual and `Q_D,P_D` drift.

Cross-orbit `Phi_s` construction is rejected rather than silently coerced into a gauge relation.

## External reparameterization remains separately typed

Stage 12A reuses the Stage 11 positive family on every canonical physical orbit:

- identity;
- affine;
- cubic;
- hyperbolic/sinh.

The implementation wraps each Stage 11 trajectory with explicit Stage 12 physical-orbit provenance and the transformation type

`external_reparameterization`.

Constraint-generated transports instead carry the type

`constraint_generated_gauge_flow`.

Thus

`constraint-generated gauge flow != external reparameterization by definition`.

There are **16 external parameterization views** (`4 orbits * 4 parameterizations`) and **208 parameterized event entries** (`16 * 13 Stage 11 events`).

The inherited Stage 11 lapse/Jacobian law is checked on every view.

## Typed provenance

Every representative explicitly stores

- physical orbit id;
- representative id;
- relational-event id;
- event role;
- gauge chart id;
- gauge-flow type;
- gauge-flow parameter `s`;
- phase-space values;
- constraint value;
- reconstructed `Q_D,P_D`;
- provenance string.

Every external view separately stores physical orbit id, external parameterization id, source-label type, transformed-label type, and external-reparameterization provenance.

This is intentionally more verbose than a numerically minimal implementation because Stage 12 is testing whether typed identification survives quotienting and transport.

## Stage boundary

Stage 12A establishes the carrier needed for later tests. It does not yet establish that the quotient classes recover exactly the four intended physical orbits; that is reserved for Stage 12B/C.

In particular:

`same P_D alone != same physical orbit`,

`same Q_D alone != same physical orbit`,

but the explicit false-positive discrimination tests are Stage 12B/F work rather than Stage 12A evidence.

## Interpretation guards

- `constraint-generated gauge flow != ontological becoming`;
- `different physical orbit != later event on one orbit`;
- `Dirac-invariant orbit data != absence of relational change`;
- `multi-orbit constrained carrier != general covariance`;
- `finite constraint-generated gauge atlas precursor != diffeomorphism invariance`;
- `single Hamiltonian constraint != hypersurface-deformation algebra`;
- `constraint-generated gauge precursor != general relativity`.
