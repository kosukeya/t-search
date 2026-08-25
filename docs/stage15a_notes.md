# Stage 15A Notes — Local/Smeared First-Class Carrier and Finite Representative Family

Status: **Stage 15A scientific implementation complete; criteria 11–17 are satisfied by executable carrier diagnostics, with repository regression recorded separately.**

Incoming validated Stage 15.0 checkpoint: head `6fc58325494767bb68b22e2fef769a366a879c1c`, GitHub Actions run #1938, **`1167 passed in 699.10s (0:11:39)`**.

Stage 15A source/test checkpoint: head `e53dadffbf94257ef15d37b2a817cfa4caa05913`, GitHub Actions run #1941.

## What Stage 15A tests

Stage 15A implements only the carrier-level claims frozen before implementation:

- the four carried physical payload classes generate 27 on-surface representatives each, 108 total;
- the three presented constraints and Hamiltonian generator directions have rank three;
- the local structure function `-kappa^2 T_0` samples negative, zero, and positive values;
- the unsmeared Poisson algebra closes both on the positive surface and on deliberately off-surface probes;
- the Jacobi residual vanishes on the same carrier/probe family;
- direct smeared Poisson brackets agree with reconstruction in the original local basis, recover the unsmeared relations under Kronecker smearings, are antisymmetric, and obey the frozen support rule;
- the declared `(Q_D,P_D)` payload embedded in each representative is recovered correctly and yields four distinct payload pairs.

Finite path ordering, compensators, and endpoint path covariance remain Stage 15B. Full Dirac-observable/quotient descent remains Stage 15C. Locality-preserving basis search remains Stage 15D.

## Executable carrier

The implementation is `src/t_search/stage15_local.py`.

Commuting seeds:

`K_i=pi_i+c_i P`, with `c=(1.0,0.5,-0.25)`.

Presented basis:

`C_0=K_0+0.5 T_0 K_1`,

`C_1=K_1+0.5 T_1 K_2`,

`C_2=K_2`.

The directly evaluated local algebra is

`{C_0,C_1}=-0.25 T_0 C_2`,

`{C_0,C_2}=0`,

`{C_1,C_2}=0`.

## Deterministic diagnostics

- physical payload classes: **4**;
- representatives/class: **27**;
- positive representatives: **108**;
- off-surface bracket/Jacobi probes: **108**;
- total points used for local closure/Jacobi checks: **216**;
- frozen smearing pairs per point: **6**;
- smeared direct/reconstruction comparisons: **1296**;
- sampled structure-function values: **-0.25, 0.0, 0.25**;
- off-surface points with nonzero `{C_0,C_1}`: **72 / 108**;
- minimum constraint-gradient rank: **3**;
- minimum generator-vector rank: **3**;
- minimum singular value of both tested rank families: approximately **0.685372710841757**;
- maximum positive constraint residual: **0.0**;
- maximum unsmeared closure residual: **0.0**;
- maximum Jacobi residual: **0.0**;
- maximum smeared reconstruction residual: approximately **6.938893903907228e-18**;
- maximum smeared antisymmetry residual: **0.0**;
- all declared unsmeared and smeared support checks: **passed**.

The 72 nonzero off-surface brackets prevent the positive result from being accepted merely because `C_2=0` weakly on the positive constraint surface.

## Smeared consistency

For `C[N]=sum_i N_i C_i`, direct Poisson evaluation from the analytic constraint gradients is compared with the local-basis reconstruction

`{C[N],C[M]} = -0.25 T_0 (N_0 M_1-N_1 M_0) C_2`.

The six fixed smearing-pair families include Kronecker/local recovery, compact label support, and full-support cases. They are evaluated on both the 108 positive representatives and the 108 off-surface probes.

`finite smeared consistency != continuum hypersurface-deformation algebra`.

## Criterion closure

Stage 15A closes only criteria **11–17**:

11. frozen 108-representative family is realized on the constraint surface;
12. three constraint/generator directions remain independent;
13. the local structure function samples negative, zero, and positive values;
14. direct unsmeared first-class closure is established on- and off-surface;
15. Jacobi and frozen local-support consistency are established on the tested family;
16. direct smeared/local reconstruction, antisymmetry, Kronecker recovery, and support consistency are established;
17. deterministic diagnostics preserve the four declared payload classes without importing Stage 15B/C/D claims.

Criteria **18–50 remain pending**.

## Bounded result

`Stage 15A spatially indexed local/smeared first-class carrier and finite representative family = established`.

More specifically, the frozen three-site toy carrier has a nontrivial phase-space-dependent first-class local presentation whose direct unsmeared and finite smeared brackets close consistently in the declared local basis on the tested family.

This does **not** establish compensated path covariance, a physical quotient theorem, locality-protected non-Abelianity, the absence/presence of an L1 Abelianizing basis, refoliation invariance, a continuum hypersurface-deformation algebra, general relativity, eternalism, or ontological becoming.

Guards:

- `spatially indexed constraint precursor != general relativity`;
- `nearest-neighbor graph locality != relativistic locality`;
- `finite smeared algebra != continuum hypersurface-deformation algebra`;
- `phase-space-dependent local structure function != spacetime geometry`;
- `declared Dirac-payload consistency != full Dirac-observable descent`;
- `local/smeared closure != compensated local-path closure`;
- `Stage 15A locality consistency != Stage 15D basis obstruction`;
- `known nonlocal seed reconstruction != proof of locality-protected non-Abelianity`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## Next

Stage 15B — local/smeared path closure, Jacobi, and compensated-path checks.

The next discriminating question is whether different finite local/smeared generator orderings reach quotient/relationally equivalent endpoints with the required compensation rather than merely sharing the same infinitesimal first-class algebra.
