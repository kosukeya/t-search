# Stage 3G — Robustness and Synthesis Notes

Status: **robustness controls implemented; synthesis/final regression in progress**.

## Purpose

Stage 3G does not add a new temporal model. It stress-tests the structures isolated in Stages 3A--3F, then closes Stage 3 with an explicit synthesis and exit review.

The main questions are:

1. is the record result bookkeeping-dependent;
2. are repeated state values accidentally treated as identical occurrences;
3. what aspect of the memory boundary actually matters;
4. how does the orientation behave away from exactly 50/50 forward/reverse balance;
5. can global preparation uncertainty be distinguished from local readout uncertainty;
6. does the Stage 2 epistemic/ontic distinction survive the Stage 3 product adapter;
7. which Stage 3 claims remain local, reconstructible, ambiguous, lost, or merely candidate physical structure.

## 1. Bookkeeping relabeling

`PositionRenaming` replaces the neutral position names with arbitrary unique symbolic names while leaving the trajectory ensemble and diagnostics unchanged.

Example:

`(0,1,2) -> (alpha,pivot,omega)`.

The canonical record profile remains numerically:

`(1,1,0)` bits

and the selected side is simply translated from `lower-index` to the symbolic label attached to the same structural side.

Therefore the result is covariant under pure position renaming rather than tied to literal strings or integers.

A stronger value-level control also applies the bijection `0 <-> 1` to record and target readouts. Mutual information and Bayes-optimal decoding remain unchanged under these one-to-one value relabelings.

This supports:

`bookkeeping names != physical record content`.

It does not establish a general coordinate-invariant physical observable.

## 2. Repeated values do not define occurrence identity

The canonical all-zero trajectory contains the same complete microstate at all three positions:

`(0,0,0) -> (0,0,0) -> (0,0,0)`.

Stage 3G tags occurrences by position and verifies that all three occurrences remain distinct despite equal state values.

Likewise the exact local `(X,M)` values at positions 0, 1, and 2 can all equal `(0,0)` without collapsing the views into one occurrence.

For this repeated-value case:

- positions 0+1 still leave two compatible complete histories;
- positions 0+1+2 identify the unique all-zero trajectory.

Thus:

`state-value equality != position/event identity`.

This carries the Stage 1 identity guard into the Stage 3 trajectory setting.

## 3. Memory-boundary sweep

Stage 3D compared only the two endpoints:

- canonical `M_0=0`;
- independent uniform `M_0`.

Stage 3G introduces:

`p = P(M_0=0)`

with independent uniform `X_0,N_0` and unchanged reversible maps.

Results:

| `p` | record score `A_R` | accessibility score `A_Acc` | orientation |
|---:|---:|---:|---|
| `1` | `1` | `0.5` | lower-index |
| `3/4` | `1-h_2(1/4) ~= 0.188721875541` | `0.25` | lower-index |
| `1/2` | `0` | `0` | none |
| `1/4` | same as `3/4` | `0.25` | lower-index |
| `0` | `1` | `0.5` | lower-index |

The `p=0` endpoint is especially informative. Here the memory starts deterministically at `1`, so after `U_rec` the register is perfectly anti-correlated with `X_0`. Mutual information and optimal decoding are still maximal.

Therefore the earlier phrase "blank-memory boundary" is too specific as an explanatory summary. The more robust statement is:

**record strength in this construction tracks non-maximal uncertainty / nonuniform preparation of the memory register, not the literal choice of blank value zero.**

At `p=1/2`, the memory boundary is maximally uncertain and independent, and the record contrast vanishes.

This is still a toy-model boundary result, not a derivation of the cosmological Past Hypothesis or thermodynamic arrow.

## 4. Forward/reverse balance sweep

Stage 3D checked only forward, reverse, and exactly symmetric 50/50 mixture.

Stage 3G uses:

`mu_w = w mu_fwd + (1-w) mu_rev`.

Controls at `w=3/4,1/2,1/4` show:

- `w=3/4`: lower-index orientation;
- `w=1/2`: no signed orientation;
- `w=1/4`: upper-index orientation;
- signed record and accessibility scores obey antisymmetry under `w -> 1-w`.

Thus the equal-mixture cancellation is not an isolated special-case implementation artifact. The sign tracks which orientation dominates the mixture and changes continuously through zero at balance.

## 5. Global boundary uncertainty versus local readout noise

A useful degeneracy appears:

- a global memory boundary with `P(M_0=0)=3/4` reduces the **true global** `I(M_1;X_0)` to `~0.188721875541` bit;
- the canonical globally perfect record with a local BSC readout at `epsilon=1/4` leaves **true global** `I(M_1;X_0)=1` bit but reduces **accessible** `I(M_obs;X_0)` to the same `~0.188721875541` bit.

Therefore identical local MI values can arise from different locations of uncertainty.

This supports:

`same accessible statistic != same global information structure`.

It also reinforces the Stage 3F distinction between global representation and local accessibility.

## 6. Stage 2 integration review

The Stage 3E product adapter is rechecked rather than extended.

Two epistemic global models differing only in hidden selected history `h*` produce the same Stage 2 local view at `D_0`. Attaching the same Stage 3 record view therefore produces exactly equal complete local product views.

Thus hidden `h*` still does not leak through the Stage 3 adapter.

For epistemic versus ontic products:

- the Stage 3 record layer is identical;
- modal Actuality and matched next probabilities remain equal in the canonical fixture;
- `EpistemicPotentiality` and `OnticPotentiality` remain distinct types.

This verifies construction-level modularity only. It does not prove that a physical record arrow is independent of fixed/open-future metaphysics, because Stage 2 and Stage 3 remain explicitly separate toy substrates joined by a product interface.

## 7. Canonical model limitation retained

The canonical update has:

`X_1=X_0`.

Therefore current `X_1` is itself a redundant perfect carrier of lower-side information. Record-specific accessibility through `M` and total local accessibility through `(X,M)` are not identical.

Stage 3 synthesis must retain this limitation. A richer later model should separate current state persistence from an explicit memory trace more cleanly.

## 8. Robustness vocabulary

Supported:

- bookkeeping-covariant record diagnostics under the tested renamings;
- occurrence identity preserved despite repeated state values;
- record strength robust to which deterministic memory value is chosen but sensitive to memory-boundary uncertainty;
- orientation sign tracks forward/reverse ensemble balance;
- local statistics alone do not identify whether uncertainty is global or interface-local;
- Stage 2 hidden/absent-future distinction survives the explicit product adapter.

Not supported:

- a fundamental coordinate-free temporal observable;
- a universal Past Hypothesis derivation;
- thermodynamic irreversibility;
- empirical time-reversal violation;
- ontological becoming;
- phenomenal passage.

## Validation checkpoint

The committed Stage 3G robustness suite contains **12 focused tests**.

GitHub Actions clean PR merge-ref at the robustness code/test checkpoint:

`171 passed in 3.28s`.

A final regression will be run again after the synthesis and documentation commits.
