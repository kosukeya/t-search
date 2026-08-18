# Stage 2 Protocol — Potentiality

Status: **protocol frozen before implementation**.

Stage 2 begins only after the Stage 1 classical reconstruction checkpoint is merged. Its purpose is to introduce Potentiality as an explicit model structure while keeping epistemic uncertainty separate from ontic non-preselection.

This document is a specification. Code written for Stage 2 should follow it unless a later experiment exposes a contradiction or an important ambiguity; any revision must be documented rather than silently changing the semantics.

## 1. Stage 2 question

Stage 1 showed that the same incomplete relational data can be compatible with multiple global completions. Stage 2 asks a different question:

> Can two models share the same branching possibilities and the same local operational predictions while differing in whether one complete future history is already selected inside the formal object?

The comparison is deliberately between:

1. an **epistemic-history model**, in which a complete history is selected but locally hidden;
2. an **ontic-extension model**, in which the current actuality and admissible extensions are represented but no complete future history is preselected.

The target is to locate the formal difference precisely and test whether the chosen local observables distinguish it.

## 2. Non-goals

Stage 2 does **not** establish that:

- physical reality is ontically open;
- eternalism is true because a complete hidden history can be represented;
- becoming is true because a model can omit a selected future;
- random sampling in Python is physical actualization;
- epistemic probability and ontic chance are physically identical because they can share numbers;
- compatible completions produced by missing information are automatically ontic possibilities;
- the Stage 2 branching structure is already a realistic spacetime, relativistic, gravitational, or quantum model.

The principal methodological guards are:

`compatible completions != ontic possibilities`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

## 3. Separate the two axes

Do not identify:

`epistemic model == block`

or:

`ontic model == becoming`.

Stage 2 treats these as separate conceptual axes:

- **global/local representation** — how much of the structure is represented in one description;
- **epistemic/ontic Potentiality** — whether one complete future is already selected in the model state.

This prevents the desired metaphysical conclusion from being inserted by definition.

## 4. Shared branching substrate

Both models use the same finite branching law / possibility structure `T`.

For the baseline, `T` is a rooted finite DAG that is in fact a tree.

Let:

`T = (E, C, H)`

where:

- `E` is the event set;
- `C` is the direct oriented edge relation;
- `H` is the set of complete maximal root-to-leaf histories admitted by `T`.

A history is an ordered event path consistent with `C`.

A current actual structure `D` is a valid prefix of at least one history in `H`.

Write:

`D <= h`

when `D` is a prefix of history `h`.

Define the compatible/admissible extension set:

`Ext_T(D) = {h in H | D <= h}`.

Event identity remains distinct from state value. If a state map is later added:

`s: E -> Sigma`

then:

`state equality != event identity`.

## 5. Canonical Stage 2 branching structure

The baseline substrate is deliberately asymmetric so that the two complete continuations are not merely left/right relabelings.

Use:

`E = {p, n, l1, l2, r1}`

and:

`C = {(p,n), (n,l1), (l1,l2), (n,r1)}`.

Diagram:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

The complete histories are:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`.

The baseline current actual prefix is:

`D_0 = (p,n)`.

Therefore:

`Ext_T(D_0) = {h_L, h_R}`.

The two histories are relationally distinguishable because their future branch structures have different lengths. Their distinction therefore does not depend only on the event names `l*` versus `r*`.

## 6. Equivalence of histories and worlds

Do not count mere event renaming as a distinct possible world.

Two branching structures or histories are equivalent when related by the relevant rooted directed-graph isomorphism while preserving any physical/state labels explicitly declared by the protocol.

Event identifiers are bookkeeping labels unless a later experiment explicitly gives them physical meaning.

Potentiality sets should therefore be interpreted as equivalence classes of genuinely distinct continuations, not raw renamed copies.

The canonical `h_L` and `h_R` are intentionally non-equivalent under this criterion.

## 7. Actuality

At Stage 2, current Actuality is represented by the actual prefix:

`A_now = D_now`.

Use the whole prefix, not only its terminal state/event. This avoids collapsing repeated states that occur at different relational positions.

The tip/current event may be derived from the prefix:

`tip(D_now)`.

Stage 2 does not yet add inherited record semantics. Records enter Stage 3.

## 8. Two typed notions of Potentiality

The same mathematical carrier set can play two different model roles. The implementation must keep these roles type-distinct.

### 8.1 Epistemic Potentiality

For current prefix `D`, define:

`EPot(D) = {h in H | D <= h and q_E(h | D) > 0}`.

Its interpretation is:

> hypotheses about which already-selected complete history is actual.

One member is in fact `h*`, but the local perspective does not know which one.

### 8.2 Ontic-extension Potentiality

Define:

`OPot(D) = Ext_T(D)`

with admissibility/transition weights `K` where needed.

Its interpretation is:

> continuations allowed from the current actual structure, with no complete actual continuation selected inside the model state.

The implementation should use distinct classes or wrappers for epistemic versus ontic Potentiality even when their event/history contents are numerically identical.

## 9. Epistemic-history model

The global epistemic object is:

`M_E = (T, h*, q_E)`

where:

- `T` is the branching substrate;
- `h* in H` is one complete actual history selected in advance;
- `q_E` is the local observer/model's epistemic distribution over complete histories.

For the deterministic baseline fixture, use:

`h* = h_L`.

At `D_0`, use:

`q_E(h_L | D_0) = 1/2`

`q_E(h_R | D_0) = 1/2`.

These probabilities represent uncertainty about the hidden selected history. They are not generated by reading `h*`.

The current prefix is a perspective/evidence parameter supplied to the local projection. It should not reveal the future portion of `h*`.

A privileged global diagnostic may inspect `h*` for tests, for example to verify that a hidden selected future exists. Such a diagnostic is **not** a local observable.

## 10. Ontic-extension model

The ontic model state is:

`M_O(D) = (D, Ext_T(D), K)`

where:

- `D` is the current actual prefix;
- `Ext_T(D)` is the set of admissible complete extensions;
- `K` supplies admissibility/transition weights where probabilities are used.

Critical structural requirement:

**There must be no field, hidden selector, seed-derived variable, or equivalent state that singles out one complete future history before update.**

The branching law `T` may be available as background structure used to derive admissible extensions. Representing all allowed possibilities is not the same as representing one of them as already actual.

At `D_0`, choose weights so that the immediate next alternatives match the epistemic predictive distribution:

`K(l1 | D_0) = 1/2`

`K(r1 | D_0) = 1/2`.

These weights are interpreted as admissibility/chance weights inside the ontic model, not uncertainty about a hidden `h*`.

## 11. Stage 2 becoming-like local views

Stage 2 upgrades the Stage 1 structural local view into a minimal modal becoming-like description, but still without records.

Define separate typed views:

`G_E(D) = (A_now, EPot(D), pi_E(next | D))`

and:

`G_O(D) = (A_now, OPot(D), pi_O(next | D))`.

Here:

- `A_now = D` is current Actuality;
- the Potentiality field carries epistemic hypotheses or ontic extensions, respectively;
- `pi(next | D)` is the induced immediate-next predictive distribution.

This is still not the final Stage 3 form:

`G = (Records, Actuality, Potentiality)`.

Stage 2 supplies only the `Actuality + Potentiality` layer.

## 12. Projection maps

Define:

`F_E^D: M_E -> G_E(D)`

and:

`F_O: M_O(D) -> G_O(D)`.

### 12.1 Epistemic projection rule

`F_E^D` must intentionally hide `h*`.

Changing the hidden selected history from `h_L` to `h_R`, while keeping `T`, `D`, and the epistemic distribution the same, must not change the local operational output before discriminating evidence arrives.

### 12.2 Ontic projection rule

`F_O` exposes the current Actuality and admissible Potentiality but cannot expose a selected complete future because no such datum exists in `M_O`.

The distinction to preserve is:

`hidden information` versus `information absent from the model state`.

## 13. Operational observable interface

To compare the two models without cheating by inspecting their Python types or hidden fields, define an ontology-neutral operational erasure/interface:

`O(G) = (A_now, Next(D), pi(next | D))`.

`Next(D)` is the set of inequivalent immediate next alternatives induced by the live Potentiality set.

For the baseline at `D_0`, require:

`O(G_E(D_0)) = O(G_O(D_0))`.

Numerically:

`Next(D_0) = {l1, r1}`

and:

`pi(l1 | D_0) = pi(r1 | D_0) = 1/2`.

This equality is an intentionally constructed control. It tests whether a formal ontological distinction can remain operationally invisible under the selected observables.

## 14. Epistemic predictive probabilities

For epistemic Potentiality, the immediate-next probability is obtained by marginalizing the belief distribution over live complete histories:

`pi_E(x | D) = sum_{h in EPot(D), next_D(h)=x} q_E(h | D)`.

The hidden `h*` must not be consulted when computing this local predictive distribution.

This permits two epistemic models with different hidden selected histories to produce the same current local prediction when the observer has the same evidence.

## 15. Ontic transition/admissibility probabilities

For ontic Potentiality, use:

`pi_O(x | D) = K(x | D)`

or an equivalent normalized marginal over admissible extensions.

For the baseline control, choose `K` so that:

`pi_O(x | D_0) = pi_E(x | D_0)`.

Numerical equality does not erase the semantic distinction:

- `q_E` = uncertainty about a hidden selected history;
- `K` = weight over not-yet-selected admissible continuations in the model.

## 16. Update / actualization rules

Stage 2 must distinguish the model update semantics after an observed next event `x`.

No random sampling is required for the baseline experiment. The test should provide the observed next event explicitly.

### 16.1 Epistemic update

Given evidence/observation `x`:

1. extend the current evidence prefix from `D` to `D' = D + x`;
2. keep the global hidden `h*` unchanged;
3. condition `q_E` on histories compatible with `D'`;
4. remove incompatible epistemic hypotheses from `EPot(D')`.

For a baseline actual-run test with `h* = h_L`, use observation `l1`, which is consistent with the hidden actual history.

If a supplied "actual observation" contradicts `h*`, the implementation should reject the run as inconsistent rather than silently changing `h*`. A separate counterfactual-conditioning helper may be added later if useful.

### 16.2 Ontic update

Given observed next event `x`:

1. extend Actuality to `D' = D + x`;
2. replace `Ext_T(D)` with the subset compatible with `D'`;
3. renormalize `K` if needed;
4. continue to store no selected complete future beyond `D'`.

Thus the formal difference after update remains:

- epistemic: the complete `h*` was already present and remains unchanged;
- ontic: the actual prefix grows/updates while future extensions remain unselected.

## 17. Privileged structural diagnostics versus local observables

Stage 2 needs tests that prove the two model structures are genuinely different without pretending those diagnostics are physically accessible.

Allow privileged test-only diagnostics such as:

- epistemic: `selected_history(M_E) -> h*`;
- epistemic: `actual_next_from_hidden_history(M_E, D)`;
- ontic: assertion that no selected complete-history field exists.

These diagnostics must never be included in `O(G)`.

The experiment therefore separates:

`formal/internal distinguishability`

from:

`local/operational distinguishability`.

## 18. Reversibility and identifiability

The Stage 2 projections are expected to behave differently from the Stage 1A round trip.

### 18.1 Epistemic projection

`F_E^D` is intentionally non-injective with respect to `h*`.

Different hidden selected histories can map to the same current local view when evidence and beliefs are the same.

Therefore the local view does not generally reconstruct `h*`.

### 18.2 Ontic projection

There is no hidden `h*` to reconstruct.

If the local operational interface discards deeper extension structure, different ontic extension models may still map to the same operational view. That is ordinary projection loss and must not be described as a hidden preselected future.

The core distinction is therefore not simply "both maps lose information" but:

`epistemic: selected-future information exists globally and is hidden`

versus:

`ontic: no selected-future datum exists before update`.

## 19. Stage 2 experiment sequence

### Stage 2A — common branching substrate

Implement and validate:

- events and direct edges of canonical `T`;
- maximal histories `H`;
- prefix validation;
- `Ext_T(D)`;
- history/world equivalence rules;
- explicit proof in tests that `h_L` and `h_R` are not merely renamed copies.

### Stage 2B — epistemic-history model

Implement:

`M_E = (T, h*, q_E)`

and verify:

- `h*` exists globally;
- local projection hides `h*`;
- changing hidden `h*` alone does not alter the baseline operational view;
- epistemic hypotheses condition correctly after observation.

### Stage 2C — ontic-extension model

Implement:

`M_O(D) = (D, Ext_T(D), K)`

and verify:

- all admissible extensions are represented;
- no selected complete future exists in the state;
- update extends Actuality and prunes extensions without introducing a hidden future selector.

### Stage 2D — operational-equivalence experiment

With matched weights, compare:

`O(G_E(D_0))`

and:

`O(G_O(D_0))`.

Baseline expected result:

`operationally equal before discriminating evidence`.

If they are equal, report operational indistinguishability under this interface rather than treating it as proof of ontological equivalence.

### Stage 2E — update comparison

Provide a common observed next event, initially `l1`.

Compare:

- updated Actuality;
- updated Potentiality;
- next-event probabilities;
- privileged internal diagnostics.

Expected formal contrast:

- epistemic `h*` remains the already-selected complete history;
- ontic state contains only the now-longer actual prefix plus remaining extensions.

### Stage 2F — controls and synthesis

At minimum include:

1. event-renaming invariance / isomorphism control;
2. repeated state-label control so `state equality != event identity` remains enforced;
3. a weight-mismatch control showing that operational equivalence is not automatic if `q_E` and `K` are numerically different;
4. terminal-prefix behavior;
5. invalid-prefix / invalid-observation guards.

Then produce a Stage 2 synthesis report.

## 20. Required baseline assertions

The implementation should make the following statements executable as tests.

1. `Ext_T(D_0) == {h_L, h_R}` up to the declared equivalence.
2. `h_L` and `h_R` are not equivalent by mere relabeling.
3. `M_E` contains one `h*`.
4. `M_O` contains no selected complete future.
5. With the same `D_0` and matched weights, the operational views are equal.
6. Replacing epistemic `h* = h_L` with `h* = h_R` alone does not change the pre-observation operational view.
7. After observing `l1`, both models agree on the updated actual prefix.
8. After observing `l1`, both models agree operationally on the remaining immediate continuation under the baseline law.
9. After the same update, privileged internal diagnostics still distinguish the model structures.
10. Changing only the numerical weights can change operational predictions, demonstrating that operational equality is a controlled condition rather than a theorem of epistemic/ontic semantics.

## 21. Property classification for Stage 2

Every result should distinguish at least:

- **local observable** — directly present in `O(G)`;
- **internal/formal property** — present in model structure but deliberately not locally exposed;
- **reconstructible property** — inferable from the allowed family of observations plus stated assumptions;
- **ambiguous property** — multiple non-equivalent assignments remain possible;
- **lost property** — not recoverable under the interface;
- **strict invariant** — reserved for genuine reversible representation transformations.

Do not call numerical agreement of two operational interfaces a strict physical invariant by default.

## 22. Physical-interpretation discipline

The strongest allowed Stage 2 conclusions are of the form:

- the epistemic and ontic models are formally different;
- a selected complete history is globally present in one formalism and absent in the other;
- the chosen local operational interface can or cannot distinguish them;
- update rules encode different internal semantics while perhaps preserving the same current predictions.

Do not infer from these toy-model facts that physical reality chooses one ontology.

If the models are operationally indistinguishable, the correct conclusion is:

`operationally indistinguishable under the tested observables`.

If they become distinguishable only because different probability kernels are assigned, the result concerns those kernels, not the metaphysical interpretation by itself.

## 23. Stage 2 deliverables

Planned implementation artifacts:

- `src/t_search/stage2.py` or a small set of clearly separated Stage 2 modules;
- `experiments/stage2a_branching.py`;
- `experiments/stage2b_epistemic.py`;
- `experiments/stage2c_ontic.py`;
- `experiments/stage2d_operational_equivalence.py`;
- `experiments/stage2e_update.py`;
- Stage 2 tests mirroring each experiment;
- result Markdown files for each major experiment;
- `results/stage2_synthesis.md`.

Implementation may split modules more finely if this improves semantic separation, especially between epistemic and ontic types.

## 24. Stage 2 exit criteria

Stage 2 is complete only when all of the following are satisfied.

1. The shared branching substrate and history-equivalence rule are explicit and tested.
2. Epistemic and ontic Potentiality are implemented as semantically/type-distinct structures.
3. The epistemic model contains an explicit preselected `h*` that is hidden from local operational projection.
4. The ontic model contains no hidden or implicit selected complete future before update.
5. `F_E`, `F_O`, and the ontology-neutral operational interface `O` are explicit.
6. Baseline matched-weight operational equivalence is tested rather than assumed.
7. Update rules are implemented and compared after at least one common observation.
8. Event renaming and repeated-state controls preserve the Stage 1 identity lessons.
9. Results classify local, internal, reconstructible, ambiguous, lost, and candidate surviving structures without overusing `invariant`.
10. The six fixed project questions can be answered for Stage 2 without conflating formal representation with physical ontology.
11. A synthesis report states whether any operational discriminator arose and what assumptions produced it.

## 25. Stop / revise conditions

Revise this protocol before continuing if implementation reveals that:

- the supposedly ontic model secretly encodes a selected complete future;
- the epistemic `h*` has no formal role even in privileged/global semantics;
- the two baseline alternatives differ only by arbitrary event names;
- operational equality is obtained by accidentally exposing different interfaces;
- `Potentiality` becomes definitionally circular with `Actuality`;
- probability semantics are silently changed between experiments;
- an apparent ontic/epistemic distinction is merely a serialization or class-name difference with no model-semantic consequence;
- a claimed empirical distinction is actually produced only by assigning different numerical parameters.

## 26. Fixed questions at the Stage 2 protocol level

These are provisional answers to be tested by implementation.

1. **Block-like/global descriptions:** epistemic `M_E = (T,h*,q_E)`; ontic modal state `M_O(D) = (D,Ext_T(D),K)`.
2. **Becoming-like/local descriptions:** typed `G_E(D)` and `G_O(D)` carrying current Actuality, Potentiality, and immediate predictive weights.
3. **Transformations:** `F_E^D` and `F_O`, followed by ontology-neutral operational erasure `O`.
4. **Reversibility:** `F_E^D` is intentionally non-injective in `h*`; `F_O` has no hidden `h*` to recover and may still lose deeper extension information under operational projection.
5. **Candidate surviving structure:** current actual prefix, admissible-next relational structure, and matched next-event probabilities may survive the epistemic/ontic representation change under the baseline interface; this must be tested rather than called a physical invariant in advance.
6. **Physical meaning:** undecided at protocol freeze. Stage 2 can establish formal and operational facts about the toy models, not the ontology of physical time.
