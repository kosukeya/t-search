# Research Roadmap

This roadmap is intentionally provisional. Each stage may revise earlier definitions.

## North-star question

Can block-like and becoming-like descriptions be treated as different perspectives on one deeper relational temporal structure, with explicit transformations between them and non-trivial structures that remain stable across those transformations?

## Stage 0 — Definitions and scope — completed

Define working meanings for `block`, `becoming`, `Actuality`, `Potentiality`, `record`, `perspective`, `transformation`, and `invariant`.

Exit criterion: satisfied.

## Stage 0.5 — Stage 1 protocol freeze — completed

Key guards established:

- event identity != state/configuration value;
- direct adjacency != induced reachability;
- strict invariant != reconstructible property != local observable;
- simulation order != modeled temporal order.

Exit criterion: satisfied.

## Stage 1 — Minimal classical graph model — completed and merged

Integrated result:

- [`../results/stage1_synthesis.md`](../results/stage1_synthesis.md)

Stage 1 established finite classical global/local reconstruction machinery and controlled representation/information-loss variants. No fundamental physical invariant was claimed.

## Stage 2 — Potentiality — completed and merged

Protocol and synthesis:

- [`stage2_protocol.md`](stage2_protocol.md)
- [`../results/stage2_synthesis.md`](../results/stage2_synthesis.md)

Core formal comparison:

`M_E=(T,h*,q_E)`

versus:

`M_O(D)=(D,Ext_T(D),K)`.

A hidden-selected-future model and a no-selected-future model can be formally different while producing the same tested local operational outputs under matched positive-support conditions.

Full clean regression before merge:

`99 passed`.

Stage 2 exit criterion: satisfied; PR #3 merged.

## Stage 3.0 — Records and temporal direction protocol freeze — completed

Detailed specification:

- [`stage3_protocol.md`](stage3_protocol.md)

Stage 3 separates:

1. ordered structure;
2. microscopic reversibility;
3. record asymmetry;
4. experienced temporal direction.

Principal guards:

`order != arrow`

`microdynamical reversibility != record symmetry`

`correlation != causation`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

`simulation order != modeled temporal order`.

Canonical substrate:

`Z=(X,M,N) in {0,1}^3`

`U_rec(X,M,N)=(X,M XOR X,N)`

`U_scr(X,M,N)=(X XOR N,M,N)`.

Canonical boundary:

`X_0=a`, `M_0=0`, `N_0=b`, with independent uniform `a,b`.

## Stage 3A — Reversible record substrate — completed

Result / notes:

- [`../results/stage3a_reversible_substrate.md`](../results/stage3a_reversible_substrate.md)
- [`stage3a_notes.md`](stage3a_notes.md)

Verified complete eight-state microstate space, bijective/self-inverse updates, exact forward/reversed trajectory ensembles, modeled history reversal, and full-state entropy preservation `(2,2,2)` bits.

Focused tests: **10**.

## Stage 3B — Record diagnostics — completed

Result / notes:

- [`../results/stage3b_record_diagnostics.md`](../results/stage3b_record_diagnostics.md)
- [`stage3b_notes.md`](stage3b_notes.md)

Implemented exact Shannon entropy, mutual information, conditional entropy, Bayes-optimal decoding/accessibility, record/accessibility profiles, and signed `A_R` / `A_Acc` diagnostics.

Canonical values:

`I(M_1;X_0)=1`, `I(M_1;X_2)=0`, `A_R=1`, `A_Acc=1/2`.

Focused tests: **11**.

Stage 3B clean regression: `120 passed`.

## Stage 3C — Asymmetric-record model — completed

Result / notes:

- [`../results/stage3c_asymmetric_record.md`](../results/stage3c_asymmetric_record.md)
- [`stage3c_notes.md`](stage3c_notes.md)

A record-defined orientation is recognized only when MI and decoder signed diagnostics are both nonzero, agree in sign, and the selected side carries nonzero MI.

Canonical assessment:

`A_R=1`, `A_Acc=1/2`, `orientation=lower-index`, `record_defined=True`.

Strongest allowed statement:

**the canonical reversible blank-memory ensemble contains a record-defined orientation toward the lower-index side under the declared interface.**

Focused tests: **8**.

Stage 3C clean regression: `128 passed`.

## Stage 3D — Reversal and symmetric controls — completed

Result / notes:

- [`../results/stage3d_controls.md`](../results/stage3d_controls.md)
- [`stage3d_notes.md`](stage3d_notes.md)

Required controls all passed:

- exact history reversal flips `A_R` and `A_Acc` signs and swaps orientation;
- equal forward/reverse mixing cancels signed bias while equal nonzero correlations remain;
- order-only/no-record control preserves ordered reversible change but yields no orientation;
- independent uniform-memory boundary with canonical reversible maps removes the canonical record contrast.

Strongest supported statement:

**within this finite toy construction, the Stage 3C orientation is not a consequence of mere order or microscopic irreversibility. It tracks record coupling plus asymmetric boundary preparation, reverses covariantly under modeled history reversal, and cancels under orientation-symmetric mixing.**

Focused tests: **9**.

Stage 3D clean regression: `137 passed`.

## Stage 3E — Complete local view — completed

Result / notes:

- [`../results/stage3e_complete_local_view.md`](../results/stage3e_complete_local_view.md)
- [`stage3e_notes.md`](stage3e_notes.md)

Stage 3E introduces an explicit block-like record object:

`B_3=(Z_space,U_1,U_2,Omega,mu)`

and a deliberately reduced local Actuality:

`A_k^loc=(X_k,M_k)`.

The environment bit `N_k` is not exposed. This avoids making the local view trivially equivalent to the complete reversible microstate.

The explicit projection:

`F_k:(B_3,omega)->G_{omega,k}^rec`

returns:

`G_k^rec=(Records_k,Actuality_k)`

with current record readout plus the diagnostics granted by the experiment interface, but without the complete trajectory, opposite-side actual microstates, hidden `N_k`, or privileged initial boundary labels.

Canonical information result:

- one central local view `(X_1,M_1)=(1,1)` is compatible with two complete global histories because hidden `N` remains ambiguous;
- adding a compatible position-2 local view makes the global trajectory unique;
- therefore `single-view ambiguity != multi-view reconstructibility`.

Potentiality is reintroduced using typed product adapters rather than by identifying the Stage 2 and Stage 3 substrates:

`G_E^complete=(Records,A_product,EPot,next probabilities)`

`G_O^complete=(Records,A_product,OPot,next probabilities)`.

The same record layer is attached to both while `EPot` and `OPot` remain distinct types. The epistemic hidden `h*` does not leak into Stage 3E.

Focused Stage 3E tests: **10**.

Stage 3E clean regression: `147 passed`.

## Stage 3F — Accessibility and information controls — completed

Result / notes:

- [`../results/stage3f_accessibility_controls.md`](../results/stage3f_accessibility_controls.md)
- [`stage3f_notes.md`](stage3f_notes.md)

Stage 3F keeps the global block fixed and changes only the local observation channel.

A binary-symmetric channel degrades the record readout while current `X` can independently be exposed or masked.

Record-only checkpoints:

- `epsilon=0`: `I(M_obs;X_0)=1`, decoder `1`, accessible `A_R=1`, `A_Acc=0.5`;
- `epsilon=1/4`: `I(M_obs;X_0)~=0.188721875541`, decoder `0.75`, accessible `A_R` has the same MI value, `A_Acc=0.25`;
- `epsilon=1/2`: `I(M_obs;X_0)=0`, decoder `0.5`, accessible signed contrasts vanish.

Throughout, the unchanged global relation remains:

`I(true M_1;X_0)=1 bit`.

This explicitly realizes the model-level guard:

`inaccessible information != information absent from the formal global state`.

A second result exposes a canonical-model redundancy:

`X_1=X_0`.

Therefore maximally noisy `M` does not remove total local access when `X_1` is still visible. Record-specific accessibility must be distinguished from full-interface accessibility.

With `X` masked, quarter-noise changes an observed `M_obs=1` outcome from two compatible global histories to four positive-posterior histories, with posterior mass `3/4` on `X_0=1`. Complete masking leaves all four histories compatible. These are interface/epistemic ambiguity changes, not ontic branching.

View coverage remains an independent axis: one exact central view is ambiguous while central plus position-2 exact views reconstruct the complete history.

Focused Stage 3F tests: **12**.

GitHub Actions clean PR merge-ref regression after warning cleanup:

`159 passed in 3.17s`.

## Stage 3G — Robustness and synthesis — next

Run the remaining robustness and closure work:

- event/position/register relabeling;
- repeated-value/state controls;
- any remaining informative boundary/noise variants;
- Stage 2 epistemic/ontic integration review;
- final information classification;
- full repository regression;
- six fixed questions;
- `results/stage3_synthesis.md`;
- merge-readiness review for Draft PR #4.

### Stage 3 exit criterion

Stage 3 is complete only if reversible dynamics, record diagnostics, reversal/symmetric/no-record/boundary controls, entropy distinctions, full `Records+Actuality+Potentiality` views, projection/information classification, accessibility robustness, full regression, and six fixed questions are all completed without turning a record-defined orientation into metaphysical proof.

## Stage 4 — Finite Page–Wootters-style quantum model

Use a finite-dimensional clock `C` and system `S`.

Global/block-like representation:

`|Psi> = sum_t |t>_C |psi_t>_S`.

Relational/becoming-like representation:

`|psi_S(t)> proportional to <t|_C Psi>`.

Test conditional dynamics and preserved correlations/transition probabilities.

## Stage 5 — Change of clock / perspective

Use at least three subsystems and explicit changes between clock-relative descriptions. Search for structures stable under block -> becoming and becoming(clock C) -> becoming(clock A).

## Stage 6 — Candidate temporal structure T

Compare structures surviving Stages 1–5, including causal/conditioning order, relational correlations, record accessibility, allowed transitions, and consistency constraints among perspectives.

Do not force a unique invariant if evidence supports a family of complementary structures.

## Stage 7 — Generally covariant / gravitational extension

Only after toy models are stable. Possible progression: parametrized particle -> simple constrained/minisuperspace model -> tractable gravitational setting.

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

- simulation order != modeled temporal order;
- random sampling != evidence of ontic becoming;
- successful software construction != ontological proof;
- global mathematical description != physically realizable God's-eye observer;
- reconstructible structure != automatically fundamental physical structure;
- formal/internal distinguishability != automatically operational distinguishability;
- operational equality != ontological equivalence;
- support semantics != physical possibility;
- order != arrow;
- microdynamical reversibility != record symmetry;
- record asymmetry != phenomenal passage;
- inaccessible information != ontologically absent information.

## Stop / revise conditions

Revise rather than force progress if:

- `block` or `becoming` becomes definitionally circular;
- an alleged invariant is notation-dependent;
- a Stage 3 score merely restates event indices;
- an alleged record is a single-trajectory coincidence;
- a supposedly reversible update is not bijective;
- symmetric controls retain unexplained signed bias;
- global entropy changes under an allegedly closed bijective update because of implementation error;
- a claimed physical arrow is only a boundary/support convention relabeled as physics;
- local inaccessibility is silently reinterpreted as ontological absence;
- a claimed novelty is already an established object under another name.
