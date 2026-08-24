# Stage 13F Notes — Basis Equivalence, Ablation, Anomaly, and False Positives

Status: **validated on the frozen finite family; criteria 44–47 satisfied.**

Incoming Stage 13E validated head `5da1f7b07189ac9fd23c756ed432bfc7406caf37`, GitHub Actions run #1801: **`1084 passed in 703.45s (0:11:43)`**.

Stage 13F implementation head: `0abd4681f04df91fab9fbe9de2d811ce26461c57`.

Stage 13F repository-validated branch head: `518a92315575b4b1d75ef51cad5a2dedd9dd40da`, GitHub Actions run #1809: **`1085 passed in 562.97s (0:09:22)`**.

## Why this gate matters

Stage 13A–E used a first-class but noncommuting presentation

`{K_T,K_X}=-K_X`.

That algebraic appearance is not by itself physical evidence for fundamental non-Abelianity because

`K_X_tilde=exp(-T)K_X=p_X+a p`

is an explicitly equivalent presentation with

`{K_T,K_X_tilde}=0`.

Stage 13F therefore tests whether the already established finite physical quotient and O/P/R/V descent survive that presentation change. On the frozen finite carrier they do: the sampled physical quotient and licensed quotient-level operational content are unchanged under the typed basis correspondence. The noncommuting path presentation is therefore Xi-level representation/provenance on this carrier rather than an independently established quotient-level physical distinction.

## Validated positive comparison

The commuting basis uses

`Phi_X_tilde(u): (X,q) -> (X+u,q+a u)`.

Repository-validated finite evidence:

- **36 / 36** representatives satisfy the commuting-basis constraints;
- **144** single-generator arrows = **72 `Phi_T` + 72 `Phi_X_tilde`**;
- exactly **4** connected quotient classes of **9** representatives each;
- **4 / 4** component memberships coincide with the Stage 13D quotient;
- **36 / 36** basis-equivalence checks preserve quotient identity, `(Q_D,P_D)`, complete-relational values, and inherited public O/P/R/V content;
- **144 / 144** mixed pairs close under both `TX` and `XT` using the same raw `s=T1-T0`, `u=X1-X0` in the commuting presentation;
- source diagnostics report criteria 44–47 satisfied, and the full repository regression independently passed at run #1809.

This establishes the bounded equivalence claim only for the declared finite carrier and typed correspondence.

## Validated controls

All **6 / 6** destructive/anomaly controls are rejected as intended:

1. duplicated `K_T` / rank-one pair -> `rank_deficient_constraint_control_rejected`;
2. `K_X_decoupled=p_X`, which fails to preserve `Q_D` -> `decoupled_constraint_control_rejected`;
3. Stage 13B wrong compensator -> `wrong_compensator_detected`;
4. one-clock-incomplete observable -> `one_clock_observable_incomplete`;
5. same-`P_D` / same-`Q_D` cross-orbit false matches -> `cross_orbit_false_positive_rejected`;
6. `K_X_bad=exp(T)(p_X+a p)+0.1q` -> `constraint_algebra_anomaly_detected`.

For the anomaly,

`{K_T,K_X_bad}+K_X_bad=0.1(q-p)`,

so failure is read as a constraint-algebra anomaly, not as an alternative positive physical carrier.

## Bounded result

`Stage 13F basis equivalence, ablation, anomaly, and false-positive controls on the frozen finite family = established`.

The finite result supports the narrower statement that the Stage 13A–E quotient-level physical content is not tied to the original noncommuting presentation on this carrier. It does not show that every admissible constraint presentation is commuting or basis-trivializable, and it does not establish a hypersurface-deformation algebra or refoliation invariance.

## Boundary

`basis presentation != physical orbit`.

`basis-specific Xi provenance != quotient-level physical content`.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-basis change != physical-orbit change`.

`basis-equivalent finite quotient != refoliation invariance`.

`commuting presentation != proof that all admissible presentations commute`.

`multi-constraint path covariance != refoliation invariance`.

`constraint-algebra anomaly != ontological becoming`.

`Dirac-invariant data + relational change != proof of eternalism`.

`complete relational observable != ontological becoming by definition`.

`constraint-algebra/refoliation precursor != general relativity`.

`finite-model success != empirical discovery`.

`repository validation != new scientific evidence`.

Next: **Stage 13G — executable synthesis and evidence-selected next gate**.