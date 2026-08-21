# Stage 8E Results — P/O/R/V Compatibility and Underdetermination

Status: **completed for the declared canonical finite continuation family, pending final documentation-synchronized regression.**

## Compatibility matrix

| Relation | Status | Evidence |
|---|---|---|
| `P-O(event effects)` | `compatible` | continuation-specific clock atlases transport the ordered event-effect family with induced-metric consistency |
| `P-R(current record)` | `compatible` | corrected corresponding target/memory observables reproduce and transport the one-bit current record; wrong-target and bare-matrix controls reject false covariance |
| `P-V(class/weights)` | `compatible` | inherited Stage 8D continuation-class/weight covariance |
| `O-V(extension)` | `compatible` | canonical continuations share the prefix through e1 and first differ only at e2; invalid-current and terminal controls pass |
| `R(current)-V` | `underdetermined` | physically inequivalent h_L/h_R share the same current target-specific record |
| `O=>R(direction)` | `implication_refuted` | canonical V carrier has zero directional score, while the same order/current state admits the Stage 7C record-scramble completion with score +1 |
| `P/O/current-R=>V semantics` | `underdetermined` | the same physical carrier/public P-O-current-R data host selected-h* and no-selected-continuation semantics |
| `full P/O/directional-R/V` | `partial` | canonical V carrier lacks directional R and full Stage 8C measurement-family covariance remains not_established |

## Record-coordinate correction

The first implementation used the fixed A-rest support projector directly as if it were already expressed in continuation-specific QR support coordinates. That produced a formally transported but semantically wrong record observable and returned zero record information.

The corrected path explicitly changes basis before the physical lift and perspective transport:

`T_{h,e}=Q_{h,A,e}^dagger K_A`,

`O_QR=T_{h,e} O_fixed T_{h,e}^{-1}`.

The resulting current record is cross-checked against the independent Stage 8A direct diagnostic.

Frozen guard:

`covariance of a wrongly typed observable != semantic correctness`.

## Current record versus directional record

For both canonical continuation classes after the correction:

- `I_lower = 1 bit`;
- `I_current = 1 bit`;
- `I_upper = 1 bit`;
- `A_R = 0`;
- `A_acc = 0`;
- orientation = `none`.

Thus record content is present while record-defined temporal direction is absent.

The Stage 7C record-scramble contrast shares the same `e0<e1<e2` event skeleton and the same A/e1 current state but has:

- `A_R = +1`;
- defined lower-index orientation.

Therefore the declared finite family refutes `O=>R(direction)`.

## Modal underdetermination survives P/O/current-R

The canonical epistemic and ontic-extension models share the same continuation carrier and public P/O/current-record structure. With matched `(0.5,0.5)` weights, public modal views match at all nine physical-clock nodes while privileged selected-vs-unselected modal structure remains different.

Changing ontic weights to `(0.75,0.25)` remains detectable after B/C transport, so the public equality is not hardcoded.

Accordingly:

`same P/O/current-R public data != modal identity`.

## Boundaries

Stage 8E does not establish:

- `P=O=R=V`;
- universal irreducibility of any layer;
- ontic openness of the physical future;
- directional R in the canonical Stage 8 V carrier;
- full Stage 8C cross-continuation measurement covariance;
- thermodynamic arrow, ontological becoming, or phenomenal passage.

`directional R absent in canonical Stage 8 V carrier != universal R-V incompatibility`.

`not_established != false`.

## Validation history

Before the coordinate correction, Stage 8E exposed a false record readout caused by basis mismatch.

After the correction, workflow run #838 produced:

**`650 passed / 1 failed`**

where the single failure was documentation-only: the Stage 8D results file lacked the exact historical guard `equal numeric clock readings != event identity` required by the documentation-consistency audit. All Stage 8E scientific tests passed in that run.

A final documentation-synchronized full regression follows after repairing that guard and advancing current planning documents to Stage 8E completed / Stage 8F next.

## Exit criteria

Stage 8E closes criteria **36–41**. Criteria **42–50** remain Stage 8F–G work.

## Strongest bounded statement

**Within the declared canonical finite continuation family, P is compatible with the tested ordered event effects, current target-specific records, and continuation-class/weight V structure; O is compatible with future-only extension structure; physically inequivalent V continuations can share the same current record; and the same P/O/current-R public carrier can support distinct selected-vs-unselected modal semantics. At the same time, order does not force a directional record arrow, the canonical V carrier has current record content but no directional R, and the stronger full cross-continuation measurement covariance remains not established. This supports a layered compatibility/underdetermination picture rather than collapse of P/O/R/V into one role.**

## Next

Stage 8F — ablation / reconstruction / mismatch matrix.
