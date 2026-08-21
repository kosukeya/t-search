# Stage 7 Concepts — Quantum Record / Perspective Vocabulary

Status: **frozen at Stage 7.0 and extended through Stage 7G; provisional at the project level**.

This note fixes the vocabulary needed to place physical clock perspectives and quantum record structure inside one constrained model without identifying distinct roles by notation.

## 1. Spectator memory

A **spectator memory** is an explicit subsystem `M` carried by the constrained model while no nontrivial record coupling acts on it.

Canonical baseline: `H_M=C^2`, `H_M^(0)=0`.

`memory present != record present`.

## 2. Record target

A **record target** is the explicitly declared observable/variable `Q` about which a memory readout is intended to carry information. Its semantics must be fixed before the record diagnostic is evaluated.

## 3. Memory readout and access channel

A **memory readout** is the declared observable through which information in `M` is addressed. A **local access channel** maps the physical memory result to what a local perspective may actually read.

Stage 7E distinguishes exact, hidden, maximally noisy, and coarse channels while keeping the global physical state fixed.

`same memory tensor factor != same accessible record across perspectives`.

`locally inaccessible record != globally absent record`.

## 4. Quantum record

A **quantum record of `Q`** is a target-specific correlation between memory and `Q`, supported by an explicit information diagnostic and distinguished from no-record / wrong-target controls.

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

A **record-information diagnostic** measures information in the memory readout specifically about the declared target/event. Stage 7 uses classical target-memory mutual information and an independent Bayes-optimal discrimination score.

## 9. Record-defined orientation

A **record-defined orientation** is an asymmetric record-information profile across an explicitly ordered event/history structure.

Canonical Stage 7C contrasts:

`A_R=I(M_e1;Q_e0)-I(M_e1;Q_e2)`

and

`A_acc=Acc(Q_e0|M_e1)-Acc(Q_e2|M_e1)`.

No orientation is inferred merely from `I(M;Q)>0`.

`target-specific record correlation != record-defined direction`.

## 10. Perspective with memory

A perspective remains a physical clock-relative description. In the spectator-memory baseline its support factorizes as `K_X^M=K_X tensor H_M`; this factorization is not assumed for the interacting record model.

## 11. Interacting perspective chart

After record interaction modifies the constrained model, a clock/readout node `(X,j)` is represented by the image of the re-derived reduction from the common modified physical space.

Stage 7D shows that these charts can remain full-rank even when the reductions cease to be Euclidean isometries.

## 12. Induced physical metric

If the re-derived reduction in image coordinates is `y_X=C_X c`, the chart inherits

`G_X=C_X^{-dagger} C_X^{-1}`.

The interacting clock change

`S_{Y<-X}=C_Y C_X^{-1}`

is physically metric-preserving when

`S^dagger G_Y S=G_X`.

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

- **globally represented record** — record-bearing state/operator structure exists in the common physical construction;
- **reconstructible record** — the record can be recovered using the declared model and admissible perspectives, possibly through an indirect path;
- **locally accessible record** — the declared local readout interface retains usable target information.

A hidden or maximally noisy interface may eliminate local information without changing global representation. A coarse channel may retain orientation with reduced information.

`global reconstructibility != local accessibility`.

## 16. Partial perspective atlas

A **partial perspective atlas** contains a declared subset of primitive perspective edges. A target chart may be indirectly reconstructible even when its requested direct primitive edge is unavailable.

Stage 7E removes `A/e1 -> B/e0` while retaining three paths through `C/e0,e1,e2`.

`indirect reconstructibility != direct local edge availability`.

`partial atlas path consistency != universal frame availability`.

## 17. Localized atlas perturbation

A **localized edge perturbation** changes one primitive perspective edge and tests whether failures remain confined to paths that use it.

A path may fail state/metric/statistical consistency even if a tested observable algebra still transforms by similarity because the perturbation commutes with that algebra.

`observable-algebra correspondence != full state/metric path consistency`.

`localized path inconsistency != spacetime curvature`.

## 18. Stage 7F role status

Stage 7F uses five functional statuses:

- **preserved** — the role remains directly represented after neutralization;
- **reconstructible** — an explicit ingredient is absent but the role is recovered from retained declared structure;
- **inaccessible** — the global role remains represented but the declared local interface cannot access it;
- **lost** — the baseline role is removed by the declared ablation with no reconstruction witness;
- **not_established** — the retained structure does not license a verdict.

These are evidence statuses, not ontological categories.

`lost != metaphysically irreducible`.

`reconstructible != universally redundant`.

`not_established != false`.

## 19. Memory removal versus hidden memory

**Memory removal** removes `M` from the retained record carrier; target-memory information no longer exists in that ablated representation.

**Hidden memory** leaves the global memory-record relation intact but removes local access to the readout.

Therefore Stage 7F classifies memory removal as record `lost`, while hidden/noisy access is `inaccessible`.

## 20. Record-coupling ablation

A **record-coupling ablation** neutralizes the record write while retaining the internally anchored history and tested perspective carrier.

The Stage 7C no-record family provides the canonical witness: the multi-clock perspective structure and `e0<e1<e2` anchor remain, while `A_R=A_acc=0` and no record-defined direction is present.

Thus, in the declared Stage 7 family:

`P + internal O => R`

is refuted.

This is a model-family counterexample, not a universal impossibility theorem.

## 21. History-anchor ablation

A **history-anchor ablation** retains target-specific record correlation but removes the internally modeled lower/current/upper event structure required for a directional score.

Stage 7B supplies this witness: `I(Q;M)=1 bit` after recording, but no directional score is defined.

Therefore record correlation survives while record-defined direction is `not_established`.

## 22. Explicit edge-map reconstruction

An **explicit perspective edge** is the matrix representation used to transport between two declared perspective charts.

Stage 7F removes those explicit matrices while retaining the common physical carrier and per-node reductions `C_X`, then reconstructs

`S_{Y<-X}=C_Y @ inv(C_X)`.

The explicit edge-matrix representation is therefore `reconstructible` in the declared interface.

This does not eliminate the perspective layer because the reconstruction still uses the common carrier and per-perspective reductions.

`explicit perspective-map reconstruction != elimination of the perspective layer`.

## 23. Missing versus wrong event correspondence

If `chi` is **missing**, local P and local R can remain represented while the cross-perspective P-R statement is untyped:

`P_R_covariance = not_established`.

If `chi` is **wrong or misdeclared**, the comparison is executable and fails its predeclared covariance rule. Stage 7F keeps these two cases distinct.

`missing chi != false covariance`.

`wrong chi mismatch != destruction of P or R`.

## 24. Stage 7 model hierarchy

Stage 7 distinguishes:

1. spectator-memory extension of Stage 5;
2. reversible record-writing automorphism;
3. internally anchored record-bearing modified constraint;
4. re-derived interacting multi-clock metric atlas;
5. local access channels and partial-atlas reconstruction;
6. ablation / reconstruction / mismatch classification;
7. synthesis and evidence-selected gate ranking.

A result at a lower level is not silently promoted to a stronger level.

## 25. Strengthened layered core

A **strengthened layered core** is the Stage 7G synthesis classification for the P/O/R portion of the Stage 6 candidate.

It requires both:

- positive compatibility in one common construction, especially `Xi_PR`; and
- a separating countermodel/ablation where retained P plus internal O do not reconstruct R.

Stage 7G therefore uses `strengthened` rather than `reduced`, `broken`, or `inconclusive`.

This is a structural classification inside the declared finite-model family:

`strengthened finite-model candidate != fundamental ontology`.

## 26. Derived representation inside P

Stage 7 does not treat every piece of a retained layer as equally primitive.

The explicit cross-clock edge matrices are reconstructed from the common physical carrier and the per-perspective reduction data. Therefore one can simultaneously say:

- P remains a separate represented role;
- explicit P edge matrices are derived in the current implementation.

`derived edge representation != derived/redundant perspective layer`.

## 27. Unintegrated V

`V` denotes the Stage 2/6 Potentiality / extension-semantics layer.

After Stage 7, V is the only explicit Stage 6 layer not yet integrated into the shared constrained quantum construction. Stage 6E supports typed P-V extension transport, but Stage 7 does not identify V with:

- Born probability;
- quantum randomness;
- superposition;
- sampling;
- measurement outcome selection;
- ignorance about an already selected history.

Stage 8 must preserve the distinction between epistemic selected-history uncertainty and ontic no-selected-future extension structure unless an executable witness collapses that distinction.

`Potentiality != quantum randomness by definition`.

## 28. Relationship to the Stage 6 layered candidate

The project-level candidate remains provisionally:

`T_candidate=(O,P,R,V;Xi)`.

After Stage 7 the evidence is asymmetric:

- P/O/R and especially `Xi_PR` are strengthened by single-model constrained-quantum evidence;
- explicit edge matrices inside P are reconstructible;
- V remains explicit but separately modeled;
- the tested Omega role remains derived in the Stage 5/6 operator interface.

Stage 7G selects V integration as the next evidence gate because it is the cleanest remaining model-separation weakness.
