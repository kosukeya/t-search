# Stage 11 Protocol — Parametrized Covariance Precursor

Status: **Stage 11.0 protocol freeze and Stage 11A completed; criteria 1–16 satisfied; criteria 17–50 pending implementation and external review.**

Selected Stage 11 gate from Stage 10G:

> **Construct a parametrized covariance precursor that preserves the typed O/P/R/V measurement architecture without assuming a preferred external time parameterization.**

Stage 11 carries forward, without metaphysical promotion,

`T10_candidate=(O,P,R,V;Xi)`

with

`R=(R_content,R_direction,R_access)`

and

`V=(V_extension,V_semantics,V_weights)`.

The Stage 10 bounded result carried into Stage 11 is

`fully typed finite future-measurement covariance = established`.

The repeatedly retained project boundary remains

`finite clock covariance != general covariance`.

Stage 11 tests one controlled ingredient beyond Stage 10: whether the same typed relational architecture can survive or be reconstructed across different admissible external parameterizations.

## 1. Frozen scientific question

Stage 11 asks whether a preferred external trajectory parameter is necessary for the Stage 10 relational/clock/modal/record/measurement structure, or whether the structure can be represented on a parametrized constrained precursor in which different admissible labels trace the same typed physical relational history.

The target claim, if the complete later evidence supports it, is only:

`finite typed parametrized covariance precursor = established`.

It is not assumed from Stage 11A alone.

The Stage 11G classification vocabulary is:

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
- clock/event/class/outcome correspondences inherited from Stage 10.

Frozen guards:

`parameter label != internal clock reading`.

`parameter label != event identity`.

`internal clock perspective != external parameterization`.

`same numerical parameter value != same physical event`.

`same physical event != same parameter value across parameterizations`.

`parameterization correspondence != event identity`.

## 3. Parametrized constrained precursor

Stage 11A implements the frozen minimal canonical parametrized-mechanics precursor with variables

`(T,p_T;q,p)`

and constraint

`C = p_T + H(q,p) approx 0`.

The deterministic seed uses

`H(q,p)=p^2/2`

with `p=1.25`, `p_T=-p^2/2`, and a nonzero configuration motion.

The external label `lambda` is not interpreted as physical time. The identity representation uses the positive nonconstant lapse-like seed

`N(lambda)=1+lambda^2/4`

so

`dT/dlambda = N(lambda)`

and

`T(lambda)=lambda+lambda^3/12`.

For any phase-space quantity `z`, the precursor notation remains

`dz/dlambda = N(lambda) {z,H}`.

The canonical configuration seed is

`q(T)=-0.35+1.25 T`.

The invariant candidate reserved for Stage 11B is relational motion such as

`dq/dT = (dq/dlambda)/(dT/dlambda)`

rather than a raw derivative with respect to `lambda`.

This classical constrained seed is a precursor/scaffold for testing parameter redundancy. It does not replace or re-interpret the Stage 10 quantum measurement carrier.

`classical parametrized precursor != fundamental classical ontology`.

## 4. Admissible reparameterization family

Positive/admissible reparameterizations are smooth, bijective on the tested trajectory domain, strictly monotone, and orientation-preserving:

`lambda' = f(lambda)` with `f'(lambda) > 0`.

The frozen minimum positive family is implemented exactly as:

1. identity: `f_id(lambda)=lambda`;
2. positive affine: `f_aff(lambda)=2 lambda + 1`;
3. nonlinear cubic: `f_cub(lambda)=lambda + lambda^3/4`, with `f'_cub(lambda)=1+3 lambda^2/4 > 0`;
4. nonlinear hyperbolic: `f_sinh(lambda)=sinh(lambda)`, with `f'_sinh(lambda)=cosh(lambda) > 0`.

The lapse-like rate transforms by the frozen chain rule:

`N'(lambda') = N(lambda) dlambda/dlambda' = N(lambda)/f'(lambda)`.

Raw parameter derivatives are therefore expected, in general, to differ:

`dq/dlambda != dq/dlambda'`.

Relational derivatives are the candidate invariant:

`dq/dT = (dq/dlambda)/(dT/dlambda) = (dq/dlambda')/(dT/dlambda')`.

`raw parameter derivative equality != reparameterization covariance criterion`.

## 5. Stage 11A physical-event carrier and correspondence

Stage 11A samples 13 explicit physical events on the source-label domain `[-1.5,1.5]`, with event ids

`orbit_event_00 ... orbit_event_12`.

Representations are compared through explicit typed physical-event correspondence, never by equal raw parameter values.

For parameterizations `rho` and `sigma`, Stage 11 uses

`chi_event^{rho->sigma}: e_rho -> e_sigma`

while allowing

`lambda_rho(e) != lambda_sigma(e)`.

The Stage 11A constructor requires corresponding event identity plus agreement of physical `T` and `q`. Across affine/cubic/hyperbolic versus identity there are 36 corresponding event pairs whose raw parameter values differ.

For an internal clock X, later stages retain the operational anchor

`e_X(tau) := physical event where X reads tau`

when the clock reading is unique in the tested domain.

Equal parameter labels alone are never sufficient.

## 6. Stage 11A executable diagnostics

The canonical Stage 11A diagnostics establish only the minimal carrier checkpoint:

- event count: **13**;
- positive parameterization count: **4**;
- minimum transformed positive lapse: **0.5**;
- maximum constraint residual: **0.0**;
- maximum lapse chain-rule residual: **0.0**;
- maximum `T`, `q`, `p`, and `p_T` orbit residual across the positive family: **0.0**;
- corresponding event pairs with different raw parameter labels: **36**;
- nonlinear-map sample points with different raw `dq/dlambda` rates: **24**.

The 24 raw-rate differences are an anti-triviality witness, not yet closure of the Stage 11B relational-derivative criterion.

The bounded Stage 11A result is:

`minimal Stage 11A constraint orbit preservation = established`.

`same constraint orbit != established general covariance`.

## 7. Frozen O/P/R/V/Xi lift target

Stage 11C must attempt to transport/reconstruct the full typed architecture across admissible parameterizations.

### O

`O` is attached to typed physical relational events, not to bare parameter values.

### P

The Stage 10 modal extension carrier is retained at the reference anchor:

`QExt(e1)={h_L,h_R}`.

Stage 11 tests whether

`QExt^rho(e1) ~= QExt^sigma(e1)`

under explicit continuation/event correspondence.

`reparameterization invariance of QExt != ontic future openness`.

### R

`R=(R_content,R_direction,R_access)` is tested under orientation-preserving admissible maps. The physical directional relation is not defined from increasing `lambda` alone.

`parameter orientation != physical record direction by definition`.

### V

`V=(V_extension,V_semantics,V_weights)` is transported/reconstructed with continuation/class alignment and weight semantics explicit.

### Xi

Stage 11 extends the operational typing resources in `Xi` with at least:

- parameterization identity;
- parameter-event correspondence;
- lapse/rate transformation semantics;
- inherited clock/event/class/outcome correspondences;
- normalization convention;
- continuation-weight semantics.

`typed-resource use != metaphysical fundamentality`.

## 8. Frozen Stage 10 measurement carry-over

Stage 11D reuses the Stage 10 future-signature measurement family rather than inventing a new measurement after inspecting reparameterization results.

Reference anchor: `e1`.

Reference target: `e2`.

Reference continuation carrier: `QExt(e1)={h_L,h_R}`.

Reference outcomes:

- `future_signature_left`;
- `future_signature_other`.

The Stage 10 probability form remains

`p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

Stage 11 asks whether, for corresponding typed physical events,

`p_rho(o|h,e1->e2) = p_sigma(o|h,e1->e2)`

across admissible parameterizations, before and after the already-separated weight/update layers.

The comparison is not

`p_rho(o|h,lambda=a) = p_sigma(o|h,lambda=a)`

unless explicit event correspondence independently establishes that the two labels refer to the same physical event.

## 9. Frozen clock-change × reparameterization compatibility target

Let `G_{rho->sigma}` denote an admissible reparameterization transport/correspondence and let `C_{X->Y}` denote the Stage 10 genuine internal-clock transport.

Stage 11E tests the typed commuting-square target

`C_{X->Y} o G_{rho->sigma} ~= G_{rho->sigma} o C_{X->Y}`

for corresponding physical objects, not necessarily entrywise-identical intermediate matrices.

The comparison must cover at least:

- O/event data;
- continuation/modal typing;
- measurement effects/normalization roles;
- per-continuation probabilities;
- weighted predictions and evidence-update outputs when applicable.

All A/B/C internal-clock perspectives and all frozen positive parameterizations must participate in the final Stage 11E positive family.

`internal-clock covariance != reparameterization covariance`.

`commuting typed diagram != general covariance`.

## 10. Frozen negative and false-positive controls

The controls remain frozen before the stages that use them:

1. raw-equal-parameter matching: identify events only because `lambda_rho=lambda_sigma`;
2. wrong/missing parameter-event correspondence;
3. omit the lapse transformation and reuse `N` numerically under nonlinear `f`;
4. use the wrong derivative Jacobian in `N'`;
5. use a non-injective map such as `f_noninj(lambda)=lambda^2` on a domain containing both signs;
6. orientation reversal `f_rev(lambda)=-lambda` treated as outside the initial admissible gauge family;
7. wrong continuation/class correspondence;
8. wrong measurement outcome correspondence;
9. wrong normalization semantics;
10. parameter-dependent corruption of a physical O/P/R/V or measurement payload while preserving superficial labels;
11. identify parameter direction with `R_direction` by definition;
12. mix parameterizations inside one probability/weight/update calculation without a typed correspondence.

Stage 11A already implements controls 5 and 6 as explicitly excluded parameterization specifications and rejects them in the positive trajectory constructor.

Orientation reversal is a boundary/control, not an automatic physical record reversal:

`orientation reversal != physical record reversal by definition`.

`orientation-preserving reparameterization != time reversal`.

Non-injective maps are not silently interpreted as gauge-equivalent:

`non-injective relabeling != admissible reparameterization`.

## 11. Frozen anti-triviality requirements

A positive Stage 11 result may not be based only on unchanged discrete labels.

The full evidence chain must demonstrate at least:

- genuinely different numerical parameter labels for corresponding events;
- genuinely different raw parameter derivatives for at least one nonlinear parameterization;
- correct transformed lapse-like rates;
- invariant relational observables/derivatives;
- preserved/reconstructed O/P/R/V typing;
- preserved Stage 10 measurement probabilities through typed physical-event correspondence;
- compatibility of clock changes with reparameterization;
- rejection/classification of the frozen negative controls.

Stage 11A has already supplied the first three carrier-level witnesses: 36 different-label event pairs, 24 nonlinear raw-rate differences, and zero chain-rule residual.

`same labels after relabeling != sufficient evidence of covariance`.

## 12. Stage sequence and exit-criterion allocation

### Stage 11.0 — protocol freeze — completed

Criteria 1–10.

External full-repository regression after the freeze: run #1285, `874 passed in 640.88s (0:10:40)`.

### Stage 11A — minimal parametrized constrained carrier and admissible family — completed

Criteria 11–16.

### Stage 11B — relational observables and relational derivatives — next

Criteria 17–23.

### Stage 11C — typed O/P/R/V/Xi lift

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

17. Relational observables such as `q(T=tau)` are constructed at corresponding physical events — **pending**.
18. Relational observable values agree across all positive parameterizations — **pending**.
19. Relational derivatives agree across the positive family — **pending**.
20. At least one nonlinear map produces demonstrably different raw parameter derivatives — **pending**.
21. Anchor/target physical-event typing remains explicit — **pending**.
22. Equal raw parameter labels are not used as event identity — **pending**.
23. Raw-parameter false comparison is rejected or classified as invalid — **pending**.

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
- `parameter orientation != physical record direction by definition`;
- `orientation-preserving reparameterization != time reversal`;
- `orientation reversal != physical record reversal by definition`;
- `non-injective relabeling != admissible reparameterization`;
- `raw parameter derivative equality != reparameterization covariance criterion`;
- `same relational orbit != same metaphysics`;
- `same constraint orbit != established general covariance`;
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
