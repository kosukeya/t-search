# Stage 14B Notes — Phase-Space-Dependent Mixed Paths and Third-Direction Compensation

Status: **validated; criteria 18–24 satisfied. Stage 14C is next.**

Incoming documentation-synchronized Stage 14A checkpoint: head `db72c8715a3b58d4422932640807dbb20297005e`, run #1846, **`1114 passed in 900.17s (0:15:00)`**.

Stage 14B source/test checkpoint: head `2b0866b63e6fb4d4951f883839e6693b12ceddfc`, run #1852, **`1122 passed in 891.20s (0:14:51)`**.

## Executable family

Stage 14B consumes the validated three-constraint Stage 14A carrier and the frozen `3 x 3 x 3` representative grid.

The canonical mixed family contains **864 ordered same-orbit source/target pairs** for which

- `T1_1 != T1_0`;
- `T2_1 != T2_0`;
- `X_1 != X_0`.

For every pair the implementation evaluates both ordered words

- `12D = Phi_1(s) -> Phi_2(u) -> Phi_D(v_12D)`;
- `21D = Phi_2(u) -> Phi_1(s) -> Phi_D(v_21D)`.

This yields **1728 positive compensated path results**.

## Exact raw path formulas

With

`s=T1_1-T1_0`,

`u=T2_1-T2_0`,

the raw `X` endpoints before the final `D` compensation are

`X_12*=X_0 exp(kappa T1_1 u)`,

`X_21*=X_0 exp(kappa T1_0 u)`.

The exact compensators are

`v_12D=X_1-X_12*`,

`v_21D=X_1-X_21*`,

with identity

`v_21D-v_12D = X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]`.

The implementation compares the executable paths against these analytic formulas rather than using the same path code as its oracle.

## Positive compensated closure

All **1728/1728** compensated positive paths close on the licensed sampled target within the frozen tolerance `1e-10`.

Deterministic floating-point maxima are at numerical-noise scale:

- maximum raw-formula residual: approximately **4.440892098500626e-16**;
- maximum final endpoint residual: approximately **4.440892098500626e-16**;
- maximum final Dirac-data residual: approximately **4.440892098500626e-16**;
- maximum compensator-identity residual: **0.0**.

Bounded classification:

`Stage 14B exact third-direction compensated mixed-path closure on the frozen finite family = established`.

## Nontrivial and exact-zero path-order subfamilies

The 864 mixed pairs split exactly into

- **576** pairs with `X_0 != 0`, all with nonzero path-order-dependent compensator difference;
- **288** pairs with `X_0 = 0`, all with exact zero compensator difference.

For the nontrivial family,

- minimum nonzero `|v_21D-v_12D|`: approximately **0.3934693402873666**;
- maximum `|v_21D-v_12D|`: approximately **2.3504023872876028**.

Thus the positive result is not based on tiny floating-point differences. At the same time, the exact `X_0=0` subfamily prevents the false claim that distinct path words must always require distinct raw compensators.

`raw path-word inequality != physical path dependence`.

## Negative controls

The executable controls classify as intended:

- wrong-sign `D` compensator rejected on **1728/1728** paths;
- half-value compensator rejected on **1728/1728** paths;
- missing / zero compensator rejected on **1728/1728** paths;
- reusing the `12D` compensator for `21D` is rejected on all **576/576** nontrivial `X_0 != 0` pairs;
- the same reused-compensator control remains compatible on the **288/288** exact-zero-difference `X_0=0` pairs, as it should;
- all **8748** cross-orbit representative pairs are rejected as licensed gauge paths.

Frozen control vocabulary supported here includes

- `wrong_structure_function_compensator_detected`;
- `missing_third_direction_compensator_detected`;
- `cross_orbit_false_positive_rejected`.

The Stage-13-style same-compensator-under-reordering control is rejected only where the frozen structure-function carrier predicts a nonzero difference; the exact-zero subfamily is not mislabeled as a failure.

## What Stage 14B adds

Stage 14A established a finite first-class carrier with three independent constraint directions and phase-space-dependent structure functions. Stage 14B now shows, on the frozen finite family, that two different ordered words can have different raw intermediate endpoints and different third-direction compensators while still descending to the same licensed representative and the same Dirac data after exact compensation.

This is stronger than Stage 14A single-generator preservation, but it remains a finite compensated-path result.

## Stage boundary

Stage 14B does **not** yet independently reconstruct the full quotient, prove all six physical-orbit separations, validate the complete three-condition relational observable across the entire licensed path family, or establish the incomplete two-clock control. Those are Stage 14C questions.

It also does not establish a hypersurface-deformation algebra, refoliation invariance, diffeomorphism invariance, gravitational field dynamics, or general relativity.

Persistent guards:

- `raw path-word inequality != physical path dependence`;
- `third-direction compensation != refoliation invariance`;
- `compensated mixed-path closure != refoliation invariance`;
- `wrong compensation failure != physical time asymmetry`;
- `compensated path closure != ontological becoming`;
- `finite first-class structure-function algebra != hypersurface-deformation algebra`;
- `hypersurface-deformation precursor != general relativity`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## Bounded Stage 14B result

`Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established`

Repository source/test checkpoint #1852 passed with **`1122 passed in 891.20s (0:14:51)`**.
