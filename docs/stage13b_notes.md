# Stage 13B Notes — Noncommuting Gauge Paths and Compensated Closure

Status: **implementation complete; criteria 17–23 close only after the Stage 13B executable/test family passes repository CI.**

Incoming Stage 13A final checkpoint: head `178f4ac8d160e7b261cd854f8c1856aa80c76675`, GitHub Actions run #1696, **`1050 passed in 886.76s (0:14:46)`**.

## Question

Stage 13B asks whether the 144 mixed ordered source/target pairs reserved by Stage 13A exhibit the protocol-frozen nontrivial two-generator path structure: reordered raw paths should differ when the same `K_X` parameter is reused, while algebraically compensated paths should close onto the same licensed target.

Stage 13B does **not** yet reconstruct Dirac data or two-clock complete relational observables from representative data. Those are Stage 13C questions.

## Canonical mixed family

The positive family is exactly the Stage 13A set of **144 ordered same-orbit pairs** for which both

`s = T1-T0 != 0`

and

`DeltaX = X1-X0 != 0`.

For every pair,

`u_TX = DeltaX / exp(T1)`,

`u_XT = DeltaX / exp(T0)`,

so the frozen compensator law is

`u_XT = exp(s) u_TX`.

All 144 pairs have `u_TX != u_XT`; the two-generator ordering is therefore nontrivial throughout the declared finite family.

## Same-raw-parameter reorder control

To isolate raw order dependence, the executable control uses the `TX` value `u_TX` in **both** path orders:

`Phi_X(u_TX) after Phi_T(s)`

versus

`Phi_T(s) after Phi_X(u_TX)`.

The first path reaches the declared target by construction. The reordered path does not. The expected endpoint separation over the frozen grid ranges from approximately

- minimum **0.6321205588285577**;
- maximum **12.778112197861299**.

Both paths nevertheless remain on the positive constraint surface. Thus the control deliberately separates

`constraint-surface preservation`

from

`correct source/target path correspondence`.

Classification:

`same_raw_parameter_reorder_false_positive_rejected`.

`raw gauge-path commutativity != successful multi-constraint closure`.

## Exact compensated closure

The positive `TX` path uses `u_TX`, while the reordered `XT` path uses `u_XT`.

The executable comparison requires, for every one of the 144 mixed pairs,

- compensator-law residual `<= 1e-10`;
- `TX` endpoint to equal the declared target within tolerance;
- `XT` endpoint to equal the declared target within tolerance;
- compensated `TX` and `XT` endpoints to agree within tolerance;
- all intermediate/final positive path points to satisfy both constraints within tolerance.

The deterministic floating-point construction has expected maximum compensator-law residual about **8.88e-16**, maximum compensated endpoint/target residual about **2.22e-16**, and positive-surface constraint residual **0.0**.

Classification:

`compensated_path_closure_established`.

## Wrong-compensator control

Stage 13B keeps wrong compensation separate from the same-raw control. For each pair it defines

`u_XT_wrong = u_XT + 0.25 (u_TX-u_XT)`.

This parameter lies one quarter of the way from the exact `XT` value toward the wrong same-raw value and is nonexact for every mixed pair.

The expected target residual ranges from approximately

- minimum **0.15803013970713942**;
- maximum **3.1945280494653243**.

The wrong path can remain on the constraint surface while failing the typed endpoint correspondence.

Classification:

`wrong_compensator_detected`.

`wrong compensator failure != physical time asymmetry`.

## Declared physical-orbit identity and cross-orbit rejection

The positive constructor requires source and target to carry the same declared physical-orbit identity. All 144 positive comparisons retain that identity while the compensated paths preserve both constraints.

A cross-orbit source/target pair is rejected at construction time rather than being assigned a compensator.

Classification:

`cross_orbit_path_rejected`.

Independent physical-orbit reconstruction from Dirac data remains Stage 13C work; Stage 13B establishes only the typed carry-over needed for the path test.

## Path-order typing

Every comparison separately records

- generator identities `K_T` and `K_X` as the Hamiltonian sources of the flows;
- `path_word_TX = (Phi_T,Phi_X)`;
- `path_word_XT = (Phi_X,Phi_T)`;
- path-word role `constraint_generated_gauge_path_word`;
- path-order role `gauge_generator_order_metadata`;
- temporal-order status `not_physical_temporal_order`;
- metaphysical-claim status `not_licensed`.

Thus constraint-generator identity and transport-segment identity remain separately interpretable, and raw path order is executable provenance rather than a physical temporal-order declaration.

`path word != physical temporal history`.

`path-order mismatch != arrow of time by definition`.

## Stage boundary

A successful Stage 13B establishes compensated two-generator path closure only on the frozen finite carrier. It does not yet establish

- representative-independent Dirac reconstruction;
- two-clock complete relational covariance;
- typed quotient/path-word descent;
- O/P/R/V measurement descent;
- refoliation invariance;
- a hypersurface-deformation algebra;
- general relativity.

## Interpretation guards

- `raw gauge-path commutativity != successful multi-constraint closure`;
- `same raw generator parameters under reordered paths != corresponding gauge path`;
- `wrong compensator failure != physical time asymmetry`;
- `path word != physical temporal history`;
- `path-order mismatch != arrow of time by definition`;
- `compensated multi-constraint path closure != refoliation invariance`;
- `first-class finite path closure != hypersurface-deformation algebra`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `finite-model success != empirical discovery`.
