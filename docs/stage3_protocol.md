# Stage 3 Protocol — Records and Temporal Direction

Status: **protocol frozen before implementation**.

Stage 3 begins after the Stage 2 Potentiality checkpoint is merged. Its purpose is to add explicit record structure and test whether asymmetric record accessibility contributes an arrow-like orientation beyond mere ordering, branching, or simulation order.

This document is a specification. Stage 3 code should follow it unless an experiment exposes a contradiction or important ambiguity; any revision must be documented rather than silently changing the semantics.

## 1. Stage 3 question

Stage 1 introduced ordered relational structure. Stage 2 added Actuality and Potentiality and showed that formally different future semantics can remain operationally indistinguishable under matched conditions.

Stage 3 asks a different question:

> Can a reversible finite model possess an asymmetric local record structure that selects one orientation of an otherwise neutral ordered trajectory, and does that asymmetry disappear or reverse under appropriate controls?

The target is not to assume a temporal arrow from event indices. The target is to measure whether record accessibility itself distinguishes the two orientations of an ordered history.

## 2. Non-goals

Stage 3 does **not** establish that:

- record asymmetry is identical to time itself;
- record asymmetry explains phenomenal passage or the felt flow of time;
- a larger mutual information value proves causal influence in a general physical system;
- reversible microdynamics imply record symmetry;
- record formation requires fundamentally irreversible laws;
- subsystem entropy increase is identical to global entropy production;
- the finite bit model is a realistic thermodynamic system;
- the Second Law has been derived;
- Python execution order is modeled temporal direction;
- the numerical ordering `0,1,2,...` is by itself a physical past-to-future orientation.

Principal guards:

`order != arrow`

`microdynamical reversibility != record symmetry`

`correlation != causation`

`record asymmetry != phenomenal passage`

`subsystem entropy change != global entropy production`

`simulation order != modeled temporal order`

## 3. Separate four notions

Stage 3 keeps the following notions distinct.

### 3.1 Order

An ordered trajectory has positions related by adjacency/order. Position indices are bookkeeping coordinates on the toy history unless a later result gives an orientation physical meaning.

### 3.2 Microdynamical reversibility

A microscopic update `U` is reversible when it is bijective on the complete microstate space and an inverse `U^{-1}` exists.

### 3.3 Record asymmetry

At a current position `k`, an accessible register may carry more information about states on one side of `k` than about states at equal separation on the other side.

### 3.4 Experienced temporal direction

The phenomenal sense of past/present/future or temporal passage is not modeled at Stage 3. A record-defined orientation is at most a candidate structural prerequisite for an experienced direction.

None of these four is identified with another by definition.

## 4. Record definition

A **record** is a presently accessible register/correlation that carries information about another event or configuration.

For Stage 3, do **not** define a record as “information about the past.” That would insert the desired arrow by definition.

Instead, for a current position `k`, let `R_k` denote an accessible record register and `X_j` a target system variable at another ordered position `j`.

The record relation is diagnosed by statistical dependence across an explicitly declared trajectory ensemble, primarily through mutual information:

`I(R_k ; X_j)`.

A single accidental equality of values in one trajectory is not sufficient to establish a record relation.

Mutual information alone is not treated as a causal diagnostic. In the canonical toy model, causal/provenance information is known separately because the microscopic update maps are explicitly specified.

## 5. Canonical microstate space

Use a closed finite three-bit microstate:

`Z = (X,M,N)`

with:

- `X in {0,1}`: system bit;
- `M in {0,1}`: accessible memory/record register;
- `N in {0,1}`: environment/ancilla bit.

The complete microstate space is:

`Z_space = {0,1}^3`.

The canonical trajectory contains three neutral ordered positions:

`z_0, z_1, z_2`.

The subscripts are position labels. Do not call `0` “past” and `2` “future” before the record analysis.

## 6. Canonical reversible update maps

Define two reversible maps.

### 6.1 Recording interaction

`U_rec(X,M,N) = (X, M XOR X, N)`.

This is self-inverse:

`U_rec^{-1} = U_rec`.

### 6.2 System-scrambling interaction

`U_scr(X,M,N) = (X XOR N, M, N)`.

This is also self-inverse:

`U_scr^{-1} = U_scr`.

The forward-labeled trajectory construction is:

`z_1 = U_rec(z_0)`

`z_2 = U_scr(z_1)`.

Both updates must be verified as bijections over all eight complete microstates. The modeled arrow, if any, must therefore not be attributed to non-invertible microscopic laws.

## 7. Canonical asymmetric boundary ensemble

Let `a` and `b` be independent uniform bits.

Use the initial ensemble:

`X_0 = a`

`M_0 = 0`

`N_0 = b`.

The special condition is the blank register:

`M_0 = 0`.

After `U_rec`:

`M_1 = X_0 = a`.

After `U_scr`:

`X_2 = a XOR b`.

Because `b` is independent uniform noise, the canonical ensemble is expected to satisfy:

`I(M_1 ; X_0) = 1 bit`

`I(M_1 ; X_2) = 0 bits`.

This asymmetry is produced by the combination of reversible dynamics and the special boundary ensemble. It is not attributed to a fundamentally irreversible update rule.

## 8. Global/block-like Stage 3 object

For the record-only core experiment, define a block-like ensemble object schematically as:

`B_3 = (Z_space, U_rec, U_scr, Omega, mu)`

where:

- `Z_space` is the full microstate space;
- `U_rec` and `U_scr` are reversible microscopic maps;
- `Omega` is the set of complete three-position trajectories admitted by the declared boundary ensemble;
- `mu` is the probability distribution over those trajectories.

A complete trajectory is represented together as one mathematical object:

`omega = (z_0,z_1,z_2)`.

This is a global mathematical representation, not a physically realizable external observer.

## 9. Neutral history reversal

Define history reversal on a complete trajectory by:

`J(z_0,z_1,z_2) = (z_2,z_1,z_0)`.

The reversed ensemble is the pushforward:

`mu_rev = J_* mu_fwd`.

A reversed trajectory must also be checked dynamically using the inverse maps in reverse order:

`z_1 = U_scr^{-1}(z_2)`

`z_0 = U_rec^{-1}(z_1)`.

History reversal is a transformation of the modeled history/ensemble. It is not implemented or interpreted merely as iterating a Python loop backward.

## 10. Symmetric control ensemble

Define the orientation-symmetric mixture:

`mu_sym = 1/2 mu_fwd + 1/2 mu_rev`.

This control contains both history orientations with equal weight.

If the record-arrow diagnostic is genuinely sensitive to orientation rather than mere ordering, the signed directional contrast should vanish in this mixture even though ordered trajectories and correlations remain present.

## 11. Order-only / no-record control

Use the same ordered positions and system scrambling but omit the recording coupling, or equivalently keep the accessible register independent of the system.

The control must preserve ordered change while producing no directional record bias:

`A_R = 0` expected.

This control is required to support the statement:

`mere order != record-defined arrow`.

## 12. Blank-boundary control

A second important control replaces the special blank memory boundary with an independent uniform memory bit:

`M_0 ~ Bernoulli(1/2)` independent of `X_0,N_0`.

After `M_1 = M_0 XOR X_0`, the register is expected to carry no information about `X_0` because the unknown initial memory masks the copied bit.

This tests whether the canonical record asymmetry depends on the special low-uncertainty memory boundary rather than on reversibility alone.

## 13. Exact information-theoretic diagnostics

Stage 3 uses exact finite-ensemble probabilities where possible. No sampling noise is necessary for the canonical model.

### 13.1 Shannon entropy

For a discrete variable `A`:

`H(A) = - sum_a p(a) log2 p(a)`.

### 13.2 Mutual information

`I(A;B) = sum_{a,b} p(a,b) log2[p(a,b)/(p(a)p(b))]`.

Terms with zero joint probability contribute zero. Do not add pseudocounts to the canonical exact calculation.

### 13.3 Conditional entropy

`H(A|B) = H(A,B) - H(B)`.

### 13.4 Optimal decoding/accessibility accuracy

For predicting target `X_j` from current record `R_k`, define Bayes-optimal accuracy:

`Acc(R_k -> X_j) = sum_r p(r) max_x p(X_j=x | R_k=r)`.

This is a second operational accessibility diagnostic and should agree qualitatively with the mutual-information asymmetry in the canonical model.

## 14. Record profile

For current position `k`, define the record profile:

`Q_R(k,j) = I(R_k ; X_j)`.

The profile itself is unsigned. Mutual information is symmetric in its two arguments and does not contain a temporal arrow by itself.

Direction enters only when the profile is compared across the two sides of a neutral ordered current position.

## 15. Signed record-arrow score

For positions equidistant from current position `k`, define:

`A_R(k,Delta) = I(R_k ; X_{k-Delta}) - I(R_k ; X_{k+Delta})`.

Use only cases in which both comparison positions exist.

Canonical Stage 3 choice:

`k = 1`

`Delta = 1`

so:

`A_R = I(M_1 ; X_0) - I(M_1 ; X_2)`.

Interpretation:

- `A_R > 0`: the record structure selects the orientation in which position `0` lies on the record-rich side;
- `A_R < 0`: the opposite orientation is selected;
- `A_R = 0`: this diagnostic does not select an orientation.

Do not rename the positive side “past” until after the score has been computed.

Expected canonical behavior:

`A_R(mu_fwd) > 0`

`A_R(mu_rev) < 0`

`A_R(mu_sym) = 0`.

## 16. Accessibility-arrow score

Define a complementary decoder-based score:

`A_Acc(k,Delta) = Acc(R_k -> X_{k-Delta}) - Acc(R_k -> X_{k+Delta})`.

The canonical model should be checked for sign agreement between `A_R` and `A_Acc`.

Agreement is a robustness check, not a proof that either score is a fundamental observable of time.

## 17. Entropy diagnostics and reversibility

Because the microscopic maps are bijective and the global distribution is transported exactly, the full-state Shannon entropy should satisfy:

`H(Z_0) = H(Z_1) = H(Z_2)`.

Subsystem entropies and correlations may change:

`H(M_k)` may change;

`I(M_k;X_j)` may change.

Therefore Stage 3 must distinguish:

`global information preservation`

from:

`subsystem entropy redistribution and correlation formation`.

Do not describe an increase of `H(M)` alone as total entropy production or as a derivation of the thermodynamic arrow.

## 18. Becoming-like record view

Stage 3 completes the schematic local description toward:

`G_k = (Records_k, Actuality_k, Potentiality_k)`.

For the early record-only experiments (Stage 3A–3D), isolate the record effect and use a reduced view:

`G_k^rec = (Records_k, Actuality_k)`.

A minimal record component contains:

- the currently accessible record-register value(s);
- the declared readout/register identity;
- record-profile or accessibility information derivable under the experiment interface.

Current Actuality is the current microstate or explicitly declared local projection of it.

Potentiality is reintroduced explicitly only after the record-only causal factor is isolated, to avoid confounding Stage 2 future semantics with Stage 3 record asymmetry.

## 19. Stage 2 integration rule

Stage 3A–3D must not multiply the experiment matrix by immediately combining:

`epistemic/ontic Potentiality x record asymmetry x history reversal`.

First isolate the record effect in the common reversible substrate.

Later, Stage 3E/G may attach the same record layer to both Stage 2 model families. If the same record-arrow structure appears in both, that supports independence from fixed/open-future formal semantics within the tested model. If they differ, the source of the difference must be isolated before interpretation.

## 20. Global-to-local projection

For a current position `k`, define a projection:

`F_k : B_3 -> G_k^rec`

and later:

`F_k : B_3 -> G_k`.

The projection must state exactly what the local view receives.

Privileged global data such as the complete trajectory, initial boundary variables, or opposite-side microstates must not be silently included in the local record-bearing view.

Stage 3 must classify:

- locally accessible information;
- globally represented but locally hidden information;
- information reconstructible from a family of views;
- ambiguous information;
- information lost under the chosen projection.

## 21. Forward/reverse covariance requirement

History reversal must transform the record profile consistently.

At the central position in the canonical three-position trajectory, reversal swaps the two comparison sides. Therefore the signed score should obey:

`A_R(J_* mu) = - A_R(mu)`

for the canonical setup.

This is a transformation property of the defined diagnostic. It is not yet a fundamental physical time-reversal theorem.

## 22. Register and event relabeling controls

Pure renaming of event/position identifiers or register names must not create or destroy a record arrow when the corresponding bijection is applied consistently.

The relevant requirement is covariance under declared bookkeeping relabelings, not raw equality of differently named structures.

This is not yet invariance under physical coordinate changes, clock changes, or quantum reference frames.

## 23. State identity guard

The Stage 1/2 rule remains active:

`state equality != event identity`.

The same bit value may recur at several ordered positions. A repeated value must not collapse distinct trajectory positions or be counted as a record merely because two values happen to match.

## 24. Canonical Stage 3 experiment sequence

### Stage 3A — reversible record substrate

Implement and verify:

- three-bit microstate;
- exact finite ensemble;
- `U_rec` and `U_scr`;
- bijectivity/inverse maps on all microstates;
- forward trajectories;
- exact reversed trajectories;
- full-state entropy preservation.

No temporal arrow is claimed yet.

### Stage 3B — record diagnostics

Implement:

- entropy;
- mutual information;
- conditional entropy;
- Bayes-optimal decoding accuracy;
- record profile `Q_R(k,j)`;
- signed scores `A_R` and `A_Acc`.

Verify that the diagnostic itself does not call lower indices “past.”

### Stage 3C — asymmetric-record model

Use the blank-memory boundary and verify the canonical directional asymmetry.

Expected:

`I(M_1;X_0)=1`

`I(M_1;X_2)=0`

`A_R>0`.

The strongest allowed conclusion is a **record-defined orientation** in this ensemble.

### Stage 3D — reversal and symmetric controls

Verify:

- reverse ensemble flips the score sign;
- symmetric forward/reverse mixture removes the signed bias;
- order-only/no-record control yields no record arrow;
- nonblank/uniform initial memory removes or weakens the canonical record.

### Stage 3E — complete local view

Upgrade toward:

`G_k=(Records_k,Actuality_k,Potentiality_k)`.

Define exact global-to-local projections and reintroduce Potentiality without changing the already-tested record semantics.

### Stage 3F — accessibility and information controls

Compare record mutual information and decoder accessibility across both sides of the current position. Add noise/degradation controls only after the exact noiseless baseline is established.

### Stage 3G — robustness and synthesis

At minimum include:

- event/register renaming;
- repeated values/state labels;
- boundary-condition variants;
- forward/reverse balance variants;
- noise where informative;
- Stage 2 epistemic/ontic integration if it remains identifiable;
- full repository regression;
- `results/stage3_synthesis.md`;
- answers to the six fixed questions.

## 25. Required negative controls

Stage 3 is not complete with only a positive asymmetric example.

Required negative/control cases:

1. same neutral order with no record coupling;
2. exact history reversal;
3. equal forward/reverse mixture;
4. nonblank/uniform memory boundary;
5. bookkeeping relabeling;
6. repeated state values;
7. invalid/non-bijective dynamics rejected where reversibility is claimed.

## 26. Interpretation hierarchy

Use the following vocabulary carefully.

### Established by a successful Stage 3 toy experiment

Potentially established if tests succeed:

- the microdynamics are reversible;
- the declared ensemble has a measurable record asymmetry;
- the signed record score reverses under history reversal;
- the symmetric control has no signed bias;
- local record accessibility is directionally asymmetric under the chosen interface.

### Candidate interpretation

A nonzero robust signed record/accessibility score may be called:

- `record-defined temporal orientation`;
- `local information-accessibility arrow`;
- `candidate arrow-like structure`.

### Not established

Do not call it:

- the fundamental arrow of physical time;
- proof that becoming is ontologically fundamental;
- proof of thermodynamic irreversibility;
- proof of an open future;
- explanation of phenomenal passage.

## 27. Stage 3 fixed questions

Stage 3 must end by answering:

1. What is the block-like/global description `B_3`?
2. What is the record-bearing becoming-like/local description `G_k`?
3. What is the transformation `F_k : B_3 -> G_k`?
4. Is `F_k` reversible, and what information is hidden/discarded?
5. What is strictly transformation-stable, reconstructible, ambiguous, lost, or locally accessible?
6. What physical meaning, if any, can be assigned to the surviving record/accessibility structure?

## 28. Stage 3 exit criteria

Stage 3 is complete only when all of the following are satisfied.

1. `order`, `reversibility`, `record asymmetry`, and `experienced direction` remain formally distinct.
2. The canonical microscopic updates are explicitly bijective and tested over the full microstate space.
3. The blank-memory asymmetric boundary ensemble is explicit.
4. Record diagnostics are defined from ensemble statistics rather than accidental single-trajectory equality.
5. A signed record/accessibility orientation is measured without defining lower indices as “past.”
6. Exact history reversal flips the signed orientation where expected.
7. A symmetric forward/reverse control removes the signed bias.
8. An order-only/no-record control demonstrates that ordering alone does not force the arrow score.
9. Boundary-condition controls distinguish reversible law from asymmetric record preparation.
10. Full-state entropy preservation is separated from subsystem entropy/correlation changes.
11. `G=(Records,Actuality,Potentiality)` is implemented without conflating Records with Potentiality.
12. The global-to-local projection and its information loss are explicit.
13. Bookkeeping renaming and repeated-value controls pass.
14. Stage 2 integration, if performed, does not erase the epistemic/ontic distinctions by accident.
15. Full repository regression passes.
16. `results/stage3_synthesis.md` answers the six fixed questions and states all interpretation limits.

## 29. Stop / revise conditions

Revise the protocol rather than forcing a positive result if:

- the arrow score merely restates the chosen index orientation;
- the claimed record is only a single-trajectory value coincidence;
- a supposedly reversible update is not bijective on the complete microstate space;
- history reversal is implemented only as Python iteration order rather than as a model transformation;
- the symmetric control retains an unexplained signed bias;
- global entropy change is produced by an implementation error in a bijective closed model;
- record asymmetry disappears under every nontrivial control;
- a claimed physical arrow is actually only a boundary-condition convention;
- the Stage 3 result duplicates a known standard information-theoretic object without adding a useful representational comparison.

## 30. Core methodological summary

Stage 3 starts from the deliberately conservative claim:

`ordered change alone does not define a temporal arrow`.

It then asks whether:

`reversible dynamics + asymmetric record boundary`

can produce:

`record-defined local orientation`

while the corresponding reversed and symmetric controls behave as required.

Even if successful:

`record-defined orientation != fundamental physical time`.
