# Stage 14 Protocol — Phase-Space-Dependent Structure-Function / Hypersurface-Deformation Precursor

Status: **Stage 14 completed at the criterion-50 merge-readiness checkpoint; criteria 1–50 satisfied. PR #15 is merge-ready, Draft, open, and unmerged.**

## 1. Incoming baseline and selected gate

Stages 1–13 are merged. Stage 13 was merged via PR #14 into `main` at merge commit `468fe6667ec6484fbe9e402135cd75f5d69420cf`.

The final pre-merge Stage 13 current-head regression was GitHub Actions run #1823 with **`1099 passed in 893.92s (0:14:53)`** at Stage 13 branch head `d0b541acb4345933a95f592f726827acf00604c0`.

Stage 13G selected the bounded synthesis

`multi_constraint_path_covariant`

and evidence-selected the Stage 14 selector

`phase_space_structure_function_precursor`.

Frozen Stage 14 gate:

> **Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

The carried typed architecture remains

`T12_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

## 2. Frozen canonical carrier and first-class target

Canonical phase space:

`(T1,p_1; T2,p_2; X,p_X; q,p)`.

Frozen constants:

`a=0.5`, `b=0.25`, `kappa=0.5`.

Positive constraints:

`D = p_X + a p approx 0`,

`H_1 = p_1 + p^2/2 approx 0`,

`H_2 = p_2 + b p + kappa T1 X D approx 0`.

Frozen bracket targets:

`{H_1,D}=0`,

`{H_1,H_2}=-kappa X D`,

`{H_2,D}=kappa T1 D`.

Thus

`f_12^D(z)=-kappa X`,

`f_2D^D(z)=kappa T1`.

The frozen Jacobi target is

`{H_1,{H_2,D}} + {H_2,{D,H_1}} + {D,{H_1,H_2}} = 0`.

`three constraint labels != three independent gauge directions`.

`phase-space-dependent first-class closure != hypersurface-deformation algebra`.

`structure functions != spacetime geometry by definition`.

## 3. Frozen representative family

The four physical Dirac-data controls are

- `omega_alpha : (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta : (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma : (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta : (Q_D,P_D)=(0.20,1.75)`.

Frozen representative grid:

`T1,T2,X in {-1,0,1}`.

This gives **27 representatives per physical orbit** and **108 positive representatives total**.

For `(Q_D,P_D)=(Q,P)`:

`p=P`,

`p_X=-aP`,

`p_1=-P^2/2`,

`p_2=-bP`,

`q=Q + P T1 + b T2 + a X`.

The target quotient contains exactly four classes of 27 sampled representatives.

`constraint-surface vanishing of a term != algebraic irrelevance of its derivatives`.

## 4. Frozen flows and compensated mixed paths

On the positive constraint surface:

`Phi_D(v): X -> X+v, q -> q+a v`.

`Phi_1(s): T1 -> T1+s, q -> q+p s`.

For `Phi_2(u)` with fixed `T1`:

`T2 -> T2+u`,

`X -> X exp(kappa T1 u)`,

`q -> q + b u + a [X exp(kappa T1 u)-X]`.

`Stage 14A single-generator surface/Dirac preservation != third-direction compensated mixed-path closure`.

For a same-orbit source `(T1_0,T2_0,X_0)` and target `(T1_1,T2_1,X_1)` define

`s=T1_1-T1_0`,

`u=T2_1-T2_0`.

Path `12D` uses `Phi_1(s)`, `Phi_2(u)`, `Phi_D(v_12D)` with

`X_12*=X_0 exp(kappa T1_1 u)`,

`v_12D=X_1-X_12*`.

Path `21D` uses `Phi_2(u)`, `Phi_1(s)`, `Phi_D(v_21D)` with

`X_21*=X_0 exp(kappa T1_0 u)`,

`v_21D=X_1-X_21*`.

Exact difference:

`v_21D-v_12D = X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]`.

The canonical family contains **864 ordered mixed pairs**.

`raw path-word inequality != physical path dependence`.

`third-direction compensation != refoliation invariance`.

`compensated mixed-path closure != refoliation invariance`.

`wrong compensation failure != physical time asymmetry`.

## 5. Frozen Dirac, relational, and quotient targets

Frozen Dirac pair:

`P_D=p`,

`Q_D=q-p T1-b T2-a X`.

Frozen complete relational observable:

`q(T1=tau1,T2=tau2,X=chi)=Q_D+P_D tau1+b tau2+a chi`.

Deliberately incomplete two-clock expression:

`q(T1=tau1,T2=tau2; X raw)=Q_D+P_D tau1+b tau2+a X`.

`three gauge directions require enough relational conditions for completeness`.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`gauge quotient != elimination of physical change`.

## 6. Frozen basis-transformation taxonomy

A `simple_scalar_rescaling` is

`H_1' = f_1(z) H_1`,

`H_2' = f_2(z) H_2`,

`D' = f_D(z) D`

with finite nonzero factors and no constraint mixing.

Modulo the `H_1'` and `H_2'` directions, the `D'` coefficient of `{H_1',H_2'}` is

`-kappa X f_1 f_2 / f_D`.

Vanishing or divergent transformations are singular and not admitted as equivalent bases.

The frozen triangular comparison is

`H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`.

Together with unchanged `H_1` and `D`, it gives a determinant-one commuting presentation.

`Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`.

`diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity`.

`triangular basis equivalence != universal basis trivializability`.

`constraint-basis change != physical-orbit change`.

## 7. Frozen O/P/R/V/Xi carry-over

Stage 14 reuses

`T12_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

The inherited vocabulary retains `QExt(e1)={h_L,h_R}`, `future_signature_left`, `future_signature_other`, external parameterization `identity`, and internal measurement chart `A/e2`.

Xi stores generator identity, structure-function values, representative identity, path word, raw `(s,u,v)`, compensator provenance, source/target correspondence, basis identity, and basis-transform provenance.

`structure-function/path Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

`future-measurement covariance != future actuality`.

## 8. Frozen controls and classification vocabulary

Required controls include `kappa=0`, duplicate/rank-deficient directions, missing `D`, wrong/missing compensation, Stage-13-style compensator reuse, cross-orbit paths, the incomplete two-clock observable, singular scalar rescaling, false universal-Abelianization interpretation, payload corruption, and

`H_2_bad = H_2 + epsilon q`

with `epsilon=0.1`.

Frozen classifications include

- `structure_function_removed_control_rejected`;
- `rank_deficient_constraint_control_rejected`;
- `missing_third_direction_control_rejected`;
- `wrong_structure_function_compensator_detected`;
- `missing_third_direction_compensator_detected`;
- `cross_orbit_false_positive_rejected`;
- `two_clock_observable_incomplete`;
- `singular_scalar_rescaling_rejected`;
- `stage13_style_scalar_rescaling_obstructed`;
- `triangular_basis_equivalent`;
- `constraint_algebra_anomaly_detected`;
- `representative_dependent_payload_corruption_detected`;
- `path_dependent_payload_corruption_detected`;
- `basis_dependent_payload_corruption_detected`.

## 9. Validated Stage 14A–F executable evidence

### Stage 14.0 / 14A

Stage 14.0 head `afe0598362ccf0e808d2c690491cda810594d87e`, run #1832: **`1106 passed in 879.78s (0:14:39)`**.

Stage 14A source/test head `d1116a743b0374c96993c476331f5cceacfbb077`, run #1838: **`1113 passed in 545.23s (0:09:05)`**.

Documentation-synchronized Stage 14A head `db72c8715a3b58d4422932640807dbb20297005e`, run #1846: **`1114 passed in 900.17s (0:15:00)`**.

Validated evidence includes **108** representatives, rank-three constraint/generator families, minimum singular value approximately **0.7812880785647448**, structure-function samples `-0.5, 0.0, 0.5`, **108** off-surface closure/Jacobi probes, **648** single-generator flow probes, zero closure/Jacobi residuals, and maximum flow Dirac residual approximately **2.220446049250313e-16**.

`Stage 14A three-constraint first-class structure-function carrier and finite representative family = established`.

### Stage 14B

Source/test head `2b0866b63e6fb4d4951f883839e6693b12ceddfc`, run #1852: **`1122 passed in 891.20s (0:14:51)`**.

Documentation-synchronized head `318d6a34a7f8ddac29966493c31bd0cf8120ac4e`, run #1860: **`1123 passed in 548.54s (0:09:08)`**.

Validated evidence includes **864** mixed pairs, **1728** positive ordered paths, **576** nonzero compensator differences, **288** exact-zero differences, minimum nonzero difference approximately **0.3934693402873666**, maximum approximately **2.3504023872876028**, endpoint/Dirac residuals of order `4.440892098500626e-16`, wrong/missing compensator rejection, and **8748/8748** cross-orbit rejection.

`Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established`.

### Stage 14C

Source/test/runner head `3e390ea59af879cc0b2962989467cdfe2b4ee1ca`, run #1866: **`1130 passed in 898.22s (0:14:58)`**.

Documentation-synchronized head `4011b90078c6a223e6d948a3034e07376fca4dbd`, run #1874: **`1132 passed in 877.20s (0:14:37)`**.

Validated evidence includes **2916** complete-relational evaluations, **23328** compensated relational comparisons, **36/36** incomplete two-clock groups retaining third-direction dependence, maximum path relational residual approximately **8.881784197001252e-16**, **6/6** physical-orbit separation, and exactly four quotient classes of 27 representatives with **8748/8748** cross-orbit pairs rejected.

`four_class_physical_quotient_established`.

`Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established`.

### Stage 14D

Source/test head `3e44454952d71ebbe9b0a52bbd9d68cd398d0635`, run #1880: **`1139 passed in 889.88s (0:14:49)`**.

Documentation-synchronized head `69c979896cc2855869a6637b41faac010b4b0b36`, run #1888: **`1140 passed in 562.70s (0:09:22)`**.

Validated evidence includes **324** scalar evaluations, **216/216** required `X != 0` scalar obstructions across **72/72** distinct nonzero-X representatives, coefficient range approximately **0.3843557173958058** to **1.135254038874606**, **72** singular witnesses, **216 = 108 positive + 108 off-surface** triangular probes, determinant one, zero strong bracket residual, exactly **4 classes × 27 representatives**, and **108/108** public-content correspondence checks.

`Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established`.

### Stage 14E

Source/test/runner head `ac2376323f9d2b442bbbf448b22bc683ed2fd3ad`, run #1890: **`1148 passed in 897.57s (0:14:57)`** on merge checkout `1662684069cfe0f44708e7d69b4cada4ae5b72d6`.

Validated evidence includes **108** typed architectures, **864** path checks, **1728** path-Xi views, **108** basis checks, **216** basis-Xi views, four distinct orbit-sensitive signatures with minimum cross-orbit separation **0.014943579189526601**, all three representative/path/basis payload-corruption controls rejected, and `criteria_39_43_satisfied = true`.

`structure_function_path_operational_payloads_descend`.

`basis_operational_payloads_descend`.

`Stage 14E typed O/P/R/V/Xi and future-measurement descent across structure-function paths and original/triangular basis choices on the frozen finite family = established`.

### Stage 14F

Source/test/runner head `9f20ad22940ba827d346fbb7386eced5e26daedd`, run #1900: **`1154 passed in 664.20s (0:11:04)`** on merge checkout `d636706b8e141befe0e80b2841413aaeb8f0cabc`.

Notes/results head `1274f2d64e8964dd0eb46c4bc0bbe9f8ba9f8497`, run #1904: **`1154 passed in 562.70s (0:09:22)`** on merge checkout `880169d21c3d1f217ea79f04ac761468c1bba8b9`.

Formal closure head `83e00e4ada2870c33e09006e25074b909be5a975`, run #1906: **`1155 passed in 850.27s (0:14:10)`**.

Validated evidence includes **14/14** rejected controls, **108/108** missing-third-direction witnesses, **1728** wrong/missing compensator witnesses, **8748** cross-orbit pairs, **36/36** incomplete groups, **72** singular witnesses, deformed-surface anomaly residual range **0.075** to **0.175**, `typed_operational_context_rejected`, `false_universal_abelianization_interpretation_rejected`, and `criteria_44_47_satisfied = true`.

`Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established`.

`negative-control rejection != positive-family obstruction`.

`constraint-algebra anomaly != fundamental physical non-Abelianity`.

`control rejection != hypersurface-deformation algebra`.

`control rejection != general relativity`.

## 10. Stage 14G validated executable synthesis and Stage 15 gate

Stage 14G implementation head `2b59d7ac4af65d58e1a155d142a8c2bbaeb2136d`.

Run #1908 completed the synthesis but failed one test-only wording assertion (`confound` versus `conflate`): **`1 failed, 1167 passed in 551.59s (0:09:11)`**. No synthesis logic or ranking changed.

The one-word assertion alignment produced source/test head `c109d1ed1c9a1f043ed741a934c32b139ca15e09`.

Run #1910 (`32791750211`) passed **`1168 passed in 891.95s (0:14:51)`** on PR merge checkout `45a13aeff70010e05ee97f32f3114f7335a13502`.

The executable selector chooses exactly

`structure_function_path_covariant_scalar_obstructed`.

The validated synthesis integrates **864/864** compensated paths, **6/6** physical-orbit pair discrimination, **4 quotient classes × 27 representatives**, **23328** complete-relational comparisons, **216/216** nonzero-X scalar obstructions, **108/108** basis-content checks, and **14/14** destructive controls.

Bounded result:

`Stage 14G synthesis on the validated Stage 14A-F finite evidence chain = structure_function_path_covariant_scalar_obstructed`.

The validated Stage 15 ranking is:

1. `spatially_indexed_constraint_algebra_precursor` — score **13**;
2. `admissible_basis_transformation_audit` — score **10**;
3. `gravitational_minisuperspace_extension` — score **8**;
4. `richer_causal_order` — score **7**;
5. `nonideal_povm_clocks` — score **7**.

Selected Stage 15 gate:

`spatially_indexed_constraint_algebra_precursor`.

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

`structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance`.

`spatially indexed constraint precursor != hypersurface-deformation algebra by definition`.

`spatially indexed constraint precursor != general relativity`.

`local/smeared precursor != spacetime diffeomorphism invariance by definition`.

## 11. Criterion 50 external review and merge readiness

Criterion-50 reviewed head:

`ab500148975ecea6e03fe8678ba1e8dcc50cb666`.

Run #1922 (`32795808985`) passed **`1166 passed in 709.02s (0:11:49)`** on PR merge checkout `c4cafff62da2ba0726153e977724f3f78c8d2ff7`.

At the reviewed checkpoint:

- branch comparison: **ahead 46 / behind 0** against `main`;
- merge base: `468fe6667ec6484fbe9e402135cd75f5d69420cf`;
- changed files: **39**;
- PR #15: Draft, open, unmerged, `mergeable = true`;
- submitted reviews: **0**;
- unresolved inline review threads: **0**;
- PR conversation comments: **0**.

The criterion-50 review found one top-level documentation debt: README/roadmap still described Stage 13 PR #14 as currently Draft/open/unmerged although Stage 13 had already merged. Those documents were corrected to preserve the historical merge-readiness marker while stating the current merged status. Run #1922 validates the correction together with all historical regressions.

No remaining repository-level blocker was found.

`Stage 14 criterion 50 external final full-repository regression / merge-readiness review = satisfied`.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## 12. Stage 14 sequence

- Stage 14.0 — protocol freeze — **completed**;
- Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**;
- Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**;
- Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **completed**;
- Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test — **completed**;
- Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases — **completed**;
- Stage 14F — ablation / anomaly / false-positive controls — **completed**;
- Stage 14G — executable synthesis and evidence-selected next gate — **completed**;
- criterion 50 — external final full-repository regression / merge-readiness review — **completed**.

## 13. Frozen synthesis vocabulary and validated selection

The frozen selector contains exactly:

- `structure_function_path_covariant_scalar_obstructed`;
- `structure_function_path_covariant_scalar_trivializable`;
- `structure_function_path_partial`;
- `structure_function_path_obstructed`;
- `inconclusive`.

Validated selection:

`structure_function_path_covariant_scalar_obstructed`.

A negative control behaving as intended does not license a positive-family obstruction classification.

## 14. Frozen criteria 1–50

1. Stage 13 merged baseline, merge commit, final branch head, and run #1823 are frozen — **satisfied**.
2. The Stage 14 selected gate and selector `phase_space_structure_function_precursor` are frozen — **satisfied**.
3. The eight-dimensional canonical phase space, constants, and three positive constraints are frozen — **satisfied**.
4. The phase-space-dependent first-class bracket targets and Jacobi target are frozen — **satisfied**.
5. The four physical Dirac-data classes and 108-representative finite family are frozen — **satisfied**.
6. The 864-pair mixed-path family and exact third-direction compensation law are frozen — **satisfied**.
7. The Dirac pair, complete relational observable, incomplete-control observable, and four-class quotient target are frozen — **satisfied**.
8. `simple_scalar_rescaling`, singular-rescaling rejection, and triangular-mixing comparison classes are frozen before testing — **satisfied**.
9. O/P/R/V/Xi carry-over and anomaly/ablation/false-positive controls are frozen — **satisfied**.
10. The Stage 14A–G sequence, synthesis vocabulary, and interpretation boundaries are frozen — **satisfied**.
11. Stage 14A constructs all 108 positive representatives on the three-constraint surface — **satisfied**.
12. All three positive constraint residuals vanish within the frozen tolerance on the representative family — **satisfied**.
13. Constraint gradients and Hamiltonian generator directions have rank three throughout the positive representative family — **satisfied**.
14. The sampled structure functions vary nontrivially across the positive family and include negative, zero, and positive values — **satisfied**.
15. All frozen Poisson-bracket closure identities and the Jacobi identity satisfy the numerical tolerance — **satisfied**.
16. Each licensed single-generator flow preserves the positive constraint surface and the declared Dirac data — **satisfied**.
17. Stage 14A rejects structure-function-removed and rank-deficient controls without promoting them to positive evidence — **satisfied**.
18. Stage 14B constructs the canonical 864 ordered mixed source/target pairs — **satisfied**.
19. Both `12D` and `21D` path implementations match the frozen exact flow formulas — **satisfied**.
20. Exact third-direction compensation closes every positive mixed pair on the same licensed target within tolerance — **satisfied**.
21. The nontrivial `X_0 != 0` subfamily exhibits the expected path-order-dependent raw compensator difference — **satisfied**.
22. Wrong-sign, wrong-value, missing, and Stage-13-style compensators are rejected on the required nontrivial cases — **satisfied**.
23. Cross-orbit source/target pairs are not licensed as gauge paths — **satisfied**.
24. Path-order / compensator results remain explicitly bounded away from refoliation invariance, time asymmetry, and ontological becoming — **satisfied**.
25. Stage 14C reconstructs representative-independent `(Q_D,P_D)` across all 108 positive representatives — **satisfied**.
26. The full Dirac pair separates all six pairs among the four physical orbit classes — **satisfied**.
27. The complete three-condition relational observable descends across all licensed compensated paths — **satisfied**.
28. The complete relational family retains nontrivial relational change across varying `(tau1,tau2,chi)` — **satisfied**.
29. The two-clock incomplete observable retains detectable third-direction gauge dependence — **satisfied**.
30. The sampled quotient contains exactly four classes of 27 representatives with zero licensed cross-orbit arrows — **satisfied**.
31. Dirac / relational / quotient results remain bounded away from eternalism, timeless ontology, and elimination of physical change — **satisfied**.
32. Stage 14D implements the frozen invertible diagonal `simple_scalar_rescaling` class without constraint mixing — **satisfied**.
33. The nonzero `D'` component obstruction is verified on all required `X != 0` positive representatives — **satisfied**.
34. Scalar transformations that vanish or diverge on the positive family are rejected as singular rather than accepted as equivalent bases — **satisfied**.
35. The frozen triangular transformation `H_2_tilde=H_2-kappa T1 X D` is verified invertible on the positive family — **satisfied**.
36. The triangular basis satisfies the frozen commuting bracket targets within tolerance — **satisfied**.
37. Correctly typed triangular-basis correspondence preserves the sampled quotient, Dirac pair, complete relational values, and inherited public O/P/R/V payloads — **satisfied**.
38. Basis results remain bounded: scalar obstruction is not promoted to universal non-Abelianizability and triangular equivalence is not promoted to universal trivializability — **satisfied**.
39. Stage 14E constructs representative-level typed O/P/R/V/Xi architectures over the 108 positive representatives — **satisfied**.
40. Licensed compensated path choices preserve quotient-level public O/P/R/V and future-measurement payloads — **satisfied**.
41. Path, structure-function, compensator, and basis provenance are retained in Xi without being silently collapsed into quotient-level physical content — **satisfied**.
42. Orbit-sensitive public / measurement signatures remain stable within each physical quotient class and discriminate the frozen physical classes where declared — **satisfied**.
43. Representative/path/basis-dependent payload corruption controls are detected, while successful operational descent is not promoted to future actuality or empirical discovery — **satisfied**.
44. Stage 14F executes the frozen ablation family, including missing-third-direction and structure-function-removed controls — **satisfied**.
45. `H_2_bad=H_2+epsilon q` is detected as a constraint-algebra anomaly rather than admitted as positive evidence — **satisfied**.
46. Wrong-compensator, incomplete-observable, cross-orbit, singular-basis, and false-typing controls are explicitly classified and rejected — **satisfied**.
47. Control results remain bounded away from hypersurface-deformation algebra, GR, fundamental non-Abelianity, eternalism, or ontological becoming — **satisfied**.
48. Stage 14G executable synthesis selects exactly one frozen Stage 14 status from the validated Stage 14A–F evidence chain — **satisfied**.
49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, gravitational field degrees of freedom, or a metaphysical conclusion — **satisfied**.
50. External final full-repository regression and merge-readiness review — **satisfied**.

## 15. Interpretation boundary

Stage 14 establishes a bounded finite structure-function path-covariance precursor with representative-independent Dirac data, nontrivial complete relational change, typed operational descent, a diagonal scalar-rescaling obstruction, an explicit richer commuting triangular presentation, and a successful destructive-control matrix. Criterion 50 adds only repository-level validation and merge-readiness review; it is not new scientific evidence.

Persistent guards:

- `phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`;
- `finite first-class structure-function algebra != hypersurface-deformation algebra`;
- `hypersurface-deformation precursor != general relativity`;
- `structure functions != spacetime geometry by definition`;
- `three constraint labels != three independent gauge directions`;
- `raw path-word inequality != physical path dependence`;
- `third-direction compensation != refoliation invariance`;
- `compensated mixed-path closure != refoliation invariance`;
- `compensated relational descent != refoliation invariance`;
- `compensated-path operational descent != refoliation invariance`;
- `basis-equivalent operational descent != refoliation invariance`;
- `Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`;
- `diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity`;
- `triangular basis equivalence != universal basis trivializability`;
- `constraint-basis change != physical-orbit change`;
- `basis-equivalent finite quotient != refoliation invariance`;
- `commuting triangular presentation != proof that all admissible presentations commute`;
- `basis equivalence != hypersurface-deformation algebra`;
- `basis equivalence != general relativity`;
- `basis equivalence != ontological becoming`;
- `structure-function/path Xi provenance != quotient-level physical content`;
- `basis-specific Xi provenance != quotient-level physical content`;
- `path word != physical temporal history`;
- `path word != modal continuation`;
- `wrong compensator failure != physical time asymmetry`;
- `two-clock incompleteness != physical time asymmetry`;
- `compensated path closure != ontological becoming`;
- `complete relational observable != ontological becoming by definition`;
- `complete three-condition relational observable != ontological becoming by definition`;
- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `four-class gauge quotient != elimination of physical change`;
- `finite relational covariance != metaphysical becoming`;
- `future-measurement covariance != future actuality`;
- `orbit-sensitive witness != empirical prediction`;
- `negative-control rejection != positive-family obstruction`;
- `structure-function removal != evidence against the positive carrier`;
- `missing-third-direction failure != physical time asymmetry`;
- `constraint-algebra anomaly != ontological becoming`;
- `constraint-algebra anomaly != fundamental physical non-Abelianity`;
- `control rejection != hypersurface-deformation algebra`;
- `control rejection != general relativity`;
- `cross-orbit rejection != spacetime causal separation`;
- `singular-basis rejection != universal non-Abelianizability`;
- `false typing rejection != empirical discovery`;
- `structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance`;
- `spatially indexed constraint precursor != hypersurface-deformation algebra by definition`;
- `spatially indexed constraint precursor != general relativity`;
- `local/smeared precursor != spacetime diffeomorphism invariance by definition`;
- `finite-dimensional/minisuperspace carrier != spatially local smeared constraint algebra`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `merge-ready != merged`;
- `not_established != false`.
