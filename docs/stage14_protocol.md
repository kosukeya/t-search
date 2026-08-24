# Stage 14 Protocol — Phase-Space-Dependent Structure-Function / Hypersurface-Deformation Precursor

Status: **Stage 14.0 protocol freeze completed; criteria 1–10 satisfied; criteria 11–50 pending.**

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

Stage 14.0 establishes only the protocol. It does not establish a structure-function covariance result.

## 2. Frozen canonical phase space and constants

Canonical phase space:

`(T1,p_1; T2,p_2; X,p_X; q,p)`.

Frozen constants:

`a=0.5`, `b=0.25`, `kappa=0.5`.

The positive Stage 14 carrier has three constraint directions:

`D = p_X + a p approx 0`,

`H_1 = p_1 + p^2/2 approx 0`,

`H_2 = p_2 + b p + kappa T1 X D approx 0`.

The three constraint labels must still be checked for independent gradients / Hamiltonian directions on the frozen finite family.

`three constraint labels != three independent gauge directions`.

## 3. Frozen first-class structure-function target

The intended Poisson-bracket closure is

`{H_1,D}=0`,

`{H_1,H_2}=-kappa X D`,

`{H_2,D}=kappa T1 D`.

Thus the nonzero structure functions are phase-space dependent:

`f_12^D(z)=-kappa X`,

`f_2D^D(z)=kappa T1`.

On the frozen representative grid, `T1` and `X` each take `{-1,0,1}`, so the structure-function values must include negative, zero, and positive values.

The Jacobi target is

`{H_1,{H_2,D}} + {H_2,{D,H_1}} + {D,{H_1,H_2}} = 0`.

Stage 14A must verify the bracket identities, numerical closure, rank, finite-family variation, and Jacobi residuals rather than inferring them from symbolic intent.

`phase-space-dependent first-class closure != hypersurface-deformation algebra`.

`structure functions != spacetime geometry by definition`.

## 4. Frozen constraint-surface representatives and physical orbit family

The Stage 13 four physical Dirac-data controls are retained:

- `omega_alpha : (Q_D,P_D)=(-0.35,1.25)`;
- `omega_beta : (Q_D,P_D)=(0.40,1.25)`;
- `omega_gamma : (Q_D,P_D)=(-0.35,0.75)`;
- `omega_delta : (Q_D,P_D)=(0.20,1.75)`.

Frozen representative grid:

`T1,T2,X in {-1,0,1}`.

This gives **27 representatives per physical orbit** and **108 positive representatives total**.

For an orbit with `(Q_D,P_D)=(Q,P)`, the representative is frozen as

`p=P`,

`p_X=-aP`,

`p_1=-P^2/2`,

`p_2=-bP`,

`q=Q + P T1 + b T2 + a X`.

Because `D=0` on these representatives, the `kappa T1 X D` term vanishes on the constraint surface while its derivatives and bracket coefficients remain nontrivial.

The target physical quotient remains exactly four physical orbit classes, each containing 27 sampled representatives.

`constraint-surface vanishing of a term != algebraic irrelevance of its derivatives`.

## 5. Frozen positive Hamiltonian flows

On the positive constraint surface:

`Phi_D(v): X -> X+v, q -> q+a v`.

`Phi_1(s): T1 -> T1+s, q -> q+p s`.

For `Phi_2(u)` with fixed `T1`:

`T2 -> T2+u`,

`X -> X exp(kappa T1 u)`,

`q -> q + b u + a [X exp(kappa T1 u)-X]`.

The constraint momenta remain on the positive constraint surface.

Stage 14A must verify exact / numerical surface preservation on the declared family.

## 6. Frozen third-direction compensated path semantics

For a same-orbit source `(T1_0,T2_0,X_0)` and target `(T1_1,T2_1,X_1)` with

`s=T1_1-T1_0`,

`u=T2_1-T2_0`,

define the two canonical ordered paths.

Path `12D`:

1. `Phi_1(s)`;
2. `Phi_2(u)`;
3. `Phi_D(v_12D)`,

with

`X_12*=X_0 exp(kappa T1_1 u)`,

`v_12D=X_1-X_12*`.

Path `21D`:

1. `Phi_2(u)`;
2. `Phi_1(s)`;
3. `Phi_D(v_21D)`,

with

`X_21*=X_0 exp(kappa T1_0 u)`,

`v_21D=X_1-X_21*`.

The exact third-direction compensation difference is

`v_21D-v_12D = X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]`.

The canonical Stage 14B mixed-pair family consists of ordered same-orbit source/target pairs for which all three sampled coordinates differ:

`T1_1 != T1_0`, `T2_1 != T2_0`, `X_1 != X_0`.

On the 4-orbit 3x3x3 grid this yields **864 ordered mixed pairs**.

The protocol expects a nontrivial subset with `X_0 != 0` to require different third-direction compensators, while `X_0=0` provides an exact zero-difference subfamily.

`raw path-word inequality != physical path dependence`.

`third-direction compensation != refoliation invariance`.

`wrong compensation failure != physical time asymmetry`.

## 7. Frozen Dirac, relational, and quotient targets

Frozen Dirac pair:

`P_D=p`,

`Q_D=q-p T1-b T2-a X`.

Frozen complete relational observable:

`q(T1=tau1,T2=tau2,X=chi)=Q_D+P_D tau1+b tau2+a chi`.

The deliberately incomplete two-clock expression is

`q(T1=tau1,T2=tau2; X raw)=Q_D+P_D tau1+b tau2+a X`.

Stage 14C must test:

- representative-independent reconstruction of `(Q_D,P_D)`;
- separation of all four physical orbits by the full Dirac pair;
- compensated-path independence of the complete relational observable;
- nontrivial relational change as `(tau1,tau2,chi)` vary;
- residual `D`-direction dependence of the two-clock incomplete observable;
- exactly four sampled quotient classes of 27 representatives.

`three gauge directions require enough relational conditions for completeness`.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`gauge quotient != elimination of physical change`.

## 8. Frozen basis-transformation taxonomy

Stage 14 distinguishes three basis notions before any result is observed.

### 8.1 Stage-13-style simple scalar rescaling

A `simple_scalar_rescaling` is an invertible diagonal transformation

`H_1' = f_1(z) H_1`,

`H_2' = f_2(z) H_2`,

`D' = f_D(z) D`,

where each scalar is finite and nonzero on every positive representative under test and **no constraint mixing is allowed**.

For such a transformation, modulo terms proportional to `H_1'` and `H_2'`, the `D'` component of `{H_1',H_2'}` is

`-kappa X f_1 f_2 / f_D`.

Therefore, on positive representatives with `X != 0`, a finite nonzero diagonal rescaling cannot remove that third-direction bracket component.

Stage 14D must verify this frozen obstruction criterion on the finite family.

A rescaling that vanishes or diverges on any frozen positive representative is classified as singular and is not admitted as an equivalent basis.

### 8.2 Triangular phase-space-dependent constraint mixing

The separately frozen comparison transformation is

`H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`.

Together with unchanged `H_1` and `D`,

`{H_1,H_2_tilde}=0`,

`{H_2_tilde,D}=0`,

`{H_1,D}=0`.

This is an invertible triangular basis change with determinant one in constraint space.

Stage 14D must test whether it preserves the sampled constraint surface, gauge distribution, physical quotient, Dirac pair, complete relational observables, and inherited public O/P/R/V payloads.

### 8.3 Frozen interpretation

A failure of `simple_scalar_rescaling` together with success of triangular mixing means only that the Stage 13 one-generator rescaling trivialization does not persist in the same form.

It does **not** establish non-Abelianizability.

`Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`.

`triangular basis equivalence != universal basis trivializability`.

`constraint-basis change != physical-orbit change`.

## 9. Frozen O/P/R/V/Xi carry-over

Stage 14 reuses the inherited typed architecture rather than redesigning it:

`T12_candidate=(O,P,R,V;Xi)`.

The inherited vocabulary retains

- `R=(R_content,R_direction,R_access)`;
- `V=(V_extension,V_semantics,V_weights)`;
- `QExt(e1)={h_L,h_R}`;
- `future_signature_left`;
- `future_signature_other`;
- external parameterization `identity`;
- internal measurement chart `A/e2`.

Xi is the designated location for representation provenance, including

- generator identity;
- structure-function values;
- path word;
- raw parameters `(s,u,v)`;
- compensator provenance;
- source/target representative;
- constraint-basis identity;
- scalar-rescaling or triangular-mixing provenance.

Stage 14E must retest quotient-level public O/P/R/V and future-measurement descent while keeping these representation fields typed separately.

`structure-function/path Xi provenance != quotient-level physical content`.

`basis-specific Xi provenance != quotient-level physical content`.

`future-measurement covariance != future actuality`.

## 10. Frozen anomaly, ablation, and false-positive controls

Required controls include:

- `kappa=0` / structure-function-removed carrier falsely admitted as the positive Stage 14 structure-function case;
- rank-deficient or duplicate constraint directions;
- missing third constraint `D`;
- wrong sign or wrong value in the structure-function compensation law;
- `v=0` / no third-direction compensation where nonzero compensation is required;
- Stage-13-style two-generator compensator falsely reused for the three-generator carrier;
- cross-orbit paths falsely licensed as gauge-related;
- two-clock incomplete observable falsely called complete;
- singular diagonal basis rescaling falsely accepted as equivalent;
- triangular mixing falsely interpreted as proof of universal Abelianizability;
- representative/path/basis-dependent O/P/R/V corruption;
- deliberately non-first-class deformation

`H_2_bad = H_2 + epsilon q`

with `epsilon=0.1`.

The anomalous deformation introduces non-constraint residual terms, including an `-epsilon p` contribution in `{H_1,H_2_bad}` and an `epsilon a` contribution in `{H_2_bad,D}` under the frozen canonical convention.

Frozen control vocabulary includes:

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

## 11. Frozen Stage 14 sequence

- Stage 14.0 — protocol freeze — **completed**;
- Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **next**;
- Stage 14B — phase-space-dependent mixed paths and third-direction compensation;
- Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination;
- Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test;
- Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases;
- Stage 14F — ablation / anomaly / false-positive controls;
- Stage 14G — executable synthesis and evidence-selected next gate;
- criterion 50 — external final full-repository regression / merge-readiness review.

No later stage is considered established by Stage 14.0.

## 12. Frozen synthesis vocabulary

Stage 14G will select exactly one of:

- `structure_function_path_covariant_scalar_obstructed`;
- `structure_function_path_covariant_scalar_trivializable`;
- `structure_function_path_partial`;
- `structure_function_path_obstructed`;
- `inconclusive`.

The first two statuses refer only to the frozen Stage-13-style **diagonal scalar-rescaling** question. Success of triangular mixing is recorded separately and does not by itself choose between metaphysical interpretations.

A deliberately anomalous carrier or negative control behaving correctly does not license `structure_function_path_obstructed`; that status is reserved for failure of the positive Stage 14 family.

## 13. Frozen criteria 1–50

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

11. Stage 14A constructs all 108 positive representatives on the three-constraint surface — **pending**.
12. All three positive constraint residuals vanish within the frozen tolerance on the representative family — **pending**.
13. Constraint gradients and Hamiltonian generator directions have rank three throughout the positive representative family — **pending**.
14. The sampled structure functions vary nontrivially across the positive family and include negative, zero, and positive values — **pending**.
15. All frozen Poisson-bracket closure identities and the Jacobi identity satisfy the numerical tolerance — **pending**.
16. Each licensed single-generator flow preserves the positive constraint surface and the declared Dirac data — **pending**.
17. Stage 14A rejects structure-function-removed and rank-deficient controls without promoting them to positive evidence — **pending**.

18. Stage 14B constructs the canonical 864 ordered mixed source/target pairs — **pending**.
19. Both `12D` and `21D` path implementations match the frozen exact flow formulas — **pending**.
20. Exact third-direction compensation closes every positive mixed pair on the same licensed target within tolerance — **pending**.
21. The nontrivial `X_0 != 0` subfamily exhibits the expected path-order-dependent raw compensator difference — **pending**.
22. Wrong-sign, wrong-value, missing, and Stage-13-style compensators are rejected on the required nontrivial cases — **pending**.
23. Cross-orbit source/target pairs are not licensed as gauge paths — **pending**.
24. Path-order / compensator results remain explicitly bounded away from refoliation invariance, time asymmetry, and ontological becoming — **pending**.

25. Stage 14C reconstructs representative-independent `(Q_D,P_D)` across all 108 positive representatives — **pending**.
26. The full Dirac pair separates all six pairs among the four physical orbit classes — **pending**.
27. The complete three-condition relational observable descends across all licensed compensated paths — **pending**.
28. The complete relational family retains nontrivial relational change across varying `(tau1,tau2,chi)` — **pending**.
29. The two-clock incomplete observable retains detectable third-direction gauge dependence — **pending**.
30. The sampled quotient contains exactly four classes of 27 representatives with zero licensed cross-orbit arrows — **pending**.
31. Dirac / relational / quotient results remain bounded away from eternalism, timeless ontology, and elimination of physical change — **pending**.

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

## 14. Interpretation boundary

Stage 14.0 is a protocol freeze, not a scientific result beyond the choice of what will be tested.

Persistent guards:

- `phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`;
- `finite first-class structure-function algebra != hypersurface-deformation algebra`;
- `hypersurface-deformation precursor != general relativity`;
- `structure functions != spacetime geometry by definition`;
- `three constraint labels != three independent gauge directions`;
- `third-direction compensation != refoliation invariance`;
- `Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`;
- `triangular basis equivalence != universal basis trivializability`;
- `constraint-basis change != physical-orbit change`;
- `path word != physical temporal history`;
- `wrong compensator failure != physical time asymmetry`;
- `complete relational observable != ontological becoming by definition`;
- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `future-measurement covariance != future actuality`;
- `constraint-algebra anomaly != ontological becoming`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
