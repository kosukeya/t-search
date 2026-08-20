# Stage 4C — Conditional Dynamics

Status: **implementation/focused-test checkpoint complete; PR validation pending**.

Canonical model:

`d=4`, with normalized zero-constraint states

`|Psi_c>=sum_n c_n |n>_C|n>_S`.

For the ideal DFT clock basis:

`|tilde_psi_j>=(<t_j| tensor I)|Psi_c>`

and:

`p_j=||tilde_psi_j||^2=1/4`

for every normalized physical coefficient vector in the canonical matched-energy family.

The normalized physical reduction is:

`R_j=sqrt(d)(<t_j| tensor I)`

restricted to the zero-constraint physical subspace. It gives:

`R_j|Psi_c>=sum_n c_n exp(-i n t_j)|n>_S`.

For a generic normalized complex coefficient vector, direct numerical cross-checks give all four clock probabilities equal to `0.25` up to floating-point precision.

The reduced states satisfy:

`R_j|Psi>=exp[-i H_S(t_j-t_0)]R_0|Psi>`

with reference residuals zero at machine precision for the canonical diagonal Hamiltonian implementation.

The one-step relation:

`psi_{j+1}=exp(-i H_S Delta)psi_j`

also holds through the periodic wrap-around. The largest independent canonical wrap residual is about `4.31e-16`, and the full-period system-unitary residual is about `9.16e-16`, both far below the frozen `1e-10` tolerance.

For the equal-amplitude baseline, `|<psi_0|psi_1>|` is about `7.2e-17`, so the first relative step is not merely a global-phase change.

The same conditional-dynamics identities are tested at `d=5` for generic complex coefficients.

`tests/test_stage4c_conditional_dynamics.py` contains 12 focused tests.

A nonphysical kinematic state can be formally clock-conditioned, but the Stage 4C `physical_reduction` API rejects it. Therefore:

`formal clock conditioning != physical Page-Wootters reduction`.

Strongest allowed Stage 4C statement:

**within the ideal finite constrained Page--Wootters-style model, stationary global physical states encode normalized clock-relative system states that obey exact discrete unitary Schrödinger dynamics.**

This does not establish fundamental emergent time, ontological becoming, a temporal arrow, or phenomenal passage.

Next: Stage 4D — reduction-map reversibility.