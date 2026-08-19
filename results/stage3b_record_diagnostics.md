# Stage 3B — Record Diagnostics

Status: **completed; GitHub Actions full regression passed**.

## Purpose

Stage 3B adds exact information-theoretic and decoder-based diagnostics to the reversible Stage 3A substrate. It defines how to measure a record relation and a signed side-to-side contrast without yet declaring either side to be physically past or future.

## Implemented diagnostics

The new module `src/t_search/stage3_diagnostics.py` provides:

- trajectory-derived exact marginal distributions;
- exact joint distributions;
- Shannon entropy;
- mutual information;
- conditional entropy;
- Bayes-optimal decoding accuracy;
- record profile `Q_R(k,j)`;
- accessibility profile;
- signed record score `A_R(k,delta)`;
- signed accessibility score `A_Acc(k,delta)`.

The Stage 3A dynamics module remains separate from these diagnostics.

## Canonical exact measurements

Using the exact Stage 3A canonical ensemble:

`X_0=a`

`M_0=0`

`N_0=b`

with independent uniform bits `a,b`, the Stage 3B machinery gives the following canonical values.

### Subsystem entropies

`H(M_0)=0 bit`

`H(M_1)=1 bit`

`H(X_0)=1 bit`

`H(X_2)=1 bit`.

The change in memory-register entropy occurs inside the Stage 3A model whose full-state entropy is already verified to remain `2 bits` at every position. Therefore this is subsystem entropy redistribution, not total entropy production.

### Mutual information

`I(M_1;X_0)=1 bit`

`I(M_1;X_2)=0 bit`.

The current record register therefore has different statistical dependence on the two neutral comparison positions under the declared ensemble.

At Stage 3B this is reported only as an information contrast. No side is yet renamed “past”.

### Conditional entropy

`H(X_0|M_1)=0 bit`

`H(X_2|M_1)=1 bit`.

Thus `M_1` removes all uncertainty about `X_0` in the canonical ensemble while leaving the one-bit uncertainty of `X_2` unchanged.

### Bayes-optimal accessibility

`Acc(M_1->X_0)=1`

`Acc(M_1->X_2)=1/2`.

This supplies an operational decoder-based check in addition to mutual information.

## Record and accessibility profiles

At neutral current position `k=1`, using `M_1` as the accessible register and `X_j` as target:

`Q_R(1,j)={0:1,1:1,2:0}` bits.

The corresponding Bayes-optimal accessibility profile is:

`Acc(1,j)={0:1,1:1,2:1/2}`.

These profiles are indexed by neutral ordered positions only.

## Signed diagnostic outputs

With `delta=1`:

`A_R(1,1)=I(M_1;X_0)-I(M_1;X_2)=1 bit`.

`A_Acc(1,1)=Acc(M_1->X_0)-Acc(M_1->X_2)=1/2`.

These positive values are **signed neutral-side contrasts under the protocol’s orientation convention**. Stage 3B does not yet make the stronger interpretive move of calling this a temporal arrow. Stage 3C evaluates whether the narrower phrase **record-defined orientation** is justified for the blank-memory ensemble.

## Important guards

### Accidental equality is not a record

A one-trajectory ensemble can have `M_1 == X_0` while both variables are constant. In that case:

`I(M_1;X_0)=0`.

Therefore a single matching value is insufficient; the record criterion is ensemble-level statistical dependence.

### Decoder accuracy alone is insufficient

A constant target can be decoded with accuracy `1` while carrying zero mutual information. Decoder accuracy is therefore interpreted alongside entropy and mutual information.

### Correlation is not causation

Mutual information is symmetric and does not identify a causal arrow. Causal/provenance structure in the canonical toy model is separately known from the explicitly declared microscopic maps.

### Subsystem entropy is not global entropy production

`H(M_0)=0 -> H(M_1)=1` does not contradict the Stage 3A result:

`H(Z_0)=H(Z_1)=H(Z_2)=2 bits`.

## Validation

The committed Stage 3B test file contains **11 focused tests** covering:

1. exact canonical component marginals;
2. exact marginal/joint helper normalization;
3. subsystem entropy measurements;
4. mutual information for perfect dependence and independence;
5. conditional entropy;
6. Bayes-optimal decoder accuracy;
7. record profile;
8. accessibility profile;
9. signed score definitions;
10. the single-trajectory accidental-equality guard;
11. invalid position/component/window rejection.

GitHub Actions clean PR merge-ref regression:

`120 passed in 2.24s`.

This includes Stage 1, Stage 2, Stage 3A, and Stage 3B tests.

## Strongest justified Stage 3B conclusion

**The reversible Stage 3 substrate now has exact, independently testable information-theoretic and decoder-based machinery for quantifying record accessibility and signed side-to-side contrasts without defining the lower-index side as the past.**

Stage 3B does not establish a fundamental temporal arrow, thermodynamic irreversibility, causal direction from MI alone, or phenomenal passage.
