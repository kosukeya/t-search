# Stage 14 Protocol — Phase-Space-Dependent Structure-Function / Hypersurface-Deformation Precursor

Status: **Stage 14C source/test checkpoint validated; criteria 1–31 satisfied; criteria 32–50 pending. Stage 14D is next.**

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

Stage 14.0 froze the protocol. Stage 14A established the bounded carrier. Stage 14B established exact compensated mixed-path closure. Stage 14C now establishes only the bounded Dirac / relational / quotient evidence stated below.

## 2. Frozen canonical phase space and constants

Canonical phase space:

`(T1,p_1; T2,p_2; X,p_X; q,p)`.

Frozen constants:

`a=0.5`, `b=0.25`, `kappa=0.5`.

The positive Stage 14 carrier has three constraint directions:

`D = p_X + a p approx 0`,

`H_1 = p_1 + p^2/2 approx 0`,

`H_2 = p_2 + b p + kappa T1 X D approx 0`.

Stage 14A verifies that the three positive constraint gradients and Hamiltonian directions have rank three on every frozen representative.

`three constraint labels != three independent gauge directions`.

## 3. Frozen first-class structure-function target

The Poisson-bracket closure target is

`{H_1,D}=0`,

`{H_1,H_2}=-kappa X D`,

`{H_2,D}=kappa T1 D`.

Thus the nonzero structure functions are phase-space dependent:

`f_12^D(z)=-kappa X`,

`f_2D^D(z)=kappa T1`.

The frozen grid samples negative, zero, and positive values.

The Jacobi target is

`{H_1,{H_2,D}} + {H_2,{D,H_1}} + {D,{H_1,H_2}} = 0`.

Stage 14A checks these identities on all positive representatives and on deliberately off-surface probes, rather than inferring closure only weakly from `D=0`.

`phase-space-dependent first-class closure != hypersurface-deformation algebra`.

`structure functions != spacetime geometry by definition`.

## 4. Frozen constraint-surface representatives and physical orbit family

The four carried physical Dirac-data controls are

- `omega_alpha : (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta : (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma : (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta : (Q_D,P_D)=(0.20,1.75)`.

Frozen representative grid:

`T1,T2,X in {-1,0,1}`.

This gives **27 representatives per physical orbit** and **108 positive representatives total**.

For `(Q_D,P_D)=(Q,P)` the representatives use

`p=P`,

`p_X=-aP`,

`p_1=-P^2/2`,

`p_2=-bP`,

`q=Q + P T1 + b T2 + a X`.

Because `D=0` on these representatives, the `kappa T1 X D` contribution vanishes on the positive surface while its derivatives and structure-function coefficients remain nontrivial.

The target physical quotient remains exactly four classes of 27 sampled representatives.

`constraint-surface vanishing of a term != algebraic irrelevance of its derivatives`.

## 5. Frozen positive Hamiltonian flows

On the positive constraint surface:

`Phi_D(v): X -> X+v, q -> q+a v`.

`Phi_1(s): T1 -> T1+s, q -> q+p s`.

For `Phi_2(u)` with fixed `T1`:

`T2 -> T2+u`,

`X -> X exp(kappa T1 u)`,

`q -> q + b u + a [X exp(kappa T1 u)-X]`.

Stage 14A checks each generator at parameters `-0.5` and `+0.5` from every positive representative, yielding 648 single-generator flow probes.

`Stage 14A single-generator surface/Dirac preservation != third-direction compensated mixed-path closure`.

## 6. Frozen third-direction compensated path semantics

For a same-orbit source `(T1_0,T2_0,X_0)` and target `(T1_1,T2_1,X_1)`, define

`s=T1_1-T1_0`,

`u=T2_1-T2_0`.

Path `12D` uses `Phi_1(s)`, then `Phi_2(u)`, then `Phi_D(v_12D)` with

`X_12*=X_0 exp(kappa T1_1 u)`,

`v_12D=X_1-X_12*`.

Path `21D` uses `Phi_2(u)`, then `Phi_1(s)`, then `Phi_D(v_21D)` with

`X_21*=X_0 exp(kappa T1_0 u)`,

`v_21D=X_1-X_21*`.

The exact compensation difference is

`v_21D-v_12D = X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]`.

The canonical Stage 14B family contains **864 ordered mixed pairs** with all three sampled coordinates changed.

Stage 14B validates both ordered implementations and exact compensation on all 864 pairs.

`raw path-word inequality != physical path dependence`.

`third-direction compensation != refoliation invariance`.

`compensated mixed-path closure != refoliation invariance`.

`wrong compensation failure != physical time asymmetry`.

## 7. Frozen Dirac, relational, and quotient targets

Frozen Dirac pair:

`P_D=p`,

`Q_D=q-p T1-b T2-a X`.

Frozen complete relational observable:

`q(T1=tau1,T2=tau2,X=chi)=Q_D+P_D tau1+b tau2+a chi`.

The deliberately incomplete two-clock expression is

`q(T1=tau1,T2=tau2; X raw)=Q_D+P_D tau1+b tau2+a X`.

Stage 14C tests representative-independent Dirac reconstruction, all six pairwise orbit separations, compensated-path descent, nontrivial relational change, incomplete-observable `D` dependence, and exactly four quotient classes.

`three gauge directions require enough relational conditions for completeness`.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`gauge quotient != elimination of physical change`.

## 8. Frozen basis-transformation taxonomy

### 8.1 Stage-13-style simple scalar rescaling

A `simple_scalar_rescaling` is an invertible diagonal transformation

`H_1' = f_1(z) H_1`,

`H_2' = f_2(z) H_2`,

`D' = f_D(z) D`

with finite nonzero scalar factors on every positive representative and no constraint mixing.

Modulo the `H_1'` and `H_2'` directions, the `D'` component of `{H_1',H_2'}` is

`-kappa X f_1 f_2 / f_D`.

A rescaling that vanishes or diverges on the positive family is singular and is not admitted as an equivalent basis.

### 8.2 Triangular phase-space-dependent mixing

The frozen comparison transformation is

`H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`.

Together with unchanged `H_1` and `D`, the target brackets are commuting. The transformation is triangular with determinant one in constraint space.

### 8.3 Frozen interpretation

`Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`.

`triangular basis equivalence != universal basis trivializability`.

`constraint-basis change != physical-orbit change`.

## 9. Frozen O/P/R/V/Xi carry-over

Stage 14 reuses

`T12_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

The inherited vocabulary retains `QExt(e1)={h_L,h_R}`, `future_signature_left`, `future_signature_other`, external parameterization `identity`, and internal measurement chart `A/e2`.

Xi stores representation provenance including generator identity, structure-function values, path word, raw `(s,u,v)`, compensator provenance, source/target representative, basis identity, and basis-transform provenance.

`structure-function/path Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

`future-measurement covariance != future actuality`.

## 10. Frozen anomaly, ablation, and false-positive controls

Required controls include `kappa=0`, duplicate/rank-deficient directions, missing `D`, wrong or missing third-direction compensation, reuse of the Stage-13-style two-generator compensator, cross-orbit paths, the two-clock incomplete observable, singular scalar rescaling, false universal-Abelianization interpretation, payload corruption, and

`H_2_bad = H_2 + epsilon q`

with `epsilon=0.1`.

Frozen classification vocabulary includes

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
- `representative_dependent_payload_corruption_detected`.

## 11. Stage 14A validated executable evidence

Incoming repository-validated Stage 14.0 checkpoint: head `afe0598362ccf0e808d2c690491cda810594d87e`, run #1832, **`1106 passed in 879.78s (0:14:39)`**.

Stage 14A source/test head: `d1116a743b0374c96993c476331f5cceacfbb077`, run #1838, **`1113 passed in 545.23s (0:09:05)`**.

Documentation-synchronized Stage 14A head: `db72c8715a3b58d4422932640807dbb20297005e`, run #1846, **`1114 passed in 900.17s (0:15:00)`**.

Validated deterministic Stage 14A evidence:

- physical orbits: **4**;
- positive representatives: **108 = 4 x 27**;
- positive constraint residual maximum: **0.0**;
- minimum constraint-gradient rank: **3**;
- minimum Hamiltonian-generator rank: **3**;
- minimum singular value of both row families: approximately **0.7812880785647448**;
- sampled structure-function values: **-0.5, 0.0, 0.5**;
- off-surface closure/Jacobi probes: **108**;
- maximum Poisson-closure identity residual: **0.0**;
- maximum Jacobi residual: **0.0**;
- single-generator flow probes: **648**;
- maximum flow constraint residual: **0.0**;
- maximum flow Dirac residual: approximately **2.220446049250313e-16**;
- `structure_function_removed_control_rejected`;
- `rank_deficient_constraint_control_rejected`.

Bounded result:

`Stage 14A three-constraint first-class structure-function carrier and finite representative family = established`.

## 12. Stage 14B validated executable evidence

Stage 14B source/test head: `2b0866b63e6fb4d4951f883839e6693b12ceddfc`, run #1852, **`1122 passed in 891.20s (0:14:51)`**.

Documentation-synchronized Stage 14B head: `318d6a34a7f8ddac29966493c31bd0cf8120ac4e`, run #1860, **`1123 passed in 548.54s (0:09:08)`**.

Validated deterministic Stage 14B evidence:

- canonical ordered mixed pairs: **864**;
- positive ordered path results: **1728**;
- nontrivial `X_0 != 0` pairs: **576**;
- exact-zero `X_0 = 0` pairs: **288**;
- nonzero compensator-difference count: **576**;
- zero compensator-difference count: **288**;
- minimum nonzero `|v_21D-v_12D|`: approximately **0.3934693402873666**;
- maximum `|v_21D-v_12D|`: approximately **2.3504023872876028**;
- maximum compensator-identity residual: **0.0**;
- maximum raw-formula residual: approximately **4.440892098500626e-16**;
- maximum final endpoint residual: approximately **4.440892098500626e-16**;
- maximum final Dirac residual: approximately **4.440892098500626e-16**;
- wrong-sign compensator rejected: **1728/1728**;
- half-value compensator rejected: **1728/1728**;
- missing compensator rejected: **1728/1728**;
- reused Stage-13-style same-`D` compensator rejected on **576/576** nontrivial pairs;
- exact-zero-difference compatibility retained on **288/288** `X_0=0` pairs;
- cross-orbit false positives rejected: **8748/8748**.

Bounded result:

`Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established`.

This result establishes only finite compensated mixed-path closure. It does not establish refoliation invariance, hypersurface-deformation algebra, general covariance, gravitational field dynamics, or GR.

## 13. Stage 14C validated executable evidence

Stage 14C source/test/runner head: `3e390ea59af879cc0b2962989467cdfe2b4ee1ca`, run #1866, **`1130 passed in 898.22s (0:14:58)`**.

Validated deterministic Stage 14C evidence:

- raw Dirac estimates: **108**;
- physical-orbit summaries: **4 × 27 representatives**;
- maximum declared `Q_D` reconstruction residual: approximately **1.6653345369377348e-16**;
- maximum declared `P_D` reconstruction residual: **0.0**;
- maximum within-orbit `Q_D` spread: approximately **2.220446049250313e-16**;
- maximum within-orbit `P_D` spread: **0.0**;
- maximum strong Dirac bracket residual against `D,H_1,H_2`: **0.0**;
- distinct physical-orbit pairs: **6**, all **6/6** separated;
- minimum full Dirac-pair separation: **0.5**;
- same-`P_D`/different-`Q_D` anti-triviality controls: **1**;
- same-`Q_D`/different-`P_D` anti-triviality controls: **1**;
- complete three-condition relational evaluations: **2916**;
- maximum complete-relational target residual: approximately **2.220446049250313e-16**;
- complete-relational within-orbit spread: **3.0 to 5.0**;
- compensated-path relational comparisons: **23328 = 864 × 27**;
- maximum compensated-path relational residual: approximately **8.881784197001252e-16**;
- two-clock incomplete evaluations: **108** in **36** fixed-clock groups;
- incomplete groups retaining third-direction dependence: **36/36**;
- raw-`X` spread: approximately **0.9999999999999998 to 1.0000000000000002**;
- quotient reconstructed from raw `(Q_D,P_D)`: exactly **4 classes × 27 representatives**;
- licensed cross-orbit arrows: **0**;
- rejected cross-orbit ordered representative pairs: **8748/8748**.

Bounded result:

`Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established`.

This result establishes finite representative-independent orbit data, nontrivial complete relational change, and complete-relational descent across the validated compensated path family. It does not establish eternalism, ontological becoming, refoliation invariance, hypersurface-deformation algebra, general covariance, gravity, or GR.

## 14. Frozen Stage 14 sequence

- Stage 14.0 — protocol freeze — **completed**;
- Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**;
- Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**;
- Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **completed**;
- Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test — **next**;
- Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases;
- Stage 14F — ablation / anomaly / false-positive controls;
- Stage 14G — executable synthesis and evidence-selected next gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

## 15. Frozen synthesis vocabulary

Stage 14G will select exactly one of:

- `structure_function_path_covariant_scalar_obstructed`;
- `structure_function_path_covariant_scalar_trivializable`;
- `structure_function_path_partial`;
- `structure_function_path_obstructed`;
- `inconclusive`.

A negative control behaving as intended does not license a positive-family obstruction classification.

## 16. Frozen criteria 1–50

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

32. Stage 14D implements the frozen invertible diagonal `simple_scalar_rescaling` class without constraint mixing — **pending**.
33. The nonzero `D'` component obstruction is verified on all required `X != 0` positive representatives — **pending**.
34. Scalar transformations that vanish or diverge on the positive family are rejected as singular rather than accepted as equivalent bases — **pending**.
35. The frozen triangular transformation `H_2_tilde=H_2-kappa T1 X D` is verified invertible on the positive family — **pending**.
36. The triangular basis satisfies the frozen commuting bracket targets within tolerance — **pending**.
37. Correctly typed triangular-basis correspondence preserves the sampled quotient, Dirac pair, complete relational values, and inherited public O/P/R/V payloads — **pending**.
38. Basis results remain bounded: scalar obstruction is not promoted to universal non-Abelianizability and triangular equivalence is not promoted to universal trivializability — **pending**.

39. Stage 14E constructs representative-level typed O/P/R/V/Xi architectures over the 108 positive representatives — **pending**.
40. Licensed compensated path choices preserve quotient-level public O/P/R/V and future-measurement payloads — **pending**.
41. Path, structure-function, compensator, and basis provenance are retained in Xi without being silently collapsed into quotient-level physical content — **pending**.
42. Orbit-sensitive public / measurement signatures remain stable within each physical quotient class and discriminate the frozen physical classes where declared — **pending**.
43. Representative/path/basis-dependent payload corruption controls are detected, while successful operational descent is not promoted to future actuality or empirical discovery — **pending**.

44. Stage 14F executes the frozen ablation family, including missing-third-direction and structure-function-removed controls — **pending**.
45. `H_2_bad=H_2+epsilon q` is detected as a constraint-algebra anomaly rather than admitted as positive evidence — **pending**.
46. Wrong-compensator, incomplete-observable, cross-orbit, singular-basis, and false-typing controls are explicitly classified and rejected — **pending**.
47. Control results remain bounded away from hypersurface-deformation algebra, GR, fundamental non-Abelianity, eternalism, or ontological becoming — **pending**.

48. Stage 14G executable synthesis selects exactly one frozen Stage 14 status from the validated Stage 14A–F evidence chain — **pending**.
49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, gravitational field degrees of freedom, or a metaphysical conclusion — **pending**.
50. External final full-repository regression and merge-readiness review — **pending**.

## 17. Interpretation boundary

Stage 14A establishes a finite three-constraint first-class structure-function carrier. Stage 14B establishes exact third-direction compensated mixed-path closure on the declared finite family. Stage 14C establishes representative-independent Dirac reconstruction, a four-class sampled quotient, nontrivial three-condition relational change, and complete-relational descent across the compensated path family.

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
- `Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`;
- `triangular basis equivalence != universal basis trivializability`;
- `constraint-basis change != physical-orbit change`;
- `path word != physical temporal history`;
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
- `constraint-algebra anomaly != ontological becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
