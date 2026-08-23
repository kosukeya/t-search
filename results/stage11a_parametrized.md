# Stage 11A Results — Minimal Parametrized Constrained Carrier and Admissible Family

Status: **criteria 11–16 satisfied by the executable Stage 11A diagnostics; broader Stage 11 covariance remains unestablished.**

## Result summary

Stage 11A successfully implements the frozen minimal parametrized constrained scaffold without treating the external parameter as physical time.

Constraint:

`C = p_T + p^2/2 = 0`.

Canonical physical seed:

- momentum `p=1.25`;
- conjugate clock momentum `p_T=-0.78125`;
- positive lapse `N(lambda)=1+lambda^2/4`;
- internal clock `T(lambda)=lambda+lambda^3/12`;
- configuration `q(T)=-0.35+1.25 T`;
- 13 explicitly typed sampled physical events.

## Frozen positive parameterization family

| id | map | admissible |
| --- | --- | --- |
| `identity` | `lambda'=lambda` | yes |
| `affine` | `lambda'=2 lambda+1` | yes |
| `cubic` | `lambda'=lambda+lambda^3/4` | yes |
| `hyperbolic` | `lambda'=sinh(lambda)` | yes |

For every positive chart:

`N'(lambda')=N(lambda)/f'(lambda)`.

The minimum transformed lapse over the full tested positive family is **0.5**, so the implemented positive family never crosses or touches zero lapse.

## Constraint and orbit preservation

Executable diagnostics:

| diagnostic | value |
| --- | ---: |
| event count | 13 |
| positive parameterization count | 4 |
| minimum positive lapse | 0.5 |
| max constraint residual | 0.0 |
| max lapse chain-rule residual | 0.0 |
| max clock-orbit residual | 0.0 |
| max q-orbit residual | 0.0 |
| max p-orbit residual | 0.0 |
| max p_T-orbit residual | 0.0 |
| different-label corresponding event pairs | 36 |
| nonlinear raw-rate differences | 24 |

The same event carrier therefore preserves `T`, `q`, `p`, and `p_T` exactly in the canonical finite arithmetic while raw external labels differ.

The positive result is deliberately stated as

`minimal Stage 11A constraint orbit preservation = established`

rather than as a general covariance claim.

## Anti-triviality witness

Across the affine/cubic/hyperbolic representations, **36** corresponding physical-event pairs have unequal external parameter values relative to the identity representation.

For the two nonlinear representations, **24** sampled points have raw `dq/dlambda` rates that differ from the identity representation.

Thus the implementation is not validated merely because unchanged event labels were copied between charts.

`same labels after relabeling != sufficient evidence of covariance`.

The relational derivative itself is reserved for Stage 11B.

## Excluded controls

The following maps are represented explicitly but rejected by the positive trajectory constructor:

- `orientation_reverse`: `f(lambda)=-lambda`;
- `noninjective_square`: `f(lambda)=lambda^2` on the both-sign test domain.

Therefore:

`orientation reversal != member of the initial positive admissible family`.

`non-injective relabeling != admissible reparameterization`.

## Criteria 11–16

11. Minimal constrained parametrized trajectory with positive lapse — **satisfied**.
12. Identity/affine/cubic/hyperbolic family implemented — **satisfied**.
13. Different raw parameter values at corresponding events demonstrated — **satisfied**.
14. Chain-rule lapse transformation verified — **satisfied**.
15. Constraint-orbit/relational trajectory preserved — **satisfied**.
16. Orientation-reversing and non-injective maps excluded from the positive family — **satisfied**.

## Boundary of the result

Stage 11A alone does not establish `parametrized_covariant`. In particular it has not yet shown that relational observables/derivatives, O/P/R/V/Xi, the Stage 10 future measurement, or the A/B/C clock-change square are covariant under reparameterization.

Guards:

- `same constraint orbit != same metaphysics`;
- `same constraint orbit != established general covariance`;
- `parameter orientation != physical record direction by definition`;
- `parametrized covariance precursor != general relativity`;
- `absence of preferred external parameterization != absence of ontological becoming`;
- `finite-model success != empirical discovery`.

Next checkpoint: **Stage 11B — relational observables and relational derivatives.**
