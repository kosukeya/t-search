# Stage 7F Results — Ablation / Reconstruction / Mismatch Matrix

Status: **scientific implementation complete; documentation-head regression pending.**

## Main result

Stage 7F separates functional loss, reconstruction, inaccessibility, and lack of evidence inside the single Stage 7 constrained quantum family.

| Neutralization | Result |
| --- | --- |
| remove memory record carrier | target record / direction / local record readout `lost` |
| neutralize record coupling | R roles `lost`; multi-clock P and internal event anchor preserved |
| remove internal history anchor | target-specific record preserved; directional R `not_established` |
| remove explicit cross-clock edge matrices | P maps and P-R covariance `reconstructible` from retained reductions |
| remove `chi` | local P/R preserved; cross-perspective P-R covariance `not_established` |
| hidden local memory interface | local record readout `inaccessible` |
| maximally noisy local memory interface | local record readout `inaccessible` |

## P + O without R

The internally anchored Stage 7C no-record family retains the tested perspective structure:

- 54 distinct-clock/readout comparisons;
- rank 14 at the tested reductions;
- state transport residual `<=1e-9`;
- inverse residual `<=1e-9`;
- induced-metric covariance residual `<=1e-9`;
- internal `e0<e1<e2` anchoring retained.

Yet:

- `record_defined=false`;
- `A_R=0`;
- `A_acc=0`.

Therefore the implication

`P + internal O => R`

is refuted in the declared Stage 7 family.

This is not a universal theorem about every model containing perspectives and order.

## Explicit P-edge reconstruction

With explicit Stage 7D edge matrices removed but the common physical carrier and per-node reduction coordinates retained, Stage 7F reconstructs

`S_{Y<-X}=C_Y @ inv(C_X)`

for all 54 directed distinct-clock/readout comparisons.

Reference-map agreement, state transport, inverse consistency, induced-metric covariance, record-score covariance, and accessibility covariance all remain within `1e-9`.

Thus the explicit edge-matrix representation is `reconstructible` in this interface.

Guard:

`explicit perspective-map reconstruction != elimination of the perspective layer`.

## Record correlation without directional anchor

The Stage 7B witness survives removal of the Stage 7C history anchor:

- `I(Q;M)=1 bit` after recording;
- target-specific record witness positive;
- directional score not defined.

Therefore:

`target-specific record correlation != record-defined temporal direction`.

Direction is classified `not_established`, not `false`.

## Accessibility

Hidden and maximally noisy memory interfaces preserve the globally represented record and global orientation while local record information vanishes.

Therefore:

`local_record_readout = inaccessible`,

not `lost`.

## Event correspondence

Removing `chi` leaves local P and local R intact but makes the cross-perspective P-R comparison untyped.

Therefore:

`P_R_covariance = not_established`.

A wrong/misdeclared `chi`, by contrast, is an executable mismatch:

- record-score residual `2`;
- accessibility-score residual `1`.

## Local edge mismatch

The Stage 7E perturbation of only `C/e1 -> B/e0` remains localized. Map/state/metric/record-statistic diagnostics fail on that path while the other two indirect paths remain consistent. The tested projector algebra can nevertheless continue to similarity-transport, so observable correspondence alone is not sufficient for full path consistency.

## Strongest bounded statement

**Within the declared Stage 7 finite constrained family, the record-defined role R is not reconstructed from the retained tested perspective structure plus internal neutral event anchoring when record coupling is neutralized, whereas explicit cross-clock edge matrices are reconstructed from the common physical carrier and per-perspective reductions. Local record access can separately become inaccessible without global record destruction, and missing event correspondence makes P-R covariance not established rather than false.**

This strengthens the functional layered interpretation of P/O/R but does not establish metaphysical irreducibility, a fundamental ontology of time, ontological becoming, phenomenal passage, or a novel empirical prediction.

## Validation

Stage 7F adds **12 focused tests**.

Implementation-inclusive PR merge-ref regression:

`548 passed in 146.97s`.

## Exit criteria

Stage 7F satisfies criteria **30–31** in the declared scope:

30. memory / record / perspective / access / correspondence ingredients are neutralized separately where applicable;
31. `lost`, `reconstructible`, `inaccessible`, and `not_established` are distinguished by executable evidence.

Criteria 32–36 remain for Stage 7G synthesis, Stage 8 gate selection, interpretation review, and final merge-readiness validation.

## Next

Stage 7G — synthesis and Stage 8 gate.
