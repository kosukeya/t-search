# Stage 13F — Basis / Ablation / Anomaly / False-Positive Controls

Status: **source/test implementation prepared; full repository validation pending.**

Incoming validated checkpoint: Stage 13E source/test head `5da1f7b07189ac9fd23c756ed432bfc7406caf37`, GitHub Actions run #1801, **`1084 passed in 703.45s (0:11:43)`**.

## Frozen evidence matrix

| item | required finite count / condition |
| --- | ---: |
| positive representatives | 36 |
| commuting-basis single-generator arrows | 144 |
| `Phi_T` arrows | 72 |
| `Phi_X_tilde` arrows | 72 |
| commuting-basis quotient classes | 4 |
| representatives per quotient class | 9 |
| Stage 13D representative-set matches | 4 / 4 |
| basis-equivalence public/Dirac/relational checks | 36 |
| commuting mixed-path checks | 144 |
| destructive/anomaly controls | 6 |
| required rejected controls | 6 |

## Positive comparison

The equivalent presentation is

`K_X_tilde=exp(-T)K_X=p_X+a p`

with

`{K_T,K_X_tilde}=0`.

The finite test requires the commuting-basis atlas to reconstruct the same four sampled quotient classes as Stage 13D and the same quotient-level Dirac/complete-relational/O/P/R/V content as Stage 13E.

For mixed pairs the commuting presentation uses the same raw `s=T1-T0` and `u=X1-X0` in `TX` and `XT`; both orders must close on the same target.

## Negative controls

Required rejections:

- rank-deficient duplicate constraint direction;
- decoupled `p_X` direction;
- wrong Stage 13B compensator;
- one-clock-incomplete observable;
- same-single-invariant cross-orbit false match;
- non-first-class `K_X_bad` deformation.

The anomaly diagnostic is

`{K_T,K_X_bad}+K_X_bad=epsilon(q-p)`

with `epsilon=0.1`.

## Bounded claim

The bounded result

`Stage 13F basis equivalence, ablation, anomaly, and false-positive controls on the frozen finite family = established`

is **not yet promoted here**. Promotion requires the current Stage 13F source/test head to pass the full repository regression.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`basis-equivalent finite quotient != refoliation invariance`.

`constraint-algebra anomaly != ontological becoming`.

`constraint-algebra/refoliation precursor != general relativity`.