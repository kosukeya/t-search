# Stage 10 Protocol — Fully Typed Future-Measurement Covariance

Status: **Stage 10.0 protocol frozen; Stage 10A completed; criteria 1–16 completed; Stage 10B next.**

Selected Stage 10 gate from Stage 9G:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Stage 10 retains the Stage 9 refined finite-model candidate:

`T10_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

The future-measurement family is an operationally typed structure over this candidate, not assumed to be a new fundamental primitive.

## 1. Frozen central question

Can the Stage 9C future-signature measurement be promoted into a single **fully typed cross-continuation measurement family** whose outcome semantics, effects, normalization rule, probabilities, continuation classes, and event/outcome correspondences remain operationally consistent under the genuine continuation-specific A/B/C clock changes established in Stage 9D?

`state covariance != measurement covariance by definition`.

`same numeric probability != same operational question`.

## 2. Frozen carrier and reference measurement

Stage 10 reuses the merged Stage 9 carrier:

`QExt(e1)={h_L,h_R}`.

Prediction anchor: `e1`.

Future measurement target: `e2`.

Reference Stage 9C measurement:

`M_ref={future_signature_left,future_signature_other}`

with:

`E_left=|psi_L(e2)><psi_L(e2)|`

`E_other=I-E_left`.

The existing Stage 9C normalized-reduced-state Born probabilities remain the operational reference.

`prediction anchor e1 != measurement target e2`.

`reference effect derived from h_L != ontic selector h*`.

## 3. Fully typed measurement-family schema

The frozen schema makes the following resources explicit:

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
- continuation-weight semantics when forming mixtures.

An individual typed effect must be identifiable by:

`(family,continuation,prediction_anchor,target_event,clock,index,outcome,semantics,basis,normalization)`.

The family-level object separately carries the relevant `chi_event`, `chi_class`, and `chi_outcome` resources when those transports are introduced.

`same outcome label != outcome identity`.

`same matrix entries != same typed effect`.

## 4. Normalization remains a scientific decision boundary

Stage 9C uses the Euclidean Born rule on normalized reduced e2 states. Stage 9D clock-change support maps need not be Euclidean-unitary and preserve an induced physical metric instead.

Stage 10 therefore distinguishes candidate representations rather than deciding by fiat:

1. **chart-local POVM representation** — local effects with `sum_o E_o=I` and declared normalized local conditional states;
2. **metric-aware effect-form representation** — local metric `G`, effect forms with `sum_o F_o=G`, and

   `p(o|h)=z^dagger F_o z / (z^dagger G z)`.

Candidate dual transport:

`G_Y=S^{-dagger} G_X S^{-1}`

`F_{o,Y}=S^{-dagger} F_{o,X} S^{-1}`.

This remains a candidate to test in Stage 10B, not an imported theorem.

`metric-aware candidate law != established measurement covariance`.

`normalization convention != mere implementation detail`.

## 5. Strong covariance target

For every canonical continuation and every genuine distinct-clock transport `(X,j)->(Y,k)`, Stage 10 seeks:

`p^h_{X,j}(o)=p^h_{Y,k}(chi_outcome(o))`

within tolerance after event, class, outcome, basis, and normalization typing has been validated.

The comparison is **per-continuation before weighting**.

A full positive result additionally requires valid effects/normalization at every chart, correct transport, probability invariance, route consistency, and semantic correspondence.

`weighted probability equality != per-continuation measurement covariance`.

`effect covariance without outcome typing != full measurement covariance`.

## 6. Composition and route consistency

Stage 10 will extend the Stage 9D 108 genuine ordered distinct-clock state transports and 324 three-clock compositions to the typed measurement family.

For each `X -> Y -> Z` route, composed measurement transport must agree with direct `X -> Z` transport in both numerical representation and outcome correspondence.

`matrix composition consistency != semantic outcome consistency`.

## 7. Mixture, modal, and update layer

Only after per-continuation likelihood covariance is established or refuted are continuation weights restored:

`P_{X,j}(o)=sum_h w_h p^h_{X,j}(o)`.

Canonical modal models remain:

`M_E^QR=(QRCarrier,e1,h*,q_E)`

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`.

Later stages test matched public predictions, hidden epistemic `h*` swap invariance, weight mismatch, and common explicit evidence conditioning/posteriors without creating an ontic selector.

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

Controls must use discriminating valid inputs when one canonical state gives accidental equality.

`accidental probability equality != validated covariance`.

`covariance of a wrongly typed measurement != semantic correctness`.

## 9. Stage 10A — typed reference future-measurement family — completed

Stage 10A introduces `Stage10ReferenceMeasurementFamily`, `Stage10OutcomeIdentity`, and `Stage10TypedReferenceEffect` while leaving the Stage 9C reference question unchanged.

The reference representation is explicitly A/e2 with prediction anchor e1. The common Stage 9C effect pair is typed separately for h_L and h_R, yielding four typed effects total. This is reference typing only; it is not yet the independently derived physical/support lift required by Stage 10B.

Stage 10A independently recomputes each continuation's Born probabilities from the normalized A/e2 reduced state and the typed effect matrices, then compares them with Stage 9C likelihoods.

Established at the reference node:

- canonical outcome identities reproduced;
- canonical effect matrices reproduced within tolerance;
- e1 prediction anchor and e2 target explicitly distinct;
- positivity/Hermiticity/completeness independently revalidated;
- h_L/h_R future rays remain operationally discriminating (`overlap^2 < 1`);
- per-continuation likelihoods reproduce Stage 9C within tolerance;
- public measurement schema has no hidden epistemic selector/modal-type field.

`typed continuation id != hidden selected continuation`.

`reference-node validity != cross-clock measurement covariance`.

Scientific validation: **`783 passed in 461.16s`** (run #1145).

## 10. Stage sequence

- **Stage 10.0 — protocol freeze — completed**;
- **Stage 10A — typed reference future-measurement family — completed**;
- **Stage 10B — continuation-specific measurement lift / normalization choice — next**;
- **Stage 10C — continuation-aware A/B/C measurement transport**;
- **Stage 10D — per-continuation Born/completeness/positivity covariance**;
- **Stage 10E — weights, modal models, and evidence-update covariance**;
- **Stage 10F — ablation / wrong-typing / false-positive controls**;
- **Stage 10G — synthesis and evidence-selected next gate**;
- **criterion 50 — external full-repository regression / merge-readiness review**.

No later stage is considered successful merely because an earlier stage passes.

## 11. Exit-criterion allocation

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

11. A typed reference measurement-family object reproduces the Stage 9C canonical outcomes and effects without semantic change — **satisfied**.
12. Outcome identity/provenance and e1-prediction/e2-target typing are explicit — **satisfied**.
13. Reference positivity/completeness are independently revalidated — **satisfied**.
14. The reference family remains operationally discriminating for h_L/h_R future rays — **satisfied**.
15. Per-continuation reference probabilities reproduce Stage 9C likelihoods within tolerance — **satisfied**.
16. The reference public measurement schema contains no hidden epistemic selector/modal-type field — **satisfied**.

### Stage 10B — criteria 17–23

17. Each continuation receives an independently derived measurement representation on its own physical/support coordinates.
18. No universal h-independent measurement map is assumed where Stage 9D requires continuation-specific maps.
19. Effect/effect-form and normalization objects are mathematically well-defined in the chosen representation.
20. The retained normalization representation is selected by explicit equivalence to the Stage 9C reference, not convenience.
21. Reference-node probabilities agree under the retained representation for both continuations.
22. Continuation-class and outcome correspondences are explicit in the lift.
23. A wrong-continuation lift/map is rejected or produces a discriminating nonzero residual.

### Stage 10C — criteria 24–31

24. Valid typed measurement representations exist at every canonical h_L/h_R A/B/C chart.
25. All genuine ordered distinct-clock measurement transports are tested over the declared atlas.
26. Direct representation transport agrees with reconstruction through the shared physical object where applicable.
27. Three-clock measurement compositions agree with direct transport within tolerance.
28. Completeness is covariant in the declared normalization convention.
29. Positivity/self-adjointness requirements are covariant in the declared convention.
30. Outcome identity and event/class correspondence remain valid at every node.
31. Bare-effect and wrong-event/class controls do not pass as semantically valid covariance.

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

44. Removing event/class/outcome correspondence exposes which typed identifications become `not_established` while retaining executable bare transport where applicable.
45. Removing/corrupting normalization semantics classifies probability covariance as lost, underdetermined, or not established as warranted.
46. Bare-effect, wrong-continuation, wrong-outcome, wrong-event, and weight-misalignment controls receive explicit witnesses/residuals.
47. Reconstruction/ablation results use the project functional-status vocabulary without metaphysical promotion.

### Stage 10G — criteria 48–49

48. Executable synthesis selects among at least `measurement_covariant`, `measurement_partial`, `measurement_obstructed`, or `inconclusive`.
49. The next gate is evidence-selected from remaining unresolved boundaries.

### Criterion 50

50. External final full-repository regression and merge-readiness review close Stage 10 only after criteria 1–49 are satisfied or explicitly resolved.

## 12. Status vocabulary

`preserved / reconstructible / inaccessible / lost / underdetermined / not_established / compatible / implication_refuted`.

Overall measurement-covariance status additionally permits:

`established / partial / refuted / not_established`.

`not_established != false`.

`refuted measurement covariance != ontological becoming`.

## 13. Interpretation guards

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
- `full finite-clock measurement covariance != general covariance`;
- `finite-model measurement success != empirical discovery`;
- `not_established != false`.

## 14. Immediate next step

Proceed to **Stage 10B — continuation-specific measurement lift / normalization choice**.
