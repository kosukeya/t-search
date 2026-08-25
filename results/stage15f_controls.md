# Stage 15F Result — Destructive Control Audit

## Validated checkpoint

- branch: `agent/stage-15-spatially-indexed-constraint-algebra`
- final source/test head: `96b7ca36af8a13d5925b0433052c84af97e0ca80`
- GitHub Actions PR run: **#1982** (`32816700390`)
- result: **`1242 passed in 489.65s (0:08:09)`**

`repository validation != new scientific evidence`.

## Control outcome

Stage 15F implements **15** destructive controls and rejects **15/15** as intended. The matrix covers all **10** required protocol classifications.

Deterministic diagnostics:

- baseline nonzero local brackets: **72**;
- nonzero local brackets after `kappa=0`: **0**;
- middle-generator deletion minimum rank: **2**;
- disconnected 0-to-2 false path: rejected;
- locality/basis controls: **4/4** rejected;
- wrong-sign smearing probes: **648**, detections **360**;
- Jacobi anomaly probes: **108**, detections **108**, signal **0.125**;
- cross-orbit false-path pairs: **8748**, rejected **8748/8748**, licensed **0**;
- incomplete-relational groups: **108**, rejected **108/108**, maximum spread **2.0**;
- typed public O/P/R/V corruption controls: **4/4** detected;
- known full seed reconstruction: one-step L1 = **false**, `Lfinite` depth = **2**.

## Locality / basis discrimination

The controls distinguish four logically separate failure modes: support expansion, distance-2 coefficient dependence, noninvertibility, and non-one-step locality of the known seed reconstruction. A map can therefore be locally shaped in support bookkeeping while still failing invertibility, and an algebraic Abelianization can remain equivalent while not qualifying as one-step L1.

This preserves the Stage 15D result: a different partial nearest-neighbour shear provides the positive L1 Abelianization witness, while the full seed reconstruction itself remains Lfinite depth 2.

## Algebra / path discrimination

Removing `kappa` removes all nontrivial tested local brackets. Wrong-sign smearing fails antisymmetry on the expected nonzero subset, an explicit `epsilon*T2` anomalous term fails Jacobi on every off-surface probe, and cross-orbit representative pairs remain unlicensed as local physical paths.

These are validator-discrimination results only.

## Relational / typed discrimination

Every one-clock-omitted relational group retains representative dependence and is rejected. Representative/path/basis provenance injected into public O/P/R/V is also detected, while the positive architecture continues to keep those data in Xi.

## Bounded result

`Stage 15F frozen locality-breaking, anomaly, false-positive, relational, and typed-payload controls on the Stage 15 finite carrier = all declared controls rejected as intended`

This does **not** establish continuum correctness, GR, refoliation invariance, causal locality, a quantum anomaly theorem, ontological superselection, eternalism, ontological becoming, absence of becoming, or empirical discovery.

Guards:

- `negative-control rejection != proof of continuum correctness`;
- `graph disconnection control != relativistic causal disconnection`;
- `locality-breaking detection != physical causal locality`;
- `constraint-algebra anomaly detection != quantum anomaly theorem`;
- `cross-orbit rejection != ontological superselection`;
- `incomplete relational rejection != ontological becoming`;
- `typed corruption detection != ontological equivalence`;
- `local Abelianization surviving controls != physical triviality`;
- `known seed non-L1 classification != universal nonlocality of Abelianization`;
- `spatially indexed constraint precursor != general relativity`;
- `repository validation != new scientific evidence`.

## Gate status

Stage 15F closes criteria **44–47**.

Stage 15 protocol status: **criteria 1–47 satisfied / 48–50 pending**.

Criteria **48–50 remain pending at the Stage 15F checkpoint**.

Next: **Stage 15G — executable synthesis and evidence-selected Stage 16 gate**.
