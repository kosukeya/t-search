# Stage 3E — Complete Local View Notes

Status: **implemented; full PR regression passed at the code/test checkpoint**.

Stage 3E converts the Stage 3 record experiment from a global trajectory description into an explicit local information interface and then reintroduces Stage 2 Potentiality as a typed product layer.

## 1. Explicit block-like object

The record-only global object is represented as:

`B_3=(Z_space,U_1,U_2,Omega,mu)`

through `Stage3RecordBlock`:

- complete eight-state microstate space;
- two declared bijective updates;
- exact weighted trajectory ensemble.

Every trajectory in the block must be compatible with the declared updates.

The object is a global mathematical representation, not a physically available external observer.

## 2. Declared local Actuality

Stage 3E deliberately does **not** expose the complete current microstate `Z_k=(X_k,M_k,N_k)`.

The local Actuality interface is:

`A_k^loc=(X_k,M_k)`.

The environment/ancilla bit `N_k` is omitted.

This is important methodologically. If the full current microstate were exposed together with the known bijective updates, the canonical complete trajectory would be trivially reconstructible from a single view and the global/local distinction would largely disappear.

## 3. Record-bearing local view

The reduced record view is:

`G_k^rec=(Records_k,Actuality_k)`.

`RecordReadout` exposes:

- register identity `M`;
- current register value `M_k`;
- target identity `X`;
- record-information profile over neutral positions;
- decoder/accessibility profile;
- Stage 3C orientation label where a two-sided window exists.

The profiles are ensemble-level diagnostics granted by the declared experiment interface. Their presence in `G_k^rec` does **not** mean that a physical single-run observer can infer mutual information from one observation.

The view does not contain fields for:

- `N_k`;
- complete trajectory;
- opposite-side actual microstates;
- privileged initial boundary labels.

## 4. Global-to-local projection

The explicit projection is implemented as:

`project_record_view(block, trajectory, position=k)`.

Conceptually:

`F_k:(B_3,omega)->G_{omega,k}^rec`.

A trajectory instance must belong to the block ensemble. The projection returns only the declared local interface.

## 5. Ambiguity and reconstruction

For the canonical example with initial state `(X_0,M_0,N_0)=(1,0,1)`, the central local Actuality is:

`(X_1,M_1)=(1,1)`.

Because `N_1` is hidden, this single central view is compatible with **two** canonical complete trajectories, one with `N=0` and one with `N=1`.

Therefore:

`single local view -> ambiguous global history`.

However, adding a compatible local view from position `2` exposes the change/no-change relation in `X`, which determines the hidden conserved `N` for this toy dynamics. The pair of views then has exactly one compatible complete trajectory.

Therefore:

`view family -> complete trajectory reconstructible`.

This is a concrete Stage 3 version of the Stage 1 distinction between local accessibility and reconstruction from multiple views.

## 6. Information classification

For the declared `(X,M)` local interface:

### Locally accessible

- current neutral position;
- current `X_k`;
- current `M_k`;
- declared record/accessibility diagnostics supplied by the experiment interface.

### Globally represented but hidden from one local view

- current `N_k`;
- opposite-side actual microstates;
- complete actual trajectory;
- privileged initial boundary labels.

### Ambiguous from one local view

- complete trajectory;
- hidden `N`;
- opposite-side actual microstates.

### Reconstructible from a suitable family of local views

- complete trajectory;
- hidden `N` in the canonical dynamics.

### Lost without weighted global structure

- full probability weights over complete trajectories;
- global cross-position trajectory correlations not encoded by one unweighted local instance.

`hidden != lost != ambiguous != reconstructible` remains an explicit guard.

## 7. Reintroducing Potentiality

Stage 3E attaches the already-tested record layer to the already-projected Stage 2 local views.

This is deliberately an explicit **product construction**, not a claim that the Stage 2 branching substrate and Stage 3 bit dynamics are one physical system.

The product Actuality is:

`A_product=(record_position, record_actuality, modal_actuality)`.

Two separate complete local-view types are retained:

`EpistemicCompleteLocalView=(Records,A_product,EPot,next probabilities)`

and:

`OnticCompleteLocalView=(Records,A_product,OPot,next probabilities)`.

The Potentiality types remain distinct.

## 8. No hidden-future leakage

The epistemic adapter accepts an already-projected `EpistemicLocalView`, not the global `EpistemicHistoryModel`. Therefore the Stage 2 hidden selected history `h*` is not available to the adapter and is not added to the Stage 3E view.

The ontic adapter likewise adds no selected-future datum.

This preserves:

`hidden selected future != absent selected future`.

## 9. Record semantics under typed Potentiality

The same `RecordReadout` object can be attached to both the epistemic and ontic local views. In the canonical product fixture:

- both receive the same record layer;
- both keep the Stage 3C `lower-index` record-defined orientation;
- both use modal Actuality `('p','n')`;
- their Potentiality objects remain different types.

This establishes only **construction-level separation**: the typed Potentiality adapter does not modify the already-tested record layer by design.

It is not empirical evidence that real-world record arrows are independent of metaphysical fixed/open-future semantics.

## 10. Validation

The committed Stage 3E test file contains **10 focused tests** covering:

1. explicit reversible block object;
2. local `(X,M)` projection without `N`/trajectory leakage;
3. two-history ambiguity from one central view;
4. unique reconstruction from a two-position view family;
5. incompatible-view rejection;
6. nonmember trajectory and duplicate-position guards;
7. typed epistemic complete view without `h*` leakage;
8. typed ontic complete view without selected-future leakage;
9. shared record layer across the two modal semantics;
10. explicit information classification.

GitHub Actions code/test checkpoint:

`147 passed in 3.21s`.

## 11. Interpretation limit

Stage 3E completes a useful formal local-description shape:

`G=(Records,Actuality,Potentiality)`.

It does not establish that this tuple is the unique or fundamental ontology of temporal becoming.

The Stage 2 + Stage 3 composition remains a product of toy-model layers whose physical unification is not yet derived.

## Next

Stage 3F tests accessibility and information degradation more directly, including whether the reconstruction/record claims survive controlled loss or noise without confusing reduced accessibility with ontological absence.
