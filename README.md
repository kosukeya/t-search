# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations between **block-like/global** and **becoming-like/local** descriptions, with careful separation between strict invariance, reconstructibility, accessibility, and interpretation.

## Research question

Can block-like and becoming-like descriptions be related explicitly, and can any non-trivial relational structure survive those transformations well enough to count as a candidate ingredient of physical time?

## Current status

**Stage 1 and Stage 2 are complete and merged. Stage 3A--3G, synthesis, and full regression are complete on `agent/stage-3-records`; Draft PR #4 is intentionally left unmerged for checkpoint review.**

Integrated syntheses:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)
- [`results/stage3_synthesis.md`](results/stage3_synthesis.md)

Stage 3 protocol / closure:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)
- [`docs/stage3g_notes.md`](docs/stage3g_notes.md)
- [`results/stage3g_robustness.md`](results/stage3g_robustness.md)

Latest documentation-inclusive clean PR merge-ref regression before final checkpoint review:

`171 passed in 3.24s`.

No strict fundamental invariant of time, empirical discriminator between fixed/open-future interpretations, thermodynamic arrow, or phenomenal passage has been established.

## Stage 1 — Global/local reconstruction

Stage 1 established finite classical reconstruction machinery and information-loss controls.

Main lessons:

- reconstruction depends on the interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability/minimal-cover structure is more stable than transitively redundant edge encoding;
- `state equality != event identity`;
- rich anonymous relational context can sometimes recover structure up to isomorphism.

## Stage 2 — Potentiality

Stage 2 separated global/local representation from epistemic/ontic Potentiality.

Core comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

Under matched positive-support conditions, formally distinct models can share the same tested operational description:

`O(G)=(A_now,Next(D),pi(next|D))`.

Supported conclusion:

`operational equality != ontological equivalence`.

## Stage 3 — Records and temporal direction

Stage 3 asks whether record asymmetry can define an orientation beyond mere order while microscopic dynamics remain reversible.

Canonical finite substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both maps are bijective/self-inverse.

Canonical record diagnostics at neutral position 1:

`I(M_1;X_0)=1`

`I(M_1;X_2)=0`

`A_R=1`

`A_Acc=1/2`.

The resulting label is only a **record-defined orientation toward the lower-index side**; lower index is not definitionally called physical past.

### Main Stage 3 controls

The record-defined orientation:

- disappears when record coupling is removed despite ordered reversible change;
- flips under exact modeled history reversal;
- cancels under equal forward/reverse mixing while equal nonzero correlations remain;
- disappears for maximally uncertain independent initial memory;
- is robust to pure position naming and bijective bit-value relabeling;
- does not collapse when identical state values occur at different positions.

Stage 3G refines the boundary result. Let:

`p=P(M_0=0)`.

Then:

| `p` | `A_R` | `A_Acc` | orientation |
|---:|---:|---:|---|
| `1` | `1` | `0.5` | lower-index |
| `3/4` | `~0.188721875541` | `0.25` | lower-index |
| `1/2` | `0` | `0` | none |
| `1/4` | `~0.188721875541` | `0.25` | lower-index |
| `0` | `1` | `0.5` | lower-index |

So the literal convention `M_0=0` is not the robust ingredient. The relevant toy-model feature is **non-maximal uncertainty / nonuniform preparation of the memory boundary**.

### Global versus local information

Stage 3E defines:

`B_3=(Z_space,U_1,U_2,Omega,mu)`

and the reduced local Actuality:

`A_k^loc=(X_k,M_k)`.

The explicit projection:

`F_k:(B_3,omega)->G_{omega,k}^rec`

omits hidden `N_k`, opposite-side actual microstates, the complete trajectory as a direct field, and privileged boundary labels.

One exact central view can be ambiguous while a suitable family of exact views reconstructs the complete actual trajectory.

Stage 3F then degrades only the local readout. The global canonical relation can remain:

`I(true M_1;X_0)=1 bit`

while maximal readout noise gives:

`I(M_obs;X_0)=0`.

Therefore:

`inaccessible information != information absent from the formal global state`.

Stage 3G adds a second caution: the same accessible MI can arise from a genuinely weaker global boundary correlation or from local readout noise on a globally perfect record.

Thus:

`same local statistic != same global information structure`.

### Completing `G=(Records,Actuality,Potentiality)`

Stage 3E attaches the already-tested record layer to Stage 2 local Potentiality through explicit typed product adapters:

`G_E^complete=(Records,A_product,EPot,pi_E)`

`G_O^complete=(Records,A_product,OPot,pi_O)`.

Stage 3G rechecks that swapping hidden epistemic `h*` does not leak into the complete local view and that epistemic/ontic Potentiality types remain distinct.

This is formal modularity, not a proof that Stage 2 and Stage 3 describe one physical substrate.

## Strongest Stage 3 conclusion

Within this finite toy construction:

**ordered reversible dynamics can support a measurable record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

But the result is still boundary-, ensemble-, and interface-dependent. The canonical model also has the redundancy `X_1=X_0`, so explicit memory `M` is not the only carrier of lower-side information.

Therefore the result is a **candidate relational/information-accessibility component of temporal direction**, not a completed theory of physical time.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

`order != arrow`

`microdynamical reversibility != record symmetry`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

`inaccessible information != ontologically absent information`

`same local statistic != same global information structure`

A successful software construction is not by itself an ontological result.

## Fixed questions

Every stage ends by asking:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is that transformation reversible, and what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Stage 3 answers are in [`results/stage3_synthesis.md`](results/stage3_synthesis.md).
