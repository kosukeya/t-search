# Stage 13F Protocol — Basis / Ablation / Anomaly / False-Positive Controls

Status: **frozen from the validated Stage 13E checkpoint; executable source/test validation pending.**

Incoming validated Stage 13E checkpoint:

- branch: `agent/stage-13-multi-constraint-refoliation-precursor`;
- head: `5da1f7b07189ac9fd23c756ed432bfc7406caf37`;
- GitHub Actions run #1801: **`1084 passed in 703.45s (0:11:43)`**;
- Stage 13 criteria **1–43** are treated as the incoming validated evidence boundary for this gate.

## 1. Question

Stage 13F asks whether the Stage 13A–E positive result is robust to an **equivalent change of constraint presentation**, while deliberately invalid carriers and false correspondences remain rejected.

The central distinction is:

`constraint presentation != quotient-level physical content`.

Stage 13F does not attempt to establish refoliation invariance. It tests a finite precursor question: whether one noncommuting first-class presentation and one explicitly equivalent commuting presentation recover the same sampled physical quotient and the same inherited quotient-level O/P/R/V operational content when the typed correspondence is correct.

## 2. Frozen positive basis comparison

The Stage 13A positive presentation remains

`K_T = p_T + p^2/2`

and

`K_X = exp(T)(p_X + a p)`

with `a = 0.5` and `{K_T,K_X} = -K_X`.

Stage 13F compares it with the equivalent rescaled presentation

`K_X_tilde = exp(-T) K_X = p_X + a p`

for which

`{K_T,K_X_tilde}=0`.

The corresponding frozen finite flow is

`Phi_X_tilde(u): X -> X+u, q -> q+a u`

with all other canonical coordinates unchanged.

For a mixed same-orbit source/target pair the commuting presentation uses

`s = T1-T0`

and

`u = X1-X0`

in both `TX` and `XT` orderings. Unlike the original `K_X` presentation, no order-dependent compensator is needed because the two frozen finite generators commute in this equivalent presentation.

Positive requirements:

1. all 36 canonical representatives satisfy `K_T=K_X_tilde=0`;
2. `{K_T,K_X_tilde}=0` on the frozen family;
3. the commuting-basis sampled atlas contains 72 `Phi_T` and 72 `Phi_X_tilde` arrows;
4. connectivity recovers exactly four classes of nine representatives;
5. those four representative sets match the Stage 13D quotient classes;
6. all 36 representative-to-quotient basis checks preserve the full `(Q_D,P_D)` pair, complete-relational values, and inherited quotient-level public O/P/R/V payload;
7. all 144 mixed pairs close in both commuting path orders with the same raw `(s,u)`.

Classification:

`basis_presentation_equivalent`.

## 3. Frozen destructive controls

Stage 13F requires all of the following to be rejected.

### F1 — rank-deficient constraint pair

Duplicate `K_T` as the nominal second constraint direction. The sampled constraint/generator rank is then one rather than two.

Classification: `rank_deficient_constraint_control_rejected`.

### F2 — decoupled second constraint

Use `K_X_decoupled = p_X`. Its flow translates `X` while failing to apply the compensating `q` shift required to preserve `Q_D = q-pT-aX`.

Classification: `decoupled_constraint_control_rejected`.

### F3 — wrong compensator

Reuse the Stage 13B deliberately wrong `XT` compensator. Every one of the 144 mixed pairs must remain detectably off target.

Classification: `wrong_compensator_detected`.

### F4 — one-clock incompleteness

Treat `q(T=tau; X raw)=Q_D+P_D tau+aX` as if fixing `T` alone produced a complete observable. Across the frozen three-value `X` grid each of the 12 `(orbit,tau)` groups must retain nonzero spread.

Classification: `one_clock_observable_incomplete`.

### F5 — cross-orbit false match

Use the canonical same-`P_D` and same-`Q_D` orbit pairs as false equivalence controls. Equality of one invariant must not collapse distinct full Dirac pairs.

Classification: `cross_orbit_false_positive_rejected`.

## 4. Frozen anomaly deformation

The deliberately non-first-class deformation is

`K_X_bad = exp(T)(p_X + a p) + epsilon q`

with `epsilon = 0.1`.

Using the frozen canonical Poisson convention,

`{K_T,K_X_bad} + K_X_bad = epsilon (q-p)`.

On the 36 positive Stage 13 representatives, the deformation also has nonzero `K_X_bad = epsilon q` residual because the undeformed `K_X` term vanishes there.

The positive requirement is therefore not to repair this deformation but to classify it as

`constraint_algebra_anomaly_detected`

and refuse admission as a positive carrier.

## 5. Frozen finite evidence counts

The executable Stage 13F source is required to expose:

- **36** positive representatives;
- **144** commuting-basis single-generator arrows: **72 `Phi_T` + 72 `Phi_X_tilde`**;
- **4** commuting-basis quotient classes, each with **9** representatives;
- **4 / 4** exact representative-set matches to the Stage 13D quotient;
- **36** basis-equivalence public/Dirac/relational checks;
- **144** commuting mixed-path checks;
- **6** destructive/anomaly controls, all required to be rejected.

## 6. Criteria allocation

Stage 13F is limited to Stage 13 criteria 44–47:

44. Noncommuting and equivalent commuting constraint presentations are compared and shown not to change licensed quotient-level physical content when typed correspondence is correct.
45. Rank-deficient, decoupled, wrong-compensator, one-clock-incomplete, and cross-orbit false positives are explicitly classified.
46. `K_X_bad` is detected as a constraint-algebra anomaly rather than admitted as a positive carrier.
47. Basis/path/anomaly results are not promoted to fundamental non-Abelianity, refoliation invariance, GR, eternalism, or ontological becoming.

Criteria 48–49 remain Stage 13G. Criterion 50 remains the external final repository regression / merge-readiness review.

## 7. Interpretation guards

- `noncommuting constraint presentation != fundamental physical non-Abelianity`;
- `constraint-basis change != physical-orbit change`;
- `basis-equivalent finite quotient != refoliation invariance`;
- `commuting presentation != proof that all admissible presentations commute`;
- `wrong compensator failure != physical time asymmetry`;
- `one clock condition in a two-gauge-direction model != complete relational observable`;
- `constraint-algebra anomaly != ontological becoming`;
- `multi-constraint path covariance != refoliation invariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `complete relational observable != ontological becoming by definition`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`.

## 8. Exit rule

The bounded result

`Stage 13F basis equivalence, ablation, anomaly, and false-positive controls on the frozen finite family = established`

may be promoted into the Stage 13 master protocol only after the Stage 13F source/test head passes the full repository regression.

Until then:

`Stage 13F source diagnostics satisfied != repository-validated Stage 13F completion`.