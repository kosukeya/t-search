# Stage 11D Notes — Future-Measurement Reparameterization Covariance

Status: **Stage 11D implementation is present; criteria 32–38 are decided by executable diagnostics, with repository-level regression tracked separately.**

Stage 11C baseline: run #1355 — **`899 passed in 647.28s (0:10:47)`**.

## Question

Stage 11D asks whether the already frozen Stage 10 future-signature measurement question remains operationally unchanged when the same Stage 11 relational event roles are represented by the four admissible external parameterizations.

The physical measurement question is not redesigned:

- reference family: `stage9c_future_signature`;
- prediction anchor: Stage 10 `e1`;
- measurement target: Stage 10 `e2`;
- continuation carrier: `QExt(e1)={h_L,h_R}`;
- outcomes: `future_signature_left`, `future_signature_other`;
- probability form: `p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

## Separation from Stage 11E

Stage 11D fixes the internal Stage 10 reference chart to **A/e2** and changes only the external parameterization.

This isolates two representation questions:

1. Stage 11D: external reparameterization at one fixed internal clock chart;
2. Stage 11E: compatibility/commutation between external reparameterization and genuine A/B/C internal-clock change.

Therefore:

`future-measurement reparameterization covariance != clock-change x reparameterization compatibility`.

## Typed event bridge

For each positive parameterization, the Stage 11C architecture supplies:

- `parameterization_id`;
- raw anchor/target parameter values;
- transformed lapse values;
- `e1/e2 -> physical Stage 11 event id` correspondence;
- continuation/class correspondence;
- outcome correspondence.

Stage 11D locates the measurement anchor/target through these typed role/event correspondences. It never identifies the event by searching for an equal numerical raw parameter value.

The physical Stage 11 anchor and target ids must remain the same across parameterizations while their raw external parameter values are allowed to differ.

`equal raw lambda != physical-event correspondence`.

## Per-continuation measurement views

For every pair

`parameterization rho x continuation h`, 

Stage 11D builds one typed measurement view at the frozen Stage 10 A/e2 chart.

The minimum positive family therefore contains:

- 4 external parameterizations;
- 2 continuation classes;
- 8 typed measurement views;
- 2 outcomes per view;
- 16 canonical outcome-probability evaluations.

Each view retains:

- Stage 10 family id;
- continuation id;
- Stage 10 e1/e2 anchor/target roles;
- Stage 11 physical anchor/target event ids;
- raw parameter values as representation metadata;
- internal clock/chart identity;
- outcome identities;
- normalization semantics;
- probabilities;
- probability-sum residual;
- completeness residual;
- effect/normalization positivity diagnostics;
- normalization denominator.

## Probability comparison

For each continuation independently, Stage 11D compares

`p_rho(o|h,e1->e2)`

across all four external parameterizations and also against the unchanged Stage 9C/10 reference likelihood table.

The comparison is deliberately before any continuation-weight aggregation.

`per-continuation probability covariance != modal identity`.

## Completeness, positivity, normalization

The Stage 10 operational normalization form is preserved as a typed resource. Stage 11D verifies:

- `sum_o F_{h,o}=N_h` in the fixed reference chart;
- effect positivity/Hermiticity within numerical tolerance;
- positive normalization form;
- positive canonical normalization denominator;
- normalized probabilities.

The external lapse is not substituted for the Stage 10 operational normalization form.

`external lapse != quantum measurement normalization form`.

## Weighted/modal public views

Stage 11D then reuses Stage 10E without changing its semantics.

For matched `(0.5,0.5)` continuation weights it checks across all four parameterizations:

- weighted future prediction covariance;
- matched epistemic/ontic-extension public-view equality;
- hidden epistemic `h*` swap invariance of the public view;
- continued private distinction between epistemic-selected and ontic-extension modal roles;
- selector-free public weighted schema.

`selector-free public projection != absence of privileged modal semantics`.

## Common evidence update

The common evidence is the already frozen Stage 10/9C outcome

`future_signature_left`.

Stage 11D reuses the Stage 10E/Stage 9C update rules and checks:

- epistemic posterior covariance across parameterizations;
- ontic posterior covariance across parameterizations;
- matched epistemic/ontic posterior weights;
- preservation of the hidden epistemic selected continuation;
- selector-free updated ontic state.

`evidence-update covariance != ontological becoming`.

## Stage 11D controls

Four controls close criterion 38.

### Wrong event correspondence

The Stage 11 physical targets assigned to `e1` and `e2` are swapped. The context must be rejected before probability evaluation.

### Wrong lapse/Jacobian

A nonlinear parameterization is supplied with the identity-chart target lapse rather than its transformed lapse. The typed context must reject the mismatch even though the Born-rule matrices themselves do not consume the classical lapse numerically.

This is intentional:

`numerically unchanged probability payload != well-typed reparameterization context`.

### Wrong outcome correspondence

`future_signature_left` and `future_signature_other` are swapped in Xi. The context must be rejected as an outcome-semantic mismatch.

### Wrong normalization

A normalization form from a different Stage 10 chart is deliberately reused in the fixed A/e2 chart. A Hermitian-tomography-complete Stage 10D probe family supplies an explicit numerical witness that this misaligned normalization changes probabilities.

The three correspondence/Jacobian failures are typed rejections; the normalization control is a numerical witness. They are not conflated.

## Interpretation boundary

A successful Stage 11D result establishes covariance only for the declared finite product construction in which the tested Stage 10 quantum measurement object is associated with the Stage 11 parameterized event carrier through explicit typing.

It does not derive the Stage 10 quantum dynamics or Born rule from the classical Stage 11A parametrized scaffold.

`typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor`.

`future-measurement reparameterization covariance != clock-change x reparameterization compatibility`.

`parameterization-covariant future probabilities != future actuality`.

`parameterization-covariant future probabilities != proof of eternalism`.

`parameterization-covariant future probabilities != refutation of ontological becoming`.

`evidence-update covariance != ontological becoming`.

`finite typed parametrized covariance != general covariance`.

`parametrized covariance precursor != general relativity`.

`repository validation != new scientific evidence`.

Next checkpoint after criteria 32–38 close: **Stage 11E — clock-change x parameterization compatibility.**
