# Stage 8F Notes — Ablation / Reconstruction / Mismatch Matrix

Status: **completed for the declared finite Stage 8 continuation family.**

## Question

Which Stage 8 roles remain directly represented, which can be reconstructed, which become locally inaccessible, which are lost, which are underdetermined, and which are not established when one declared ingredient is neutralized at a time?

The status vocabulary is functional rather than metaphysical:

- `preserved`
- `reconstructible`
- `inaccessible`
- `lost`
- `underdetermined`
- `not_established`

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`underdetermined != ontically open`.

`inaccessible != globally absent`.

`not_established != false`.

## Frozen roles

Stage 8F tracks seven roles:

1. `V_physical_multiplicity`
2. `V_selected_vs_unselected_semantics`
3. `V_weights`
4. `P_V_class_transport`
5. `O_V_extension_relation`
6. `current_record_content`
7. `local_record_access`

## Record-coupling neutralization

The strongest new ablation witness replaces the canonical e1 record write by identity in both continuations:

- `h_L^0`: current action identity, future action identity;
- `h_R^0`: current action identity, future action C-sector phase.

This pair is **not** passed through the canonical Stage 8A `QExt` validator because that validator intentionally requires the original one-bit current-record prefix. Instead Stage 8F re-derives and checks the ablated constrained construction directly.

Executable checks establish that the no-record pair retains:

- physical dimension 14;
- rank-14 A/B/C reductions;
- two physically inequivalent future continuations;
- a common e1 current state;
- 108 distinct-clock state transports with inverse and induced-metric covariance;
- matched epistemic/ontic operational views under `(0.5,0.5)`;
- distinct privileged selected-vs-unselected modal structure;
- a detectable `(0.75,0.25)` weight mismatch.

At the same time, current target-memory mutual information falls to zero for both continuations.

Therefore the declared finite family contains a witness with nontrivial `P/O/V` structure while current target-specific `R` is absent.

`record-neutral V witness != universal R-V independence theorem`.

## Singleton-QExt ablation

Collapsing the carrier to one admissible class `h_L` removes physical continuation multiplicity, but the two model schemas remain formally distinct:

- epistemic selected-continuation model;
- ontic no-selected-continuation model.

The sole normalized continuation weight is then reconstructible as `(1.0,)`.

Thus:

`physical continuation multiplicity != selected-vs-unselected type distinction`.

`singleton support != absence of a formal selected-vs-unselected type distinction`.

## Modal-semantics ablation

If selected-vs-unselected model typing is discarded while the physical carrier, weights, P/O structure, and current record are retained, the semantic role is lost.

Stage 8E supplies the non-reconstruction witness: the same retained public P/O/current-R carrier supports both selected-`h*` and no-selected-continuation semantics.

Therefore the removed modal semantic distinction is not uniquely reconstructed from those retained public structures in this family.

## Weight ablation

If q_E/K are left unspecified while the same carrier is retained, the weight role is `underdetermined`, not reconstructible.

The same carrier admits at least:

- `(0.5,0.5)`;
- `(0.75,0.25)`.

These assignments produce different future predictions, so carrier structure alone does not select one nontrivial weight assignment.

For a singleton carrier, by contrast, normalization reconstructs the only weight as `1`.

## Perspective-map ablation

Removing explicit cross-clock edge matrices while retaining each continuation's per-node reduction coordinates does not remove the tested P role.

All 108 canonical continuation-specific maps are reconstructed by:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

State transport, inverse structure, and induced-metric covariance are preserved to numerical tolerance.

Result: explicit edge matrices are `reconstructible` in the declared Stage 8D atlas.

`P-V map reconstruction != P=V`.

## Event/class correspondence ablation

Removing the declared event/class correspondence `chi` while retaining local continuation atlases and V classes leaves local P and V structure in place, but the cross-perspective `P-V` correspondence becomes `not_established`.

This is not the same as a failed correspondence. A wrong declared class/event map is an executable mismatch; no declared `chi` is insufficient typing for the comparison.

## Record-access ablation

Hiding the record from the local readout interface does not erase the globally represented one-bit current record.

Therefore:

- `current_record_content = preserved`;
- `local_record_access = inaccessible`.

## Mismatch matrix

Stage 8F retains five discriminating controls:

- wrong continuation map;
- wrong physical continuation-class correspondence;
- wrong event correspondence;
- weight mismatch;
- wrong observable coordinates.

All are detected by executable residuals or validity audits.

The observable-coordinate control preserves the Stage 8E guard:

`covariance of a wrongly typed observable != semantic correctness`.

## Directional-record and measurement boundaries

The canonical Stage 8 V family still has current record content but no directional record arrow. Stage 8F does not upgrade this into a universal R-V incompatibility claim.

The stronger cross-continuation Stage 8C measurement-family covariance also remains:

`full Stage 8C measurement covariance = not_established`.

## Current execution ledger

Stage 8F closes criteria **42–47**:

42. typed ablation/status matrix with six functional statuses kept distinct;
43. record-neutral constrained continuation pair retains nontrivial P/O/V while current R is lost;
44. singleton-QExt ablation separates physical multiplicity from modal typing and makes the sole weight reconstructible;
45. selected-vs-unselected semantics and nontrivial weights are not uniquely reconstructed from retained public carrier structure;
46. explicit P-V maps are reconstructible from node coordinates while removal of `chi` makes cross-perspective P-V correspondence not established;
47. hidden record access and wrong-map/class/event/weight/observable controls distinguish inaccessible/lost/underdetermined/not-established cases.

Criteria **48–50** remain Stage 8G work.

## Validation

Initial implementation-inclusive full regression:

**`662 passed in 139.81s`**

on implementation head `123b552f91ab42c8d33465a8ef48978adc46839c` / PR merge-ref `ecaadaac42cdec1d091b3e521bc07335ac4236e0`.

A final documentation-synchronized regression follows after propagating this checkpoint to current planning documents.

## Next

Stage 8G — synthesis and evidence-selected next gate.
