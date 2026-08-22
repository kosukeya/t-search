# Stage 9A Results — Common Directional-R/V Continuation Substrate

Status: **Stage 9A scientific implementation complete; Stage 9B directional diagnostics and controls are next.**

## Question

Can one constrained quantum continuation family retain nontrivial physical `QExt` at a shared current Actuality while every canonical continuation separately carries the same nonzero directional record structure?

## Executable answer

**Yes in the declared finite Stage 9A family.**

The canonical extension set is:

`QExt(e1) = {h_L,h_R}`

with common prefix:

- `V_0 = I`;
- `V_1 = U_rec`.

The future completions are:

- `h_L: V_2 = U_scr U_rec`;
- `h_R: V_2 = Z_C U_scr U_rec`.

The common `U_scr` restores the Stage 7C target-scrambling mechanism in both continuations. The continuation difference remains the Stage 8 C-sector phase action.

## Shared current Actuality

The normalized A-perspective e0 and e1 states agree across h_L/h_R to the declared numerical tolerance. The e2 schedules are physically distinct.

Thus Stage 9A retains a single declared current Actuality through e1 while leaving two admissible physical future completions.

## Per-continuation directional witness

Direction is evaluated before any modal weights are supplied.

For each canonical continuation:

`A_R(h,e1) = I(M_e1;X_e0) - I(M_e1;X_e2)`

and the matching decoder-accessibility contrast are nonzero and select the same neutral side.

The focused tests establish for **both** h_L and h_R:

- `record_defined = true`;
- orientation = `lower-index`;
- `A_R > 0.9`;
- accessibility contrast `> 0.4`;
- h_L/h_R directional scores agree within numerical tolerance.

Therefore the directional sign is not manufactured by weighting opposite-arrow branches.

`weighted directional score != continuation-independent directional structure`.

## Branch/arrow separation

The continuation-defining branch action is audited separately from the record channel.

For both canonical branch actions:

- memory neutrality = `true`;
- declared record-target neutrality = `true`.

At the same time the two future completions remain physically inequivalent through their e2 operator/state/coherence structure.

Therefore the positive Stage 9A witness satisfies:

`continuation identity != record-direction identity`.

## Constrained-carrier validity

For both h_L and h_R:

- physical dimension = `14`;
- minimum reduction rank across all A/B/C clock indices = `14`;
- schedule unitarity residual is within tolerance;
- dressing unitarity residual is within tolerance;
- constraint Hermiticity residual is within tolerance;
- physical-state constraint residual is within tolerance.

This is a substrate-validity result. Full continuation-aware frame transport, composition, and corresponding-observable covariance remain Stage 9D work.

## Controls already present at substrate level

Stage 9A also verifies:

- a pure rename of h_L does not create a third physical continuation;
- h_L and h_R are not equivalent;
- a current-incompatible continuation is rejected;
- `QExt(e2)=empty` at the terminal anchor.

The forward/reversed/balanced/no-record **directional** controls are deliberately not claimed here; they are allocated to Stage 9B.

## Stage 9A criteria 11–16 assessment

11. Nontrivial physically inequivalent canonical `QExt(e1)` with two continuations — **satisfied**.
12. h_L/h_R share the declared current Actuality through e1 — **satisfied**.
13. Every canonical continuation separately carries the same nonzero directional-record orientation before weighting — **satisfied**.
14. Continuation identity is physically separated from the memory/record-target direction channel — **satisfied**.
15. Both constrained completions retain dimension 14 and rank-14 A/B/C reductions with numerical residuals within tolerance — **satisfied**.
16. Mere-label, invalid-current, and terminal-extension controls behave as declared without promoting the result to ontological openness/becoming — **satisfied**.

## Scientific interpretation

Stage 8 ended with `full P/O/directional-R/V = partial` because its canonical V carrier had current record content but zero directional record score.

Stage 9A removes that specific substrate-level separation: **nontrivial physical continuation multiplicity and coherent directional record structure now coexist in one constrained continuation family at one shared current anchor.**

This is evidence that directional R and nontrivial V are not structurally incompatible in this finite family.

It is not evidence that:

- the physical future is ontically open;
- an actualization process is ontological becoming;
- record direction determines selected-vs-unselected modal semantics;
- record direction fixes continuation weights;
- record direction is the thermodynamic arrow or phenomenal passage;
- finite multi-clock compatibility is general covariance.

## Validation

Initial Stage 9A run #933: **693 passed / 2 failed**; both failures were pre-existing exact-string documentation checks introduced at Stage 9.0. All Stage 9A scientific/focused tests passed.

After correcting those checks to test semantics rather than exact prose, run #935 passed:

**`695 passed in 199.79s`**.

A documentation-synchronized current-head regression is run after recording this Stage 9A checkpoint; it validates branch/documentation consistency rather than adding a new Stage 9A scientific claim.

## Next

**Stage 9B — directional diagnostics and controls**: construct forward/reversed/balanced/no-record variants on this same carrier and verify the expected sign reversal/cancellation/removal without sacrificing nontrivial V by definition.
