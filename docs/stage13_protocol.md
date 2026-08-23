# Stage 13 Protocol — Multi-Constraint Constraint-Algebra / Refoliation Precursor

Status: **Stage 13.0 completed; criteria 1–10 satisfied; criteria 11–50 pending.**

Selected Stage 13 gate from Stage 12G:

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

Stage 12 is merged into `main` at `ee4baec55fa994217b275f9f2451e25fc6736787`.

The final pre-merge Stage 12 current-head regression was run #1654 with **`1025 passed in 693.84s (0:11:33)`**.

The bounded Stage 12 synthesis carried forward is

`Stage 12 finite typed multi-orbit gauge status = multi_orbit_gauge_covariant`.

The retained finite-model candidate is

`T12_candidate=(O,P,R,V;Xi)`

with

`R=(R_content,R_direction,R_access)`

and

`V=(V_extension,V_semantics,V_weights)`.

Stage 13 changes the constraint-generated path structure. It does not assume that the new finite model is a model of general relativity.

`multi_orbit_gauge_covariant finite family != general covariance`.

`constraint-algebra/refoliation precursor != refoliation invariance`.

`constraint-algebra/refoliation precursor != general relativity`.

## 1. Frozen scientific question

Stage 13 asks whether the Stage 12 physical-orbit quotient, complete relational observables, and typed O/P/R/V measurement content remain well defined when one-dimensional constraint-generated gauge flow is replaced by a two-dimensional first-class gauge distribution with nontrivial path ordering.

The central positive question is not whether two raw gauge transports commute.

Instead, Stage 13 tests whether order-dependent raw paths satisfy the frozen first-class algebra and can be related by the algebraically required compensating gauge parameter so that licensed corresponding endpoints carry the same quotient-level physical content.

Frozen distinction:

`raw gauge-path commutativity != successful multi-constraint closure`.

Positive target:

`noncommuting raw path order + correct algebraic compensator -> same licensed gauge endpoint / same quotient-level physical content`.

No Stage 13 path-covariance or refoliation result is established by this protocol freeze.

## 2. Frozen phase space and two-constraint carrier

Canonical phase-space coordinates are

`(T,p_T; X,p_X; q,p)`

with canonical brackets

`{T,p_T}=1`, `{X,p_X}=1`, `{q,p}=1`

and all other elementary brackets zero.

The positive Stage 13 constraint pair is frozen as

`K_T = p_T + p^2/2 approx 0`,

`K_X = exp(T) (p_X + a p) approx 0`,

with

`a = 0.5`.

On the positive constraint surface,

`p_T = -p^2/2`,

`p_X = -a p`.

The two constraints satisfy

`{K_T,K_X} = -K_X`.

Thus the pair is first-class on the declared finite model and the two generator directions are nontrivially related.

Stage 13A must also verify that the two constraint gradients / Hamiltonian generator directions are independent on every declared positive representative; merely duplicating one constraint under another name does not satisfy the protocol.

`two constraint labels != two independent gauge directions`.

`first-class closure on this toy carrier != hypersurface-deformation algebra`.

## 3. Frozen generator flows

The `K_T` Hamiltonian flow, with parameter `s`, is frozen as

`dT/ds = 1`,

`dq/ds = p`,

`dX/ds = 0`,

`dp/ds = 0`,

`dp_X/ds = 0`,

`dp_T/ds = 0`.

The `K_X` Hamiltonian flow, with parameter `u`, is frozen on the positive constraint surface as

`dX/du = exp(T)`,

`dq/du = a exp(T)`,

`dT/du = 0`,

`dp/du = 0`,

`dp_X/du = 0`,

`dp_T/du = 0` on `K_X=0`.

Typed transport names:

- `Phi_T(s)` — `K_T`-generated gauge transport;
- `Phi_X(u)` — `K_X`-generated gauge transport.

The generator identity is part of Xi/provenance and is not itself quotient-level physical content.

`constraint-generator identity != physical-event identity`.

`constraint-generator identity != internal-clock perspective`.

## 4. Frozen noncommuting path law and compensator

For a source representative with clock coordinate `T0`, a mixed target changes both `T` and `X`.

Let

`s = T1 - T0`,

`DeltaX = X1 - X0`.

For the path that applies `Phi_T(s)` first and then `Phi_X`, the required second parameter is

`u_TX = DeltaX / exp(T1)`.

For the path that applies `Phi_X` first and then `Phi_T(s)`, the required first parameter is

`u_XT = DeltaX / exp(T0)`.

The frozen compensator law is therefore

`u_XT = exp(s) u_TX`.

For mixed paths with `s != 0` and `DeltaX != 0`, using the same raw `u` in both orders is expected to produce different raw endpoints.

This order dependence is positive evidence for the nontrivial presentation, not a failure.

The positive closure test is

`Phi_X(u_TX) after Phi_T(s)`

versus

`Phi_T(s) after Phi_X(u_XT)`

with `u_XT = exp(s) u_TX`.

The two compensated paths must land on the same declared representative within tolerance and must agree on all quotient-level physical payloads tested in later substages.

`same raw generator parameters under reordered paths != corresponding gauge path`.

`wrong compensator failure != physical time asymmetry`.

## 5. Frozen Dirac data and complete relational observable

The Stage 13 Dirac-type invariant pair is frozen as

`P_D = p`,

`Q_D = q - p T - a X`.

Stage 13 must verify independently from sampled representatives that

`{P_D,K_T}=0`, `{P_D,K_X}=0`,

`{Q_D,K_T}=0`, `{Q_D,K_X}=0`

on the declared positive family.

The complete relational observable is frozen as

`q(T=tau,X=chi) = Q_D + P_D tau + a chi`.

The one-clock expression

`q(T=tau; X raw) = Q_D + P_D tau + a X`

is deliberately not treated as a complete observable because it retains the second gauge coordinate `X`.

Stage 13C must include a control in which fixing `T=tau` alone while varying the licensed `K_X` representative changes the one-clock value. That control is expected to be classified as incomplete rather than as a failure of the two-clock relational construction.

`one clock condition in a two-gauge-direction model != complete relational observable`.

`complete relational observable != ontological becoming by definition`.

## 6. Frozen physical-orbit family and representative grid

Stage 13 retains the Stage 12 four physical initial-data classes in `(Q_D,P_D)`:

- `omega_alpha: (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta: (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma: (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta: (Q_D,P_D)=(0.20,1.75)`.

This preserves the same-P/different-Q and same-Q/different-P anti-triviality controls while changing only the gauge-distribution structure.

The canonical positive representative grid per physical orbit is frozen as

`T in {-1.0,0.0,1.0}`

and

`X in {-1.0,0.0,1.0}`.

For each `(T,X)` pair,

`p = P_D`,

`q = Q_D + P_D T + a X`,

`p_T = -P_D^2/2`,

`p_X = -a P_D`.

This gives

- **9 representatives per physical orbit**;
- **36 representatives total**;
- **288 ordered nonidentity same-orbit source/target pairs**;
- **144 ordered mixed pairs** for which both `T` and `X` change.

The 144 mixed pairs are the canonical positive family for noncommuting-order / compensator tests.

`different physical orbit != different path through one gauge orbit`.

`different path word != different physical orbit`.

## 7. Frozen quotient and path-word semantics

Stage 13D must build the multi-constraint gauge quotient from typed generator/path connectivity, not by directly grouping stored `orbit_id` labels.

A path word may contain `Phi_T` and `Phi_X` segments. The path word and its raw parameters belong to representation/provenance metadata.

The intended physical quotient remains exactly four classes, each containing the nine representatives associated with one canonical `(Q_D,P_D)` pair.

A successful quotient must establish both

`different licensed path words -> same quotient class when they connect the same physical orbit`,

and

`different physical Dirac data -> not collapsed merely by multi-constraint gauge connectivity`.

`path-word history != quotient-level physical state`.

`quotient path equivalence != temporal-history identity`.

## 8. Frozen constraint-basis control

The same positive constraint surface admits the rescaled second constraint

`K_X_tilde = exp(-T) K_X = p_X + a p`.

For the pair `(K_T,K_X_tilde)`,

`{K_T,K_X_tilde}=0`.

On the constraint surface, the rescaling changes the generator parameterization but preserves the gauge distribution.

Stage 13F must therefore compare the noncommuting presentation `(K_T,K_X)` with the commuting presentation `(K_T,K_X_tilde)` and require agreement of the physical quotient, Dirac data, and declared complete relational / operational payloads after typed correspondence.

This is a central anti-overinterpretation control.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`commuting equivalent basis != absence of the gauge redundancy represented by the original basis`.

`constraint-basis change != physical-orbit change`.

## 9. Frozen anomaly / failure controls

The negative family must include at least the following controls.

### Wrong path semantics

- reorder `Phi_T` and `Phi_X` while incorrectly reusing the same raw `u`;
- use a deliberately wrong compensator instead of `u_XT=exp(s)u_TX`;
- falsely treat raw path-word equality as necessary for physical equivalence;
- falsely treat different path words as distinct physical time histories.

### Incomplete relational typing

- treat `q(T=tau;X raw)` as a complete observable;
- drop the `X` correspondence while claiming two-clock equality;
- identify gauge coordinate `X` with modal continuation identity or with ontological becoming.

### Degenerate anti-triviality carriers

- `a=0`, which decouples `q` from the second gauge direction and cannot establish the intended two-clock relational coupling;
- a commuting-limit presentation used as if it independently established the nontrivial path-order target;
- duplicate / rank-deficient constraint directions.

### Broken first-class closure

A deliberately anomalous deformation is frozen as

`K_X_bad = exp(T)(p_X + a p) + epsilon q`

with nonzero `epsilon` chosen in Stage 13F.

Its bracket with `K_T` is generically not weakly zero on the declared `K_T=K_X_bad=0` surface. It must therefore be rejected as a positive first-class carrier.

Expected classification vocabulary includes

- `compensated_path_closure_established`;
- `wrong_compensator_detected`;
- `same_raw_parameter_reorder_false_positive_rejected`;
- `one_clock_observable_incomplete`;
- `rank_deficient_constraint_control_rejected`;
- `constraint_algebra_anomaly_detected`;
- `basis_presentation_equivalent`;
- `cross_orbit_path_rejected`;
- `representative_dependent_payload_corruption_detected`.

`broken first-class closure != ontological becoming`.

`path-order mismatch != arrow of time by definition`.

## 10. Frozen Stage 12 O/P/R/V/Xi and measurement carry-over

Stage 13 reuses rather than redesigns

`T12_candidate=(O,P,R,V;Xi)`.

The inherited physical/modal/measurement vocabulary remains:

- `R=(R_content,R_direction,R_access)`;
- `V=(V_extension,V_semantics,V_weights)`;
- `QExt(e1)={h_L,h_R}`;
- prediction anchor `e1` and measurement target `e2`;
- outcomes `future_signature_left` and `future_signature_other`;
- continuation-specific normalization/effect typing;
- class/weight alignment;
- matched epistemic and ontic-extension public interfaces;
- hidden-selector nonleakage.

Stage 13E isolates the new multi-constraint path question by fixing the inherited external parameterization to `identity` and the inherited internal measurement chart to `A/e2`, unless an executable reason discovered in Stage 13A–D requires a protocol amendment.

Xi is extended with representation metadata for

- constraint-generator identity;
- path word;
- raw path parameters;
- compensator provenance;
- source/target representative;
- constraint-basis identity.

Those fields must not leak into quotient-level physical content merely because they are available in Xi.

The orbit-sensitive diagnostic witness must depend on Dirac/complete-relational data rather than on raw path parameters.

`path-specific Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

`typed bridge to relational data != dynamical derivation of quantum measurement from the constraints`.

## 11. Frozen Stage 13 sequence

- Stage 13.0 — protocol freeze — **completed**;
- Stage 13A — two-constraint first-class carrier and finite representative family — **next**;
- Stage 13B — noncommuting gauge paths and compensated closure — pending;
- Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — pending;
- Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — pending;
- Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — pending;
- Stage 13F — basis / ablation / anomaly / false-positive controls — pending;
- Stage 13G — executable synthesis and evidence-selected next gate — pending;
- criterion 50 — external final full-repository regression / merge-readiness review — pending.

## 12. Frozen synthesis vocabulary

Stage 13G must select exactly one of:

- `multi_constraint_path_covariant`;
- `multi_constraint_path_partial`;
- `multi_constraint_path_obstructed`;
- `inconclusive`.

`multi_constraint_path_obstructed` is reserved for an explicit failure of the positive family, not for a deliberately anomalous or wrong-compensator control behaving correctly.

Stage 13G must evidence-select the next gate without presupposing GR. The live candidate pool includes at least:

- a phase-space-dependent structure-function / hypersurface-deformation precursor;
- a gravitational/minisuperspace extension;
- a richer causal/order layer;
- nonideal/POVM clocks.

## 13. Exit criteria

### Criteria 1–10 — Stage 13.0

1. Exact Stage 12G-selected Stage 13 gate and merged Stage 12 baseline are frozen — **satisfied**.
2. Stage 12 bounded synthesis/candidate is carried forward without promotion to general covariance or GR — **satisfied**.
3. Canonical six-dimensional phase space and two independent constraint roles are frozen — **satisfied**.
4. Positive pair `K_T`, `K_X`, first-class bracket `{K_T,K_X}=-K_X`, and finite generator flows are frozen — **satisfied**.
5. Noncommuting path-order semantics and exact compensator law `u_XT=exp(s)u_TX` are frozen — **satisfied**.
6. Dirac pair `Q_D,P_D`, two-clock complete relational observable, and one-clock incompleteness control are frozen — **satisfied**.
7. Four physical orbits, 3x3 representative grid, quotient/path-word target, and anti-collapse rules are frozen — **satisfied**.
8. Equivalent commuting constraint-basis control and non-Abelian-presentation guard are frozen — **satisfied**.
9. O/P/R/V/Xi carry-over, anomaly/false-positive controls, synthesis vocabulary, and interpretation guards are frozen — **satisfied**.
10. Stage 13A–G sequence and criteria 11–50 allocation are frozen — **satisfied**.

### Criteria 11–16 — Stage 13A

11. All 36 canonical representatives satisfy both positive constraints within tolerance — **pending**.
12. The two constraint gradients / generator directions are independent over the declared positive family — **pending**.
13. Numerical/symbolic evaluation confirms `{K_T,K_X}=-K_X` on the declared carrier — **pending**.
14. `Phi_T` and `Phi_X` individually preserve the two-constraint surface on licensed paths — **pending**.
15. The four Stage 12 physical initial-data classes are represented without accidental collapse — **pending**.
16. Generator, representative, orbit, event, clock, and basis provenance remain separately typed — **pending**.

### Criteria 17–23 — Stage 13B

17. All 144 mixed ordered source/target pairs exhibit the declared nontrivial two-generator path structure — **pending**.
18. Same-raw-`u` reordered mixed paths are detectably different when the protocol predicts they should be — **pending**.
19. The exact compensator `u_XT=exp(s)u_TX` maps the two canonical path orders to the same target within tolerance — **pending**.
20. Compensated path closure preserves both constraints and the declared physical-orbit identity — **pending**.
21. Wrong-compensator paths are numerically detected — **pending**.
22. Path-order / generator-order metadata remains distinct from physical temporal order — **pending**.
23. Cross-orbit path construction is rejected rather than compensated into false equivalence — **pending**.

### Criteria 24–31 — Stage 13C

24. `Q_D=q-pT-aX` and `P_D=p` are independently reconstructed from all 36 representatives — **pending**.
25. Same-orbit representatives agree in the full Dirac pair — **pending**.
26. All six canonical different-orbit pairs remain physically distinct under the full Dirac pair — **pending**.
27. `q(T=tau,X=chi)=Q_D+P_D tau+a chi` is reconstructed across the declared finite family — **pending**.
28. Complete relational values agree across compensated path choices leading to corresponding gauge representatives — **pending**.
29. Fixing `T=tau` alone is explicitly shown insufficient under variation of the second gauge coordinate — **pending**.
30. Same-P/different-Q and same-Q/different-P anti-triviality controls remain explicit — **pending**.
31. Complete-relational change is not promoted to ontological becoming or eternalism — **pending**.

### Criteria 32–38 — Stage 13D

32. Typed nodes distinguish physical orbit, representative, generator/basis, path word, event, clock, and modal roles — **pending**.
33. The multi-constraint atlas is built from typed `Phi_T` / `Phi_X` connectivity rather than stored orbit labels — **pending**.
34. The quotient recovers exactly four physical classes of nine representatives each — **pending**.
35. Different compensated path words to corresponding representatives descend to the same quotient-level Dirac/relational payload — **pending**.
36. Distinct physical Dirac data are not collapsed by path connectivity — **pending**.
37. Path-word / compensator removal is classified separately from numerical reconstructibility — **pending**.
38. Path word is not identified with modal continuation or physical temporal history — **pending**.

### Criteria 39–43 — Stage 13E

39. O/P/R/V/Xi architecture is lifted over every canonical Stage 13 representative with path/basis provenance confined to Xi — **pending**.
40. Licensed compensated path choices preserve quotient-level typed O/P/R/V content — **pending**.
41. Inherited future-measurement payloads descend across compensated multi-constraint path choices — **pending**.
42. An orbit-sensitive operational witness based on Dirac/complete-relational data remains representative/path independent within an orbit while preserving physical-orbit discrimination — **pending**.
43. Wrong path/event/class/outcome/normalization or representative-dependent O/P/R/V/measurement payloads are rejected — **pending**.

### Criteria 44–47 — Stage 13F

44. Noncommuting and equivalent commuting constraint presentations are compared and shown not to change licensed quotient-level physical content when typed correspondence is correct — **pending**.
45. Rank-deficient, decoupled, wrong-compensator, one-clock-incomplete, and cross-orbit false positives are explicitly classified — **pending**.
46. `K_X_bad` or an equivalent deliberately non-first-class deformation is detected as a constraint-algebra anomaly rather than admitted as a positive carrier — **pending**.
47. Basis/path/anomaly results are not promoted to fundamental non-Abelianity, refoliation invariance, GR, eternalism, or ontological becoming — **pending**.

### Criteria 48–49 — Stage 13G

48. Executable synthesis selects exactly one frozen Stage 13 status from the full Stage 13A–F evidence chain — **pending**.
49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, or a hypersurface-deformation algebra — **pending**.

### Criterion 50 — external repository validation

50. External final full-repository regression and merge-readiness review — **pending**.

## 14. Interpretation guards

- `raw gauge-path commutativity != successful multi-constraint closure`;
- `noncommuting constraint presentation != fundamental physical non-Abelianity`;
- `constraint-basis change != physical-orbit change`;
- `first-class closure on this finite model != hypersurface-deformation algebra`;
- `multi-constraint path covariance != refoliation invariance`;
- `refoliation precursor != general covariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `path word != physical temporal history`;
- `path-order mismatch != arrow of time by definition`;
- `wrong compensator failure != physical time asymmetry`;
- `one clock condition in a two-gauge-direction model != complete relational observable`;
- `complete relational observable != ontological becoming by definition`;
- `different physical orbit != later event on one orbit`;
- `constraint-generated gauge flow != ontological becoming`;
- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `path-specific Xi provenance != quotient-level physical content`;
- `basis-specific Xi provenance != quotient-level physical content`;
- `typed bridge to relational data != dynamical derivation of quantum measurement from the constraints`;
- `future-measurement covariance != future actuality`;
- `broken first-class closure != ontological becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
