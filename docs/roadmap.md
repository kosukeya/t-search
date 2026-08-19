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

Stage 2 separated global/local representation from epistemic/ontic Potentiality.

Core formal comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

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
- forward and reverse dynamical validity;
- modeled history reversal `J(z0,z1,z2)=(z2,z1,z0)`;
- exact full-state probability-mass preservation;
- full-state entropy profile `(2,2,2)` bits.

Interpretive limit:

**Stage 3A establishes a reversible substrate only. It does not establish a record relation or temporal orientation.**

Focused Stage 3A tests: **10**.

## Stage 3B — Record diagnostics — completed

Results:

- [`../results/stage3b_record_diagnostics.md`](../results/stage3b_record_diagnostics.md)

Design notes:

- [`stage3b_notes.md`](stage3b_notes.md)

Implemented exact finite-ensemble diagnostics in a module separate from the Stage 3A dynamics:

- marginal and joint distributions;
- Shannon entropy;
- mutual information;
- conditional entropy;
- Bayes-optimal decoding/accessibility accuracy;
- record profile `Q_R(k,j)=I(R_k;X_j)`;
- accessibility profile;
- signed record score `A_R(k,Delta)`;
- signed accessibility score `A_Acc(k,Delta)`.

Canonical Stage 3 measurements at neutral position `k=1` are:

- `I(M_1;X_0)=1` bit;
- `I(M_1;X_2)=0` bit;
- `Acc(M_1->X_0)=1`;
- `Acc(M_1->X_2)=1/2`;
- `A_R=1` bit;
- `A_Acc=1/2`.

These are diagnostic outputs under neutral index labels. Stage 3B does not rename the lower-index side “past” and does not promote the signed contrast to a physical temporal arrow.

Focused Stage 3B tests: **11**.

Stage 3B clean PR merge-ref regression:

`120 passed`.

## Stage 3C — Asymmetric-record model — completed

Result:

- [`../results/stage3c_asymmetric_record.md`](../results/stage3c_asymmetric_record.md)

Design notes:

- [`stage3c_notes.md`](stage3c_notes.md)

Stage 3C adds no new arrow metric. It introduces a conservative interpretation criterion over the Stage 3B outputs.

A **record-defined orientation** is assigned only when:

1. `A_R` is nonzero;
2. `A_Acc` is nonzero;
3. the two signed diagnostics select the same neutral side;
4. the selected side carries nonzero mutual information with the current record register.

Canonical assessment:

- `I(M_1;X_0)=1` bit;
- `I(M_1;X_2)=0` bit;
- `Acc(M_1->X_0)=1`;
- `Acc(M_1->X_2)=1/2`;
- `A_R=1` bit;
- `A_Acc=1/2`;
- `orientation=lower-index`;
- `record_defined=True`;
- microscopic maps remain reversible.

Strongest supported conclusion:

**the canonical reversible blank-memory ensemble contains a record-defined orientation toward the lower-index side under the declared information/accessibility interface.**

Stage 3C does not yet establish that the blank-memory boundary causes, uniquely determines, or is necessary for this orientation. That isolation is deferred to Stage 3D.

Focused Stage 3C tests: **8 committed tests**.

Still forbidden:

`record-defined orientation == fundamental temporal arrow`.

## Stage 3D — Reversal and symmetric controls — next

Test:

- exact history reversal sign flip;
- equal forward/reverse mixture cancellation;
- order-only/no-record control;
- independent uniform-memory boundary control.

Goal: distinguish mere order, reversible dynamics, and asymmetric record-boundary preparation. Stage 3D is the first checkpoint allowed to make a stronger claim about whether the Stage 3C orientation depends on the special record boundary.

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
