# Stage 10 Protocol — Fully Typed Future-Measurement Covariance

Status: **Stage 10.0 protocol frozen; criteria 1–10 completed; Stage 10A next.**

Selected Stage 10 gate from Stage 9G:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Stage 10 retains the Stage 9 refined finite-model candidate:

`T10_candidate=(O,P,R,V;Xi)`

with:

`R=(R_content,R_direction,R_access)`

`V=(V_extension,V_semantics,V_weights)`.

The future-measurement family is an operationally typed structure over this candidate. Stage 10 does **not** assume that it is a new fundamental primitive.

## 1. Frozen central question

Can the Stage 9C future-signature measurement be promoted from one reference representation into a single **fully typed cross-continuation measurement family** whose outcome semantics, effects, normalization rule, probabilities, continuation classes, and event/outcome correspondences remain operationally consistent under the genuine continuation-specific A/B/C clock changes established in Stage 9D?

Equivalently, Stage 10 asks whether:

`state / record / class / weight covariance`

can be strengthened to:

`fully typed future-measurement-family covariance`.

A positive result is not assumed in advance.

`state covariance != measurement covariance by definition`.

`same numeric probability != same operational question`.

## 2. Frozen carrier and reference measurement

Stage 10 must reuse the merged Stage 9 carrier rather than changing the physical dynamics while testing measurement covariance.

Canonical carrier:

`QExt(e1)={h_L,h_R}`.

Prediction anchor:

`D_*=e1`.

Future measurement target:

`F_*=e2`.

Reference Stage 9C measurement:

`M_ref={future_signature_left,future_signature_other}`

with canonical reference effects derived from the Stage 9C e2 continuation rays:

`E_left=|psi_L(e2)><psi_L(e2)|`

`E_other=I-E_left`.

The reference operational probabilities are the existing Stage 9C normalized-reduced-state Born probabilities. Stage 10 must reproduce these probabilities; it must not silently redefine the original future-signature question.

`prediction anchor e1 != measurement target e2`.

`reference effect derived from h_L != ontic selector h*`.

## 3. Fully typed measurement-family schema

A Stage 10 measurement representation must make the following resources explicit rather than infer them from array position or string coincidence:

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

At minimum, an individual typed effect must be identifiable by:

`(family,continuation,prediction_anchor,target_event,clock,index,outcome,semantics,basis,normalization)`.

The family-level object must separately carry the relevant `chi_event`, `chi_class`, and `chi_outcome` resources.

`same outcome label != outcome identity`.

`same matrix entries != same typed effect`.

## 4. Frozen normalization rule and decision boundary

Stage 9C defines its reference measurement using the ordinary Euclidean Born rule on normalized reduced e2 states. Stage 9D, however, showed that genuine clock-change support maps need not be Euclidean-unitary and preserve an induced physical metric instead.

Stage 10 therefore does **not** assume in the protocol that one normalization representation is automatically correct.

Two mathematically possible representations may be tested:

1. **chart-local POVM representation**
   - local effects `E_o`;
   - local completeness `sum_o E_o=I`;
   - probabilities evaluated using the declared normalized local conditional state;

2. **metric-aware effect-form representation**
   - local metric `G`;
   - local effect forms `F_o`;
   - completeness `sum_o F_o=G`;
   - probabilities

     `p(o|h)=z^dagger F_o z / (z^dagger G z)`.

For a clock map `z_Y=S z_X`, a metric-aware candidate transport has the dual form:

`G_Y=S^{-dagger} G_X S^{-1}`

`F_{o,Y}=S^{-dagger} F_{o,X} S^{-1}`.

This is a **candidate representation law to test**, not a frozen positive result.

Whichever representation is retained after Stage 10A/B must satisfy all of the following:

- it reproduces the exact Stage 9C reference probabilities at the reference node;
- one normalization convention is declared consistently rather than switched ad hoc between charts;
- positivity and completeness are verified in the appropriate declared sense;
- transported probabilities are computed from the transported typed measurement, not inserted from the reference result;
- a deliberately wrong normalization/metric control is detectable.

`metric-aware candidate law != established measurement covariance`.

`normalization convention != mere implementation detail`.

## 5. Strong per-continuation covariance criterion

For each canonical continuation `h in {h_L,h_R}`, each genuine distinct-clock transport

`(X,j) -> (Y,k)`

from the Stage 9D continuation-specific atlas, and every declared outcome `o`, Stage 10 seeks:

`p^h_{X,j}(o)=p^h_{Y,k}(chi_outcome(o))`

within the declared numerical tolerance, **after** the event, class, outcome, basis, and normalization typings have been validated.

The comparison must be performed before continuation-weight aggregation.

A positive full-family result additionally requires:

- valid measurement representation at every canonical chart;
- correct effect transport;
- correct normalization transport;
- probability invariance;
- direct-vs-composed measurement transport consistency;
- outcome identity preservation;
- event/class correspondence validity.

`weighted probability equality != per-continuation measurement covariance`.

`effect covariance without outcome typing != full measurement covariance`.

## 6. Composition and route consistency

Stage 9D established 108 genuine ordered distinct-clock state transports and 324 three-clock compositions for the two-continuation A/B/C atlas.

Stage 10 must pressure-test the measurement family over the same declared atlas rather than only checking one A-to-B example.

For each valid continuation-specific route:

`X -> Y -> Z`

measurement transport by composition must agree with direct:

`X -> Z`

in the appropriate typed representation.

The comparison must include both effect/effect-form representation and outcome correspondence.

`matrix composition consistency != semantic outcome consistency`.

## 7. Mixture, modal, and update covariance

After per-continuation likelihood covariance is established or refuted, Stage 10 must restore continuation weights and Stage 9C modal roles.

For declared weights `w_h`:

`P_{X,j}(o)=sum_h w_h p^h_{X,j}(o)`.

Under valid class/weight/outcome correspondence, Stage 10 tests whether:

`P_{X,j}(o)=P_{Y,k}(chi_outcome(o))`.

The canonical matched models remain:

`M_E^QR=(QRCarrier,e1,h*,q_E)`

and

`M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)`.

Stage 10 must test, rather than assume, whether Stage 9C operational underdetermination survives the fully transported measurement family:

- matched `q_E=K` public predictions across all charts;
- hidden epistemic `h*` swap remains outside the public measurement schema;
- weight mismatch remains operationally visible in every correctly corresponding chart;
- common explicit evidence produces chart-independent likelihood conditioning/posteriors;
- the ontic-extension update remains selector-free.

`measurement covariance != modal/ontological identity`.

`weight covariance != selected-continuation observability`.

`evidence-update covariance != ontological becoming`.

## 8. Frozen negative controls

Stage 10 must include controls designed to catch numerical false positives and typing errors.

At minimum:

1. **bare-effect reuse** — reuse a source-chart effect matrix in a distinct chart without the required representation transport;
2. **wrong-continuation map** — use an h_L-derived measurement transport on h_R or vice versa;
3. **swapped continuation classes** — misidentify h_L and h_R while keeping numeric arrays otherwise plausible;
4. **swapped/misdeclared outcomes** — exchange `future_signature_left` and `future_signature_other` or claim an identity outcome map while applying a swap;
5. **anchor/target confusion** — identify prediction anchor e1 with measurement target e2;
6. **wrong/missing event correspondence** — remove or reverse the relational-event typing while declaring preservation;
7. **wrong normalization/metric** — evaluate a transported family with an undeclared or mismatched inner product/metric;
8. **weight misalignment** — keep weights numerically fixed while applying the wrong continuation-class correspondence;
9. **outcome-typing removal** — retain arrays but remove the semantic outcome correspondence;
10. **mixed normalization convention** — switch between incompatible probability conventions across charts to manufacture equality.

A control may show accidental equality for one special state. Such an equality is not sufficient; the control must be tested on a discriminating set of canonical/perturbed valid inputs where needed.

`accidental probability equality != validated covariance`.

`covariance of a wrongly typed measurement != semantic correctness`.

## 9. Stage sequence

Stage 10 is frozen as:

- **Stage 10.0 — protocol freeze**;
- **Stage 10A — typed reference future-measurement family**;
- **Stage 10B — continuation-specific measurement lift / normalization choice**;
- **Stage 10C — continuation-aware A/B/C measurement transport**;
- **Stage 10D — per-continuation Born/completeness/positivity covariance**;
- **Stage 10E — weights, modal models, and evidence-update covariance**;
- **Stage 10F — ablation / wrong-typing / false-positive controls**;
- **Stage 10G — synthesis and evidence-selected next gate**;
- **criterion 50 — external full-repository regression / merge-readiness review**.

No later stage is considered successful merely because an earlier stage passes.

## 10. Frozen exit-criterion allocation

### Stage 10.0 — criteria 1–10

1. The exact Stage 9G-selected Stage 10 gate is frozen.
2. Stage 10 reuses the merged Stage 9 h_L/h_R constrained carrier and does not alter its dynamics to manufacture covariance.
3. The Stage 9C reference future-signature outcomes/effects/probabilities are frozen as the operational reference.
4. Prediction anchor e1 and future measurement target e2 are typed separately.
5. Measurement-family/effect schema explicitly includes continuation, perspective, event, outcome, basis, normalization, and provenance typing.
6. Normalization is a scientific decision boundary: candidate chart-local and metric-aware representations are distinguished, and neither is declared successful by fiat.
7. Strong covariance requires per-continuation typed probability equality before weighting plus effect/normalization validity and route consistency.
8. Mixture/modal/update covariance is separately required after per-continuation covariance.
9. Wrong-continuation, wrong-outcome, wrong-event, wrong-normalization, bare-effect, weight, and typing controls are frozen.
10. Interpretation guards, stage sequence, status vocabulary, and criteria 11–50 allocation are frozen.

### Stage 10A — criteria 11–16

11. A typed reference measurement-family object reproduces the Stage 9C canonical outcomes and effects without semantic change.
12. Outcome identity/provenance and e1-prediction/e2-target typing are explicit.
13. Reference positivity/completeness are independently revalidated.
14. The reference family remains operationally discriminating for h_L/h_R future rays.
15. Per-continuation reference probabilities reproduce Stage 9C likelihoods within tolerance.
16. The reference public measurement schema contains no hidden epistemic selector/modal-type field.

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
31. Bare-effect and wrong-event/class transport controls do not pass as semantically valid covariance.

### Stage 10D — criteria 32–38

32. Per-continuation outcome probabilities are invariant across all declared corresponding clock nodes.
33. Every transported chart reproduces the Stage 9C reference likelihoods for each continuation/outcome.
34. Per-continuation likelihood covariance is established before branch-weight aggregation.
35. Swapped/misdeclared outcome correspondence is detected.
36. Wrong normalization/metric use is detected on a discriminating input family.
37. Accidental canonical-state equality is ruled out where necessary by additional valid discriminating inputs.
38. Full typed future-measurement covariance receives an explicit evidence status (`established`, `partial`, `refuted`, or `not_established`) rather than being inferred from state covariance.

### Stage 10E — criteria 39–43

39. Weighted future predictions are covariant under valid continuation-class/weight/outcome correspondence.
40. Matched epistemic/ontic-extension public measurement views agree across all declared clock nodes if supported by the evidence.
41. Hidden epistemic h* swaps remain outside the public typed measurement schema.
42. Weight mismatch remains predictively visible with the same transported operational meaning across perspectives.
43. Common evidence conditioning/posteriors are perspective-consistent and the ontic-extension update remains selector-free.

### Stage 10F — criteria 44–47

44. Removing event/class/outcome correspondence separately exposes which typed identifications become `not_established` while retaining any still-executable bare transport.
45. Removing or corrupting normalization semantics exposes whether probability covariance is lost, underdetermined, or merely not established.
46. Bare-effect, wrong-continuation, wrong-outcome, wrong-event, and weight-misalignment controls are classified with explicit witnesses/residuals.
47. Reconstruction/ablation results use the established functional-status vocabulary without promoting loss or reconstruction to metaphysical necessity/redundancy.

### Stage 10G — criteria 48–49

48. An executable synthesis selects among at least `measurement_covariant`, `measurement_partial`, `measurement_obstructed`, or `inconclusive` according to the accumulated evidence.
49. The next gate is evidence-selected from remaining unresolved boundaries rather than fixed in advance.

### Criterion 50

50. External final full-repository regression and merge-readiness review close Stage 10 only after criteria 1–49 are satisfied or explicitly resolved according to the protocol.

## 11. Status vocabulary

Stage 10 retains the project vocabulary where appropriate:

`preserved / reconstructible / inaccessible / lost / underdetermined / not_established / compatible / implication_refuted`.

For the overall measurement-covariance gate it additionally permits:

`established / partial / refuted / not_established`.

`not_established != false`.

`refuted measurement covariance != ontological becoming`.

## 12. Interpretation guards

Stage 10 must preserve at least the following boundaries:

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

## 13. Immediate next step

Proceed to **Stage 10A — typed reference future-measurement family** using the merged Stage 9C canonical future-signature measurement as the unchanged operational reference.
