# Stage 8A Notes — Common Quantum-Extension Substrate

Status: **completed for the declared canonical finite continuation family**.

## Question

Can the shared Stage 7 constrained quantum carrier support a nontrivial executable extension set `QExt(e1)` whose members agree on the same declared current quantum Actuality through `e1` and differ only beyond the current anchor, without defining the future distinction through the memory-record variable itself?

Stage 8A answers this substrate question only. It does not yet implement epistemic selected-continuation or ontic no-selected-continuation semantics.

## Canonical current Actuality

The current anchor is the internally modeled A-clock event:

`e1`.

Both canonical continuations share the same cumulative schedule through the current anchor:

- `V0 = I`;
- `V1 = U_rec`.

Thus both contain the same Stage 7 target-specific record at `e1` and the same constrained reduced physical state through `e1`.

The executable diagnostics give:

- `||psi_L(e0)-psi_R(e0)|| <= 1e-10`;
- `||psi_L(e1)-psi_R(e1)|| <= 1e-10`;
- current target-memory information is `I(Q;M)=1 bit` in both continuations.

The canonical record target remains the Stage 7 B-energy predicate. The continuation difference is not defined by changing this target or by changing memory.

## Canonical continuation family

The canonical extension set is:

`QExt(e1) = {h_L, h_R}`.

### h_L

Future completion:

`V2^L = U_rec`.

### h_R

Future completion:

`V2^R = Z_C U_rec`,

where `Z_C` is a reversible phase operation that multiplies the A-clock rest-pair sector with `C energy label == +1` by `-1` and acts as `+1` otherwise.

`Z_C` acts as identity on the memory qubit.

It also commutes with the B-based Stage 7 record-target projector.

Therefore the canonical future distinction is:

- memory neutral;
- record-target neutral;
- physically nontrivial on B/C pair coherence.

This is deliberately chosen so Stage 8 does not define `V` from `R` at baseline.

## Constrained embedding

Each continuation defines its own internally clock-conditioned dressing:

`W_h = sum_j |t_j><t_j|_A tensor V_j^h`.

The corresponding constrained completion is:

`H_h = W_h H_0 W_h^dagger`.

The continuation-specific physical basis is derived from that dressing:

`B_phys^h = W_h B_phys^(7A)`.

For both canonical continuations:

- physical dimension = `14`;
- constraint residual is within `1e-10`;
- all nine A/B/C clock/readout reductions have rank `14`.

Thus both continuations remain physically admissible in the declared finite constrained construction and preserve a full-rank multi-clock description.

## Executable future inequivalence

The two continuations do not merely carry different labels.

For the canonical source state:

- future-operator Frobenius residual = `4`;
- squared overlap of normalized `e2` reduced states = `0`;
- Euclidean distance of normalized `e2` reduced states = `sqrt(2)`;
- a pair-coherence probe that is identity on memory distinguishes the two future states.

Hence `h_L` and `h_R` belong to different continuation-equivalence classes under the declared Stage 8A diagnostics.

Frozen guard:

`future physical inequivalence != modal semantics by itself`.

## Renaming control

A renamed copy of `h_L` with a different `continuation_id` but the same physical schedule is classified as physically equivalent to `h_L`.

Adding:

`h_L_renamed`

to `{h_L,h_R}` still yields two equivalence classes after deduplication.

Therefore:

`different continuation labels != physically different continuations`.

## Invalid-current-prefix control

A candidate continuation with `V1=I` rather than the declared current `V1=U_rec` does not share the frozen current Actuality.

It fails the current-prefix compatibility audit and is rejected from `QExt(e1)`.

Thus Stage 8A does not manufacture alternatives by changing what was already declared actual.

## Terminal behavior

For the canonical three-event family:

`QExt(e2) = empty`.

No further event beyond `e2` is represented in this baseline.

This is a declared finite-model terminal convention, not a claim about physical time ending after three events.

## What Stage 8A establishes

Within the declared finite carrier, Stage 8A establishes an executable common quantum-extension substrate with at least two physically inequivalent future completions sharing one current constrained Actuality.

It therefore removes one important integration-failure possibility from Stage 8.0: Stage 8 no longer relies only on attaching Stage 2 branch metadata beside the Stage 7 model.

However, Stage 8A does **not** yet establish:

- `EPot_Q`;
- `OPot_Q`;
- a hidden selected continuation;
- absence of a selected continuation in an ontic-extension model;
- operational underdetermination between the two modal semantics;
- genuine P-V covariance across clock changes;
- V independence from P/O/R;
- ontic openness of the real future.

`QExt represented != ontically real futures by definition`.

## Exit-criteria checkpoint

Stage 8A satisfies criteria **11–16** in the declared canonical continuation family:

11. two physically inequivalent continuations share one current Actuality;
12. inequivalence is executable rather than label-only;
13. renaming does not create another continuation class;
14. retained continuations are physically admissible;
15. current-incompatible continuation is rejected;
16. terminal-current behavior is explicit.

Criteria 17–50 remain future work.

## Validation

Stage 8A adds 13 focused tests.

Implementation-inclusive regression after pinning the canonical numerical diagnostics:

`581 passed in 193.93s`.

## Next

Stage 8B should place two type-distinct modal semantics on this **same** `QExt(e1)` substrate:

- an epistemic model containing one hidden selected continuation `h*`;
- an ontic-extension model containing `{h_L,h_R}` but no selected continuation or equivalent hidden selector.
