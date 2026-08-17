# Stage 1B B4 Protocol — Reachability-only Views

Status: **implementation protocol for B4**.

## 1. Purpose

B4 restores complete view coverage and shared global event IDs. The manipulated information is now the distinction between direct adjacency and transitive order.

Start from:

`B_1 = (E, C)`

and define the non-reflexive reachability relation:

`prec = TC(C)`.

The B4 projection discards the one-hop/direct-edge distinction and retains only which events lie before or after each event in the reachability order.

The central question is:

> If only `prec` is retained, when can the original direct/cover relation `C` be recovered?

## 2. Reachability-only local view

For each event `e`, define:

`R_e = (id_e, Anc(e), Desc(e))`

where:

`Anc(e) = {x in E | x prec e}`

`Desc(e) = {y in E | e prec y}`.

B4 retains:

- one view for every event;
- shared global event IDs;
- the complete ancestor set;
- the complete descendant set.

B4 removes:

- immediate predecessor/successor information;
- direct-versus-transitive path-length information;
- any indication that a reachable pair was connected by an explicit shortcut edge in the original encoding.

## 3. Consistency conditions

The family `{R_e}` is valid only if:

1. every referenced ID is also a view owner;
2. no event is its own ancestor or descendant;
3. ancestor and descendant reports are dual:
   `x in Anc(e)` iff `e in Desc(x)`;
4. the induced relation is acyclic;
5. the induced relation is transitive.

If any condition fails, reconstruction must reject the view family instead of silently repairing it.

## 4. Reconstructing the order

From descendant reports:

`prec_hat = {(e,y) | y in Desc(e)}`.

Ancestor reports independently induce the same relation when the views are consistent.

The primary B4 preservation test is therefore:

`prec_hat = prec`.

## 5. Reconstructing a cover relation

Given a finite DAG representing the full transitive relation `prec_hat`, compute its transitive reduction:

`C_cover_hat = TR(prec_hat)`.

For a finite DAG, the transitive reduction is unique and has the same reachability relation.

Exact recovery of the original `C` requires an additional assumption:

> the original `C` is itself the cover/minimal generating relation (equivalently, already transitively reduced).

Under this assumption:

`TR(TC(C)) = C`.

The canonical Stage 1 graph satisfies this condition and is the primary positive case.

## 6. Redundant-edge control

B4 must also test a block whose direct-edge encoding contains a transitive shortcut, for example the canonical graph plus:

`a -> d`.

Because `a` already reaches `d` through `a -> b -> d` and `a -> c -> d`, adding the shortcut does not change `prec`.

Therefore the canonical block and the redundant-edge block have identical reachability-only views.

Transitive reduction should remove the shortcut and return the same minimal cover relation for both.

This control distinguishes two claims:

1. **reachability/partial order is reconstructible from reachability-only views**;
2. **an arbitrary original direct-edge encoding is reconstructible**.

B4 expects the first to hold and the second to fail when redundant shortcut edges are allowed.

## 7. Required diagnostics

For the canonical positive case record:

- events represented: 6;
- reachability pairs supplied: expected 13;
- reachability consistency: pass/fail;
- reconstructed cover-edge count;
- labeled equality against canonical `C`;
- unlabeled isomorphism;
- reachability equality.

For the redundant-edge control record:

- whether its reachability-only views equal the canonical views;
- whether the shortcut survives transitive reduction;
- direct-edge equality against the redundant original;
- reachability equality against the redundant original.

## 8. Property classification

### Local observable

In one `R_e`:

- event ID;
- all ancestors of `e`;
- all descendants of `e`.

### Reconstructible

From the complete consistent family:

- event set `E`;
- full reachability relation `prec`;
- unique cover relation `TR(prec)` for a finite DAG.

### Lost / not identifiable from B4 data

Without the cover/minimality assumption:

- whether the original encoding contained a transitive shortcut edge;
- the exact arbitrary generating edge set used before taking transitive closure.

### Strict invariant

No strict invariant is claimed merely from B4. The result is still a labeled reconstruction under complete coverage.

## 9. Interpretation rule

If canonical `C` is recovered, record only:

> For this finite DAG, once `C` is restricted to the cover/minimal relation, the reachability order contains enough information to reconstruct it by transitive reduction.

Do **not** infer from this alone that physical time is fundamentally a partial order.

The redundant-edge control is required precisely to show which part of the result depends on the chosen representation convention.

## 10. Next step

After B4, proceed to B5 — state-label collision — while restoring the ordinary direct-edge local representation. B5 asks whether distinct event identities remain separate when they share the same state value.
