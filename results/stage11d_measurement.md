# Stage 11D Result — Future-Measurement Reparameterization Covariance

Status: **completed; criteria 32–38 satisfied by executable diagnostics.**

Source/unit-test validation checkpoint: run #1361 — **`907 passed in 590.98s (0:09:50)`**.

The documentation-synchronized full regression is tracked separately from the scientific evidence.

`repository validation != new scientific evidence`.

## Frozen physical question

Stage 11D reuses the Stage 10 future-signature measurement family without changing its physical question:

- family: `stage9c_future_signature`;
- prediction anchor: Stage 10 `e1`;
- measurement target: Stage 10 `e2`;
- continuation carrier: `QExt(e1)={h_L,h_R}`;
- outcomes: `future_signature_left`, `future_signature_other`;
- fixed internal Stage 10 chart: **A/e2**;
- probability form: `p(o|h)=c_h^dagger F_{h,o} c_h / (c_h^dagger N_h c_h)`.

The internal chart is deliberately fixed here so that Stage 11D tests external reparameterization only. Genuine A/B/C clock-change × reparameterization compatibility remains Stage 11E work.

## Positive family and typed measurement views

The frozen positive external-parameterization family contains four representations:

1. identity;
2. positive affine;
3. nonlinear cubic;
4. nonlinear hyperbolic/sinh.

For each parameterization and each continuation `h_L/h_R`, Stage 11D constructs one typed measurement view.

Executable counts:

- positive parameterizations: **4**;
- continuation classes: **2**;
- typed measurement views: **8**;
- canonical outcome-probability evaluations: **16**.

The Stage 11 physical anchor and target event ids are invariant across the four parameterizations, while the raw external parameter values at those roles are not forced to agree. The tests require more than one distinct raw anchor value and more than one distinct raw target value.

Therefore the comparison is made by typed physical-event correspondence rather than numerical raw-parameter equality.

`equal raw lambda != physical-event correspondence`.

## Per-continuation probabilities

For each continuation independently, all four parameterizations reproduce the same Stage 10 future-signature likelihood table at the corresponding typed `e1 -> e2` measurement question.

Executable bounds from the Stage 11D test suite:

- maximum per-continuation reparameterization probability residual: **<= 1e-9**;
- maximum residual against the unchanged Stage 9C/10 reference likelihood: **<= 1e-9**;
- maximum probability-sum residual: **<= 1e-9**;
- minimum probability: **>= -1e-9**;
- maximum probability: **<= 1 + 1e-9**.

Bounded operational conclusion:

`per-continuation future-measurement probabilities are reparameterization-covariant on the frozen positive family`.

## Completeness, positivity, and normalization

At every typed view the fixed Stage 10 A/e2 measurement remains a valid operational measurement:

- `sum_o F_{h,o}=N_h` within **1e-9**;
- minimum effect eigenvalue **>= -1e-9**;
- minimum normalization-form eigenvalue **> 1e-9**;
- canonical normalization denominator **> 1e-9**.

The classical Stage 11 external lapse is retained as reparameterization metadata in Xi and is not substituted for the Stage 10 operational normalization form.

`external lapse != quantum measurement normalization form`.

## Weighted/modal public views

Stage 11D reuses the Stage 10E weighting semantics rather than introducing a new Stage 11 weighting rule.

Executable results:

- matched epistemic/ontic weighted public views are equal across all four parameterizations;
- weighted future predictions are reparameterization-covariant within **1e-9**;
- swapping the hidden epistemic selected continuation `h*` leaves the public weighted measurement view unchanged;
- epistemic-selected and ontic-extension privileged modal roles remain distinct outside the public projection;
- the public weighted schema remains selector-free.

Thus public operational equality is preserved without identifying the two modal interpretations.

`selector-free public projection != absence of privileged modal semantics`.

`reparameterization covariance != modal/ontological identity`.

## Common evidence update

The common evidence outcome is the already frozen

`future_signature_left`.

Using the existing Stage 10E / Stage 9C update semantics, Stage 11D verifies:

- epistemic posterior reparameterization residual: **<= 1e-9**;
- ontic posterior reparameterization residual: **<= 1e-9**;
- epistemic/ontic posterior mismatch: **<= 1e-9**;
- hidden epistemic selected continuation is preserved;
- updated ontic state remains selector-free.

`evidence-update covariance != ontological becoming`.

## Criterion-38 controls

Four controls are implemented and all **4 / 4** are rejected.

### 1. Wrong event correspondence

The Stage 11 physical events assigned to Stage 10 `e1/e2` are swapped. The measurement context is rejected before probability evaluation.

### 2. Wrong lapse/Jacobian

The nonlinear cubic parameterization is supplied with an incompatible target lapse/Jacobian value. The typed context is rejected even though the Stage 10 Born-rule matrices do not numerically consume the classical lapse.

`numerically unchanged probability payload != well-typed reparameterization context`.

### 3. Wrong outcome correspondence

`future_signature_left` and `future_signature_other` are swapped in Xi. The context is rejected as an outcome-semantic mismatch.

### 4. Wrong normalization

A normalization form from a different Stage 10 chart is deliberately reused at the fixed A/e2 chart. The Stage 10D Hermitian-tomography-complete probe family supplies a numerical witness:

- wrong-normalization matrix residual: **> 1e-9**;
- wrong-normalization probability residual: **> 1e-9**.

The correspondence/Jacobian controls are typed rejections; the normalization control is a numerical witness. These failure modes remain distinct.

## Criteria 32–38

32. Stage 10 reference future-measurement family lifted without changing its physical question — **satisfied**.
33. Corresponding anchor/target events found through typed event correspondence rather than equal parameter values — **satisfied**.
34. Per-continuation probabilities agree across the positive parameterization family — **satisfied**.
35. Probability completeness/positivity and normalization roles remain valid — **satisfied**.
36. Weighted predictions and matched modal public views remain parameterization-covariant — **satisfied**.
37. Common-evidence update/posteriors remain parameterization-covariant — **satisfied**.
38. Wrong event/Jacobian/normalization/outcome controls are rejected — **satisfied**.

## Bounded result

**`Stage 11D future-measurement reparameterization covariance on the frozen positive family = established`.**

This means that, in the declared finite typed product construction and at the fixed Stage 10 A/e2 internal chart, the same future-measurement probabilities, weighting semantics, and evidence-update outputs survive all four admissible external parameterizations when the correct event/class/outcome/lapse/normalization typing is retained.

It does **not** establish:

- general covariance or general relativity;
- clock-change × reparameterization compatibility;
- dynamical derivation of the Stage 10 quantum carrier from the classical Stage 11A precursor;
- modal/ontological identity;
- future actuality;
- eternalism;
- absence of ontological becoming;
- empirical discovery.

Guards:

`typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor`.

`future-measurement reparameterization covariance != clock-change x reparameterization compatibility`.

`parameterization-covariant future probabilities != future actuality`.

`parameterization-covariant future probabilities != proof of eternalism`.

`parameterization-covariant future probabilities != refutation of ontological becoming`.

`finite typed parametrized covariance != general covariance`.

`parametrized covariance precursor != general relativity`.

Next checkpoint: **Stage 11E — clock-change × parameterization compatibility.**
