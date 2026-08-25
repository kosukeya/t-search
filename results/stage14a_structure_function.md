# Stage 14A Result — Three-Constraint First-Class Structure-Function Carrier and Finite Representative Family

Status: **validated; criteria 11–17 satisfied. Stage 14B is next.**

Incoming validated baseline: Stage 14.0 head `afe0598362ccf0e808d2c690491cda810594d87e`, run #1832, **`1106 passed in 879.78s (0:14:39)`**.

Stage 14A source/test checkpoint: head `d1116a743b0374c96993c476331f5cceacfbb077`, run #1838, **`1113 passed in 545.23s (0:09:05)`**.

## Executable carrier

The implementation in `src/t_search/stage14_structure_function.py` realizes

`D=p_X+0.5p`,

`H_1=p_1+p^2/2`,

`H_2=p_2+0.25p+0.5 T1 X D`

on the four carried physical classes and the frozen `3 x 3 x 3` `(T1,T2,X)` grid.

Family size:

- physical orbits: **4**;
- representatives/orbit: **27**;
- representatives total: **108**;
- off-surface bracket/Jacobi probes: **108**;
- single-generator flow probes: **648**.

## Constraint surface and independence

All 108 representatives satisfy all three positive constraints with maximum residual **0.0**.

At every positive representative:

- constraint-gradient rank = **3**;
- Hamiltonian-generator-vector rank = **3**.

The minimum singular value of both tested three-row families is approximately **0.7812880785647448**.

Thus the positive family does not obtain three labels by duplicating a lower-rank gauge direction.

## Phase-space-dependent structure functions

The sampled coefficient family is

`f_12^D=-0.5 X`,

`f_2D^D=0.5 T1`.

Across the frozen grid the realized coefficient values are exactly

**{-0.5, 0.0, 0.5}**.

Negative, zero, and positive coefficients therefore all occur in the positive family.

This is a finite structure-function variation result only.

## First-class closure and Jacobi

The implementation evaluates the frozen canonical Poisson brackets from analytic gradients:

`{H_1,D}=0`,

`{H_1,H_2}=-0.5 X D`,

`{H_2,D}=0.5 T1 D`.

The identities are checked on all 108 positive representatives and on 108 deliberately off-surface probes with nonzero `D`.

Maximum bracket-identity residual: **0.0**.

The Jacobi combination is evaluated on the same 216 points.

Maximum Jacobi residual: **0.0**.

Bounded classification:

`Stage 14A first-class phase-space-dependent closure and Jacobi consistency on the frozen finite carrier = established`.

`finite first-class structure-function algebra != hypersurface-deformation algebra`.

## Individual flow preservation

Every positive representative is evolved under each of `Phi_D`, `Phi_1`, and `Phi_2` at both `-0.5` and `+0.5`, giving **648** finite flow probes.

Maximum target constraint residual: **0.0**.

Maximum `(Q_D,P_D)` preservation residual: approximately **2.220446049250313e-16**.

Thus each generator separately preserves the declared positive surface and carried Dirac data on the tested finite family.

`Stage 14A single-generator surface/Dirac preservation != third-direction compensated mixed-path closure`.

## Controls

The `kappa=0` carrier has no nontrivial Stage 14 structure-function values and is classified

`structure_function_removed_control_rejected`.

The duplicate-direction control has constraint-gradient rank two and is classified

`rank_deficient_constraint_control_rejected`.

These are negative controls, not positive-family obstructions.

## Bounded Stage 14A result

`Stage 14A three-constraint first-class structure-function carrier and finite representative family = established`.

The next executable question is Stage 14B: construct the 864 frozen mixed pairs and test exact `12D`/`21D` third-direction compensation.

## Guards

- `phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`;
- `finite first-class structure-function algebra != hypersurface-deformation algebra`;
- `structure functions != spacetime geometry by definition`;
- `three constraint labels != three independent gauge directions`;
- `Stage 14A single-generator surface/Dirac preservation != third-direction compensated mixed-path closure`;
- `third-direction compensation != refoliation invariance`;
- `hypersurface-deformation precursor != general relativity`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.
