# Stage 6A Notes — Structural Inventory and Executable Adapters

Status: **completed pending final documentation-inclusive regression**.

Stage 6A converts selected results from Stages 1--5 into a common executable witness interface. It deliberately does not classify the Stage 6B implication matrix yet.

## 1. Evidence rule

A Stage 6A witness must recompute its measurements through existing stage APIs. A prose-derived boolean such as `has_arrow=True` is not accepted as evidence.

Every witness record contains:

- `witness_id`;
- `source_stage`;
- a declared `domain`;
- explicit `assumptions`;
- semantic `roles`;
- machine-readable `measurements`;
- an optional numerical `tolerance`.

The implementation lives in:

`src/t_search/stage6_inventory.py`.

A JSON inventory can be printed with:

`python experiments/stage6a_structural_inventory.py`.

## 2. W1 — Stage 1 reconstruction / accessibility

W1 recomputes the canonical six-event DAG, projects the complete labeled one-hop view family, glues that family, and compares the reconstruction with the original block.

It separately evaluates a single local interface at event `a`.

The complete family reconstructs the labeled block and its reachability relation. At the same time, event `e` is globally reachable from `a` but is absent from the one-hop view at `a`.

This witness therefore carries both global-family reconstructibility and a declared local-accessibility limitation without converting that observation into a Stage 6B implication classification yet.

## 3. W2 — Stage 2 modality / operational underdetermination

W2 recomputes the canonical epistemic-history and ontic-extension models at Actuality prefix:

`('p','n')`.

The ontology-neutral operational views are compared through the Stage 2 operational API.

The witness records:

- operational equality;
- equality of Actuality, immediate alternatives, and probabilities;
- the epistemic selected complete history;
- absence of a selected-future field from the ontic model;
- distinct runtime Potentiality types;
- the live-history counts.

The adapter therefore preserves the distinction between operational comparison and modal/model structure rather than erasing it into one boolean.

## 4. W3 — Stage 3 order / record direction

W3 calls the frozen Stage 3D control suite and records the assessments for:

- `forward`;
- `reversed`;
- `symmetric`;
- `no-record`;
- `uniform-memory`.

For each control it records:

- neutral orientation label;
- whether a record-defined orientation is detected;
- signed mutual-information record score;
- signed accessibility score;
- reversibility of the actual declared microscopic update maps;
- declared position count.

Important adapter correction: the Stage 3 `RecordOrientationAssessment.microscopic_maps_reversible` field refers to the canonical `U_rec/U_scr` pair. The Stage 6A adapter therefore computes reversibility of the `no-record` control from its actual `u_identity/U_scr` maps rather than silently reusing canonical metadata.

## 5. W4 — Stage 4 same-clock transition structure

W4 exhaustively recomputes the canonical `d=4` Stage 4E transition diagnostics:

- identity;
- inverse;
- composition;
- agreement with the independently constructed expected system transition;
- unitarity.

Only residuals and the declared tolerance are stored. The adapter does not label these reversible transition arrows as a temporal arrow.

## 6. W5 — Stage 5 genuine clock changes and operational covariance

W5 recomputes all:

`6 * 3^3 = 162`

ordered distinct-clock three-perspective routes in the canonical qutrit model and records the maximum support-coordinate composition residual.

It also recomputes Born covariance for all ordered distinct source/target clocks and all reading pairs using a generic physical state and transformed rank-one support projectors.

Finally, it recomputes the explicit entanglement control:

- A-clock perspective: approximately `1 bit`;
- B-clock perspective: approximately `0 bit`;
- C-clock perspective: approximately `0 bit`.

Thus W5 carries both an operational-correspondence diagnostic and a perspective-dependent-structure diagnostic.

## 7. Machine-readable inventory

`build_stage6a_inventory()` returns exactly:

`(W1,W2,W3,W4,W5)`

with source stages:

`(1,2,3,4,5)`.

`stage6a_inventory_rows()` converts them to JSON-friendly records while preserving measurement names, values, units, domains, assumptions, roles, and tolerances.

The purpose is to let Stage 6B attach witness IDs and measured quantities to each implication classification instead of relying on remembered prose.

## 8. What Stage 6A does not establish

Stage 6A does **not** yet claim that:

- `order => arrow` is universally false;
- any Stage 6 layer is fundamental or irreducible;
- the five witnesses span every possible temporal role;
- the Stage 5 groupoid-like atlas is time itself;
- operational equivalence settles modal or ontological equivalence;
- record orientation is phenomenal passage;
- a particular Stage 6 candidate `T` has already been selected.

Those questions begin in Stage 6B and later substages.

## 9. Focused tests

Stage 6A adds **13 focused tests** checking:

- each W1--W5 adapter against direct existing-stage API calls;
- expected discrete witness properties;
- numerical transition/composition/Born residuals remain below declared tolerances;
- exact W1--W5 inventory coverage;
- machine-readable JSON serialization;
- measurement lookup validation.

Initial code/test checkpoint:

`352 passed in 18.57s`.
