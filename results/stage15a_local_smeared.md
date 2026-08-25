# Stage 15A Result — Local/Smeared First-Class Carrier and Finite Representative Family

Status: **carrier result established; criteria 11–17 satisfied. Stage 15B is next.**

Incoming validated baseline: Stage 15.0 head `6fc58325494767bb68b22e2fef769a366a879c1c`, run #1938, **`1167 passed in 699.10s (0:11:39)`**.

Stage 15A source/test checkpoint: head `e53dadffbf94257ef15d37b2a817cfa4caa05913`, run #1941.

## Positive finite family

The implementation in `src/t_search/stage15_local.py` realizes the frozen three-site carrier

`K_i=pi_i+c_iP`,

`C_0=K_0+0.5 T_0 K_1`,

`C_1=K_1+0.5 T_1 K_2`,

`C_2=K_2`,

with `c=(1.0,0.5,-0.25)`.

The four carried `(Q_D,P_D)` payload pairs are represented on the full `3 x 3 x 3` clock grid, giving:

- physical payload classes: **4**;
- representatives/class: **27**;
- representatives total: **108**.

All positive representatives satisfy `C_0=C_1=C_2=0` with maximum residual **0.0**.

The embedded expressions

`P_D=P`,

`Q_D=Q-c_0T_0-c_1T_1-c_2T_2`

recover the declared payload pair at every positive representative and produce exactly four distinct pairs. Full Dirac invariance/descent is deliberately deferred to Stage 15C.

## Independent local directions

At every positive representative, both the three constraint gradients and the corresponding Hamiltonian generator vectors have rank **3**.

The minimum singular value observed for each tested rank family is approximately

**0.685372710841757**.

The result therefore does not arise from three labels duplicating a lower-rank constraint family.

## Phase-space-dependent local algebra

Direct canonical Poisson evaluation gives

`{C_0,C_1}=-0.25 T_0 C_2`,

`{C_0,C_2}=0`,

`{C_1,C_2}=0`.

The structure-function coefficient `-0.25 T_0` realizes exactly

**{-0.25, 0.0, 0.25}**

on the positive grid.

The identities are tested on all 108 positive representatives and on 108 deliberately off-surface probes. Among the off-surface probes, **72 / 108** have nonzero `{C_0,C_1}`, so closure is not accepted merely from weak vanishing on `C_2=0`.

Maximum unsmeared closure residual across all 216 tested points: **0.0**.

Maximum Jacobi residual across the same family: **0.0**.

All frozen unsmeared support checks pass.

Bounded classification:

`Stage 15A local phase-space-dependent first-class closure and Jacobi consistency on the frozen finite carrier = established`.

## Finite smeared algebra

For `C[N]=sum_i N_i C_i`, the direct bracket is evaluated from the analytic gradient of each smeared generator and compared with reconstruction in the same local basis.

The tested decomposition is

`{C[N],C[M]}=-0.25 T_0 (N_0M_1-N_1M_0) C_2`.

Six frozen smearing-pair families are evaluated on all 216 positive/off-surface points, producing **1296** direct/reconstruction comparisons.

Results:

- maximum direct-vs-reconstructed residual: approximately **6.938893903907228e-18**;
- maximum antisymmetry residual: **0.0**;
- Kronecker smearings recover the unsmeared algebra;
- all tested compact/full smearing support checks pass.

This establishes finite smeared consistency on the declared toy carrier only.

`finite smeared algebra != continuum distributional algebra`.

`finite smeared algebra != continuum hypersurface-deformation algebra`.

## Criteria 11–17

Criteria **11–17** are satisfied by executable evidence:

- 11 — frozen 108 positive representatives realized on-surface;
- 12 — rank-three constraint/generator directions;
- 13 — negative/zero/positive local structure-function sampling;
- 14 — direct unsmeared on/off-surface first-class closure;
- 15 — Jacobi and local-support consistency;
- 16 — finite smeared direct/reconstruction, antisymmetry, Kronecker recovery, and support consistency;
- 17 — four declared payload classes remain correctly embedded while Stage 15B/C/D claims remain unasserted.

Criteria **18–50 remain pending**.

## Bounded Stage 15A result

`Stage 15A spatially indexed local/smeared first-class carrier and finite representative family = established`.

This means only that the frozen finite three-site precursor realizes a nontrivial local first-class presentation and finite smeared closure with the declared support bookkeeping.

It does not establish:

- finite path-ordering covariance or compensator sufficiency;
- a physical quotient/Dirac-observable theorem;
- any L0/L1 Abelianization result;
- locality-protected or fundamental non-Abelianity;
- refoliation invariance;
- a continuum hypersurface-deformation algebra;
- general relativity;
- eternalism, ontological becoming, absence of becoming, or future actuality.

## Next

Stage 15B — local/smeared path closure, Jacobi, and compensated-path checks.

The key next test is finite rather than infinitesimal: compare different orderings of licensed local/smeared flows and determine whether the algebraically required compensation restores the same quotient/relational endpoint on the frozen family.
