# Stage 6D Notes — Horizontal / Vertical Compatibility

Status: **completed**.

Stage 6D places two arrow types in one executable model without identifying them:

- horizontal perspective maps `M_{q<-p}` from the Stage 6C partial clock atlas;
- vertical order/conditioning maps `D_p(e2<-e1)` represented separately in each perspective.

The implementation lives in:

`src/t_search/stage6_compatibility.py`.

The machine-readable diagnostic entry point is:

`python experiments/stage6d_horizontal_vertical_compatibility.py`.

## 1. Frozen type distinction

The Stage 6 protocol requires:

`perspective-change arrow != temporal-succession arrow`.

Stage 6D preserves this literally in the code. Horizontal maps are reconstructed Stage 6C clock-perspective transformations. Vertical maps are a separately declared reversible conditioning family carried by event labels.

A successful commuting square therefore means that the two typed structures are compatible. It does not mean that they are the same map, the same relation, or the same physical role.

## 2. Explicit event domain

The canonical vertical event family is:

- `e0` at coordinate `0`;
- `e1` at coordinate `1`;
- `e2` at coordinate `3`.

The unequal spacings are deliberate. They make a wrong event correspondence detectable instead of allowing a shifted or permuted correspondence to pass accidentally because all steps have equal size.

The declared forward order relations are:

- `e0 < e1`;
- `e0 < e2`;
- `e1 < e2`.

These event coordinates are part of the Stage 6D toy conditioning model. They are **not** identified with Stage 5 clock-reading indices.

Frozen guard:

`same clock-coordinate value != same physical event`.

## 3. Explicit event correspondence chi

For every source/target perspective pair, Stage 6D constructs an explicit correspondence object:

`chi_{q<-p}: E_p -> E_q`.

The canonical correspondence maps labels identically:

- `e0 -> e0`;
- `e1 -> e1`;
- `e2 -> e2`.

This map is declared independently of source and target clock indices. For example, the canonical perspective pair is `C0 -> B2`, yet its event correspondence still maps `e0 -> e0`, `e1 -> e1`, and `e2 -> e2`. Nothing in the implementation infers `chi` from `0` and `2`.

## 4. Vertical conditioning family

Stage 6D introduces one common reversible conditioning family on the seven-dimensional constrained physical-support coordinates.

For event-coordinate difference `Delta`, the common map is a diagonal unitary:

`U(Delta)=diag(exp(-i * 0.37 * lambda_n * Delta))`,

with centered finite support labels `lambda_n`.

This family satisfies identity, inverse, and composition in the toy model.

For one clock perspective `p`, let `R_p` be the Stage 5 support-coordinate reduction matrix from common physical-support coordinates into the local support coordinates. The local vertical map is defined as:

`D_p(e2<-e1) = R_p U(Delta) R_p^dagger`.

This is a conditioning/succession structure for Stage 6D. It is not asserted to be a fundamental Hamiltonian of time or a record-defined arrow.

## 5. Horizontal maps from the partial atlas

Horizontal maps are not inserted as a complete primitive pairwise table.

For each ordered source/target clock perspective, Stage 6D rebuilds the Stage 6C sparse atlas and uses each available two-hop path through the third clock:

`p -> r_k -> q`.

Thus every horizontal map tested in Stage 6D is obtained by composition of retained Stage 6C atlas edges.

As a diagnostic reference only, Stage 6D compares each path map with the common-physical-space bridge:

`R_q R_p^dagger`.

All such bridge residuals remain below the frozen tolerance in the ideal family.

## 6. Commuting-square test

For an explicit event correspondence `chi`, Stage 6D tests:

`M_{q<-p} D_p(e2<-e1)`

against

`D_q(chi(e2)<-chi(e1)) M_{q<-p}`.

The residual is:

`H_square = || M D_p - D_q M ||_F`.

The canonical `C0 -> B2` case contains three Stage 6C two-hop horizontal paths and three forward event relations, producing exactly nine commuting-square checks.

All nine residuals remain within `1e-10`, and all three declared source-order relations remain order-covariant under the explicit identity correspondence.

## 7. Exhaustive family scan

Stage 6D scans every ordered pair of distinct physical clocks and every source/target reading in the canonical qutrit family:

- ordered distinct-clock choices: `6`;
- source/target reading pairs per clock pair: `3^2 = 9`;
- endpoint cases: `54`;
- Stage 6C indirect horizontal paths per endpoint: `3`;
- total indirect paths: `162`;
- forward event relations per endpoint: `3`;
- total independent order-covariance checks: `162`;
- total commuting squares: `54 * 3 * 3 = 486`.

Across the ideal family:

- maximum horizontal path-versus-physical-bridge residual remains within `1e-10`;
- maximum commuting-square residual remains within `1e-10`;
- order-covariance violations: `0`.

Thus the Stage 6C partial perspective atlas is compatible with the separately typed vertical conditioning structure throughout the declared canonical family.

## 8. Deliberate mismatch control

The negative control keeps the entire horizontal atlas topology and map content fixed.

Canonical pair/path:

`C0 -> A1 -> B2`.

Only the event correspondence is changed. The deliberately wrong correspondence swaps `e1` and `e2` while still claiming to be orientation-preserving:

- `e0 -> e0`;
- `e1 -> e2`;
- `e2 -> e1`.

The consequences are executable:

- the canonical correspondence still gives commuting squares within tolerance;
- at least one mismatched square residual rises above tolerance;
- the mismatch produces at least one order-covariance violation;
- the horizontal graph remains unchanged and connected;
- the primitive `C0 -> B2` edge remains absent exactly as in Stage 6C.

The failure is therefore caused by incompatible cross-perspective event identification, not by removal of a perspective or by horizontal network disconnection.

## 9. Structural interpretation

Stage 6D supplies the first positive executable compatibility relation between two provisional Stage 6 layers:

- `P`: perspective transport;
- `O`: declared order/succession/conditioning.

In the tested family, these layers can coexist in a commuting structure when they are linked by an explicit, order-compatible event correspondence.

This result should be read as:

`typed horizontal structure + typed vertical structure + compatible chi -> commuting covariance in the declared family`.

It should **not** be read as:

- perspective change is temporal succession;
- clock change is the passage of time;
- the vertical conditioning model is fundamental physics;
- successful covariance proves that `P` and `O` reduce to one structure.

Indeed, the mismatch control shows that explicit `chi` carries nontrivial compatibility information not contained in horizontal connectivity alone.

## 10. Validation

Stage 6D adds **14 focused tests**.

Implementation-inclusive PR merge-ref checkpoint:

`395 passed in 29.42s`.

## 11. Next

Stage 6E — record and modality transport.

The next substage must add the remaining cross-layer transport questions while keeping their semantics separate:

- record orientation under declared orientation-preserving/reversing event correspondence;
- accessibility restrictions in each perspective;
- explicit transport relation for Potentiality/extension sets;
- preservation of the Stage 2 operational-under\-determination result;
- no inference from record transport to phenomenal passage.
