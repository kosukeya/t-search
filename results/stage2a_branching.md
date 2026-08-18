# Stage 2A — Common Branching Substrate

Status: **completed**.

## Purpose

Stage 2A implements only the ontology-neutral branching substrate required by both later Stage 2 models. No epistemic-history or ontic-extension interpretation is introduced here.

The canonical structure is:

```text
           l1 -> l2
          /
p -> n
          \
           r1
```

with:

`E = {p,n,l1,l2,r1}`

`C = {(p,n),(n,l1),(l1,l2),(n,r1)}`.

The implementation stores `E`, `C`, and the root. The history set `H` is derived from those data rather than duplicated as independent mutable state.

## Observed baseline

The experiment reports:

```text
Stage 2A — common branching substrate
simulation order != modeled temporal order

events: 5
direct edges: 4
maximal histories: 2
current prefix: ('p', 'n')
tip: n
extensions: (('p', 'n', 'l1', 'l2'), ('p', 'n', 'r1'))
next events: ['l1', 'r1']
extension equivalence classes: 2
h_L equivalent to h_R by renaming: False
```

Thus the maximal histories are:

`h_L = (p,n,l1,l2)`

`h_R = (p,n,r1)`

and for:

`D_0 = (p,n)`

we obtain:

`Ext_T(D_0) = {h_L,h_R}`.

The immediate next-event set is:

`Next(D_0) = {l1,r1}`.

## Equivalence result

History and continuation equivalence deliberately ignores raw event identifiers unless physical/state labels are explicitly supplied.

The canonical alternatives are not equivalent by mere renaming because their continuation path lengths differ:

- left continuation: `n -> l1 -> l2`;
- right continuation: `n -> r1`.

Therefore the baseline contains **two genuinely distinct continuation classes**, not two copies generated only by the arbitrary labels `l*` and `r*`.

As a control, two unlabeled histories with the same path structure are treated as equivalent, and a fully renamed copy of the canonical branching substrate is rooted-graph isomorphic to the original.

## Prefix behavior

A valid current Actuality is a non-empty prefix of at least one maximal history.

For example:

`D_0 = (p,n)`

can extend to either branch.

After extending left:

`D_1 = (p,n,l1)`

only `h_L` remains compatible and:

`Next(D_1) = {l2}`.

At the terminal prefix:

`D_2 = (p,n,l1,l2)`

`Ext_T(D_2) = {h_L}`

and:

`Next(D_2) = empty`.

Invalid prefixes and inadmissible immediate extensions are rejected.

## Validation scope

Focused Stage 2A validation:

`8 passed`.

The tests cover:

1. canonical events, edges, root, and maximal histories;
2. `Ext_T(D_0)` and immediate next events;
3. two non-equivalent canonical continuation classes;
4. equivalence of same-shape histories under pure renaming;
5. rooted-structure renaming invariance;
6. prefix extension and terminal behavior;
7. invalid-prefix / invalid-next-event guards;
8. rejection of disconnected or non-tree baseline substrates.

## Interpretation

Stage 2A makes no claim about whether the two continuations are epistemic hypotheses or ontic possibilities. It establishes only the shared neutral carrier structure on which those two interpretations will later be implemented separately.

In particular:

`branching structure != evidence of ontic openness`.

The Stage 2.0 guards remain in force:

`compatible completions != ontic possibilities`

`simulation order != modeled temporal order`

`formal representational difference != empirical physical difference`.

## Next step

Stage 2B will implement the epistemic-history model:

`M_E = (T,h*,q_E)`

with an explicit selected complete history `h*` that exists globally but is intentionally hidden from the local projection.
