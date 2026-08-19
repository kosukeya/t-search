# Stage 3B — Record Diagnostics Notes

Status: **completed; branch-level full regression passed**.

Stage 3B adds exact measurement machinery to the Stage 3A reversible trajectory ensemble. It does not yet promote a nonzero signed score to a physical temporal arrow.

## Separation from Stage 3A

`src/t_search/stage3.py` remains the reversible-substrate module.

Stage 3B uses a separate module:

- `src/t_search/stage3_diagnostics.py`

This keeps the microscopic dynamics independent from the diagnostics used to inspect them.

## Exact ensemble statistics

All canonical probabilities are inherited from the exact `Fraction`-weighted Stage 3A ensemble. No Monte Carlo sampling, pseudocounts, or smoothing are used.

Stage 3B implements:

- exact marginal distributions of trajectory-derived variables;
- exact joint distributions;
- Shannon entropy;
- mutual information;
- conditional entropy;
- Bayes-optimal decoding accuracy.

## Record profile

At neutral current position `k`, the record profile is:

`Q_R(k,j)=I(R_k;X_j)`.

For the canonical Stage 3 choice:

- `k=1`;
- `R_k=M_1`;
- target variable `X_j`;
- `j in {0,1,2}`.

The profile is unsigned. Mutual information itself does not specify a temporal direction.

## Signed contrasts

The protocol-frozen signed record score is:

`A_R(k,delta)=I(R_k;X_{k-delta})-I(R_k;X_{k+delta})`.

The decoder analogue is:

`A_Acc(k,delta)=Acc(R_k->X_{k-delta})-Acc(R_k->X_{k+delta})`.

At Stage 3B, `k-delta` and `k+delta` are still only the lower-index and upper-index sides of a neutral ordered position. The positive side is not renamed “past”.

## Canonical measurement outputs

For the Stage 3A canonical ensemble, the diagnostics report:

- `H(M_0)=0` bit;
- `H(M_1)=1` bit;
- `I(M_1;X_0)=1` bit;
- `I(M_1;X_2)=0` bit;
- `H(X_0|M_1)=0` bit;
- `H(X_2|M_1)=1` bit;
- `Acc(M_1->X_0)=1`;
- `Acc(M_1->X_2)=1/2`;
- `Q_R(1,j)={0:1,1:1,2:0}` bits;
- `A_R(1,1)=1` bit;
- `A_Acc(1,1)=1/2`.

These are diagnostic facts about the declared ensemble. Stage 3C is responsible for interpreting the nonzero contrast as a candidate record-defined orientation only after the measurement semantics are fixed.

## Single-trajectory guard

A single trajectory can satisfy `M_1 == X_0` numerically while both variables are constant across the one-trajectory ensemble. In that case:

`I(M_1;X_0)=0`.

Therefore accidental value equality is not sufficient to establish a record relation.

## Decoder guard

Bayes-optimal accuracy must be interpreted together with target uncertainty. A constant target can have decoding accuracy `1` even when mutual information is zero. This is why Stage 3 uses both information-theoretic and decoder-based diagnostics rather than treating accuracy alone as a record criterion.

## Entropy guard

The increase from `H(M_0)=0` to `H(M_1)=1` is a subsystem-entropy change inside the already-verified globally reversible model. It must not be described as total entropy production.

## Validation

Stage 3B adds 11 focused tests. The GitHub Actions clean PR merge-ref regression after the Stage 3B implementation/status updates passed:

`120 passed in 2.24s`.

This includes Stage 1, Stage 2, Stage 3A, and Stage 3B tests.

## What Stage 3B does not establish

Stage 3B does not establish:

- that the lower-index side is physically the past;
- a fundamental arrow of time;
- thermodynamic irreversibility;
- causal direction from mutual information alone;
- phenomenal passage.

Stage 3C is the next checkpoint and asks whether the already-defined diagnostics support the narrower phrase **record-defined orientation** for the canonical blank-memory ensemble.
