# Stage 9A Notes — Common Directional-R/V Continuation Substrate

Status: **completed in the declared finite family; Stage 9B directional controls are next.**

## Purpose

Stage 9A tests the strongest unresolved Stage 8 link at substrate level: can one constrained multi-clock quantum continuation family carry both nontrivial physical continuation multiplicity `V_extension` and a continuation-independent directional record structure `R_direction` at the same declared current anchor?

The construction is intentionally minimal and reuses already-tested Stage 7/8 ingredients rather than introducing an unrelated model.

## Canonical schedule

The common A-clock current anchor remains `e1`.

Both canonical continuations share:

- `V_0 = I`;
- `V_1 = U_rec`.

The e2 completion restores the Stage 7C target scrambler in both branches and then keeps the Stage 8 continuation distinction in the C-sector:

- `h_L: V_2 = U_scr U_rec`;
- `h_R: V_2 = Z_C U_scr U_rec`.

Thus the directional mechanism is common while the continuation identity is carried by the separate future C-sector action.

`continuation identity != record-direction identity`.

## Why this construction is typed correctly

`U_rec` writes the current memory record.

`U_scr` supplies the common upper-side target scrambling needed for the Stage 7C mutual-information contrast.

`Z_C` is the Stage 8 future continuation action. It is identity on the memory subsystem and commutes with the declared B-energy record-target projector. The Stage 9A implementation audits both properties directly.

Therefore the h_L/h_R distinction is not encoded as “positive-arrow branch versus negative-arrow branch”. Both continuations inherit the same arrow channel and differ through a future physical action outside that channel.

## Shared Actuality

The executable diagnostics compare the normalized A-perspective reduced states of h_L and h_R.

They agree through:

- e0 boundary/source;
- e1 current Actuality.

The e2 schedules differ physically.

This preserves the Stage 8 meaning of a common current quantum Actuality with more than one admissible physical continuation.

## Continuation-specific direction

The direction diagnostic is evaluated separately for h_L and h_R before any continuation weights are introduced.

For each continuation, the code computes:

`A_R = I(M_e1 ; X_e0) - I(M_e1 ; X_e2)`

and the matching optimal-decoder accessibility contrast.

The focused Stage 9A tests require and obtain for both h_L and h_R:

- `record_defined = true`;
- orientation `lower-index`;
- `A_R > 0.9`;
- accessibility contrast `> 0.4`;
- equal directional scores across the two canonical continuations to numerical tolerance.

The important result is the sign/coherence and per-continuation provenance, not the bookkeeping label “lower”.

`weighted directional score != continuation-independent directional structure`.

## Physical admissibility

Each canonical continuation is re-derived as its own constrained completion:

`H_h = W_h H_0 W_h^dagger`.

For both h_L and h_R the executable checks establish:

- cumulative schedule unitarity;
- dressing unitarity;
- constraint Hermiticity;
- normalized physical-state constraint residual within tolerance;
- physical dimension `14`;
- minimum A/B/C clock-reduction rank `14` over all nine clock/readout charts.

Stage 9A does not yet test the full continuation-aware cross-clock transport algebra; that remains Stage 9D.

## Physical continuation inequivalence

The two continuations are not mere labels.

The implementation checks the e2 schedule/operator difference and also requires a future-state or coherence-probe distinction. Pure renaming of h_L is identified as equivalent and deduplicates back to two physical continuation classes.

The canonical extension set is therefore:

`QExt(e1) = {h_L,h_R}`.

At terminal e2:

`QExt(e2) = empty`.

A continuation with an incompatible current action is rejected from the canonical extension set.

## What Stage 9A establishes

Within this finite constrained family, Stage 9A supplies an executable positive witness in which:

1. the current Actuality is shared;
2. at least two physically inequivalent admissible future continuations remain;
3. each continuation separately carries the same nonzero directional record orientation;
4. the continuation-defining future action is memory-neutral and record-target-neutral;
5. the constrained multi-clock carrier remains full rank in every tested A/B/C chart.

This closes the substrate-level coexistence problem that was only `partial` at the end of Stage 8.

It does **not** yet decide whether directional R constrains modal semantics or continuation weights, and it does not yet test forward/reversed/balanced/no-record controls inside this new family. Those are Stage 9B/C/E questions.

## Interpretation guards

- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- `QExt represented != ontically real futures by definition`;
- `continuation identity != record-direction identity`;
- `weighted directional score != continuation-independent directional structure`;
- `record content != directional record arrow`;
- `order != directional record arrow`;
- `finite constrained-model success != empirical discovery`.

## Validation

The first Stage 9A implementation run (#933) reached **693 passed** and failed only the two pre-existing brittle Stage 9.0 documentation-string checks. No Stage 9A scientific/focused test failed.

After replacing those exact-string checks with semantic documentation checks, GitHub Actions run #935 passed the complete repository suite:

**`695 passed in 199.79s`**.

## Next

Proceed to **Stage 9B — directional diagnostics and controls**, using this same canonical carrier for forward/reversed/balanced/no-record pressure tests rather than changing the substrate ad hoc.
