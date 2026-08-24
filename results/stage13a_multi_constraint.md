# Stage 13A Result — Two-Constraint First-Class Carrier and Finite Representative Family

Status: **validated; criteria 11–16 satisfied. Stage 13B is next.**

Incoming validated baseline: Stage 13.0 head `898f36682b3cadac4abd953ba1bac8e32f17103e`, run #1672, **`1039 passed in 542.21s (0:09:02)`**.

Stage 13A source/test checkpoint: head `ccd35956ac034de5d73d8b884a361fbe2fc92784`, run #1676, **`1048 passed in 592.23s (0:09:52)`**.

## Executable family

The implementation in `src/t_search/stage13_multi_constraint.py` realizes the Stage 13.0 frozen carrier

`K_T = p_T + p^2/2`,

`K_X = exp(T)(p_X + 0.5p)`

on the four retained Stage 12 physical initial-data classes and the `3 x 3` `(T,X)` grid.

Deterministic family size:

- physical orbits: **4**;
- representatives/orbit: **9**;
- representatives total: **36**;
- `Phi_T` ordered nonidentity transports: **72**;
- `Phi_X` ordered nonidentity transports: **72**;
- single-generator transports total: **144**;
- mixed ordered pairs reserved for Stage 13B: **144**;
- nonzero off-surface bracket probes: **36**.

## Constraint satisfaction

All canonical representatives are constructed with

`p_T=-P_D^2/2`,

`p_X=-0.5P_D`,

so both positive constraints vanish within the Stage 13A tolerance `1e-10`.

The deterministic construction gives

- max `|K_T|`: **0.0**;
- max `|K_X|`: **0.0**.

## Independence

At every one of the 36 positive representatives:

- constraint-gradient rank = **2**;
- Hamiltonian-generator-vector rank = **2**.

The minimum singular value of both tested two-row families is approximately

**0.3778026572933153**.

Thus the finite carrier does not obtain two generator labels by duplicating one direction.

## First-class closure

The implementation evaluates the canonical Poisson bracket from analytic gradients and checks

`{K_T,K_X}+K_X = 0`.

The check is performed on the 36 positive representatives and on 36 deliberately off-surface probes with nonzero `K_X`. The deterministic maximum bracket-identity residual is **0.0**.

Bounded classification:

`Stage 13A first-class bracket identity on the frozen finite carrier = established`.

This classification does not imply a hypersurface-deformation algebra.

## Individual flow preservation

For every licensed `Phi_T` and `Phi_X` transport, the implementation reconstructs the predicted phase-space endpoint and evaluates both constraints there.

Deterministic maxima:

- max `Phi_T` endpoint residual: approximately **2.220446049250313e-16**;
- max `Phi_X` endpoint residual: approximately **2.220446049250313e-16**;
- max predicted/source/target positive-surface constraint residual: **0.0**.

Thus each frozen generator separately preserves the positive two-constraint surface on the declared finite path family.

## Physical-class carry-over

The four declared `(Q_D,P_D)` initial-data pairs remain distinct and each owns exactly nine positive representatives. The finite family still contains the Stage 12 same-P/different-Q and same-Q/different-P anti-triviality controls.

This is only a carrier-level non-collapse result. Independent Dirac reconstruction and physical-orbit discrimination are intentionally deferred to Stage 13C.

## Typed provenance

Representative and transport records keep separate typed roles for

- physical orbit;
- representative;
- event;
- `T` clock;
- `X` clock;
- generator;
- constraint basis.

No generator label is treated as an event, clock, or physical-orbit identifier.

## Stage boundary

Stage 13A does **not** establish compensated two-generator closure. The 144 mixed pairs are enumerated but not promoted to positive path-covariance evidence.

`Stage 13A single-generator surface preservation != compensated multi-generator path closure`.

The next executable question is Stage 13B:

> compare the two noncommuting path orders across all 144 mixed pairs, verify detectable same-raw-parameter order dependence, and test the exact compensator `u_XT=exp(s)u_TX`.

## Bounded Stage 13A result

`Stage 13A two-constraint first-class carrier and finite representative family on the frozen four-orbit family = established`

Repository source/test checkpoint #1676 passed with **`1048 passed in 592.23s (0:09:52)`**.

## Guards

- `two constraint labels != two independent gauge directions`;
- `first-class closure on this toy carrier != hypersurface-deformation algebra`;
- `Stage 13A single-generator surface preservation != compensated multi-generator path closure`;
- `multi-constraint carrier != refoliation invariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `finite-model success != empirical discovery`.
