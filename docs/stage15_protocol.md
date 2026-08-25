# Stage 15 Protocol — Spatially Indexed Constraint-Algebra Precursor

Status: **Stage 15.0 protocol freeze in progress; criteria 1–10 are assigned to the freeze and criteria 11–50 remain pending.**

## Incoming validated baseline

Stage 14 is completed and merged via PR #15. Its validated synthesis is

`structure_function_path_covariant_scalar_obstructed`.

The evidence-selected Stage 15 selector is

`spatially_indexed_constraint_algebra_precursor`.

Frozen gate:

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

Stage 14 obstructed the frozen diagonal scalar-rescaling class but admitted a determinant-one triangular commuting presentation. Stage 15 therefore asks whether an explicit spatial support structure restricts that basis equivalence.

No Stage 15 locality-protected non-Abelianity result is established by this freeze.

## Frozen spatial carrier

Use the open three-site path graph

`Lambda={0,1,2}`, with edges `0~1` and `1~2`.

Canonical phase space:

`(Q,P; T_0,pi_0; T_1,pi_1; T_2,pi_2)`.

Canonical Poisson brackets are

`{Q,P}=1`, `{T_i,pi_j}=delta_ij`,

with all undeclared brackets zero.

Constants:

`kappa=0.5`,

`c_0=1.0`, `c_1=0.5`, `c_2=-0.25`.

Define the commuting seed constraints

`K_i = pi_i + c_i P`.

The **positive presented basis** is frozen as the nearest-neighbor triangular frame

`C_0 = K_0 + kappa T_0 K_1`,

`C_1 = K_1 + kappa T_1 K_2`,

`C_2 = K_2`.

Declared site labels and supports are

- `label(C_0)=0`, `supp(C_0)={0,1}`;
- `label(C_1)=1`, `supp(C_1)={1,2}`;
- `label(C_2)=2`, `supp(C_2)={2}`.

The global pair `(Q,P)` is spatially neutral for support bookkeeping. This convention is frozen before Stage 15D.

## Frozen local algebra target

Stage 15A must derive, not assume, the complete unsmeared algebra. The required target is

`{C_0,C_1} = -kappa^2 T_0 C_2`,

`{C_0,C_2}=0`,

`{C_1,C_2}=0`,

plus antisymmetric counterparts.

The structure function `-kappa^2 T_0` must sample negative, zero, and positive values on the frozen family.

Required positive checks:

- exact symbolic Poisson-bracket agreement;
- direct numerical agreement on every positive representative;
- first-class closure both on and off the constraint surface;
- off-surface Jacobi identity;
- no bracket support outside the union of the input supports.

`spatial indexing != continuum field theory`.

`nearest-neighbor first-class closure != hypersurface-deformation algebra`.

`phase-space-dependent local structure function != spacetime geometry`.

## Frozen smeared generators

For a site smearing `N=(N_0,N_1,N_2)`, define

`C[N] = sum_i N_i C_i`.

Stage 15A/B must derive `{C[N],C[M]}` from the direct Poisson bracket. It must agree with the unsmeared algebra and be antisymmetric under `N <-> M`.

For the frozen carrier the derived expression is expected to be representable in the original local basis with support no larger than the support union of the two smearings. The implementation must derive this expression rather than insert it as a special case.

Required checks include:

- local-to-smeared consistency;
- smeared-to-local recovery using Kronecker-delta smearings;
- compact support on `{0,1}` and `{1,2}`;
- at least one full-support smearing;
- symbolic/direct numerical equality;
- antisymmetry and Jacobi checks.

`finite smeared algebra != continuum distributional algebra`.

## Frozen finite representative family

Carry the Stage 14 physical Dirac-data classes:

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`.

Interpret these as `(Q_D,P_D)`.

Freeze

`T_0,T_1,T_2 in {-1,0,1}`.

This gives **27 representatives per physical orbit and 108 positive representatives total**.

For each representative set

`P=P_D`,

`pi_i=-c_i P`,

`Q=Q_D + sum_i c_i T_i`.

Because the triangular constraint matrix has determinant one, `C_i=0` is equivalent to `K_i=0` on the whole carrier.

The target physical quotient is exactly **four classes of 27 representatives**.

The finite site graph is a diagnostic precursor, not a spatial discretization of general relativity.

## Frozen Dirac and relational observables

Freeze

`P_D=P`,

`Q_D=Q-sum_i c_i T_i`.

Stage 15C must verify that both Poisson-commute with every `C_i`, remain representative-independent inside each physical class, and separate all four physical classes as a pair.

Complete relational observable:

`Q(T_0=tau_0,T_1=tau_1,T_2=tau_2)=Q_D+c_0 tau_0+c_1 tau_1+c_2 tau_2`.

It must show nontrivial relational change while descending to the quotient.

Controls must include omission of one clock condition and use of a raw representative coordinate as though it were a complete relational observable.

`complete spatially indexed relational observable != ontological becoming by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

## Frozen locality classes for basis transformations

The graph metric fixes

`N_r(i)={j : dist(i,j)<=r}`.

A transformed generator carrying label `i` is classified relative to that label. A basis map is **L1-locality-preserving** iff all of the following hold:

1. the transformed generator labelled `i` mixes only original generators labelled in `N_1(i)`;
2. every mixing coefficient depends only on canonical variables with site labels in `N_1(i)` plus the spatially neutral global pair `(Q,P)`;
3. the map is finite and invertible on every positive representative;
4. after symbolic simplification, the transformed generator has support contained in `N_1(i)`;
5. the inverse map satisfies conditions 1–4 with the same labels.

The stricter **L0** subclass permits only same-site mixing and same-site coefficient dependence.

The broader audit class **Lfinite** permits a finite composition of L1 maps. Any Lfinite success must report the minimal composition depth found and may not be relabelled as a one-step L1 success.

Any map failing the L1 conditions is `nonlocal_for_stage15_L1` even if it preserves the constraint surface and quotient.

These classes are frozen before any Stage 15D search result is evaluated.

`basis locality != physical causal locality`.

`finite graph locality != relativistic microcausality`.

`locality-preserving basis map != gauge transformation`.

## Frozen known Abelianizing comparison and anti-bias rule

The commuting seed basis is reconstructible algebraically:

`K_2=C_2`,

`K_1=C_1-kappa T_1 C_2`,

`K_0=C_0-kappa T_0 C_1+kappa^2 T_0 T_1 C_2`.

This map is an explicit **known algebraic Abelianization control**. Its `K_0` row contains the distance-2 generator `C_2`, so under the frozen one-step definition the full map is **not automatically licensed as L1**.

This fact is a protocol input, not the Stage 15D result.

Stage 15D must still search for **other** invertible Abelianizing bases in the declared L0/L1 classes. Failure of the displayed seed reconstruction to be L1 does not prove that no different L1 Abelianization exists.

Conversely, the implementation may not enlarge L1 after seeing a negative result merely to admit the known seed reconstruction.

This is the central anti-bias rule of Stage 15.

## Frozen basis pressure test

Stage 15D must audit separately:

- diagonal scalar rescalings;
- L0 triangular/general mixing;
- general invertible L1 mixing;
- Lfinite compositions;
- the known seed reconstruction above;
- deliberately unrestricted full-matrix mixing as a nonlocal control.

For every candidate basis report:

- invertibility;
- locality class (`L0`, `L1`, `Lfinite`, or nonlocal);
- unsmeared closure;
- smeared closure;
- strongly commuting vs merely first class;
- physical quotient preservation;
- Dirac-pair preservation;
- complete-relational preservation;
- typed O/P/R/V/Xi preservation once Stage 15E exists.

Frozen Stage 15D classifications:

- `local_abelianization_persists`;
- `L1_obstructed_but_Lfinite_abelianizable`;
- `only_nonlocal_abelianization_found`;
- `no_abelianization_found_in_declared_search`;
- `basis_audit_inconclusive`.

`known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal`.

`L1 obstruction != universal non-Abelianizability`.

`only-nonlocal Abelianization found != fundamental physical non-Abelianity`.

`local Abelianization != absence of meaningful local constraint structure`.

## Frozen local/smeared path tests

Stage 15B must construct finite flows generated by individual `C_i` and declared smeared combinations.

Positive comparisons must include:

- same-orbit path pairs with different local-generator orderings;
- compactly supported smearings on `{0,1}` and `{1,2}`;
- a full-support smearing;
- exact or numerically controlled compensators where required;
- quotient/relational endpoint comparison rather than raw path-word equality.

`raw local path-word inequality != physical path dependence`.

`compensated local-path closure != refoliation invariance`.

## Frozen typed O/P/R/V/Xi carry-forward

Stage 15E carries

`T_candidate=(O,P,R,V;Xi)`,

with

`R=(R_content,R_direction,R_access)` and

`V=(V_extension,V_semantics,V_weights)`.

The requirement is typed descent/compatibility across the spatially indexed quotient, licensed local/smeared paths, and basis classes established by Stage 15D.

No new ontological semantics are assigned merely because the carrier has spatial labels.

Required guards:

`future-measurement covariance != future actuality`;

`path-independent evidence update != ontological becoming`;

`Potentiality != quantum randomness by definition`;

`typed operational descent != ontological equivalence`.

## Frozen controls

Stage 15F must include at least:

- structure-function removal (`kappa=0`);
- deletion/disconnection of a site;
- disconnected-site false-positive path;
- support-expanding generator corruption;
- distance-2 coefficient dependence in an alleged L1 map;
- singular/noninvertible basis map;
- wrong smearing sign / antisymmetry corruption;
- Jacobi-violating anomalous term;
- cross-orbit path false positive;
- incomplete relational observable;
- representative/path/basis-dependent O/P/R/V corruption;
- the known distance-2 seed reconstruction to ensure algebraic Abelianization is not silently counted as one-step L1.

Expected control vocabulary includes

`structure_function_removed_control_rejected`,

`disconnected_site_false_positive_rejected`,

`support_expansion_detected`,

`distance2_basis_nonlocal_detected`,

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

The next gate must be evidence-selected from Stage 15A–F rather than chosen to preserve a prior metaphysical preference.

## Criteria

Stage 15 uses 50 criteria.

### Stage 15.0 — criteria 1–10

1. Stage 14 merged baseline and selected Stage 15 gate recorded.
2. Three-site graph, canonical phase space, and spatially neutral global pair frozen.
3. Commuting seed and nearest-neighbor presented constraint basis frozen.
4. Unsmeared/smeared first-class targets and support rules frozen.
5. 108-representative positive family and four-class quotient target frozen.
6. Dirac pair and complete relational observable frozen.
7. L0/L1/Lfinite/nonlocal basis classes frozen before Stage 15D evidence.
8. Known distance-2 Abelianizing control and anti-bias rule frozen.
9. Required controls and interpretation guards frozen.
10. Stage 15A–G sequence and Stage 15G synthesis vocabulary frozen.

### Stage 15A–G and criterion 50 — criteria 11–50

Criteria 11–49 are assigned monotonically across Stage 15A–G and may be satisfied only by executable evidence plus synchronized notes/results. Criterion 50 remains an external final full-repository regression / merge-readiness review.

At Stage 15.0, criteria **11–50 are pending**.

## Interpretation boundary

Stage 15 is a finite spatially indexed constraint-algebra precursor. It does **not** establish general relativity, a continuum hypersurface-deformation algebra, spacetime diffeomorphism invariance, refoliation invariance, relativistic locality, fundamental non-Abelianity, eternalism, ontological becoming, absence of becoming, future actuality, or empirical discovery.

Guards:

- `spatially indexed constraint precursor != general relativity`;
- `local/smeared precursor != spacetime diffeomorphism invariance by definition`;
- `nearest-neighbor graph locality != relativistic locality`;
- `finite smeared algebra != continuum hypersurface-deformation algebra`;
- `phase-space-dependent local structure functions != spacetime geometry by definition`;
- `known nonlocal Abelianization != proof of locality-protected non-Abelianity`;
- `locality-preserving Abelianization != physical triviality`;
- `locality obstruction in the declared basis class != universal non-Abelianizability`;
- `constraint-basis change != physical-orbit change`;
- `raw path-word inequality != physical path dependence`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `future-measurement covariance != future actuality`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
