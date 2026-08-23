# Stage 11E Notes — Clock-Change × Parameterization Compatibility

Status: **implementation and executable tests added; criteria 39–43 are decided by Stage 11E diagnostics, with repository-level regression tracked separately.**

Stage 11D baseline: latest documentation-synchronized head passed run #1393 — **`908 passed in 589.63s (0:09:49)`**.

## Question

Stage 11E asks whether the two representation changes already tested separately can be combined consistently:

- `G_{rho->sigma}`: external reparameterization transport;
- `C_{X->Y}`: genuine Stage 10 continuation-aware internal-clock transport.

The frozen target is the typed commuting square

`C_{X->Y} o G_{rho->sigma} ~= G_{rho->sigma} o C_{X->Y}`.

This stage does not introduce a new physical interaction between the two transformations. It tests compatibility of the finite product construction already built in Stages 10 and 11A–D.

`commuting typed product square != independent interaction law`.

## Tested finite family

External parameterization nodes:

- identity;
- affine;
- cubic;
- hyperbolic/sinh.

The Stage 11E positive transport family uses all **12 ordered distinct reparameterization edges**.

Internal clock/readout nodes:

- `A/0`, `A/1`, `A/2`;
- `B/0`, `B/1`, `B/2`;
- `C/0`, `C/1`, `C/2`.

Thus there are **9 internal clock/readout nodes**.

For each continuation, Stage 11E uses all ordered genuine distinct-clock edges:

- 3 source clocks;
- 3 source readouts;
- 2 distinct target clocks;
- 3 target readouts;

for **54 clock transports per continuation** and **108 total clock transports** over `h_L/h_R`.

## Explicit typed transports

### External transport `G`

`G_{rho->sigma}` retains:

- typed physical anchor/target event identities;
- continuation/class correspondence;
- outcome correspondence;
- relational O payload.

It changes:

- external parameterization id;
- raw anchor/target parameter values;
- transformed lapse metadata in Xi.

It does not act as an internal-clock map.

`external reparameterization transport != internal clock transport`.

### Internal clock transport `C`

`C_{X->Y}` is the already-tested Stage 10C continuation-aware support map and dual measurement transport.

For the measurement form,

`H^Y = S^{-dagger} H^X S^{-1}`.

Stage 11E uses this rule for the operational normalization form and both future-signature effects.

It changes the internal chart representation while leaving the external parameterization/Xi choice unchanged.

`internal-clock covariance != reparameterization covariance`.

## Relational O/event squares

The event/O comparison is built from the typed Stage 11 physical anchor/target roles plus the internal-clock/readout tag.

All 12 ordered parameterization edges are crossed with all 54 ordered distinct-clock/readout edges, giving **648 event/O squares**.

Both paths must end at the same:

- target external parameterization;
- target internal clock/readout;
- physical anchor/target event ids;
- target raw parameter metadata;
- relational `T` and `q(T)` payload.

The internal clock leg does not redefine the Stage 11 physical event ids.

## Measurement/probability squares

For each continuation independently, every external edge is crossed with every genuine Stage 10 clock edge.

Counts:

- 12 external edges;
- 54 clock edges per continuation;
- 2 continuations;
- **1296 measurement squares**.

For each square, Stage 11E compares:

1. `G` then genuine Stage 10C dual clock transport;
2. genuine Stage 10C clock transport then `G`;
3. the directly reconstructed target Stage 10 chart.

The comparison covers:

- normalization-form matrices;
- future-signature effect matrices;
- per-continuation probabilities;
- continuation/event/outcome typing.

Thus a positive result requires more than identical labels: the clock leg uses nontrivial 14×14 continuation-aware transport matrices and must reproduce the direct target chart.

## Weighted/modal public outputs

The same 12 × 54 square family gives **648 weighted/modal squares**.

Stage 11E reuses Stage 10E public views and checks path independence at the common target node for:

- continuation weights;
- predictive density;
- record scores/accessibility/orientation;
- future-signature weighted probabilities.

At every target endpoint it also checks:

- matched epistemic/ontic public equality;
- hidden epistemic `h*` swap invariance of the public view.

The private modal distinction remains outside the public projection.

`path-independent matched public views != modal/ontological identity`.

## Common-evidence update squares

The frozen evidence remains

`future_signature_left`.

Again the 12 × 54 family gives **648 posterior squares**.

Both paths must agree on:

- epistemic posterior weights;
- ontic posterior weights;
- hidden epistemic selected continuation;
- selector-free updated ontic state.

`path-independent evidence update != ontological becoming`.

## Wrong-path control

Stage 11E includes an explicit noncommuting control.

A source measurement chart is relabeled as the target internal clock/readout **without applying the genuine Stage 10C dual transport**. Superficial target clock labels therefore look correct while the matrices remain source-chart matrices.

The control compares that mislabeled/untransported object against the direct target chart and requires detectable differences in:

- normalization form;
- effect form;
- canonical probabilities.

Expected classification:

`noncommuting_wrong_clock_path_detected`.

This control targets path mixing rather than the broader ablations reserved for Stage 11F.

## Interpretation boundary

A successful Stage 11E result would establish compatibility only in the declared finite typed product family.

It would not establish:

- general covariance;
- general relativity;
- a dynamical interaction law between external reparameterization and internal clocks;
- future actuality;
- eternalism;
- absence of ontological becoming;
- empirical discovery.

Guards:

`internal-clock covariance != reparameterization covariance`.

`commuting typed product square != independent interaction law`.

`commuting typed diagram != general covariance`.

`path-independent future probabilities != future actuality`.

`path-independent evidence update != ontological becoming`.

`absence of preferred external parameterization != absence of ontological becoming`.

`finite typed parametrized covariance != general covariance`.

`repository validation != new scientific evidence`.

Next checkpoint after criteria 39–43 close: **Stage 11F — ablation / wrong-gauge / false-positive controls.**
