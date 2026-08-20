# Stage 5B Results — Per-Clock Reductions and Supports

Status: **completed**.

## Canonical support spaces

For each physical clock choice `X in {A,B,C}`:

`K_X = Im[R_X(j)]`

is seven-dimensional inside the nine-dimensional rest tensor product.

Thus:

`dim(K_A)=dim(K_B)=dim(K_C)=7 < 9`.

The support bases are orthonormal, have rank `7`, and are proper subspaces of their ambient rest spaces.

## Ideal physical clock probabilities

For a generic normalized complex physical state:

`p_X(j)=||P_X,j^kin |Psi>||^2=1/3`

for every `X in {A,B,C}` and every qutrit clock reading `j=0,1,2`.

The three probabilities for each clock sum to one.

## Reduction isometry

In orthonormal coordinates on `H_phys` and `K_X`, the physical reduction matrix is unitary for all three clocks and all three readings.

Maximum support-coordinate isometry residual:

`2.25e-16`.

Generic physical-state norms and inner products are preserved by every tested `R_X(j)`.

## Reduction / reconstruction round trips

The ambient rest-space composition is:

`R_X(j) E_X(j)=P_KX`.

Maximum residual:

`2.22e-16`.

Therefore the composition is the identity only on `K_X`; it is not the identity on the full nine-dimensional rest space.

On the global physical subspace:

`E_X(j) R_X(j)=I_phys`.

Maximum physical-basis round-trip residual:

`2.22e-16`.

This realizes:

`H_phys ~= K_X`

for each clock separately, while preserving the support-space guard.

## Same-clock transition structure

For each fixed physical clock:

`T_X(k<-j)=R_X(k)E_X(j)`.

The tested ambient operator agrees with:

`P_KX exp[-i H_rest^(X)(t_k^(X)-t_j^(X))] P_KX`.

Maximum residual across all clocks and reading pairs:

`3.14e-16`.

On support coordinates, the family satisfies:

`T_X(j<-j)=I_KX`,

`T_X(j<-k)T_X(k<-j)=I_KX`,

and:

`T_X(l<-k)T_X(k<-j)=T_X(l<-j)`.

Maximum composition residual:

`2.48e-16`.

Thus the Stage 4 same-clock perspective-consistency pattern is recovered independently for A, B, and C.

## Negative / boundary controls

The nonphysical state:

`|+1,+1,+1>`

can still be formally conditioned by a clock bra, but the physical reduction/probability APIs reject it because its constraint residual is `3`.

Vectors outside `K_X` are rejected by the reconstruction API.

Unnormalized physical states are rejected by the ideal clock-probability API.

Hence:

`formal conditioning != physical clock perspective`.

## Strongest supported Stage 5B result

**within the canonical symmetric three-qutrit constrained model, each of the three candidate physical clocks independently defines a seven-dimensional clock-relative support that is isometrically equivalent to the common seven-dimensional physical constrained space; ideal clock probabilities are uniform, explicit reconstruction is exact on the declared support, and same-clock transitions reproduce the expected rest-Hamiltonian evolution with identity/inverse/composition consistency.**

This is still an intra-clock result.

It does **not** yet show that changing the physical clock subsystem preserves the description or its operational content.

`per-clock reversibility != genuine cross-clock covariance`.

## Validation

Focused Stage 5B tests: **12**.

Code/test clean PR merge-ref checkpoint:

`279 passed in 4.82s`.
