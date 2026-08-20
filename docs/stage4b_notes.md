# Stage 4B — Constrained Global Physical State Notes

Status: **implementation and focused tests added; Stage 4C is next after checkpoint validation**.

## Scope

Stage 4B adds the noninteracting finite Page--Wootters-style constraint structure on top of the Stage 4A clock kinematics.

It still does **not** implement clock conditioning, normalized reduction maps `R_j`, conditional Schrödinger dynamics, or any claim that time has emerged.

## Total constraint

For canonical `d=4`:

`H_tot = H_C tensor I_S + I_C tensor H_S`.

With:

`H_C=diag(0,-1,-2,-3)`

and:

`H_S=diag(0,1,2,3)`,

the computational tensor-basis eigenvalue for `|c>_C|s>_S` is `s-c`.

Therefore the zero-eigenvalue sector is exactly the matched-energy sector `c=s`.

## Analytic and numerical physical subspaces

The analytic physical basis is:

`B_phys=[|0,0>,|1,1>,|2,2>,|3,3>]`.

The implementation separately diagonalizes `H_tot` with `numpy.linalg.eigh`, extracts the zero-eigenvalue numerical kernel, and compares the resulting projector with the analytic matched-energy projector.

For canonical `d=4`, both projectors agree at machine precision.

This avoids merely assuming the expected kernel structure in the test.

## Physical-state family

A general matched-energy state is:

`|Psi_c> = sum_n c_n |n>_C|n>_S`.

The implementation supports both exact supplied coefficients and optional normalization.

The equal-amplitude baseline is:

`|Psi_eq>=(1/2) sum_n |n>_C|n>_S`.

A generic normalized complex coefficient vector is also tested so that zero constraint residual is not an artifact of equal amplitudes.

## Constraint residual and stationarity

Physicality is diagnosed by:

`r_C(Psi)=||H_tot|Psi>||_2`.

For canonical physical states the residual is numerically zero.

Global stationarity with respect to the constraint generator is diagnosed by:

`r_stat(Psi,tau)=||exp(-i H_tot tau)|Psi>-|Psi>||_2`.

Multiple positive and negative external parameters are tested.

This is called **constraint-generator stationarity** only. It must not be paraphrased as "nothing happens physically".

## Negative control

The explicit off-diagonal energy product state:

`|0>_C|1>_S`

is outside the kernel.

For the canonical spectra:

`||H_tot |0,1>||=1`.

At `tau=0.37`, it also changes under `exp(-i H_tot tau)`, with stationarity residual about `0.368`.

Thus the constraint distinguishes matched-energy physical states from a simple nonphysical kinematic state.

## Dimension robustness

The same matched-energy kernel structure is tested at `d=5`:

- `dim(H_kin)=25`;
- `dim ker(H_tot)=5`;
- numerical and analytic physical-subspace projectors agree within the frozen tolerance.

## Interpretation guards

Stage 4B establishes a finite constrained global state space and constraint-generator stationarity.

It does not establish:

- conditional clock-relative dynamics;
- reduction-map reversibility;
- an arrow of time;
- ontological becoming;
- phenomenal passage;
- fundamental emergent time.

The next checkpoint, Stage 4C, introduces ideal clock conditioning and asks whether normalized conditional states obey exact discrete Schrödinger dynamics.
