# Stage 13F Notes — Basis Equivalence, Ablation, Anomaly, and False Positives

Status: **implementation prepared against the validated Stage 13E checkpoint; full repository validation pending.**

Incoming Stage 13E validated head `5da1f7b07189ac9fd23c756ed432bfc7406caf37`, GitHub Actions run #1801: **`1084 passed in 703.45s (0:11:43)`**.

## Why this gate matters

Stage 13A–E used a first-class but noncommuting presentation

`{K_T,K_X}=-K_X`.

That algebraic appearance is not by itself physical evidence for fundamental non-Abelianity because

`K_X_tilde=exp(-T)K_X=p_X+a p`

is an explicitly equivalent presentation with

`{K_T,K_X_tilde}=0`.

Stage 13F therefore tests whether the already established finite physical quotient and O/P/R/V descent survive that presentation change. If they do, the noncommuting path word belongs to Xi-level representation/provenance rather than to the quotient-level physical content on this finite carrier.

## Positive executable comparison

The commuting basis uses

`Phi_X_tilde(u): (X,q) -> (X+u,q+a u)`.

Expected finite evidence:

- 36 representatives satisfy both commuting-basis constraints;
- 144 single-generator arrows = 72 `Phi_T` + 72 `Phi_X_tilde`;
- 4 connected components of 9 representatives;
- 4/4 component memberships coincide with Stage 13D;
- 36 basis-equivalence checks preserve quotient id, `(Q_D,P_D)`, complete-relational values, and inherited public O/P/R/V;
- 144 mixed pairs close under both `TX` and `XT` using the same raw `s=T1-T0`, `u=X1-X0`.

## Controls

Six controls are deliberately kept logically separate:

1. duplicated `K_T` / rank-one pair;
2. `K_X_decoupled=p_X`, which fails to preserve `Q_D`;
3. Stage 13B wrong compensator;
4. one-clock-incomplete observable;
5. same-`P_D` / same-`Q_D` cross-orbit false matches;
6. `K_X_bad=exp(T)(p_X+a p)+0.1q`.

For the anomaly,

`{K_T,K_X_bad}+K_X_bad=0.1(q-p)`,

so failure is read as a constraint-algebra anomaly, not as an alternative positive physical carrier.

## Boundary

`basis presentation != physical orbit`.

`basis-specific Xi provenance != quotient-level physical content`.

`basis-equivalent finite quotient != refoliation invariance`.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`constraint-algebra anomaly != ontological becoming`.

`Dirac-invariant data + relational change != proof of eternalism`.

`constraint-algebra/refoliation precursor != general relativity`.