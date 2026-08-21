# Stage 8F Results — Ablation / Reconstruction / Mismatch Matrix

Status: **completed for the declared finite Stage 8 continuation family, pending final documentation-synchronized regression.**

## Status vocabulary

`preserved`, `reconstructible`, `inaccessible`, `lost`, `underdetermined`, `not_established`.

These are functional statuses only.

## Ablation matrix

| Ablation | V physical multiplicity | V selected-vs-unselected semantics | V weights | P-V class transport | O-V extension | current record | local record access |
|---|---|---|---|---|---|---|---|
| record coupling neutralized | preserved | preserved | preserved | preserved | preserved | lost | lost |
| QExt collapsed to singleton | lost | preserved | reconstructible | preserved | preserved | preserved | preserved |
| modal semantics removed | preserved | lost | preserved | preserved | preserved | preserved | preserved |
| weights unfixed | preserved | preserved | underdetermined | preserved | preserved | preserved | preserved |
| explicit perspective maps removed | preserved | preserved | preserved | reconstructible | preserved | preserved | preserved |
| event/class correspondence removed | preserved | preserved | preserved | not_established | preserved | preserved | preserved |
| current record access hidden | preserved | preserved | preserved | preserved | preserved | preserved | inaccessible |

## Strongest new ablation witness

Neutralizing the e1 record write in both continuations produces a two-member constrained continuation family with:

- physical dimension 14;
- minimum clock-reduction rank 14;
- 108 continuation-specific genuine clock transports;
- state/inverse/metric covariance within tolerance;
- two physically inequivalent future completions sharing the same e1 current state;
- matched epistemic/ontic operational views under `(0.5,0.5)`;
- distinct privileged modal semantics;
- detectable weight mismatch;
- zero current target-memory information in both continuations.

Thus the declared finite construction supplies an executable counterexample to any implication of the form:

`nontrivial P/O/V structure => current target-specific R`.

Equivalently, current R is not required for the represented nontrivial V/P/O roles in this ablated family.

This is a finite-model counterexample, not a universal irreducibility theorem.

`record-neutral V witness != universal R-V independence theorem`.

## Singleton result

With one continuation class retained:

- physical continuation multiplicity is lost;
- selected-vs-unselected model typing remains formally distinct;
- the only normalized continuation weight is reconstructible as `1`;
- current record and genuine perspective transport remain present.

Therefore physical multiplicity, modal typing, and nontrivial weighting are distinct roles in the declared interface.

## Semantic non-reconstruction

Removing selected-vs-unselected model typing does not permit unique reconstruction of that semantic role from retained public P/O/current-R structure.

The same retained carrier supports both:

- hidden selected continuation semantics;
- no-selected-continuation semantics.

Result: the semantic role is lost under direct ablation and has no unique reconstruction witness from those retained public structures.

## Weight non-reconstruction

The same two-continuation carrier supports both `(0.5,0.5)` and `(0.75,0.25)`, and the two assignments produce different future predictions.

Therefore nontrivial V weights are `underdetermined` when the assignment is removed; they are not reconstructed from carrier structure alone.

## Perspective-map reconstruction

All 108 canonical continuation-specific explicit maps are reconstructed from retained per-node coordinates by:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

The reconstruction matches the reference maps and preserves state transport, inverse structure, and induced-metric covariance to tolerance.

Result: explicit P-V edge matrices are `reconstructible` in the declared atlas.

`P-V map reconstruction != P=V`.

## Event correspondence

If local P atlases and V classes are kept but explicit event/class `chi` is removed, cross-perspective P-V correspondence is `not_established` rather than false.

Wrong declared class/event correspondences remain separately detectable mismatches.

## Record accessibility

Hiding the record readout keeps global current record information represented but makes the declared local record interface inaccessible.

`inaccessible != globally absent`.

## Mismatch matrix

All declared controls are detected:

1. wrong continuation map — Stage 8D wrong-map state residual remains nonzero;
2. wrong physical class correspondence — rejected;
3. wrong event correspondence — rejected;
4. `(0.75,0.25)` weight mismatch — transported predictive density changes;
5. wrong record-observable coordinates — rejected by metric/semantic cross-check.

`covariance of a wrongly typed observable != semantic correctness`.

## Boundaries

Stage 8F does not establish:

- metaphysical irreducibility of V, P, O, or R;
- universal independence of V from R;
- ontically open physical futures;
- P=V or O=V;
- directional R in the canonical V carrier;
- full Stage 8C measurement-family covariance.

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`underdetermined != ontically open`.

`full Stage 8C measurement covariance remains not_established`.

## Exit criteria

Stage 8F closes criteria **42–47**. Criteria **48–50** remain Stage 8G work.

## Validation

Implementation-inclusive full regression:

**`662 passed in 139.81s`**

implementation head `123b552f91ab42c8d33465a8ef48978adc46839c`

PR merge-ref `ecaadaac42cdec1d091b3e521bc07335ac4236e0`

A final documentation-synchronized regression follows.

## Strongest bounded statement

**Within the declared finite Stage 8 family, neutralizing the current record write leaves a two-continuation constrained P/O/V witness with genuine clock transport, physically inequivalent future completions, selected-vs-unselected modal underdetermination, and nontrivial weight-sensitive prediction while target-specific current record information vanishes. Separately, collapsing QExt to one class removes physical multiplicity without removing formal modal typing and makes its sole weight reconstructible; nontrivial weights are underdetermined by the two-class carrier; explicit P-V edge maps are reconstructed from per-node coordinates; removing event/class correspondence makes cross-perspective P-V identification not established; and hiding local record access does not erase the global record. This strengthens a layered-role interpretation in the declared toy family but does not establish fundamental ontology, universal independence, or ontic openness.**

## Next

Stage 8G — synthesis and evidence-selected next gate.
