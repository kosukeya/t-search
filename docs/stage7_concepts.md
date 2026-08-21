# Stage 7 Concepts — Quantum Record / Perspective Vocabulary

Status: **frozen for Stage 7.0; provisional at the project level**.

This note fixes the vocabulary needed to put Stage 5 clock perspectives and Stage 3/6 record structure into one constrained quantum model without identifying them by notation.

## 1. Spectator memory

A **spectator memory** is an explicit subsystem `M` carried by the constrained model while no nontrivial record coupling acts on it.

Canonical Stage 7.0 baseline:

`H_M=C^2`, `H_M^(0)=0`.

A spectator memory is a control, not a record.

`memory present != record present`.

## 2. Record target

A **record target** is the explicitly declared observable/variable `Q` about which a memory readout is intended to carry information.

The target may be represented by a projector, a projective family, a POVM, or another typed observable, but its semantics must be fixed before the record diagnostic is evaluated.

## 3. Memory readout

A **memory readout** is the declared observable/channel through which information in `M` is locally or operationally accessed.

The global subsystem `M` can exist even when a particular perspective is denied access to its readout algebra.

## 4. Quantum record

A **quantum record of `Q`** is a target-specific correlation between the memory and `Q`, supported by an explicit measurement/information diagnostic and distinguished from no-record/wrong-target controls.

Nonzero entanglement or mutual information with an unspecified subsystem is insufficient.

## 5. Record-writing gate

A **record-writing gate** is a reversible controlled operation intended to correlate the memory with a declared target.

A minimal support-local binary form is:

`U_rec=Q tensor X_M + (I-Q) tensor I_M`.

Its unitarity is not by itself evidence of autonomous physical record formation.

## 6. Physical-subspace automorphism

A **physical-subspace automorphism** is a reversible map from the declared constrained physical subspace to itself.

It may be obtained by lifting a valid support operation through reduction/reconstruction.

It is distinct from a dynamically localized interaction:

`physical-subspace automorphism != time-localized dynamical interaction`.

## 7. Relationally localized record formation

A **relationally localized record-forming interaction** is a process whose event anchor is encoded internally in the constrained model rather than supplied by Python execution order.

If implementing it requires a modified constraint, all physical spaces and perspective maps must be recomputed from that modified constraint.

## 8. Record information

A **record-information diagnostic** measures information in the memory readout specifically about the declared target/event.

Possible diagnostics include:

- classical mutual information for a declared joint readout;
- Holevo information of conditional memory states;
- trace-distance distinguishability;
- target-specific discrimination error;
- quantum mutual information with explicit target semantics.

## 9. Record-defined orientation

A **record-defined orientation** is an asymmetric record-information profile across an explicitly ordered event/history structure.

A schematic contrast is:

`A_R=I(M;Q_past)-I(M;Q_future)`.

No orientation is inferred merely from `I(M;Q)>0`.

## 10. Perspective with memory

For Stage 7, a perspective remains a physical clock-relative description. In the spectator-memory baseline its support extends as:

`K_X^M=K_X tensor H_M`.

The factorization is a baseline property, not an assumption for interacting record models.

## 11. Record correspondence across perspectives

A cross-perspective record comparison requires four separately declared correspondences:

1. state/support transport;
2. event correspondence `chi`;
3. target-observable correspondence;
4. memory/readout-observable correspondence.

Equal clock labels or an unchanged memory tensor factor do not supply these correspondences automatically.

## 12. Record covariance

**Record covariance** means that corresponding target-specific record statistics agree under the declared perspective/event/observable transports.

For an orientation-preserving correspondence the same record structure is expected. For an orientation-reversing correspondence the expected sign transformation must be declared before evaluation.

`record covariance != identity of perspectives`.

## 13. Record accessibility

Stage 7 distinguishes:

- globally represented record information;
- reconstructible record information;
- locally accessible memory readout.

A hidden or maximally noisy readout may make a record locally unusable without deleting the global correlation.

## 14. Record ablation

A **record ablation** removes or neutralizes a declared record resource, for example:

- remove `M`;
- set `U_rec=I`;
- use maximally uncertain memory preparation;
- hide the local readout;
- replace the target with a wrong observable.

The resulting role status must distinguish `lost`, `reconstructible`, `inaccessible`, `not_applicable`, and `not_established` where appropriate.

## 15. Stage 7 model hierarchy

Stage 7 deliberately distinguishes three levels:

1. spectator-memory extension of the Stage 5 model;
2. reversible record-writing automorphism on a valid support/physical subspace;
3. internally anchored record-forming dynamics or modified constrained model.

A result at a lower level is not silently promoted to a stronger level.

## 16. Relationship to the Stage 6 layered candidate

Stage 7 does not assume the Stage 6 candidate is correct.

The hypothesis under pressure is:

`P`, `O`, and `R` remain distinct represented roles in one finite constrained quantum construction and are connected by nontrivial `Xi` compatibility conditions.

Stage 7 may strengthen, reduce, break, or fail to decide this hypothesis.
