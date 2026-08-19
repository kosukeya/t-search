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

Controls established:

- event-renaming covariance;
- repeated state values do not collapse event identity;
- matched non-uniform positive weights can preserve operational equality;
- probability mismatches can break equality without supplying an ontological discriminator;
- zero-support semantics can expose representation-dependent differences in `Next`;
- terminal and invalid-input behavior is explicit.

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

### Canonical reversible substrate

Use the closed finite microstate:

`Z=(X,M,N) in {0,1}^3`

with reversible maps:

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both maps are self-inverse and must be verified as bijections over all eight complete microstates.

Canonical boundary ensemble:

- `X_0=a`;
- `M_0=0`;
- `N_0=b`;
- `a,b` independent uniform bits.

The blank register is a special boundary condition, not an irreversible law.

### Record diagnostic

At neutral ordered position `k`, define:

`Q_R(k,j)=I(R_k;X_j)`

and the signed directional contrast:

`A_R(k,Delta)=I(R_k;X_{k-Delta})-I(R_k;X_{k+Delta})`.

Canonical choice:

`A_R=I(M_1;X_0)-I(M_1;X_2)`.

Do not call lower indices “past” before this score selects an orientation.

Complementary accessibility score:

`A_Acc=Acc(R_k->X_{k-Delta})-Acc(R_k->X_{k+Delta})`.

### Required reversal/control behavior

History reversal:

`J(z_0,z_1,z_2)=(z_2,z_1,z_0)`.

Expected canonical transformation:

`A_R(J_*mu)=-A_R(mu)`.

Orientation-symmetric mixture:

`mu_sym=1/2 mu_fwd + 1/2 mu_rev`

should have no signed bias.

Required negative controls also include:

- same neutral order without record coupling;
- independent uniform initial memory instead of `M_0=0`;
- register/event renaming;
- repeated values;
- rejection of non-bijective updates when reversibility is claimed.

### Entropy guard

Because the complete dynamics are bijective:

`H(Z_0)=H(Z_1)=H(Z_2)`

must hold for the transported full-state distribution.

Subsystem entropies and mutual information may change. This is correlation/entropy redistribution, not automatically thermodynamic entropy production.

### Stage 3 sequence

#### Stage 3A — reversible record substrate — next

Implement and verify:

- three-bit microstate;
- exact finite ensemble;
- `U_rec` / `U_scr` and inverse/bijectivity tests;
- forward trajectories;
- exact reversed trajectories;
- full-state Shannon entropy preservation.

No temporal arrow is claimed in Stage 3A.

#### Stage 3B — record diagnostics

Implement entropy, mutual information, conditional entropy, Bayes-optimal decoding, record profiles, and signed record/accessibility scores.

#### Stage 3C — asymmetric-record model

Use the blank-memory boundary and test whether a record-defined orientation appears.

#### Stage 3D — reversal and symmetric controls

Test sign reversal, symmetric-mixture cancellation, order-only/no-record control, and nonblank-memory boundary control.

#### Stage 3E — complete local view

Upgrade toward:

`G_k=(Records_k,Actuality_k,Potentiality_k)`

and define explicit global-to-local projections.

#### Stage 3F — accessibility and information controls

Compare information and reconstructibility on both sides of the current position; add noise only after the exact baseline is established.

#### Stage 3G — robustness and synthesis

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
