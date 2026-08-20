# Stage 4A — Finite Clock Kinematics Notes

Status: **implementation and focused tests added; Stage 4B is next after checkpoint validation**.

## Scope

Stage 4A implements only the finite quantum clock/system kinematics fixed by `docs/stage4_protocol.md`.

It deliberately does **not** implement `H_tot`, the Page--Wootters physical constraint, conditional states, reduction maps, or any claim of emergent time.

## Implemented objects

Canonical dimension:

`d_C=d_S=d=4`.

Energy Hamiltonians:

`H_S=diag(0,1,2,3)`

`H_C=diag(0,-1,-2,-3)`.

Clock spacing:

`Delta=2*pi/d`.

DFT clock readings:

`|t_j>=(1/sqrt(d)) sum_n exp(i n t_j)|n>`

with `t_j=2*pi*j/d` plus an optional origin shift.

The kinematic tensor-space dimension is recorded as `d_C*d_S=16` without yet constructing a total constraint operator.

## Stage 4A identification tests

The focused tests require:

- canonical energy bases and Hermitian Hamiltonians;
- exact declared clock readings for `d=4`;
- DFT clock-basis orthonormality;
- normalization of every clock state;
- one-step translation `exp(-i H_C Delta)|t_j>=|t_{j+1 mod d}>`;
- multi-step and negative-step modular translation;
- full-period identity after `d` steps;
- origin-shift covariance of the kinematic clock orbit;
- the same construction at `d=5` as a noncanonical robustness check;
- unitary exponentiation of a generic Hermitian test matrix;
- rejection of invalid dimensions, indices, state shapes, and non-Hermitian generators.

## Numerical checkpoint

Independent direct evaluation of the implemented formulas gives, for canonical `d=4`:

- DFT Gram maximum residual: about `1.17e-16`;
- one-step translation maximum residual: about `3.67e-16`;
- full-period identity maximum residual: about `7.35e-16`.

For `d=5`, the corresponding residuals are also below `1e-15`.

These are far below the frozen Stage 4 tolerance `1e-10`.

## Interpretation guards

No Page--Wootters physical state has been constructed at Stage 4A.

Therefore Stage 4A establishes only an internally consistent **finite periodic quantum clock kinematics**.

It does not establish:

- a Hamiltonian constraint;
- global stationarity;
- conditional Schrödinger dynamics;
- a physical/global-to-local reduction;
- an arrow of time;
- ontological becoming;
- fundamental periodicity of physical time;
- emergent time.

The next checkpoint, Stage 4B, introduces `H_tot` and tests the constrained physical subspace.