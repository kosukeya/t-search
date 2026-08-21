# Stage 8 Concepts — Quantum Potentiality

Status: **Stage 8.0 vocabulary frozen before implementation.**

This document fixes the meanings used by Stage 8. It supplements `stage8_protocol.md` and does not establish an ontology of time.

## Quantum Actuality

`A_Q(D)` denotes the currently declared quantum actuality: the common current event/history anchor `D`, the constrained physical information declared actual at that anchor, and the current operational interface needed to specify the present situation.

It is **not** a complete future history.

Guard:

`same current quantum Actuality != same complete continuation`.

## QuantumContinuation

A `QuantumContinuation` is a physically admissible completion of the declared current quantum Actuality beyond the current anchor.

It must contain executable future physical structure: a continuation-specific schedule, physical map, constrained completion, or equivalent construction acting on the Stage 7 carrier.

It is not merely:

- a string label;
- a Python branch;
- a random seed;
- an unused metadata object;
- an event renaming.

Guard:

`different continuation labels != different physical continuations`.

## Continuation equivalence

Two continuation descriptions count as the same Stage 8 physical continuation when they differ only by a declared representational equivalence while preserving the designated physical observables and continuation diagnostics.

Pure renaming must therefore preserve the continuation equivalence class.

## QExt(D)

`QExt(D)` is the set of equivalence classes of physically admissible quantum continuations of the current quantum Actuality.

`QExt(D)` is a modal carrier. It is not itself a declaration that every represented extension is ontically real.

Guard:

`represented extension != ontically real future by definition`.

## Epistemic quantum Potentiality

`EPot_Q(D)` is a typed set of live continuation hypotheses in a model that already contains one selected complete continuation `h*`.

The epistemic weight `q_E(h|D)` represents uncertainty about which already-selected continuation is actual.

The hidden `h*` is a privileged internal datum and must not enter the pre-discriminating operational interface.

## Ontic-extension quantum Potentiality

`OPot_Q(D)` is a typed set of admissible continuations in a model that contains no selected complete future datum before update.

The ontic-extension model may contain continuation weights `K`, but it must not contain a hidden selector, seed-equivalent selector, precomputed outcome, or any other state that singles out a complete continuation.

Guard:

`no selected continuation field != proof that nature is ontically open`.

## Selected continuation

A selected continuation `h*` is a global model datum that singles out one complete member of `QExt(D)` before discriminating evidence arrives.

Its presence defines the Stage 8 epistemic-history model role.

Its absence from the ontic-extension model is a formal difference, not an empirical conclusion.

## Operational quantum interface

`O_Q` is an ontology-neutral interface exposing only declared current physical/record/next-outcome data.

It must not expose:

- model class names;
- `h*`;
- hidden selectors;
- privileged modal diagnostics.

Matched equality under `O_Q` means only operational underdetermination relative to that interface.

Guard:

`O_Q equality != modal identity`.

## Privileged modal diagnostic

A privileged modal diagnostic is a test-only capability that may inspect structural facts such as whether `h*` exists.

It is not a local observable unless a later protocol explicitly embeds such access physically.

Guard:

`internal distinguishability != operational accessibility`.

## Quantum continuation weight

Stage 8 distinguishes two numerically similar but semantically different weights:

- `q_E`: epistemic belief over an already-selected continuation;
- `K`: weight over admissible no-selected-future continuations.

Guard:

`same numerical weights != same probability semantics`.

## Actualization / update

An update extends the declared Actuality after explicitly supplied evidence.

Epistemic update retains the pre-existing `h*` and conditions beliefs.

Ontic-extension update grows Actuality and prunes `QExt` without introducing a hidden complete future.

Stage 8 does not identify this API update with collapse, ontological becoming, or phenomenal passage.

## P-V covariance

`P-V covariance` means that corresponding quantum continuation families and their modal semantics can be represented consistently under genuine Stage 7/8 clock-perspective transformations with explicit continuation/event correspondence.

It does not mean:

`P=V`.

Nor does it imply:

`perspective consistency => modal equivalence`.

## R-V compatibility

`R-V compatibility` means that a declared record-bearing physical construction and a declared V semantics can coexist consistently.

Stage 8 will test whether the same record-defined orientation can coexist with both epistemic and ontic-extension semantics.

If so, this is a finite-model counterexample to:

`record-defined direction => unique ontic-future semantics`.

It is not a proof about the ontology of the real future.

## O-V compatibility

`O-V compatibility` means that the same internal order/history anchor can support the declared V semantics.

Stage 8 must not define one modal semantics from the existence of `e0<e1<e2` alone.

Guard:

`internal order != ontic openness`.

## Superposition control

A coherent superposition over branch/continuation labels may be used as a physical control but is not, by itself, an `OPot_Q` witness.

Guard:

`superposition != ontic Potentiality by definition`.

## Density-matrix ambiguity

A density matrix can admit multiple decompositions and does not, by itself, specify whether one complete continuation is globally selected.

Guard:

`density matrix decomposition != unique modal semantics`.

## Integration success

Stage 8 counts V as integrated only if:

- `QExt` contains physically meaningful continuations acting on the constrained carrier;
- both typed modal semantics use that same continuation substrate;
- operational comparison is executable;
- update semantics are executable;
- genuine clock-perspective transport is eventually executable.

## Integration failure

Stage 8 is not considered integrated if the strongest construction is merely:

`Stage 7 quantum model + unrelated Stage 2 modal metadata`.

Guard:

`product decoration != integrated layer`.

## Evidence statuses

Stage 8 uses:

- `preserved`;
- `lost`;
- `reconstructible`;
- `inaccessible`;
- `not_established`;
- `not_applicable`.

The philosophical cautions remain:

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`not_established != false`.
