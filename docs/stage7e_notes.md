# Stage 7E Notes — Accessibility and Partial-Atlas Record Consistency

## Question

Stage 7D established that the same record-bearing modified physical construction can be represented covariantly across genuine A/B/C clock perspectives when the induced support metric and corresponding observables are transported consistently.

Stage 7E asks two narrower questions:

1. can a record remain globally represented/reconstructible while becoming locally inaccessible through the declared memory interface?;
2. can record transport remain consistent when a requested direct clock-perspective edge is absent and must be reconstructed indirectly through a partial atlas?

These tests target Stage 7 exit criteria 26–29.

## Accessibility interfaces

The physical state, target operators, and memory subsystem are held fixed. Only the declared memory readout channel changes.

Four interfaces are executable:

- `full`: exact computational memory readout;
- `hidden`: both memory values are mapped to one visible output;
- `maximally-noisy`: binary-symmetric channel with crossover probability `1/2`;
- `coarse`: binary-symmetric channel with crossover probability `1/4`.

This is deliberate. A hidden interface and a maximally noisy interface both erase accessible record information, but they do so for different interface reasons.

For every one of the nine Stage 7D clock/readout nodes, the globally represented preserving record remains the Stage 7D record:

`A_R=+1`, `A_acc=+1/2`, orientation `lower-index`.

With `full` access, the local diagnostics reproduce those values.

With `hidden` or `maximally-noisy` access, the local diagnostics become:

`A_R^local=0`, `A_acc^local=0`, orientation `none`,

while the global record representation remains unchanged.

With `coarse` access, the record is degraded but not erased. For the balanced binary canonical witness:

`A_R^local = 1 - H_2(1/4) ~= 0.1887218755`,

`A_acc^local = 1/4`,

and the local orientation remains `lower-index`.

Therefore Stage 7E distinguishes at least three statuses in one physical record-bearing family:

- globally represented and fully accessible;
- globally represented and degraded but accessible;
- globally represented but locally inaccessible.

## Partial interacting atlas

The canonical direct edge

`A/e1 -> B/e0`

is intentionally removed from the declared local atlas.

The target perspective remains present, and three two-edge indirect paths remain available:

- `A/e1 -> C/e0 -> B/e0`;
- `A/e1 -> C/e1 -> B/e0`;
- `A/e1 -> C/e2 -> B/e0`.

The re-derived Stage 7D direct map is used only as a mathematical oracle for the test. It is not counted as an available primitive edge.

For each ideal indirect path, composition agrees with the oracle within tolerance for:

- the support-coordinate map;
- the transported canonical state;
- induced-metric covariance;
- corresponding record/memory observables;
- the record score `A_R=+1`;
- the accessibility score `A_acc=+1/2`.

Thus indirect reconstructibility survives removal of the direct local edge in the canonical partial atlas.

## Localized perturbation control

Only the edge

`C/e1 -> B/e0`

is perturbed. The perturbation scales one correct target/memory joint-record sector in the target chart.

The path through `C/e1` then develops nonzero map, state, metric, and record-statistic residuals, while the paths through `C/e0` and `C/e2` remain consistent.

The first implementation checkpoint exposed an important diagnostic separation: the chosen perturbation commutes with the tested record projector algebra. Consequently, corresponding-observable similarity transport remains numerically correct even while the state/metric relation and record statistic are inconsistent. The failed test assumption was corrected rather than changing the perturbation to force every diagnostic to fail.

This adds a new guard:

`observable-algebra correspondence != full state/metric path consistency`.

The localized control therefore checks consistency using multiple independent witnesses rather than requiring every witness to fail simultaneously.

## Interpretation guards

Stage 7E adds or reinforces:

- `locally inaccessible record != globally absent record`;
- `global reconstructibility != local accessibility`;
- `indirect reconstructibility != direct local edge availability`;
- `partial atlas path consistency != universal frame availability`;
- `localized path inconsistency != spacetime curvature`;
- `observable-algebra correspondence != full state/metric path consistency`;
- `record covariance != P=R`.

## Scope boundary

The partial atlas is a finite algebraic perspective network. A missing primitive edge is not a claim that a physical frame is impossible, and a perturbed path residual is not gravitational curvature or holonomy without an independent spacetime derivation.

Likewise, hiding or corrupting a readout channel changes local accessibility, not the globally represented physical record state.

## Next

Stage 7F — ablation / reconstruction / mismatch matrix.
