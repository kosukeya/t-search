# Stage 16A Notes — Four-Site Cyclic First-Class Carrier, Exact Local/Smeared Algebra, Support Audits, and Finite Representative Family

Status: **Stage 16A scientific result established; criteria 11–17 satisfied. Criteria 18–50 remain pending.**

Incoming validated Stage 16.0 checkpoint: head `29a61144b0274e452208de8201b5703a5fa26b89`; push run #2011 **`1268 passed in 906.14s (0:15:06)`**; PR run #2012 **`1268 passed in 552.90s (0:09:12)`**.

Stage 16A scientific source/test checkpoint:

`20f448e676499ecdab87b890bef79c9e19302832`

PR run #2014 validates the merge checkout `bc7b18714841751bf0107646298003059ff4ce70` with

**`1276 passed in 716.34s (0:11:56)`**.

Push run #2013 was still in progress when this scientific checkpoint was documented and is not used as evidence for closing criteria 11–17.

## What Stage 16A tests

Stage 16A implements only the carrier-level evidence frozen in `docs/stage16_protocol.md`:

- the four carried physical payload classes generate 81 on-surface representatives each, 324 total;
- the cyclic frame remains nonsingular on the entire frozen positive grid;
- the four presented constraint gradients and Hamiltonian generator vectors have rank four;
- the complete unsmeared Poisson algebra is independently certified by an exact sparse-polynomial oracle and by analytic/numerical evaluation;
- direct brackets agree both with the seed-coordinate identities and with exact first-class reconstruction in the presented `C` basis;
- the Jacobi identity is checked on the positive and deterministic off-surface families;
- canonical-function support and presented-basis closure-coordinate support are audited separately;
- the frozen smeared family is independently certified symbolically and checked by direct, seed-coordinate, and presented-`C` reconstruction, including antisymmetry, Kronecker recovery, and the parallel zero-wedge control.

Finite path defects and compensation remain Stage 16B. Full quotient/reachability and complete-relational descent remain Stage 16C. Locality-preserving Abelianization remains Stage 16D. Typed O/P/R/V/Xi descent remains Stage 16E.

## Executable cyclic carrier

Implementation: `src/t_search/stage16_local.py`.

The carrier is

`K_i=pi_i+c_i P`, with `c=(1.0,0.5,-0.25,0.75)`,

`C_i=K_i+0.5 T_i K_{i+1 mod 4}`.

The cyclic frame determinant is

`Delta=1-0.5^4 T_0 T_1 T_2 T_3`.

On `T_i in {-1,0,1}`, the realized determinant values are exactly

`{15/16,1,17/16}`

with minimum absolute value **15/16 = 0.9375**.

The exact inverse reconstruction is exercised numerically on the positive and off-surface families, with maximum seed-inverse residual approximately

**`1.1102230246251565e-16`**.

## Exact local algebra

An independent exact sparse-polynomial oracle implemented in `tests/test_stage16a_local_smeared.py` uses `fractions.Fraction` and exact monomial arithmetic. It certifies all ordered unsmeared Poisson identities without relying on sampled floating-point agreement.

The adjacent forward brackets are

`{C_0,C_1}=-0.25 T_0 K_2`,

`{C_1,C_2}=-0.25 T_1 K_3`,

`{C_2,C_3}=-0.25 T_2 K_0`,

`{C_3,C_0}=-0.25 T_3 K_1`,

with antisymmetric counterparts and opposite pairs zero.

The sampled structure-function factors realize exactly

**`{-0.25,0.0,0.25}`**.

Across all 324 deterministic off-surface probes, the four adjacent forward brackets are nonzero in **864** cases. Thus first-class reconstruction is not accepted merely from weak vanishing on the positive constraint surface.

Maximum direct-vs-seed unsmeared residual: **0.0**.

Maximum direct-vs-presented-`C` reconstruction residual: approximately **`1.3877787807814457e-17`**.

## Rank and finite family

Deterministic counts:

- physical payload classes: **4**;
- representatives/class: **81**;
- positive representatives: **324**;
- off-surface probes: **324**;
- total positive/off-surface points used in algebra/support checks: **648**;
- minimum constraint-gradient rank: **4**;
- minimum Hamiltonian-generator rank: **4**;
- minimum constraint-gradient singular value: **0.5**;
- minimum Hamiltonian-generator singular value: approximately **0.5**;
- maximum positive constraint residual: **0.0**.

The embedded expressions `P_D=P` and `Q_D=Q-sum_i c_i T_i` recover the declared payload pair for every positive representative. Full Dirac-observable descent is still Stage 16C.

## Jacobi audit

The four independent three-generator triples are checked on all 648 positive/off-surface points, giving

**2592 Jacobi probes**.

Maximum Jacobi residual: **0.0**.

## Support audit

Stage 16A deliberately keeps two support notions separate.

For an adjacent bracket such as `{C_0,C_1}=-0.25 T_0 K_2`, its canonical-function support is `{0,2}`, contained in the union of the canonical supports of `C_0` and `C_1`, namely `{0,1,2}`.

However, replacing `K_2` by the exact cyclic inverse can activate all four presented `C` labels. Across the positive/off-surface family, **768 adjacent-forward probes** have closure-coordinate support size four; the maximum observed closure-coordinate support size is **4**.

This is a representation/support result only:

`local canonical support != local closure-coordinate support`.

`cycle-spanning closure coordinates != physical nonlocality by definition`.

It is not evidence that a locality-preserving Abelianizing basis is obstructed; that is deferred to Stage 16D.

## Finite smeared algebra

The exact sparse-polynomial oracle also certifies the eight frozen smeared identities. Direct analytic-gradient evaluation is then compared with both seed-coordinate and presented-`C` reconstruction on all positive/off-surface points.

Deterministic counts:

- frozen smearing pairs: **8**;
- smeared probes: **5184**;
- parallel zero-wedge probes: **648**.

Maximum direct-vs-seed smeared residual: **0.0**.

Maximum direct-vs-presented-`C` smeared residual: approximately **`2.7755575615628914e-17`**.

Maximum antisymmetry residual: **0.0**.

All canonical-function support checks pass, Kronecker smearings recover the unsmeared algebra, and the frozen parallel pair has zero direct bracket throughout the 648-point source family.

`finite smeared algebra != continuum hypersurface-deformation algebra`.

## Criteria 11–17

Stage 16A closes only criteria **11–17**:

11. the frozen four-orbit / 324-positive / 324-off-surface family and nonsingular cyclic frame are realized;
12. four independent constraint-gradient and Hamiltonian-generator directions are established throughout the positive family;
13. the frozen unsmeared algebra is certified exactly and the structure factors sample negative, zero, and positive values;
14. on- and off-surface direct brackets agree with both seed-coordinate identities and exact presented-`C` first-class reconstruction;
15. Jacobi, canonical-function support, and closure-coordinate support audits are established while their physical interpretation remains separated;
16. exact/direct finite smeared algebra, antisymmetry, Kronecker recovery, zero-wedge control, and support checks are established;
17. deterministic diagnostics preserve the four declared payload embeddings without importing Stage 16B/C/D/E claims.

Criteria **18–50 remain pending**.

## Bounded result

`Stage 16A four-site cyclic first-class carrier, exact local/smeared algebra, support audits, and finite representative family = established`

This means only that the frozen four-cycle gives a nondegenerate finite first-class carrier whose local and finite-smeared algebra is internally consistent and exactly reconstructible in the presented basis on the declared family.

It does not establish finite compensated path covariance, quotient/reachability, a local Abelianization witness or obstruction, refoliation invariance, relativistic locality, a continuum hypersurface-deformation algebra, general relativity, eternalism, ontological becoming, absence of becoming, or future actuality.

Guards:

- `four-site cycle != spatial topology of the universe`;
- `cyclic first-class closure != hypersurface-deformation algebra`;
- `cycle-spanning closure coordinates != physical nonlocality by definition`;
- `local canonical support != local closure-coordinate support`;
- `declared Dirac-payload consistency != full Dirac-observable descent`;
- `local/smeared closure != compensated cycle-path closure`;
- `Stage 16A support audit != Stage 16D locality obstruction`;
- `known global Abelianization != proof that all Abelianizations are nonlocal`;
- `failure to Abelianize != ontological becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## Next

Stage 16B — local/smeared/cycle path defects, seed compensation, presented-basis compensation search, and independent flow oracle.
