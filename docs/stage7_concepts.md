# Stage 7 Concepts — Quantum Record / Perspective Vocabulary

Status: **frozen at Stage 7.0 and extended through Stage 7E; provisional at the project level**.

This note fixes the vocabulary needed to place physical clock perspectives and quantum record structure inside one constrained model without identifying distinct roles by notation.

## 1. Spectator memory

A **spectator memory** is an explicit subsystem `M` carried by the constrained model while no nontrivial record coupling acts on it.

Canonical baseline: `H_M=C^2`, `H_M^(0)=0`.

A spectator memory is a control, not a record:

`memory present != record present`.

## 2. Record target

A **record target** is the explicitly declared observable/variable `Q` about which a memory readout is intended to carry information. Its semantics must be fixed before the record diagnostic is evaluated.

## 3. Memory readout and access channel

A **memory readout** is the declared observable through which information in `M` is addressed. A **local access channel** is the interface mapping the physical memory result to what a local perspective may actually read.

Stage 7E distinguishes exact, hidden, maximally noisy, and coarse channels while keeping the global physical state fixed.

`same memory tensor factor != same accessible record across perspectives`.

`locally inaccessible record != globally absent record`.

## 4. Quantum record

A **quantum record of `Q`** is a target-specific correlation between the memory and `Q`, supported by an explicit measurement/information diagnostic and distinguished from no-record/wrong-target controls.

Nonzero entanglement or mutual information with an unspecified subsystem is insufficient.

## 5. Record-writing gate

A **record-writing gate** is a reversible controlled operation intended to correlate the memory with a declared target.

A minimal support-local binary form is:

`U_rec=Q tensor X_M + (I-Q) tensor I_M`.

Its unitarity is not by itself evidence of autonomous physical record formation.

## 6. Physical-subspace automorphism

A **physical-subspace automorphism** is a reversible map from the declared constrained physical subspace to itself. It is distinct from a dynamically localized interaction:

`physical-subspace automorphism != time-localized dynamical interaction`.

## 7. Relationally localized record formation

A **relationally localized record-forming interaction** is a process whose event anchor is encoded internally in the constrained model rather than supplied by Python execution order.

If implementing it requires a modified constraint, all physical spaces and perspective maps must be recomputed from that modified constraint.

## 8. Record information

A **record-information diagnostic** measures information in the memory readout specifically about the declared target/event. Examples include classical mutual information for a declared joint readout, Holevo information, trace-distance distinguishability, target-specific discrimination error, or quantum mutual information with explicit target semantics.

## 9. Record-defined orientation

A **record-defined orientation** is an asymmetric record-information profile across an explicitly ordered event/history structure.

Canonical Stage 7C contrast:

`A_R=I(M_e1;Q_e0)-I(M_e1;Q_e2)`.

An independent accessibility contrast is:

`A_acc=Acc(Q_e0|M_e1)-Acc(Q_e2|M_e1)`.

No orientation is inferred merely from `I(M;Q)>0`.

## 10. Perspective with memory

A perspective remains a physical clock-relative description. In the spectator-memory baseline its support factorizes as `K_X^M=K_X tensor H_M`; this factorization is not assumed for the interacting record model.

## 11. Interacting perspective chart

After record interaction modifies the constrained model, a clock/readout node `(X,j)` is represented by the image of the re-derived reduction from the common modified physical space.

Stage 7D shows that these charts can remain full-rank even when the reductions cease to be Euclidean isometries.

## 12. Induced physical metric

If the re-derived reduction in orthonormal image coordinates is `y_X=C_X c`, the chart inherits the physical inner product through

`G_X=C_X^{-dagger} C_X^{-1}`.

The interacting clock change

`S_{Y<-X}=C_Y C_X^{-1}`

is physically metric-preserving when

`S^dagger G_Y S=G_X`.

Therefore:

`non-Euclidean-unitary map != failed perspective map when the induced physical metric is preserved`.

## 13. Record correspondence across perspectives

A cross-perspective record comparison requires separately declared:

1. state/support transport;
2. event correspondence `chi`;
3. target-observable correspondence;
4. memory/readout-observable correspondence.

Equal clock labels or an unchanged memory tensor factor do not provide these automatically.

## 14. Record covariance

**Record covariance** means that corresponding target-specific record statistics agree under declared perspective/event/observable transports.

For orientation-preserving correspondence the same record structure is expected; for orientation-reversing correspondence the sign transformation must be declared before evaluation.

`record covariance != identity of perspectives`.

`P-R covariance != P=R`.

## 15. Global representation, reconstructibility, and accessibility

Stage 7 distinguishes:

- **globally represented record**: record-bearing state/operator structure exists in the common physical construction;
- **reconstructible record**: the record can be recovered using the declared model and admissible perspective maps, possibly through an indirect path;
- **locally accessible record**: the declared local readout interface retains usable information about the target.

A hidden or maximally noisy interface may eliminate local information without changing global representation. A coarse channel may retain orientation with reduced information.

`global reconstructibility != local accessibility`.

## 16. Partial perspective atlas

A **partial perspective atlas** contains a declared subset of primitive perspective edges. A target chart may be indirectly reconstructible even when its requested direct primitive edge is unavailable.

Stage 7E removes `A/e1 -> B/e0` while retaining three paths through `C/e0,e1,e2`.

`indirect reconstructibility != direct local edge availability`.

`partial atlas path consistency != universal frame availability`.

## 17. Localized atlas perturbation

A **localized edge perturbation** changes one declared primitive perspective edge and tests whether failures remain confined to paths that use it.

A path may fail state/metric/statistical consistency even if a tested observable algebra still transforms by similarity because the perturbation commutes with that algebra.

`observable-algebra correspondence != full state/metric path consistency`.

A finite algebraic path residual is not spacetime curvature without an independent physical derivation:

`localized path inconsistency != spacetime curvature`.

## 18. Record ablation

A **record ablation** removes or neutralizes a declared resource, for example removing `M`, setting `U_rec=I`, using maximally uncertain memory preparation, hiding the local readout, replacing the target, removing valid perspective transport, or corrupting `chi`.

The resulting role status must distinguish `lost`, `reconstructible`, `inaccessible`, `not_applicable`, and `not_established` where appropriate.

## 19. Stage 7 model hierarchy

Stage 7 distinguishes:

1. spectator-memory extension of Stage 5;
2. reversible record-writing automorphism on a valid support/physical subspace;
3. internally anchored record-bearing modified constrained model;
4. re-derived interacting multi-clock metric atlas;
5. local access channels and partial-atlas reconstruction.

A result at a lower level is not silently promoted to a stronger level.

## 20. Relationship to the Stage 6 layered candidate

Stage 7 does not assume the Stage 6 candidate is correct.

The hypothesis under pressure is:

`P`, `O`, and `R` remain distinct represented roles in one finite constrained quantum construction and are connected by nontrivial `Xi` compatibility conditions.

Stage 7A–E provide increasingly strong single-model compatibility witnesses; Stage 7F must now test minimality by ablation before Stage 7G decides whether the layered candidate is strengthened, reduced, broken, or remains inconclusive.