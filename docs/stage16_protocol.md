# Stage 16 Protocol — Four-Site Closed-Cycle Locality Pressure Test

Status: **Stage 16.0 protocol freeze in progress; criteria 1–10 are assigned to the freeze and criteria 11–50 remain pending.**

## Incoming validated baseline

Stage 15 is completed and merged via PR #16 at

`cca49e37b3d4171ea74fd6c15fa119fcd4392e2d`.

The carried bounded Stage 15 synthesis is

`spatial_local_path_covariant_local_abelianizable`.

The evidence-selected Stage 16 selector is

`four_site_closed_cycle_constraint_algebra_precursor`.

Frozen gate:

> **Construct a minimal four-site closed-cycle spatially indexed first-class constraint-algebra precursor with no terminal seed generator, retain explicit local/smeared structure-function dependence, test whether one-step L1 or finite-depth locality-preserving Abelianization still exists, and retest compensated paths, the physical quotient, complete relational observables, and typed O/P/R/V/Xi descent without assuming general relativity or refoliation invariance.**

Stage 15 found an admissible one-step L1 Abelianizing witness on an open three-site chain. Stage 16 removes the terminal-seed / acyclic peeling feature while preserving a nontrivial radius-1 locality restriction.

No Stage 16 local obstruction or persistence result is established by this freeze.

## Frozen four-site cycle

Use the cycle graph

`Lambda=C4={0,1,2,3}`, with edges `0~1`, `1~2`, `2~3`, and `3~0`, abbreviated `0~1~2~3~0`.

All site arithmetic below is modulo 4 unless stated otherwise.

Canonical phase space:

`(Q,P; T_0,pi_0; T_1,pi_1; T_2,pi_2; T_3,pi_3)`.

Canonical Poisson brackets are

`{Q,P}=1`, `{T_i,pi_j}=delta_ij`,

with all undeclared brackets zero.

Constants:

`kappa=0.5`,

`c_0=1.0`, `c_1=0.5`, `c_2=-0.25`, `c_3=0.75`.

Define commuting seed constraints

`K_i=pi_i+c_i P`.

Define

`a_i=kappa T_i`.

The positive cyclic presented basis is frozen as

`C_i = K_i + a_i K_{i+1 mod 4}`.

Explicitly,

`C_0=K_0+kappa T_0 K_1`,

`C_1=K_1+kappa T_1 K_2`,

`C_2=K_2+kappa T_2 K_3`,

`C_3=K_3+kappa T_3 K_0`.

There is no terminal generator of the Stage 15 form `C_last=K_last`.

Declared labels and canonical-function supports are

- `label(C_0)=0`, `supp(C_0)={0,1}`;
- `label(C_1)=1`, `supp(C_1)={1,2}`;
- `label(C_2)=2`, `supp(C_2)={2,3}`;
- `label(C_3)=3`, `supp(C_3)={3,0}`.

The global pair `(Q,P)` is spatially neutral for support bookkeeping.

`closed cycle != spatial topology of the universe`.

## Frozen constraint-frame determinant and known global inverse

Write `C=A(T)K`, with cyclic shear frame `A` defined by the equations above.

The exact determinant target is

`Delta=1-kappa^4 T_0 T_1 T_2 T_3`.

For the frozen representative grid `T_i in {-1,0,1}` and `kappa=0.5`,

`Delta in {15/16, 1, 17/16}`,

so the presented and seed constraint surfaces are algebraically equivalent on the whole positive family.

The exact seed reconstruction is frozen as the known unrestricted Abelianization control:

`K_i = (C_i - a_i C_{i+1} + a_i a_{i+1} C_{i+2} - a_i a_{i+1} a_{i+2} C_{i+3}) / Delta`.

This reconstruction mixes the opposite-site generator `C_{i+2}` and its denominator depends on all four clock variables. Therefore the displayed full seed reconstruction is **not one-step L1** under the frozen Stage 16 locality definition.

This known global reconstruction is a protocol input, not the Stage 16D result.

Crucially:

`known global seed reconstruction != proof that every Abelianization is nonlocal`.

`global Abelianization != physical triviality`.

Stage 16D must still search for alternative locality-preserving Abelianizing bases.

## Frozen distinction among three locality notions

Stage 16 freezes three different notions that must never be silently identified:

1. **canonical-function support** — which site-labelled canonical variables occur in the Poisson-bracket function itself;
2. **closure-coordinate support** — which presented constraints `C_j` occur when an exact first-class bracket is expanded in the `C` basis;
3. **basis-map locality** — whether a change of constraint basis satisfies the frozen L0/L1/Lfinite definition.

A bracket can have canonical-function support contained in the union of its input supports while its exact `C`-basis closure coefficients are cycle-spanning.

`local canonical support != local closure-coordinate support`.

`local closure-coordinate support != locality-preserving basis equivalence`.

These distinctions are frozen before Stage 16A or Stage 16D evidence is evaluated.

## Frozen unsmeared algebra target

Stage 16A must derive, not assume, the complete Poisson algebra.

The protocol preflight target in seed coordinates is

`{C_i,C_{i+1}}=-kappa^2 T_i K_{i+2}`,

with antisymmetric counterparts, while opposite pairs vanish:

`{C_0,C_2}=0`,

`{C_1,C_3}=0`.

In particular,

`{C_0,C_1}=-kappa^2 T_0 K_2`,

`{C_1,C_2}=-kappa^2 T_1 K_3`,

`{C_2,C_3}=-kappa^2 T_2 K_0`,

`{C_3,C_0}=-kappa^2 T_3 K_1`.

Stage 16A must also substitute the exact seed reconstruction and verify exact first-class closure in the presented `C` basis. The resulting closure-coordinate support and coefficient dependence must be reported rather than hidden.

Required checks include:

- exact symbolic Poisson-bracket agreement;
- numerical agreement on every positive and frozen off-surface probe;
- exact first-class reconstruction in the `C` basis;
- independent constraint-gradient and generator-vector rank 4 on the positive family;
- structure coefficient sampling at negative, zero, and positive values;
- off-surface Jacobi identity;
- canonical-function support audit;
- closure-coordinate support audit.

`cyclic first-class closure != hypersurface-deformation algebra`.

`cycle-spanning closure coordinates != physical nonlocality by definition`.

## Frozen smeared generators

For a constant site smearing `N=(N_0,N_1,N_2,N_3)`, define

`C[N]=sum_i N_i C_i`.

The expected seed-coordinate bracket target is

`{C[N],C[M]} = -kappa^2 sum_i (N_i M_{i+1}-N_{i+1} M_i) T_i K_{i+2}`.

Stage 16A/B must derive this directly from canonical Poisson brackets and independently reconstruct it in the presented `C` basis.

Frozen smearings are

- `N_01=(1,-0.5,0,0)`;
- `N_12=(0,1,-0.5,0)`;
- `N_23=(0,0,1,-0.5)`;
- `N_30=(-0.5,0,0,1)`;
- `N_full_A=(1,-0.5,0.25,0.75)`;
- `N_full_B=(-0.25,0.75,1,-0.5)`;
- parallel zero-wedge control `N_parallel=2*N_full_A`.

Positive checks must include all four edge-supported smearings, at least one edge-vs-edge noncommuting case, both full-support smearings, and the exact parallel zero-wedge control.

For finite smeared flows, Stage 16B must exploit the exact affine-linear clock system / matrix exponential when available and compare it with an independent direct ODE or Hamiltonian-vector-field oracle. Numerical integration may not be the sole source of truth.

`finite constant smearing != continuum lapse/shift field`.

## Frozen finite representative family

Carry the four physical Dirac-data classes:

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`.

Interpret each pair as `(Q_D,P_D)`.

Freeze

`T_0,T_1,T_2,T_3 in {-1,0,1}`.

This gives **81 representatives per physical orbit and 324 positive representatives total**.

For each representative set

`P=P_D`,

`pi_i=-c_i P`,

`Q=Q_D+sum_i c_i T_i`.

The target physical quotient is exactly **four classes of 81 representatives**.

Freeze one deterministic off-surface probe per positive representative by shifting

`(pi_0,pi_1,pi_2,pi_3)` by `(0.125,-0.25,0.375,-0.5)` while retaining the other coordinates. These probes are algebra/Jacobi diagnostics only and are not physical-orbit representatives.

`finite four-cycle family != spatial discretization of general relativity`.

## Frozen Dirac and relational observables

Freeze

`P_D=P`,

`Q_D=Q-sum_i c_i T_i`.

Stage 16C must verify strong Poisson commutation with every presented `C_i`, representative independence inside each physical class, and separation of all four classes as a pair.

Freeze the complete four-clock relational observable

`Q(T_0=tau_0,T_1=tau_1,T_2=tau_2,T_3=tau_3)=Q_D+sum_i c_i tau_i`.

It must show nontrivial relational change while descending to the quotient.

Controls must include all four single-clock omissions and raw `Q` as an incomplete/non-descending representative coordinate.

`complete relational observable != ontological becoming by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

## Frozen local finite-flow probes

For local pair probes, freeze step values

`STAGE16_LOCAL_STEP_PAIRS={(0.5,0.5),(-0.5,0.5)}`.

Every positive representative must be tested on every adjacent cycle edge `(0,1)`, `(1,2)`, `(2,3)`, `(3,0)` in both generator orderings. Opposite pairs `(0,2)` and `(1,3)` are commuting controls.

For each adjacent pair Stage 16B must distinguish:

- the raw ordering defect;
- the exact defect predicted in seed-flow coordinates;
- **seed compensation**, which is an algebraic/gauge oracle because the `K` basis is known globally;
- **presented-basis compensation**, which must be constructed only from declared `C_i` flows and reported separately.

Seed compensation may not be relabelled as a locality-preserving presented-basis compensator.

For presented-basis compensation, freeze the candidate word family to all 24 permutations of the four labels `(0,1,2,3)`, with deterministic root solving for four flow parameters. Parameters are bounded to `[-2,2]`, endpoint tolerance is `1e-10`, and solver failure must be reported as a bounded search failure rather than physical path dependence.

Quotient/Dirac equality remains an independent endpoint check.

`raw path-word inequality != physical path dependence`.

`seed-compensated closure != local presented-basis compensation`.

`presented compensator not found in frozen word search != physical obstruction`.

`compensated cycle path closure != refoliation invariance`.

## Frozen locality classes for basis transformations

The graph metric fixes

`N_r(i)={j : dist_C4(i,j)<=r}`.

For the four-cycle,

`N_1(i)={i-1,i,i+1}`,

so the opposite site `i+2` is excluded. This is the minimal cycle for which radius-1 locality remains nontrivial; on a three-cycle every radius-1 neighborhood is global.

A transformed generator carrying label `i` is **L1-locality-preserving** iff all of the following hold:

1. it mixes only original generator labels in `N_1(i)`;
2. every mixing coefficient depends only on canonical variables with site labels in `N_1(i)` plus spatially neutral `(Q,P)`;
3. the map is finite and invertible on every positive representative;
4. after symbolic simplification, the transformed generator has canonical-function support contained in `N_1(i)`;
5. the inverse map satisfies conditions 1–4 with the same labels.

The stricter **L0** subclass permits only same-site generator mixing and same-site coefficient dependence.

The broader **Lfinite** class permits finite compositions of L1 maps. Every success must report the minimal exhibited composition depth and may not be relabelled as one-step L1.

Anything failing L1 is `nonlocal_for_stage16_L1` even if it is algebraically equivalent and preserves the quotient.

`basis locality != physical causal locality`.

`finite graph locality != relativistic microcausality`.

`locality-preserving basis map != gauge transformation`.

## Frozen Stage 16D basis-search family

The conceptual L1 class above is broader than any finite executable search. Stage 16 therefore freezes the executable search separately and forbids a negative search result from being promoted to a universal L1 nonexistence claim.

### Tier 1 — explicit local candidates

Audit identity, L0 diagonal/rescaling controls, all four cyclic Stage-15-style local shears, their reverse-neighbor analogues, and all cyclic rotations.

Elementary shear operations are frozen as

`S(i,dir,sign): row_i <- row_i + sign * a_neighbor * row_neighbor`,

where `dir` is forward or backward, `sign in {-1,+1}`, and the neighbor is in `N_1(i)`.

### Tier 2 — finite L1 compositions

Freeze

`STAGE16_LFINITE_SEARCH_MAX_DEPTH=4`.

Enumerate deterministic compositions of the elementary shears through depth 4, deduplicate algebraically equivalent matrices where practical, and report the minimal depth of every strongly commuting witness found.

Failure through depth 4 means only `no witness in the frozen depth<=4 composition search`.

### Tier 3 — symbolic one-step L1 ansatz

Freeze a **translation-covariant affine L1 ansatz** in which each row mixes `C_{i-1}`, `C_i`, and `C_{i+1}`, and each coefficient is affine in `(1,T_{i-1},T_i,T_{i+1})` with a shared cyclic coefficient template.

Strong commutation equations must be derived symbolically. If an exhaustive algebraic solver can certify the ansatz solution set, the certificate applies only to this frozen affine cyclic ansatz, not to all conceivable L1 maps.

Numerical agreement on sampled probes alone may not be upgraded to `strongly commuting`.

### Tier 4 — unrestricted comparison

Always audit the known global seed reconstruction and at least one unrestricted full-matrix equivalent basis as nonlocal controls.

For every basis candidate report:

- invertibility on all 324 positive representatives;
- L0/L1/Lfinite/nonlocal class;
- one-step inverse locality;
- minimal exhibited Lfinite depth when applicable;
- symbolic strong commutation vs merely first class;
- off-surface bracket residuals;
- physical quotient preservation;
- Dirac-pair preservation;
- complete-relational preservation;
- typed O/P/R/V/Xi preservation once Stage 16E exists.

Frozen Stage 16D classifications are

- `one_step_L1_abelianization_witness_found`;
- `no_L1_witness_in_frozen_search_but_Lfinite_witness_found`;
- `only_nonlocal_abelianization_witness_found_in_frozen_search`;
- `no_local_witness_found_in_declared_search`;
- `basis_search_inconclusive`.

No classification above is a universal theorem of local non-Abelianizability.

`no L1 witness in frozen search != no L1 Abelianization exists`.

`only nonlocal witness found != fundamental physical non-Abelianity`.

## Frozen topology controls

Stage 16F must include topology-specific controls:

1. **wrap-edge opening control** — remove only the `kappa T_3 K_0` term so the carrier becomes a four-site open chain; report how the exhibited Abelianization depth changes without treating this as Stage 15 itself;
2. **three-site projection control** — remove site 3 and recover the Stage 15 open three-site pattern, including its known one-step L1 witness;
3. **three-cycle locality-degeneracy control** — explicitly show that on `C3` every `N_1(i)` contains all sites, so an apparent `L1` result there is not a nontrivial locality test;
4. **disconnected false-positive control** — cut enough edges to create disconnected components and reject cross-component path claims.

`cycle opening changes graph topology != proof that topology is ontic`.

`three-cycle L1 label != nontrivial locality evidence`.

## Frozen typed O/P/R/V/Xi carry-forward

Stage 16E carries

`T_candidate=(O,P,R,V;Xi)`,

with

`R=(R_content,R_direction,R_access)` and

`V=(V_extension,V_semantics,V_weights)`.

No new measurement law is introduced. Carry the previously validated future-measurement / weighted / posterior family and replace only the relational O-events with the four-clock complete observable.

Freeze relational event clock quadruples

`e1=(-1,-1,-1,-1)`,

`e2=(1,1,1,1)`.

Public quotient-level O/P/R/V and future-measurement content must be tested for descent across representatives, licensed local/smeared paths, and every physically equivalent basis candidate admitted by Stage 16D.

Xi may retain cycle orientation, canonical support, closure-coordinate support, path word, compensator type, basis id, locality class, and Lfinite depth. Those provenance fields may not silently enter quotient-level public payloads.

Required guards:

`future-measurement covariance != future actuality`;

`path-independent evidence update != ontological becoming`;

`Potentiality != quantum randomness by definition`;

`typed operational descent != ontological equivalence`.

## Frozen destructive / false-positive controls

Stage 16F must include at least:

- `kappa=0` structure-function removal;
- wrap-edge opening and three-site projection topology controls;
- three-cycle radius-1 locality-degeneracy control;
- disconnected cross-component false-positive path;
- support-expanding generator corruption;
- opposite-site coefficient dependence in an alleged L1 map;
- a fake L1 map whose forward map is local but inverse is not;
- the known global seed reconstruction to ensure it is not silently counted as one-step L1;
- singular-frame control using `kappa=1` and `T_0=T_1=T_2=T_3=1`, for which `Delta=0`;
- wrong smearing sign / antisymmetry corruption;
- Jacobi-violating anomalous term;
- wrong or insufficient local compensator;
- cross-orbit path false positive;
- incomplete four-clock relational observable;
- representative/path/basis/depth-dependent O/P/R/V corruption;
- numerical-only commuting false positive that lacks symbolic certification.

Expected control vocabulary includes

`structure_function_removed_control_rejected`,

`cycle_opening_control_detected`,

`three_cycle_locality_degeneracy_detected`,

`disconnected_component_false_positive_rejected`,

`support_expansion_detected`,

`opposite_site_basis_nonlocal_detected`,

`inverse_nonlocality_detected`,

`global_seed_not_L1_detected`,

`singular_cycle_frame_rejected`,

`smearing_antisymmetry_corruption_detected`,

`constraint_algebra_anomaly_detected`,

`wrong_compensator_rejected`,

`cross_orbit_false_positive_rejected`,

`relational_observable_incomplete`,

`typed_payload_provenance_corruption_detected`,

`numerical_only_commuting_claim_rejected`.

## Frozen Stage 16 sequence

- Stage 16.0 — protocol freeze — **current**;
- Stage 16A — four-site cyclic first-class carrier, exact local/smeared algebra, support audits, and finite representative family;
- Stage 16B — local/smeared/cycle path defects, seed compensation, presented-basis compensation search, and independent flow oracle;
- Stage 16C — Dirac pair, four-clock complete relational observables, physical quotient, reachability, and orbit discrimination;
- Stage 16D — locality-preserving Abelianization pressure test and minimal exhibited locality depth;
- Stage 16E — typed O/P/R/V/Xi and future-measurement descent across cycle quotient, paths, and basis classes;
- Stage 16F — topology-breaking / locality-breaking / anomaly / false-positive controls;
- Stage 16G — executable synthesis and evidence-selected Stage 17 gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

## Frozen Stage 16G synthesis vocabulary

Stage 16G must select exactly one of:

- `closed_cycle_local_path_covariant_L1_abelianizable`;
- `closed_cycle_local_path_covariant_Lfinite_abelianizable`;
- `closed_cycle_local_path_covariant_nonlocal_only_in_declared_search`;
- `closed_cycle_local_path_covariant_basis_inconclusive`;
- `closed_cycle_local_path_partial`;
- `closed_cycle_local_path_obstructed`;
- `inconclusive`.

The `nonlocal_only_in_declared_search` wording is deliberately bounded and must not be rewritten as a universal locality obstruction without a separate completeness result.

## Frozen Stage 17 candidate pool and ranking rubric

Stage 16G must evidence-rank, rather than preselect, the following candidate pool:

- `larger_sparse_graph_locality_scaling_audit`;
- `admissible_basis_transformation_completeness_audit`;
- `path_cycle_tree_topology_comparison_family`;
- `gravitational_minisuperspace_extension`;
- `nonideal_povm_clock_extension`;
- `record_thermodynamic_potentiality_integration`;
- `closed_cycle_carrier_repair_or_reformulation`.

Score each candidate from 0–3 on each frozen axis:

1. discriminating power against the uncertainty actually left by Stage 16A–F;
2. prerequisite readiness from validated evidence;
3. locality/topology specificity where relevant;
4. resistance to metaphysical overinterpretation / confound control;
5. computational and regression tractability.

Maximum score is 15. Ties are broken by higher discriminating-power score, then higher prerequisite-readiness score, then lexical selector id. A repair/reformulation gate may rank first if the carrier/path construction itself fails; gravity or quantum extensions do not receive priority merely for being physically richer.

## Criteria

Stage 16 uses 50 criteria.

### Stage 16.0 — criteria 1–10

1. Stage 15 merged baseline, bounded synthesis, and selected Stage 16 gate recorded.
2. Four-cycle graph, canonical phase space, constants, and spatially neutral global pair frozen.
3. Commuting seed, cyclic shear basis, determinant target, and known global inverse frozen.
4. Canonical-function support, closure-coordinate support, unsmeared/smeared algebra targets, and their distinction frozen.
5. 324-representative positive family, deterministic off-surface probes, and four-class quotient target frozen.
6. Dirac pair, four-clock complete relational observable, local/smeared flow probes, and compensation distinction frozen.
7. L0/L1/Lfinite/nonlocal basis classes and known-global-reconstruction anti-bias rule frozen.
8. Executable Stage 16D basis-search tiers, depth-4 composition cap, bounded negative semantics, and classifications frozen.
9. Typed carry-forward, topology/destructive controls, expected control vocabulary, and interpretation guards frozen.
10. Stage 16A–G sequence, Stage 16G synthesis vocabulary, Stage 17 candidate pool, and ranking rubric frozen.

### Stage 16A — criteria 11–17

11. 324 positive representatives and 324 deterministic off-surface probes implemented exactly.
12. Cyclic frame determinant/inverse and positive-family invertibility independently verified.
13. Constraint-gradient and Hamiltonian-generator rank 4 established on the positive family.
14. Direct unsmeared algebra and negative/zero/positive structure sampling established.
15. Exact `C`-basis first-class reconstruction plus canonical-support / closure-coordinate-support audits established.
16. Direct smeared algebra, delta-smearing recovery, antisymmetry, and declared support cases established.
17. Off-surface Jacobi and Stage 16A documentation/result synchronization established.

### Stage 16B — criteria 18–24

18. Exact local finite flows and independent Hamiltonian-flow oracle established.
19. Adjacent ordering defects match seed-coordinate predictions over the frozen probe family.
20. Seed-compensated closure established and kept distinct from locality-preserving compensation.
21. Presented-`C` compensator word search executed under the frozen 24-word / bounded-parameter rule and classified without overclaim.
22. Exact constant-smeared flow construction and independent oracle established.
23. Smeared ordering defects / compensation and quotient-payload endpoint checks established.
24. Wrong/missing compensator controls and Stage 16B documentation/result synchronization established.

### Stage 16C — criteria 25–31

25. `Q_D,P_D` strong Dirac invariance established.
26. Exactly four quotient classes of 81 representatives established.
27. All six physical-orbit pairs separated by the Dirac pair.
28. Same-orbit reachability / path connectivity checked under the declared presented-generator atlas.
29. Four-clock complete relational observable evaluated exhaustively and nontrivial relational change established.
30. Local/smeared path descent of Dirac and complete-relational content established where licensed.
31. All omitted-clock/raw-coordinate controls rejected and Stage 16C docs synchronized.

### Stage 16D — criteria 32–39

32. Known global seed Abelianization verified and correctly rejected as one-step L1.
33. L0/rescaling candidate family audited.
34. Explicit one-step L1 shear / reverse-neighbor / cyclic-rotation candidate family audited.
35. Translation-covariant affine one-step L1 symbolic ansatz audited with exact strong-commutation equations.
36. Lfinite elementary-shear compositions through depth 4 audited and minimal exhibited depth reported.
37. Strong commutation, first-class closure, invertibility, and off-surface residuals separated correctly.
38. Every equivalent candidate checked for quotient, Dirac, and complete-relational preservation.
39. Stage 16D classification issued with bounded-negative semantics and synchronized documentation/results.

### Stage 16E — criteria 40–44

40. Four-clock typed `(O,P,R,V;Xi)` architecture constructed without introducing a new measurement law.
41. Public O/P/R/V and inherited future-measurement payloads descend to the four physical quotient classes.
42. Licensed local/smeared path descent established while path/compensator provenance remains in Xi.
43. Equivalent basis/locality-depth descent established while basis/depth provenance remains in Xi.
44. Measurement/weighted/posterior/witness completeness and interpretation guards synchronized in tests/docs/results.

### Stage 16F — criteria 45–47

45. Topology/locality controls, including wrap opening, three-site projection, three-cycle degeneracy, disconnected false positives, opposite-site contamination, inverse nonlocality, and singular frame, reject as intended.
46. Algebra/path controls, including `kappa=0`, smearing-sign corruption, Jacobi anomaly, wrong compensation, and numerical-only commuting claims, reject as intended.
47. Cross-orbit, incomplete-relational, typed-provenance corruption controls and the full frozen control vocabulary are validated and synchronized.

### Stage 16G — criteria 48–49

48. Exactly one frozen Stage 16G synthesis classification is selected from validated Stage 16A–F evidence.
49. The Stage 17 candidate pool is scored with the frozen rubric and exactly one next gate is evidence-selected.

### Criterion 50

50. External final full-repository regression / merge-readiness review passes on the documentation-synchronized Stage 16 branch.

At Stage 16.0, criteria **11–50 are pending**.

## Interpretation boundary

Stage 16 is a finite four-site cyclic constraint-algebra precursor. It does **not** establish general relativity, a continuum hypersurface-deformation algebra, spacetime diffeomorphism invariance, refoliation invariance, relativistic locality, spacetime curvature, fundamental non-Abelianity, universal local Abelianizability, universal locality obstruction, eternalism, ontological becoming, absence of becoming, future actuality, or empirical discovery.

Persistent guards:

- `four-site cycle != spatial topology of the universe`;
- `spatially indexed constraint precursor != general relativity`;
- `finite smeared algebra != continuum hypersurface-deformation algebra`;
- `cycle path defect != spacetime curvature`;
- `finite graph locality != relativistic locality`;
- `local canonical support != local closure-coordinate support`;
- `closure-coordinate spreading != physical nonlocality by definition`;
- `known global Abelianization != proof that all Abelianizations are nonlocal`;
- `global Abelianization != physical triviality`;
- `no L1 witness in frozen search != no L1 Abelianization exists`;
- `locality-preserving Abelianization != absence of meaningful local constraint structure`;
- `failure to Abelianize != ontological becoming`;
- `raw path-word inequality != physical path dependence`;
- `presented compensator not found in frozen word search != physical obstruction`;
- `compensated cycle path closure != refoliation invariance`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `future-measurement covariance != future actuality`;
- `typed operational descent != ontological equivalence`;
- `closed-cycle selection != predicted locality obstruction`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
