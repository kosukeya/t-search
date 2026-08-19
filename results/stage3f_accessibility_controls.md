# Stage 3F — Accessibility and Information Controls

Status: **implemented; final GitHub Actions checkpoint result to be recorded after the Stage 3F head completes**.

## Purpose

Stage 3F changes only the declared local observation channel. The global reversible block and its trajectory distribution remain fixed.

The core question is whether information can remain globally represented while becoming degraded or inaccessible through a local interface.

## 1. Exact record-readout degradation

For the record-only interface at neutral position `1`, the true canonical relation is:

`M_1=X_0`.

Passing the readout through a binary-symmetric channel with error probability `epsilon` gives:

`I(M_obs;X_0)=1-h_2(epsilon)`

and:

`I(M_obs;X_2)=0`.

The tested checkpoints are:

| `epsilon` | lower-side MI | upper-side MI | lower decoder | upper decoder | accessible `A_R` | accessible `A_Acc` |
|---:|---:|---:|---:|---:|---:|---:|
| `0` | `1` | `0` | `1` | `0.5` | `1` | `0.5` |
| `1/4` | `~0.188721875541` | `0` | `0.75` | `0.5` | `~0.188721875541` | `0.25` |
| `1/2` | `0` | `0` | `0.5` | `0.5` | `0` | `0` |

Thus the accessible record-defined contrast decreases continuously to zero under maximal binary readout noise.

## 2. Global information remains unchanged

Across all access policies above, the underlying block is unchanged and still satisfies:

`I(M_1;X_0)=1 bit`.

At `epsilon=1/2` with current `X` masked:

`I(true M_1;X_0)=1`

while:

`I(M_obs;X_0)=0`.

Therefore the construction explicitly realizes:

**globally represented information can be locally inaccessible under a declared observation channel.**

The supported distinction is model/interface-relative:

`inaccessible != absent from the formal global state`.

It is not a proof of a metaphysical hidden reality.

## 3. Redundant local information survives record-readout failure

The canonical recording map leaves:

`X_1=X_0`.

Consequently, at maximally noisy record readout (`epsilon=1/2`) with `X_1` still exposed:

- record-only `I(M_obs;X_0)=0`;
- record-only decoder accuracy `=1/2`;
- full local observation `I((X_1,M_obs);X_0)=1`;
- full local decoder accuracy `=1`.

An `X`-only interface also retains perfect lower-side access.

This is an important limitation/feature of the canonical model:

**record-specific accessibility and total local accessibility are not the same quantity.**

Noise applied only to `M` cannot erase information redundantly available in `X_1`.

## 4. Masking `X` exposes readout-noise ambiguity

With `X` hidden and exact `M` readout, observed:

`(X_obs,M_obs)=(None,1)`

is compatible with two global histories.

At `epsilon=1/4`, the same observed outcome has positive probability under all four canonical histories.

The exact posterior is:

- two histories with `X_0=1`: probability `3/8` each;
- two histories with `X_0=0`: probability `1/8` each.

Hence:

`P(X_0=1 | M_obs=1)=3/4`.

The compatible-history count changes:

`2 -> 4`.

This is increased epistemic/interface ambiguity. It is not evidence of additional ontic alternatives.

## 5. Visible `X` prevents that support expansion

At the same `epsilon=1/4`, if `X_1` is exposed, the outcome:

`(X_1,M_obs)=(1,1)`

remains compatible with only two histories because exact `X_1` already fixes `X_0=1` in the canonical model.

The posterior over the two hidden-`N` histories is `1/2,1/2`.

This control makes the redundancy explicit rather than attributing all local information to the record register.

## 6. Complete masking endpoint

If both local bits are hidden, the only observation is:

`(None,None)`.

Then:

`I(O;X_0)=0`

and Bayes-optimal decoding returns prior-level accuracy:

`1/2`.

All four canonical histories remain compatible.

The histories and their global weights have not been deleted; they are simply not distinguished by this local interface.

## 7. Coverage remains a separate reconstruction axis

The Stage 3E exact-view result is retained as a Stage 3F coverage control:

- central exact view alone: `2` compatible histories;
- central plus position-2 exact views: `1` compatible history.

Therefore:

`readout quality != view coverage`.

Information loss/degradation at one interface dimension and reconstruction from multiple perspectives must be analyzed separately.

## Information classification after Stage 3F

### Still globally represented

- the complete reversible trajectories;
- true `M_1` and its perfect canonical correlation with `X_0`;
- hidden `N`;
- exact global trajectory weights.

### Locally accessible under the strongest interface

- current `X_1`;
- exact or noisy `M_obs` according to policy;
- lower-side target information through whichever exposed variables carry it.

### Degraded by record noise

- information specifically available through `M_obs`;
- record-only Bayes accessibility;
- accessible signed record contrast.

### Ambiguous under masking/noise

- global history identity when exposed fields fail to distinguish hidden variables;
- lower-side target value when both redundant access paths are removed or degraded.

### Reconstructible with suitable complementary coverage

- hidden `N` and the full actual trajectory from compatible multi-position exact `(X,M)` views in the canonical model.

## Strongest justified Stage 3F conclusion

Within the declared finite toy-model interfaces:

**local accessibility is an interface-relative property. The same reversible global block can retain a perfect record correlation while a noisy or masked local readout carries less or no usable information about that correlation. Redundant exposed variables can preserve total local accessibility even after record-specific accessibility is lost, and reduced access expands compatible-history classes without creating new global histories.**

This strengthens the project guard:

`inaccessible information != information absent from the formal model`.

## Limits

Stage 3F does not establish:

- that inaccessible physical information always exists globally in nature;
- a fundamental observer-independent notion of information accessibility;
- thermodynamic erasure or entropy production;
- a fundamental temporal arrow;
- ontological becoming;
- phenomenal passage.

The BSC is an explicit readout/interface control, not a microscopic physical noise theory.

## Validation scope

The committed Stage 3F tests cover:

- access-policy validation;
- exact record-only baseline recovery;
- quarter-noise BSC information/decoder values;
- half-noise disappearance of accessible record contrast;
- monotone accessible-MI degradation with unchanged global true-register MI;
- redundant current-`X` control;
- `X`-only interface;
- masked-`X` posterior/compatible-history expansion;
- visible-`X` support control;
- complete-masking endpoint;
- view-coverage reconstruction control;
- invalid/zero-probability input guards.

The clean full-repository GitHub Actions result will be recorded once the final Stage 3F checkpoint head completes.

## Next

Stage 3G — robustness and synthesis.
