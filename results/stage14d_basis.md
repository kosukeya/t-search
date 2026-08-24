# Stage 14D Result — Basis Pressure Test

## Validated checkpoint

- branch: `agent/stage-14-structure-function-precursor`
- source/test head: `3e44454952d71ebbe9b0a52bbd9d68cd398d0635`
- GitHub Actions run: **#1880**
- PR merge checkout: `ddaf724a880b32f5b45b8442866c29cc33713cc3`
- result: **`1139 passed in 889.88s (0:14:49)`**

`repository validation != new scientific evidence`

## Deterministic evidence

### Frozen simple-scalar class

For

`H_1' = f_1(z) H_1`, `H_2' = f_2(z) H_2`, `D' = f_D(z) D`,

with finite nonzero diagonal factors and no constraint mixing,

`{H_1',H_2'} mod span(H_1',H_2') = [-kappa X f_1 f_2/f_D] D'`.

Therefore, on the frozen `kappa=0.5` carrier, an admissible diagonal rescaling cannot eliminate this component at `X != 0`.

Executable checks:

- scalar factor families: **3**;
- scalar evaluations: **324 = 108 × 3**;
- `X != 0` evaluations: **216**;
- nonzero-component obstruction: **216/216**;
- distinct `X != 0` representatives covered: **72/72**;
- `X = 0` evaluations: **108**;
- expected zero component at `X=0`: **108/108**;
- minimum nonzero `|D'|` coefficient: approximately **0.3843557173958058**;
- maximum `|D'|` coefficient: approximately **1.135254038874606**.

### Singular controls

- vanishing-factor control: **36** singular witnesses;
- nonfinite-factor control: **36** singular witnesses;
- controls rejected: **2/2** as `singular_scalar_rescaling_rejected`.

### Frozen triangular mixing

`H_2_tilde = H_2-kappa T1 X D = p_2+b p`.

- triangular probes: **216**;
- positive probes: **108**;
- off-surface probes: **108**;
- determinant: **1.0** on every probe;
- inverse-identity residual maximum: **0.0**;
- forward/inverse constraint-correspondence residual maximum: **0.0**;
- exact `H_2_tilde` formula residual maximum: **0.0**;
- strong commuting-bracket residual maximum: **0.0**.

### Basis-content preservation

- typed basis-content checks: **108**;
- quotient membership preserved: **108/108**;
- sampled quotient retained: **4 classes × 27 representatives**;
- Dirac-pair residual maximum: **0.0**;
- complete three-condition relational residual maximum: **0.0**;
- triangular-basis Dirac-bracket residual maximum: **0.0**;
- inherited public `O/P/R/V` payload equality: **108/108**;
- public payloads containing neither original nor triangular basis ID: **108/108**.

## Bounded result

`Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established`

This is evidence that the Stage 13F **simple multiplicative trivialization does not persist** unchanged on the Stage 14 carrier: diagonal nonzero rescaling cannot eliminate the nonzero third-direction coefficient where `X != 0`. However, a richer invertible triangular mixing does provide an equivalent commuting presentation.

Accordingly:

- `noncommuting presentation != fundamental physical non-Abelianity`;
- `Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability`;
- `triangular basis equivalence != universal basis trivializability`;
- `constraint-basis change != physical-orbit change`;
- `basis-equivalent finite quotient != refoliation invariance`;
- `commuting triangular presentation != proof that all admissible presentations commute`;
- `basis equivalence != hypersurface-deformation algebra`;
- `basis equivalence != general relativity`;
- `basis equivalence != ontological becoming`;
- `finite-model success != empirical discovery`.

## Gate status

Stage 14D closes the frozen criteria **32–38** at the validated source/test checkpoint. After documentation synchronization, the next step is **Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases**.
