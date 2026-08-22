# Stage 9F Notes — Ablation / Reconstruction / Accessibility

Status: **Stage 9F completed; criteria 43–47 satisfied.**

## Purpose

Stage 9E established positive structural compatibility of `P/O/R_direction/V` in the declared finite constrained family. Stage 9F asks a different question:

> Which represented roles survive, disappear, become reconstructible, become locally inaccessible, or remain underdetermined when one ingredient is removed at a time?

The functional vocabulary is:

`preserved / reconstructible / inaccessible / lost / underdetermined / not_established`.

These are model-level statuses, not metaphysical claims.

## Role typing

Stage 9F keeps the refined record/modal bookkeeping explicit:

- `R_content`: represented target-memory record content;
- `R_direction`: asymmetric lower/upper record relation;
- `R_access`: availability of represented record content to the declared local interface;
- `V_extension_multiplicity`: more than one physically inequivalent continuation;
- `V_selected_vs_unselected_semantics`;
- `V_weights`;
- physical `P` perspective transport;
- event/class correspondence;
- typed cross-perspective P-R-V identification;
- the O-V current-anchor/extension relation.

`A_acc` remains a diagnostic of **directional accessibility asymmetry**. It is not identical to the yes/no question whether record content is locally accessible.

`A_acc=0 != inaccessible record content`.

## Directional-mechanism ablations

### Record write neutralized

The existing Stage 9B no-record construction removes `U_rec` but retains the common scrambler and the independent h_L/h_R future branch action.

Executable outcome:

- current target-memory information vanishes;
- `R_direction` and its accessibility asymmetry vanish;
- h_L/h_R `V_extension` remains nontrivial;
- the re-derived constrained carriers remain valid with minimum chart rank 14;
- a two-continuation clock atlas still supplies 108 ordered distinct-clock comparisons.

This is a V-without-record witness in the declared family.

### Scrambler neutralized

A distinct Stage 9F construction retains the e1 record write but removes the e2 target scrambler:

- `h_L: (I,U_rec,U_rec)`;
- `h_R: (I,U_rec,Z_C U_rec)`.

The current record remains represented while lower/upper record correlations become symmetric.

Executable outcome:

- current target-memory information remains one bit;
- `A_R=0`;
- directional accessibility asymmetry `A_acc=0`;
- h_L/h_R `V_extension` remains nontrivial;
- the re-derived constrained carriers remain valid;
- the two-continuation clock atlas retains 108 ordered distinct-clock comparisons.

The discriminating relation is therefore:

`R_content preserved + R_direction lost + V_extension multiplicity preserved`.

This directly sharpens:

`record content != directional record arrow`.

## Singleton-QExt ablation

Retain only h_L at the same current anchor.

Executable outcome:

- `|QExt|=1`;
- current record information remains one bit;
- `(A_R,A_acc)=(+1,+0.5)`;
- `V_extension_multiplicity` is lost;
- formal selected-vs-unselected typing remains distinct on singleton support;
- the ontic-extension wrapper still has no selected-continuation field;
- normalization reconstructs the sole weight as `1`;
- the remaining continuation retains 54 ordered distinct-clock comparisons.

This tests whether nonzero directional R requires branching multiplicity in the declared family.

## Modal-semantics and weight ablations

### Modal semantics removed

Keep the physical P/O/R carrier, continuation classes, and weights but erase selected-vs-unselected model typing.

Because Stage 9C already supplied distinct privileged modal structures with matched public data, the erased semantic role is not uniquely recoverable from the retained public carrier.

### Weights unfixed

Keep carrier and modal typing but remove the declared `q_E/K` assignment.

The same carrier admits `(0.5,0.5)` and `(0.75,0.25)` with different future predictions while current directional data remain fixed.

Therefore nontrivial `V_weights` are `underdetermined`, not reconstructed from the carrier alone.

## Accessibility ablation

Construct a declared local public view that retains:

- current anchor;
- continuation identities;
- continuation weights;
- current record information;
- global directional score/orientation;

while omitting local `accessibility_score`.

The underlying global record/direction and V structure remain represented, but `R_access` is `inaccessible` through the ablated interface.

`inaccessible != globally absent`.

## Perspective reconstruction and typing

### Explicit P edges removed

Retain every per-node continuation-specific QR coordinate matrix but remove stored edge matrices.

Reconstruct:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

All 108 canonical h_L/h_R ordered distinct-clock edges are reconstructed within tolerance.

### Event/class correspondence removed

Keep the local clock atlas and physical edge reconstruction but erase declared event/class `chi`.

Bare P transport remains executable, but typed cross-perspective identification of corresponding events/continuation classes becomes `not_established`.

### Wrong observable coordinates

Reuse of a bare source-chart record-observable matrix is retained as a deliberate mismatch and is rejected.

`covariance of a wrongly typed observable != semantic correctness`.

## Interpretation guards

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
- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- full Stage 9C future-signature measurement covariance remains `not_established`.

## Validation

GitHub Actions run #1077:

**`754 passed in 438.94s`**.

## Next

**Stage 9G — synthesis and evidence-selected next gate**.