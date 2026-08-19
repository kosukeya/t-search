# Stage 3E — Complete Local View

Status: **completed; GitHub Actions full regression passed at the Stage 3E code/test checkpoint**.

## Purpose

Stage 3E makes the local perspective explicit. The questions are:

1. what does a record-bearing local view actually receive from the global Stage 3 block;
2. what remains hidden, ambiguous, reconstructible, or lost;
3. how can Stage 2 Potentiality be reintroduced without changing the record semantics already isolated in Stage 3A–3D?

## Global record-only object

The block-like object is:

`B_3=(Z_space,U_1,U_2,Omega,mu)`.

The implementation stores:

- all eight complete microstates;
- the two declared bijective updates;
- the exact canonical trajectory ensemble.

Every ensemble trajectory is validated against the declared maps.

## Local projection

The local Actuality interface is deliberately reduced from:

`Z_k=(X_k,M_k,N_k)`

to:

`A_k^loc=(X_k,M_k)`.

The explicit projection is:

`F_k:(B_3,omega)->G_{omega,k}^rec`

with:

`G_k^rec=(Records_k,Actuality_k)`.

`Records_k` contains the current record-register readout plus the declared ensemble-level record/accessibility diagnostics. It does not contain the actual hidden environment bit or opposite-side microstates.

## Canonical example

Use the canonical complete trajectory beginning at:

`(X_0,M_0,N_0)=(1,0,1)`.

At the central position:

`(X_1,M_1,N_1)=(1,1,1)`.

The local view receives only:

`Actuality_1^loc=(1,1)`

and the record readout:

`M_1=1`.

The Stage 3B/C ensemble diagnostics carried by the declared interface retain:

`Q_R(1,j)={0:1,1:1,2:0}`

and:

`orientation=lower-index`.

The returned local data structure has no field for `N`, the complete trajectory, or an opposite-side actual state.

## Single-view ambiguity

The central local state `(X_1,M_1)=(1,1)` is compatible with two canonical histories:

- one with hidden `N=0`;
- one with hidden `N=1`.

Therefore:

`|Compatible(B_3,G_1^rec)|=2`.

A single central local view does not uniquely reconstruct the actual global trajectory.

This is genuine representational ambiguity caused by the declared local interface, not stochastic uncertainty introduced by sampling.

## Reconstruction from a view family

Add the position-2 local view from the same actual trajectory.

The pair:

`(G_1^rec,G_2^rec)`

fixes whether `X` changed between positions 1 and 2. Under the declared reversible map:

`X_2=X_1 XOR N`,

so the hidden conserved `N` becomes reconstructible.

The compatibility class contracts from two histories to one:

`|Compatible(B_3,{G_1^rec,G_2^rec})|=1`.

Thus the complete actual trajectory is reconstructible from this suitable family of local views even though it is not locally accessible from either single view alone.

## Information classification

### Locally accessible

- current neutral position;
- current `X_k`;
- current record value `M_k`;
- record/accessibility diagnostics explicitly supplied by the experiment interface.

### Globally represented but hidden

- current `N_k`;
- actual opposite-side microstates;
- complete actual trajectory;
- privileged initial boundary labels.

### Ambiguous from one local view

- complete trajectory;
- hidden environment bit;
- opposite-side actual states.

### Reconstructible from a suitable family of local views

- complete actual trajectory;
- hidden `N` in the canonical model.

### Lost without weighted global structure

- the full probability distribution over complete trajectories;
- global cross-position trajectory correlations not encoded in one unweighted local instance.

This checkpoint therefore exhibits all of the distinctions:

`local accessibility != hidden information != ambiguity != reconstructibility != loss`.

## Completing `G=(Records,Actuality,Potentiality)`

Stage 2 Potentiality is reintroduced after record asymmetry has already been isolated.

The construction is explicitly a product of toy-model layers.

Product Actuality:

`A_product=(record position, record Actuality, modal Actuality)`.

Epistemic version:

`G_E^complete=(Records,A_product,EPot,next probabilities)`.

Ontic version:

`G_O^complete=(Records,A_product,OPot,next probabilities)`.

The Potentiality types remain distinct.

## Hidden versus absent future information remains preserved

The epistemic product adapter consumes an already-projected Stage 2 `EpistemicLocalView`. It never receives the global hidden selected history `h*`.

Therefore no Stage 3E field leaks `selected_history`.

The ontic product adapter likewise contains no selected future.

The Stage 2 distinction survives:

`selected-future information hidden globally`

versus:

`selected-future information absent from the model state`.

## Shared record layer across both Potentiality semantics

For the canonical product fixture, both complete local views receive exactly the same Stage 3 record layer:

`Records_E = Records_O`.

Both therefore retain the same Stage 3C record-defined orientation:

`lower-index`.

But:

`type(EPot) != type(OPot)`.

This is an intentional construction-level control showing that the Potentiality adapter does not alter the record layer.

It does **not** establish a physical theorem that record arrows are independent of fixed/open-future metaphysics.

## Strongest supported Stage 3E conclusion

Within the declared finite toy-model interfaces:

**a block-like weighted trajectory description can be projected to an explicit record-bearing local view that omits privileged global information; one local view can be ambiguous while a family of compatible local views reconstructs the global history; and the same already-tested record layer can be combined with either typed Stage 2 Potentiality semantics without leaking their privileged global distinctions.**

Stage 3E therefore realizes the formal shape:

`G=(Records,Actuality,Potentiality)`

without treating it as a metaphysical proof of becoming.

## Important limits

Stage 3E does not establish:

- that `(Records,Actuality,Potentiality)` is a unique fundamental ontology;
- that Stage 2 and Stage 3 toy substrates are one physical system;
- that ensemble-level mutual information is directly measurable by a single-run internal observer;
- a fundamental temporal arrow;
- ontological becoming;
- phenomenal passage.

## Validation

The committed Stage 3E suite contains **10 focused tests**.

GitHub Actions clean PR merge-ref at the code/test checkpoint:

`147 passed in 3.21s`.

This includes Stage 1, Stage 2, and Stage 3A–3E tests.

## Next

Stage 3F — accessibility and information controls — will stress the new projection under controlled information degradation and ask which record/reconstruction claims survive when access is reduced without interpreting inaccessible information as ontologically absent.
