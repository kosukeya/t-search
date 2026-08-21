# Stage 8 Concepts — Quantum Potentiality

Status: **Stage 8.0 vocabulary frozen; Stage 8A provides executable `QExt`; Stage 8B realizes two typed modal models on that same carrier.**

This document fixes the meanings used by Stage 8. It supplements `stage8_protocol.md` and does not establish an ontology of time.

## Quantum Actuality

`A_Q(D)` denotes the currently declared quantum actuality: the current relational anchor `D`, constrained physical information declared actual there, and the operational interface needed to specify that current situation.

It is not a complete future history.

`same current quantum Actuality != same complete continuation`.

## QuantumContinuation

A `QuantumContinuation` is a physically admissible executable completion of the current quantum Actuality beyond the current anchor.

It must contain future physical structure acting on the constrained carrier. It is not merely a string label, Python branch, random seed, unused metadata object, or event renaming.

`different continuation labels != physically different continuations`.

## Continuation equivalence

Two continuation descriptions are equivalent when they differ only by declared representational changes while preserving their executable physical schedule and designated continuation diagnostics.

Cosmetic renaming therefore preserves the continuation-equivalence class.

## QExt(D)

`QExt(D)` is the set of equivalence classes of physically admissible quantum continuations of the current Actuality.

It is a modal carrier, not a declaration that every represented extension is ontically real.

`QExt represented != ontically real futures by definition`.

## Stage 8A canonical realization

The first executable substrate is:

`QExt(e1) = {h_L, h_R}`.

Both continuations share `V0=I` and `V1=U_rec`, hence the same constrained current state and one-bit target-specific record at `e1`.

They differ only at `e2`:

- `h_L`: `V2=U_rec`;
- `h_R`: `V2=Z_C U_rec`.

`Z_C` is a reversible C-sector phase, identity on memory and commuting with the Stage 7 B-based record-target projector. The baseline future distinction is therefore memory neutral and record-target neutral.

The canonical `e2` reduced states are physically inequivalent, while a renamed copy of `h_L` remains the same continuation class. The finite terminal convention is `QExt(e2)=empty`.

`future physical inequivalence != modal semantics by itself`.

## QuantumContinuationCarrier

A `QuantumContinuationCarrier` is the validated tuple of physical continuation-equivalence representatives at a declared current anchor.

Stage 8B uses one canonical carrier object containing `{h_L,h_R}` and passes that same object into both typed modal models.

`same physical continuation carrier != same modal type`.

## Epistemic quantum Potentiality

`EPot_Q(D)` is a typed set of live continuation hypotheses in a model that already contains one selected complete continuation `h*`.

`M_E^Q=(QCarrier,D,h*,q_E)`.

The Stage 8B concrete type is `EpistemicQuantumPotentiality`.

The epistemic weight `q_E(h|D)` represents uncertainty about which already-selected continuation is actual. The hidden `h*` is privileged model data and must not enter the pre-discriminating public interface.

The selected continuation must belong to one `QExt` equivalence class and retain positive epistemic support.

## Ontic-extension quantum Potentiality

`OPot_Q(D)` is the typed extension structure of a model that contains no selected complete future datum before update.

`M_O^Q(D)=(QCarrier,D,QExt(D),K)`.

The Stage 8B concrete type is `OnticExtensionQuantumPotentiality`.

The frozen/slots Stage 8B ontic model stores only the shared carrier and extension weights. Its schema contains no selected continuation, selected history, selector, seed, precomputed outcome, latent branch selector, or direct singleton continuation field.

A structural selector audit checks this bounded software fact. It does not prove that nature is ontically open.

`no selected continuation field != proof that nature is ontically open`.

## Selected continuation

A selected continuation `h*` is a privileged global model datum that singles out one complete member of `QExt(D)` before discriminating evidence arrives. Its presence defines the Stage 8 epistemic role.

Its formal absence from the ontic-extension model is not itself an empirical result.

`hidden h* diagnostic != operational access to h*`.

## Matched continuation weights

Stage 8 distinguishes:

- `q_E`: epistemic belief over an already-selected continuation;
- `K`: weight over admissible continuations in the no-selected-future model.

Stage 8B constructs the canonical matched vector `(0.5,0.5)` from the shared carrier alone. The weight constructor receives no selected continuation.

`same numerical weights != same probability semantics`.

## Stage 8B pre-discriminating projection

Stage 8B defines only a minimal public projection used to test selector non-leakage before the full Stage 8C operational interface is implemented.

It contains:

- current anchor;
- shared current constrained reduced state;
- current record information;
- `QExt` size;
- continuation weights.

It contains neither `h*` nor model-type names.

With carrier and weights fixed, swapping epistemic `h*=h_L` to `h*=h_R` changes the privileged diagnostic while leaving this projection unchanged.

`Stage 8B pre-discriminating view != full Stage 8C O_Q interface`.

## Operational quantum interface

`O_Q` is the Stage 8C+ ontology-neutral interface exposing declared current physical, record, accessible-observable, and next-outcome information.

It must not expose class names, `h*`, hidden selectors, or privileged modal diagnostics.

`O_Q equality != modal identity`.

## Privileged modal diagnostic

A privileged diagnostic is a test-only inspection of structural facts such as whether `h*` exists. It is not automatically a local physical observable.

`internal distinguishability != operational accessibility`.

## Actualization / update

An update extends declared Actuality after explicitly supplied evidence.

Epistemic update retains the pre-existing `h*` and conditions beliefs.

Ontic-extension update grows Actuality and prunes `QExt` without introducing a hidden complete future.

Stage 8B does not implement this update yet.

`actualization API update != ontological becoming`.

## P-V covariance

P-V covariance means corresponding continuation families and their modal semantics can be represented consistently under genuine Stage 7/8 clock-perspective transformations with explicit continuation/event correspondence.

`P-V covariance != P=V`.

`perspective consistency != modal equivalence`.

## R-V compatibility

R-V compatibility means one record-bearing physical construction and one declared V semantics coexist consistently.

Stage 8A deliberately makes the continuation difference memory and record-target neutral, and Stage 8B places both modal types on that same carrier. Stage 8E will perform the explicit R-V pressure test.

`R-V compatibility != R=V`.

## O-V compatibility

O-V compatibility means the same internal order/history anchor can support the declared V semantics.

`internal order != ontic openness`.

## Quantum-randomness and superposition controls

Stage 8 does not define V through generic quantum uncertainty.

`Potentiality != quantum randomness by definition`.

`Potentiality != superposition by definition`.

`Potentiality != Born probability by definition`.

`superposition != ontic Potentiality by definition`.

A coherent superposition over continuation labels may later be used as a physical control, but it is not by itself an `OPot_Q` witness.

## Density-matrix ambiguity

A density matrix may admit multiple decompositions and does not by itself specify whether a complete continuation is globally selected.

`density matrix decomposition != unique modal semantics`.

## Integration success

Stage 8 counts V as integrated only if:

- `QExt` contains physically meaningful continuations acting on the constrained carrier;
- both typed modal semantics use that same continuation substrate;
- operational comparison is executable;
- update semantics are executable;
- genuine clock-perspective transport is executable.

Stage 8A establishes the first item. Stage 8B establishes the second for the canonical family. The remaining items are Stage 8C/D work.

## Integration failure

The following is not sufficient:

`Stage 7 quantum model + unrelated Stage 2 modal metadata`.

`product decoration != integrated layer`.

## Evidence statuses

Stage 8 uses:

- `preserved`;
- `lost`;
- `reconstructible`;
- `inaccessible`;
- `not_established`;
- `not_applicable`.

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`not_established != false`.
