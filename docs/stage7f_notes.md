# Stage 7F Notes — Ablation / Reconstruction / Mismatch Matrix

Status: **scientific implementation complete; documentation-head regression pending.**

Stage 7F asks a narrower question than Stage 7G synthesis:

> when memory, record coupling, internal history anchoring, explicit perspective edges, event correspondence, or local record access is neutralized one at a time, which Stage 7 roles are preserved, reconstructible, inaccessible, lost, or not established?

The purpose is functional minimality inside the declared finite model family. It is not a metaphysical irreducibility test.

## Frozen role vocabulary

Stage 7F tracks six roles:

- `target_specific_record` — a positive target-memory record relation;
- `record_defined_direction` — the signed lower-vs-upper record orientation;
- `local_record_readout` — usable local record information through the declared interface;
- `perspective_transport` — admissible cross-clock transport;
- `P_R_covariance` — compatibility of transported perspectives and record semantics;
- `internal_history_anchor` — internally modeled `e0<e1<e2` event anchoring.

Statuses:

- `preserved` — directly represented after neutralization;
- `reconstructible` — explicit ingredient absent but role recovered from retained declared structure;
- `inaccessible` — global role retained but local interface cannot access it;
- `lost` — baseline role removed in the declared ablation with no reconstruction witness;
- `not_established` — retained structure does not license a verdict.

Guards:

- `lost != metaphysically irreducible`;
- `reconstructible != universally redundant`;
- `not_established != false`.

## Ablation matrix

| Neutralized ingredient | Main role consequence | Stage 7F status |
| --- | --- | --- |
| memory record carrier `M` | target record / direction / local record readout disappear | `lost` |
| record coupling | internally anchored no-record family retains P/O while R disappears | `lost` for R roles |
| internal history anchor | Stage 7B target-specific record survives but directional semantics do not | correlation `preserved`, direction `not_established`, anchor `lost` |
| explicit cross-clock edge matrices | maps rebuilt from retained reductions as `C_Y @ inv(C_X)` | `reconstructible` |
| event correspondence `chi` | local P and R remain, cross-perspective P-R comparison lacks event typing | `P_R_covariance = not_established` |
| hidden local memory access | global R remains, local record readout unavailable | `inaccessible` |
| maximally noisy local access | global R remains, local record readout carries no usable information | `inaccessible` |

## 1. Memory removal

The Stage 7D A/e1 lower/upper joint record distributions are collapsed over the memory variable, representing removal of `M` from the retained record carrier rather than merely hiding its local output.

Baseline:

- lower-event target-memory information: `1 bit`;
- upper-event target-memory information: `0`.

After removing the memory variable:

- lower information: `0`;
- upper information: `0`;
- `A_R=0`;
- `A_acc=0`;
- orientation `none`.

The A/B/C clock carrier remains independently available. Therefore record loss is not treated as loss of the perspective layer.

This is deliberately different from Stage 7E hidden access: hidden access retains the global memory-record relation, whereas memory removal removes the memory endpoint from the retained record representation.

## 2. Record-coupling neutralization: the central P+O-without-R countermodel

The Stage 7C `no-record` family retains:

- the internally anchored `e0<e1<e2` construction;
- all nine clock/readout nodes;
- rank-14 reduction coordinates;
- 54 distinct-clock comparison cases;
- state transport;
- inverse consistency;
- induced-metric covariance.

All tested residuals remain within `1e-9`.

At the same time:

- `record_defined = false`;
- `A_R=0`;
- `A_acc=0`.

Hence, in the declared Stage 7 model family:

`P + internal O retained` **does not imply** `R`.

This is a finite-model counterexample to reconstructing the Stage 7 record-defined role from the retained perspective structure plus internal event anchoring alone.

It is not a theorem that P/O can never generate records in another physical model.

## 3. Removing the internal history anchor

Stage 7B is reused as the controlled anchor-ablation witness.

It still has:

- explicit target `Q`;
- explicit computational memory readout;
- `I(Q;M)=1 bit` after the reversible record write;
- a positive target-specific record witness.

But Stage 7B deliberately has:

`directional_score_defined = false`.

Therefore:

- target-specific correlation survives;
- local target-record readout survives;
- record-defined temporal direction is `not_established`;
- the internal history-anchor role is `lost`.

This makes executable the distinction:

`target-specific record correlation != record-defined direction`.

## 4. Removing explicit perspective edge matrices

The explicit Stage 7D cross-clock edge matrix is withheld while retaining the common physical carrier and per-node reduction coordinates `C_X`.

For all 54 directed distinct-clock/readout comparisons Stage 7F rebuilds:

`S_reconstructed = C_Y @ inv(C_X)`.

The rebuilt maps agree with the Stage 7D reference maps and satisfy state transport, inverse consistency, induced-metric covariance, record-score covariance, and accessibility-score covariance within `1e-9`.

Therefore the **explicit edge matrix representation** is `reconstructible` in the current interface.

This does **not** remove the perspective layer itself. The reconstruction uses the retained common physical carrier and per-perspective reductions; those are still P-relevant structure.

Guard:

`explicit perspective-map reconstruction != elimination of the perspective layer`.

## 5. Removing event correspondence chi

With local perspectives, records, readouts, and the internal history retained, a single-perspective record orientation remains defined.

However, if `chi` is withheld, the cross-perspective statement “this lower/upper event corresponds to that lower/upper event” is not typed.

Stage 7F therefore classifies:

`P_R_covariance = not_established`

rather than `false`.

This preserves the protocol guard:

`missing chi != false covariance`.

## 6. Local-access ablations

The Stage 7E hidden and maximally noisy channels are reclassified under the common Stage 7F status evaluator.

Both cases retain:

- global target-specific record representation;
- global lower-index record direction;
- perspective transport;
- global P-R covariance;
- the internal history anchor.

But local record information is zero, so:

`local_record_readout = inaccessible`.

This distinguishes `inaccessible` from both `lost` and `not_established`.

## 7. Mismatch matrix

Stage 7F retains two discriminating mismatch controls rather than treating every failure as an ablation.

### Wrong / misdeclared chi

Comparing the preserving source interpretation with an event-swapped `chi` falsely declared preserving yields:

- record-score residual `2`;
- accessibility-score residual `1`;
- source orientation `lower-index`;
- wrong orientation `upper-index`.

The mismatch affects the declared `P_R_covariance` relation; it does not delete P or R themselves.

### Perturbed local perspective edge

The Stage 7E `C/e1 -> B/e0` perturbation remains localized:

- map residual nonzero;
- state residual nonzero;
- induced-metric covariance residual nonzero;
- record-score residual nonzero (`~0.0350432330` in the Stage 7E diagnostic);
- the two unaffected indirect paths remain consistent;
- tested projector-algebra similarity can remain at numerical zero.

Thus:

`observable-algebra correspondence != full state/metric path consistency`.

## 8. Stage 7F structural consequence

The strongest new bounded result is:

> **Within the declared Stage 7 finite constrained family, retaining the tested multi-clock perspective structure and the internally anchored neutral event order is insufficient to reconstruct the record-defined role when record coupling is neutralized. Conversely, explicit cross-clock edge matrices are reconstructible from the retained common physical carrier and per-perspective reductions.**

This strengthens the Stage 6/7 hypothesis that `R` is a separate represented role connected to P/O by compatibility conditions, while refining what is primitive inside `P`: the explicit edge matrices need not be primitive once the common carrier plus reductions are retained.

It does not establish that R is metaphysically fundamental or universally irreducible, nor that P is universally redundant.

## Validation

Stage 7F adds **12 focused tests**.

Implementation-inclusive PR merge-ref regression:

`548 passed in 146.97s`.

Final documentation-head regression remains to be recorded after protocol / roadmap / README synchronization.

## Next

Stage 7G — synthesis and evidence-selected Stage 8 gate.
