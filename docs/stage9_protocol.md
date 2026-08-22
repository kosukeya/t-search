# Stage 9 Protocol — Directional Records with Nontrivial Quantum Potentiality

Status: **Stage 9.0 protocol frozen before Stage 9A implementation.**

Selected Stage 9 gate from Stage 8G:

> **Integrate directional record formation with nontrivial quantum Potentiality in one constrained continuation family.**

Current refined candidate carried into Stage 9:

`T9_candidate=(O,P,R,V;Xi)`

with tested internal role typing:

`R=(R_content,R_direction,R_access)`

`V=(V_extension,V_semantics,V_weights)`.

These labels are finite-model bookkeeping roles. Stage 9 does not assume that they are fundamental or metaphysically irreducible.

## 1. Central question

Stage 8 placed nontrivial quantum Potentiality `V` in the same constrained multi-clock construction as `P/O/current-R`, but its canonical continuation family had one-bit current record content and **zero directional record score**. Stage 7C/8E separately supplied a directional-record completion with the same minimal order/current prefix.

Stage 9 asks:

> Can a single constrained quantum continuation family carry both nontrivial `V` and a genuinely directional `R_direction`, with the two structures remaining correctly typed and perspective-consistent under genuine clock changes, while selected-versus-unselected future semantics remain testable rather than being assumed from the record arrow?

The target is a same-family pressure test of the strongest unresolved Stage 8 compatibility link:

`R_direction <-> V`.

Stage 9 does **not** assume that a positive result means ontological becoming.

## 2. Strong integration criterion

A canonical Stage 9 current anchor `D_*` must satisfy all of the following in the same declared family:

1. `QExt(D_*)` contains at least two physically inequivalent admissible quantum continuations;
2. the continuations share the declared current Actuality/prefix through `D_*`;
3. each canonical continuation supports a nonzero directional-record diagnostic at the same declared current anchor;
4. the canonical continuation family gives a coherent direction rather than obtaining the sign only by averaging branch-dependent opposite arrows;
5. the physical distinction between continuation classes is not definitionally the memory/record label used to diagnose `R_direction`;
6. no selected complete continuation is inserted into the ontic-extension model before update.

A convenient canonical target is therefore:

`|QExt(D_*)| >= 2`

and, for every canonical `h in QExt(D_*)`,

`A_R(h,D_*) > 0`

with a matching accessibility-direction sign where the declared interface exposes the relevant record.

The exact numerical value is not frozen in advance; the nonzero sign, provenance, and controls are.

## 3. Why per-continuation direction is required

A weighted aggregate score alone is insufficient because it could manufacture an apparent arrow from branch weights or from mixing continuations with different signs.

Stage 9 therefore distinguishes:

- `A_R(h,D_*)`: continuation-specific structural record-direction score;
- `A_R^mix(D_*)`: an optional model-level score obtained after weighting continuations by `q_E` or `K`.

The canonical positive witness must establish direction before the model-level mixture is used.

Guard:

`weighted directional score != continuation-independent directional structure`.

## 4. Canonical construction strategy

Stage 9A should begin from the smallest Stage 7/8-compatible extension rather than inventing a new unrelated model.

Preferred design:

- retain the Stage 8 constrained multi-clock carrier and common current A-perspective anchor;
- retain a reversible record-writing interaction before or at the current anchor;
- use a later common record-target scrambling interaction so that the current record is informative about the lower-side target but not the corresponding upper-side target;
- place the nontrivial `V` distinction in a future degree of freedom that is memory-neutral and record-target-neutral, such as the continuation-specific C-sector action already used to distinguish Stage 8 continuations;
- re-derive the constrained completion and A/B/C clock atlases for each continuation rather than assuming Stage 8 maps remain valid.

Schematic requirement:

`common prefix / record formation -> D_* -> { directional completion h_L, directional completion h_R }`

where `h_L` and `h_R` differ physically after `D_*` but share the same record-direction convention.

This is a construction target, not a predeclared success result.

## 5. Directional record semantics

Stage 9 inherits the Stage 3/7 rule that a record is not defined as "information about the past".

For a current anchor and two declared comparison events/targets, use information/provenance diagnostics such as:

`A_R = I(R_* ; X_lower) - I(R_* ; X_upper)`

and, when a local readout interface is declared,

`A_acc = Acc(R_* -> X_lower) - Acc(R_* -> X_upper)`.

The labels `lower` and `upper` refer to neutral event correspondence/order positions. They are not called physical past/future before the directional diagnostic is evaluated.

A nonzero mutual-information contrast is not sufficient by itself. The implementation must also retain explicit provenance of the recording/scrambling interactions and the event/observable correspondence used by the diagnostic.

## 6. Direction is distinct from record content and access

Stage 9 preserves the Stage 8 refinement:

`R=(R_content,R_direction,R_access)`.

Therefore all of the following remain distinct questions:

- does a current register carry target-specific information? (`R_content`)
- does the record profile select one orientation? (`R_direction`)
- is that information available through a declared local interface? (`R_access`)

A current one-bit record with `A_R=0` remains a no-direction control, not a directional record.

## 7. Potentiality semantics carried forward

Stage 9 inherits the Stage 8 selected-versus-unselected distinction without modification.

Epistemic:

`M_E^Q=(QCarrier,D_*,h*,q_E)`

where one complete continuation `h*` is already selected globally but hidden from the declared operational interface.

Ontic-extension:

`M_O^Q(D_*)=(QCarrier,D_*,QExt(D_*),K)`

where admissible continuations and weights are represented but **no selected complete continuation datum exists before update**.

The presence of a directional record does not alter these definitions by fiat.

Stage 9 must test whether the formal distinction remains underdetermined by the declared public P/O/R-direction/V interface when numerical weights are matched.

## 8. Ontology-neutral directional operational interface

Stage 9C should define a typed operational interface that extends Stage 8C without inspecting model classes or hidden selectors.

A provisional target is:

`O_QR=(D_*,rho_now,R_now,R_dir_access,Next_Q(D_*),pi_Q(next|D_*),observed_outcome)`.

Here `R_dir_access` must contain only directional record statistics or corresponding observables granted by the declared interface. Privileged access to a hidden selected continuation is forbidden.

The protocol must separately retain privileged test-only diagnostics for structural audits.

Matched epistemic and ontic-extension models should be compared through `O_QR`, not by Python type or hidden fields.

## 9. Frozen directional controls

Stage 9 requires four orientation controls on the same or explicitly corresponding constrained carrier family.

### Forward

The canonical family should produce a coherent nonzero record direction, conventionally reported as positive only after the lower/upper event correspondence is declared.

Expected target:

`A_R > 0`.

### Reversed

Apply an explicitly defined modeled-history / interaction reversal or an equivalent reversed constrained completion. Do not implement reversal merely by iterating Python indices backward.

Expected covariance target:

`A_R^rev = -A_R^fwd`.

The reversed family must retain nontrivial `V` unless the experiment is explicitly diagnosing why reversal destroys it.

### Balanced

Use an orientation-balanced construction or mixture with no signed bias while preserving the relevant order and continuation structure.

Expected target:

`A_R = 0`.

### No-record

Neutralize the record-writing channel while retaining the continuation family, order anchor, and as much P/O/V structure as possible.

Expected target:

`R_direction = absent/zero` while `V_extension` remains nontrivial.

These controls test directional structure rather than mere order, branch multiplicity, or simulation order.

## 10. Branch distinction must not be the arrow

The Stage 9 continuation classes must be physically inequivalent for a reason independent of the directional record label.

Required design guard:

`continuation identity != record-direction identity`.

The preferred canonical witness uses the same record formation/scrambling structure in both `h_L` and `h_R`, while the V distinction acts on a disjoint or record-neutral physical degree of freedom.

A construction in which "left branch means positive arrow" and "right branch means negative arrow" does not satisfy the canonical integration criterion.

## 11. Genuine clock-change requirement

For every canonical continuation `h`, Stage 9D must re-derive the physical A/B/C clock reductions and reconstructions from that continuation's constrained carrier.

Perspective maps remain:

`S^h_{Y<-X}(k,j)=R^h_Y(k)E^h_X(j)`.

Required checks include:

- rank/support validity for every declared chart;
- direct-global route consistency;
- inverse/round-trip consistency;
- three-clock composition consistency;
- correct transport of record observables and V class/weight data;
- explicit event correspondence `chi` and continuation/class correspondence.

Do not reuse a map derived for one continuation or coordinate convention without proving it is valid for the target continuation.

## 12. Record-observable typing guard

Stage 8E exposed a real failure mode: a mathematically covariant observable can still be semantically wrong when expressed in the wrong coordinate/support basis.

Stage 9 therefore freezes:

`covariance of a wrongly typed observable != semantic correctness`.

Every directional record observable must carry enough metadata to identify:

- source physical support;
- continuation;
- perspective/clock;
- event anchor;
- coordinate basis;
- target variable/register semantics.

The Stage 8 fixed-support / QR-coordinate mismatch must remain covered by regression tests or an equivalent typed assertion.

## 13. Event and class correspondence

Equal numeric clock readings do not identify physical events.

Stage 9 must declare maps such as:

`chi_{Y<-X}^h : E_X^h -> E_Y^h`

and continuation/class correspondence such as:

`h_L -> h_L`, `h_R -> h_R`

or an explicitly justified alternative.

Removing or corrupting these correspondences is a required negative control.

Guards:

`equal numeric clock readings != event identity`

`bare matrix covariance != physical event/class correspondence`.

## 14. Directional R–V compatibility questions

Stage 9E must distinguish at least the following questions instead of reporting one undifferentiated `R-V` relation:

1. `R_direction` with `V_extension`: can a coherent arrow coexist with multiple physical continuations?
2. `R_direction` with `V_weights`: does changing continuation weight alter, preserve, or destroy the direction diagnostic?
3. `R_direction` with `V_semantics`: does selected-versus-unselected modal typing remain operationally underdetermined when direction is present?
4. `R_access` with `V`: can global directional structure persist when local record access is hidden or degraded?
5. `P-R_direction-V`: does directional structure transform consistently together with continuation classes under genuine clock changes?
6. `O-R_direction-V`: does the declared event/order anchor remain compatible with direction and extension structure?

Every row must use one of the functional/evidential statuses already established by Stage 8:

`compatible / preserved / reconstructible / inaccessible / lost / underdetermined / not_established / implication_refuted`.

The exact status vocabulary may be narrowed for a particular table, but meanings must not be collapsed.

## 15. Modal underdetermination test with direction present

Stage 9C/E must repeat the Stage 8 hidden-selected-versus-no-selector comparison on the directional carrier.

Minimum checks:

- same physical continuation carrier;
- same current Actuality;
- same accessible directional record interface;
- matched positive continuation weights;
- hidden `h*` swap does not change the declared pre-discriminating `O_QR` view;
- changing only ontic/epistemic weights changes prediction where the interface is weight-sensitive;
- the ontic-extension object contains no selected complete continuation datum;
- directional record structure remains present in both typed models.

A matched result supports operational underdetermination in the declared family. It does not prove that the future is ontically open or fixed.

## 16. Ablation requirements

Stage 9F must remove or neutralize one ingredient at a time where physically meaningful.

Required targets include at least:

- directional record coupling/scrambling neutralized while V remains nontrivial;
- `QExt` collapsed to a singleton while directional R is retained if possible;
- selected-versus-unselected modal semantics erased while physical P/O/R/V carrier data are retained;
- nontrivial V weights unfixed;
- local record access hidden;
- event/class correspondence removed;
- explicit perspective edge matrices removed while per-node coordinates remain, testing reconstructibility;
- one deliberately wrong record-observable coordinate transport.

Do not call a role metaphysically irreducible merely because one ablation loses it.

## 17. Evidence taxonomy

Every scientific claim must be tagged or inferable as one of:

- executable positive witness;
- executable negative/countermodel witness;
- reconstruction result;
- interface/accessibility result;
- underdetermination result;
- not established;
- candidate interpretation.

The protocol forbids promoting `not_established` to `false` or `underdetermined` to `ontically open`.

## 18. Stage 9 sequence

### Stage 9.0 — protocol freeze — completed

Freeze the directional-R/V integration criterion, per-continuation direction requirement, modal semantics, controls, clock-transport typing, ablations, evidence vocabulary, interpretation guards, and exit criteria.

### Stage 9A — common directional-R/V continuation substrate — next

Construct the smallest constrained family with:

- a shared current Actuality;
- at least two physically inequivalent future continuations;
- continuation-independent directional record formation at the declared current anchor;
- branch distinction separated from the record-direction channel.

### Stage 9B — directional diagnostics and controls

Implement/reuse exact record-information and accessibility diagnostics, then verify forward/reversed/balanced/no-record controls on the constrained continuation family.

### Stage 9C — typed modal models and directional operational underdetermination

Place epistemic selected-`h*` and ontic no-selected-continuation semantics on the same directional carrier and test the declared `O_QR` interface, hidden-selector swap, matched/mismatched weights, and explicit update semantics.

### Stage 9D — continuation-aware clock transport

Re-derive A/B/C atlases for each continuation and transport states, record observables, event correspondences, continuation classes, and weights with mismatch controls.

### Stage 9E — P/O/R_direction/V compatibility matrix

Evaluate the typed compatibility questions in Section 14, including whether direction constrains V classes, semantics, or weights.

### Stage 9F — ablation / reconstruction / accessibility matrix

Run the one-ingredient ablations in Section 16 and classify each role without metaphysical overclaiming.

### Stage 9G — synthesis and evidence-selected next gate

Decide whether the Stage 8 `refined_layered` candidate is strengthened, requires new `Xi_RV` constraints, is reduced, is broken in the declared family, or remains inconclusive. Re-rank the remaining gates from executable evidence.

## 19. Exit criteria

Stage 9 defines 50 exit criteria. Stage 9.0 freezes criteria **1–10** only; criteria 11–50 remain future work.

### Stage 9.0 — criteria 1–10

1. The Stage 9 gate exactly matches the Stage 8G evidence-selected gate.
2. `T9_candidate=(O,P,R,V;Xi)` is carried forward without assuming fundamental status.
3. `R_content`, `R_direction`, and `R_access` remain explicitly distinct.
4. `V_extension`, `V_semantics`, and `V_weights` remain explicitly distinct.
5. Successful integration requires nontrivial physically inequivalent `QExt(D_*)` and nonzero per-continuation `R_direction` at one declared common anchor.
6. Continuation identity is required to be physically distinct from the record-direction label/channel.
7. Selected-versus-unselected modal semantics are frozen without using direction as evidence for ontic openness.
8. Forward/reversed/balanced/no-record controls are frozen before implementation.
9. Genuine continuation-aware clock transport requires explicit event/class/observable typing.
10. Interpretation/evidence guards prohibit promoting operational underdetermination or record direction into ontological becoming.

### Future allocation

- criteria **11–16**: Stage 9A substrate;
- criteria **17–23**: Stage 9B directional diagnostics/controls;
- criteria **24–30**: Stage 9C typed modal/operational tests;
- criteria **31–36**: Stage 9D genuine clock transport;
- criteria **37–42**: Stage 9E compatibility/constraint matrix;
- criteria **43–47**: Stage 9F ablation/reconstruction/accessibility;
- criteria **48–49**: Stage 9G synthesis and next-gate selection;
- criterion **50**: external final full-repository regression and merge-readiness review.

Criterion 50 is intentionally external to the executable scientific classifier.

## 20. Frozen mandatory guards

- `directional record arrow != ontological future openness`;
- `directional record arrow != ontological becoming`;
- `explicit evidence update != ontological becoming`;
- `Potentiality != quantum randomness by definition`;
- `Potentiality != superposition by definition`;
- `QExt represented != ontically real futures by definition`;
- `operational quantum equality != modal/ontological identity`;
- `record content != directional record arrow`;
- `record content != unique future continuation`;
- `order != directional record arrow`;
- `continuation identity != record-direction identity`;
- `weighted directional score != continuation-independent directional structure`;
- `P-V covariance != P=V`;
- `R-V compatibility != R=V`;
- `P-R_direction-V covariance != ontic openness`;
- `equal numeric clock readings != event identity`;
- `covariance of a wrongly typed observable != semantic correctness`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `underdetermined != ontically open`;
- `inaccessible != globally absent`;
- `not_established != false`;
- `finite constrained-model success != empirical discovery`;
- `finite clock covariance != general covariance`.

## 21. Non-goals

Stage 9 does not establish by construction that:

- the physical future is ontically open;
- one complete future is physically preselected;
- a record arrow is the thermodynamic arrow;
- a record arrow is phenomenal passage;
- actualization is a fundamental dynamical process;
- the Stage 9 constrained family is a realistic spacetime;
- quantum randomness is the source of Potentiality;
- the layered candidate is unique or fundamental;
- finite clock covariance is gravitational/general covariance;
- a successful implementation is a new empirical law.

## 22. Strongest statement allowed at protocol freeze

**Stage 8G identifies directional `R` with nontrivial quantum `V` as the highest-value unresolved finite-model compatibility link. Stage 9.0 therefore freezes a stronger single-family test: at one declared common current anchor, at least two physically inequivalent admissible quantum continuations must remain while each continuation carries the same nonzero directional record structure, with continuation identity separated from the record channel. The construction must survive forward/reversed/balanced/no-record controls, typed selected-versus-unselected modal comparison, and genuine continuation-aware A/B/C clock transport before any stronger synthesis is allowed. Stage 9.0 itself establishes none of those positive results and does not identify record direction or Potentiality with ontological becoming.**

## 23. Immediate next step

Stage 9A should build the smallest continuation pair that combines the Stage 7C directional-record mechanism with the Stage 8 future continuation distinction while preserving a shared current anchor and keeping the continuation-defining physical action record-neutral.
