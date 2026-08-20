# Stage 5G Results — Robustness

Status: **completed; final Stage 5 robustness and pre-finalization documentation checkpoint passed.**

## Joint robustness suite

Stage 5G evaluates the following identities together for each declared control family:

- physical constraint;
- ideal `1/d` clock probabilities;
- per-clock reduction/reconstruction isometry;
- same-clock rest-Hamiltonian dynamics;
- genuine cross-clock support unitarity;
- direct-global route consistency;
- three-clock composition consistency;
- transformed rank-one Born covariance.

All tested residuals are required to remain below the frozen `1e-10` tolerance.

## Canonical coefficient families

For the symmetric qutrit baseline:

`d=3`, `rates=(1,1,1)`, `dim(H_phys)=7`, `dim(K_X)=7`,

the joint suite passes for:

- generic complex full-support coefficients;
- alternating complex full-support coefficients;
- sparse coherent two-sector coefficients.

Thus the Stage 5 identities are not confined to one equal-amplitude or specially tuned physical state.

## Symmetric d=5 control

For:

`d=5`, `rates=(1,1,1)`,

the independently generated zero-sum physical sector has dimension:

`19`.

All three clock-relative supports also have dimension:

`19`

inside `25`-dimensional rest tensor-product spaces.

The full joint Stage 5 suite passes for both generic and sparse physical coefficient families.

Therefore the canonical clock-change/composition/operational structure is not restricted to the qutrit `7`-dimensional physical/support sector.

## Asymmetric clock-rate control

For:

`d=3`, `rates=(1,1,2)`,

the physical constraint is:

`a+b+2c=0`.

The physical sector has dimension:

`5`,

and each clock-relative support has dimension:

`5`.

The discrete clock-coordinate spacings are:

- `Delta_A=2*pi/3`;
- `Delta_B=2*pi/3`;
- `Delta_C=pi/3`.

The same joint constraint/reduction/same-clock/cross-clock/composition/Born suite passes for generic and alternating coefficient families.

This is the strongest Stage 5G control against explaining the result purely by permutation symmetry among three identical qutrit Hamiltonians.

It does not model realistic clock-rate dynamics or gravitational time dilation.

## Global phase control

For canonical qutrit, symmetric `d=5`, and asymmetric-rate qutrit configurations, multiplying a physical state by `exp(i*0.731)` leaves tested reduced density matrices and ideal clock probabilities unchanged within tolerance.

Thus:

`ket representative change != change of tested ray-level/operational content`.

## Subsystem permutation covariance

For all six subsystem permutations in the symmetric qutrit baseline, explicit tensor-product permutation operators satisfy:

`U_pi H_tot U_pi^dagger=H_tot`,

`U_pi P_phys U_pi^dagger=P_phys`.

Per-clock reductions obey the corresponding global-to-rest permutation diagram, and genuine cross-clock maps obey the induced source/target rest-space permutation diagram.

This verifies bookkeeping/subsystem permutation covariance at the operator level rather than only by renaming function arguments.

Negative guard:

holding the asymmetric tuple `(1,1,2)` fixed while swapping A and C does **not** leave `H_tot` invariant.

Therefore:

`symmetric permutation covariance != unrestricted physical permutation symmetry`.

## Strongest supported Stage 5G robustness result

**within the declared finite noninteracting constrained family, the Stage 5 perspective-consistency structure survives multiple generic/sparse physical coefficient choices, a higher symmetric odd dimension with a nineteen-dimensional physical/support sector, and an asymmetric qutrit clock-rate model with a five-dimensional physical/support sector; in the symmetric baseline it is also covariant under explicit subsystem tensor permutations, while controls show that this permutation symmetry disappears when unequal rates are held fixed.**

This strengthens the claim that the canonical Stage 5 result is not merely an artifact of one seven-dimensional symmetric qutrit example.

It still does not establish equivalence of arbitrary clocks, interacting-clock covariance, or quantum/gravitational general covariance.

## Validation

Focused Stage 5G tests: **12**.

Code/test clean PR merge-ref checkpoint:

`339 passed in 14.91s`.

Documentation/synthesis/README/roadmap-inclusive clean PR merge-ref checkpoint before the final status-only commits:

`339 passed in 9.89s`.

## Merge-readiness review checkpoint

At the documentation-inclusive review point:

- branch status versus `main`: `67 commits ahead / 0 behind`;
- changed files: `40`;
- changed-file scope: Stage 5 code/tests/experiments/docs/results plus the expected README/roadmap synchronization only;
- PR state: open, Draft, unmerged, `mergeable=true`;
- unresolved review threads: `0`;
- submitted reviews: `0`;
- PR conversation comments: `0`.

A final regression is run after the status-only result/synthesis commits so the reported merge-ready state refers to the actual final head.
