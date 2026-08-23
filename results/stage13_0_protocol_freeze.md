# Stage 13.0 Results — Multi-Constraint Constraint-Algebra / Refoliation Precursor Protocol Freeze

Status: **Stage 13.0 completed; criteria 1–10 satisfied; criteria 11–50 pending.**

## Selected gate carried from Stage 12G

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

Stage 12 is merged into `main` at `ee4baec55fa994217b275f9f2451e25fc6736787`.

The final pre-merge Stage 12 current-head regression was run #1654 with **`1025 passed in 693.84s (0:11:33)`**.

The carried bounded Stage 12 synthesis is

`multi_orbit_gauge_covariant`.

No Stage 13 multi-constraint path-covariance result is established by this freeze.

## Frozen positive carrier

Canonical phase space:

`(T,p_T; X,p_X; q,p)`.

Positive constraints:

`K_T = p_T + p^2/2 approx 0`,

`K_X = exp(T)(p_X + 0.5 p) approx 0`.

Frozen first-class relation:

`{K_T,K_X} = -K_X`.

The model therefore has two independently typed, nontrivially related constraint-generated directions. Stage 13A must still verify independence and numerical closure on the declared finite representative family.

`two constraint labels != two independent gauge directions`.

`first-class closure on this toy carrier != hypersurface-deformation algebra`.

## Frozen path-order target

The two positive transport types are

- `Phi_T(s)`;
- `Phi_X(u)`.

For a source `(T0,X0)` and mixed target `(T1,X1)`, define

`s=T1-T0`,

`DeltaX=X1-X0`,

`u_TX=DeltaX/exp(T1)`,

`u_XT=DeltaX/exp(T0)`.

The exact compensator relation is

`u_XT = exp(s) u_TX`.

The protocol explicitly expects that reordering the two generator flows while naively keeping the same raw `u` will generally change the raw endpoint.

That is not the failure condition.

The positive condition is compensated closure:

`Phi_X(u_TX) after Phi_T(s)`

and

`Phi_T(s) after Phi_X(u_XT)`

must reach the same licensed endpoint and later descend to the same quotient-level physical payload.

`raw gauge-path commutativity != successful multi-constraint closure`.

`same raw generator parameters under reordered paths != corresponding gauge path`.

## Frozen Dirac and relational structure

Dirac-type data:

`P_D=p`,

`Q_D=q-pT-0.5X`.

Complete relational observable:

`q(T=tau,X=chi)=Q_D+P_D tau+0.5 chi`.

The deliberately incomplete one-clock expression is

`q(T=tau;X raw)=Q_D+P_D tau+0.5X`.

Stage 13C must show explicitly that fixing only `T` leaves second-direction gauge dependence, while the two-clock observable descends across licensed representatives.

`one clock condition in a two-gauge-direction model != complete relational observable`.

## Frozen physical-orbit / representative family

The Stage 12 four physical classes are retained:

- `omega_alpha=(-0.35,1.25)`;
- `omega_beta=(0.40,1.25)`;
- `omega_gamma=(-0.35,0.75)`;
- `omega_delta=(0.20,1.75)`;

in `(Q_D,P_D)`.

Canonical representative grid:

`T in {-1.0,0.0,1.0}`,

`X in {-1.0,0.0,1.0}`.

This freezes:

- **9 representatives per orbit**;
- **36 representatives total**;
- **288 ordered nonidentity same-orbit source/target pairs**;
- **144 ordered mixed pairs** with both `T` and `X` changed.

The 144 mixed pairs are the canonical Stage 13B compensated-path family.

The target quotient remains exactly four physical classes of nine representatives each.

`different path word != different physical orbit`.

`path-word history != quotient-level physical state`.

## Frozen constraint-basis control

Equivalent rescaled presentation:

`K_X_tilde = exp(-T)K_X = p_X + 0.5p`.

Its bracket is

`{K_T,K_X_tilde}=0`.

The noncommuting and commuting presentations must be compared in Stage 13F. Correctly typed basis correspondence must preserve the physical quotient, Dirac data, complete relational observables, and declared operational payloads.

This prevents the project from treating the noncommuting presentation itself as physically fundamental.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-basis change != physical-orbit change`.

## Frozen anomaly / false-positive family

Required controls include:

- same-raw-`u` reordered path falsely called corresponding;
- wrong compensator;
- path word falsely treated as physical temporal history;
- cross-orbit path falsely treated as gauge-related;
- one-clock observable falsely called complete;
- missing `X` correspondence;
- rank-deficient / duplicate constraint directions;
- `a=0` decoupled second direction used as an anti-triviality control;
- equivalent commuting basis misread as refuting the original gauge distribution;
- representative/path-dependent O/P/R/V or measurement corruption;
- deliberately non-first-class deformation
  `K_X_bad=exp(T)(p_X+0.5p)+epsilon q`.

Expected statuses include

`compensated_path_closure_established`,

`wrong_compensator_detected`,

`same_raw_parameter_reorder_false_positive_rejected`,

`one_clock_observable_incomplete`,

`constraint_algebra_anomaly_detected`,

`basis_presentation_equivalent`,

`cross_orbit_path_rejected`,

`representative_dependent_payload_corruption_detected`.

## Frozen O/P/R/V/Xi carry-over

The retained candidate is

`T12_candidate=(O,P,R,V;Xi)`

with

`R=(R_content,R_direction,R_access)`

and

`V=(V_extension,V_semantics,V_weights)`.

Stage 13E isolates the new constraint-path question at inherited external parameterization `identity` and inherited internal measurement chart `A/e2` unless an executable protocol amendment is later justified.

Xi gains path/basis provenance fields, including generator identity, path word, raw parameters, compensator, representative source/target, and basis identity.

Those representation fields are not automatically physical content.

`path-specific Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

## Frozen Stage 13 sequence

- Stage 13.0 — protocol freeze — **completed**;
- Stage 13A — two-constraint first-class carrier and finite representative family — **next**;
- Stage 13B — noncommuting gauge paths and compensated closure;
- Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination;
- Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent;
- Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices;
- Stage 13F — basis / ablation / anomaly / false-positive controls;
- Stage 13G — executable synthesis and evidence-selected next gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

## Frozen synthesis vocabulary

Stage 13G will select exactly one of:

- `multi_constraint_path_covariant`;
- `multi_constraint_path_partial`;
- `multi_constraint_path_obstructed`;
- `inconclusive`.

A deliberately anomalous carrier or wrong-compensator control behaving correctly does not by itself license `multi_constraint_path_obstructed`; that status is reserved for positive-family failure.

## Criterion closure

Criteria **1–10** are satisfied by the protocol freeze.

Criteria **11–50** remain pending and are not inferred from the protocol alone.

## Interpretation boundary

Stage 13.0 establishes only a research protocol. It does not establish multi-constraint path covariance, refoliation invariance, general covariance, a hypersurface-deformation algebra, general relativity, fundamental physical non-Abelianity, future actuality, eternalism, ontological becoming, absence of becoming, or empirical discovery.

Guards:

- `raw gauge-path commutativity != successful multi-constraint closure`;
- `noncommuting constraint presentation != fundamental physical non-Abelianity`;
- `first-class closure on this finite model != hypersurface-deformation algebra`;
- `multi-constraint path covariance != refoliation invariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `path word != physical temporal history`;
- `path-order mismatch != arrow of time by definition`;
- `one clock condition in a two-gauge-direction model != complete relational observable`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `finite-model success != empirical discovery`;
- `not_established != false`.
