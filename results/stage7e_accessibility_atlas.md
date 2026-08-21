# Stage 7E Results — Accessibility and Partial-Atlas Record Consistency

Status: **scientific implementation complete for the declared canonical Stage 7D forward record family; corrected implementation regression passed; final documentation-head regression pending.**

## Accessibility result

The underlying common physical record is unchanged while only the declared local memory-readout interface is varied.

Across all nine interacting clock/readout nodes:

### Full access

- global `A_R=+1`;
- global `A_acc=+1/2`;
- local `A_R=+1`;
- local `A_acc=+1/2`;
- orientation `lower-index`.

### Hidden access

- the global record remains represented;
- local `A_R=0`;
- local `A_acc=0`;
- local orientation `none`.

### Maximally noisy access

- the global record remains represented;
- local `A_R=0`;
- local `A_acc=0`;
- local orientation `none`.

### Coarse access (`p_flip=1/4`)

- global record remains represented;
- local record information is reduced to `1-H_2(1/4) ~= 0.1887218755`;
- local accessibility score is reduced to `1/4`;
- orientation remains `lower-index`.

Therefore:

`locally inaccessible record != globally absent record`.

The same physical record-bearing construction supports full, degraded, and inaccessible local interfaces without changing the global record representation.

## Partial-atlas result

The primitive edge

`A/e1 -> B/e0`

is deliberately unavailable.

Three indirect paths remain:

1. `A/e1 -> C/e0 -> B/e0`;
2. `A/e1 -> C/e1 -> B/e0`;
3. `A/e1 -> C/e2 -> B/e0`.

All three ideal paths reproduce, within tolerance, the mathematically re-derived omitted direct map and its target consequences:

- state transport;
- induced physical metric;
- corresponding record/memory observable representation;
- `A_R=+1`;
- `A_acc=+1/2`.

Thus the target record remains indirectly reconstructible even though the direct local edge is absent.

## Perturbed-edge control

Only `C/e1 -> B/e0` is perturbed.

The affected path develops detectable nonzero:

- map residual;
- state residual;
- induced-metric covariance residual;
- record-score residual.

The first implementation regression measured a record-score residual of approximately:

`0.0350432330`.

The unaffected `C/e0` and `C/e2` paths remain consistent.

An initially over-strong negative-control expectation required the corresponding-observable residual to fail as well. That expectation was falsified: the chosen target-sector perturbation commutes with the tested projector algebra, so its observable similarity residual remains at numerical zero (`~8.3e-16`) even while map/state/metric/statistical consistency fails.

The executable criterion was corrected to preserve this diagnostic separation rather than changing the perturbation merely to make every signal fail.

New guard:

`observable-algebra correspondence != full state/metric path consistency`.

## Exit-criteria consequence

Stage 7E satisfies criteria 26–29 in the declared canonical family:

26. global record representation and local memory accessibility are separately represented and diagnosed;
27. hidden and maximally noisy memory controls are explicit, with a coarse degraded-access control in addition;
28. the missing direct perspective edge is reconstructed consistently along three indirect paths;
29. one locally perturbed edge produces a localized path inconsistency while unaffected paths remain consistent.

## Strongest bounded statement

**Within the declared finite Stage 7 record-bearing constrained family, global/reconstructible record structure can survive complete loss of local memory accessibility, and record covariance can remain path-consistent across a partial interacting clock atlas even when the requested direct edge is unavailable. A perturbation of one primitive edge is localized by independent map/state/metric/statistical diagnostics; preservation of the tested observable algebra alone is insufficient to certify full atlas consistency.**

This strengthens the distinction between record existence, reconstructibility, and accessibility. It does not establish a fundamental temporal arrow, universal reference-frame availability, spacetime curvature, general covariance, ontological becoming, or phenomenal passage.

## Validation

Stage 7E adds **23 focused tests**.

The first implementation run reached `534 passed / 2 failed`; both failures came from the deliberately over-strong assumption that the chosen local perturbation must also break observable similarity transport. The run itself showed the intended map/state/metric/record-statistic inconsistency and motivated the corrected diagnostic separation.

Corrected implementation-inclusive PR merge-ref regression on head `c638326e64e0bd031596d32880a5648a778f06da` / merge-ref `548f91c2736bd71e2cbe973b05cdbe22e3beb4d9`:

`536 passed in 170.07s`.

A final documentation-head regression is required after the Stage 7E checkpoint updates.

## Next

Stage 7F — ablation / reconstruction / mismatch matrix.