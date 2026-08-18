# Stage 2 Synthesis — Potentiality

Status: **Stage 2 experiments and controls completed; exit criteria satisfied pending PR review/merge**.

## 1. Purpose

Stage 2 asked whether two formally different models of future possibility can share the same local operational description.

The distinction was deliberately defined without identifying:

`epistemic == block`

or:

`ontic == becoming`.

Instead Stage 2 kept two axes separate:

1. global/internal versus local/operational representation;
2. epistemic uncertainty versus ontic non-preselection of a future continuation.

The central formal comparison was:

`M_E = (T,h*,q_E)`

versus:

`M_O(D) = (D,Ext_T(D),K)`.

The principal question was not which ontology is true. It was:

> Can selected-future information exist globally and be hidden in one model, while being absent from the state of another model, yet both produce the same declared local observables?

Stage 2 answers **yes under controlled conditions**, while also identifying conditions under which the operational equality fails.

---

## 2. Shared neutral substrate

Both model families use the same finite rooted branching structure:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with complete histories:

`h_L = (p,n,l1,l2)`

and:

`h_R = (p,n,r1)`.

The baseline current prefix is:

`D_0 = (p,n)`.

Therefore:

`Ext_T(D_0) = {h_L,h_R}`

and:

`Next(D_0) = {l1,r1}`.

The two continuations are not merely left/right renamings. Their future relational path lengths differ, so they occupy two distinct continuation-isomorphism classes.

This substrate is ontology-neutral:

`branching structure != evidence of ontic openness`.

---

## 3. Stage 2A — common branching substrate

Stage 2A implemented:

- finite rooted branching structure `T`;
- maximal histories derived from the graph;
- valid non-empty current prefixes;
- `Ext_T(D)`;
- immediate next-event sets;
- prefix extension;
- terminal behavior;
- history/continuation equivalence up to event renaming;
- rooted branching-structure equivalence;
- optional preservation of state labels during equivalence checks.

The key result was that the neutral possibility structure can be specified before assigning either epistemic or ontic semantics.

This prevented the Stage 2 conclusion from being built into the substrate definition.

---

## 4. Stage 2B — epistemic-history model

The epistemic model is:

`M_E = (T,h*,q_E)`.

Its defining feature is that one complete history exists in the global model state:

`h* in H`.

For the canonical fixture:

`h* = h_L`.

At `D_0`, local belief is deliberately symmetric:

`q_E(h_L)=q_E(h_R)=1/2`.

The typed local view is:

`G_E(D) = (A_now,EPot(D),pi_E(next|D))`.

The epistemic projection:

`F_E^D: M_E -> G_E(D)`

intentionally does not expose or consult `h*` when generating the local prediction.

Two global states:

`M_E^L = (T,h_L,q_E)`

and:

`M_E^R = (T,h_R,q_E)`

produce the same pre-observation local view when `D` and `q_E` are the same.

Therefore:

`F_E^D(M_E^L) = F_E^D(M_E^R)`

while:

`M_E^L != M_E^R`.

Thus `F_E^D` is intentionally non-injective with respect to `h*`.

The formal content is:

`selected-future information exists globally and is locally hidden`.

This is not evidence that physical reality has a fixed future.

---

## 5. Stage 2C — ontic-extension model

The ontic-extension model is:

`M_O(D) = (D,Ext_T(D),K)`.

Its state contains:

- current Actuality/prefix `D`;
- every structurally admissible complete extension;
- normalized weights over those extensions.

The implementation contains no:

- `selected_history`;
- `hidden_history`;
- selected-future field of equivalent explicit role.

The typed local view is:

`G_O(D) = (A_now,OPot(D),pi_O(next|D))`.

The critical contrast with Stage 2B is therefore not simply that both models hide different fields.

It is:

`epistemic: selected-future information exists but is hidden`

versus:

`ontic: selected-future information is absent from the model state`.

The ontic update extends Actuality and prunes incompatible extensions without creating a selected complete future beyond the new prefix.

This is a formal model construction, not evidence that the physical future is ontically open.

---

## 6. Stage 2D — ontology-neutral operational interface

The typed local views are intentionally different objects:

`EpistemicPotentiality != OnticPotentiality`.

To compare local observations without cheating by inspecting model type or privileged fields, Stage 2D introduced:

`O(G) = (A_now,Next(D),pi(next|D))`.

For the matched baseline:

`q_E(h_L)=q_E(h_R)=1/2`

and:

`K(h_L)=K(h_R)=1/2`.

Then:

`O(G_E(D_0)) = O(G_O(D_0))`.

Both expose:

- Actuality `(p,n)`;
- immediate alternatives `{l1,r1}`;
- probabilities `1/2,1/2`.

The strongest justified statement is:

**operationally indistinguishable under the tested observables and matched baseline conditions**.

This is not ontological equivalence.

A hidden-`h*` swap remains invisible under `O`, confirming that the operational interface does not indirectly leak the selected epistemic history.

---

## 7. Stage 2E — update comparison

Both models were given the same explicit observation:

`l1`.

No random sampling was used as a surrogate for physical becoming.

### Epistemic update

Evidence changes:

`(p,n) -> (p,n,l1)`.

Beliefs condition to the left history:

`q_E(h_L)=1`

`q_E(h_R)=0`.

But:

`h*` remains unchanged.

### Ontic update

Actuality changes:

`(p,n) -> (p,n,l1)`.

The incompatible right extension is removed and surviving weights are renormalized.

No selected complete future field is created.

### Operational result

After update, both models expose:

- Actuality `(p,n,l1)`;
- `Next={l2}`;
- `pi(l2)=1`.

Therefore:

`O(G_E(D_1)) = O(G_O(D_1))`.

The same equality persists through the common terminal update `l2`.

Thus the canonical matched run demonstrates:

`different internal update semantics`

coexisting with:

`same tested operational trajectory`.

---

## 8. Stage 2F — controls

Stage 2F tested whether the preceding conclusions survive several changes.

### 8.1 Pure event renaming

The branching substrate, local operational descriptions, and common update relationship transform covariantly under a bijective event rename.

The correct relation is:

`rename(O(G)) = O(rename(G))`.

Raw string equality across renamed event IDs is not expected.

This establishes robustness to bookkeeping labels only. It is not yet a physical reference-frame invariance result.

### 8.2 Repeated state labels

Assigning the same state value to different events does not collapse event identity inside the Stage 2 model.

For example:

`state(l1)=state(r1)=X`.

Then event-level:

`Next(D_0)={l1,r1}`

still contains two alternatives, while a naive state projection becomes only:

`{X}`.

The canonical complete continuations also remain in two distinct relational equivalence classes.

Therefore Stage 2 preserves:

`state equality != event identity`.

### 8.3 Matched non-uniform positive weights

Using matched:

`0.75 / 0.25`

weights in both model families still gives operational equality.

Therefore the Stage 2D result is not specific to uniform `1/2 / 1/2` weights.

Under the current interface, matching **positive-support** predictions are the relevant condition.

### 8.4 Positive-support mismatch

If the two model families have the same Actuality and same supported immediate alternatives but different probabilities, then:

- Actuality equality survives;
- Next equality survives;
- probability equality fails;
- full operational equality fails.

This is a parameter distinction, not an ontological discriminator.

### 8.5 Zero-support boundary

A more interesting boundary appears when both numerical maps are:

`h_L:1`

`h_R:0`.

Epistemic Potentiality excludes zero-support hypotheses, so:

`Next_E={l1}`.

Ontic Potentiality is defined structurally as all admissible extensions even when one has zero `K`, so:

`Next_O={l1,r1}`

with zero weight on `r1`.

Therefore operational equality fails at this boundary under the current definition of `Next`.

This result limits the Stage 2D conclusion.

It does **not** demonstrate a physical difference between fixed and open futures. The distinction is produced by a declared support convention.

A later operational interface could instead remove zero-probability alternatives in both models, in which case this difference may disappear.

The correct classification is:

**support-semantics boundary**.

---

## 9. Information-preservation map

| Structure / datum | Epistemic global state | Epistemic local view | Ontic state | Ontic local view | Operational `O` |
|---|---:|---:|---:|---:|---:|
| current Actuality prefix | derivable/supplied | yes | yes | yes | yes |
| complete branching substrate `T` | yes | not generally | background/internal | not generally | no |
| selected complete `h*` | yes | no | absent | absent | absent |
| epistemic belief over histories | yes | represented through live Potentiality / marginals | n/a | n/a | only immediate marginal |
| ontic complete extensions | n/a | n/a | yes | yes | only immediate consequences |
| per-history extension weights | n/a | n/a | yes | reduced to next-event marginal | only immediate marginal |
| epistemic/ontic Potentiality semantics | internal | typed | internal | typed | erased |
| immediate next alternatives | derivable | yes | derivable | yes | yes |
| immediate next probabilities | derivable | yes | derivable | yes | yes |

This table shows that operational equality can coexist with substantial information loss.

---

## 10. Reversibility and identifiability

### 10.1 Epistemic projection

`F_E^D` is not reversible in general.

The clearest lost/hidden datum is `h*`:

`M_E^L != M_E^R`

but:

`F_E^D(M_E^L)=F_E^D(M_E^R)`

before discriminating evidence.

Therefore the local view cannot reconstruct which selected complete history is stored globally.

### 10.2 Ontic projection

There is no hidden selected future to recover.

However `F_O` is not generally information-complete either.

The local view keeps current Actuality, current complete live extensions, and immediate-next marginals, but it does not generally preserve:

- the full background substrate outside current live extensions after pruning;
- arbitrary distinctions in per-history weights that produce the same immediate marginal in more complex trees.

For the tiny canonical baseline some of this structure happens to be reconstructible from the complete live histories, but that is not a general reversibility theorem.

### 10.3 Operational erasure

`O` is deliberately many-to-one.

It removes:

- selected `h*`;
- Potentiality type/meaning;
- complete-extension interpretation;
- deeper distributional structure beyond the immediate marginal.

Thus:

`operational equality`

is expected to be weaker than:

`model-state equality`.

---

## 11. What is preserved across the Stage 2 comparison?

Under matched positive-support conditions, the strongest shared operational structures are:

1. current Actuality prefix;
2. immediate next alternatives, modulo bookkeeping renaming;
3. immediate-next predictive probabilities;
4. the common operational trajectory along the tested explicit left-branch updates.

The repeated-state control shows that these structures should remain event/relational rather than be reduced naively to state values.

The event-renaming control shows covariance under bookkeeping relabeling.

These are best called:

- shared operational structures;
- representation-stable/covariant structures under the tested transformations;
- candidate ingredients for later invariance tests.

They are **not yet strict physical invariants**.

---

## 12. What Stage 2 does not establish

Stage 2 does not establish:

- that the physical future is ontically open;
- that a global fixed future exists physically;
- that eternalism and becoming are physically equivalent;
- that operational indistinguishability under `O` implies ontological equivalence;
- that the zero-support distinction is an empirical prediction;
- that probability has the same interpretation in the two model families;
- that the Stage 2 tree is a realistic spacetime;
- that the shared operational structure is invariant under Lorentz transformations, general covariance, clock changes, or quantum reference frames;
- that records or an arrow of time have been modeled;
- that random sampling constitutes actual becoming;
- that a fundamental physical invariant of time has been found.

---

## 13. The six fixed questions at the end of Stage 2

### ① What is the block-like/global description `B`?

Stage 2 no longer has one single global object playing every role.

The explicitly complete-history model is:

`B_E := M_E = (T,h*,q_E)`.

It contains the whole branching law and one selected complete history.

The comparison partner is a different internal state:

`M_O(D)=(D,Ext_T(D),K)`.

It should not simply be renamed `B`, because Stage 2 intentionally separates global/local representation from epistemic/ontic Potentiality.

Thus the Stage 2 answer is plural:

- `M_E` is the clear block-like/global selected-history representation;
- `M_O(D)` is a modal internal state with current Actuality plus unselected extensions.

### ② What is the becoming-like/local description `G`?

Stage 2 introduces two typed minimal modal local views:

`G_E(D)=(A_now,EPot(D),pi_E)`

and:

`G_O(D)=(A_now,OPot(D),pi_O)`.

They contain Actuality + Potentiality but still no record structure.

For cross-model operational comparison:

`O(G)=(A_now,Next(D),pi(next|D))`.

This remains a proto-/minimal becoming-like description rather than the final Stage 3 `Records + Actuality + Potentiality` form.

### ③ What is the transformation `F`?

There are now two projection maps:

`F_E^D: M_E -> G_E(D)`

and:

`F_O: M_O(D) -> G_O(D)`.

Then both can be mapped through the ontology-neutral erasure:

`O: G -> OperationalView`.

The comparison diagram is therefore:

```text
M_E  --F_E-->  G_E  --O-->  O(G_E)

M_O  --F_O-->  G_O  --O-->  O(G_O)
```

### ④ Is `F` reversible?

Not in general.

For epistemic `F_E`, the answer is clearly **no** with respect to `h*`: different selected complete histories can produce the same local view.

For ontic `F_O`, there is no hidden `h*`, but projection can still discard background substrate information or detailed extension-weight information beyond what the local view retains.

The operational map `O` is even more strongly non-injective because it deliberately erases modal semantics and deeper structure.

### ⑤ What is preserved?

Under the tested matched positive-support conditions:

- current Actuality prefix;
- immediate next alternatives up to bookkeeping renaming;
- immediate-next predictive probabilities;
- the tested common operational update trajectory.

The branching/isomorphism controls also preserve relational distinctions even when state values repeat.

No non-trivial **strict physical invariant** is claimed.

### ⑥ Does the preserved structure have physical meaning?

Not yet established.

The strongest current interpretation is that:

`Actuality + immediate relational alternatives + transition probabilities`

form a compact operational structure shared by two different Stage 2 internal semantics under controlled conditions.

This makes them plausible **candidate ingredients** for a more physical relational account of time.

But their status is limited because:

- equality depends on the chosen operational interface;
- probability matching matters;
- support conventions can break equality;
- no realistic spacetime, records, quantum clocks, or reference-frame transformations have yet been tested.

Therefore:

`representation-stable operational structure != fundamental physical time`.

---

## 14. Strongest justified Stage 2 conclusions

1. **A hidden-selected-future model and a no-selected-future model can be formally distinct while sharing the same declared local operational outputs.**
2. **The distinction between hidden information and absent information can be implemented explicitly rather than left verbal.**
3. **Operational indistinguishability can persist through matched explicit updates, not only at one initial snapshot.**
4. **The equality is conditional, not automatic: probability mismatch breaks it.**
5. **Uniform probabilities are not essential: matched non-uniform positive weights still preserve equality.**
6. **Zero-support conventions expose a support-semantics boundary where operational equality can fail even with matching numerical weights.**
7. **Pure event renaming changes notation but preserves the relevant structure covariantly.**
8. **Repeated state values do not justify collapsing distinct events or relational histories.**
9. **No empirical discriminator between fixed-future and ontically-open-future model families has been established.**
10. **No strict physical invariant of time has yet been established.**

---

## 15. Stage 2 exit criteria

Stage 2 exit criteria are satisfied:

1. shared branching substrate and equivalence rules are explicit and tested — **satisfied**;
2. epistemic and ontic Potentiality are semantically and type-distinct — **satisfied**;
3. epistemic selected history exists globally and is hidden by local projection — **satisfied**;
4. ontic model contains no selected complete future field and updates without creating one — **satisfied**;
5. ontology-neutral operational interface is explicit — **satisfied**;
6. matched pre-observation operational equality is tested — **satisfied**;
7. update semantics and post-update comparison are explicit — **satisfied**;
8. renaming, repeated-state, weight, support, terminal, and invalid-input controls are tested — **satisfied**;
9. clean full-repository regression has run on GitHub Actions — **satisfied: 99 passed**;
10. limitations and the six fixed questions are explicitly documented — **satisfied**.

Final Stage 2 synthesis judgment:

`Stage 2 exit criteria: satisfied`.

The remaining repository-management step is PR #3 review/merge readiness assessment. Stage 2 should not be merged solely because this synthesis says the conceptual exit criteria are satisfied; the final PR diff and latest CI status should still be reviewed.

---

## 16. Carry-forward to Stage 3

Stage 2 supplied:

`Actuality + Potentiality`.

Stage 3 should add explicit records/memory/environment structure and ask a new question:

> Can temporal direction be distinguished from mere branching/order by asymmetric record accessibility?

The natural next representation is:

`G = (Records,Actuality,Potentiality)`.

Stage 3 should include at least:

- a symmetric/reversible record control;
- an asymmetric-record model;
- forward/reverse comparison;
- a clear distinction between ordering, record asymmetry, and experienced temporal direction.

The Stage 2 support-semantics boundary should also remain in view: future work should distinguish structural admissibility, positive probability, epistemic support, and operational accessibility rather than using one word "possible" for all four.
