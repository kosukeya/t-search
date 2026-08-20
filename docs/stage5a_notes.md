# Stage 5A Notes — Symmetric Three-Subsystem Constrained Model

Status: **completed at the focused implementation checkpoint**.

Stage 5A implements only the substrate frozen in `docs/stage5_protocol.md`. It does **not** yet implement per-clock reductions `R_X`, support spaces `K_X`, reconstructions `E_X`, or genuine clock-change maps `S_{Y<-X}`.

## Canonical substrate

Three qutrit subsystems are used:

`A`, `B`, `C`.

Each has centered energy labels:

`m in {-1,0,+1}`

and canonical rate:

`lambda_A=lambda_B=lambda_C=1`.

Thus:

`H_X=diag(-1,0,+1)`.

The kinematic dimension is:

`3^3=27`.

## Total constraint

Stage 5A constructs:

`H_tot=H_A tensor I tensor I + I tensor H_B tensor I + I tensor I tensor H_C`.

On a product energy state `|a,b,c>` the constraint eigenvalue is:

`a+b+c`.

The exact zero-sum triples are:

- `(-1,0,+1)`
- `(-1,+1,0)`
- `(0,-1,+1)`
- `(0,0,0)`
- `(0,+1,-1)`
- `(+1,-1,0)`
- `(+1,0,-1)`.

Therefore:

`dim(H_phys)=7`.

## Independent kernel verification

The analytic seven-column product basis is built from the zero-sum triples.

Independently, `numpy.linalg.eigh(H_tot)` identifies the numerical zero eigenspace. Stage 5A compares the two projectors rather than comparing arbitrary eigenvector coordinates.

For the canonical model the projector residual is exactly zero at numerical precision.

This guards against defining the desired physical subspace and then only testing that definition against itself.

## Generic physical state check

A generic complex seven-component coefficient vector is embedded into the analytic physical basis and normalized. Its recovered physical coordinates agree with the normalized input coefficients, and its constraint residual vanishes within the declared tolerance.

An explicit negative control `|+1,+1,+1>` has total constraint eigenvalue `+3`, so its constraint residual is `3`.

## Per-subsystem finite clocks

Each subsystem gets the same finite clock construction in the symmetric baseline:

`Delta=2*pi/3`

and:

`|t_j>=(1/sqrt(3)) sum_{m=-1}^{+1} exp[-i m t_j] |m>`.

The three clock bases are mathematically identical in this symmetric fixture, but they belong to distinct subsystem Hilbert spaces. Their identical coordinate matrices must not be interpreted as one shared physical clock.

The positive Hamiltonian translates the declared reading states forward:

`exp(-i H_X Delta)|t_j>=|t_{j+1 mod 3}>`.

Three steps return the identity.

## Scope guard

Stage 5A establishes only:

- three subsystem Hilbert spaces;
- their centered Hamiltonians;
- the total zero-sum constraint;
- the seven-dimensional physical kernel;
- one ideal periodic DFT clock basis per subsystem.

It does **not** yet establish:

- that any subsystem is an operationally good clock after reduction;
- that `H_phys` is isomorphic to a reduced support `K_X`;
- any genuine physical clock-change map;
- cross-clock composition consistency;
- operational covariance across clock choices.

Those are Stage 5B--5E questions.

## Validation

Focused Stage 5A tests: **12**.

Code/test PR merge-ref checkpoint:

`267 passed in 4.58s`.

The project-wide Node.js action-runtime deprecation warning remains non-blocking and unrelated to the pytest result.
