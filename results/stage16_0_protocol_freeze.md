# Stage 16.0 Results — Four-Site Closed-Cycle Protocol Freeze

Status: **Stage 16.0 completed; criteria 1–10 satisfied; criteria 11–50 pending.**

## Incoming validated baseline

Stage 15 is completed and merged via PR #16 at

`cca49e37b3d4171ea74fd6c15fa119fcd4392e2d`.

The carried bounded synthesis is

`spatial_local_path_covariant_local_abelianizable`.

The evidence-selected Stage 16 selector is

`four_site_closed_cycle_constraint_algebra_precursor`.

Frozen gate:

> **Construct a minimal four-site closed-cycle spatially indexed first-class constraint-algebra precursor with no terminal seed generator, retain explicit local/smeared structure-function dependence, test whether one-step L1 or finite-depth locality-preserving Abelianization still exists, and retest compensated paths, the physical quotient, complete relational observables, and typed O/P/R/V/Xi descent without assuming general relativity or refoliation invariance.**

No Stage 16A–G scientific result is inferred from this freeze.

## Frozen carrier

The spatial index graph is

`Lambda=C4={0,1,2,3}`, `0~1~2~3~0`.

Canonical variables:

`(Q,P; T_0,pi_0; T_1,pi_1; T_2,pi_2; T_3,pi_3)`.

Constants:

`kappa=0.5`, `c_0=1.0`, `c_1=0.5`, `c_2=-0.25`, `c_3=0.75`.

Commuting seed constraints:

`K_i=pi_i+c_i P`.

With `a_i=kappa T_i`, freeze the cyclic presented basis

`C_i = K_i + a_i K_{i+1 mod 4}`.

Explicitly,

`C_0=K_0+kappa T_0 K_1`,

`C_1=K_1+kappa T_1 K_2`,

`C_2=K_2+kappa T_2 K_3`,

`C_3=K_3+kappa T_3 K_0`.

Every presented generator has nearest-neighbor canonical-function support, and there is no terminal `C_i=K_i` seed.

## Protocol preflight only

The displayed definitions were checked algebraically before freezing the protocol.

The cyclic frame determinant is

`Delta=1-kappa^4 T_0 T_1 T_2 T_3`.

For `kappa=0.5` and `T_i in {-1,0,1}`,

`Delta in {15/16, 1, 17/16}`,

so the frame is invertible at all 324 positive representatives.

The exact global seed reconstruction is

`K_i = (C_i - a_i C_{i+1} + a_i a_{i+1} C_{i+2} - a_i a_{i+1} a_{i+2} C_{i+3}) / Delta`.

The independent unsmeared Poisson brackets reduce to

`{C_0,C_1}=-kappa^2 T_0 K_2`,

`{C_1,C_2}=-kappa^2 T_1 K_3`,

`{C_2,C_3}=-kappa^2 T_2 K_0`,

`{C_3,C_0}=-kappa^2 T_3 K_1`,

with `{C_0,C_2}=0`, `{C_1,C_3}=0` and antisymmetric counterparts.

All four independent three-generator Jacobiators vanish identically under the canonical Poisson bracket.

These checks establish only that the frozen formulas are internally non-contradictory.

`protocol preflight != Stage 16A scientific evidence`.

Stage 16A must independently implement and exhaustively validate the carrier on the full positive/off-surface family.

## Frozen support distinctions

Three different locality notions are frozen:

- canonical-function support;
- closure-coordinate support in the exact presented `C` basis;
- basis-map locality under L0/L1/Lfinite.

The adjacent bracket has canonical-function support inside the union of the two input supports, but replacing `K_{i+2}` with the exact cyclic inverse can require cycle-spanning `C`-basis coordinates and the global denominator `Delta`.

Therefore:

`local canonical support != local closure-coordinate support`.

This distinction is part of the protocol rather than a Stage 16A outcome.

## Frozen representative family and quotient target

Carry four Dirac-data classes:

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`.

Freeze `T_0,T_1,T_2,T_3 in {-1,0,1}`: **81 representatives per physical orbit and 324 positive representatives total**.

For `(Q_D,P_D)` set

`P=P_D`,

`pi_i=-c_i P`,

`Q=Q_D+sum_i c_i T_i`.

The target quotient is exactly **four classes of 81 representatives**.

One deterministic off-surface probe per positive representative shifts `(pi_0,pi_1,pi_2,pi_3)` by `(0.125,-0.25,0.375,-0.5)`.

Frozen Dirac data and relational observable:

`P_D=P`,

`Q_D=Q-sum_i c_i T_i`,

`Q(T_0=tau_0,T_1=tau_1,T_2=tau_2,T_3=tau_3)=Q_D+sum_i c_i tau_i`.

## Frozen local/smeared path program

Local step pairs are frozen as

`STAGE16_LOCAL_STEP_PAIRS={(0.5,0.5),(-0.5,0.5)}`.

Every positive representative will be checked on the four adjacent cycle edges in both orderings, with opposite pairs as commuting controls.

Stage 16B must distinguish raw ordering defects, exact seed-coordinate predictions, seed compensation as a global algebraic oracle, and locality-sensitive compensation constructed from presented `C_i` flows.

The presented compensator search is frozen to all 24 permutations of `(0,1,2,3)`, four flow parameters in `[-2,2]`, and endpoint tolerance `1e-10`.

Failure of this bounded word search is not physical path dependence.

Frozen constant smearings include all four edge-supported vectors, two full-support vectors, and the exact parallel zero-wedge control defined in `docs/stage16_protocol.md`.

## Frozen locality and Abelianization audit

For the four-cycle,

`N_1(i)={i-1,i,i+1}`,

so the opposite site is excluded.

A one-step L1 map and inverse must each mix only `N_1(i)`, use only `N_1(i)`-labelled coefficient dependence plus neutral `(Q,P)`, remain finite/invertible on all positive representatives, and simplify to canonical-function support inside `N_1(i)`.

**L0** is the same-site subclass.

**Lfinite** is a finite composition of L1 maps and must report minimal exhibited depth.

Anything else is `nonlocal_for_stage16_L1`.

The known exact seed reconstruction contains `C_{i+2}` and the all-clock denominator `Delta`, so it is a frozen **global/non-L1 Abelianization control**.

`known global seed reconstruction != proof that every Abelianization is nonlocal`.

The executable search is frozen in four tiers:

1. explicit L0/local shear candidates and cyclic rotations;
2. elementary L1 shear compositions through `STAGE16_LFINITE_SEARCH_MAX_DEPTH=4`;
3. a translation-covariant affine L1 ansatz with coefficients affine in `(1,T_{i-1},T_i,T_{i+1})`;
4. known global/unrestricted comparison bases.

Negative search results remain bounded to the declared search.

`no L1 witness in frozen search != no L1 Abelianization exists`.

Frozen Stage 16D classifications:

- `one_step_L1_abelianization_witness_found`;
- `no_L1_witness_in_frozen_search_but_Lfinite_witness_found`;
- `only_nonlocal_abelianization_witness_found_in_frozen_search`;
- `no_local_witness_found_in_declared_search`;
- `basis_search_inconclusive`.

## Frozen topology and destructive controls

Stage 16F must include:

- wrap-edge opening control;
- three-site projection recovering the Stage 15 open-chain pattern;
- three-cycle radius-1 locality-degeneracy control;
- disconnected cross-component false-positive control;
- `kappa=0` structure-function removal;
- support expansion and opposite-site L1 contamination;
- forward-local/inverse-nonlocal fake basis;
- known global seed map misclassification control;
- singular frame at `kappa=1`, all `T_i=1`, where `Delta=0`;
- smearing-sign corruption and Jacobi anomaly;
- wrong/missing compensation;
- cross-orbit false paths;
- incomplete relational observables;
- representative/path/basis/depth-dependent O/P/R/V corruption;
- numerical-only commuting false positive without symbolic certification.

The expected control vocabulary is frozen in the protocol.

## Frozen typed carry-forward

Carry

`T_candidate=(O,P,R,V;Xi)`,

`R=(R_content,R_direction,R_access)`,

`V=(V_extension,V_semantics,V_weights)`.

No new measurement law is introduced.

The four-clock relational events are frozen at

`e1=(-1,-1,-1,-1)` and `e2=(1,1,1,1)`.

Cycle/path/basis/depth provenance remains in Xi and may not silently enter quotient-level public O/P/R/V or inherited future-measurement payloads.

## Frozen sequence

- Stage 16.0 — protocol freeze — **completed**;
- Stage 16A — four-site cyclic first-class carrier, local/smeared algebra, support audits, and finite representative family — **next**;
- Stage 16B — local/smeared/cycle path defects and compensation audits;
- Stage 16C — Dirac / four-clock complete relational observables / quotient / reachability;
- Stage 16D — locality-preserving Abelianization pressure test and minimal exhibited locality depth;
- Stage 16E — typed O/P/R/V/Xi and future-measurement descent;
- Stage 16F — topology/locality/anomaly/false-positive controls;
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

The bounded `nonlocal_only_in_declared_search` wording may not be promoted to a universal obstruction without separate completeness evidence.

## Frozen Stage 17 ranking pool

The frozen candidate pool is

- `larger_sparse_graph_locality_scaling_audit`;
- `admissible_basis_transformation_completeness_audit`;
- `path_cycle_tree_topology_comparison_family`;
- `gravitational_minisuperspace_extension`;
- `nonideal_povm_clock_extension`;
- `record_thermodynamic_potentiality_integration`;
- `closed_cycle_carrier_repair_or_reformulation`.

Each is scored 0–3 on five frozen axes: discriminating power, prerequisite readiness, locality/topology specificity, confound/overinterpretation resistance, and computational/regression tractability. Maximum 15; tie-breaks are discriminating power, prerequisite readiness, then lexical selector id.

## Criterion closure

Criteria **1–10** are satisfied by the freeze.

Criteria **11–50** remain pending.

## Interpretation boundary

Stage 16.0 establishes only the research protocol. It does not establish local path covariance, local Abelianization persistence, locality obstruction, general relativity, continuum hypersurface deformations, spacetime curvature, refoliation invariance, relativistic locality, eternalism, ontological becoming, absence of becoming, future actuality, or empirical discovery.

Guards:

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
- `failure to Abelianize != ontological becoming`;
- `raw path-word inequality != physical path dependence`;
- `presented compensator not found in frozen word search != physical obstruction`;
- `compensated cycle path closure != refoliation invariance`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `future-measurement covariance != future actuality`;
- `typed operational descent != ontological equivalence`;
- `closed-cycle selection != predicted locality obstruction`;
- `protocol preflight != Stage 16A scientific evidence`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
