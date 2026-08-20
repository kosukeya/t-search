# Stage 4F — Operational and Negative Controls

Status: **implementation complete; final CI checkpoint pending documentation-inclusive head**.

## Purpose

Stage 4F tests which parts of the ideal finite Page--Wootters-style construction are operationally meaningful and which depend on the physical constraint or the chosen clock basis.

The checkpoint keeps four distinctions explicit:

`global conditional probability != local probability by definition`

`formal clock conditioning != physical Page--Wootters dynamics`

`vector change != ray/density-matrix change`

`arbitrary clock basis != ideal relational time basis`.

## 1. Global/local Born consistency

For a system projector `Pi`, define:

`P_global(a|t_j)=<Psi|(|t_j><t_j| tensor Pi)|Psi> / <Psi|(|t_j><t_j| tensor I)|Psi>`.

The local clock-relative state predicts:

`P_local(a|t_j)=<psi_j|Pi|psi_j>`.

Stage 4F uses the non-energy-diagonal projector:

`Pi_+=|+><+|`,

with:

`|+>=(|0>+|1>)/sqrt(2)`.

This projector does not commute with `H_S`, so it exposes actual reading dependence rather than a trivially constant observable.

For the equal-amplitude `d=4` physical state, the analytic profile is:

`[1/2, 1/4, 0, 1/4]`.

Both the global conditional formula and the local Born rule must reproduce this profile.

The equality is also checked for a generic complex physical coefficient vector and in `d=5`.

## 2. Constraint-violating formal-conditioning control

Use:

`|Phi_bad>=(|0>_C|0>_S+|0>_C|1>_S)/sqrt(2)`.

This is not in `ker(H_tot)`.

Because its clock sector is fixed at clock energy `0`, formal DFT-clock conditioning gives the same normalized system vector at every reading:

`(|0>_S+|1>_S)/sqrt(2)`.

However the expected system Schrödinger evolution changes the relative phase between `|0>` and `|1>`.

Therefore the formal conditional sequence fails the Stage 4C Schrödinger relation for nonzero clock steps.

This implements the guard:

`being decomposable by clock readings != satisfying the Page--Wootters physical constraint`.

The physical global conditional Born API also rejects this nonphysical state.

## 3. Single-energy physical control

Use the physical product state:

`|Psi_triv>=|1>_C|1>_S`.

It satisfies the constraint, and its clock-relative vectors are:

`|psi_j>=exp(-i t_j)|1>_S`.

For `j=0` and `j=1` in `d=4`, the vectors differ by phase and have nonzero vector distance. But:

`fidelity(|psi_0>,|psi_1>)=1`,

and:

`rho_0=rho_1=|1><1|`.

Thus:

`constraint satisfaction != nontrivial relational ray change`.

The implementation explicitly distinguishes vector equality, pure-state ray fidelity, and density-matrix equality.

## 4. Wrong-clock-basis control

Conditioning on the clock energy basis rather than the DFT time basis gives:

`(<m|_C tensor I)|Psi_c>=c_m |m>_S`.

On physical coefficient coordinates, this is the matrix:

`Q_m=|m><m|`.

For `d=4`:

`rank(Q_m)=1`,

`nullity(Q_m)=3`.

Thus the clock-energy-basis projection is many-to-one even on `H_phys`, unlike the ideal DFT time-basis reduction `R_j`, which Stage 4D showed to be invertible/isometric.

A constructive witness uses two distinct physical coefficient vectors with the same coefficient in sector `m`; they have identical `Q_m` output while differing elsewhere.

The same rank-one/nullity-`d-1` structure is checked in `d=5`.

## Interpretation guard

These controls identify properties of the chosen ideal finite construction. They do not show that there is a unique physically correct quantum clock basis in general, nor that the Page--Wootters representation settles the ontology of time.

The supported distinction is narrower:

**within this matched-energy toy model, the DFT clock-reading basis supports a reversible physical reduction and operationally consistent conditional dynamics, whereas clock-energy-basis conditioning discards physical coefficient sectors and constraint-violating histories do not satisfy the same relational Schrödinger structure.**

Next: Stage 4G — robustness and synthesis.
