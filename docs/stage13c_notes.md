# Stage 13C Notes — Dirac / Two-Clock Complete Relational Observables and Physical-Orbit Discrimination

Status: **implementation complete; criteria 24–31 close only after the Stage 13C executable/test family passes repository CI.**

Incoming Stage 13B documentation-synchronized checkpoint: head `d559c031590a058962c50d170b144acbe8eabadd`, GitHub Actions run #1726, **`1059 passed in 538.54s (0:08:58)`**.

## Question

Stage 13C asks whether the two-constraint carrier preserves representative-independent physical initial data and nontrivial relational change after Stage 13B has established compensated path closure.

The executable questions are deliberately separated:

1. reconstruct `Q_D=q-pT-0.5X` and `P_D=p` independently from all 36 raw representatives;
2. test same-orbit agreement and all six different-orbit pairs under the full Dirac pair;
3. evaluate the two-clock complete observable `q(T=tau,X=chi)` over the declared 3x3 clock grid;
4. compare complete-relational values across the two compensated Stage 13B path orders;
5. show explicitly that fixing only `T=tau` leaves `X` gauge dependence;
6. retain same-P/different-Q and same-Q/different-P anti-triviality controls;
7. keep relational change separate from eternalism and ontological becoming claims.

Stage 13C does **not** yet construct the typed multi-constraint quotient/path-word atlas. That remains Stage 13D.

## Independent Dirac reconstruction

For every representative, the executable code uses raw phase-space values rather than the stored declared orbit pair:

`Q_D_reconstructed = q - p T - 0.5 X`,

`P_D_reconstructed = p`.

The declared values are used only afterward as a diagnostic comparison.

The expected deterministic finite-family maxima are

- `max |Q_D_reconstructed-Q_D_declared| <= 2.220446049250313e-16`;
- `max |P_D_reconstructed-P_D_declared| = 0.0`;
- maximum same-orbit `Q_D` spread `<= 2.220446049250313e-16`;
- maximum same-orbit `P_D` spread `= 0.0`.

The analytic-gradient Poisson checks verify

`{Q_D,K_T}=0`, `{Q_D,K_X}=0`,

`{P_D,K_T}=0`, `{P_D,K_X}=0`

on all 36 positive representatives.

`Dirac invariant != timeless ontology by definition`.

## Physical-orbit discrimination

The four retained orbit summaries produce exactly **6** unordered distinct-orbit comparisons.

All six must remain distinct under the full `(Q_D,P_D)` pair. The minimum finite-family full-pair separation is **0.5**.

The explicit anti-triviality controls remain:

- `omega_alpha` vs `omega_beta`: same `P_D=1.25`, different `Q_D`;
- `omega_alpha` vs `omega_gamma`: same `Q_D=-0.35`, different `P_D`.

Therefore neither `Q_D` alone nor `P_D` alone is licensed as a universal physical-orbit identifier on this family.

`full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem`.

## Two-clock complete relational family

The Stage 13A representative grid itself is reused as the finite target clock grid:

`tau,chi in {-1,0,1}`.

For each of 4 physical orbits, 9 source representatives independently reconstruct `(Q_D,P_D)` and evaluate all 9 target clock pairs. This yields

**4 x 9 x 9 = 324 complete-relational evaluations**.

The observable is

`q(T=tau,X=chi)=Q_D+P_D tau+0.5chi`.

Each result is compared with the canonical representative at the corresponding `(tau,chi)` within the same physical orbit. The deterministic maximum target residual is approximately **2.220446049250313e-16**.

For each orbit and target clock pair, the 9 source representatives therefore descend to one common complete-relational value within tolerance.

The 9 target clock pairs also produce more than one value on every physical orbit, so relational change remains nontrivial after representative redundancy is removed.

`gauge quotient != elimination of physical change`.

`complete relational observable != ontological becoming by definition`.

## Compensated path-choice relational covariance

Stage 13B supplies **144** compensated mixed path comparisons. Stage 13C reconstructs Dirac data independently from both compensated endpoints and evaluates all 9 target clock pairs for each comparison:

**144 x 9 = 1296 compensated-path complete-relational comparisons**.

For every comparison the executable test requires

- `q_TX ~= q_XT`;
- `q_TX ~= q_target`;
- `q_XT ~= q_target`.

The expected deterministic maximum residual is approximately **2.220446049250313e-16**.

Classification:

`compensated_path_complete_relational_covariance_established`.

This is a finite path-choice covariance statement only.

`compensated-path relational covariance != refoliation invariance`.

## One-clock incompleteness control

To test the frozen negative control, Stage 13C fixes `T=tau` while leaving `X_raw` variable:

`q(T=tau;X raw)=Q_D+P_D tau+0.5X_raw`.

For 4 orbits and 3 values of `tau`, the code forms **12 one-clock groups**. Each group contains the 3 values `X_raw in {-1,0,1}`, giving **36 one-clock evaluations** total.

All 12 groups have nonzero spread; the deterministic spread is approximately **1.0** throughout the family.

Classification:

`one_clock_observable_incomplete`.

Thus one clock condition does not remove the second gauge direction on this model.

`one clock condition in a two-gauge-direction model != complete relational observable`.

## Metaphysical boundary

Every Stage 13C Dirac, complete-relational, compensated-path, and one-clock record carries

`metaphysical_claim_status = not_licensed`.

The executable finite model may establish representative-independent relational change while remaining silent on whether actuality is globally block-like, locally becoming-like, or neither in an ontological sense.

- `Dirac-invariant data + relational change != proof of eternalism`;
- `complete relational change != ontological becoming by definition`;
- `path-independent complete-relational values != future actuality`;
- `finite-model success != empirical discovery`.

## Stage boundary

A successful Stage 13C establishes only the bounded Dirac / complete-relational layer. It does not yet establish

- a typed multi-constraint atlas built from `Phi_T/Phi_X` connectivity;
- quotient recovery of exactly four 9-representative classes;
- path-word / compensator descent at quotient level;
- O/P/R/V/Xi future-measurement descent;
- constraint-basis presentation equivalence;
- refoliation invariance;
- a hypersurface-deformation algebra;
- general relativity.
