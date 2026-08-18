# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial structures that remain stable across those transformations?

## Stage 0 — Definitions and scope — completed

Goal: define working meanings for `block`, `becoming`, `Actuality`, `Potentiality`, `record`, `perspective`, `transformation`, and `invariant`.

Exit criterion: satisfied.

## Stage 0.5 — Stage 1 protocol freeze — completed

Key decisions:

- distinguish event identity from state/configuration value;
- distinguish direct adjacency from induced reachability;
- keep Stage 1 free of Potentiality and records;
- specify the information interface of every local view;
- distinguish strict invariants, reconstructible properties, and local observables;
- enforce `simulation order != modeled temporal order`.

Exit criterion: satisfied.

## Stage 1 — Minimal classical graph model — completed and merged

Integrated result:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

Stage 1 established the finite classical global/local reconstruction machinery and six controlled information-loss/representation variants.

Main findings:

- reconstruction depends on the information interface and equivalence assumptions;
- coverage loss can produce reconstructible, ambiguous, or lost structure;
- reachability/minimal cover structure survives redundant-edge encoding changes better than arbitrary direct-edge lists;
- `state equality != event identity`;
- shared global IDs are sufficient but not always necessary;
- sufficiently rich anonymous relational context can reconstruct the canonical six-event graph up to isomorphism in the tested search class.

No fundamental physical invariant was claimed.

## Stage 2.0 — Potentiality protocol freeze — completed

Detailed specification:

- [`stage2_protocol.md`](stage2_protocol.md)

Stage 2 separates two conceptual axes:

- global versus local representation;
- epistemic versus ontic Potentiality.

Canonical neutral substrate:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`

`D_0 = (p,n)`.

The two continuations are not mere relabelings because their future relational path lengths differ.

## Stage 2A — Common branching substrate — completed

Implemented:

- finite rooted branching structure `T`;
- maximal histories `H` derived from `E,C`;
- valid actual prefixes `D`;
- `Ext_T(D)`;
- immediate next-event sets;
- prefix extension and terminal behavior;
- history/continuation equivalence up to event renaming;
- rooted branching-structure equivalence;
- optional state-label-preserving equivalence.

Result:

- [`../results/stage2a_branching.md`](../results/stage2a_branching.md)

## Stage 2B — Epistemic-history model — completed

Implemented:

`M_E=(T,h*,q_E)`.

The selected complete history `h*` exists globally but is intentionally hidden by the local projection:

`F_E^D: M_E -> G_E(D)`.

Changing only `h*` while holding current evidence and beliefs fixed does not change the local view.

Thus `F_E^D` is deliberately non-injective with respect to `h*`.

Result:

- [`../results/stage2b_epistemic.md`](../results/stage2b_epistemic.md)

Interpretive limit:

`a hidden selected future can be represented != physical reality has a fixed future`.

## Stage 2C — Ontic-extension model — completed

Implemented:

`M_O(D)=(D,Ext_T(D),K)`.

The model stores current Actuality, all structurally admissible extensions, and weights, but no selected complete future field.

Updates extend Actuality, prune incompatible extensions, and renormalize weights without creating a hidden future selector.

Result:

- [`../results/stage2c_ontic.md`](../results/stage2c_ontic.md)

Interpretive limit:

`a model with no selected future != evidence that physical reality is ontically open`.

## Stage 2D — Operational equivalence — completed

Introduced the ontology-neutral interface:

`O(G)=(A_now,Next(D),pi(next|D))`.

With matched baseline weights:

`O(G_E(D_0)) = O(G_O(D_0))`.

Both expose:

- Actuality `(p,n)`;
- Next `{l1,r1}`;
- probabilities `1/2,1/2`.

Thus the supported result is:

**operationally indistinguishable under the tested interface and matched conditions**.

Result:

- [`../results/stage2d_operational_equivalence.md`](../results/stage2d_operational_equivalence.md)

Interpretive limit:

`operational equality != ontological equivalence`.

## Stage 2E — Update comparison — completed

The same explicit observation `l1` was applied to both model families using their different update rules.

After update both operationalize to:

- Actuality `(p,n,l1)`;
- Next `{l2}`;
- `pi(l2)=1`.

Therefore:

`O(G_E(D_1)) = O(G_O(D_1))`.

The same operational equality persists through the terminal `l2` update, while the internal distinction remains:

- epistemic `h*` was already present and remains unchanged;
- ontic selected complete future remains absent from the state schema.

Result:

- [`../results/stage2e_update_comparison.md`](../results/stage2e_update_comparison.md)

## Stage 2F — Controls and synthesis — completed

Controls:

- pure event-renaming covariance / isomorphism;
- repeated state labels;
- matched non-uniform positive weights;
- mismatched positive-support weights;
- zero-support boundary semantics;
- terminal and invalid-input cases.

Key findings:

1. pure bookkeeping renaming preserves the relevant structures covariantly;
2. repeated state values do not collapse distinct events or the canonical continuation classes;
3. operational equality does not depend on uniform `1/2,1/2` weights — matched positive `0.75/0.25` also works;
4. mismatched probabilities break operational equality without constituting an ontological discriminator;
5. matching numerical `{1,0}` weights can still produce different `Next` sets because `EPot` removes zero-support hypotheses while `OPot=Ext_T(D)` retains structurally admissible zero-weight extensions;
6. the zero-support result is a **support-semantics boundary**, not a physical prediction.

Results:

- [`../results/stage2f_controls.md`](../results/stage2f_controls.md)
- [`../results/stage2_synthesis.md`](../results/stage2_synthesis.md)

Full clean regression was added through GitHub Actions and passed:

`99 passed in 2.98s`.

### Stage 2 strongest conclusions

- a hidden-selected-future model and a no-selected-future model can be formally different while producing the same tested local operational outputs under matched positive-support conditions;
- the difference between **hidden information** and **information absent from the model state** can be represented explicitly;
- operational equality can persist through matched updates;
- the equality is conditional on the chosen interface, probability matching, and support conventions;
- event labels are bookkeeping under the tested renaming control;
- state equality remains distinct from event identity;
- no strict physical invariant and no empirical fixed-vs-open-future discriminator has yet been established.

Stage 2 exit criterion: **satisfied pending PR #3 review/merge**.

## Stage 3 — Records and temporal direction — next after Stage 2 merge

Add explicit memory/environment/record structure and upgrade the minimal modal view toward:

`G = (Records,Actuality,Potentiality)`.

Required comparisons:

1. symmetric/reversible record control;
2. asymmetric-record model;
3. forward/reverse history comparison;
4. distinction among mere order, record asymmetry, and experienced temporal direction;
5. information-theoretic diagnostics only where the model makes them meaningful.

Goal:

Test, rather than assume, whether asymmetric records add an arrow-like structure beyond mere state change or branching order.

## Stage 4 — Finite Page–Wootters-style quantum model

Use a finite-dimensional clock `C` and system `S`.

Global/block-like representation:

`|Psi> = sum_t |t>_C |psi_t>_S`.

Relational/becoming-like representation:

`|psi_S(t)> proportional to <t|_C Psi>`.

Test conditional dynamics and preserved correlations/transition probabilities.

## Stage 5 — Change of clock / perspective

Use at least three subsystems and construct explicit changes between clock-relative descriptions.

Search for structures stable under:

1. block -> becoming;
2. becoming(clock C) -> becoming(clock A).

This is the first planned stage where a genuinely physical perspective-change candidate can be tested rather than mere bookkeeping renaming.

## Stage 6 — Candidate temporal structure T

Compare structures surviving Stages 1–5.

Possible ingredients include:

- causal/conditioning order;
- relational correlations;
- record accessibility;
- allowed-transition structure;
- consistency constraints among perspectives.

Do not force a unique invariant if the evidence supports a family of complementary structures.

## Stage 7 — Generally covariant / gravitational extension

Only after the toy models are stable.

Possible progression:

1. parametrized particle;
2. simple constrained/minisuperspace model;
3. tractable gravitational setting.

Question: does the candidate temporal structure survive when external time and preferred slicing are removed?

## Stage 8 — Empirical relevance (only if warranted)

Only seek empirical tests after deriving a genuinely discriminating prediction not guaranteed by the underlying standard formalism.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is the transformation reversible; what information is discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to surviving structures?

## Cross-cutting methodological cautions

- `simulation order != modeled temporal order`;
- `random sampling != evidence of ontic becoming`;
- successful software construction != ontological proof;
- global mathematical description != physically realizable God's-eye observer;
- reconstructible structure != automatically fundamental physical structure;
- compatible alternatives != automatically ontic possibilities;
- formal/internal distinguishability != automatically local/operational distinguishability;
- operational equality != ontological equivalence;
- support semantics must be distinguished from physical possibility.

## Stop / revise conditions

Revise the program rather than forcing progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is merely notation-dependent;
- local descriptions cannot be consistently related in the intended toy model;
- the supposedly ontic model secretly stores a selected complete future;
- the epistemic `h*` has no genuine formal role;
- an apparent operational distinction is produced only by assigning different numerical parameters or conventions;
- a claimed novelty is already an established object under another name.
