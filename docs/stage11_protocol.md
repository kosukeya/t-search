# Stage 11 Protocol — Parametrized Covariance Precursor

Status: **Stage 11.0, Stage 11A, and Stage 11B completed; criteria 1–23 satisfied; criteria 24–50 pending implementation and external review.**

Selected Stage 11 gate from Stage 10G:

> **Construct a parametrized covariance precursor that preserves the typed O/P/R/V measurement architecture without assuming a preferred external time parameterization.**

Stage 11 carries forward, without metaphysical promotion,

`T10_candidate=(O,P,R,V;Xi)`

with

`R=(R_content,R_direction,R_access)`

and

`V=(V_extension,V_semantics,V_weights)`.

The Stage 10 bounded result carried into Stage 11 remains

`fully typed finite future-measurement covariance = established`.

The project boundary remains

`finite clock covariance != general covariance`.

## 1. Frozen scientific question

Stage 11 asks whether a preferred external trajectory parameter is necessary for the Stage 10 relational/clock/modal/record/measurement structure, or whether the same typed physical relational history can be represented across admissible external parameterizations.

The strongest later target, only if the full Stage 11A–F evidence warrants it, is

`finite typed parametrized covariance precursor = established`.

Stage 11G classification vocabulary remains frozen as:

- `parametrized_covariant`;
- `parametrized_partial`;
- `parametrized_obstructed`;
- `inconclusive`.

`parametrized_covariant` may be selected only from the complete Stage 11A–F evidence chain.

## 2. Frozen type distinctions

The following objects remain typed separately:

- external parameterization identity `rho`;
- external parameter label/value `lambda_rho`;
- physical event identity `e`;
- internal clock perspective `X in {A,B,C}`;
- internal clock reading `tau_X`;
- continuation identity/class `h in {h_L,h_R}` where applicable;
- prediction anchor and measurement target;
- measurement-family identity;
- outcome identity/semantics/provenance;
- normalization/inner-product convention;
- continuation-weight semantics;
- parameter-event correspondence;
- inherited clock/event/class/outcome correspondences.

Frozen guards:

`parameter label != internal clock reading`.

`parameter label != event identity`.

`internal clock perspective != external parameterization`.

`same numerical parameter value != same physical event`.

`same physical event != same parameter value across parameterizations`.

`parameterization correspondence != event identity`.

## 3. Stage 11A parametrized constrained precursor

The minimal precursor uses canonical variables

`(T,p_T;q,p)`

and constraint

`C = p_T + H(q,p) approx 0`.

The deterministic seed is

`H(q,p)=p^2/2`

with `p=1.25`, `p_T=-p^2/2`, positive nonconstant lapse

`N(lambda)=1+lambda^2/4`,

and internal clock

`T(lambda)=lambda+lambda^3/12`.

The configuration seed is

`q(T)=-0.35+1.25 T`.

The external label `lambda` is not interpreted as physical time. For a phase-space quantity `z`, the precursor notation is

`dz/dlambda = N(lambda) {z,H}`.

This classical scaffold tests parameter redundancy only.

`classical parametrized precursor != fundamental classical ontology`.

## 4. Frozen admissible reparameterization family

Positive/admissible maps are smooth, injective on the tested domain, strictly monotone, and orientation-preserving:

`lambda' = f(lambda)` with `f'(lambda) > 0`.

The frozen minimum family is implemented exactly as:

1. identity: `f_id(lambda)=lambda`;
2. positive affine: `f_aff(lambda)=2 lambda + 1`;
3. nonlinear cubic: `f_cub(lambda)=lambda + lambda^3/4`;
4. nonlinear hyperbolic: `f_sinh(lambda)=sinh(lambda)`.

The lapse-like rate transforms by

`N'(lambda') = N(lambda) dlambda/dlambda' = N(lambda)/f'(lambda)`.

Raw parameter derivatives generally differ:

`dq/dlambda != dq/dlambda'`.

The relational derivative candidate is

`dq/dT = (dq/dlambda)/(dT/dlambda) = (dq/dlambda')/(dT/dlambda')`.

`raw parameter derivative equality != reparameterization covariance criterion`.

## 5. Stage 11A physical-event carrier and result

Stage 11A samples 13 explicit physical events on source-label domain `[-1.5,1.5]`:

`orbit_event_00 ... orbit_event_12`.

Representations are compared through explicit typed event correspondence

`chi_event^{rho->sigma}: e_rho -> e_sigma`

while allowing

`lambda_rho(e) != lambda_sigma(e)`.

The Stage 11A diagnostics establish:

- event count: **13**;
- positive parameterization count: **4**;
- minimum transformed positive lapse: **0.5**;
- maximum constraint residual: **0.0**;
- maximum lapse chain-rule residual: **0.0**;
- maximum `T/q/p/p_T` orbit residual: **0.0**;
- corresponding event pairs with different raw parameter labels: **36**;
- nonlinear-map sample points with different raw `dq/dlambda` rates: **24**.

Orientation reversal `f_rev(lambda)=-lambda` and non-injective `f_noninj(lambda)=lambda^2` on the both-sign domain remain excluded controls.

Bounded Stage 11A result:

`minimal Stage 11A constraint orbit preservation = established`.

Repository-level Stage 11A checkpoint: run #1309 — **`883 passed in 630.96s (0:10:30)`**.

`same constraint orbit != established general covariance`.

## 6. Stage 11B relational observable and derivative checkpoint

Stage 11B constructs the sampled relational observable

`q(T=tau)`

at unique internal-clock readings and compares charts only after explicit physical-event correspondence.

Across 4 positive parameterizations × 13 events:

- relational-observable evaluations: **52**;
- maximum corresponding-event `q(T=tau)` residual: **0.0** within the deterministic carrier;
- relational-derivative evaluations: **52**;
- reconstructed `dq/dT`: **1.25**;
- maximum cross-parameterization relational-derivative residual: **0.0** within tolerance;
- maximum residual of `dq/dT` against momentum `p`: **0.0** within tolerance.

The nonlinear cubic and hyperbolic charts still differ from identity in raw `dq/dlambda` at **24** sampled chart-event points; the largest raw-rate difference is approximately **1.2263808139534884**.

Stage 11B keeps explicit precursor event roles:

- prediction anchor: `orbit_event_06`;
- measurement target: `orbit_event_10`;
- typed anchor/target views across the four parameterizations: **8**.

These precursor roles do not replace the Stage 10 quantum `e1 -> e2` measurement typing; that lift is reserved for Stage 11D.

### Equal-raw-parameter false comparison

Identity versus affine has **7** equal numerical raw-parameter overlaps. Only **1** is also the same explicit physical event; **6** pair different physical event ids and different internal-clock readings.

The executable classification is

`invalid_equal_raw_parameter_event_rule`.

Therefore

`equal raw lambda != physical-event correspondence`.

Bounded Stage 11B result:

`Stage 11B relational observable/derivative covariance on the frozen positive family = established`.

Stage 11B validation checkpoints:

- source/result checkpoint run #1319 — **`890 passed in 640.07s (0:10:40)`**;
- documentation-synchronized current-head run #1327 — **`891 passed in 628.78s (0:10:28)`**.

These are repository-validation checkpoints only:

`repository validation != new scientific evidence`.

This Stage 11B result is narrower than O/P/R/V or measurement covariance.

`relational covariance on one finite orbit != general covariance`.

## 7. Frozen O/P/R/V/Xi lift target

Stage 11C must now transport/reconstruct the full typed architecture across admissible parameterizations.

### O

`O` is attached to typed physical relational events, not bare parameter values.

### P

The Stage 10 modal extension carrier remains

`QExt(e1)={h_L,h_R}`.

Stage 11C tests

`QExt^rho(e1) ~= QExt^sigma(e1)`

under explicit continuation/event correspondence.

`reparameterization invariance of QExt != ontic future openness`.

### R

`R=(R_content,R_direction,R_access)` is transported under orientation-preserving maps without defining physical direction from increasing `lambda`.

`parameter orientation != physical record direction by definition`.

### V

`V=(V_extension,V_semantics,V_weights)` is transported/reconstructed with continuation/class alignment and weight semantics explicit.

### Xi

Stage 11 extends `Xi` with at least:

- parameterization identity;
- parameter-event correspondence;
- lapse/rate transformation semantics;
- inherited clock/event/class/outcome correspondences;
- normalization convention;
- continuation-weight semantics.

`typed-resource use != metaphysical fundamentality`.

## 8. Frozen Stage 10 measurement carry-over

Stage 11D must reuse the Stage 10 future-signature measurement family rather than redesigning it after seeing reparameterization results.

Reference anchor: `e1`.

Reference target: `e2`.

Reference continuation carrier: `QExt(e1)={h_L,h_R}`.

Reference outcomes:

- `future_signature_left`;
- `future_signature_other`.

The Stage 10 probability form remains

`p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

The Stage 11D comparison target is

`p_rho(o|h,e1->e2) = p_sigma(o|h,e1->e2)`

for corresponding typed physical events, not equality at the same raw parameter value.

## 9. Frozen clock-change × reparameterization compatibility target

Let `G_{rho->sigma}` denote admissible reparameterization transport and `C_{X->Y}` the Stage 10 genuine internal-clock transport.

Stage 11E tests

`C_{X->Y} o G_{rho->sigma} ~= G_{rho->sigma} o C_{X->Y}`

for typed corresponding physical objects.

The comparison must eventually cover:

- O/event data;
- continuation/modal typing;
- measurement effects/normalization roles;
- per-continuation probabilities;
- weighted predictions and evidence-update outputs.

All A/B/C internal-clock perspectives and all four frozen positive parameterizations must participate.

`internal-clock covariance != reparameterization covariance`.

`commuting typed diagram != general covariance`.

## 10. Frozen negative and false-positive controls

The original controls remain frozen:

1. raw-equal-parameter matching: identify events only because `lambda_rho=lambda_sigma`;
2. wrong/missing parameter-event correspondence;
3. omit the lapse transformation and reuse `N` numerically under nonlinear `f`;
4. use the wrong derivative Jacobian in `N'`;
5. use a non-injective map such as `f_noninj(lambda)=lambda^2` on a domain containing both signs;
6. orientation reversal `f_rev(lambda)=-lambda` outside the initial positive gauge family;
7. wrong continuation/class correspondence;
8. wrong measurement outcome correspondence;
9. wrong normalization semantics;
10. parameter-dependent corruption of a physical O/P/R/V or measurement payload while preserving superficial labels;
11. identify parameter direction with `R_direction` by definition;
12. mix parameterizations inside one probability/weight/update calculation without typed correspondence.

Stage 11A implements controls 5 and 6 as excluded parameterizations. Stage 11B supplies an explicit control for item 1: 7 equal raw-label overlaps contain 6 false event identifications.

`orientation reversal != physical record reversal by definition`.

`orientation-preserving reparameterization != time reversal`.

`non-injective relabeling != admissible reparameterization`.

## 11. Anti-triviality requirements

A positive Stage 11 synthesis may not be based only on unchanged labels.

Evidence already obtained:

- **36** genuinely different numerical parameter labels for corresponding events;
- **24** nonlinear raw-derivative differences;
- correct transformed lapse with zero chain-rule residual;
- **52** covariant `q(T=tau)` evaluations;
- **52** covariant `dq/dT` evaluations;
- explicit rejection/classification of raw-equal-parameter event matching.

Still pending:

- preserved/reconstructed O/P/R/V typing;
- preserved Stage 10 measurement probabilities;
- clock-change × reparameterization compatibility;
- remaining frozen ablations/controls.

`same labels after relabeling != sufficient evidence of covariance`.

## 12. Stage sequence and exit-criterion allocation

### Stage 11.0 — protocol freeze — completed

Criteria 1–10.

External regression after freeze: run #1285, `874 passed in 640.88s (0:10:40)`.

### Stage 11A — minimal parametrized constrained carrier and admissible family — completed

Criteria 11–16.

Repository-level Stage 11A checkpoint: run #1309, `883 passed in 630.96s (0:10:30)`.

### Stage 11B — relational observables and relational derivatives — completed

Criteria 17–23.

Source/result checkpoint: run #1319, `890 passed in 640.07s (0:10:40)`.

Documentation-synchronized current-head checkpoint: run #1327, `891 passed in 628.78s (0:10:28)`.

### Stage 11C — typed O/P/R/V/Xi lift — next

Criteria 24–31.

### Stage 11D — future-measurement reparameterization covariance

Criteria 32–38.

### Stage 11E — clock-change × parameterization compatibility

Criteria 39–43.

### Stage 11F — ablation / wrong-gauge / false-positive controls

Criteria 44–47.

### Stage 11G — synthesis and evidence-selected next gate

Criteria 48–49.

### Criterion 50 — external final repository validation

Final full-repository regression / merge-readiness review only after Stage 11G.

## 13. Exit criteria

### Criteria 1–10 — Stage 11.0

1. Exact Stage 10G-selected Stage 11 gate frozen — **satisfied**.
2. Stage 10 bounded candidate/results carried forward without metaphysical promotion — **satisfied**.
3. Parameterization id, parameter label, event identity, internal clock, continuation, and measurement typing separated — **satisfied**.
4. Minimal parametrized constraint/lapse precursor law frozen — **satisfied**.
5. Positive admissible reparameterization family frozen with affine and genuinely nonlinear maps — **satisfied**.
6. Explicit parameter-event correspondence and relational comparison rule frozen — **satisfied**.
7. O/P/R/V/Xi and Stage 10 measurement carry-over targets frozen — **satisfied**.
8. Clock-change × reparameterization commuting target frozen — **satisfied**.
9. Negative controls, anti-triviality requirements, status vocabulary, and interpretation guards frozen — **satisfied**.
10. Stage 11A–G sequence and criteria 11–50 allocation frozen — **satisfied**.

### Criteria 11–16 — Stage 11A

11. Minimal constrained parametrized trajectory implemented with positive lapse-like rate — **satisfied**.
12. Frozen identity/affine/cubic/hyperbolic positive parameterizations implemented — **satisfied**.
13. Corresponding physical events carry different raw parameter values where expected — **satisfied**.
14. Chain-rule lapse transformation is numerically verified — **satisfied**.
15. Constraint-orbit/relational trajectory is preserved across the positive family — **satisfied**.
16. Orientation-reversing and non-injective maps are explicitly kept outside the positive admissible family — **satisfied**.

### Criteria 17–23 — Stage 11B

17. Relational observables such as `q(T=tau)` are constructed at corresponding physical events — **satisfied**.
18. Relational observable values agree across all positive parameterizations — **satisfied**.
19. Relational derivatives agree across the positive family — **satisfied**.
20. At least one nonlinear map produces demonstrably different raw parameter derivatives — **satisfied**.
21. Anchor/target physical-event typing remains explicit — **satisfied**.
22. Equal raw parameter labels are not used as event identity — **satisfied**.
23. Raw-parameter false comparison is rejected or classified as invalid — **satisfied**.

### Criteria 24–31 — Stage 11C

24. O is preserved/reconstructed by physical-event correspondence — **pending**.
25. `QExt(e1)={h_L,h_R}` and P typing are isomorphic across positive parameterizations — **pending**.
26. `R_content`, `R_direction`, and `R_access` are preserved/reconstructed without defining direction from `lambda` — **pending**.
27. `V_extension`, `V_semantics`, and `V_weights` are preserved/reconstructed — **pending**.
28. Xi explicitly carries parameterization/event/lapse semantics needed for typed comparison — **pending**.
29. Continuation/class/outcome correspondences remain explicit and valid — **pending**.
30. Hidden epistemic selector/modal-type information is not leaked into the public operational schema — **pending**.
31. Parameter-dependent O/P/R/V corruption is detected — **pending**.

### Criteria 32–38 — Stage 11D

32. Stage 10 reference future-measurement family is lifted without changing its physical question — **pending**.
33. Corresponding anchor/target events are found through typed event/clock correspondence rather than equal parameter values — **pending**.
34. Per-continuation probabilities agree across the positive parameterization family — **pending**.
35. Probability completeness/positivity and normalization roles remain valid — **pending**.
36. Weighted predictions and matched modal public views remain parameterization-covariant — **pending**.
37. Common-evidence update/posteriors remain parameterization-covariant — **pending**.
38. Wrong event/Jacobian/normalization/outcome controls are rejected — **pending**.

### Criteria 39–43 — Stage 11E

39. Reparameterization transports and Stage 10 A/B/C clock transports are both represented with explicit typing — **pending**.
40. Clock-change × reparameterization squares commute for relational O/event data — **pending**.
41. The squares commute for per-continuation measurement data/probabilities — **pending**.
42. Weighted/modal/update outputs are path-independent across the tested square family — **pending**.
43. Deliberately wrong correspondence/path mixing produces a detectable noncommuting control — **pending**.

### Criteria 44–47 — Stage 11F

44. Removing parameter-event correspondence is classified separately from numerical reconstructibility — **pending**.
45. Missing/wrong lapse-Jacobian semantics are classified and have explicit witnesses — **pending**.
46. Orientation reversal, non-injective relabeling, raw-lambda matching, and parameter-dependent corruption have explicit false-positive controls — **pending**.
47. Ablation results are not promoted to claims of metaphysical fundamentality or ontological becoming — **pending**.

### Criteria 48–49 — Stage 11G

48. Executable synthesis selects one frozen Stage 11 status from the full Stage 11A–F evidence chain — **pending**.
49. The next research gate is evidence-selected and documented without presupposing general covariance — **pending**.

### Criterion 50 — external repository validation

50. External final full-repository regression and merge-readiness review — **pending**.

## 14. Interpretation guards

- `parameter label != internal clock reading`;
- `parameter label != event identity`;
- `internal clock perspective != external parameterization`;
- `same numerical parameter value != same physical event`;
- `equal raw lambda != physical-event correspondence`;
- `parameter orientation != physical record direction by definition`;
- `orientation-preserving reparameterization != time reversal`;
- `orientation reversal != physical record reversal by definition`;
- `non-injective relabeling != admissible reparameterization`;
- `raw parameter derivative equality != reparameterization covariance criterion`;
- `relational observable covariance != full O/P/R/V covariance`;
- `relational derivative covariance != measurement covariance`;
- `same relational orbit != same metaphysics`;
- `same constraint orbit != established general covariance`;
- `relational covariance on one finite orbit != general covariance`;
- `reparameterization covariance != modal/ontological identity`;
- `reparameterization covariance != future actuality`;
- `reparameterization covariance != proof of eternalism`;
- `reparameterization covariance != refutation of ontological becoming`;
- `absence of preferred external parameterization != absence of ontological becoming`;
- `typed-resource use != metaphysical fundamentality`;
- `finite typed parametrized covariance != general covariance`;
- `parametrized covariance precursor != general relativity`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `not_established != false`.
