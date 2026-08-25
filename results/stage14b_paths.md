# Stage 14B Result — Phase-Space-Dependent Mixed Paths and Third-Direction Compensation

Status: **validated; criteria 18–24 satisfied. Stage 14C is next.**

Incoming Stage 14A synchronized checkpoint: head `db72c8715a3b58d4422932640807dbb20297005e`, run #1846, **`1114 passed in 900.17s (0:15:00)`**.

Stage 14B source/test head: `2b0866b63e6fb4d4951f883839e6693b12ceddfc`, run #1852, **`1122 passed in 891.20s (0:14:51)`**.

## Validated finite family

- physical orbits carried from Stage 14A: **4**;
- positive representatives: **108**;
- canonical ordered mixed pairs: **864**;
- positive compensated path results: **1728** (`12D` and `21D` for every pair);
- nontrivial `X_0 != 0` pairs: **576**;
- exact-zero `X_0 = 0` pairs: **288**.

The exact compensation law is

`v_21D-v_12D = X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]`.

Validated deterministic values:

- nonzero compensator-difference count: **576**;
- zero compensator-difference count: **288**;
- minimum nonzero absolute difference: approximately **0.3934693402873666**;
- maximum absolute difference: approximately **2.3504023872876028**;
- maximum compensator-identity residual: **0.0**;
- maximum raw analytic-formula residual: approximately **4.440892098500626e-16**;
- maximum positive final-endpoint residual: approximately **4.440892098500626e-16**;
- maximum positive final Dirac-data residual: approximately **4.440892098500626e-16**.

Thus both ordered path implementations match the frozen exact formulas, and exact third-direction compensation closes all positive mixed paths on their licensed target within the `1e-10` tolerance.

## Validated controls

- wrong-sign compensator: rejected on **1728/1728** paths;
- half-value compensator: rejected on **1728/1728** paths;
- missing third-direction compensator: rejected on **1728/1728** paths;
- Stage-13-style same-`D`-compensator-under-reordering control: rejected on **576/576** nontrivial pairs;
- exact-zero-difference compatibility retained on **288/288** `X_0=0` pairs;
- cross-orbit false positives: **8748/8748** rejected.

Supported bounded control labels include

`wrong_structure_function_compensator_detected`,

`missing_third_direction_compensator_detected`,

`cross_orbit_false_positive_rejected`.

## Bounded result

`Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established`

This means that, on the validated finite carrier, path order can change raw intermediate coordinates and the required `D` compensator, while exact compensation returns both ordered words to the same licensed sampled target and preserves the same Dirac data.

It does **not** mean that the raw path words are physically distinct histories.

It does **not** establish refoliation invariance, a hypersurface-deformation algebra, general covariance, diffeomorphism invariance, gravity, or GR.

## Closed criteria

Stage 14B closes exactly criteria **18–24**:

18. canonical 864 mixed pairs constructed;
19. both ordered path implementations match frozen exact formulas;
20. exact third-direction compensation closes every positive mixed pair;
21. the nontrivial `X_0 != 0` subfamily has the expected nonzero raw compensator difference;
22. frozen wrong/missing/Stage-13-style controls are rejected where required;
23. cross-orbit pairs are never licensed as gauge paths;
24. the interpretation remains explicitly bounded away from refoliation invariance, time asymmetry, and ontological becoming.

## Next

Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination.

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
