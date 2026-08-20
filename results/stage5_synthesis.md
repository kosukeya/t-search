# Stage 5 Synthesis — Change of Clock / Perspective

Status: **Stage 5A--5G scientific implementation complete; final documentation-inclusive CI and merge-readiness review pending.**

## 1. Stage 5 question

Stage 4 showed that one fixed ideal finite clock supports reversible clock-relative reductions and a composition-consistent family of same-clock transition maps.

Stage 5 asked a stronger question:

> if the physical subsystem chosen as clock is itself changed, can the resulting reduced descriptions still be connected by reversible, composition-consistent maps that preserve corresponding operational predictions?

The canonical model uses three qutrit subsystems `A`, `B`, `C` with no globally privileged clock and the constraint:

`H_tot=H_A+H_B+H_C`.

The primary baseline is symmetric, while Stage 5G adds higher-dimension and asymmetric-rate controls.

## 2. Fixed question 1 — What is the global/block-like description B5?

The Stage 5 global mathematical description is:

`B5=(H_A,H_B,H_C,H_kin,H_A,H_B,H_C,H_tot,H_phys,|Psi>,clock models)`.

More explicitly:

- `H_kin=H_A tensor H_B tensor H_C`;
- `H_tot=H_A+H_B+H_C` with the appropriate tensor identities;
- `H_phys=ker(H_tot)`;
- `|Psi>` is a normalized vector in `H_phys`;
- each subsystem carries its own declared finite DFT clock-reading basis.

For the canonical symmetric qutrit:

`dim(H_kin)=27`,

`dim(H_phys)=7`.

For symmetric `d=5`:

`dim(H_phys)=19`.

For the asymmetric qutrit rates `(1,1,2)`:

`dim(H_phys)=5`.

`B5` is perspective-neutral only in the mathematical sense that every tested clock-relative description can be reconstructed from it. It is not interpreted as a physically realizable God's-eye observer.

## 3. Fixed question 2 — What are the local / clock-relative descriptions G5?

For clock subsystem `X` at discrete reading coordinate `j`, define:

`G_X(j)=(K_X,rho_X(j),O_X,rest-factor semantics)`.

Here:

- `K_X=Im[R_X(j)]` is the constraint-compatible support inside the tensor product of the two non-clock subsystems;
- `rho_X(j)=|psi_X(j)><psi_X(j)|` with `|psi_X(j)>=R_X(j)|Psi>`;
- `O_X` denotes observables acting inside `K_X`;
- the tensor factors themselves depend on the clock choice.

For example:

- C-clock perspective uses rest factors `A:B`;
- A-clock perspective uses rest factors `B:C`.

Therefore raw vector or matrix-coordinate equality across clock choices is not by itself a physical comparison.

## 4. Fixed question 3 — What are the transformations?

### Global to local

`R_X(j): H_phys -> K_X`.

### Local to global reconstruction

`E_X(j): K_X -> H_phys`.

### Same-clock reading change

`T_X(k<-j)=R_X(k)E_X(j)`.

### Genuine physical clock change

For distinct clocks:

`S_{Y<-X}(k,j)=R_Y(k)E_X(j): K_X -> K_Y`.

### Unified perspective map

It is useful after Stage 5 to write both same-clock and cross-clock transformations as:

`M_{(Y,k)<-(X,j)}=R_Y(k)E_X(j)`.

When `X=Y`, this is the same-clock transition `T_X`. When `X!=Y`, it is the genuine clock-change map `S`.

### Observable transformation

Corresponding reduced observables transform as:

`O_Y=M O_X M^dagger`.

A source reduced observable also admits a common-physical-space representative:

`O_phys=P_phys E_X O_X R_X P_phys`.

The bilateral physical projector is essential because the ambient matrix representation of `R_X` has a larger kinematic domain than its physical interpretation.

## 5. Fixed question 4 — Are the transformations reversible; what is discarded?

### On the declared physical/support spaces

For every tested ideal clock:

`R_X E_X=I_KX`,

`E_X R_X=I_phys`.

For genuine clock changes:

`S_{X<-Y}S_{Y<-X}=I_KX`

in support coordinates.

Thus the canonical clock-relative descriptions are mathematically reconstructible from one another when the constraint, support, and clock model are known.

### On unrestricted ambient rest spaces

Reversibility does **not** extend to the full rest tensor products.

In the canonical qutrit:

`dim(K_X)=7 < 9=dim(H_rest^(X))`.

The embedded clock-change maps have rank `7`, a two-dimensional ambient kernel, and satisfy:

`S^dagger S=P_KX`,

`S S^dagger=P_KY`.

Hence off-support ambient information is not part of the physical reduced perspective and is annihilated by the embedded map.

### Wrong clock basis

Energy-basis conditioning is non-injective on the seven-dimensional physical coefficient space, with ranks:

`(-1,0,+1) -> (2,3,2)`.

Thus reversibility depends on the declared ideal clock-reading interface.

### Accessibility guard

Mathematical reconstruction from `K_X` plus the theory does not imply that an internal observer operationally possesses or can execute the global reconstruction `E_X`.

`reconstructibility != automatic local operational accessibility`.

## 6. Fixed question 5 — What is preserved, reconstructible, perspective-dependent, or lost?

### Preserved within the tested finite family

The following structures survive the declared clock changes and robustness controls:

1. physical/support Hilbert-space inner products under the ideal reductions/maps;
2. direct-global route consistency;
3. pairwise inverse consistency;
4. cross-clock composition:

   `M_{p3<-p2} M_{p2<-p1}=M_{p3<-p1}`;

5. closed perspective loops return the source support identity;
6. corresponding expectation values when states and observables transform together;
7. corresponding tested Born probabilities;
8. density-matrix covariance;
9. the same structural identities for multiple physical coefficient families;
10. the same joint structure at symmetric `d=5` and asymmetric qutrit rates `(1,1,2)`.

In the symmetric qutrit baseline, the construction is also covariant under all explicit subsystem tensor permutations.

### Reconstructible but not necessarily directly accessible

- the common physical state from any declared support state;
- one clock-relative state from another;
- the corresponding reduced observable via the common physical representation.

### Perspective-dependent

The following need not remain numerically or structurally identical:

- the clock subsystem itself;
- the rest tensor-factor decomposition;
- the reduced ket representative;
- bare operator matrices;
- clock-coordinate labels;
- reduced tensor-factor entanglement.

The explicit entanglement control gives one bit in the A-clock `B:C` description and zero in the B- and C-clock rest descriptions.

### Excluded / lost relative to the declared physical interface

- off-support directions in the unrestricted rest tensor products;
- information erased by wrong-basis energy conditioning;
- nonphysical kinematic states as candidates for the physical frame-change API.

## 7. Fixed question 6 — What physical meaning can be assigned?

The strongest narrow Stage 5 interpretation is:

**a finite noninteracting constrained quantum model can support several internal clock choices whose physical reduced descriptions are connected by reversible support-space maps satisfying identity/inverse/composition consistency and preserving tested corresponding operational predictions, even though representation-dependent quantities such as reduced tensor-factor entanglement change with the clock perspective.**

Stage 5G strengthens this by showing the structure in:

- several physical coefficient families;
- a symmetric `d=5` model with `dim(H_phys)=19`;
- an asymmetric-rate qutrit model `(1,1,2)` with `dim(H_phys)=5`.

This is evidence of robustness **within the declared finite ideal family**.

It is not evidence that:

- every physical clock is equivalent;
- interacting clocks admit the same exact maps;
- quantum or gravitational general covariance has been established;
- the problem of time in quantum gravity has been solved;
- time is fundamentally relational;
- ontological becoming or eternalism has been established;
- a thermodynamic arrow or phenomenal passage has been explained.

## 8. Stage 5 central structure

After Stage 5, the cleanest finite-model object is an atlas of clock-relative perspectives and invertible maps between their physical supports:

`P5=({G_X(j)}, {M_(Y,k)<-(X,j)}, composition, operational correspondence)`.

The maps satisfy:

`M_p<-p=I_p`,

`M_p<-q M_q<-p=I_p`,

`M_r<-q M_q<-p=M_r<-p`.

Because every declared map is invertible on its physical support, this has a **groupoid-like** mathematical structure over the finite set of clock-relative perspectives.

The phrase `groupoid-like` is descriptive of the verified finite map algebra. It is not a claim that a groupoid has been established as the fundamental ontology of physical time.

The corresponding operational rule is not that all local matrices are invariant. Instead:

`state + corresponding observable + perspective map -> same tested prediction`.

This is the strongest concrete realization so far of the project-level idea:

`objectivity ~= consistency among perspectives`,

rather than numerical identity of all perspective-relative representations.

## 9. Cross-stage comparison — Stages 1 through 5

### Stage 1 — classical global/local reconstruction

Stage 1 showed that local descriptions can be lossy or ambiguous depending on the interface, while relational structure may still be reconstructible up to an appropriate equivalence. It introduced the recurring distinction:

`global reconstructibility != local accessibility`.

### Stage 2 — Potentiality

Stage 2 showed that formally different global semantics can share the same tested local operational outputs. It established:

`operational equality != ontological equivalence`.

This remains important in Stage 5: successful clock-perspective covariance does not uniquely determine an ontology of time.

### Stage 3 — records and direction

Stage 3 showed that record-defined orientation depends on boundary preparation and accessibility even when microscopic dynamics is reversible. It separated:

`order`, `record asymmetry`, `accessibility`, and `phenomenal passage`.

Stage 5 does not replace this result: clock-perspective consistency is not a temporal arrow.

### Stage 4 — one-clock quantum relational dynamics

Stage 4 established an explicitly reversible physical reduction and a composition-consistent transition family for multiple readings of one physical clock. The strongest survivor became:

`perspective-consistent transition structure`.

But the physical clock subsystem itself remained fixed.

### Stage 5 — change of physical clock

Stage 5 extends that pattern to different physical clock choices. The same abstract form:

`M_r<-q M_q<-p=M_r<-p`

survives genuine changes of clock subsystem, higher finite dimension, and an asymmetric clock-rate control, while corresponding operational predictions remain consistent when observables are transformed correctly.

Thus the most stable project-level candidate after Stages 1--5 is not an absolute state, clock value, or tensor decomposition, but:

**a network of admissible perspectives together with reconstructible/composition-consistent transformations and the operational correspondences they preserve.**

## 10. What is established versus what is only a candidate interpretation?

### Established inside the implemented toy families

- exact finite constraint kernels;
- explicit ideal clock reductions/reconstructions;
- support-space reversibility;
- genuine pairwise clock changes;
- all canonical three-clock composition routes;
- transformed-observable expectation/Born consistency for the tested operators/states;
- perspective-dependent reduced entanglement;
- declared negative controls;
- robustness at `d=5`, multiple coefficient families, global phase, symmetric subsystem permutations, and asymmetric rates `(1,1,2)`.

### Candidate project-level interpretation

`perspective-consistent transformation structure` may be a useful ingredient for thinking about relational temporal structure and objectivity.

### Not established

- a new physical law;
- a novel Page--Wootters/QRF theorem;
- a universal invariant of time;
- a discriminating empirical prediction;
- a fundamental metaphysics of time.

## 11. Non-novelty guard

The reduction/reconstruction/frame-change algebra is closely aligned with existing constrained-system and quantum-reference-frame constructions. The exact identities are therefore not presented as new quantum physics.

The contribution of `t-search` at this stage is methodological and comparative: the same explicit global/local protocol, information-loss accounting, negative controls, and interpretation guards are carried from classical reconstruction through Potentiality, records, one-clock relational quantum dynamics, and finally genuine changes of quantum clock perspective.

## 12. Remaining limitations / next scientific pressure tests

A later stage should not simply add more finite dimensions. More discriminating extensions include:

- interacting subsystems/clocks;
- nonideal or nonorthogonal clock states;
- POVM-based clock interfaces;
- continuous or larger spectral limits;
- cases where the constraint does not give a unique clock label for each rest support coordinate;
- sequential measurements and event-order questions;
- constrained systems closer to generally covariant/gravitational models.

Only if such extensions preserve a related structure should the project consider stronger physical claims.

## 13. Stage 5 exit-criteria assessment

The 28 protocol exit criteria are scientifically satisfied by Stages 5A--5G:

- criteria 1--7: Stage 5A;
- criteria 8--14: Stage 5B;
- criteria 15--17: Stage 5C;
- criterion 18 and coordinate guard 19: Stage 5D plus Stage 5C/F controls;
- criteria 20--22: Stage 5E;
- criteria 23--26: Stage 5F;
- criterion 27: Stage 5G higher-dimension/asymmetric-rate robustness;
- criterion 28: this synthesis and the interpretation discipline above.

Final repository regression and PR merge-readiness review are recorded separately before Stage 5 is declared merge-ready.
