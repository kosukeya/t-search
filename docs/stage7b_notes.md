# Stage 7B Notes — Reversible Quantum Record Witness

Status: **completed in the declared canonical support/physical-subspace family**.

## Question

Can the Stage 7 spectator-memory carrier support a reversible, target-specific quantum record witness without yet smuggling in a temporal orientation or an externally imposed history?

Stage 7B intentionally answers a narrower question than Stage 7C.  It constructs a reversible support-local record write and verifies its lift to the common constrained physical subspace.  It does **not** yet claim that the write happened at one relational time.

## Canonical perspective and target typing

The witness is declared in the A-clock perspective at clock reading `j=0`.

For the qutrit support, the A-clock rest ordering is `(B,C)`.

The explicit binary target is:

`Q = 1 iff B energy label == -1`.

The explicit wrong-target control is:

`W = 1 iff C energy label == +1`.

The memory readout is the computational qubit observable:

`Z_M = diag(+1,-1)`.

The source state is an equal superposition of four A-clock support basis pairs:

- `(-1,0)`;
- `(-1,1)`;
- `(0,0)`;
- `(0,1)`;

with memory initially in `|0>_M`.

This choice is deliberate: in the source distribution, `Q` and `W` are independently balanced.  Thus a controlled write of `Q` can be distinguished from generic correlation with `W`.

## Reversible write

On support coordinates:

`U_rec = Q tensor X_M + (I_K-Q) tensor I_M`.

The implementation also constructs an ambient completion that acts as identity outside the A-clock support.

Executable checks establish:

- support-coordinate unitarity;
- ambient unitarity;
- support preservation;
- involution / exact inverse property `U_rec^2=I`;
- applying the write twice returns the canonical source state.

Therefore the record witness is reversible.

Frozen interpretation:

`reversible record correlation != irreversible temporal arrow`.

## Target-specific information

The declared diagnostic is classical mutual information between the binary target readout and the computational memory readout.

Before the write:

`I(Q;M)=0`.

Under the identity/no-record control:

`I(Q;M)=0`.

After the intended controlled write:

`I(Q;M)=1 bit`.

For the independently balanced wrong target after the same write:

`I(W;M)=0`.

Thus the positive witness is not inferred merely from the presence of a memory tensor factor or from an arbitrary correlation.  The write produces information about the explicitly declared target and not about the declared independent wrong target.

Frozen guard:

`target-specific mutual information != record-defined temporal orientation`.

## Physical-subspace automorphism

Stage 7B lifts the support-local write through the Stage 7A reduction/reconstruction pair:

`U_phys = P_phys E_A^M(0) U_rec R_A^M(0) P_phys`.

The induced 14x14 matrix in the common physical-basis coordinates is unitary within tolerance.

A canonical physical source state is reconstructed from the A-clock support, transformed by `U_phys`, and checked to:

- remain in the Stage 7A constrained physical subspace;
- reduce back to the same recorded support state obtained by the direct support-local write.

This establishes a **physical-subspace automorphism** in the declared spectator constraint.

It does not establish an autonomous time-localized interaction.

Frozen guard:

`physical-subspace automorphism != time-localized dynamical interaction`.

## No directional claim in Stage 7B

Stage 7B defines no past/future ordering and no directional score `A_R`.

`directional_score_defined = false`.

That is intentional.  The protocol requires an internally modeled event/history relation before directional language is admissible.  Constructing that relational anchoring is the task of Stage 7C.

Consequently Stage 7B does **not** establish:

- record-defined temporal orientation;
- an arrow of time;
- ontological becoming;
- thermodynamic irreversibility;
- phenomenal passage;
- clock-change covariance of the record-bearing construction.

## Tests

Stage 7B adds 11 focused tests covering:

1. explicit target / wrong-target / memory-readout typing;
2. balanced independent source construction;
3. support-unitary reversibility;
4. ambient unitarity and support preservation;
5. one-bit intended target record;
6. zero wrong-target information;
7. identity/no-record control;
8. inverse recovery after a second write;
9. physical-subspace automorphism and constraint preservation;
10. diagnostic gate for a positive target-specific record witness;
11. non-directional interpretation guards.

Implementation-inclusive PR merge-ref regression:

`462 passed in 141.66s`.

## Stage 7B conclusion

Within the declared canonical qutrit A-clock support, an explicit reversible controlled write can create a target-specific one-bit memory record while an independently balanced wrong target remains unrecorded.  The write lifts to a unitary automorphism of the common Stage 7A physical subspace and preserves the spectator constraint.  This is executable evidence for a reversible quantum **record correlation witness**, not yet evidence for record formation along an internally modeled relational history or for a temporal arrow.

## Next

Stage 7C must introduce an internally anchored event/history construction and then test whether a directional record profile can be defined without identifying Python execution order with physical time.  Forward/reversed/balanced/no-record/uncertain-memory controls become central there.
