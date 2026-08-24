# Stage 13 Protocol — Multi-Constraint Constraint-Algebra / Refoliation Precursor

Status: **Stage 13D completed; criteria 1–38 satisfied; criteria 39–50 pending.**

## 1. Incoming baseline and selected gate

Stages 1–12 are historical and merged. Stage 12 was merged via PR #13 into `main` at `ee4baec55fa994217b275f9f2451e25fc6736787`. Final pre-merge Stage 12 current-head run #1654 passed **`1025 passed in 693.84s (0:11:33)`**.

Stage 12G selected `multi_orbit_gauge_covariant` on its frozen finite family and selected the following Stage 13 gate:

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

The Stage 12 candidate carried forward is

`T12_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

Stage 13 does not promote Stage 12 to general covariance, diffeomorphism invariance, refoliation invariance, a hypersurface-deformation algebra, or general relativity.

## 2. Frozen carrier and constraint roles

Canonical phase space:

`(T,p_T; X,p_X; q,p)`.

Frozen positive constraints:

`K_T = p_T + p^2/2 approx 0`,

`K_X = exp(T) (p_X + a p) approx 0`,

with

`a = 0.5`,

and first-class bracket

`{K_T,K_X} = -K_X`.

The positive finite Hamiltonian flows are typed separately:

`Phi_T(s)` with `dT/ds = 1` and `dq/ds = p`,

`Phi_X(u)` with `dX/du = exp(T)` and `dq/du = a exp(T)`.

`two constraint labels != two independent gauge directions`.

`first-class closure on this toy carrier != hypersurface-deformation algebra`.

## 3. Frozen physical-orbit family

The four Stage 12-carried physical Dirac-data controls are

- `omega_alpha : (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta : (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma : (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta : (Q_D,P_D)=(0.20,1.75)`.

The representative grid is

`T,X in {-1,0,1}`,

giving **9 representatives per physical orbit**, **36 representatives total**, **288 ordered nonidentity same-orbit source/target pairs**, and **144 ordered mixed pairs** with both gauge coordinates changed.

`path-word history != quotient-level physical state`.

## 4. Frozen compensated mixed-path semantics

For a mixed same-orbit source/target pair,

`s = T1 - T0`,

`DeltaX = X1 - X0`,

`u_TX = DeltaX / exp(T1)`,

`u_XT = DeltaX / exp(T0)`,

with exact compensator law

`u_XT = exp(s) u_TX`.

The two canonical path words are

`path_word_TX=(Phi_T,Phi_X)`

and

`path_word_XT=(Phi_X,Phi_T)`.

Frozen classifications include

- `compensated_path_closure_established`;
- `wrong_compensator_detected`;
- `same_raw_parameter_reorder_false_positive_rejected`;
- `cross_orbit_path_rejected`.

`raw gauge-path commutativity != successful multi-constraint closure`.

`same raw generator parameters under reordered paths != corresponding gauge path`.

`wrong compensator failure != physical time asymmetry`.

## 5. Frozen Dirac and relational structure

The two-constraint Dirac pair is

`P_D = p`,

`Q_D = q - p T - a X`.

The two-clock complete relational observable is

`q(T=tau,X=chi) = Q_D + P_D tau + a chi`.

The explicit one-clock incompleteness control is

`q(T=tau; X raw) = Q_D + P_D tau + a X`.

Frozen classifications include

- `full_dirac_pair_orbit_discrimination_established`;
- `compensated_path_complete_relational_covariance_established`;
- `one_clock_observable_incomplete`.

`one clock condition in a two-gauge-direction model != complete relational observable`.

`complete relational observable != ontological becoming by definition`.

## 6. Equivalent basis and anomaly controls

The equivalent commuting presentation reserved for Stage 13F is

`K_X_tilde = exp(-T) K_X = p_X + a p`,

with

`{K_T,K_X_tilde}=0`.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-basis change != physical-orbit change`.

The deliberately anomalous deformation reserved for Stage 13F is

`K_X_bad = exp(T)(p_X + a p) + epsilon q`.

Frozen control vocabulary includes

- `rank_deficient_constraint_control_rejected`;
- `constraint_algebra_anomaly_detected`;
- `basis_presentation_equivalent`;
- `representative_dependent_payload_corruption_detected`.

## 7. Frozen O/P/R/V/Xi carry-over

Stage 13 reuses rather than redesigns the Stage 12 architecture:

`T12_candidate=(O,P,R,V;Xi)`.

The inherited vocabulary retains

- `R=(R_content,R_direction,R_access)`;
- `V=(V_extension,V_semantics,V_weights)`;
- `QExt(e1)={h_L,h_R}`;
- `future_signature_left`;
- `future_signature_other`;
- external parameterization `identity`;
- internal measurement chart `A/e2`.

Xi is the designated location for representation provenance such as generator identity, constraint-basis identity, path word, raw parameters, compensator provenance, and source/target representative.

`path-specific Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

## 8. Stage 13A executable evidence

Stage 13A source/test head `ccd35956ac034de5d73d8b884a361fbe2fc92784` passed run #1676 with **`1048 passed in 592.23s (0:09:52)`**. Its documentation-synchronized head `178f4ac8d160e7b261cd854f8c1856aa80c76675` passed run #1696 with **`1050 passed in 886.76s (0:14:46)`**.

Evidence:

- **36** positive representatives;
- constraint-gradient and Hamiltonian-generator rank **2** at every representative;
- minimum finite-family singular value approximately **0.3778026572933153**;
- **36** nonzero off-surface bracket probes;
- `{K_T,K_X}+K_X` maximum residual **0.0**;
- **72 `Phi_T` + 72 `Phi_X` = 144** licensed single-generator transports;
- maximum single-flow endpoint residual approximately **2.220446049250313e-16**.

Bounded result:

`Stage 13A two-constraint first-class carrier and finite representative family on the frozen four-orbit family = established`.

`Stage 13A single-generator surface preservation != compensated multi-generator path closure`.

## 9. Stage 13B executable evidence

Stage 13B source/test head `645ce6ab099d5f9db573c29ba81ac0854c4c26ca` passed run #1710 with **`1058 passed in 696.20s (0:11:36)`**. Its documentation-synchronized head `d559c031590a058962c50d170b144acbe8eabadd` passed run #1726 with **`1059 passed in 538.54s (0:08:58)`**.

All **144 / 144** mixed pairs have nontrivial generator-order structure. Same-raw reordered endpoint separation is approximately **0.6321205588285577–12.778112197861299**.

The exact compensator closes **144 / 144** pairs with maximum compensator-law residual **8.881784197001252e-16**, maximum endpoint/target residual **2.220446049250313e-16**, and positive two-constraint residual **0.0**.

Wrong-compensator target residual is approximately **0.15803013970713942–3.1945280494653243** and is detected in **144 / 144** cases.

Bounded result:

`Stage 13B compensated two-generator path closure on the frozen 144-pair finite family = established`.

`constraint-surface preservation != correct source/target path correspondence`.

`compensated multi-constraint path closure != refoliation invariance`.

## 10. Stage 13C executable evidence

Stage 13C source/test head `56f80e8984872591a26f27eb5902310e36616bf0` passed run #1734 with **`1069 passed in 550.80s (0:09:10)`**. Documentation synchronization, including restoration of the historical Stage 11D guard wording, closed at head `51f119845ec0e9ade3ee8cdeeb4e00ca7b992569`, run #1762, with **`1066 passed in 892.04s (0:14:52)`**.

Evidence:

- **36** independently reconstructed Dirac estimates;
- **4** same-orbit summaries;
- all **6 / 6** different-orbit pairs distinct under the full Dirac pair;
- minimum full-pair separation **0.5**;
- **324** complete-relational evaluations;
- **1296** compensated-path complete-relational comparisons;
- **36** one-clock values in **12** groups, all **12 / 12** nonzero-spread with spread approximately **1.0**;
- deterministic positive residuals at most approximately **2.220446049250313e-16**.

Bounded result:

`Stage 13C Dirac / two-clock complete relational observables and physical-orbit discrimination on the frozen finite family = established`.

Finite structural conjunction:

`representative-independent Dirac orbit data + compensated-path-independent complete relational values + nontrivial relational change`.

`compensated-path relational covariance != refoliation invariance`.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`gauge quotient != elimination of physical change`.

## 11. Stage 13D executable evidence

Stage 13D implements

- `src/t_search/stage13_gauge_atlas.py`;
- `tests/test_stage13d_gauge_atlas.py`;
- `experiments/stage13d_gauge_atlas.py`;
- `docs/stage13d_notes.md`;
- `results/stage13d_gauge_atlas.md`.

Stage 13D source/test head `ab7a5c4a917e7612ee89b547baddf127d48947e7` passed GitHub Actions run #1766 with **`1076 passed in 908.96s (0:15:08)`**.

Typed finite atlas evidence:

- **87 typed nodes** separating physical orbit, representative, generator, basis, path word, event, clock, and modal continuation roles;
- **72 `Phi_T` + 72 `Phi_X` = 144** typed single-generator atlas arrows;
- **0** licensed cross-orbit atlas arrows;
- connected components built from typed arrow endpoints rather than stored orbit labels;
- exactly **4 quotient classes** of **9 representatives** each, covering all **36** representatives;
- **0** mixed-orbit quotient classes;
- all **6 / 6** quotient-class pairs remain distinct under the full Dirac pair;
- **36** quotient-level Dirac/two-clock descent evaluations;
- **144** compensated path-word descent checks consuming **1296** Stage 13C relational evaluations;
- `TX=(Phi_T,Phi_X)` and `XT=(Phi_X,Phi_T)` descend to the same quotient-level Dirac/relational payload within the frozen `1e-10` tolerance;
- path-word/compensator ablation: typed status **`lost`**, finite numerical status **`reconstructible`**, **144 / 144** targets uniquely reconstructible;
- path-word nodes remain distinct from modal-continuation nodes and all compensated descent records retain `not_physical_temporal_order` / `not_licensed` typing.

Classifications:

- `compensated_path_words_descend_to_same_quotient_payload`;
- `path_word_compensator_provenance_lost_numerically_reconstructible`.

Bounded result:

`Stage 13D typed multi-constraint gauge atlas, path-word quotient, and Dirac/relational descent on the frozen finite family = established`.

Finite structural conjunction:

`typed Phi_T/Phi_X connectivity + four-class physical quotient + path-word-independent Dirac/two-clock descent`.

`stored orbit label != quotient-construction rule`.

`numerical reconstructibility != typed operational identification`.

`reconstructible != universally redundant`.

`lost != metaphysically irreducible`.

`path word != modal continuation`.

`path word != physical temporal history`.

`compensated path-word descent != refoliation invariance`.

## 12. Stage 13 sequence

- Stage 13.0 — protocol freeze — **completed**;
- Stage 13A — two-constraint first-class carrier and finite representative family — **completed**;
- Stage 13B — noncommuting gauge paths and compensated closure — **completed**;
- Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — **completed**;
- Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — **completed**;
- Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — **next**;
- Stage 13F — basis / ablation / anomaly / false-positive controls — pending;
- Stage 13G — executable synthesis and evidence-selected next gate — pending;
- criterion 50 — external final full-repository regression / merge-readiness review — pending.

## 13. Frozen synthesis vocabulary

Stage 13G must select exactly one of:

- `multi_constraint_path_covariant`;
- `multi_constraint_path_partial`;
- `multi_constraint_path_obstructed`;
- `inconclusive`.

`multi_constraint_path_obstructed` is reserved for an explicit positive-family failure rather than a deliberately invalid control behaving correctly.

Live Stage 14 gate candidates remain

- `phase-space-dependent structure-function / hypersurface-deformation precursor`;
- `gravitational/minisuperspace extension`;
- `richer causal/order layer`;
- `nonideal/POVM clocks`.

## 14. Exit criteria

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

11. All 36 canonical representatives satisfy both positive constraints within tolerance — **satisfied**.
12. The two constraint gradients / generator directions are independent over the declared positive family — **satisfied**.
13. Numerical/analytic-gradient evaluation confirms `{K_T,K_X}=-K_X` on the declared carrier and nonzero off-surface probes — **satisfied**.
14. `Phi_T` and `Phi_X` individually preserve the two-constraint surface on licensed paths — **satisfied**.
15. The four Stage 12 physical initial-data classes are represented without accidental collapse — **satisfied**.
16. Generator, representative, orbit, event, clock, and basis provenance remain separately typed — **satisfied**.

### Criteria 17–23 — Stage 13B

17. All 144 mixed ordered source/target pairs exhibit the declared nontrivial two-generator path structure — **satisfied**.
18. Same-raw-`u` reordered mixed paths are detectably different when the protocol predicts they should be — **satisfied**.
19. The exact compensator `u_XT=exp(s)u_TX` maps the two canonical path orders to the same target within tolerance — **satisfied**.
20. Compensated path closure preserves both constraints and the declared physical-orbit identity — **satisfied**.
21. Wrong-compensator paths are numerically detected — **satisfied**.
22. Path-order / generator-order metadata remains distinct from physical temporal order — **satisfied**.
23. Cross-orbit path construction is rejected rather than compensated into false equivalence — **satisfied**.

### Criteria 24–31 — Stage 13C

24. `Q_D=q-pT-aX` and `P_D=p` are independently reconstructed from all 36 representatives — **satisfied**.
25. Same-orbit representatives agree in the full Dirac pair — **satisfied**.
26. All six canonical different-orbit pairs remain physically distinct under the full Dirac pair — **satisfied**.
27. `q(T=tau,X=chi)=Q_D+P_D tau+a chi` is reconstructed across the declared finite family — **satisfied**.
28. Complete relational values agree across compensated path choices leading to corresponding gauge representatives — **satisfied**.
29. Fixing `T=tau` alone is explicitly shown insufficient under variation of the second gauge coordinate — **satisfied**.
30. Same-P/different-Q and same-Q/different-P anti-triviality controls remain explicit — **satisfied**.
31. Complete-relational change is not promoted to ontological becoming or eternalism — **satisfied**.

### Criteria 32–38 — Stage 13D

32. Typed nodes distinguish physical orbit, representative, generator/basis, path word, event, clock, and modal roles — **satisfied**.
33. The multi-constraint atlas is built from typed `Phi_T` / `Phi_X` connectivity rather than stored orbit labels — **satisfied**.
34. The quotient recovers exactly four physical classes of nine representatives each — **satisfied**.
35. Different compensated path words to corresponding representatives descend to the same quotient-level Dirac/relational payload — **satisfied**.
36. Distinct physical Dirac data are not collapsed by path connectivity — **satisfied**.
37. Path-word / compensator removal is classified separately from numerical reconstructibility — **satisfied**.
38. Path word is not identified with modal continuation or physical temporal history — **satisfied**.

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

## 15. Interpretation guards

- `two constraint labels != two independent gauge directions`;
- `Stage 13A single-generator surface preservation != compensated multi-generator path closure`;
- `raw gauge-path commutativity != successful multi-constraint closure`;
- `same raw generator parameters under reordered paths != corresponding gauge path`;
- `constraint-surface preservation != correct source/target path correspondence`;
- `noncommuting constraint presentation != fundamental physical non-Abelianity`;
- `constraint-basis change != physical-orbit change`;
- `first-class closure on this toy carrier != hypersurface-deformation algebra`;
- `compensated multi-constraint path closure != refoliation invariance`;
- `compensated-path relational covariance != refoliation invariance`;
- `compensated path-word descent != refoliation invariance`;
- `multi-constraint path covariance != refoliation invariance`;
- `refoliation precursor != general covariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `path word != modal continuation`;
- `path word != physical temporal history`;
- `path-order mismatch != arrow of time by definition`;
- `wrong compensator failure != physical time asymmetry`;
- `one clock condition in a two-gauge-direction model != complete relational observable`;
- `complete relational observable != ontological becoming by definition`;
- `different physical orbit != later event on one orbit`;
- `constraint-generated gauge flow != ontological becoming`;
- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem`;
- `gauge quotient != elimination of physical change`;
- `stored orbit label != quotient-construction rule`;
- `path-independent complete-relational values != future actuality`;
- `path-specific Xi provenance != quotient-level physical content`;
- `basis-specific Xi provenance != quotient-level physical content`;
- `numerical reconstructibility != typed operational identification`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `finite multi-constraint gauge atlas != hypersurface-deformation algebra`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `merge-ready != merged`;
- `not_established != false`.
