# Stage 9B Results — Directional Diagnostics and Controls

Status: **Stage 9B scientific control family implemented; strict current-head validation follows the executable checks below.**

## Question

Can `R_direction` be reversed, symmetrized, or removed on the Stage 9A constrained continuation family without defining away the nontrivial `V_extension` distinction?

## Executable answer

**Yes in the declared finite Stage 9B control family.**

The same h_L/h_R continuation distinction is retained throughout. Direction is measured separately for each continuation and never inferred from continuation weights.

## Control matrix

| control | common directional schedule | `A_R` | `A_acc` | orientation | nontrivial `V_extension` |
| --- | --- | ---: | ---: | --- | --- |
| forward | `(I,U_rec,U_scr U_rec)` | `+1` | `+0.5` | lower-index | retained |
| reversed | `(U_scr U_rec,U_rec,I)` | `-1` | `-0.5` | upper-index | retained |
| balanced | equal forward/reversed history mixture | `0` | `0` | none | retained |
| no-record | `(I,I,U_scr)` | `0` | `0` | none | retained |

For h_R, the independent C-sector continuation action `Z_C` remains on the e2 side of each pure control. Thus h_L/h_R remain physically distinct even when the arrow reverses or vanishes.

## 1. Forward

Both h_L and h_R reproduce the Stage 9A exact directional values:

`A_R=+1`

`A_acc=+0.5`.

No continuation weight is used.

## 2. Reversed

The reversed control does not reverse a Python loop or negate a result after measurement. It reverses the common record/scramble interaction skeleton around the shared e1 record-bearing state.

For h_L:

`(I,U_rec,U_scr U_rec) -> (U_scr U_rec,U_rec,I)`.

For h_R, the same common R-direction reversal is used while the independent future C-sector branch action remains at e2.

Both h_L and h_R give:

`A_R=-1`

`A_acc=-0.5`.

Therefore:

`A_R^rev=-A_R^fwd`

`A_acc^rev=-A_acc^fwd`.

Forward and reversed controls share the declared e1 current Actuality.

## 3. Balanced

Balanced is an equal operational mixture of the forward and reversed constrained histories for each continuation.

It gives:

`A_R=0`

`A_acc=0`.

This is a cancellation of signed direction, not necessarily removal of record content. The two sides can retain equal nonzero information.

`balanced zero R_direction != no R_content`.

Balanced is not assigned an averaged unitary dressing:

`balanced mixture != pure constrained history`.

## 4. No-record

No-record removes `U_rec` while retaining the scrambler and h_L/h_R future distinction.

It gives:

`A_R=0`

`A_acc=0`.

Here the current memory is blank, so this control removes the record-writing channel rather than merely symmetrizing its directional profile.

## 5. V remains nontrivial

For every control, h_L/h_R remain a physically nontrivial continuation pair. For each pure control the e2 schedule operators differ by the same independent C-sector branch action. Balanced inherits this distinction from both pure mixture components.

Thus neither reversal nor zero-direction controls are produced by collapsing `QExt` to a singleton.

## 6. Constrained-carrier validity

Forward, reversed, and no-record are each independently valid constrained multi-clock histories:

- physical dimension = `14`;
- minimum reduction rank over all A/B/C clock readings = `14`;
- schedule unitarity residual within tolerance;
- dressing unitarity residual within tolerance;
- constraint Hermiticity residual within tolerance;
- physical-state constraint residual within tolerance.

Balanced is explicitly typed as a mixture of the two separately valid forward/reversed constrained histories.

## Stage 9B criteria 17–23 assessment

17. Exact target-memory information and decoder-accessibility diagnostics are reused at the declared e1 anchor without continuation weighting — **satisfied**.
18. Forward gives `(A_R,A_acc)=(+1,+0.5)` independently in h_L and h_R — **satisfied**.
19. Modeled common interaction reversal gives `(-1,-0.5)` and exact sign covariance, without using reversed Python iteration — **satisfied**.
20. Equal forward/reversed constrained-history mixture gives zero signed direction while retaining nontrivial V — **satisfied**.
21. Neutralizing the record write gives zero signed direction while retaining the h_L/h_R continuation distinction — **satisfied**.
22. Every pure control retains physical dimension 14, rank-14 A/B/C reductions, and valid constrained-carrier residuals; balanced is a typed mixture of valid pure components — **satisfied**.
23. Direction is controlled without continuation weights or identifying branch class with arrow orientation, while interpretation guards remain explicit — **satisfied**.

## Scientific interpretation

Stage 9A showed coexistence of nontrivial `V_extension` and positive `R_direction` in one constrained family. Stage 9B strengthens this substantially: in the declared finite family, the directional record structure can be reversed, symmetrized, or removed while the h_L/h_R physical continuation distinction remains nontrivial.

This supports **structural compatibility and controllable separation of `R_direction` from `V_extension` in this model**.

It does not establish universal independence between R and V. In particular, Stage 9B does not yet decide the relation of direction to:

- `V_semantics`;
- `V_weights`;
- cross-clock P transport;
- local accessibility changes;
- ontological openness or becoming.

## Guards

- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- `control of R_direction != control of V_semantics`;
- `record content != directional record arrow`;
- `continuation identity != record-direction identity`;
- `balanced mixture != pure constrained history`;
- `reversed diagnostic sign != reversed Python iteration`;
- `Potentiality != quantum randomness by definition`;
- `finite constrained-model success != empirical discovery`.

## Validation history

The first Stage 9B full-suite run (#973) reached **707 passed / 1 failed**. The single failure was only a regex mismatch between the expected and actual `ValueError` wording for balanced-mixture admissibility; all scientific Stage 9B control tests passed.

The message assertion was corrected and the directional tests were tightened to the exact values shown above. A strict full-suite validation is used to close the Stage 9B checkpoint before advancing to Stage 9C.
