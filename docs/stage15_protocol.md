# Stage 15 Protocol — Spatially Indexed Constraint-Algebra Precursor

Status: **Stage 15.0 protocol freeze in progress; criteria 1–10 are assigned to the freeze and criteria 11–50 remain unavailable until later substages.**

## Incoming validated baseline

Stage 14 is completed and merged via PR #15. The validated Stage 14 synthesis is

`structure_function_path_covariant_scalar_obstructed`.

The evidence-selected Stage 15 selector is

`spatially_indexed_constraint_algebra_precursor`.

Frozen gate:

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

Stage 14 established a diagonal scalar-rescaling obstruction on its finite carrier but also exhibited an equivalent determinant-one triangular commuting presentation. Stage 15 therefore asks a narrower question: **does adding an explicit spatial index and a predeclared locality criterion constrain that basis equivalence?**

No Stage 15 locality-protected non-Abelianity result is established by this protocol.

## Frozen spatial carrier

Use the open three-site path graph

`Lambda={0,1,2}`, with edges `0~1` and `1~2`.

Canonical phase space:

`(Q,P; T_i,pi_i; q_i,p_i)`, for `i in Lambda`.

Poisson brackets are canonical and all undeclared cross-site brackets vanish.

Constants:

`kappa=0.5`, `b=0.5`, and

`c_0=1.0`, `c_1=0.5`, `c_2=-0.25`.

Define

`D_i = p_i`,

`A_0 = b + kappa T_0`,

`A_i = b + kappa(T_i + q_{i-1})` for `i=1,2`,

and local Hamiltonian-like constraints

`H_i = pi_i + c_i P + A_i D_i`.

Declared support:

- `supp(D_i)={i}`;
- `supp(H_0)={0}`;
- `supp(H_1)={0,1}`;
- `supp(H_2)={1,2}`.

This support declaration is part of the protocol and must not be changed after Stage 15A results are known.

## Frozen local algebra target

Stage 15A must verify symbolically and numerically on the declared finite family that the positive carrier is first class and spatially local.

Target unsmeared relations include

`{D_i,D_j}=0`,

`{H_i,D_j}=kappa delta_{j,i-1} D_i` for `i>0`, with all other `H_i-D_j` brackets zero,

and nearest-neighbor

`{H_i,H_{i+1}} = -kappa A_i D_{i+1}` for `i=0,1`,

with `H_0-H_2` bracket zero.

The coefficient `A_i` is phase-space dependent and must take at least one negative, one zero, and one positive value somewhere in the frozen finite family. With the frozen sample and `b=kappa=0.5`, the attainable coefficient set is `{-0.5,0,0.5,1.0,1.5}`.

The positive locality criterion is not merely first-class closure: the bracket of compactly supported generators must close within the union of their supports enlarged by at most one graph edge.

`spatial indexing != continuum field theory`.

`nearest-neighbor closure != hypersurface-deformation algebra`.

`phase-space-dependent local structure function != spacetime geometry`.

## Frozen smeared generators

For site smearings `N=(N_0,N_1,N_2)` and `M=(M_0,M_1,M_2)`, define

`H[N] = sum_i N_i H_i`,

`D[M] = sum_i M_i D_i`.

Stage 15A/B must derive the smeared bracket directly from the unsmeared Poisson algebra rather than hard-code the expected answer.

The derived result must be expressible as a linear combination of the same local `D_i` generators with phase-space-dependent coefficients. Smearing dependence must be antisymmetric under `N <-> M` for the `H-H` bracket.

Required positive checks include:

- local-to-smeared consistency;
- smeared-to-local recovery using Kronecker-delta smearings;
- off-constraint-surface Jacobi checks;
- support propagation no larger than one graph edge beyond the input support union;
- exact agreement between symbolic and direct Poisson-bracket evaluation on all sampled representatives.

`finite smeared algebra != continuum distributional algebra`.

## Frozen finite representative family

Physical Dirac-data classes are carried from Stage 14 as

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`.

Interpret these as `(Q_D,P_D)` values.

Freeze three clock-coordinate triples

- `tau_A=(-1,0,1)`;
- `tau_B=(0,1,-1)`;
- `tau_C=(1,-1,0)`;

and three local-gauge triples

- `rho_A=(0,-1,1)`;
- `rho_B=(1,0,-1)`;
- `rho_C=(-1,1,0)`.

Use the Cartesian product of these two triple sets: **9 representatives per physical orbit, 36 positive representatives total**.

For each representative set

`P=P_D`,

`p_i=0`,

`pi_i=-c_i P`,

`T_i=tau_i`,

`q_i=rho_i`,

`Q=Q_D + sum_i c_i T_i`.

The target physical quotient is exactly **four classes of nine representatives**.

The finite family is a diagnostic sample, not a discretization of physical space.

## Frozen Dirac and relational observables

Freeze

`P_D=P`,

`Q_D=Q-sum_i c_i T_i`.

Stage 15C must verify that both are invariant under every licensed local constraint flow on the positive family and that the pair separates all four physical classes.

Complete relational observable:

`Q(T_0=tau_0,T_1=tau_1,T_2=tau_2)=Q_D + c_0 tau_0 + c_1 tau_1 + c_2 tau_2`.

The observable must show nontrivial relational change while remaining quotient-compatible.

Controls must include omission of one clock condition and use of a raw gauge coordinate where a complete relational condition is required.

`complete spatially indexed relational observable != ontological becoming by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

## Frozen locality notion

The declared graph metric on `Lambda` fixes neighborhoods

`N_r(i)={j : dist(i,j)<=r}`.

A basis map is **L1-locality-preserving** only if all of the following hold:

1. each transformed generator labelled by site `i` mixes only generators labelled by sites in `N_1(i)`;
2. every coefficient multiplying those generators depends only on canonical variables whose site labels lie in `N_1(i)` plus the global Dirac pair `(Q,P)`;
3. the map is finite and invertible on every positive representative;
4. the transformed generator support, after explicit symbolic simplification, is contained in `N_1(supp(original generator))`;
5. the inverse map satisfies the same four conditions.

This definition is frozen **before** Stage 15D basis results are evaluated.

A map violating any one condition is classified `nonlocal_for_stage15_L1`, even if it preserves the finite quotient.

A stricter ultralocal subclass `L0` allows only same-site generator mixing and same-site coefficient dependence. A broader audit class `Lfinite` allows a composition of finitely many L1 maps, but Stage 15D must report the required composition depth and may not silently relabel an `Lfinite` success as an `L1` success.

`locality-preserving basis map != gauge transformation`.

`basis locality != physical causal locality`.

`finite graph locality != relativistic microcausality`.

## Frozen basis pressure test

Stage 15D must test, without changing the locality definition, whether the Stage 14 style triangular Abelianization persists.

The following classes must be audited separately:

- diagonal scalar rescalings;
- `L0` triangular `H-D` mixing;
- general invertible `L1` mixing;
- broader `Lfinite` compositions;
- deliberately nonlocal full-matrix mixing as a control.

For every candidate basis, Stage 15D must report:

- invertibility;
- locality class (`L0`, `L1`, `Lfinite`, or nonlocal);
- unsmeared closure;
- smeared closure;
- whether the transformed algebra is strongly commuting or only first class;
- physical quotient preservation;
- Dirac-pair preservation;
- complete-relational preservation;
- typed O/P/R/V/Xi preservation when Stage 15E is available.

No candidate basis may be declared physically preferred solely because it is commuting.

Possible Stage 15D classifications are frozen as:

- `local_abelianization_persists`;
- `L1_obstructed_but_Lfinite_abelianizable`;
- `only_nonlocal_abelianization_found`;
- `no_abelianization_found_in_declared_search`;
- `basis_audit_inconclusive`.

`L1 obstruction != universal non-Abelianizability`.

`only-nonlocal Abelianization found != fundamental physical non-Abelianity`.

`local Abelianization != absence of meaningful local constraint structure`.

## Frozen local/smeared path tests

Stage 15B must construct licensed finite local flows generated by individual `H_i`, `D_i`, and smeared combinations.

Positive comparisons must include:

- same-orbit path pairs using different local-generator orderings;
- compactly supported smearings on `{0,1}` and `{1,2}`;
- at least one full-support smearing;
- exact or numerically controlled compensators where the algebra requires them;
- endpoint equality at the quotient/relational level rather than raw path-word equality.

`raw local path-word inequality != physical path dependence`.

`compensated local-path closure != refoliation invariance`.

## Frozen typed O/P/R/V/Xi carry-forward

Stage 15E carries the typed architecture

`T_candidate=(O,P,R,V;Xi)`,

with

`R=(R_content,R_direction,R_access)` and

`V=(V_extension,V_semantics,V_weights)`.

The Stage 15 requirement is descent/compatibility across the spatially indexed quotient, licensed local/smeared paths, and basis choices classified in Stage 15D.

No new ontological semantics may be assigned to O/P/R/V merely because spatial indexing is present.

Required guards remain:

`future-measurement covariance != future actuality`;

`path-independent evidence update != ontological becoming`;

`Potentiality != quantum randomness by definition`;

`typed operational descent != ontological equivalence`.

## Frozen controls

Stage 15F must include at least:

- structure-function removal (`kappa=0`);
- deletion of a spatial site;
- disconnected-site false-positive path;
- support-expanding generator corruption;
- coefficient dependence on a distance-2 site;
- singular basis map;
- noninvertible local mixing;
- wrong smearing sign / antisymmetry corruption;
- Jacobi-violating anomalous term;
- cross-orbit path false positive;
- incomplete relational observable;
- representative/path/basis-dependent O/P/R/V payload corruption;
- a deliberately nonlocal Abelianizing map, if one is available, to ensure the classifier distinguishes algebraic equivalence from L1 locality.

Expected control vocabulary includes

`structure_function_removed_control_rejected`,

`disconnected_site_false_positive_rejected`,

`support_expansion_detected`,

`distance2_coefficient_nonlocal_detected`,

`singular_basis_map_rejected`,

`smearing_antisymmetry_corruption_detected`,

`constraint_algebra_anomaly_detected`,

`cross_orbit_false_positive_rejected`,

`relational_observable_incomplete`,

`representative_dependent_payload_corruption_detected`.

## Frozen Stage 15 sequence

- Stage 15.0 — protocol freeze — **current**;
- Stage 15A — local/smeared first-class carrier and finite representative family;
- Stage 15B — local/smeared path closure, Jacobi, and compensated-path checks;
- Stage 15C — Dirac / complete relational observables, physical quotient, and orbit discrimination;
- Stage 15D — locality-preserving basis pressure test;
- Stage 15E — typed O/P/R/V/Xi and future-measurement descent across local/smeared paths and basis classes;
- Stage 15F — locality-breaking / anomaly / false-positive controls;
- Stage 15G — executable synthesis and evidence-selected Stage 16 gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

## Frozen Stage 15G synthesis vocabulary

Stage 15G must select exactly one of:

- `spatial_local_path_covariant_local_abelianizable`;
- `spatial_local_path_covariant_locality_obstructed`;
- `spatial_local_path_covariant_basis_inconclusive`;
- `spatial_local_path_partial`;
- `spatial_local_path_obstructed`;
- `inconclusive`.

The selector must rank the next gate from evidence accumulated through Stage 15A–F rather than preserving a pre-Stage-15 philosophical preference.

## Criteria

Stage 15 uses 50 criteria.

### Stage 15.0 — criteria 1–10

1. Stage 14 merged baseline and Stage 15 selected gate recorded.
2. Spatial graph/sites and canonical phase space frozen.
3. Local constraints and declared supports frozen.
4. Local and smeared closure targets frozen.
5. Finite representative family and four-class quotient target frozen.
6. Dirac and complete-relational observables frozen.
7. `L0`, `L1`, `Lfinite`, and nonlocal basis classes frozen before results.
8. Basis-audit reporting requirements and classifications frozen.
9. Required negative controls and interpretation guards frozen.
10. Stage 15A–G sequence and synthesis vocabulary frozen.

### Stage 15A–G and criterion 50 — criteria 11–50

Criteria 11–49 are assigned monotonically across Stage 15A–G and may be marked satisfied only by executable evidence and synchronized notes/results. Criterion 50 remains an external final full-repository regression / merge-readiness review.

At Stage 15.0, criteria **11–50 are pending**.

## Interpretation boundary

Stage 15 is a finite spatially indexed constraint-algebra precursor. It does **not** establish general relativity, the continuum hypersurface-deformation algebra, spacetime diffeomorphism invariance, refoliation invariance, relativistic locality, fundamental non-Abelianity, eternalism, ontological becoming, absence of becoming, future actuality, or empirical discovery.

Guards:

- `spatially indexed constraint precursor != general relativity`;
- `local/smeared precursor != spacetime diffeomorphism invariance by definition`;
- `nearest-neighbor graph locality != relativistic locality`;
- `finite smeared algebra != continuum hypersurface-deformation algebra`;
- `phase-space-dependent local structure functions != spacetime geometry by definition`;
- `locality-preserving Abelianization != physical triviality`;
- `locality obstruction in the declared basis class != universal non-Abelianizability`;
- `constraint-basis change != physical-orbit change`;
- `raw path-word inequality != physical path dependence`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `future-measurement covariance != future actuality`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
