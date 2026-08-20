# Stage 4 Synthesis — Finite Page--Wootters-Style Quantum Model

Status: **Stage 4 scientific/implementation synthesis complete; final documentation-inclusive CI and merge-readiness review tracked separately below.**

## Executive result

Stage 4 constructs a finite exact Page--Wootters-style model with:

- a stationary zero-constraint global physical state;
- an ideal finite DFT clock;
- exact clock-relative unitary system dynamics;
- an unrestricted kinematic clock projection that is lossy;
- a normalized physical reduction that is isometric/invertible on the matched-energy physical subspace;
- explicit local-to-local transition maps with identity, inverse, and composition consistency;
- matching global/local conditional Born predictions;
- negative controls separating constraint satisfaction, nontrivial ray change, and clock-basis quality;
- robustness under modest dimension, coefficient, origin, global-phase, and bookkeeping-label changes.

The strongest surviving Stage 4 object is not an absolute clock reading or a particular ket representative. It is the **relational family of admissible reduction/reconstruction and local-to-local transition maps together with their operational predictions**.

This remains a finite toy-model representation result. It does not establish fundamental emergent time, eternalism, ontological becoming, a temporal arrow, phenomenal passage, or fundamental periodicity.

---

## 1. Fixed question 1 — What is the block-like/global description `B_4`?

The declared finite global model is:

`B_4=(H_C,H_S,H_Cgen,H_Sgen,H_tot,H_phys,|Psi>,{|t_j>})`,

where:

- `H_C` and `H_S` are finite Hilbert spaces of equal dimension `d`;
- `H_Cgen|n>_C=-n|n>_C`;
- `H_Sgen|n>_S=+n|n>_S`;
- `H_tot=H_Cgen tensor I + I tensor H_Sgen`;
- `H_phys=ker(H_tot)=span{|n>_C|n>_S}`;
- `|Psi>=sum_n c_n |n>_C|n>_S` is a physical global vector;
- `|t_j>` is the declared ideal DFT clock-reading basis used for relational reduction.

For every physical vector:

`H_tot|Psi>=0`,

so:

`exp(-i H_tot tau)|Psi>=|Psi>`

for every external parameter `tau`.

This is stationarity under the constraint generator, not evidence that nothing physically happens in the universe.

The global mathematical description is also not interpreted as a physically realized God's-eye observer.

---

## 2. Fixed question 2 — What is the local / becoming-like description `G_j`?

At clock reading `j`, a convenient vector representative is:

`|psi_j>=R_j|Psi>`.

For normalized physical states this is normalized automatically in the ideal model. The physically relevant pure-state content is the ray or density matrix:

`rho_j=|psi_j><psi_j|`.

A minimal local description can therefore be written as:

`G_j^PW=(j,rho_j,{P(a|t_j)})`.

The index/reading is relational bookkeeping tied to the declared clock basis. The density matrix and conditional observable probabilities encode the local system description.

Calling `G_j` "becoming-like" is only a project-level comparison with earlier local descriptions. Stage 4 does not model ontological becoming or phenomenal passage.

---

## 3. Fixed question 3 — What is the transformation from global to local?

Stage 4 distinguishes two maps.

### Formal kinematic conditioning

`P_j^kin=(<t_j| tensor I_S): H_kin -> H_S`.

This is defined for arbitrary kinematic vectors, including nonphysical ones.

### Physical reduction

On the zero-constraint physical subspace:

`R_j=sqrt(d) P_j^kin restricted to H_phys`.

For:

`|Psi_c>=sum_n c_n |n,n>`,

one obtains:

`R_j|Psi_c>=sum_n c_n exp(-i n t_j)|n>_S`.

The explicit reconstruction is:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n,n>`.

Local-to-local transport is then:

`T_{k<-j}=R_k E_j`.

In the ideal finite model:

`T_{k<-j}=exp[-i H_S(t_k-t_j)]`.

---

## 4. Fixed question 4 — Is the transformation reversible; what is hidden or discarded?

The answer depends critically on the domain.

### Full kinematic space

For canonical `d=4`:

`P_j^kin: C^16 -> C^4`

has rank `4` and nullity `12`.

Thus it is many-to-one. Explicit distinct kinematic vectors with identical clock projection exist.

Therefore:

`kinematic projection = lossy`.

### Physical subspace

The physical subspace has dimension `d`, equal to the system Hilbert-space dimension. In matched-energy physical coordinates:

`R_j^dagger R_j=R_j R_j^dagger=I`.

The explicit inverse satisfies:

`R_j E_j=I_S`,

`E_j R_j=I_phys`.

Norms and inner products are preserved.

Therefore, in this ideal model:

`R_j: H_phys <-> H_S`

is an isometric isomorphism.

A single exact clock-relative system vector is mathematically sufficient to reconstruct the complete physical global vector **given the declared constraint, spectra, clock basis, and reconstruction map**.

This is mathematical reconstructibility, not automatic operational access by an internal observer.

### Basis dependence

Clock-energy-basis conditioning acts as:

`Q_m=|m><m|`

on physical coefficients. It has rank `1` and nullity `d-1`, so it is non-injective even on `H_phys`.

Hence:

`physical-subspace reversibility depends on the declared ideal clock-reading basis`.

---

## 5. Fixed question 5 — What survives, and what does not?

### Survives within the tested Stage 4 family

1. **Constraint structure**

   Generic physical coefficients in tested dimensions remain in `ker(H_tot)`.

2. **Hilbert-space geometry under physical reduction**

   Norms and inner products are preserved by `R_j` on `H_phys`.

3. **Clock-relative transition family**

   `T_{k<-j}=R_kE_j=exp[-iH_S(t_k-t_j)]`.

4. **Perspective consistency**

   `T_{l<-k} T_{k<-j}=T_{l<-j}`.

5. **Identity/inverse structure**

   `T_{j<-j}=I` and `T_{j<-k}=T_{k<-j}^{-1}`.

6. **Common-origin covariance**

   Local vector representatives change under `t_j -> t_j+alpha`, but the transition family does not.

7. **Operational global/local consistency**

   Global conditional Born probabilities and local clock-relative Born probabilities agree for the tested noncommuting observable.

8. **Global-phase invariance of operational content**

   `|Psi> -> exp(i theta)|Psi>` leaves clock probabilities, local density matrices, and tested Born predictions unchanged.

9. **Bookkeeping relabeling covariance**

   Pure renaming of clock labels does not alter the transition matrices or their composition law.

10. **Modest finite-dimension / coefficient robustness**

    The joint Stage 4 residual suite passes at `d=3,4,5,6`, for equal-amplitude, generic complex, and sparse multi-sector physical coefficient choices.

### Does not survive as an invariant object

- the literal clock label `j`;
- the absolute clock origin;
- a particular local ket representative;
- a global ket representative up to common phase;
- invertibility of arbitrary clock-basis conditioning;
- invertibility of unrestricted kinematic conditioning.

### Not yet tested

The physical clock subsystem itself has not been changed. Therefore:

`origin invariance / bookkeeping covariance != clock-choice invariance`.

Stage 5 is required before the transition family can be considered robust under genuine changes of clock perspective.

---

## 6. Fixed question 6 — What physical meaning can be assigned?

The strongest supported physical reading is narrow:

**a stationary constrained finite quantum description can encode exact internal clock-relative unitary dynamics whose local descriptions are linked by reversible, composition-consistent transition maps and reproduce the same tested conditional Born predictions as the global description.**

This is a finite Page--Wootters-style realization of relational quantum dynamics.

It supports treating `T_{k<-j}` and the compatible family of global/local maps as a candidate **relational temporal structure**.

It does not by itself decide whether the universe is fundamentally block-like, becoming-like, or neither. It also does not explain a thermodynamic arrow, records, open future, subjective passage, or consciousness.

---

## What the negative controls taught us

Stage 4F/G sharpen the positive construction.

### Constraint violation

A nonphysical kinematic vector can still be formally conditioned on every clock reading, but its conditional sequence need not satisfy the expected Schrödinger relation.

Therefore:

`history-like decomposition != physical Page--Wootters dynamics`.

### Single-energy physical state

A constrained single-energy state changes only by local vector phase. Its ray and density matrix remain unchanged.

Therefore:

`constraint satisfaction != nontrivial relational ray change`.

### Sparse multi-sector state

A coherent two-sector physical state already produces nontrivial ray change.

Therefore the equal-amplitude full-spectrum baseline is not necessary. Within this canonical pure matched-energy family, multi-sector coherent support is sufficient to produce nontrivial relative ray variation over the cycle.

This must not be generalized into the claim that entanglement universally creates time.

### Wrong clock basis

Clock-energy-basis conditioning loses physical coefficient sectors and is non-injective even on `H_phys`.

Therefore:

`arbitrary clock basis != ideal relational time basis`.

---

## Stage 1--4 comparison

| Stage | Main global/local lesson | Candidate surviving structure | Main limitation |
| --- | --- | --- | --- |
| Stage 1 | local views can be lossy while families can reconstruct global relational structure | consistency/reconstructibility of graph relations | classical finite graph only |
| Stage 2 | operationally matched local outputs can underdetermine hidden-selected vs no-selected future semantics | separation of representation from Potentiality semantics | no empirical fixed/open-future discriminator |
| Stage 3 | reversible ordered dynamics can support boundary-dependent record orientation; accessibility is interface-relative | record/information-accessibility relations | no thermodynamic/fundamental arrow |
| Stage 4 | stationary constrained quantum states can support reversible clock-relative dynamics and consistent local-to-local maps | `T_{k<-j}` plus compatible reduction/reconstruction/Born structure | same physical clock subsystem throughout |

The common pattern becoming clearer across the stages is not one privileged local state or one absolute temporal coordinate. It is a **network/family of admissible perspectives and transformations constrained by composition consistency and by what information/operational predictions they preserve**.

A compact candidate is:

`mathfrak T = ({G_i},{T_{j<-i}})`

with:

`T_{k<-j} T_{j<-i}=T_{k<-i}`.

In Stage 4 the `T` maps are unitary. In earlier stages the corresponding maps need not be invertible or information-preserving.

This suggests that the project should continue searching for **perspective-consistency structure** rather than assuming in advance that a single scalar time variable or a single local state is fundamental.

This is still a project-level candidate, not a discovered law of nature.

---

## Novelty / literature guard

The Page--Wootters mechanism, conditional states, and unitary relational evolution used here are standard theoretical ideas. Stage 4 should not be presented as a new quantum-physics discovery.

The contribution of `t-search` at this point is methodological and comparative: the same explicit six-question global/local protocol has now been carried from classical reconstruction, through Potentiality and record asymmetry, into a constrained finite quantum model with controlled information-loss and representation tests.

Any claim of physical novelty would require substantially more than these toy-model identities.

---

## Stage 4 conclusion

The strongest Stage 4 conclusion is:

**within the tested finite matched-energy Page--Wootters-style family, a stationary constrained global quantum state and its ideal clock-relative local descriptions are connected by an explicitly reversible physical reduction, an origin- and bookkeeping-stable unitary transition family satisfying identity/inverse/composition consistency, and matching tested global/local conditional Born predictions. These structures survive modest changes of finite dimension, physical coefficient family, global phase, and clock-origin convention, while targeted controls show that they do not extend to arbitrary kinematic states or arbitrary clock bases.**

The best surviving candidate is therefore relational and transformation-based:

`perspective-consistent transition structure`

rather than:

`absolute clock value`, `particular ket`, or `unrestricted global projection`.

Stage 5 should test the decisive next question:

**does an analogous structure survive when the physical clock subsystem itself is changed?**
