# Stage 6C Notes — Partial Perspective Atlas

Status: **completed**.

Stage 6C removes the Stage 5 convenience assumption that every requested clock-perspective map is available as a primitive direct edge. It represents the Stage 5 support-space perspective maps as a sparse directed atlas and tests reconstruction, alternate-path consistency, loop consistency, absence semantics, and deliberate inconsistency detection.

The implementation lives in:

`src/t_search/stage6_partial_atlas.py`.

The machine-readable diagnostic entry point is:

`python experiments/stage6c_partial_atlas.py`.

## 1. Atlas object

A perspective node is a physical clock choice together with one declared clock reading:

`p=(clock,index)`.

A primitive horizontal atlas edge is a Stage 5 support-coordinate clock-change map:

`M_{q<-p}: K_p -> K_q`.

`PartialPerspectiveAtlas` stores only explicitly declared nodes and direct edges. It distinguishes:

- `has_perspective(q)`;
- `has_direct_map(p,q)`;
- a missing primitive edge between two existing nodes;
- an unknown/nonexistent target node in the declared atlas.

The frozen Stage 6 distinction is therefore executable:

`direct edge absent != target perspective absent`.

## 2. Canonical sparse atlas

The decisive canonical case uses:

- source: `C0`;
- target: `B2`;
- intermediate perspectives: `A0`, `A1`, `A2`.

The primitive `C0 -> B2` edge is deliberately omitted.

The atlas retains:

- `C0 -> A0 -> B2`;
- `C0 -> A1 -> B2`;
- `C0 -> A2 -> B2`;
- one return edge `B2 -> C0` for loop diagnostics.

Thus the declared graph has five perspectives and seven primitive directed edges. The target `B2` exists even though the direct `C0 -> B2` edge does not.

## 3. Indirect reconstruction

For each of the three available two-hop paths, Stage 6C composes the declared edges:

`M_{B2<-Ak} M_{Ak<-C0}`.

The result is compared with the Stage 5 primitive `C0 -> B2` support map as an **external reference only**. That reference is not inserted into the sparse atlas.

All three indirect maps agree with the external direct reference within the frozen Stage 5 tolerance:

`1e-10`.

Therefore this family demonstrates:

`primitive direct edge absent + connected compatible path -> indirect map reconstructible`.

This is a statement about the declared ideal support-space atlas, not a claim that every physical perspective transformation is globally reconstructible.

## 4. Alternate-path consistency

The three distinct paths differ in the intermediate A-clock reading.

Stage 6C compares every pair of induced source-to-target maps. Their pairwise residuals remain below the declared tolerance.

This executablely preserves the Stage 5 result that the intermediate clock reading cancels from the final cross-clock map, now interpreted as an overlap/path-consistency property of a partial atlas rather than as availability of a complete primitive map table.

## 5. Loop consistency

Each reconstruction path is closed using the retained `B2 -> C0` return edge:

`C0 -> Ak -> B2 -> C0`.

For a loop map `M_loop`, Stage 6C evaluates:

`H_loop = ||M_loop - I||`.

All three canonical loop residuals remain below `1e-10` on the declared source support.

This is algebraic path consistency only.

Frozen guard:

`algebraic loop residual != gravitational/physical holonomy unless independently derived`.

## 6. Exhaustive partial-atlas family scan

Stage 6C repeats the sparse-atlas construction for every:

- ordered pair of distinct physical clocks: `6` choices;
- source reading: `3` choices;
- target reading: `3` choices.

This produces exactly:

- `54` endpoint cases with a deliberately missing primitive source-to-target edge;
- `54` present target perspectives;
- `162` available two-hop reconstruction paths;
- `162` corresponding closed loops.

Across the entire canonical qutrit family:

- every intended direct endpoint edge is absent from the declared atlas;
- every target perspective remains present;
- every indirect map agrees with the external Stage 5 direct reference within `1e-10`;
- alternate indirect paths agree within `1e-10`;
- all declared loop residuals remain within `1e-10`.

Thus the Stage 5 `162` three-clock routes survive after direct endpoint edges are removed as primitives.

## 7. Deliberate edge-perturbation control

The canonical atlas is copied and only one declared edge is perturbed:

`C0 -> A1`.

The `(0,0)` support-matrix entry is shifted by:

`epsilon = 1e-4`.

The graph topology is unchanged. `B2` still exists, the direct `C0 -> B2` edge remains absent, and all three indirect paths remain topologically available.

Nevertheless the diagnostics detect the corrupted edge:

- maximum indirect-versus-reference residual rises far above tolerance;
- pairwise path inconsistency rises far above tolerance;
- the loop using `A1` acquires a nonzero residual far above tolerance.

The routes through `A0` and `A2`, which do not use the perturbed edge, remain consistent within tolerance.

This is the Stage 6C negative control required to show that the path/loop tests are sensitive to map content rather than merely to graph connectivity.

## 8. Protocol checklist

The six frozen Stage 6C requirements are satisfied:

1. **remove direct edges while retaining connected paths** — the source-to-target primitive edge is omitted in all 54 endpoint cases;
2. **reconstruct an indirect map by composition** — all 162 two-hop maps are composed from retained edges;
3. **compare distinct paths** — three intermediate-reading paths are compared for every endpoint case;
4. **verify loop consistency** — all 162 reconstruction paths are closed with a declared return edge;
5. **separate absent direct map from absent target** — the API raises different conditions for these two cases;
6. **perturb one edge and detect failure** — the single-edge perturbation produces localized path/loop inconsistency.

## 9. Interpretation

Stage 6C strengthens the perspective-layer `P` result in a specific way:

> a consistent perspective atlas need not be represented by a complete set of primitive pairwise arrows; in the tested ideal clock family, missing direct arrows can be reconstructed from compatible local/overlap paths, and path/loop residuals provide executable consistency diagnostics.

This does not imply that the perspective layer is the whole of time. Stage 6B already kept perspective consistency distinct from temporal succession, record direction, and modal semantics.

It also does not show physical spacetime curvature, physical holonomy, gauge curvature, or a fundamental sheaf/groupoid ontology. Those would require additional physical derivation.

## 10. Validation

Stage 6C adds **11 focused tests**.

The PR merge-ref GitHub Actions checkpoint after the Stage 6C implementation, focused tests, and experiment entry point is:

`381 passed in 21.58s`.

## 11. Next

Stage 6D — horizontal/vertical compatibility.

The next pressure test must put both typed arrow families into one executable model:

- horizontal perspective maps `M_{q<-p}`;
- vertical temporal/order/conditioning maps `D_p`;
- explicit event correspondence `chi`;
- commuting-square/order-covariance diagnostics;
- a deliberate mismatch control.

Stage 6D must preserve the guard:

`perspective-change arrow != temporal-succession arrow`.
