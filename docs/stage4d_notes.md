# Stage 4D — Reduction-Map Reversibility Notes

Status: **completed**.

## Scope

Stage 4D tests whether the normalized Page--Wootters reduction is genuinely reversible on the frozen zero-constraint physical subspace, while the corresponding clock projection remains many-to-one on the full kinematic Hilbert space.

This checkpoint deliberately does not yet construct local-to-local transition maps `T_{k<-j}`. Those remain Stage 4E.

## Two maps with the same clock bra

The full kinematic projection is:

`P_j^kin=(<t_j|_C tensor I_S): H_kin -> H_S`.

For canonical `d=4`:

- `dim(H_kin)=16`;
- `P_j^kin` has matrix shape `4 x 16`;
- `rank(P_j^kin)=4`;
- `dim ker(P_j^kin)=12`.

Hence the full kinematic projection is necessarily non-injective.

The normalized physical reduction is:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

Using the orthonormal matched-energy physical basis, `R_j` is represented by:

`diag(exp(-i n t_j))`.

Therefore the Stage 4D tests require both:

`R_j^dagger R_j=I`

and:

`R_j R_j^dagger=I`.

## Explicit reconstruction

The inverse candidate is:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`.

Stage 4D tests:

`R_j E_j=I_S`

and, for every physical state:

`E_j R_j|Psi_phys>=|Psi_phys>`.

The implementation checks these both as operator identities in the chosen orthonormal coordinates and as vector round trips for generic complex states.

## Inner-product preservation

For physical states `|Psi>` and `|Phi>`, the checkpoint tests:

`<Psi|Phi>=<R_j Psi|R_j Phi>`.

Norm preservation is also tested for unnormalized physical vectors, so the result is not an artifact of unit normalization.

## Explicit kinematic non-injectivity control

At clock reading `j=0`, the nonzero vector:

`(|0>_C|2>_S-|1>_C|2>_S)/sqrt(2)`

lies in `ker(P_0^kin)` because the two clock amplitudes cancel.

Therefore a base kinematic vector and that same vector plus the kernel element are distinct global vectors with identical clock projections.

This gives an explicit constructive witness of many-to-one kinematic projection, rather than relying only on rank counting.

## Full-space lift is not an inverse

The composed full-space operator:

`E_j sqrt(d) P_j^kin`

has rank `d`, not `d^2`, and is not the identity on `H_kin`.

However it acts as identity on the matched-energy physical basis. Thus:

`physical reversibility != global kinematic reversibility`.

The reconstruction map only inverts the normalized reduction after restriction to the declared physical subspace.

## Robustness

The same rank/nullity, isometry, and physical round-trip structure is checked at `d=5`.

## Interpretation

Stage 4D establishes, within the ideal finite matched-energy model:

**a single clock-relative system vector retains all information required to reconstruct the corresponding constrained global physical vector, even though the formally similar clock projection is lossy on the unrestricted kinematic space.**

This is a representation-theoretic result about the declared constrained model. It does not establish:

- a physical God's-eye observer;
- that arbitrary quantum projections are reversible;
- that information loss never occurs physically;
- ontological becoming;
- a temporal arrow;
- fundamental emergent time.

Next: Stage 4E tests the relational transition family `T_{k<-j}=R_k E_j` and its composition laws.
