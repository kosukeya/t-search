# Stage 8E Notes — P/O/R/V Compatibility and Underdetermination

Status: **completed for the declared canonical finite continuation family.**

## Question

Which relations among perspective `P`, internal event/order structure `O`, record structure `R`, and quantum Potentiality `V` are actually supported when they are tested on the same continuation-aware constrained quantum carrier?

Stage 8E deliberately distinguishes **current target-specific record content** from a **directional record arrow**. The canonical Stage 8A continuations preserve the recorded target at e2, so a one-bit current record can coexist with zero lower-minus-upper directional score.

## Observable typing correction

The first Stage 8E implementation exposed an important coordinate error. The Stage 7/8 record projector is defined in the fixed A-rest support basis, whereas Stage 8D perspective maps use continuation-specific QR support coordinates. Inserting the fixed-basis matrix directly into QR coordinates produced a covariantly transported but semantically wrong zero-information observable.

The corrected construction uses the explicit basis change

`T_{h,e}=Q_{h,A,e}^dagger K_A`,

then

`O_QR = T_{h,e} O_fixed T_{h,e}^{-1}`,

before lifting to physical coefficients and transporting to the requested clock chart.

This yields the additional guard:

`covariance of a wrongly typed observable != semantic correctness`.

The corrected record interface is also checked against the independent Stage 8A direct record diagnostic, preventing a false positive in which all perspectives agree on the wrong observable.

## P-O compatibility

The three A-clock relational event effects e0/e1/e2 are represented as physical effects for each continuation and transported through each continuation-specific atlas.

The executable checks require:

- operator correspondence under the re-derived clock maps;
- induced-metric self-adjointness;
- effect completeness;
- perspective-independent probabilities for the same declared physical state/effects.

Result: `P-O(event effects) = compatible` in the canonical family.

Guard: `event-effect covariance != temporal succession`.

## P-R compatibility at the current-record level

The corrected target and memory observables reproduce the Stage 8A one-bit current record and transport consistently across A/B/C charts. Wrong-target information remains zero to tolerance, while reusing the bare fixed-coordinate observable in B/C charts fails the induced-metric self-adjointness check.

Result: `P-R(current record) = compatible`.

Guards:

- `current record covariance != directional record arrow`;
- `corresponding observable transport != bare matrix reuse`.

## O-V compatibility

The two canonical physical continuation classes share the same frozen prefix through e1 and first differ only at e2. A candidate that changes the current prefix is rejected, and terminal `QExt(e2)=empty` remains explicit.

Result: `O-V(extension) = compatible` for the declared prefix/extension relation.

Guard: `O-V compatibility != O=V`.

## R(current)-V underdetermination

`h_L` and `h_R` are physically inequivalent future continuations but have the same target-specific current record. Therefore current record content does not select a unique represented future continuation in this family.

Result: `R(current)-V = underdetermined`.

Guard: `record content != unique future continuation`.

## O does not force directional R

For both canonical Stage 8 continuation classes, the corrected record profile has:

- lower information = 1 bit;
- current information = 1 bit;
- upper information = 1 bit;
- record score = 0;
- accessibility score = 0;
- orientation = none.

Thus the record exists but carries no lower-vs-upper directional contrast.

The Stage 7C forward record-scramble completion provides a contrast on the same e0<e1<e2 skeleton and the same A/e1 current state, with record score `+1` and a defined lower-index orientation.

Result: `O=>R(direction) = implication_refuted` in this declared finite family.

Guard: `order != directional record arrow`.

## P/O/current-R do not fix V semantics

The same `QuantumContinuationCarrier`, current physical structure, event/order structure, and current-record structure host both:

- epistemic selected-`h*` semantics;
- ontic-extension no-selected-continuation semantics.

With matched `(0.5,0.5)` weights their public transported modal views remain equal at all nine nodes, while privileged modal diagnostics remain distinct. Changing ontic weights to `(0.75,0.25)` remains detectably different after B/C transport.

Result: `P/O/current-R=>V semantics = underdetermined`.

Guard: `same P/O/current-R public data != modal identity`.

## Full integration boundary

The canonical Stage 8 V carrier does not itself contain directional R, and Stage 8D still reports the stronger cross-continuation Stage 8C measurement-family covariance as `not_established`.

Therefore:

`full P/O/directional-R/V = partial`.

This does **not** establish universal R-V incompatibility. It only prevents the project from upgrading current-record compatibility into a stronger directional full-integration claim without additional evidence.

## Validation

After the record-coordinate correction, workflow run #838 produced **650 passing scientific tests**. The only remaining failure in that run was a Stage 8D documentation assertion requiring the exact historical guard `equal numeric clock readings != event identity` in the Stage 8D results file.

The documentation-only failure is repaired during the Stage 8E synchronization pass; a final full regression is required on the synchronized head.

## Current execution ledger

Stage 8E closes criteria **36–41**:

36. P-O event-effect covariance;
37. corrected P-R current-record covariance plus wrong-target/bare-observable controls;
38. O-V future-only extension compatibility and prefix/terminal controls;
39. R(current)-V underdetermination across physically inequivalent continuations;
40. same order/current state does not force directional R;
41. same P/O/current-R carrier supports distinct V semantics while stronger directional/full-measurement integration remains explicitly partial.

Criteria **42–50** remain Stage 8F–G work.

## Next

Stage 8F — ablation / reconstruction / mismatch matrix.
