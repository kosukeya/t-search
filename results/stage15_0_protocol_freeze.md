# Stage 15.0 Results — Spatially Indexed Constraint-Algebra Protocol Freeze

Status: **Stage 15.0 completed; criteria 1–10 satisfied; criteria 11–50 pending.**

## Incoming validated baseline

Stage 14 is completed and merged via PR #15. The carried bounded synthesis is

`structure_function_path_covariant_scalar_obstructed`.

The evidence-selected Stage 15 selector is

`spatially_indexed_constraint_algebra_precursor`.

Frozen gate:

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

No Stage 15A–G scientific result is inferred from this freeze.

## Frozen carrier

The spatial index set is the open three-site chain

`Lambda={0,1,2}`, `0~1~2`.

Canonical variables:

`(Q,P; T_0,pi_0; T_1,pi_1; T_2,pi_2)`.

Constants:

`kappa=0.5`, `c_0=1.0`, `c_1=0.5`, `c_2=-0.25`.

Commuting seed constraints:

`K_i=pi_i+c_i P`.

Frozen positive presented basis:

`C_0=K_0+kappa T_0 K_1`,

`C_1=K_1+kappa T_1 K_2`,

`C_2=K_2`.

Frozen supports:

`supp(C_0)={0,1}`, `supp(C_1)={1,2}`, `supp(C_2)={2}`.

The global pair `(Q,P)` is spatially neutral for Stage 15 support bookkeeping.

## Frozen local/smeared targets

The protocol target is

`{C_0,C_1}=-kappa^2 T_0 C_2`,

`{C_0,C_2}=0`,

`{C_1,C_2}=0`,

with antisymmetric counterparts.

For smearings `N,M`,

`C[N]=sum_i N_i C_i`

and Stage 15A/B must derive the smeared algebra directly from Poisson brackets, recover the local brackets from delta smearings, and check antisymmetry, Jacobi, and support.

## Protocol preflight only

Before closing the freeze, the displayed symbolic definitions were algebraically checked for internal consistency:

- direct symbolic evaluation gives `{C_0,C_1}=-kappa^2 T_0 C_2`;
- the other independent brackets vanish;
- the unsmeared Jacobiator vanishes identically;
- for `kappa=0.5`, `T_0 in {-1,0,1}`, the sampled structure-function coefficient `-kappa^2 T_0` takes `0.25`, `0`, and `-0.25`;
- the triangular constraint matrix has determinant one;
- the displayed inverse reconstruction of `K_i` is algebraically exact.

These checks establish only that the frozen protocol is non-contradictory at the displayed algebraic level.

`protocol preflight != Stage 15A scientific evidence`.

Stage 15A must independently implement and test the carrier over the full frozen positive family.

## Frozen representative family and quotient target

Carry four Dirac-data classes:

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`.

Freeze `T_0,T_1,T_2 in {-1,0,1}`: **27 representatives per orbit, 108 total**.

For `(Q_D,P_D)` set

`P=P_D`,

`pi_i=-c_i P`,

`Q=Q_D+sum_i c_i T_i`.

The target quotient is exactly four classes of 27 representatives.

Frozen invariants and complete relational observable:

`P_D=P`,

`Q_D=Q-sum_i c_i T_i`,

`Q(T_0=tau_0,T_1=tau_1,T_2=tau_2)=Q_D+c_0 tau_0+c_1 tau_1+c_2 tau_2`.

## Frozen locality-preserving basis class

Stage 15 fixes graph neighborhoods `N_r(i)` before basis-search results are known.

A one-step **L1** map and its inverse must each:

- mix the generator labelled `i` only with labels in `N_1(i)`;
- use coefficients depending only on variables in `N_1(i)` plus the spatially neutral `(Q,P)`;
- remain finite and invertible on every positive representative;
- simplify to support contained in `N_1(i)`.

**L0** is the same-site subclass.

**Lfinite** permits a finite composition of L1 maps but must retain/report composition depth.

Anything failing L1 is `nonlocal_for_stage15_L1` even if algebraically equivalent.

This locality definition is now frozen and must not be weakened or enlarged in response to Stage 15D results.

## Frozen known Abelianization control

The seed basis satisfies

`K_2=C_2`,

`K_1=C_1-kappa T_1 C_2`,

`K_0=C_0-kappa T_0 C_1+kappa^2 T_0 T_1 C_2`.

The `K_0` row contains the distance-2 generator `C_2`, so the full displayed reconstruction is not automatically licensed as a one-step L1 map.

Crucially:

`known distance-2 seed reconstruction != proof that every Abelianization is nonlocal`.

Stage 15D must search for alternative L0/L1 Abelianizations under the frozen definition.

This removes the principal post-hoc freedom exposed by Stage 14: locality cannot be redefined after the basis result is seen.

## Frozen controls

Required Stage 15F controls include structure-function removal, site deletion/disconnection, disconnected-site false-positive paths, support expansion, distance-2 contamination of an alleged L1 map, singular/noninvertible basis maps, smearing-sign corruption, Jacobi anomaly, cross-orbit paths, incomplete relational observables, O/P/R/V corruption, and explicit classification of the known distance-2 Abelianizing reconstruction.

## Frozen sequence

- Stage 15.0 — protocol freeze — **completed**;
- Stage 15A — local/smeared first-class carrier and finite representative family — **next**;
- Stage 15B — local/smeared path closure, Jacobi, and compensated paths;
- Stage 15C — Dirac / complete relational observables, quotient, and orbit discrimination;
- Stage 15D — locality-preserving basis pressure test;
- Stage 15E — typed O/P/R/V/Xi and future-measurement descent;
- Stage 15F — locality-breaking / anomaly / false-positive controls;
- Stage 15G — executable synthesis and evidence-selected Stage 16 gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

## Frozen synthesis vocabulary

Stage 15G must select exactly one of:

- `spatial_local_path_covariant_local_abelianizable`;
- `spatial_local_path_covariant_locality_obstructed`;
- `spatial_local_path_covariant_basis_inconclusive`;
- `spatial_local_path_partial`;
- `spatial_local_path_obstructed`;
- `inconclusive`.

## Criterion closure

Criteria **1–10** are satisfied by the freeze.

Criteria **11–50** remain pending.

## Interpretation boundary

Stage 15.0 establishes only the research protocol. It does not establish local path covariance, locality-protected non-Abelianity, general relativity, the continuum hypersurface-deformation algebra, spacetime diffeomorphism invariance, refoliation invariance, relativistic locality, eternalism, ontological becoming, absence of becoming, future actuality, or empirical discovery.

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
- `protocol preflight != Stage 15A scientific evidence`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
