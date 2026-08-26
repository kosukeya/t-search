# Stage 16B Result — Cyclic Path Defects and Compensation Audits

Status: **Stage 16B scientific implementation validated; criteria 18–24 satisfied by executable path evidence. Criteria 25–50 remain pending.**

Incoming validated Stage 16A documentation checkpoint: head `02dee737257b241719902b17959445e8dc9456e5`, PR run #2016, **`1281 passed in 909.08s (0:15:09)`**.

Stage 16B source/test checkpoint: head `5f7806f9cebcb0173d215c3795412c9ab384d8d9`, PR run #2022, **`1289 passed in 915.46s (0:15:15)`**.

## Scope

Stage 16B tests finite path ordering on the validated four-site cyclic carrier without importing Stage 16C quotient theorems or Stage 16D basis-Abelianization claims.

It distinguishes four levels that must not be collapsed:

1. raw ordering defects of presented `C_i` flows;
2. exact defect prediction in seed coordinates;
3. compensation by commuting global seed `K_i` flows as an algebraic/gauge oracle;
4. compensation constructed solely from finite words of the presented `C_i` flows under the frozen 24-word / bounded-parameter search.

`seed-compensated closure != local presented-basis compensation`.

`Stage 16B path compensation != Stage 16D basis Abelianization`.

## Exact local flows and independent oracle

On the positive surface, the exact `C_i` flow with parameter `s` changes only

`T_i -> T_i+s`

and

`T_{i+1} -> T_{i+1}+kappa*(T_i*s+s^2/2)`

with indices modulo four; the carried `(Q_D,P_D)` is kept fixed when reconstructing the phase-space point.

A separate RK4 Hamiltonian-vector-field oracle integrates the full ten-dimensional canonical vector field. A deterministic 12-representative subset (three clock configurations per physical orbit), all four generators, and both `±0.5` parameters gives **96 independent local-oracle comparisons**.

Maximum exact-flow vs independent-oracle phase-space residual: **0.0**.

## Adjacent ordering defects

The frozen family contains

`324 representatives × 4 adjacent edges × 2 step pairs = 2592`

adjacent local probes.

For edge `(i,i+1)`, comparing `i(s)` then `i+1(u)` against the reverse ordering produces a defect only in clock `i+2`:

`Delta T_{i+2}=kappa^2*u*(T_i*s+s^2/2)`.

Results:

- adjacent probes: **2592**;
- nonzero raw defects: **2592 / 2592**;
- maximum prediction residual: **0.0**;
- maximum off-axis clock residual: **0.0**;
- opposite-pair commuting controls: **1296 / 1296**.

The raw ordering defect is therefore real on the frozen finite carrier rather than a constraint-surface zero.

`raw path-word inequality != physical path dependence`.

## Global seed compensation

Because the commuting seed basis is known globally, a seed flow can shift the defect clock directly. Applying the required `K_{i+2}` correction to the reverse adjacent endpoint closes all 2592 local probes.

- maximum seed-compensated local phase-space residual: **2.220446049250313e-16**;
- maximum local payload residual: **2.220446049250313e-16**.

This is deliberately labelled `global_seed_oracle`; it is not counted as locality-preserving presented-basis compensation.

## Frozen presented-`C` compensation search

For every adjacent raw endpoint pair, Stage 16B executes the frozen candidate family of all **24 permutations** of `(0,1,2,3)`. Each word receives four deterministic Newton-solved flow parameters, each restricted to `[-2,2]`, and success requires endpoint residual `<=1e-10`.

Observed classification:

`presented_C_compensator_found_for_all_frozen_local_probes`.

Results:

- successful searches: **2592 / 2592**;
- failures: **0**;
- maximum attempts before success: **1**;
- every probe succeeds with the first frozen word `(0,1,2,3)`;
- maximum absolute presented parameter: **0.10279126289269715**;
- maximum formula-composed presented endpoint residual: **1.13420384195706e-12**;
- independent Hamiltonian-oracle residual for a deterministic 96-probe compensation subset: **1.1337597527472099e-12**.

This is a finite path-compensation result. It does **not** imply that an L1 or Lfinite Abelianizing basis exists.

`presented compensator found != locality-preserving Abelianizing basis`.

## Constant-smeared finite flows

For constant smearing `N`, the clock system is affine linear:

`dT_i/dlambda=N_i+kappa*N_{i-1}*T_{i-1}`.

Stage 16B solves this by a deterministic scaling/squaring matrix exponential of the augmented affine system and compares it with an independent full Hamiltonian RK4 oracle.

Independent single-smeared oracle comparisons: **84**.

Maximum single-smeared matrix-exponential vs independent-oracle residual: **2.5299762285158067e-11**.

For the eight frozen smearing pairs at `(alpha,beta)=(0.5,0.5)`:

- smeared ordering probes: **2592**;
- nonzero raw ordering defects: **2268**;
- exact zero-wedge controls: **324**;
- maximum independent smeared-order defect-oracle residual: **7.926992395823618e-14**;
- maximum seed-compensated smeared phase-space residual: **8.881784197001252e-16**;
- maximum smeared payload residual: **8.881784197001252e-16**.

`finite constant smearing != continuum lapse/shift field`.

## Four-generator cycle-word audit

All 24 permutations of `(0,1,2,3)` are also applied with a common finite parameter `0.5` inherited from the frozen local-step family to every positive representative, using `(0,1,2,3)` as the reference word.

- cycle-word endpoint probes: **7776 = 324×24**;
- reference-word equalities: **324**;
- non-reference raw word defects: **7452 = 324×23**;
- maximum seed-compensated cycle endpoint residual: **4.440892098500626e-16**;
- maximum cycle payload residual: **4.440892098500626e-16**.

The cycle therefore exhibits finite word-order dependence on every non-reference permutation in this frozen audit, while the known seed atlas still supplies exact orbit-level endpoint compensation.

`cycle path defect != spacetime curvature`.

`compensated cycle path closure != refoliation invariance`.

## Negative controls

The same 2592 adjacent defects reject both deliberately inadequate controls:

- minimum missing-compensator residual: **0.015625**;
- minimum wrong-sign-compensator residual: **0.03125**.

Both exceed the frozen `1e-10` endpoint tolerance on every local probe.

## Criteria 18–24

18. Exact local finite flows and an independent Hamiltonian-flow oracle are established.
19. All 2592 adjacent ordering defects match the frozen seed-coordinate prediction exactly; 1296 opposite-pair controls commute.
20. Global seed compensation closes every adjacent defect and is kept semantically separate from presented-`C` compensation.
21. The frozen 24-word / `[-2,2]` presented-`C` search is executed over all adjacent probes and finds a bounded compensator for all 2592 without promotion to a basis-Abelianization claim.
22. Exact affine-linear constant-smeared flows are implemented by matrix exponential and independently checked against the Hamiltonian ODE oracle.
23. Smeared ordering defects, seed compensation, payload preservation, and the 24-permutation cycle-word audit are established on the declared finite family.
24. Missing/wrong-sign compensation controls reject, and Stage 16B tests/docs/results are synchronized.

Criteria **25–50 remain pending**.

## Bounded result

`Stage 16B finite cyclic local/smeared path defects, seed compensation, presented-C compensation search, and independent flow oracle = established`.

More specifically, finite presented paths on the four-cycle are strongly order-sensitive on the frozen family, while both the known global seed atlas and a bounded four-presented-generator word search can compensate the tested adjacent endpoint defects. The frozen smeared and full-cycle word families likewise display raw ordering dependence but preserve the carried payload under seed compensation.

This does not establish a physical quotient theorem, same-orbit reachability, complete relational descent, L1/Lfinite Abelianization, locality obstruction, refoliation invariance, spacetime curvature, general relativity, eternalism, ontological becoming, absence of becoming, or empirical discovery.

Persistent guards:

- `raw path-word inequality != physical path dependence`;
- `seed-compensated closure != local presented-basis compensation`;
- `presented compensator found != locality-preserving Abelianizing basis`;
- `presented compensator not found in frozen word search != physical obstruction`;
- `compensated cycle path closure != refoliation invariance`;
- `cycle path defect != spacetime curvature`;
- `finite constant smearing != continuum lapse/shift field`;
- `Stage 16B path compensation != Stage 16D basis Abelianization`;
- `repository validation != new scientific evidence`.

## Next

Stage 16C — Dirac pair, four-clock complete relational observables, physical quotient, reachability, and orbit discrimination.
