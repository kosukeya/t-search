# Stage 12B Notes — Dirac/Relational Observables and Physical-Orbit Discrimination

Status: **Stage 12B completed; criteria 17–23 satisfied.**

Stage 12B uses the Stage 12A multi-orbit carrier without changing the frozen constraint law or canonical orbit family. Its purpose is to test whether gauge-related representatives agree in the full frozen Dirac pair while physically distinct canonical orbits remain distinguishable, and whether nontrivial relational change survives that representative invariance.

## Independent Dirac reconstruction

For every sampled gauge representative, Stage 12B recomputes rather than trusts stored invariant fields:

`P_D = p`

`Q_D = q - p T`.

The finite carrier supplies **20 representative Dirac estimates**: five representatives for each of four canonical physical orbits. Constraint residuals and disagreement with the Stage 12A stored values are required to remain within `1e-10`.

The same reconstruction is repeated over all Stage 11 positive external representations. The four canonical orbits times identity/affine/cubic/sinh give **16 external Dirac estimates**. Each estimate is reconstructed from every sampled physical event in that representation, so success is not restricted to the Stage 12A seed gauge chart.

## Physical-orbit discrimination

All six unordered pairs among the four canonical physical orbits are compared using the **full** `(Q_D,P_D)` pair. The finite-model classification rule is:

`same Q_D and same P_D => candidate same physical orbit within the frozen family`;

`different Q_D or different P_D => different physical orbit within the frozen family`.

The deliberately difficult controls remain essential:

- `omega_alpha` versus `omega_beta`: same `P_D=1.25`, different `Q_D`; rejected as same orbit;
- `omega_alpha` versus `omega_gamma`: same `Q_D=-0.35`, different `P_D`; rejected as same orbit.

Thus equality of only one invariant is insufficient.

`full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem`.

## Relational observable

Stage 12B evaluates

`q(T=tau)=Q_D+P_D tau`

at

`tau in {-1.25,-0.25,0.75,1.50}`.

It evaluates this from both independently reconstructed representative data and independently reconstructed external-parameterization data, producing **144 relational q(T=tau) evaluations** in total. Every canonical orbit changes nontrivially across the tested `tau` values because every frozen `P_D` is nonzero.

This is the central controlled coexistence test:

`Dirac-invariant orbit data can be constant while relational q(T=tau) changes`.

Neither side is promoted to a metaphysical conclusion.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`relational change != ontological becoming by definition`.

## Relational derivative

The target

`dq/dT=P_D`

is evaluated using physical-clock differences rather than raw external labels.

- All unordered pairs of the five gauge representatives give 10 finite-difference evaluations per orbit, 40 total.
- Every adjacent physical-clock interval in each of the 16 external representations gives 192 more evaluations.

Total: **232 relational derivative evaluations**.

Raw external `lambda` is never used as the denominator for this test.

## Equal-label / equal-single-variable controls

Stage 12B deliberately enumerates cross-orbit coincidences that would generate false identifications under weaker matching rules:

- **30 equal-T cross-orbit matches**;
- **2 equal-q cross-orbit matches**;
- **312 equal-raw-lambda cross-orbit matches** across the four positive external representations.

All are rejected as sufficient physical-orbit identifiers because the full Dirac pair differs. The control classification is `false_positive_rejected`.

These are finite constructive counterexamples to the corresponding matching rules, not universal statements about every constrained system.

## Criteria closed

17. `Q_D,P_D` independently recomputed from sampled representatives — satisfied.
18. Same-orbit representatives agree in both invariants — satisfied.
19. Canonical distinct-orbit controls are not gauge-collapsed — satisfied.
20. `q(T=tau)=Q_D+P_D tau` reconstructed across all canonical orbits — satisfied.
21. `dq/dT=P_D` agrees across representatives and external parameterizations — satisfied.
22. Same-P/different-Q and same-Q/different-P anti-triviality controls pass — satisfied.
23. Equal-label/equal-single-variable false orbit matching is rejected — satisfied.

## Interpretation boundary

Stage 12B establishes a finite diagnostic separation between representative invariance, physical-orbit discrimination, and relational change. It does **not** establish general covariance, diffeomorphism invariance, a hypersurface-deformation algebra, eternalism, or ontological becoming.

`different physical orbit != later event on one orbit`.

`gauge quotient != elimination of physical change`.

`multi-orbit gauge covariance != general covariance`.

Next: **Stage 12C — typed gauge atlas, quotient, and descent of relational structure.**
