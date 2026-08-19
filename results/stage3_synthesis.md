# Stage 3 Synthesis — Records and Temporal Direction

Status: **Stage 3A--3G substantive work complete; final-head regression and merge-readiness review remain before the Stage 3 checkpoint is declared merge-ready**.

## 1. Stage 3 question

Stage 3 asked whether a temporal orientation can be isolated from **record asymmetry** rather than being inserted by mere ordering or irreversible microscopic laws.

The conservative starting guard was:

`ordered change alone does not define a temporal arrow`.

Stage 3 therefore separated four notions throughout:

1. neutral order;
2. microscopic reversibility;
3. record/information asymmetry;
4. experienced temporal direction.

No result below identifies these four notions with one another.

## 2. Canonical reversible substrate

The Stage 3 record substrate is the finite three-bit system:

`Z=(X,M,N) in {0,1}^3`.

The two microscopic updates are:

`U_rec(X,M,N)=(X,M XOR X,N)`

and:

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both maps are bijective and self-inverse on all eight microstates.

The canonical boundary ensemble is:

`X_0=a`, `M_0=0`, `N_0=b`,

with independent uniform bits `a,b`.

The full-state Shannon entropy is preserved:

`H(Z_0)=H(Z_1)=H(Z_2)=2 bits`.

Thus any canonical record orientation does not arise from non-bijective microscopic dynamics or global Shannon-entropy production in this closed toy model.

## 3. Record diagnostics

At neutral current position `1`, the explicit record register is `M_1`.

The principal information diagnostic is:

`Q_R(k,j)=I(R_k;X_j)`.

The signed record contrast is:

`A_R(k,delta)=I(R_k;X_{k-delta})-I(R_k;X_{k+delta})`.

A second diagnostic uses Bayes-optimal decoding accuracy:

`A_Acc=Acc(R_k->X_{k-delta})-Acc(R_k->X_{k+delta})`.

For the canonical ensemble:

`I(M_1;X_0)=1 bit`

`I(M_1;X_2)=0`

`Acc(M_1->X_0)=1`

`Acc(M_1->X_2)=1/2`

so:

`A_R=1`

and:

`A_Acc=1/2`.

The project calls this a **record-defined orientation toward the lower-index side** only because both diagnostics are nonzero and agree in sign.

The lower-index side is not definitionally called the physical past.

## 4. Order is not sufficient

The no-record control replaces the first update with the identity while retaining:

- three ordered positions;
- reversible system scrambling;
- the same neutral indexing convention.

The result is:

`A_R=A_Acc=0`

and no record-defined orientation.

Therefore, within this construction:

`mere order != record-defined orientation`.

## 5. Microscopic reversibility is compatible with record asymmetry

The canonical maps remain bijective while the canonical ensemble has a nonzero record-defined orientation.

Thus the model explicitly realizes:

`microscopic reversibility != record symmetry`.

This does not show that real thermodynamic irreversibility is reducible to records; it only demonstrates logical/formal compatibility in the finite toy model.

## 6. History reversal and orientation balance

For exact modeled history reversal `J`:

`A_R(J_*mu_fwd)=-A_R(mu_fwd)`

and similarly for `A_Acc`.

The canonical orientation flips from lower-index to upper-index.

For the equal mixture:

`mu_sym=1/2 mu_fwd + 1/2 mu_rev`,

both signed scores vanish even though equal nonzero correlations remain on the two sides.

Stage 3G extends this to:

`mu_w=w mu_fwd+(1-w)mu_rev`.

Forward-biased mixtures choose the lower-index side, reverse-biased mixtures choose the upper-index side, and the scores are antisymmetric under:

`w -> 1-w`.

The sign crosses zero at exact balance.

Therefore the Stage 3 orientation behaves covariantly under the declared modeled-history reversal and tracks ensemble orientation balance rather than literal position names.

## 7. Boundary preparation, not the literal blank value

Stage 3D showed that independent uniform initial memory removes the canonical orientation.

Stage 3G refines this with:

`p=P(M_0=0)`.

With unchanged reversible maps:

| `p` | `A_R` | `A_Acc` | orientation |
|---:|---:|---:|---|
| `1` | `1` | `0.5` | lower-index |
| `3/4` | `~0.188721875541` | `0.25` | lower-index |
| `1/2` | `0` | `0` | none |
| `1/4` | `~0.188721875541` | `0.25` | lower-index |
| `0` | `1` | `0.5` | lower-index |

At `p=0`, the register begins deterministically at `1` and becomes perfectly anti-correlated with `X_0`, but mutual information and optimal decoding remain maximal.

Therefore the robust explanatory statement is not:

`blank value zero causes the record`.

It is instead:

**non-maximal uncertainty / nonuniform preparation of the memory register permits the reversible coupling to create an informative record; maximal independent memory uncertainty masks that record.**

This is a toy-model boundary statement, not a derivation of a cosmological Past Hypothesis.

## 8. Global record structure versus local accessibility

Stage 3E makes the block/local map explicit.

The record-only block-like object is:

`B_3=(Z_space,U_1,U_2,Omega,mu)`.

The declared local Actuality is deliberately reduced to:

`A_k^loc=(X_k,M_k)`.

The environment bit `N_k`, complete trajectory, opposite-side actual microstates, and privileged boundary labels are not silently included.

The record-only projection is:

`F_k:(B_3,omega)->G_{omega,k}^rec`

with:

`G_k^rec=(Records_k,Actuality_k)`.

A single canonical central view can be compatible with two complete histories because hidden `N` remains unresolved.

A suitable family of exact local views can uniquely reconstruct the complete actual trajectory.

Thus:

`single-view local accessibility != multi-view reconstructibility`.

## 9. Accessibility is interface-relative

Stage 3F changes only the local observation channel while keeping the global reversible block fixed.

For a record-only binary-symmetric channel with error probability `epsilon`:

| `epsilon` | `I(M_obs;X_0)` | decoder | accessible `A_R` | accessible `A_Acc` |
|---:|---:|---:|---:|---:|
| `0` | `1` | `1` | `1` | `0.5` |
| `1/4` | `~0.188721875541` | `0.75` | same MI value | `0.25` |
| `1/2` | `0` | `0.5` | `0` | `0` |

The unchanged global relation remains:

`I(true M_1;X_0)=1 bit`.

At maximal readout noise, therefore:

`I(true M_1;X_0)=1`

while:

`I(M_obs;X_0)=0`.

This explicitly separates:

`globally represented information`

from:

`information accessible through the declared local interface`.

The supported guard is:

`inaccessible information != information absent from the formal global model`.

## 10. Same local statistic can hide different global structures

Stage 3G compares two ways to obtain the same reduced value `~0.188721875541` bit.

### Global boundary uncertainty

With `P(M_0=0)=3/4`, the **true global** record relation itself is reduced:

`I(M_1;X_0)~=0.188721875541`.

### Local readout uncertainty

With the canonical globally perfect record and readout noise `epsilon=1/4`:

`I(true M_1;X_0)=1`

but:

`I(M_obs;X_0)~=0.188721875541`.

Therefore:

`same accessible/local statistic != same global information structure`.

This is an important limitation on inferring global temporal structure from a single local information measure.

## 11. Redundant accessibility is a canonical-model limitation

The canonical recording update leaves:

`X_1=X_0`.

Consequently current `X_1` is itself a perfect lower-side information carrier.

Destroying the `M` readout therefore does not destroy total local access while `X_1` remains exposed:

`record-specific accessibility lost != all local accessibility lost`.

This limitation means Stage 3 does not yet isolate a realistic memory trace whose temporal information is absent from the contemporaneous system state.

A richer later model should separate system persistence from dedicated record storage more strongly.

## 12. Bookkeeping and repeated-value robustness

Pure symbolic renaming of positions changes only names, not the numerical record profile. The selected structural side follows the renaming covariantly.

Bijective binary value relabelings preserve mutual information and Bayes-optimal decoding.

The all-zero trajectory also supplies a repeated-value control:

`(0,0,0)->(0,0,0)->(0,0,0)`.

All three state values are equal, but position-tagged occurrences remain distinct.

Repeated local `(X,M)` values likewise do not collapse different positions.

Therefore Stage 3 retains the Stage 1 guard:

`state equality != occurrence/event identity`.

## 13. Completing G=(Records,Actuality,Potentiality)

Stage 3E reintroduces Stage 2 Potentiality only after the record semantics have been independently tested.

The integration is an explicit **product construction**, not a claim that the Stage 2 branching substrate and Stage 3 bit substrate are already one physical system.

The complete local forms are:

`G_E^complete=(Records,A_product,EPot,next probabilities)`

and:

`G_O^complete=(Records,A_product,OPot,next probabilities)`.

The same Stage 3 record layer attaches to both.

Stage 3G rechecks two critical guards:

1. swapping the epistemic hidden selected history `h*` while holding the Stage 2 local projection fixed does not change the complete local product view;
2. epistemic and ontic products retain identical records and matched modal predictions while their Potentiality types remain distinct.

Thus Stage 3 integration does not accidentally erase the Stage 2 hidden-versus-absent future-information distinction.

This demonstrates construction-level modularity only, not physical independence between record orientation and future ontology.

## 14. Final information classification

| Structure/information | Status under declared Stage 3 interfaces |
|---|---|
| current `X_k,M_k` under exact local interface | locally accessible |
| current hidden `N_k` | globally represented, hidden from one local view |
| complete actual trajectory from one central exact view | ambiguous |
| complete actual trajectory from suitable multi-position exact views | reconstructible in canonical model |
| full trajectory probability distribution from one unweighted actual local instance | lost/not reconstructible from that instance |
| true record MI in global ensemble | globally defined ensemble statistic |
| noisy-readout record MI | interface-relative locally accessible statistic |
| record orientation under canonical boundary/interface | candidate arrow-like structure, not invariant under all boundary/interface changes |
| numerical record profile under pure bookkeeping renaming | stable/covariant under tested relabelings |
| record score under modeled history reversal | sign-covariant, not invariant: it reverses |
| epistemic hidden `h*` | globally present in Stage 2 epistemic model, absent from projected local product |
| ontic selected future | absent from Stage 2 ontic model state |

The main lesson is that "preserved" must be qualified by the transformation class. No single strict fundamental time invariant has been established.

## 15. Six fixed questions

### 1. What is the block-like/global description `B_3`?

For the record experiment:

`B_3=(Z_space,U_1,U_2,Omega,mu)`.

It contains the complete finite microstate space, the declared reversible maps, the complete trajectory family, and the exact trajectory weights.

To project one actual local instance, the formal map also receives a selected complete trajectory `omega` from the global ensemble.

This is a global mathematical description, not a physically realizable God's-eye observer.

### 2. What is the becoming-like/local description `G_k`?

First:

`G_k^rec=(Records_k,Actuality_k)`

with local Actuality:

`A_k^loc=(X_k,M_k)`.

After the explicit Stage 2 product adapter:

`G_E^complete=(Records,A_product,EPot,pi_E)`

or:

`G_O^complete=(Records,A_product,OPot,pi_O)`.

This formal shape realizes:

`G=(Records,Actuality,Potentiality)`

without establishing it as a fundamental ontology of becoming.

### 3. What is the transformation from global to local?

For records:

`F_k:(B_3,omega)->G_{omega,k}^rec`.

It projects the actual complete microstate at position `k` to the declared `(X_k,M_k)` interface and attaches the ensemble-level diagnostics explicitly granted by the experiment interface.

Stage 2 Potentiality is then attached through typed local-to-product adapters; the adapter consumes already-projected Stage 2 local views rather than privileged global selectors.

### 4. Is the transformation reversible? What is discarded/hidden?

A single `F_k` is not injective.

It omits at least:

- `N_k`;
- opposite-side actual microstates;
- the complete actual trajectory as a direct field;
- privileged boundary labels;
- the full weighted trajectory distribution as recoverable content of one actual local instance.

In the canonical toy model a suitable family of exact local views can reconstruct the actual complete trajectory, but this does not make one local view reversible and does not reconstruct the entire global ensemble distribution from one realized history.

### 5. What is stable, reconstructible, ambiguous, lost, or locally accessible?

Locally accessible depends on the interface. Under the exact interface, current `X_k,M_k` are accessible. Under noisy/masked interfaces some or all of that information becomes degraded or inaccessible.

The actual trajectory is ambiguous from one canonical central view but reconstructible from a suitable view family.

The numerical record profile and information/decoder values are stable under the tested pure bookkeeping and bijective value relabelings.

The signed record score is **covariant**, not invariant, under history reversal: it changes sign.

The orientation is not stable under all boundary or access transformations: it vanishes for maximal independent memory uncertainty, equal forward/reverse balance, no record coupling, or sufficiently destructive record readout.

No strict fundamental temporal invariant has been established.

### 6. What physical meaning can be assigned to the surviving structure?

The strongest justified interpretation is:

**a record-defined temporal orientation / local information-accessibility arrow exists as a candidate arrow-like structure in the tested finite model when reversible record coupling acts on an appropriately nonuniform memory boundary and the relevant record information is available through the declared interface.**

This candidate structure is more than mere order because no-record controls remove it, and it is not microscopic irreversibility because the global maps are bijective.

However it remains boundary-, ensemble-, and interface-dependent.

It is not established as:

- the fundamental arrow of physical time;
- thermodynamic irreversibility;
- a cosmological Past Hypothesis;
- empirical time-reversal violation;
- ontological becoming;
- an open future;
- phenomenal passage.

## 16. Stage 3 exit-criteria review

1. order / reversibility / record asymmetry / experienced direction distinct — **satisfied**.
2. canonical maps bijective on full state space — **satisfied**.
3. asymmetric boundary explicit — **satisfied**.
4. record diagnostics ensemble-based — **satisfied**.
5. signed orientation measured without defining lower side as physical past — **satisfied**.
6. exact reversal flips orientation — **satisfied**.
7. symmetric mixture removes signed bias — **satisfied**.
8. order-only/no-record control removes orientation — **satisfied**.
9. boundary controls separate reversible law from record preparation — **satisfied**.
10. global entropy preservation separated from subsystem/correlation changes — **satisfied**.
11. `G=(Records,Actuality,Potentiality)` implemented without conflation — **satisfied**.
12. global-to-local projection and information loss explicit — **satisfied**.
13. bookkeeping renaming and repeated-value controls — **satisfied**.
14. Stage 2 integration preserves epistemic/ontic distinction — **satisfied**.
15. full repository regression — **robustness checkpoint passed; final synthesis-head run pending**.
16. synthesis answers fixed questions and states limits — **satisfied by this document, pending final-head validation**.

## 17. Strongest Stage 3 conclusion

Within the tested finite construction:

**ordered reversible dynamics can support a robustly measurable record-defined orientation when record coupling acts on a non-maximally uncertain memory boundary. The orientation reverses under modeled history reversal, cancels at orientation-symmetric balance, disappears without record coupling or under maximally uncertain memory preparation, and can become locally inaccessible without being removed from the global formal state.**

Equally important:

**the Stage 3 orientation is not representation-independent in an unrestricted sense. It is conditional on the ensemble, boundary, record coupling, and observation interface, and the canonical model contains redundant current-state information.**

Therefore Stage 3 supports a **candidate relational/information-accessibility component of temporal direction**, not a completed theory of physical time.

## 18. Carry-forward to Stage 4+

The most useful structures to carry forward are:

1. explicit separation of global mathematical state from local accessible state;
2. record correlations defined relationally rather than by literal state values;
3. signed orientation diagnostics that transform covariantly under reversal;
4. explicit distinction between global information, local accessibility, and multi-view reconstructibility;
5. typed separation of Records, Actuality, and Potentiality;
6. strict controls against interpreting bookkeeping, boundary conventions, or information loss as metaphysical time.

Stage 4 should test whether analogous relational/conditional structures survive in a finite Page--Wootters-style quantum setting, rather than assuming that the classical Stage 3 record arrow is already fundamental.
