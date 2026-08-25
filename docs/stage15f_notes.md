# Stage 15F Notes — Locality-Breaking / Anomaly / False-Positive Controls

Status: **validated source/test checkpoint; criteria 44–47 satisfied. Stage 15G is next.**

## Repository checkpoint

- branch: `agent/stage-15-spatially-indexed-constraint-algebra`
- final Stage 15F source/test head: `96b7ca36af8a13d5925b0433052c84af97e0ca80`
- GitHub Actions PR run: **#1982** (`32816700390`)
- PR merge checkout: `3b7df79dc953669b4aef5e6a4fa7326d1087432c`
- workflow conclusion: **success**
- full repository result: **`1242 passed in 489.65s (0:08:09)`**

`repository validation != new scientific evidence`.

## Stage 15F role

Stage 15F adds no new positive carrier. It deliberately breaks one frozen Stage 15 assumption at a time and checks that the relevant positive claim is not silently accepted. Passing a control therefore means **validator discrimination**, not new evidence for general relativity, refoliation invariance, causal locality, or a metaphysical conclusion.

## Deterministic control matrix

The executable Stage 15F checkpoint contains **15 destructive controls**, all **15/15 rejected as intended**, while covering all **10** classifications required by the Stage 15 protocol vocabulary.

### Structure-function removal

- off-surface probes: **108**;
- baseline nonzero `{C0,C1}` probes: **72**;
- after `kappa=0`: **0** nonzero probes;
- classification: `structure_function_removed_control_rejected`.

The control confirms that the Stage 15A nontrivial local bracket is genuinely tied to the frozen nonzero `kappa`; it does not establish a continuum structure-function algebra.

### Site deletion / disconnection

- delete the middle labelled generator: minimum tested constraint-gradient rank = **2**, below the positive rank 3;
- after deleting site 1, the graph contains no 0-to-2 route;
- disconnected false path rejected: **true**;
- classification: `disconnected_site_false_positive_rejected`.

`graph disconnection control != relativistic causal disconnection`.

### Locality / basis false positives

Four locality/basis controls are all rejected:

1. support-expanding generator corruption -> `support_expansion_detected`;
2. distance-2 coefficient dependence in an alleged L1 map -> `distance2_basis_nonlocal_detected`;
3. singular `diag(1,0,1)` map -> `singular_basis_map_rejected` on **108/108** representatives;
4. known full seed reconstruction remains **not** one-step L1 and remains `Lfinite` with exact depth **2**.

The singular control is intentionally useful because its support bookkeeping is L0-shaped; invertibility must therefore be checked independently of locality metadata.

### Smearing antisymmetry corruption

- probes: **648 = 108 × 6**;
- deliberately wrong-sign reverse-bracket violations detected: **360/648**;
- classification: `smearing_antisymmetry_corruption_detected`.

The count is independently explained by five nonzero-wedge smearing pairs times 72 nonzero-structure-function probes.

### Jacobi anomaly

The corrupted bracket adds `epsilon*T2`, with `epsilon=0.125`, to `{C0,C1}`.

- anomaly probes: **108**;
- detected: **108/108**;
- maximum anomaly signal: **0.125**;
- classification: `constraint_algebra_anomaly_detected`.

`constraint-algebra anomaly detection != quantum anomaly theorem`.

### Cross-orbit false positive

- cross-orbit ordered representative pairs: **8748**;
- licensed: **0**;
- rejected: **8748/8748**;
- classification: `cross_orbit_false_positive_rejected`.

`cross-orbit rejection != ontological superselection`.

### Incomplete relational observable

All one-clock-omitted groups retain raw-clock dependence:

- groups: **108**;
- rejected as incomplete: **108/108**;
- maximum residual spread: **2.0**;
- classification: `relational_observable_incomplete`.

`incomplete relational rejection != ontological becoming`.

### Typed O/P/R/V corruption

The final protocol item is decomposed into four explicit public-layer corruptions:

- representative-dependent O corruption;
- path-dependent P corruption;
- basis-dependent R corruption;
- representative-dependent V corruption.

All **4/4** are detected. The tests require both architecture validation failure and a changed quotient-level public projection, so the control detects provenance leaking from Xi into public O/P/R/V rather than merely checking a tag.

Classifications include:

- `representative_dependent_payload_corruption_detected`;
- `path_dependent_payload_corruption_detected`;
- `basis_dependent_payload_corruption_detected`.

`typed corruption detection != ontological equivalence`.

## Bounded result

`Stage 15F frozen locality-breaking, anomaly, false-positive, relational, and typed-payload controls on the Stage 15 finite carrier = all declared controls rejected as intended`

This establishes that the declared finite validators distinguish the tested positive Stage 15 structures from the frozen destructive corruptions. It does **not** establish continuum correctness, general relativity, refoliation invariance, physical causal locality, a quantum anomaly theorem, ontological superselection, eternalism, ontological becoming, absence of becoming, or empirical discovery.

Persistent guards:

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

Stage 15F closes criteria **44–47** at the validated source/test checkpoint.

Stage 15 protocol status is now **criteria 1–47 satisfied / 48–50 pending**.

Criteria **48–50 remain pending at the Stage 15F checkpoint**.

Next: **Stage 15G — executable synthesis and evidence-selected Stage 16 gate**.
