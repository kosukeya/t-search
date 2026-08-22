# Stage 10 Protocol — Fully Typed Future-Measurement Covariance

Status: **Stage 10.0 through Stage 10G completed; criteria 1–49 completed; criterion 50 final external full-repository regression / merge-readiness review pending.**

Historical checkpoint retained for consistency: **Stage 10A and Stage 10B completed; criteria 1–23 completed.**

Selected Stage 10 gate from Stage 9G:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Stage 10 retains `T10_candidate=(O,P,R,V;Xi)` with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

## 1. Frozen question and carrier

The frozen question is whether the Stage 9C reference future-signature measurement can be promoted to one fully typed cross-continuation measurement family whose effects, normalization, outcome semantics, probabilities, event roles, continuation classes, and correspondences remain operationally consistent under genuine continuation-aware A/B/C clock changes.

Carrier: `QExt(e1)={h_L,h_R}`.

Prediction anchor: `e1`. Measurement target: `e2`.

Stage 9C reference outcomes: `future_signature_left` and `future_signature_other`.

`prediction anchor e1 != measurement target e2`.

`typed continuation id != hidden selected continuation`.

`reference-node validity != cross-clock measurement covariance`.

## 2. Frozen measurement typing

The explicit schema retains:

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

`same outcome label != outcome identity`.

`same matrix entries != same typed effect`.

## 3. Normalization and strong covariance target

The Stage 10.0 decision boundary compared a chart-local POVM with a metric-aware effect-form description. The metric-aware notation was frozen as `sum_o F_o=G` with probability proportional to `z^dagger F_o z` and normalization `z^dagger G z`.

Stage 10B selected a reference-induced effect form and operational normalization derived from the Stage 9C reference. Genuine clock maps are non-Euclidean-unitary, so numerical identity is not independently reset in every chart.

`metric-aware candidate law != established measurement covariance`.

`normalization convention != mere implementation detail`.

`reference-chart identity normalization != identity normalization in every transported chart`.

`normalization representation selected != measurement covariance established` at the Stage 10B checkpoint.

The strong frozen criterion compares `p^h_{X,j}(o)` and `p^h_{Y,k}(chi_outcome(o))` **per-continuation before weighting**.

`weighted probability equality != per-continuation measurement covariance`.

`effect covariance without outcome typing != full measurement covariance`.

## 4. Modal/update separation

Only after per-continuation covariance are weights restored.

`M_E^QR=(QRCarrier,e1,h*,q_E)`

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`

The public interface keeps the hidden epistemic `h*` swap outside the schema, includes a weight mismatch control, and uses common explicit evidence for update comparison.

`measurement covariance != modal/ontological identity`.

`evidence-update covariance != ontological becoming`.

## 5. Frozen negative controls

The protocol includes bare-effect reuse, wrong-continuation map, swapped continuation classes, swapped/misdeclared outcomes, anchor/target confusion, wrong/missing event correspondence, wrong normalization/metric, weight misalignment, outcome-typing removal, and mixed normalization convention.

Explicit Stage 10F witnesses include wrong continuation use, wrong outcome typing, wrong event typing, weight misalignment, and fresh numerical identity normalization.

`accidental probability equality != validated covariance`.

`covariance of a wrongly typed measurement != semantic correctness`.

## 6. Stage checkpoints

### Stage 10.0 — protocol freeze — completed

Criteria 1–10 were frozen before later implementation. Validation: run #1139, `776 passed in 459.33s`.

### Stage 10A — typed reference future-measurement family — completed

The Stage 9C reference outcomes/effects/probabilities are reproduced with explicit e1/e2 and continuation typing. Scientific validation: run #1145, **`783 passed in 461.16s`**; documentation-synchronized regression: run #1157, `787 passed in 465.49s`.

### Stage 10B — continuation-specific measurement lift / normalization choice — completed

The h_L/h_R reference-induced support and physical effect-form lifts reproduce Stage 9C likelihoods and reject cross-continuation misuse. Scientific validation: run #1163, **`795 passed in 462.74s`**; documentation-synchronized regression: run #1179, `800 passed in 372.79s`.

### Stage 10C — continuation-aware A/B/C measurement transport — completed

Every continuation has nine chart representations, giving **18** charts. All **108** genuine ordered distinct-clock transports and **324** three-clock compositions are tested using dual transport `H^Y=S^{-dagger} H^X S^{-1}` and agree with direct reconstruction within the frozen tolerance. Completeness transports as `sum F=N`; positivity/Hermiticity and event/class/outcome typing are checked.

`future-measurement representation covariance = established`.

Historical Stage 10C boundary: `full per-continuation probability covariance = not_established`.

`measurement representation covariance != probability covariance by definition`.

Scientific validation: run #1185, **`809 passed in 476.21s`**; documentation-synchronized regression: run #1203, `815 passed in 471.02s`.

### Stage 10D — per-continuation Born/completeness/positivity covariance — completed

Stage 10D closes the Stage 10C probability boundary before weighting. A **196**-state Hermitian-tomography-complete constrained probe family yields **7056** probe outcome evaluations. Fresh identity normalization, a genuinely misaligned metric, and swapped outcomes are rejected.

`full typed future-measurement covariance = established` within the explicit per-continuation / pre-weighting / finite typed atlas scope.

Historical Stage 10D boundary: `weighted/modal/update covariance = not_established`.

Pilot #1209: `818 passed / 4 failed`; corrected scientific run #1213: **`823 passed in 311.17s`**; corrected documentation regression #1227: `828 passed in 381.47s`.

`typed-resource distinction != numerical inequality`.

### Stage 10E — weights, modal models, and evidence-update covariance — completed

Weights, matched epistemic/ontic-extension public views, hidden-selector swap controls, weight mismatch, and common evidence posteriors are transported consistently.

`weighted/modal/update operational covariance = established`.

Scientific validation: run #1233, **`834 passed in 455.24s`**; documentation-synchronized regression: run #1243, `839 passed in 455.87s`.

### Stage 10F — ablation / wrong-typing / false-positive controls — completed

Event correspondence, continuation-class correspondence, outcome correspondence, normalization semantics, and continuation-weight alignment are ablated or corrupted. Preserved/reconstructible numerical payload does not license typed identity when correspondence is absent; explicitly wrong rules are refuted.

`numerical reconstructibility != typed operational identification`.

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`not_established != false`.

`finite-model ablation != fundamental ontology`.

Scientific validation: run #1249, **`843 passed in 575.02s`**.

### Stage 10G — synthesis and evidence-selected next gate — completed

Frozen synthesis vocabulary: `measurement_covariant`, `measurement_partial`, `measurement_obstructed`, `inconclusive`.

Executable result: `measurement_covariant`.

The Stage 9 measurement boundary is closed only for the declared finite typed family. Current Stage 10G regression: run #1267, **`863 passed in 644.50s`**.

Stage 10G selects:

> **Construct a parametrized covariance precursor that preserves the typed O/P/R/V measurement architecture without assuming a preferred external time parameterization.**

Gate ranking: `parametrized_covariance_precursor=9`, `richer_causal_order=7`, `nonideal_povm_clocks=6`.

`parametrized covariance precursor != general relativity`.

## 7. Sequence and exit-criterion allocation

Stage 10.0 — completed; criteria 1–10.

Stage 10A — completed; criteria 11–16.

Stage 10B — completed; criteria 17–23.

Stage 10C — completed; criteria 24–31.

Stage 10D — completed; criteria 32–38.

Stage 10E — completed; criteria 39–43.

Stage 10F — completed; criteria 44–47.

Stage 10G — completed; criteria 48–49.

Criterion 50 — external final full-repository regression / merge-readiness review — pending.

### Criteria 1–10 — Stage 10.0

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

### Criteria 11–16 — Stage 10A

11. Typed reference measurement reproduces Stage 9C outcomes/effects — **satisfied**.
12. Outcome provenance and e1/e2 typing explicit — **satisfied**.
13. Reference positivity/completeness revalidated — **satisfied**.
14. Reference measurement remains operationally discriminating — **satisfied**.
15. Per-continuation reference probabilities reproduce Stage 9C — **satisfied**.
16. Public reference schema contains no hidden selector/modal-type field — **satisfied**.

### Criteria 17–23 — Stage 10B

17. Independent continuation-specific support/physical lifts — **satisfied**.
18. No universal continuation-independent lift assumed — **satisfied**.
19. Effect forms and normalization are well defined — **satisfied**.
20. Normalization representation selected by reference equivalence and nonunitarity — **satisfied**.
21. Support and physical forms reproduce Stage 9C likelihoods — **satisfied**.
22. Class and outcome correspondences explicit — **satisfied**.
23. Wrong-continuation lift use rejected — **satisfied**.

### Criteria 24–31 — Stage 10C

24. All canonical measurement chart representations exist and are typed — **satisfied**.
25. All genuine ordered distinct-clock measurement transports tested — **satisfied**.
26. Dual transport matches direct physical reconstruction — **satisfied**.
27. Three-clock compositions match direct transport — **satisfied**.
28. Completeness is covariant — **satisfied**.
29. Positivity and Hermiticity are covariant — **satisfied**.
30. Outcome/event/class typing remains valid — **satisfied**.
31. Bare-effect and wrong event/class controls rejected — **satisfied**.

### Criteria 32–38 — Stage 10D

32. Per-continuation Born probabilities evaluated at every chart — **satisfied**.
33. Corresponding-chart probabilities agree — **satisfied**.
34. Stage 9C likelihoods reproduced — **satisfied**.
35. Probability completeness and positivity retained — **satisfied**.
36. Tomography-complete probes exclude accidental canonical equality — **satisfied**.
37. Wrong normalization/metric/outcome controls rejected — **satisfied**.
38. Strong per-continuation measurement covariance classified established — **satisfied**.

### Criteria 39–43 — Stage 10E

39. Weighted predictions are perspective-covariant — **satisfied**.
40. Matched modal public views remain equal while privileged roles remain distinct — **satisfied**.
41. Hidden h* swap and public-schema guards pass — **satisfied**.
42. Weight mismatch remains visible and covariant — **satisfied**.
43. Common evidence update/posteriors are covariant — **satisfied**.

### Criteria 44–47 — Stage 10F

44. Correspondence removals classified with typed status vocabulary — **satisfied**.
45. Normalization removal/corruption classified — **satisfied**.
46. False-positive controls have explicit witnesses/residuals — **satisfied**.
47. Ablation results avoid metaphysical promotion — **satisfied**.

### Criteria 48–49 — Stage 10G

48. Executable synthesis selects `measurement_covariant` from Stage 10A–F evidence — **satisfied**.
49. The next gate is evidence-selected as `parametrized_covariance_precursor` — **satisfied**.

### Criterion 50 — external repository validation

50. External final full-repository regression and merge-readiness review — **pending** until the documentation-synchronized branch head passes and PR #11 is checked for mergeability, base freshness, and review blockers.

## 8. Interpretation guards

- `future-measurement covariance != future actuality`;
- `future-measurement covariance != ontic future openness`;
- `future-measurement covariance != hidden selected future`;
- `measurement-covariance failure != ontological becoming`;
- `measurement covariance != refutation of ontological becoming`;
- `perspective-invariant future probabilities != proof of eternalism`;
- `full finite-clock measurement covariance != general covariance`;
- `finite clock covariance != general covariance`;
- `finite-model measurement success != empirical discovery`;
- `typed-resource necessity != metaphysical fundamentality`;
- `not_established != false`.
