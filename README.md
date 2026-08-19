# t-search

`t-search` is a research workspace for exploring whether time can be understood as a perspective-invariant relational structure underlying both **block-like** and **becoming-like** descriptions.

## Research question

Can we construct explicit transformations between:

- a **block-like description** of a whole relational history, and
- **becoming-like descriptions** available from local/internal perspectives,

and identify non-trivial structures that remain stable across those transformations?

The long-term hypothesis is that such structures may be better candidates for the physical content of time than either "block" or "becoming" taken as an absolute description.

## Current status

**Stage 1 and Stage 2 are complete and merged. Stage 3.0 through Stage 3D are complete on `agent/stage-3-records`; Stage 3E — complete local view — is next.**

Integrated results:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

Stage 3 protocol and current results:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)
- [`docs/stage3a_notes.md`](docs/stage3a_notes.md)
- [`docs/stage3b_notes.md`](docs/stage3b_notes.md)
- [`docs/stage3c_notes.md`](docs/stage3c_notes.md)
- [`docs/stage3d_notes.md`](docs/stage3d_notes.md)
- [`results/stage3a_reversible_substrate.md`](results/stage3a_reversible_substrate.md)
- [`results/stage3b_record_diagnostics.md`](results/stage3b_record_diagnostics.md)
- [`results/stage3c_asymmetric_record.md`](results/stage3c_asymmetric_record.md)
- [`results/stage3d_controls.md`](results/stage3d_controls.md)

Latest Stage 3D clean PR merge-ref regression:

`137 passed in 3.11s`.

No strict physical invariant of time, no empirical discriminator between fixed-future and ontically-open-future interpretations, and no fundamental temporal arrow has yet been established.

## Stage 1 — Global/local reconstruction

Stage 1 established finite classical global/local reconstruction machinery and controlled information-loss/representation variants.

Main lessons include:

- reconstruction depends on the information interface and equivalence assumptions;
- coverage loss can move structure from reconstructible to ambiguous to lost;
- reachability/minimal-cover structure is more stable than arbitrary transitively redundant edge encodings;
- `state equality != event identity`;
- rich anonymous relational context can sometimes recover global structure up to isomorphism.

Stage 1 did not establish a fundamental physical invariant.

## Stage 2 — Potentiality

Protocol:

- [`docs/stage2_protocol.md`](docs/stage2_protocol.md)

Stage 2 separated global/local representation from epistemic/ontic Potentiality.

Core comparison:

`M_E = (T,h*,q_E)`

versus:

`M_O(D) = (D,Ext_T(D),K)`.

Under matched positive-support conditions, formally different models can share the same ontology-neutral operational description:

`O(G) = (A_now,Next(D),pi(next|D))`.

Supported conclusion:

**operationally indistinguishable under the tested interface and matched conditions**.

`operational equality != ontological equivalence`.

Detailed result:

- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)

## Stage 3 — Records and temporal direction

Stage 3 adds explicit record/memory/environment structure and tests whether record asymmetry selects an orientation beyond mere ordered change.

Protocol:

- [`docs/stage3_protocol.md`](docs/stage3_protocol.md)

Canonical reversible substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

The blank-memory boundary `M_0=0` is a special ensemble condition, not an irreversible law.

### Stage 3A — reversible substrate — completed

Verified full-space bijectivity/self-inverse behavior, exact forward/reversed trajectory ensembles, and:

`H(Z_0)=H(Z_1)=H(Z_2)=2 bits`.

Result:

- [`results/stage3a_reversible_substrate.md`](results/stage3a_reversible_substrate.md)

### Stage 3B — record diagnostics — completed

Implemented exact Shannon entropy, mutual information, conditional entropy, Bayes-optimal decoding, record/accessibility profiles, and signed scores.

Canonical diagnostics:

`I(M_1;X_0)=1`, `I(M_1;X_2)=0`, `A_R=1 bit`, `A_Acc=1/2`.

These remain neutral-side diagnostics rather than a physical past/future assignment.

Result:

- [`results/stage3b_record_diagnostics.md`](results/stage3b_record_diagnostics.md)

### Stage 3C — asymmetric-record model — completed

A conservative interpretation layer recognizes a **record-defined orientation** only when the MI and decoder signed diagnostics are both nonzero, agree in sign, and the selected side carries nonzero MI.

Canonical result:

`orientation=lower-index`, `record_defined=True`, while microscopic maps remain reversible.

`record-defined orientation != fundamental temporal arrow`.

Result:

- [`results/stage3c_asymmetric_record.md`](results/stage3c_asymmetric_record.md)

### Stage 3D — reversal and symmetric controls — completed

The required controls behave as follows:

| Ensemble | `A_R` | `A_Acc` | Orientation |
|---|---:|---:|---|
| canonical forward | `+1` | `+0.5` | `lower-index` |
| exact reversed | `-1` | `-0.5` | `upper-index` |
| 50/50 forward+reverse | `0` | `0` | `none` |
| no-record / identity first map | `0` | `0` | `none` |
| independent uniform initial memory | `0` | `0` | `none` |

The symmetric mixture is especially informative: it retains equal nonzero MI (`≈0.188721875541` bit on each side) and equal decoder accuracy (`0.75`) while the signed bias cancels.

Supported toy-model conclusion:

**the tested orientation is not a consequence of mere order or microscopic irreversibility; within this construction it tracks record coupling plus asymmetric boundary preparation and reverses covariantly under modeled history reversal.**

This is not a fundamental physical arrow, thermodynamic arrow, empirical time-reversal violation, ontological becoming, or phenomenal passage.

Result:

- [`results/stage3d_controls.md`](results/stage3d_controls.md)

### Stage 3E — next

Stage 3E will define the explicit record-bearing local view and global-to-local projection:

`G_k^rec=(Records_k,Actuality_k)`

and then upgrade toward:

`G_k=(Records_k,Actuality_k,Potentiality_k)`.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`random sampling != evidence of ontic becoming`

`formal representational difference != empirical physical difference`

`operational equality != ontological equivalence`

`order != arrow`

`microdynamical reversibility != record symmetry`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

A successful software construction is not by itself an ontological result.

## Fixed questions for every stage

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from the global to the local description?
4. Is that transformation reversible? If not, what information is discarded?
5. What is strictly invariant, what is only reconstructible, and what is locally accessible?
6. What physical meaning, if any, can be assigned to the surviving structures?

Failure to find an invariant, arrow, or operational discriminator is a valid research result rather than something to hide.
