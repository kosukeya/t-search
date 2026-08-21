# Stage 8E Notes — P/O/R/V Compatibility and Underdetermination

Status: **completed for the declared canonical finite continuation family.**

## Question

Which relations among perspective `P`, internal event/order structure `O`, record structure `R`, and quantum Potentiality `V` are actually supported when they are tested on the same continuation-aware constrained quantum carrier?

Stage 8E deliberately distinguishes **current target-specific record content** from a **directional record arrow**. The canonical Stage 8A continuations preserve the recorded target at e2, so a one-bit current record can coexist with zero lower-minus-upper directional score.

## Observable typing correction

The first Stage 8E implementation exposed an important coordinate error. The Stage 7/8 record projector is defined in the fixed A-rest support basis, whereas Stage 8D perspective maps use continuation-specific QR support coordinates. Inserting the fixed-basis matrix directly into QR coordinates produced a covariantly transported but semantically wrong zero-information observable.

The corrected construction uses the explicit basis change `T_{h,e}=Q_{h,A,e}^dagger K_A`, then `O_QR=T_{h,e} O_fixed T_{h,e}^{-1}` before lifting to physical coefficients and transporting to the requested clock chart.

`covariance of a wrongly typed observable != semantic correctness`.

The corrected record interface is cross-checked against the independent Stage 8A direct record diagnostic.

## Compatibility results

- `P-O(event effects) = compatible`;
- `P-R(current record) = compatible`;
- `P-V(class/weights) = compatible`;
- `O-V(extension) = compatible`;
- `R(current)-V = underdetermined`;
- `O=>R(direction) = implication_refuted`;
- `P/O/current-R=>V semantics = underdetermined`;
- `full P/O/directional-R/V = partial`.

## Current record versus directional record

For both canonical Stage 8 continuation classes:

- lower information = 1 bit;
- current information = 1 bit;
- upper information = 1 bit;
- **directional record score = 0**;
- accessibility score = 0;
- orientation = none.

Thus record content is present but record-defined temporal direction is absent.

The Stage 7C forward record-scramble completion has the same `e0<e1<e2` skeleton and the same A/e1 current state, but record score `+1` and a lower-index orientation.

Therefore `order != directional record arrow` in this declared finite family.

## Modal underdetermination

Physically inequivalent `h_L/h_R` share the same current target record, so `record content != unique future continuation`.

The same P/O/current-R carrier also hosts epistemic selected-`h*` and ontic no-selected-continuation semantics with matched public transported views, while privileged modal diagnostics remain distinct.

`same P/O/current-R public data != modal identity`.

## Full integration boundary

The canonical Stage 8 V carrier does not itself contain directional R, and Stage 8D still reports the stronger cross-continuation Stage 8C measurement-family covariance as `not_established`.

`full P/O/directional-R/V = partial`.

`directional R absent in canonical Stage 8 V carrier != universal R-V incompatibility`.

## Validation

After the record-coordinate correction, workflow run #838 produced **650 passing scientific tests**. Its only failure was a Stage 8D documentation guard, repaired during Stage 8E synchronization.

The first documentation-synchronized Stage 8E run then exposed only two wording/ledger assertions; both are documentation-only and are repaired without changing the scientific implementation.

## Current execution ledger

Stage 8E closes criteria **36–41**. Criteria **42–50** remain Stage 8F–G work.

## Next

Stage 8F — ablation / reconstruction / mismatch matrix.
