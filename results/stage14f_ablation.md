# Stage 14F Result — Ablation / Anomaly / False-Positive Controls

## Validated checkpoint

- branch: `agent/stage-14-structure-function-precursor`
- source/test/runner head: `9f20ad22940ba827d346fbb7386eced5e26daedd`
- GitHub Actions run: **#1900** (`32740094197`)
- PR merge checkout: `d636706b8e141befe0e80b2841413aaeb8f0cabc`
- result: **`1154 passed in 664.20s (0:11:04)`**

`repository validation != new scientific evidence`.

## Deterministic control matrix

The executable Stage 14F matrix contains **14 controls** and rejects **14/14** from the positive evidence family.

| Control | Classification | Frozen witness |
|---|---|---:|
| `kappa=0` structure-function removal | `structure_function_removed_control_rejected` | 108 |
| duplicate direction | `rank_deficient_constraint_control_rejected` | 108 |
| missing `D` direction | `missing_third_direction_control_rejected` | 108 |
| wrong-sign / wrong-value compensator | `wrong_structure_function_compensator_detected` | 1728 |
| missing `D` compensator | `missing_third_direction_compensator_detected` | 1728 |
| cross-orbit gauge path | `cross_orbit_false_positive_rejected` | 8748 |
| two-clock expression | `two_clock_observable_incomplete` | 36 groups |
| singular scalar basis | `singular_scalar_rescaling_rejected` | 72 |
| `H_2_bad=H_2+epsilon q` | `constraint_algebra_anomaly_detected` | 108 |
| representative payload corruption | `representative_dependent_payload_corruption_detected` | rejected |
| path payload corruption | `path_dependent_payload_corruption_detected` | rejected |
| basis payload corruption | `basis_dependent_payload_corruption_detected` | rejected |
| false Xi typing | `typed_operational_context_rejected` | rejected |
| universal-Abelianization overclaim | `false_universal_abelianization_interpretation_rejected` | rejected |

## Constraint-algebra anomaly evidence

Frozen deformation:

`H_2_bad=H_2+epsilon q`, `epsilon=0.1`.

The deformed constraint surface is rebuilt using

`p_2=-b p-epsilon q`

with the other carried coordinates chosen so that `D=H_1=0`. Hence all **108** anomaly probes satisfy

`D=H_1=H_2_bad=0`

within tolerance before bracket closure is tested.

The deformed brackets retain

`{H_1,H_2_bad}=-epsilon p`,

`{H_2_bad,D}=epsilon a`.

Executable values:

- anomaly witnesses: **108/108**;
- minimum maximum-bracket residual: **0.075**;
- maximum maximum-bracket residual: **0.175**;
- deformed-surface residual: within the frozen tolerance for all witnesses.

Thus the deformation is detected as `constraint_algebra_anomaly_detected` rather than silently admitted to the positive first-class family.

## Other destructive evidence

- structure-function-removed witnesses: **108**;
- rank-deficient witnesses: **108**;
- missing-third-direction witnesses: **108**;
- wrong-compensator witnesses: **1728**;
- missing-compensator witnesses: **1728**;
- cross-orbit rejected pairs: **8748**;
- two-clock incomplete groups: **36**;
- singular controls: **2/2**;
- singular witnesses: **72**;
- payload-corruption controls: **3/3**;
- false typing: **rejected**;
- universal-Abelianization overclaim: **rejected**;
- all control/metaphysical claims: **not licensed**;
- `criteria_44_47_satisfied = true`.

## Bounded result

`Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established`

This result says that the frozen destructive controls fail in the expected typed ways while the validated Stage 14A–E positive family remains logically separate. It does not convert negative-control behavior into new positive physical evidence.

Interpretation guards:

- `negative-control rejection != positive-family obstruction`;
- `structure-function removal != evidence against the positive carrier`;
- `missing-third-direction failure != physical time asymmetry`;
- `wrong compensator failure != physical time asymmetry`;
- `constraint-algebra anomaly != ontological becoming`;
- `constraint-algebra anomaly != fundamental physical non-Abelianity`;
- `control rejection != hypersurface-deformation algebra`;
- `control rejection != general relativity`;
- `two-clock incompleteness != physical time asymmetry`;
- `cross-orbit rejection != spacetime causal separation`;
- `singular-basis rejection != universal non-Abelianizability`;
- `false typing rejection != empirical discovery`;
- `finite-model success != empirical discovery`.
