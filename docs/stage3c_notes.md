# Stage 3C — Asymmetric Record Model Notes

Status: **completed; branch-level regression passed**.

Stage 3C does not introduce a new arrow metric. It interprets the already-frozen Stage 3B diagnostics conservatively.

## Interpretation criterion

A Stage 3C **record-defined orientation** is recognized only when:

1. the signed mutual-information contrast `A_R` is nonzero;
2. the signed decoder/accessibility contrast `A_Acc` is nonzero;
3. both contrasts select the same neutral side;
4. the selected side carries nonzero mutual information with the current record register.

The orientation labels are intentionally restricted to:

- `lower-index`;
- `upper-index`;
- `none`.

No code path renames a side `past` or `future`.

## Canonical model

The Stage 3C model uses the exact Stage 3A canonical ensemble:

`X_0=a`

`M_0=0`

`N_0=b`

with independent uniform bits `a,b`, current neutral position `k=1`, record register `M_1`, target component `X`, and `delta=1`.

The blank-memory boundary remains explicit in the ensemble. Stage 3C does **not** yet claim that this boundary is the causal source of the orientation; that attribution requires the Stage 3D uniform-memory and no-record controls.

## Canonical assessment

The already-defined Stage 3B diagnostics give:

`I(M_1;X_0)=1 bit`

`I(M_1;X_2)=0 bit`

`Acc(M_1->X_0)=1`

`Acc(M_1->X_2)=1/2`

so:

`A_R=1 bit`

`A_Acc=1/2`.

Both signed diagnostics select the `lower-index` side. The Stage 3A microscopic maps remain bijective.

The supported Stage 3C statement is therefore:

**the canonical reversible blank-memory ensemble contains a record-defined orientation toward the lower-index side under the declared record/accessibility interface.**

## Validation

Focused Stage 3C tests: **8**.

GitHub Actions clean PR merge-ref regression at this checkpoint:

`128 passed in 2.79s`.

## What this does not establish

Stage 3C does not establish:

- that lower index is fundamentally or physically the past;
- that the blank boundary is the unique or necessary source of the orientation;
- a thermodynamic arrow;
- causal direction from mutual information alone;
- ontological becoming;
- phenomenal passage;
- a fundamental physical arrow of time.

## Why two diagnostics are required

Mutual information and Bayes-optimal accessibility probe related but distinct properties. Requiring both signed contrasts to agree prevents the Stage 3C label from being assigned solely because of one metric's behavior.

A zero score in either diagnostic, or opposite signs, returns orientation `none`.

## Next control requirement

Stage 3D must test whether this interpretation survives the protocol's required controls:

- exact history reversal should flip the sign;
- equal forward/reverse mixture should cancel the signed bias;
- order-only/no-record control should give no orientation;
- independent uniform initial memory should remove or weaken the canonical record.

Only after those controls can the role of the asymmetric boundary be isolated more strongly.
