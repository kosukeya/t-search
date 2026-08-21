# Stage 7 Protocol — Quantum Records in a Constrained Multi-Clock Model

Status: **Stage 7.0 protocol frozen; Stage 7A–7E completed; Stage 7F is next.**

Stage 7 follows the Stage 6G evidence-selected gate. The earlier roadmap chronology is **superseded by the Stage 6G gate selection**: before attempting a generally covariant / gravitational extension, place an explicit memory degree of freedom and record semantics inside the constrained multi-clock quantum construction and pressure-test them under genuine clock changes.

The Stage 6 candidate entering Stage 7 is:

`T6_candidate=(O,P,R,V;Xi)`

with the tested quantum operational-correspondence role `Omega` reconstructible from perspective transport in the declared Stage 5/6 operator interface.

Stage 7 primarily pressure-tests `P`, `O`, and `R`. It does not yet integrate `V` into the same quantum construction.

## 1. Central question

> In one constrained finite quantum model containing multiple admissible internal clock perspectives and an explicit memory degree of freedom, does record-defined temporal structure remain distinct from perspective transformation and neutral order while transforming consistently under genuine clock changes?

A positive result strengthens the Stage 6 layered candidate by removing the former product-model separation between Stage 5 `P` and Stage 3/6E `R`. A negative result must instead revise that candidate if record structure reduces to retained `P/O/Xi`, fails covariance, or destroys the perspective structure required for the comparison.

## 2. Scope and non-goals

Stage 7 is a finite constrained-quantum pressure test. It does not establish a fundamental ontology of time, ontological becoming, phenomenal passage, a thermodynamic arrow, universal quantum-reference-frame availability, general covariance of gravity, realistic time dilation, or a new empirical prediction.

The former roadmap item assigning Stage 7 directly to a generally covariant / gravitational extension is deferred rather than discarded.

## 3. Inherited finite-model evidence

From Stage 5, the ideal three-clock model supplied a common constrained physical Hilbert space and support maps

`R_X(j): H_phys -> K_X`,

`E_X(j): K_X -> H_phys`,

`S_{Y<-X}(k,j)=R_Y(k)E_X(j)`.

From Stage 3 / Stage 6E, reversible dynamics can support record-information asymmetry, reversal, cancellation controls, and a distinction between global record representation and local accessibility.

From Stage 6, the current structural candidate is layered: `O`, `P`, `R`, and `V` remain functionally non-reconstructed under the declared one-layer ablations while non-trivial `Xi` compatibility relations connect them. `not_established` remains distinct from `false`.

## 4. Stage 7 carrier and baseline

The canonical carrier is

`H_kin^7 = H_A tensor H_B tensor H_C tensor H_M`,

with `H_M=C^2`.

For Stage 7A spectator memory:

`H_M^(0)=0`,

`H_tot^(0)=H_tot^(5) tensor I_M`.

The spectator model is a strict no-record control. A memory tensor factor alone is not a record.

Stage 7A verified:

- `dim(H_kin^7A)=54`;
- `dim(H_phys^7A)=14`;
- 14-dimensional per-clock supports in 18-dimensional reduced ambient spaces;
- reduction/reconstruction round trips;
- 54 distinct-clock comparisons and 162 three-clock composition cases;
- zero target-memory information in the spectator control.

## 5. Record semantics

A Stage 7 record claim requires an explicit target variable/operator, explicit memory readout, target-specific information diagnostic, appropriate no-record/wrong-target controls, and an explicit event/history correspondence before a directional interpretation is made.

Frozen guards include:

- `memory present != record present`;
- `entanglement != record`;
- `mutual information != directional record by itself`;
- `record correlation != record-defined temporal orientation`.

Stage 7B uses the target `Q=[B energy label == -1]`, wrong target `W=[C energy label == +1]`, computational memory readout, and reversible controlled write

`U_rec = Q tensor X_M + (I-Q) tensor I_M`.

The intended write raises `I(Q;M)` from `0` to `1 bit`, while identity/no-record and wrong-target controls remain zero. The write is reversible and lifts to a physical-subspace automorphism. No directional score is inferred from Stage 7B alone.

## 6. Relational record formation

Stage 7C embeds an internal three-event history into a modified constraint:

`e0 < e1 < e2`,

`W_hist = sum_j |t_j><t_j|_A tensor V_j`,

`H_hist = W_hist H_tot^(0) W_hist^dagger`.

Forward schedule:

- `V_0=I`;
- `V_1=U_rec`;
- `V_2=U_scr U_rec`.

The scrambler implements `X -> X XOR N`, with `X=1 iff B=-1` and `N=1 iff C=+1` on the declared balanced source sector.

Because the constraint changes, the physical space and interacting reductions/maps are re-derived rather than inherited unchanged.

At current event `e1`, the directional diagnostics are

`A_R = I(M_e1;Q_e0) - I(M_e1;Q_e2)`,

`A_acc = Acc(Q_e0|M_e1) - Acc(Q_e2|M_e1)`.

Stage 7C gives:

- forward: `A_R=+1`, `A_acc=+1/2`, `lower-index`;
- explicit reversed history: `A_R=-1`, `A_acc=-1/2`, `upper-index`;
- balanced forward/reverse meta-ensemble: both signed scores cancel;
- no-record history: both cancel;
- maximally mixed-memory control: both cancel.

Frozen guards:

- `simulation/intervention order != modeled temporal order`;
- `physical-subspace automorphism != time-localized dynamical interaction`;
- `clock-conditioned conjugated constraint != unique autonomous interaction Hamiltonian`;
- `record-defined orientation != thermodynamic arrow / ontological becoming / phenomenal passage`.

## 7. Event and perspective typing

Stage 7 keeps distinct:

- horizontal perspective transformations `S_{q<-p}`;
- vertical modeled history/order relations;
- explicit event correspondence `chi_{q<-p}`;
- target and memory observables.

Equal numeric clock readings do not identify events across perspectives.

`P-R covariance != P=R`.

## 8. Stage 7D — genuine clock-change record covariance — completed

The Stage 7C modified physical space was independently reduced at all nine clock/readout nodes `(X,j)`, `X in {A,B,C}`, `j in {0,1,2}`.

All nine reductions retain rank `14`. A-clock reductions remain Euclidean isometries, while B/C reductions are full-rank but non-isometric. Canonical clock probabilities become:

- A: `[1/3,1/3,1/3]`;
- B: `[4/9,5/18,5/18]`;
- C: `[7/18,7/18,2/9]`.

Writing the reduction in orthonormal image coordinates as `y_X=C_X c`, Stage 7D defines the induced physical metric

`G_X=C_X^{-dagger} C_X^{-1}`

and the interacting clock change

`S^hist_{Y<-X}=C_Y C_X^{-1}`.

All 54 directed distinct-clock/readout comparisons satisfy state transport, inverse consistency, corresponding-observable transport, and

`S^dagger G_Y S = G_X`

within tolerance. Thus the record interaction deforms the ideal Euclidean-unitary Stage 5/7A atlas into a nonideal induced-metric-preserving atlas rather than destroying the perspective structure.

Physical record observables are represented in each chart by

`O_X=C_X O_phys C_X^{-1}`

and are idempotent and `G_X`-self-adjoint, with the required commuting readouts.

Explicit event correspondences are:

- preserving: `e0->e0`, `e1->e1`, `e2->e2`;
- reversing: `e0->e2`, `e1->e1`, `e2->e0`.

Across all nine nodes, preserving `chi` yields `A_R=+1`, `A_acc=+1/2`; reversing `chi` yields `A_R=-1`, `A_acc=-1/2`.

Negative controls show that the inherited Stage 7A spectator map, an untransported bare observable, and a misdeclared `chi` do not satisfy the corresponding interacting comparison.

## 9. Stage 7E — accessibility and partial-atlas consistency — completed

Stage 7E holds the common physical record state and record operators fixed while changing only the declared local memory-readout interface.

Four interfaces are tested at all nine Stage 7D nodes:

- `full`: exact memory readout;
- `hidden`: both memory values mapped to one visible output;
- `maximally-noisy`: binary-symmetric channel with crossover `1/2`;
- `coarse`: binary-symmetric channel with crossover `1/4`.

Results:

- full: local `A_R=+1`, `A_acc=+1/2`;
- hidden: global record remains represented, local `A_R=0`, `A_acc=0`, orientation `none`;
- maximally-noisy: global record remains represented, local `A_R=0`, `A_acc=0`, orientation `none`;
- coarse: global record remains represented, local `A_R=1-H_2(1/4) ~= 0.1887218755`, local `A_acc=1/4`, orientation remains `lower-index`.

Therefore:

`locally inaccessible record != globally absent record`.

For the partial atlas, the primitive edge

`A/e1 -> B/e0`

is declared unavailable. Three indirect paths through `C/e0`, `C/e1`, and `C/e2` reproduce the omitted direct-map oracle, state, induced metric, corresponding record observables, `A_R=+1`, and `A_acc=+1/2` within tolerance.

Only `C/e1 -> B/e0` is then perturbed. Its path develops nonzero map/state/metric/record-statistic residuals while the other two paths remain consistent. The chosen perturbation commutes with the tested projector algebra, so observable similarity transport remains numerically exact even though full path consistency fails. This yields the additional guard:

`observable-algebra correspondence != full state/metric path consistency`.

Further guards:

- `global reconstructibility != local accessibility`;
- `indirect reconstructibility != direct local edge availability`;
- `partial atlas path consistency != universal frame availability`;
- `localized path inconsistency != spacetime curvature`.

## 10. Required negative controls

The Stage 7 program includes, where applicable:

- spectator memory / no record coupling;
- `U_rec=I`;
- wrong target;
- maximally mixed memory;
- explicit reversed history;
- balanced forward/reverse meta-ensemble;
- untransported bare observable;
- wrong/misdeclared `chi`;
- hidden/noisy/coarse memory interfaces;
- perturbed local perspective edge;
- rejection of invalid physical-domain assumptions.

No single residual is required to fail when independent diagnostics already distinguish the perturbation; diagnostic separability is preserved rather than forcing all controls to fail in the same way.

## 11. Evidence taxonomy

Every Stage 7 claim is one of:

1. **Executable witness** — recomputed from a declared model;
2. **Established finite-model result** — supported by executable witnesses and regressions in the declared family;
3. **Candidate structural interpretation** — synthesis across witnesses;
4. **Untested / not established** — no current witness decides the claim.

Hand-written verdict booleans copied from prose are not executable evidence.

## 12. Stage 7 sequence

- **Stage 7.0 — protocol freeze — completed**
- **Stage 7A — spectator-memory constrained baseline — completed**
- **Stage 7B — reversible quantum record witness — completed**
- **Stage 7C — relational record formation and orientation controls — completed**
- **Stage 7D — genuine clock-change record transport — completed**
- **Stage 7E — accessibility and partial-atlas record consistency — completed**
- **Stage 7F — ablation / reconstruction / mismatch matrix — next**
- **Stage 7G — synthesis and Stage 8 gate — planned**

Stage 7F must neutralize or remove memory/record/perspective/access/correspondence ingredients one at a time and classify the resulting role as `lost`, `reconstructible`, `inaccessible`, or `not_established` without inferring metaphysical fundamentality from software-level ablation.

## 13. Candidate Stage 8 gates

Stage 7G should rank at least:

- integrate explicit `V` / extension semantics into the same relational quantum construction;
- move to richer causal/order structure;
- test interacting, nonideal, or POVM clocks;
- if the finite layered architecture is stable enough, begin a parametrized / generally covariant precursor.

The gravitational direction remains deferred, not discarded.

## 14. Frozen interpretation guards

Stage 7 inherits prior guards and includes:

- `memory subsystem != conscious observer`;
- `memory present != record present`;
- `entanglement != record`;
- `mutual information != directional record by itself`;
- `record correlation != record-defined temporal orientation`;
- `record orientation != thermodynamic entropy arrow`;
- `record orientation != causal influence by definition`;
- `record orientation != ontological becoming`;
- `record orientation != phenomenal passage`;
- `perspective change != temporal succession`;
- `P-R covariance != P=R`;
- `same memory tensor factor != same accessible record across perspectives`;
- `support-local unitary != autonomous physical interaction`;
- `physical-subspace automorphism != time-localized dynamical interaction`;
- `simulation/intervention order != modeled temporal order`;
- `constraint preservation != nontrivial record formation`;
- `clock-conditioned conjugated constraint != unique autonomous interaction Hamiltonian`;
- `modeled history reversal != fundamental time-reversal symmetry`;
- `balanced forward/reverse meta-ensemble != one pure physical state under one constraint`;
- `interacting clock change != inherited spectator clock change`;
- `non-Euclidean-unitary map != failed perspective map when the induced physical metric is preserved`;
- `G-self-adjoint observable != arbitrary non-Hermitian observable`;
- `equal numeric clock readings != event identity`;
- `locally inaccessible record != globally absent record`;
- `indirect reconstructibility != direct local edge availability`;
- `partial atlas path consistency != universal frame availability`;
- `localized path inconsistency != spacetime curvature`;
- `observable-algebra correspondence != full state/metric path consistency`;
- `success with finite clocks != general covariance`;
- `Stage 7 synthesis != empirical discovery unless a new discriminating prediction is independently derived`.

## 15. Stop / revise conditions

Revise rather than force a positive conclusion if record is inferred only from entanglement; target/event correspondence is undeclared; Python execution order is used as physical temporal order; a modified constraint silently reuses old interacting maps; a cross-perspective comparison leaves a bare observable untransported; local hiding is described as global destruction; reversal is only sign relabeling; `not_established` is converted to `false`; or an ablation is interpreted as metaphysical fundamentality.

## 16. Stage 7 exit criteria

Stage 7 is complete only when all applicable criteria are satisfied.

### Protocol / typing — 1–5

1. common constrained carrier with explicit memory declared;
2. perspective arrows, history/order, event correspondences, target observables, and memory observables separately typed;
3. record correlation and record-defined orientation distinguished;
4. physical-subspace automorphism and relationally localized interaction distinguished;
5. evidence classes and failure statuses auditable.

Satisfied by Stage 7.0 and maintained through Stage 7E.

### Baseline — 6–9

6. spectator-memory model reproduces inherited constrained structure;
7. per-clock spectator reductions/reconstructions satisfy round trips;
8. spectator clock-change maps satisfy inherited inverse/composition tests;
9. spectator memory alone gives no positive record witness.

Satisfied by Stage 7A.

### Record witness — 10–14

10. explicit target and memory readout;
11. reversible record-writing construction;
12. intended coupling increases target-specific information;
13. wrong-target/no-record controls distinguish intended record semantics;
14. directional score is attached to explicit modeled history/events.

10–13 satisfied by Stage 7B; 14 by Stage 7C.

### Reversal / controls — 15–18

15. no-record coupling control;
16. uncertain/mixed-memory control;
17. explicit inverse/reversed construction;
18. balanced forward/reverse cancellation.

Satisfied through Stage 7C.

### Cross-perspective transport — 19–25

19. common record-bearing physical construction represented in multiple genuine clock perspectives;
20. corresponding record observables transported;
21. explicit `chi`;
22. preserving record covariance;
23. reversing predeclared sign rule;
24. same-bare-observable negative control;
25. wrong/misdeclared `chi` control.

Satisfied by Stage 7D in the declared canonical interacting family.

### Accessibility / atlas — 26–29

26. global record representation distinguished from local memory access;
27. hidden/noisy memory controls tested;
28. indirect perspective path tested under a partial atlas;
29. perturbed local edge produces localized inconsistency.

Satisfied by Stage 7E in the declared canonical family. Criterion 29 is witnessed jointly by map/state/metric/record-statistic failure on the perturbed `C/e1 -> B/e0` path while the unaffected indirect paths remain consistent; the tested projector-algebra similarity can remain intact and is not treated as sufficient for full consistency.

### Minimality / synthesis — 30–36

30. memory/record/perspective/access ingredients ablated or neutralized one at a time where applicable;
31. `lost`, `reconstructible`, `inaccessible`, and `not_established` distinguished;
32. Stage 7G decides whether the Stage 6 layered candidate is strengthened, reduced, broken, or inconclusive;
33. unresolved implications remain `not_established` unless directly decided;
34. Stage 8 gate selected by discriminating power;
35. interpretation guards preserved in synthesis;
36. final full regression and PR merge-readiness review have no unresolved blocker.

Criteria 30–36 remain for Stage 7F–G and final merge-readiness review.