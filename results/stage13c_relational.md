# Stage 13C Result — Dirac / Two-Clock Complete Relational Observables

Status: **executable implementation complete; repository CI checkpoint pending at the time of this result write.**

Incoming validated baseline: Stage 13B documentation-synchronized head `d559c031590a058962c50d170b144acbe8eabadd`, run #1726, **`1059 passed in 538.54s (0:08:58)`**.

## Executable family

`src/t_search/stage13_relational.py` consumes the 36 Stage 13A representatives and the 144 Stage 13B compensated mixed-path comparisons.

The executable finite family contains

- **36** independently reconstructed Dirac estimates;
- **4** same-orbit Dirac summaries;
- **6** unordered different-orbit discrimination checks;
- **324** two-clock complete-relational evaluations;
- **1296** compensated-path complete-relational comparisons;
- **36** one-clock evaluations grouped into **12** fixed-`T` groups.

## Dirac reconstruction result

For every raw representative,

`Q_D=q-pT-0.5X`,

`P_D=p`

are reconstructed without using the stored declared values as inputs.

Deterministic finite-family maxima are expected to be within floating tolerance:

- reconstructed/declaration `Q_D` residual: at most approximately **2.220446049250313e-16**;
- reconstructed/declaration `P_D` residual: **0.0**;
- same-orbit `Q_D` spread: at most approximately **2.220446049250313e-16**;
- same-orbit `P_D` spread: **0.0**;
- Dirac/constraint Poisson-bracket residual: **0.0** for the analytic-gradient construction.

All four physical orbits therefore retain representative-independent full Dirac data within the declared tolerance.

## Different-orbit result

All **6 / 6** unordered different-orbit pairs remain distinct under the full `(Q_D,P_D)` pair.

Minimum full-pair separation: **0.5**.

The family retains exactly one canonical same-P/different-Q control and one canonical same-Q/different-P control:

- alpha / beta: same `P_D`, different `Q_D`;
- alpha / gamma: same `Q_D`, different `P_D`.

Bounded classification:

`full_dirac_pair_orbit_discrimination_established`.

## Complete relational result

The existing `3 x 3` Stage 13 clock grid is used as the target family:

`tau,chi in {-1,0,1}`.

Each of 9 source representatives on each of 4 physical orbits reconstructs its own `(Q_D,P_D)` and evaluates all 9 targets:

**324 evaluations total**.

For

`q(T=tau,X=chi)=Q_D+P_D tau+0.5chi`,

the deterministic maximum residual against the canonical same-orbit target representative is approximately **2.220446049250313e-16**.

The complete-relational values are therefore representative-independent within each tested physical orbit and remain nontrivial across the target clock grid.

## Compensated path-choice result

For each of the **144** Stage 13B compensated mixed-path comparisons, Stage 13C reconstructs Dirac data independently from the `TX` and `XT` endpoints and evaluates all 9 target clock pairs.

This produces **1296** comparisons requiring

`q_TX ~= q_XT ~= q_target`.

The deterministic maximum residual is approximately **2.220446049250313e-16**.

Bounded classification:

`compensated_path_complete_relational_covariance_established`.

This does not establish refoliation invariance or a hypersurface-deformation algebra.

## One-clock negative control

The frozen one-clock expression

`q(T=tau;X raw)=Q_D+P_D tau+0.5X_raw`

is evaluated for 4 orbits x 3 `tau` values x 3 raw `X` values = **36** evaluations.

The resulting **12** fixed-orbit/fixed-`tau` groups all have nonzero `X`-dependent spread, approximately **1.0** in every group.

Classification:

`one_clock_observable_incomplete`.

Thus fixing only `T=tau` does not yield a complete relational observable in this two-gauge-direction model.

## Bounded result

`Stage 13C Dirac / two-clock complete relational observables and physical-orbit discrimination on the frozen finite family = established`

subject to repository CI validation of the new executable/test family.

The result supports the finite structural conjunction

`representative-independent Dirac orbit data + compensated-path-independent complete relational values + nontrivial relational change`.

It does **not** license an ontological conclusion.

## Guards

- `Dirac invariant != timeless ontology by definition`;
- `full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem`;
- `one clock condition in a two-gauge-direction model != complete relational observable`;
- `compensated-path relational covariance != refoliation invariance`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `path-independent complete-relational values != future actuality`;
- `finite-model success != empirical discovery`.

## Next boundary

Stage 13D is the next executable question:

> build the typed multi-constraint atlas from `Phi_T/Phi_X` connectivity rather than stored orbit labels, recover exactly four quotient classes of nine representatives, and test whether Dirac / complete-relational payloads descend across typed path words and compensators without collapsing physically distinct orbit data.
