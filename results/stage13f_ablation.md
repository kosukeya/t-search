# Stage 13F — Basis / Ablation / Anomaly / False-Positive Controls

Status: **repository validated; criteria 44–47 satisfied.**

Incoming validated checkpoint: Stage 13E source/test head `5da1f7b07189ac9fd23c756ed432bfc7406caf37`, GitHub Actions run #1801, **`1084 passed in 703.45s (0:11:43)`**.

Stage 13F implementation head: `0abd4681f04df91fab9fbe2d811ce26461c57`.

Stage 13F repository-validated branch head: `518a92315575b4b1d75ef51cad5a2dedd9dd40da`, GitHub Actions run #1809, **`1085 passed in 562.97s (0:09:22)`**.

## Validated evidence matrix

| item | validated finite count / condition |
| --- | ---: |
| positive representatives | 36 / 36 |
| commuting-basis single-generator arrows | 144 |
| `Phi_T` arrows | 72 |
| `Phi_X_tilde` arrows | 72 |
| commuting-basis quotient classes | 4 |
| representatives per quotient class | 9 |
| Stage 13D representative-set matches | 4 / 4 |
| basis-equivalence public/Dirac/relational checks | 36 / 36 |
| commuting mixed-path checks | 144 / 144 |
| destructive/anomaly controls | 6 |
| required rejected controls | 6 / 6 |

## Positive comparison

The equivalent presentation is

`K_X_tilde=exp(-T)K_X=p_X+a p`

with

`{K_T,K_X_tilde}=0`.

The validated commuting-basis atlas reconstructs exactly the same four sampled quotient classes as Stage 13D, with the same representative memberships and the same quotient-level Dirac/complete-relational/public O/P/R/V content inherited from Stage 13E.

For mixed pairs the commuting presentation uses the same raw `s=T1-T0` and `u=X1-X0` in `TX` and `XT`; all **144 / 144** pairs close on the same licensed target within the frozen tolerance.

Classification:

`basis_presentation_equivalent`.

`equivalent_commuting_path_closure_established`.

## Negative controls

All required controls are rejected:

- rank-deficient duplicate constraint direction -> `rank_deficient_constraint_control_rejected`;
- decoupled `p_X` direction -> `decoupled_constraint_control_rejected`;
- wrong Stage 13B compensator -> `wrong_compensator_detected`;
- one-clock-incomplete observable -> `one_clock_observable_incomplete`;
- same-single-invariant cross-orbit false match -> `cross_orbit_false_positive_rejected`;
- non-first-class `K_X_bad` deformation -> `constraint_algebra_anomaly_detected`.

The anomaly diagnostic is

`{K_T,K_X_bad}+K_X_bad=epsilon(q-p)`

with `epsilon=0.1`.

The deliberately deformed carrier is therefore rejected as anomalous rather than admitted as positive evidence.

## Criteria 44–47 closure

44. Noncommuting and equivalent commuting constraint presentations preserve the same licensed quotient-level physical content under the frozen typed correspondence — **satisfied**.

45. Rank-deficient, decoupled, wrong-compensator, one-clock-incomplete, and cross-orbit false positives are explicitly classified and rejected — **satisfied**.

46. `K_X_bad` is detected as a constraint-algebra anomaly rather than admitted as a positive carrier — **satisfied**.

47. Basis/path/anomaly results remain bounded and are not promoted to fundamental non-Abelianity, refoliation invariance, GR, eternalism, or ontological becoming — **satisfied**.

## Bounded result

`Stage 13F basis equivalence, ablation, anomaly, and false-positive controls on the frozen finite family = established`.

This result means that, on the declared finite toy carrier, the noncommutativity of the original constraint presentation is not itself quotient-level physical content: an explicitly equivalent commuting presentation reconstructs the same sampled physical quotient and licensed operational payloads.

It does **not** establish full refoliation invariance. In particular, this carrier has a simple basis rescaling to a commuting presentation; it does not implement a hypersurface-deformation algebra, phase-space-dependent structure functions of the GR type, or gravitational field degrees of freedom.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-basis change != physical-orbit change`.

`basis-equivalent finite quotient != refoliation invariance`.

`commuting presentation != proof that all admissible presentations commute`.

`multi-constraint path covariance != refoliation invariance`.

`constraint-algebra anomaly != ontological becoming`.

`constraint-algebra/refoliation precursor != general relativity`.

`Dirac-invariant data + relational change != proof of eternalism`.

`complete relational observable != ontological becoming by definition`.

`finite-model success != empirical discovery`.

`repository validation != new scientific evidence`.

Next: **Stage 13G — executable synthesis and evidence-selected next gate**.