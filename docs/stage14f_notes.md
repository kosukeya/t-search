# Stage 14F Notes — Ablation / Anomaly / False-Positive Controls

Status: **validated source/test checkpoint; criteria 44–47 satisfied at the scientific checkpoint. Stage 14G is next after documentation synchronization.**

## Repository checkpoint

- branch: `agent/stage-14-structure-function-precursor`
- Stage 14F source/test/runner head: `9f20ad22940ba827d346fbb7386eced5e26daedd`
- GitHub Actions run: **#1900** (`32740094197`)
- PR merge checkout: `d636706b8e141befe0e80b2841413aaeb8f0cabc`
- workflow conclusion: **success**
- full repository result: **`1154 passed in 664.20s (0:11:04)`**

`repository validation != new scientific evidence`.

## Control-matrix design

Stage 14F does not reinterpret a successful destructive control as positive physical evidence. Each control is classified by the layer it destroys:

- algebra/rank: structure-function removal, duplicated direction, missing `D`, `H_2_bad` anomaly;
- path licensing/compensation: wrong or missing `D` compensator, cross-orbit path;
- relational completeness: two-clock incomplete observable;
- basis equivalence: singular scalar rescaling;
- typed operational descent: representative/path/basis payload corruption and false Xi typing;
- interpretation boundary: false universal-Abelianization / universal-trivializability overclaim.

The matrix contains **14 controls**, all **14/14 rejected** from the positive evidence family.

## Deterministic diagnostics

- structure-function-removed `kappa=0` witnesses: **108**;
- duplicate/rank-deficient witnesses: **108**;
- missing-third-direction witnesses: **108/108**;
- wrong-sign / wrong-value compensator witnesses: **1728**;
- missing-compensator witnesses: **1728**;
- cross-orbit false-positive pairs rejected: **8748/8748**;
- two-clock incomplete groups: **36/36**;
- singular scalar-basis controls: **2/2**;
- singular witnesses: **72 = 36 vanishing + 36 nonfinite**;
- deformed-constraint anomaly witnesses: **108/108**;
- minimum anomaly closure residual: **0.075**;
- maximum anomaly closure residual: **0.175**;
- representative/path/basis payload-corruption controls: **3/3**;
- false typed operational context: **rejected**;
- false universal-Abelianization interpretation: **rejected**;
- all control/metaphysical claim statuses: **not licensed**;
- `criteria_44_47_satisfied = true`.

## Deformed-constraint anomaly

The frozen deformation is

`H_2_bad = H_2 + epsilon q`, with `epsilon=0.1`.

Stage 14F rebuilds the deformed surface rather than evaluating the new constraint only on the old positive surface. With `D=0`, the deformed surface uses

`p_2 = -b p - epsilon q`,

so that `D=H_1=H_2_bad=0` is satisfied before closure is tested.

On that deformed surface,

`{H_1,H_2_bad} = -epsilon p`,

and

`{H_2_bad,D} = epsilon a = 0.05`.

Because the sampled `P_D=p` values are all nonzero, every one of the **108** deformed-surface witnesses has a nonzero first-class closure residual. The minimum maximum-bracket residual is **0.075** and the maximum is **0.175**.

Classification:

`constraint_algebra_anomaly_detected`.

This is an anomaly of the deliberately deformed finite constraint set. It is not ontological becoming and is not evidence for fundamental physical non-Abelianity.

## Ablation controls

### Structure functions removed

Setting `kappa=0` removes both frozen phase-space-dependent structure-function channels on all **108** representatives.

Classification:

`structure_function_removed_control_rejected`.

This simpler carrier is excluded from the positive Stage 14 structure-function family; its existence does not refute that family.

### Rank / third direction removed

Duplicating `D` lowers the three-row constraint rank to two, and dropping `D` leaves only the rank-two `H_1/H_2` span on all **108** representatives.

Classifications:

- `rank_deficient_constraint_control_rejected`;
- `missing_third_direction_control_rejected`.

### Compensation controls

The validated Stage 14B family is reused without changing its positive rule:

- wrong-sign and wrong-value compensators fail on the required **1728** ordered paths;
- missing `D` compensation fails on **1728/1728** paths.

Classifications:

- `wrong_structure_function_compensator_detected`;
- `missing_third_direction_compensator_detected`.

### Cross-orbit and incomplete-relational controls

- cross-orbit licensed arrows: **0**;
- cross-orbit rejected ordered pairs: **8748**;
- two-clock fixed-clock groups retaining third-direction dependence: **36/36**.

Classifications:

- `cross_orbit_false_positive_rejected`;
- `two_clock_observable_incomplete`.

### Singular basis control

The Stage 14D vanishing-factor and nonfinite-factor controls remain rejected as singular, with **72** total singular witnesses.

Classification:

`singular_scalar_rescaling_rejected`.

## Typed operational controls

The three Stage 14E payload corruptions remain rejected:

- `representative_dependent_payload_corruption_detected`;
- `path_dependent_payload_corruption_detected`;
- `basis_dependent_payload_corruption_detected`.

Stage 14F additionally corrupts Xi outcome correspondence and confirms that typed architecture validation rejects the resulting context as

`typed_operational_context_rejected`.

The interpretation-level claim that one finite triangular Abelianization licenses universal basis trivializability is rejected as

`false_universal_abelianization_interpretation_rejected`.

## Bounded result

`Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established`

The control matrix supports the diagnostic specificity of the positive Stage 14A–E chain: removing or corrupting required structure produces the expected typed failure modes. It does not add an independent physical discovery.

Persistent guards:

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
