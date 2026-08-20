# Stage 5C Notes — Genuine Clock-Change Maps

## Scope

Stage 5C introduces the first direct transformations between **distinct physical clock choices** in the Stage 5 constrained three-qutrit model.

For distinct clocks `X` and `Y`:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

This stage verifies:

- direct-global route consistency;
- support-coordinate unitarity / isometry;
- ambient partial-isometry identities;
- two-way clock-change round trips;
- preservation of norms and inner products;
- explicit rest-factor semantic relabeling through the common physical triple;
- the guard that equal numeric readings do not make a genuine clock change an ambient identity.

Three-clock composition is intentionally deferred to Stage 5D.

## Distinct reduced tensor-factor meanings

The ambient rest-vector length is `9` for every clock perspective, but the factor meanings differ:

- `K_A subset H_B tensor H_C`;
- `K_B subset H_A tensor H_C`;
- `K_C subset H_A tensor H_B`.

Therefore the clock-change map is not introduced by silently identifying these ambient vector spaces.  It is constructed only through the common constrained physical space:

`K_X --E_X(j)--> H_phys --R_Y(k)--> K_Y`.

This preserves the methodological rule:

`same ambient dimension != same physical factorization`.

## Support-coordinate map

Using orthonormal bases of `K_X` and `K_Y`, Stage 5C represents the clock-change map by a `7 x 7` matrix.

For every ordered distinct clock pair and all canonical source/target readings:

`S^dagger S=I_KX`

and:

`S S^dagger=I_KY`.

Thus the genuine clock change is unitary/isometric **between the declared physical support spaces**.

## Ambient partial isometry

As a `9 x 9` matrix between the ambient rest-coordinate representations:

`S^dagger S=P_KX`

and:

`S S^dagger=P_KY`.

It is therefore a partial isometry on the ambient spaces, not an unrestricted `9 x 9` unitary.

This is the cross-clock analogue of the Stage 5B support-space guard.

## Direct-global route consistency

For a physical global state:

`|psi_X(j)>=R_X(j)|Psi>`.

Stage 5C verifies:

`S_{Y<-X}(k,j)|psi_X(j)>=R_Y(k)|Psi>`

for all six ordered distinct clock pairs and all nine source/target reading pairs in the canonical qutrit model.

The equality is also checked on every analytic physical basis vector, not only one generic superposition.

Thus the path:

`H_phys -> K_X -> K_Y`

agrees with the direct path:

`H_phys -> K_Y`.

## Two-way clock-change round trip

For each distinct clock pair:

`S_{X<-Y}(j,k) S_{Y<-X}(k,j)=P_KX`

in ambient rest coordinates.

Restricted to source support coordinates:

`S_{X<-Y}(j,k) S_{Y<-X}(k,j)=I_KX`.

The same holds with source/target exchanged.

This establishes pairwise reversibility in the canonical ideal model.

It does not yet establish the three-clock composition law reserved for Stage 5D.

## Explicit factor-semantics example

Consider the physical energy triple:

`(-1,0,+1)`.

With `C` as clock, the reduced rest labels are:

`(A,B)=(-1,0)`.

With `A` as clock, the reduced rest labels are:

`(B,C)=(0,+1)`.

At source/target reading `0`, the genuine clock-change map sends the corresponding `C`-perspective basis state to the corresponding `A`-perspective basis state.

This makes explicit that clock change reorganizes which tensor factors constitute the reduced description.

## Equal numeric readings are not an identity transformation

For the canonical map:

`S_{A<-C}(0,0)`

we obtain:

`||S_{A<-C}(0,0)-I_9|| ~= 3.742`.

Therefore:

`source reading 0 and target reading 0 != no perspective change`.

This supports the frozen guard:

`equal numerical clock readings != same physical event`.

## Numerical diagnostics

Across all six ordered distinct clock pairs and all nine reading pairs per ordered pair:

- maximum support-coordinate unitarity residual: approximately `4.98e-16`;
- maximum `S^dagger S-P_source` residual: approximately `4.44e-16`;
- maximum `S S^dagger-P_target` residual: approximately `4.44e-16`;
- maximum direct-global route residual: approximately `1.30e-16`;
- maximum ambient two-way round-trip residual: approximately `4.44e-16`;
- maximum support-coordinate round-trip residual: approximately `4.98e-16`.

All are far below the frozen `1e-10` tolerance.

## Interpretation guard

Stage 5C establishes **pairwise reversible genuine clock changes** in the canonical symmetric three-qutrit construction.

It does not yet establish:

- three-clock composition / cross-clock perspective consistency;
- operational covariance of transformed observables;
- robustness beyond the symmetric qutrit baseline;
- quantum general covariance;
- a fundamental ontology of relational time.

The key boundary is:

`pairwise reversible clock changes != full cross-clock perspective consistency`.
