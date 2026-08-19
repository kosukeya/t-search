# Stage 3F — Accessibility and Information Controls Notes

Status: **implemented; final GitHub Actions checkpoint result to be recorded after the Stage 3F head completes**.

## Purpose

Stage 3F degrades the **local observation interface** while keeping the global Stage 3 block fixed. The central guard is:

`inaccessible information != ontologically absent information`.

The experiment asks which claims move from locally accessible to degraded, ambiguous, or inaccessible when readout quality and field exposure are reduced.

No microscopic Stage 3 update is changed by the readout channel.

## Observation-channel layer

`src/t_search/stage3_accessibility.py` introduces:

`LocalAccessPolicy(expose_x, expose_m, record_error_probability)`.

The canonical record bit is observed through a binary-symmetric channel:

`M_obs = M` with probability `1-epsilon`

`M_obs = 1-M` with probability `epsilon`.

Stage 3F restricts:

`0 <= epsilon <= 1/2`

because the purpose is monotone degradation rather than an invertibly relabeled channel above one-half error.

The exact local observation ensemble is induced from the unchanged weighted global trajectory ensemble. Probabilities remain rational until information-theoretic logarithms are evaluated.

## Record-specific versus total local accessibility

This distinction is essential in the canonical substrate.

Because the recording map leaves the system bit unchanged:

`X_1=X_0`.

Therefore, if current `X_1` remains exposed, it is already a perfect predictor of `X_0`. Destroying the `M` readout alone does **not** destroy all local access to the lower-side target.

Stage 3F therefore reports separately:

1. **record-readout accessibility** using `M_obs` alone;
2. **full local-interface accessibility** using all exposed local fields `(X_obs,M_obs)`.

This redundancy is a limitation/property of the canonical toy model, not something to hide.

## Exact BSC expectation

For the canonical uniform source and record-only interface:

`M_1=X_0`.

After a BSC with error `epsilon`:

`I(M_obs;X_0)=1-h_2(epsilon)`

where:

`h_2(e)=-e log2(e)-(1-e)log2(1-e)`.

Because `X_2` remains independent of `X_0` in the canonical ensemble:

`I(M_obs;X_2)=0`.

Expected control points:

| `epsilon` | `I(M_obs;X_0)` | `Acc(M_obs->X_0)` | accessible `A_R` | accessible `A_Acc` |
|---:|---:|---:|---:|---:|
| `0` | `1` | `1` | `1` | `0.5` |
| `1/4` | `1-h_2(1/4) ~= 0.188721875541` | `0.75` | same MI value | `0.25` |
| `1/2` | `0` | `0.5` | `0` | `0` |

The **global true-register** value remains:

`I(M_1;X_0)=1 bit`

for all of these access policies because the block itself is not modified.

## Direct hidden-versus-inaccessible control

At `epsilon=1/2` with `X` masked:

- true global register relation: `I(M_1;X_0)=1`;
- accessible noisy readout: `I(M_obs;X_0)=0`.

Thus the same formal global model contains information that the declared local channel cannot access.

This establishes a model-level separation between **represented but inaccessible** information and **information absent from the model**. It is not a metaphysical theorem about physical reality.

## Redundant-current-X control

At `epsilon=1/2` with both `X_1` and noisy `M_obs` exposed:

- record-specific `I(M_obs;X_0)=0`;
- record-specific decoder accuracy is `1/2`;
- full-local `I((X_1,M_obs);X_0)=1`;
- full-local decoder accuracy remains `1`.

An `X`-only interface likewise retains perfect access to `X_0`.

Therefore:

`record access lost != all local access lost`.

This motivates keeping record-specific and total local diagnostics separate in later synthesis.

## History ambiguity under masking/noise

With `X` masked and exact `M` readout, observing:

`M_obs=1`

selects the two histories with `X_0=1`, leaving hidden `N` ambiguous.

With `epsilon=1/4`, the same observed readout has positive likelihood under **all four** canonical histories. The posterior weights are:

- two `X_0=1` histories at `3/8` each;
- two `X_0=0` histories at `1/8` each.

Hence:

`P(X_0=1 | M_obs=1)=3/4`.

The compatible-history class expands:

`2 -> 4`.

This is interface-induced epistemic ambiguity, not ontic branching.

## Visible-X support control

If `X_1` remains exposed, the observed outcome `(X_1,M_obs)=(1,1)` at `epsilon=1/4` is still compatible with only the two `X_0=1` histories. The noisy record bit does not expand the positive-support class because the redundant exact `X` field already constrains it.

## Complete masking endpoint

With both `X` and `M` hidden:

- the only local outcome is `(None,None)`;
- `I(O;X_0)=0`;
- optimal decoding accuracy is prior-level `1/2`;
- all four canonical histories remain compatible.

Again, the four histories and their weights still exist globally.

## Coverage control

The Stage 3E coverage result remains active:

- one exact central `(X,M)` view: two compatible global histories;
- central plus position-2 exact local views: one compatible history.

Thus:

`access quality` and `view coverage` are distinct axes.

A poor readout can increase ambiguity even at fixed coverage; additional positions can restore reconstruction when the exposed variables contain complementary information.

## Interpretation hierarchy

Stage 3F supports only interface-relative statements:

- local record accessibility can degrade continuously while the global record relation remains unchanged;
- maximal readout noise can erase the accessible signed record contrast without changing reversible global dynamics;
- redundant local variables can preserve total accessibility after record-specific accessibility is lost;
- masking and readout noise enlarge compatible-history classes;
- coverage can restore reconstruction independently of record-readout quality in this toy model.

Stage 3F does **not** establish:

- physical destruction of information;
- ontological absence from local inaccessibility;
- thermodynamic entropy production from observation noise;
- a fundamental temporal arrow;
- phenomenal passage.

## Next

Stage 3G should perform the remaining robustness and synthesis work, including bookkeeping relabeling, repeated-value/state controls, useful boundary/noise variants, Stage 2 integration review, full regression, six fixed questions, and `results/stage3_synthesis.md`.
