# Stage 8 Concepts — Quantum Potentiality

Status: **Stage 8.0 vocabulary frozen; Stage 8A provides the first executable `QExt` realization.**

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

Both continuations share the same current prefix:

- `V0=I`;
- `V1=U_rec`.

They therefore share the same constrained current state and the same one-bit target-specific record at `e1`.

Their only canonical difference is future-side at `e2`:

- `h_L`: `V2=U_rec`;
- `h_R`: `V2=Z_C U_rec`.

`Z_C` is a reversible phase on the A-clock rest-pair sector `C energy label == +1`. It is identity on memory and commutes with the Stage 7 B-based record-target projector.

The future distinction is therefore memory neutral and record-target neutral in the declared baseline.

The two futures are physically inequivalent: their normalized `e2` reduced states are orthogonal in the canonical source run, while a pure renamed copy of `h_L` remains equivalent to `h_L`.

The finite terminal convention is:

`QExt(e2)=empty`.

Stage 8A does not yet instantiate either modal semantics below.

`future physical inequivalence != modal semantics by itself`.

## Epistemic quantum Potentiality

`EPot_Q(D)` is a typed set of live continuation hypotheses in a model that already contains one selected complete continuation `h*`.

`M_E^Q=(QCarrier,D,h*,q_E)`.

The epistemic weight `q_E(h|D)` represents uncertainty about which already-selected continuation is actual. The hidden `h*` is privileged model data and must not enter the pre-discriminating operational interface.

## Ontic-extension quantum Potentiality

`OPot_Q(D)` is the typed extension structure of a model that contains no selected complete future datum before update.

`M_O^Q(D)=(QCarrier,D,QExt(D),K)`.

The model may contain continuation weights `K`, but no hidden selector, seed-equivalent selector, precomputed outcome, or other datum may single out a complete continuation.

`no selected continuation field != proof that nature is ontically open`.

## Selected continuation

A selected continuation `h*` is a global model datum that singles out one complete member of `QExt(D)` before discriminating evidence arrives. Its presence defines the Stage 8 epistemic role.

Its formal absence from the ontic-extension model is not itself an empirical result.

## Operational quantum interface

`O_Q` is an ontology-neutral interface exposing declared current physical, record, accessible-observable, and next-outcome information.

It must not expose class names, `h*`, hidden selectors, or privileged modal diagnostics.

`O_Q equality != modal identity`.

## Privileged modal diagnostic

A privileged diagnostic is a test-only inspection of structural facts such as whether `h*` exists. It is not automatically a local physical observable.

`internal distinguishability != operational accessibility`.

## Quantum continuation weights

Stage 8 distinguishes:

- `q_E`: epistemic belief over an already-selected continuation;
- `K`: weight over admissible continuations in the no-selected-future model.

`same numerical weights != same probability semantics`.

## Actualization / update

An update extends declared Actuality after explicitly supplied evidence.

Epistemic update retains the pre-existing `h*` and conditions beliefs.

Ontic-extension update grows Actuality and prunes `QExt` without introducing a hidden complete future.

`actualization API update != ontological becoming`.

## P-V covariance

P-V covariance means corresponding continuation families and their modal semantics can be represented consistently under genuine Stage 7/8 clock-perspective transformations with explicit continuation/event correspondence.

`P-V covariance != P=V`.

`perspective consistency != modal equivalence`.

## R-V compatibility

R-V compatibility means one record-bearing physical construction and one declared V semantics coexist consistently.

Stage 8A deliberately makes the continuation difference memory and record-target neutral so V is not definitionally constructed from R.

Later stages will test whether the same record-defined orientation can coexist with both epistemic and ontic-extension semantics.

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

Stage 8A establishes only the first item for the canonical family.

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
