# Stage 5B Notes — Per-Clock Reductions and Supports

## Scope

Stage 5B adds one reduced perspective at a time to the Stage 5A three-qutrit constrained substrate.

It implements:

- `K_A`, `K_B`, `K_C` as constraint-compatible support subspaces inside the corresponding nine-dimensional rest tensor products;
- formal kinematic clock conditioning `P_X,j^kin`;
- normalized physical reductions `R_X(j)` restricted to `H_phys`;
- ideal clock probabilities `p_X(j)`;
- reconstruction maps `E_X(j)`;
- same-clock transition maps `T_X(k<-j)=R_X(k)E_X(j)`;
- the expected rest-Hamiltonian evolution on each support.

It does **not** yet implement a genuine physical clock change between distinct clock subsystems. That begins in Stage 5C.

## Canonical support dimensions

For each `X in {A,B,C}`:

`dim(H_rest^(X))=9`

but:

`dim(K_X)=7`.

Thus the reduced physical perspective is a proper support subspace of the ambient two-qutrit rest tensor product.

## Physical reduction

For a normalized physical state and a clock reading `j`:

`R_X(j)=sqrt(3) P_X,j^kin restricted to H_phys`.

In orthonormal physical/support coordinates, `R_X(j)` is a `7 x 7` unitary phase matrix.

For a generic normalized complex physical state:

`p_X(j)=1/3`

for every clock choice and every canonical reading.

## Reconstruction

`E_X(j): K_X -> H_phys`

is implemented as the inverse of the support-coordinate reduction matrix, embedded back into the global physical basis.

The ambient rest-space identities are deliberately written as:

`R_X(j) E_X(j)=P_KX`

rather than `I_9`.

On `K_X`, this is the identity. On the global physical subspace:

`E_X(j) R_X(j)=I_phys`.

This preserves the Stage 5.0 guard:

`support-subspace isometry != full-rest-space unitarity`.

## Same-clock dynamics

For one fixed clock:

`T_X(k<-j)=R_X(k)E_X(j)`.

On the support:

`T_X(k<-j)=exp[-i H_rest^(X)(t_k^(X)-t_j^(X))]`.

The implementation compares the ambient partial-isometry form against:

`P_KX exp[-i H_rest^(X) Delta t] P_KX`.

The support-coordinate family satisfies identity, inverse, and composition.

## Formal conditioning versus physical reduction

Formal conditioning remains defined for arbitrary kinematic states.

A nonphysical state such as `|+1,+1,+1>` can therefore be formally conditioned, but `physical_clock_reduction` and `physical_clock_probability` reject it because it fails the Stage 5 constraint.

Thus:

`being conditionable on X != being a physical X-clock perspective`.

## Numerical diagnostics

For the canonical symmetric qutrit baseline, across all three clocks and all canonical readings:

- maximum support-coordinate isometry residual: approximately `2.25e-16`;
- maximum `R_X E_X - P_KX` residual: approximately `2.22e-16`;
- maximum physical round-trip residual: approximately `2.22e-16`;
- maximum same-clock expected-transition residual: approximately `3.14e-16`;
- maximum same-clock composition residual: approximately `2.48e-16`.

All are far below the frozen `1e-10` tolerance.

## Interpretation guard

Stage 5B establishes that each physical clock choice individually supports a reversible clock-relative description on its own declared support.

It does **not** yet establish that two different clock perspectives are mutually consistent.

`three individually valid reduced perspectives != genuine cross-clock perspective consistency`.
