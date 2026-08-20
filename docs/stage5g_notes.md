# Stage 5G Notes — Robustness and Synthesis

Status: **robustness code/test checkpoint passed; Stage 5 synthesis and final merge-readiness review in progress.**

## Purpose

Stage 5G does not introduce a new clock-change mechanism. It stress-tests the structures established in Stages 5A--5F and then synthesizes Stage 5.

The principal question is whether the canonical Stage 5 result is merely an artifact of three identical qutrits with seven-dimensional physical/support spaces.

The joint robustness suite checks together:

- total-constraint satisfaction;
- ideal clock-reading probabilities;
- per-clock reduction isometry;
- physical/support round trips;
- same-clock rest-Hamiltonian dynamics;
- genuine cross-clock support unitarity;
- direct-global route consistency;
- three-clock composition consistency;
- transformed rank-one Born covariance.

All numerical claims use the frozen `1e-10` tolerance.

## Coefficient robustness

The canonical symmetric qutrit family is re-run with three deterministic normalized physical coefficient families:

- generic complex full-support coefficients;
- alternating complex full-support coefficients;
- sparse coherent two-sector coefficients.

This guards against interpreting one equal-amplitude or specially tuned superposition as the source of the Stage 5 identities.

## Symmetric higher-dimension control

The odd-dimensional family is tested at:

`d=5`.

The centered energy labels are:

`{-2,-1,0,+1,+2}`.

For three symmetric subsystems, the zero-sum physical dimension is:

`D_phys=19`.

Each clock-relative support also has dimension `19` inside a `25`-dimensional rest tensor-product space.

The same joint constraint/reduction/clock-change/composition/Born suite is required to pass for both generic and sparse physical coefficient families.

This tests whether the Stage 5 structure is tied specifically to the canonical `7`-dimensional qutrit physical sector.

## Asymmetric clock-rate control

The protocol-reserved qutrit control is:

`(lambda_A,lambda_B,lambda_C)=(1,1,2)`.

The constraint becomes:

`a+b+2c=0`.

The allowed physical sector has dimension:

`5`.

Each clock-relative support also has dimension `5`.

Clock-coordinate steps are:

`Delta_A=Delta_B=2*pi/3`,

`Delta_C=pi/3`.

The same joint Stage 5 identities are tested with generic and alternating physical coefficient families.

This is an important control because it breaks the equality of the three subsystem Hamiltonians and therefore excludes the explanation that all Stage 5 results arise only from permuting three identical clocks.

It is still not a realistic time-dilation or interacting-clock model.

## Global phase

For canonical `d=3`, symmetric `d=5`, and asymmetric-rate qutrit controls, multiply one generic physical state by:

`exp(i*0.731)`.

The reduced ket representatives acquire the same global phase, while tested reduced density matrices and ideal clock probabilities remain unchanged.

This retains the vector/ray distinction used throughout Stage 4 and Stage 5.

## Subsystem permutation covariance

For the symmetric qutrit baseline, all six permutations of subsystem names are implemented as explicit tensor-product permutation operators.

The tests verify:

- the global permutation operator is unitary;
- `U_pi H_tot U_pi^dagger=H_tot`;
- `U_pi P_phys U_pi^dagger=P_phys`;
- per-clock reduction commutes with the corresponding global/rest permutation diagram;
- genuine cross-clock maps commute with the induced source/target rest-space permutations.

This is stronger than merely re-running functions with renamed strings because the tensor coordinates themselves are permuted.

Negative guard:

if the asymmetric rate tuple `(1,1,2)` is held fixed and A/C are swapped, the total Hamiltonian is not invariant. Therefore symmetric subsystem-permutation covariance must not be promoted into an unrestricted physical permutation symmetry.

## Origin/bookkeeping scope

Stage 5G explicitly tests global phase and subsystem bookkeeping/permutation covariance. A new continuous clock-origin parameter is not introduced in Stage 5; Stage 4 already tested common clock-origin covariance for the one-clock construction.

Therefore Stage 5G does not claim a new cross-clock origin-covariance theorem beyond the discrete clock-coordinate/frame maps already tested.

## Interpretation guard

The higher-dimension and asymmetric-rate results strengthen the finite-model claim that the perspective-consistency structure is not confined to one symmetric seven-dimensional example.

They still do not establish:

- equivalence of arbitrary physical clocks;
- interacting-clock covariance;
- quantum general covariance;
- gravitational general covariance;
- a fundamental ontology of relational time.

`robust across declared finite controls != universal physical invariance`.
