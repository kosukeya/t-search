# Stage 13B Result — Noncommuting Gauge Paths and Compensated Closure

Status: **executable implementation complete; repository CI checkpoint pending at the time of this result write.**

Incoming validated baseline: Stage 13A documentation-synchronized head `178f4ac8d160e7b261cd854f8c1856aa80c76675`, run #1696, **`1050 passed in 886.76s (0:14:46)`**.

## Executable family

`src/t_search/stage13_paths.py` consumes the Stage 13A positive carrier and evaluates the protocol-frozen **144 ordered mixed same-orbit source/target pairs** with nonzero `T` and `X` displacement.

For every pair,

`u_TX = DeltaX/exp(T1)`,

`u_XT = DeltaX/exp(T0)`,

and the positive correspondence law is

`u_XT = exp(s)u_TX`.

The implementation keeps the following three questions separate:

1. same raw `u` under reordered path words;
2. exact algebraically compensated reordered paths;
3. a deliberately wrong compensator.

## Same-raw reorder result

The canonical raw-order control uses `u_TX` in both path orders.

All **144 / 144** mixed pairs are expected to have detectably distinct final endpoints under this incorrect same-raw comparison.

Deterministic finite-grid endpoint-separation range:

- minimum: approximately **0.6321205588285577**;
- maximum: approximately **12.778112197861299**.

The `TX` path reaches the target while the reordered `XT` path does not. This is classified

`same_raw_parameter_reorder_false_positive_rejected`.

The mismatch is an endpoint-correspondence mismatch, not a constraint-surface failure.

## Compensated closure result

Using the exact `u_TX` and `u_XT`, all **144 / 144** path pairs are expected to close on the same declared target within `1e-10`.

Deterministic floating-point maxima from the frozen formulas are approximately

- compensator-law residual: **8.881784197001252e-16**;
- compensated endpoint separation: **2.220446049250313e-16**;
- compensated target residual: **2.220446049250313e-16**;
- positive two-constraint residual: **0.0**.

Bounded classification:

`Stage 13B compensated two-generator path closure on the frozen 144-pair finite family = established`

subject to repository CI validation of the new executable/test family.

## Wrong-compensator result

The deterministic wrong value is

`u_XT_wrong = u_XT + 0.25 (u_TX-u_XT)`.

It is distinct from the exact compensator on all mixed pairs. Expected target-residual range:

- minimum: approximately **0.15803013970713942**;
- maximum: approximately **3.1945280494653243**.

All **144 / 144** wrong-compensator cases are therefore expected to be detected as

`wrong_compensator_detected`.

## Surface and physical-orbit typing

The exact compensated paths preserve both positive constraints throughout the tested source/intermediate/endpoint family and retain the source/target declared physical-orbit identity.

A cross-orbit mixed-path constructor call is rejected rather than receiving a compensator:

`cross_orbit_path_rejected`.

This is typed carry-over only. Independent orbit discrimination from reconstructed Dirac data remains Stage 13C.

## Typed path provenance and temporal boundary

The Hamiltonian generator identities remain `K_T` and `K_X`, while the transport segments recorded in the path word are

`path_word_TX = (Phi_T,Phi_X)`

and

`path_word_XT = (Phi_X,Phi_T)`.

The path records carry

`temporal_order_status = not_physical_temporal_order`

and

`metaphysical_claim_status = not_licensed`.

Therefore Stage 13B does not identify generator identity with transport identity and does not interpret raw path order, compensator failure, or successful compensated closure as an arrow of time, ontological becoming, or eternalism result.

## Stage boundary

Stage 13B does not yet establish complete relational covariance or quotient/operational descent. The next executable question is Stage 13C:

> reconstruct `Q_D=q-pT-0.5X` and `P_D=p` independently across all representatives, discriminate the four physical orbits under the full pair, construct `q(T=tau,X=chi)`, and explicitly show why fixing only one clock is incomplete.

## Guards

- `raw gauge-path commutativity != successful multi-constraint closure`;
- `same raw generator parameters under reordered paths != corresponding gauge path`;
- `wrong compensator failure != physical time asymmetry`;
- `path word != physical temporal history`;
- `path-order mismatch != arrow of time by definition`;
- `compensated multi-constraint path closure != refoliation invariance`;
- `first-class finite path closure != hypersurface-deformation algebra`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `finite-model success != empirical discovery`.
