# Stage 10 Protocol — Fully Typed Future-Measurement Covariance

Status: **Stage 10.0 protocol frozen; Stage 10A, Stage 10B, and Stage 10C completed; criteria 1–31 completed; Stage 10D next.**

Historical Stage 10B checkpoint: **Stage 10A and Stage 10B completed; criteria 1–23 completed.**

Selected Stage 10 gate from Stage 9G:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Stage 10 retains `T10_candidate=(O,P,R,V;Xi)` with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

## 1. Frozen central question

Can the Stage 9C future-signature measurement be promoted into a single **fully typed cross-continuation measurement family** whose outcome semantics, effects, normalization rule, probabilities, continuation classes, and event/outcome correspondences remain operationally consistent under the genuine continuation-specific A/B/C clock changes established in Stage 9D?

`state covariance != measurement covariance by definition`.

`same numeric probability != same operational question`.

## 2. Frozen carrier and reference measurement

Stage 10 reuses the merged Stage 9 carrier:

`QExt(e1)={h_L,h_R}`.

Prediction anchor: `e1`.

Measurement target: `e2`.

Reference Stage 9C measurement:

`M_ref={future_signature_left,future_signature_other}`

with `E_left=|psi_L(e2)><psi_L(e2)|` and `E_other=I-E_left`.

The existing Stage 9C normalized-reduced-state Born probabilities remain the operational reference.

`prediction anchor e1 != measurement target e2`.

`reference effect derived from h_L != ontic selector h*`.

## 3. Fully typed measurement-family schema

The frozen schema makes these resources explicit:

- measurement-family identity;
- continuation class / continuation id;
- prediction anchor;
- measurement target event;
- clock perspective;
- clock reading;
- outcome identity;
- outcome semantics / provenance;
- effect representation;
- coordinate basis;
- normalization / inner-product convention;
- event correspondence;
- continuation-class correspondence;
- outcome correspondence;
- continuation-weight semantics.

An individual effect is typed by `(family,continuation,prediction_anchor,target_event,clock,index,outcome,semantics,basis,normalization)`.

`same outcome label != outcome identity`.

`same matrix entries != same typed effect`.

## 4. Normalization boundary and Stage 10B selection

Stage 10.0 froze two candidate descriptions:

1. **chart-local POVM representation** with `sum_o E_o=I`;
2. **metric-aware effect-form representation** with `sum_o F_o=G` and `p(o|h)=z^dagger F_o z / (z^dagger G z)`.

Candidate dual transport was frozen as:

`G_Y=S^{-dagger} G_X S^{-1}`

`F_{o,Y}=S^{-dagger} F_{o,X} S^{-1}`.

Stage 10B selected the reference-induced physical effect/normalization form. For each continuation `h` and its A/e2 reduction `R_h`:

`N_h=R_h^dagger R_h`

`F_{h,o}=R_h^dagger E_o R_h`

`p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`

`sum_o F_{h,o}=N_h`.

At A/e2 this is equivalent to the ordinary local support POVM. Genuine Stage 9D clock maps are non-Euclidean-unitary, so Stage 10 does not reset normalization to numerical identity independently in every chart.

The Stage 9D physical metric and Stage 10 operational normalization remain different typed resources.

`metric-aware candidate law != established measurement covariance`.

`normalization convention != mere implementation detail`.

`reference-chart identity normalization != identity normalization in every transported chart`.

## 5. Strong covariance target

For every continuation and genuine distinct-clock transport `(X,j)->(Y,k)`, Stage 10 seeks:

`p^h_{X,j}(o)=p^h_{Y,k}(chi_outcome(o))`

within tolerance after event/class/outcome/basis/normalization typing is validated.

The comparison is **per-continuation before weighting**.

`weighted probability equality != per-continuation measurement covariance`.

`effect covariance without outcome typing != full measurement covariance`.

## 6. Composition and route consistency

The declared atlas contains 108 genuine ordered distinct-clock transports and 324 three-clock compositions. Numerical form transport and semantic outcome consistency are both required.

`matrix composition consistency != semantic outcome consistency`.

## 7. Mixture, modal, and update layer

Only after per-continuation likelihood covariance is established or refuted are weights restored:

`P_{X,j}(o)=sum_h w_h p^h_{X,j}(o)`.

Canonical models remain:

`M_E^QR=(QRCarrier,e1,h*,q_E)`

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`.

The **hidden epistemic `h*` swap** remains outside the public schema. A **weight mismatch** must remain predictively visible if supported, and **common explicit evidence** must be conditioned using the same transported likelihood semantics.

`measurement covariance != modal/ontological identity`.

`weight covariance != selected-continuation observability`.

`evidence-update covariance != ontological becoming`.

## 8. Frozen negative controls

Stage 10 must test at least:

1. **bare-effect reuse**;
2. **wrong-continuation map**;
3. **swapped continuation classes**;
4. **swapped/misdeclared outcomes**;
5. **anchor/target confusion**;
6. **wrong/missing event correspondence**;
7. **wrong normalization/metric**;
8. **weight misalignment**;
9. **outcome-typing removal**;
10. **mixed normalization convention**.

`accidental probability equality != validated covariance`.

`covariance of a wrongly typed measurement != semantic correctness`.

## 9. Stage 10A — typed reference future-measurement family — completed

Stage 10A introduced the typed A/e2 reference family without changing Stage 9C semantics. It reproduced canonical outcomes/effects, kept e1/e2 roles explicit, revalidated positivity/completeness, retained h_L/h_R discrimination, reproduced Stage 9C likelihoods, and exposed no hidden selector/modal-type field.

`typed continuation id != hidden selected continuation`.

`reference-node validity != cross-clock measurement covariance`.

Scientific validation: **`783 passed in 461.16s`** (run #1145). Documentation-synchronized regression: **`787 passed in 465.49s`** (run #1157).

## 10. Stage 10B — continuation-specific measurement lift / normalization choice — completed

Stage 10B independently derived h_L/h_R support and physical-form lifts, selected the reference-induced operational normalization, made class/outcome correspondence explicit, and rejected wrong-continuation lift use.

`normalization representation selected != cross-clock measurement covariance established`.

Scientific validation: **`795 passed in 462.74s`** (run #1163). Documentation-synchronized regression: **`800 passed in 372.79s`** (run #1179).

## 11. Stage 10C — continuation-aware A/B/C measurement transport — completed

For each continuation, clock, and reading, Stage 10C directly reconstructs the Stage 10B physical forms with:

`H^X_h=C_{h,X,j}^{-dagger} H_h C_{h,X,j}^{-1}`.

For genuine clock changes:

`S^h_{Y,k<-X,j}=C_{h,Y,k} C_{h,X,j}^{-1}`

and:

`H^Y_h=S^{-dagger} H^X_h S^{-1}`.

Established in the declared finite atlas:

- 9 charts per continuation / **18 total**;
- **108** genuine ordered distinct-clock measurement transports;
- dual transport agrees with direct reconstruction from the shared physical object;
- **324** three-clock measurement compositions agree with direct transport;
- completeness is covariant as `sum_o F^X_{h,o}=N^X_h`;
- transported normalization is Hermitian positive definite within tolerance;
- transported effects are Hermitian positive semidefinite within tolerance;
- preserving event/class/outcome correspondence is valid at every node;
- bare-effect reuse, misdeclared event correspondence, and swapped continuation classes are rejected.

Evidence status after Stage 10C:

`future-measurement representation covariance = established` in the declared finite atlas.

`full per-continuation probability covariance = not_established` until Stage 10D.

`measurement representation covariance != probability covariance by definition`.

Scientific validation: **`809 passed in 476.21s`** (run #1185).

## 12. Stage sequence

- **Stage 10.0 — protocol freeze — completed**;
- **Stage 10A — typed reference future-measurement family — completed**;
- **Stage 10B — continuation-specific measurement lift / normalization choice — completed**;
- **Stage 10C — continuation-aware A/B/C measurement transport — completed**;
- **Stage 10D — per-continuation Born/completeness/positivity covariance — next**;
- **Stage 10E — weights, modal models, and evidence-update covariance**;
- **Stage 10F — ablation / wrong-typing / false-positive controls**;
- **Stage 10G — synthesis and evidence-selected next gate**;
- **criterion 50 — external full-repository regression / merge-readiness review**.

## 13. Exit-criterion allocation

### Stage 10.0 — criteria 1–10 — completed

1. Exact Stage 9G-selected Stage 10 gate frozen — **satisfied**.
2. Merged Stage 9 carrier reused — **satisfied**.
3. Stage 9C reference outcomes/effects/probabilities frozen — **satisfied**.
4. e1 prediction anchor and e2 target typed separately — **satisfied**.
5. Full measurement typing schema frozen — **satisfied**.
6. Normalization retained as a scientific decision boundary — **satisfied**.
7. Strong per-continuation covariance criterion frozen — **satisfied**.
8. Mixture/modal/update covariance separated — **satisfied**.
9. Negative controls frozen — **satisfied**.
10. Guards, sequence, vocabulary, and criteria 11–50 allocation frozen — **satisfied**.

### Stage 10A — criteria 11–16 — completed

11. Typed reference measurement reproduces Stage 9C outcomes/effects — **satisfied**.
12. Outcome provenance and e1/e2 typing explicit — **satisfied**.
13. Reference positivity/completeness revalidated — **satisfied**.
14. Reference measurement remains operationally discriminating — **satisfied**.
15. Per-continuation reference probabilities reproduce Stage 9C — **satisfied**.
16. Public reference schema contains no hidden selector/modal-type field — **satisfied**.

### Stage 10B — criteria 17–23 — completed

17. Independent continuation-specific support/physical lifts — **satisfied**.
18. No universal h-independent measurement map assumed — **satisfied**.
19. Effects and normalization mathematically well-defined — **satisfied**.
20. Normalization selected by Stage 9C equivalence plus nonunitarity evidence — **satisfied**.
21. Reference probabilities agree for both continuations — **satisfied**.
22. Class/outcome correspondences explicit — **satisfied**.
23. Wrong-continuation lift rejected — **satisfied**.

### Stage 10C — criteria 24–31 — completed

24. Valid typed measurement representations exist at every canonical h_L/h_R A/B/C chart — **satisfied**.
25. All 108 genuine ordered distinct-clock measurement transports are tested — **satisfied**.
26. Dual transport agrees with direct shared-physical-object reconstruction — **satisfied**.
27. All 324 three-clock compositions agree with direct transport — **satisfied**.
28. Completeness is covariant in the retained normalization convention — **satisfied**.
29. Positivity/Hermiticity requirements are covariant — **satisfied**.
30. Outcome identity and event/class correspondence remain valid at every node — **satisfied**.
31. Bare-effect and wrong-event/class controls are rejected — **satisfied**.

### Stage 10D — criteria 32–38

32. Per-continuation outcome probabilities are invariant across all declared corresponding clock nodes.
33. Every transported chart reproduces Stage 9C reference likelihoods for each continuation/outcome.
34. Per-continuation likelihood covariance is established before branch-weight aggregation.
35. Swapped/misdeclared outcome correspondence is detected.
36. Wrong normalization/metric use is detected on a discriminating input family.
37. Accidental canonical-state equality is ruled out where necessary by additional valid discriminating inputs.
38. Full typed future-measurement covariance receives an explicit evidence status: `established`, `partial`, `refuted`, or `not_established`.

### Stage 10E — criteria 39–43

39. Weighted future predictions are covariant under valid class/weight/outcome correspondence.
40. Matched epistemic/ontic-extension public measurement views agree across all declared nodes if supported.
41. Hidden epistemic h* swaps remain outside the public typed measurement schema.
42. Weight mismatch remains predictively visible with the same operational meaning across perspectives.
43. Common evidence conditioning/posteriors are perspective-consistent and ontic update remains selector-free.

### Stage 10F — criteria 44–47

44. Removing event/class/outcome correspondence classifies typed identifications using the project status vocabulary.
45. Removing/corrupting normalization semantics classifies probability covariance as warranted.
46. Bare-effect, wrong-continuation, wrong-outcome, wrong-event, and weight-misalignment controls receive explicit witnesses/residuals.
47. Reconstruction/ablation results avoid metaphysical promotion.

### Stage 10G — criteria 48–49

48. Executable synthesis selects among at least `measurement_covariant`, `measurement_partial`, `measurement_obstructed`, or `inconclusive`.
49. The next gate is evidence-selected from remaining unresolved boundaries.

### Criterion 50

50. External final full-repository regression and merge-readiness review close Stage 10 only after criteria 1–49 are satisfied or explicitly resolved.

## 14. Status vocabulary

`preserved / reconstructible / inaccessible / lost / underdetermined / not_established / compatible / implication_refuted`.

Overall measurement-covariance status additionally permits `established / partial / refuted / not_established`.

`not_established != false`.

`refuted measurement covariance != ontological becoming`.

## 15. Interpretation guards

- `future-measurement covariance != future actuality`;
- `future-measurement covariance != ontic future openness`;
- `future-measurement covariance != hidden selected future`;
- `measurement covariance != modal/ontological identity`;
- `measurement-covariance failure != ontological becoming`;
- `perspective-invariant future probabilities != proof of eternalism`;
- `same outcome label != outcome identity`;
- `same numeric probability != measurement-family identity`;
- `effect covariance != same operational question without outcome/event/class typing`;
- `reference h_L-ray effect != epistemic/ontic continuation selector`;
- `continuation-specific measurement representation != hidden branch selection`;
- `weight covariance != selected-continuation observability`;
- `evidence-update covariance != ontological becoming`;
- `metric-aware candidate law != established measurement covariance`;
- `chart-local POVM validity != cross-chart family covariance`;
- `normalization representation selected != measurement covariance established`;
- `physical metric != operational normalization by definition`;
- `measurement representation covariance != probability covariance by definition`;
- `full finite-clock measurement covariance != general covariance`;
- `finite-model measurement success != empirical discovery`;
- `not_established != false`.

## 16. Immediate next step

Proceed to **Stage 10D — per-continuation Born/completeness/positivity covariance**.
