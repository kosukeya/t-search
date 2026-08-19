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

Stage 1 established the finite classical global/local reconstruction machinery and controlled information-loss/representation variants.

No fundamental physical invariant was claimed.

## Stage 2 — Potentiality — completed and merged

Protocol:

- [`stage2_protocol.md`](stage2_protocol.md)

Integrated result:

- [`../results/stage2_synthesis.md`](../results/stage2_synthesis.md)

Stage 2 separated:

- global versus local representation;
- epistemic versus ontic Potentiality.

Core formal comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

Strongest result:

A hidden-selected-future model and a no-selected-future model can be formally different while producing the same tested local operational outputs under matched positive-support conditions.

The difference between **hidden information** and **information absent from the model state** was represented explicitly.

Full clean regression before merge:

`99 passed`.

Stage 2 exit criterion: **satisfied; PR #3 merged**.

No strict physical invariant and no empirical fixed-vs-open-future discriminator was established.

## Stage 3.0 — Records and temporal direction protocol freeze — completed

Detailed specification:

- [`stage3_protocol.md`](stage3_protocol.md)

Stage 3 separates four notions:

1. ordered structure;
2. microscopic reversibility;
3. record asymmetry;
4. experienced temporal direction.

None is identified with another by definition.

Principal guards:

`order != arrow`

`microdynamical reversibility != record symmetry`

`correlation != causation`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

`simulation order != modeled temporal order`.

Canonical reversible substrate:

`Z=(X,M,N) in {0,1}^3`

with:

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Canonical boundary ensemble:

- `X_0=a`;
- `M_0=0`;
- `N_0=b`;
- `a,b` independent uniform bits.

Record diagnostics are deliberately deferred until the reversible substrate is validated.

## Stage 3A — Reversible record substrate — completed

Result:

- [`../results/stage3a_reversible_substrate.md`](../results/stage3a_reversible_substrate.md)

Design notes:

- [`stage3a_notes.md`](stage3a_notes.md)

Implemented and verified:

- complete three-bit `Microstate` representation;
- exact enumeration of all eight complete microstates;
- `U_rec` and `U_scr` as bijections over the full state space;
- self-inverse behavior of both maps;
- rejection of a non-bijective erasure-map control when reversibility is claimed;
- exact canonical four-state boundary distribution using rational weights;
- four equiprobable complete forward trajectories;
- forward dynamical validity;
- modeled history reversal `J(z0,z1,z2)=(z2,z1,z0)`;
- reverse dynamical validity using inverse maps in reverse order;
- involutive trajectory and ensemble reversal;
- exact full-state probability-mass preservation;
- full-state entropy profile `(2,2,2)` bits for the canonical forward ensemble;
- corresponding entropy preservation in the reversed ensemble.

Interpretive limit:

**Stage 3A establishes a reversible substrate only. It does not establish a record relation or temporal orientation.**

The blank-memory condition `M_0=0` is carried forward as a declared boundary condition but is not interpreted as an arrow until Stage 3C after Stage 3B defines the diagnostics.

Focused Stage 3A tests: **10 committed tests**.

Draft tracking PR: **#4**.

## Stage 3B — Record diagnostics — next

Implement exact finite-distribution diagnostics:

- Shannon entropy for derived variables;
- mutual information;
- conditional entropy;
- Bayes-optimal decoding/accessibility accuracy;
- record profile `Q_R(k,j)=I(R_k;X_j)`;
- signed record score `A_R(k,Delta)`;
- signed accessibility score `A_Acc(k,Delta)`.

The diagnostics must not call lower indices “past.” Stage 3B defines measurement machinery only; the canonical asymmetric-record interpretation is reserved for Stage 3C.

## Stage 3C — Asymmetric-record model

Use the blank-memory boundary and test whether a record-defined orientation appears.

Canonical expected comparison:

`A_R=I(M_1;X_0)-I(M_1;X_2)`.

Strongest allowed positive conclusion: a **record-defined orientation** in the declared ensemble.

## Stage 3D — Reversal and symmetric controls

Test:

- exact history reversal sign flip;
- equal forward/reverse mixture cancellation;
- order-only/no-record control;
- independent uniform-memory boundary control.

Goal: distinguish order, reversible dynamics, and record-boundary asymmetry.

## Stage 3E — Complete local view

Upgrade toward:

`G_k=(Records_k,Actuality_k,Potentiality_k)`

and define explicit global-to-local projections.

## Stage 3F — Accessibility and information controls

Compare information and reconstructibility on both sides of the current position; add noise only after the exact baseline is established.

## Stage 3G — Robustness and synthesis

Run relabeling/state/boundary/noise controls, integrate Stage 2 epistemic/ontic Potentiality only if identifiable, run full regression, and produce:

- `results/stage3_synthesis.md`.

### Stage 3 exit criterion

Stage 3 is complete only if the protocol’s reversible dynamics, record diagnostics, reversal/symmetric controls, no-record and boundary controls, entropy distinctions, full `Records+Actuality+Potentiality` view, projection/information classification, regression, and six fixed questions are all completed without turning a record-defined orientation into metaphysical proof.

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
- support semantics must be distinguished from physical possibility;
- `order != arrow`;
- `microdynamical reversibility != record symmetry`;
- `record asymmetry != phenomenal passage`.

## Stop / revise conditions

Revise the program rather than forcing progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is merely notation-dependent;
- a Stage 3 arrow score merely restates the chosen event indices;
- an alleged record is only a single-trajectory value coincidence;
- a supposedly reversible update is not bijective;
- symmetric controls retain an unexplained signed bias;
- global entropy changes under an allegedly closed bijective update because of an implementation error;
- a claimed physical arrow is only a boundary-condition or support convention relabeled as physics;
- a claimed novelty is already an established object under another name.
