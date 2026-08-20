# Stage 5A Results — Symmetric Three-Subsystem Constrained Model

Status: **completed**.

## Canonical dimensions

- subsystem dimensions: `d_A=d_B=d_C=3`
- kinematic dimension: `27`
- physical zero-constraint dimension: `7`

## Canonical Hamiltonians

For each subsystem:

`H_X=diag(-1,0,+1)`.

The total constraint is:

`H_tot=H_A+H_B+H_C`.

On `|a,b,c>` its eigenvalue is:

`a+b+c`.

## Physical basis

The exact allowed triples are:

`(-1,0,+1)`

`(-1,+1,0)`

`(0,-1,+1)`

`(0,0,0)`

`(0,+1,-1)`

`(+1,-1,0)`

`(+1,0,-1)`.

Thus:

`dim(H_phys)=7`.

The analytic physical basis is orthonormal and is annihilated by `H_tot`.

## Analytic versus numerical zero eigenspace

The numerical kernel is obtained independently with `numpy.linalg.eigh(H_tot)`.

For the canonical model:

`||P_kernel^num-P_phys^analytic|| = 0`.

Hence the numerical zero eigenspace and the declared analytic zero-sum physical subspace coincide at machine precision.

## Generic physical-state control

A generic complex seven-component coefficient vector is embedded and normalized. The recovered physical coefficients match the normalized inputs and:

`||H_tot |Psi_phys>|| = 0`

within the frozen numerical tolerance.

Negative control:

`|+1,+1,+1>`

has:

`||H_tot |+1,+1,+1>|| = 3`.

Therefore the zero-constraint classification is not being applied indiscriminately to the full kinematic space.

## Three ideal finite clocks

Each subsystem receives its own ideal qutrit clock-reading basis:

`Delta_X=2*pi/3`

and:

`|t_j>_X=(1/sqrt(3)) sum_m exp[-i m t_j] |m>_X`.

Numerical diagnostics for the symmetric canonical model:

- maximum clock Gram residual across A/B/C: approximately `7.03e-16`
- maximum one-step translation residual: approximately `6.47e-16`
- three-step full-cycle identity residual: approximately `3.46e-16`.

All are far below the frozen `1e-10` tolerance.

The three clock coordinate matrices are identical because the baseline Hamiltonians/rates are symmetric. This does not identify the three physical clock subsystems with one another.

## Strongest supported Stage 5A result

**the declared symmetric three-qutrit toy model has an explicitly verified seven-dimensional zero-sum constrained physical subspace inside a 27-dimensional kinematic space, and each of the three distinct subsystems supports the same internally consistent finite periodic DFT clock kinematics.**

This establishes the substrate required for later clock-relative reductions.

It does **not** yet show that a genuine change of physical clock preserves any transition or operational structure.

In particular:

`three available clock kinematics != cross-clock perspective consistency`.

## Validation

Focused Stage 5A tests: **12**.

Code/test PR merge-ref checkpoint:

`267 passed in 4.58s`.
