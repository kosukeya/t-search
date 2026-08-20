# t-search

`t-search` is a research workspace for exploring whether time can be understood through explicit transformations between **block-like/global** and **becoming-like/local** descriptions, with careful separation between invariance, reconstructibility, accessibility, operational equivalence, and interpretation.

## Research question

Can block-like and becoming-like descriptions be related explicitly, and can any non-trivial relational structure survive those transformations well enough to count as a candidate ingredient of physical time?

## Current status

**Stages 1--4 are complete and merged. Stage 5.0 — change-of-clock protocol freeze — is complete on `agent/stage-5-clock-change`; Draft PR #6 tracks Stage 5 and Stage 5A is next.**

Integrated syntheses:

- [`results/stage1_synthesis.md`](results/stage1_synthesis.md)
- [`results/stage2_synthesis.md`](results/stage2_synthesis.md)
- [`results/stage3_synthesis.md`](results/stage3_synthesis.md)
- [`results/stage4_synthesis.md`](results/stage4_synthesis.md)

Stage 5 protocol:

- [`docs/stage5_protocol.md`](docs/stage5_protocol.md)

Stage 5.0 protocol-only clean PR merge-ref regression:

`255 passed in 4.53s`.

No strict fundamental invariant of time, empirical discriminator between fixed/open-future interpretations, thermodynamic arrow, phenomenal passage, or fundamental quantum-time ontology has been established.

## Stage 1 — Global/local reconstruction

Stage 1 established finite classical global/local reconstruction machinery and information-loss controls. Reconstruction depends on the declared interface and equivalence assumptions; coverage loss can move structure from reconstructible to ambiguous to lost; state equality does not imply event identity; and relational structure can sometimes be recovered up to isomorphism.

## Stage 2 — Potentiality

Stage 2 separated global/local representation from epistemic/ontic Potentiality. Formally distinct hidden-selected-future and no-selected-future models can share tested operational outputs under matched positive-support conditions, so:

`operational equality != ontological equivalence`.

## Stage 3 — Records and temporal direction

Stage 3 tested whether record asymmetry can define an orientation beyond mere order while microscopic dynamics remain reversible. Controls showed that the record-defined orientation reverses under modeled history reversal, cancels under orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible while remaining globally represented.

This remains a candidate relational/information-accessibility component of temporal direction, not a fundamental physical arrow.

## Stage 4 — Finite Page--Wootters-style quantum model — completed and merged

Stage 4 implemented a finite constrained quantum model in which:

- global physical states satisfy a zero constraint and are stationary under its generator;
- ideal DFT clock conditioning yields exact clock-relative unitary dynamics;
- unrestricted kinematic conditioning is lossy while physical-support reduction is isometric/invertible;
- explicit local-to-local maps satisfy identity, inverse, and composition consistency;
- tested global/local conditional Born predictions agree;
- negative controls separate physical constraint, nontrivial ray change, and clock-basis quality.

Strongest Stage 4 candidate:

`perspective-consistent transition structure`.

Stage 4 did **not** change the physical clock subsystem itself.

## Stage 5 — Change of clock / perspective — in progress

Stage 5 is the first stage that changes which physical subsystem is used as the clock.

### Stage 5.0 — protocol freeze — completed

Canonical baseline:

`A`, `B`, `C` are qutrit subsystems with energy labels `{-1,0,+1}`.

`H_tot=H_A+H_B+H_C`.

The physical space is the seven-dimensional zero-sum sector:

`H_phys=ker(H_tot)`.

For each clock choice `X`, physical reduction maps onto a seven-dimensional constraint-compatible support:

`R_X(j): H_phys -> K_X`,

where `K_X` is embedded in the corresponding nine-dimensional rest tensor-product space.

The genuine cross-clock map is frozen as:

`S_{Y<-X}(k,j)=R_Y(k) E_X(j): K_X -> K_Y`.

The decisive Stage 5 consistency condition is:

`S_{Z<-Y}(l,k) S_{Y<-X}(k,j)=S_{Z<-X}(l,j)`.

The protocol also requires states **and observables** to transform together for operational comparisons, rejects full-rest-space unitarity when only support-space isometry exists, and does not identify equal numeric readings with one absolute event.

Reserved robustness controls include:

- symmetric `d=5`;
- subsystem permutation covariance;
- asymmetric qutrit clock rates `(lambda_A,lambda_B,lambda_C)=(1,1,2)`.

### Stage 5A — next

Implement only the symmetric three-qutrit constrained substrate: subsystem Hamiltonians, total constraint, analytic seven-state physical basis, numerical kernel verification, and all three finite DFT clock bases. Cross-clock reductions and frame changes remain deferred until Stage 5B/C.

## Key methodological guards

`compatible global completions != ontic future possibilities`

`state equality != event identity`

`simulation order != modeled temporal order`

`operational equality != ontological equivalence`

`order != arrow`

`record asymmetry != phenomenal passage`

`inaccessible information != ontologically absent information`

`history-state encoding != physical Page--Wootters state`

`kinematic projection != physical reduction`

`physical-subspace reversibility != unrestricted kinematic reversibility`

`common clock-origin shift != physical clock change`

`bookkeeping covariance != physical clock-choice invariance`

`clock reading change != physical clock subsystem change`

`equal numerical clock readings != same physical event`

`support-subspace isometry != full-rest-space unitarity`

`state transformation without observable transformation != operational frame covariance`

`perspective-dependent entanglement != inconsistent physics`

`cross-clock composition consistency != fundamental temporal ontology`

A successful software construction is not by itself an ontological result.

## Fixed questions

Every stage ends by asking:

1. What is the block-like/global description `B`?
2. What is the becoming-like/local description `G` or `V`?
3. What is the transformation from global to local?
4. Is that transformation reversible, and what is hidden/discarded?
5. What is invariant, reconstructible, ambiguous, lost, perspective-dependent, or operationally preserved?
6. What physical meaning, if any, can be assigned to the surviving structures?
