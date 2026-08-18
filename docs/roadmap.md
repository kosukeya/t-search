# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial invariants across those transformations?

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

Stage 1A verified the information-rich round trip:

`B_1 -> {V_e} -> B_1_hat`.

Stage 1B completed six controlled variants:

1. outgoing-only;
2. incoming-only;
3. missing local views;
4. reachability-only;
5. state-label collision;
6. anonymous / global-ID-free views.

Main findings:
- reconstruction depends on the information interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability/minimal cover structure survives transitively redundant edge-encoding changes better than arbitrary edge lists;
- `state equality != event identity`;
- shared global IDs are sufficient but not always necessary for reconstruction;
- sufficiently rich anonymous relational context can recover the canonical graph up to isomorphism in the tested six-event search class.

Stage 1 does not establish a fundamental physical invariant.

## Stage 2.0 — Potentiality protocol freeze — completed

Detailed specification:

- [`stage2_protocol.md`](stage2_protocol.md)

Stage 2 separates two axes:

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

The two formal model families are:

### Epistemic-history model

`M_E = (T,h*,q_E)`

A complete `h*` is globally selected, while the local projection intentionally hides it.

### Ontic-extension model

`M_O(D) = (D,Ext_T(D),K)`

Current Actuality and all admissible extensions are represented, with no selected complete future stored in the model state.

Core guards:

`compatible completions != ontic possibilities`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`.

## Stage 2A — Common branching substrate — completed

Result:

- [`../results/stage2a_branching.md`](../results/stage2a_branching.md)

Implemented:
- finite rooted branching structure `T`;
- maximal histories `H` derived from `E,C`;
- valid actual prefixes `D`;
- `Ext_T(D)`;
- immediate next-event sets;
- neutral prefix extension and terminal behavior;
- history/continuation equivalence up to event renaming;
- rooted branching-structure equivalence;
- invalid-prefix and invalid-tree guards.

For `D_0`:

`Ext_T(D_0)={h_L,h_R}`

`Next(D_0)={l1,r1}`.

The two continuation classes are genuinely non-equivalent because their future path structures differ.

Focused validation: `8 passed`.

Interpretive limit:

`branching structure != evidence of ontic openness`.

## Stage 2B — Epistemic-history model — completed

Result:

- [`../results/stage2b_epistemic.md`](../results/stage2b_epistemic.md)

Implemented:

`M_E=(T,h*,q_E)`.

Baseline:
- hidden `h*=h_L`;
- `q_E(h_L)=q_E(h_R)=1/2`;
- `EPot(D_0)={h_L,h_R}`;
- `pi_E(l1)=pi_E(r1)=1/2`.

Changing only hidden `h*` from `h_L` to `h_R` leaves the local projection exactly unchanged, while privileged diagnostics distinguish the global states.

Thus:

`F_E^D` is intentionally non-injective with respect to `h*`.

After observation `l1`, beliefs condition to the left history but `h*` remains unchanged. An actual observation contradicting `h*` is rejected instead of rewriting the selected history.

Focused validation: `10 passed`.

Interpretive limit:

`a hidden selected future can be represented != physical reality has a fixed future`.

## Stage 2C — Ontic-extension model — completed

Result:

- [`../results/stage2c_ontic.md`](../results/stage2c_ontic.md)

Implemented:

`M_O(D)=(D,Ext_T(D),K)`.

The model state contains:
- the neutral branching substrate;
- current Actuality/prefix;
- typed `OnticPotentiality` containing exactly all live extensions;
- normalized extension weights.

It contains no selected complete future field such as `selected_history` or `hidden_history`.

At `D_0`:

`OPot(D_0)={h_L,h_R}`

and:

`pi_O(l1)=pi_O(r1)=1/2`.

After explicit observation `l1`:
- Actuality extends to `(p,n,l1)`;
- the incompatible right extension is removed;
- the left extension receives normalized weight `1`;
- the immediate-next prediction becomes `l2` with probability `1`;
- no selected complete future is created.

As a formal contrast with Stage 2B, the same unselected baseline can also accept observation `r1` when that branch has positive weight. Stage 2B's actual-run fixture with hidden `h*=h_L` rejects `r1`.

Validation limitation:
- a focused semantic harness passed `10 Stage 2C semantic checks`;
- the committed Stage 2C tests must be included in a later full repository regression before merge review.

Interpretive limit:

`a model with no selected future != evidence that physical reality is ontically open`.

## Stage 2D — Operational equivalence — completed

Result:

- [`../results/stage2d_operational_equivalence.md`](../results/stage2d_operational_equivalence.md)

Stage 2D introduces the ontology-neutral operational interface:

`O(G) = (A_now, Next(D), pi(next|D))`.

The typed local descriptions remain formally distinct, but their semantic Potentiality tags and privileged internal fields are erased before comparison.

For the matched baseline:

`O(G_E(D_0)) = O(G_O(D_0))`

with:
- the same Actuality `(p,n)`;
- the same immediate alternatives `{l1,r1}`;
- the same probabilities `1/2,1/2`.

Therefore the supported conclusion is:

**operationally indistinguishable under the tested observables and matched baseline weights**.

Additional controls:
- swapping only hidden epistemic `h*` remains operationally invisible;
- changing only `q_E` or `K` keeps Actuality/Next fixed while breaking probability equality.

A focused Stage 2D semantic harness passed `8/8 checks`. Full repository regression remains required before Stage 2 merge review.

Interpretive limit:

`operational equality != ontological equivalence`.

## Stage 2E — Update comparison — completed

Result:

- [`../results/stage2e_update_comparison.md`](../results/stage2e_update_comparison.md)

Design notes:

- [`stage2e_notes.md`](stage2e_notes.md)

A common explicit observation:

`l1`

is supplied to both model families.

The epistemic model:
- changes evidence prefix to `(p,n,l1)`;
- conditions beliefs to `h_L`;
- leaves the globally selected `h*=h_L` unchanged.

The ontic model:
- extends Actuality to `(p,n,l1)`;
- removes the incompatible right extension;
- renormalizes the left extension to weight `1`;
- creates no selected complete future field.

After these distinct updates:

`O(G_E(D_1)) = O(G_O(D_1))`

with:
- Actuality `(p,n,l1)`;
- Next `{l2}`;
- `pi(l2)=1`.

Thus the matched operational equality survives the common left-branch update while the internal semantic distinction persists.

A second common observation `l2` reaches the same terminal operational view in both models, again with epistemic `h*` preserved and no ontic future selector created.

The canonical ontic baseline can accept `r1`, while the specific epistemic fixture with `h*=h_L` rejects it. This is a formal distinction between two fixed global states, not yet an empirical family-level discriminator because an epistemic model with `h*=h_R` can represent a right-branch run.

Validation:
- the committed Stage 2E test file contains `9` focused tests;
- a compact Stage 2A–E semantic reconstruction passed `9/9 checks`;
- full repository regression remains mandatory before merge review.

Interpretive limit:

`post-update operational equality != ontological equality`.

## Stage 2F — Controls and synthesis — next

Required work:
- event-renaming / isomorphism invariance;
- repeated state labels, preserving `state equality != event identity`;
- consolidate and expand weight-mismatch controls;
- terminal prefixes and invalid prefixes/observations;
- classify local/internal/reconstructible/ambiguous/lost structure across Stage 2;
- answer the six fixed questions at Stage 2 resolution;
- produce `results/stage2_synthesis.md`;
- run full repository regression on a clean/current branch checkout;
- perform Stage 2 exit review before changing PR #3 from draft or merging.

Stage 2 exit criterion: the formal difference, projection maps, update semantics, operational comparison, controls, and limitations can all be stated explicitly without turning representational differences into metaphysical proof.

## Stage 3 — Records and temporal direction

Add memory/environment registers and compare asymmetric-record models with symmetric/reversible controls.

Goal: distinguish mere ordering from temporal direction and test whether asymmetric records provide an arrow-like structure.

## Stage 4 — Finite Page–Wootters-style quantum model

Use a finite-dimensional clock `C` and system `S`.

Global/block-like representation:

`|Psi> = sum_t |t>_C |psi_t>_S`

Relational/becoming-like representation:

`|psi_S(t)> proportional to <t|_C Psi>`.

Test conditional dynamics and preserved correlations/transition probabilities.

## Stage 5 — Change of clock / perspective

Use at least three subsystems and construct explicit changes between clock-relative descriptions.

Search for structures stable under:
1. block -> becoming;
2. becoming(clock C) -> becoming(clock A).

## Stage 6 — Candidate temporal structure T

Compare structures surviving Stages 1–5. Possible ingredients include causal/conditioning order, relational correlations, record accessibility, allowed-transition structure, and perspective-consistency constraints.

Do not force a unique invariant if the evidence supports a family of complementary structures.

## Stage 7 — Generally covariant / gravitational extension

Only after the toy models are stable. Possible progression:
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
- formal/internal distinguishability != automatically local/operational distinguishability.

## Stop / revise conditions

Revise the program rather than forcing progress if:
- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is merely notation-dependent;
- local descriptions cannot be consistently related in the intended toy model;
- the supposedly ontic model secretly stores a selected complete future;
- the epistemic `h*` has no genuine formal role;
- an apparent operational distinction is produced only by assigning different numerical parameters;
- a claimed novelty is already an established object under another name.
