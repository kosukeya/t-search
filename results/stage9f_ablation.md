# Stage 9F Results — Ablation / Reconstruction / Accessibility Matrix

Status: **Stage 9F complete; criteria 43–47 satisfied.**

## Functional status vocabulary

`preserved / reconstructible / inaccessible / lost / underdetermined / not_established`.

These are finite-model functional classifications only.

## Main ablation outcomes

| ablation | discriminating outcome |
| --- | --- |
| record write neutralized | `R_content/R_direction/R_access = lost`; nontrivial h_L/h_R V and re-derived P survive |
| scrambler neutralized | `R_content = preserved`, `R_direction = lost`, local record access preserved; nontrivial V and P survive |
| QExt collapsed to singleton | V extension multiplicity `lost`; nonzero directional R preserved; sole weight `reconstructible` as 1 |
| modal semantics removed | selected-vs-unselected semantic role `lost` and not uniquely reconstructed from retained public carrier |
| weights unfixed | `V_weights = underdetermined` |
| local record access hidden | global R content/direction preserved; `R_access = inaccessible`; V retained |
| explicit perspective edges removed | `P_perspective_transport = reconstructible` from per-node coordinates |
| event/class correspondence removed | bare local P remains; correspondence `lost`; typed P-R-V identification `not_established` |

A deliberately wrong record-observable coordinate reuse is also rejected.

## Criterion 43 — directional mechanism ablations

### Record-write neutralization

The Stage 9B no-record carrier retains the h_L/h_R future distinction and a valid re-derived clock atlas while target-memory current information and directional diagnostics vanish.

This is an executable V-without-record witness in the declared family.

### Scrambler neutralization

The distinct no-scramble schedules are:

- `h_L: (I,U_rec,U_rec)`;
- `h_R: (I,U_rec,Z_C U_rec)`.

The current target-memory record remains one bit, but lower/upper record correlations are symmetric:

- `A_R = 0`;
- directional accessibility asymmetry `A_acc = 0`.

The h_L/h_R branch distinction and the re-derived two-continuation P atlas remain; all 108 ordered distinct-clock comparisons remain valid within tolerance.

Therefore the strongest Stage 9F statement here is:

`R_content preserved + R_direction lost + V_extension multiplicity preserved`.

This is stronger than merely comparing a record-bearing carrier with a no-record carrier.

`A_acc=0 != inaccessible record content`.

## Criterion 44 — singleton QExt

With only h_L retained:

- `|QExt|=1`;
- current record information remains 1 bit;
- `(A_R,A_acc)=(+1,+0.5)`;
- selected-vs-unselected formal typing remains distinct;
- no selected-continuation field is added to the ontic-extension model;
- normalization reconstructs the sole weight as `1`;
- the one-continuation clock atlas retains 54 ordered distinct-clock comparisons.

Thus directional R survives after nontrivial `V_extension` multiplicity is deliberately removed.

Combined with the V-without-direction ablations, Stage 9F supplies finite-family countermodels in both directions. This is not a universal independence theorem.

## Criterion 45 — modal semantics and weights

Erasing selected-vs-unselected model typing removes the semantic role. Stage 9C's matched public data and distinct privileged structures show that the erased role is not uniquely reconstructed from the retained public carrier.

Unfixing weights leaves at least `(0.5,0.5)` and `(0.75,0.25)` as distinct normalized assignments on the same carrier; they change future prediction while current directional data remain fixed.

Therefore:

- `V_semantics`: lost under semantic erasure and not uniquely reconstructed;
- `V_weights`: underdetermined when unfixed.

## Criterion 46 — accessibility

The ablated public interface hides the local accessibility field while retaining:

- global one-bit record content;
- nonzero global direction;
- h_L/h_R continuation identities;
- continuation weights.

Therefore `R_access = inaccessible`, while global R and V remain represented.

`inaccessible != globally absent`.

Also:

`A_acc=0 != inaccessible record content`.

The former can arise from symmetric temporal accessibility; the latter is an interface-level access restriction.

## Criterion 47 — reconstruction, correspondence, and typing

Removing explicit P edge matrices but retaining each node's continuation-specific coordinates reconstructs the tested edges using:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

All 108 canonical h_L/h_R ordered distinct-clock edges are recovered within tolerance.

By contrast, removing event/class correspondence does not destroy local clock transport, but it removes the typing resource that licenses claims that one local event/class corresponds to another. Typed cross-perspective P-R-V identification is therefore `not_established`, not reconstructed from bare matrices alone.

The deliberate bare record-observable reuse control is rejected.

## Strongest allowed Stage 9F synthesis

Within the declared finite constrained family:

1. nontrivial continuation multiplicity can survive without directional R;
2. directional R can survive without nontrivial continuation multiplicity;
3. record content can survive without directional R;
4. local accessibility can be hidden while global record/direction and V remain;
5. explicit P edge matrices can be reconstructed from per-node coordinates;
6. event/class correspondence and semantic observable typing are not thereby eliminated.

This strengthens the layered `O/P/R/V` interpretation, but does not prove universal independence or metaphysical primitiveness.

## Guards

- `lost != metaphysically irreducible`;
- `reconstructible != universally redundant`;
- `underdetermined != ontically open`;
- `inaccessible != globally absent`;
- `not_established != false`;
- `record content != directional record arrow`;
- `directional R without V multiplicity != universal R-V independence theorem`;
- `V without directional R != universal R-V independence theorem`;
- `singleton support != absence of a formal selected-vs-unselected type distinction`;
- `P edge reconstruction != P=R or P=V`;
- `local P transport without chi != typed event/class identification`;
- `covariance of a wrongly typed observable != semantic correctness`;
- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- full Stage 9C future-signature measurement covariance remains `not_established`.

## Validation

GitHub Actions run #1077:

**`754 passed in 438.94s`**.

## Next

**Stage 9G — synthesis and evidence-selected next gate**.