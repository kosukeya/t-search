# Stage 6 Concepts — Typed Temporal Structure Vocabulary

Status: **frozen for Stage 6.0; provisional at the project level**.

This note is a compact companion to `stage6_protocol.md`. It fixes names and type distinctions used by Stages 6A--6G without asserting that the listed concepts are fundamental constituents of time.

## 1. Temporal role versus representation

A **temporal role** is a function a structure may play, such as ordering events, selecting an orientation, encoding possible extensions, connecting perspectives, or preserving predictions.

A **representation** is one mathematical realization of that role in a declared model.

Frozen guard:

`same temporal role != same mathematical representation`.

Likewise:

`same mathematical representation != same physical temporal role`.

## 2. Layer symbols

- `O`: order / succession structure.
- `P`: perspectives and admissible perspective transformations.
- `R`: records, record-defined direction, and accessibility.
- `V`: Potentiality / modality / extension structure.
- `Omega`: operational correspondences and prediction-preserving comparison rules.
- `Xi`: compatibility conditions among the other layers.

The provisional container is:

`T6=(O,P,R,V,Omega;Xi)`.

This is an analysis scaffold, not a final definition of time.

## 3. Perspective object

A perspective is written:

`p=(view/frame, local coordinate/interface, physical/support domain metadata)`.

A perspective may fail to exist globally, may overlap only partially with another perspective, or may exist even when no primitive direct map to another perspective is declared.

## 4. Horizontal morphism

A horizontal morphism is a perspective transformation:

`M_{q<-p}: G_p -> G_q`.

Its meaning is:

> transport a valid description from perspective `p` to corresponding description in perspective `q`.

Stage 5 supplies explicit invertible support-space examples.

It is not a claim that `q` occurs after `p`.

## 5. Vertical relation / morphism

A vertical relation or map represents declared temporal, causal, succession, or conditioning structure inside a perspective/domain:

`D_p(e2<-e1)`

or:

`e1 <=_p e2`.

Its exact semantics must be declared per model.

No generic Stage 6 API may silently reinterpret a horizontal map as a vertical one or vice versa.

## 6. Event correspondence

A cross-perspective event correspondence is:

`chi_{q<-p}: E_p -> E_q`.

`chi` is separate from the state/description map `M`.

It may be:

- total;
- partial;
- bijective;
- many-to-one;
- orientation-preserving;
- orientation-reversing;
- undefined.

Equal numeric clock coordinates never create `chi` automatically.

## 7. Compatibility square

When both arrow types and event correspondence are meaningful, a candidate commuting relation is:

`M^{e2}_{q<-p} D_p(e2<-e1) = D_q(chi(e2)<-chi(e1)) M^{e1}_{q<-p}`.

A successful square means that the two typed structures are mutually compatible under the declared correspondence.

It does not make them identical structures.

## 8. Perspective atlas

A perspective atlas is a network:

`A=(Perspectives, admissible direct maps, overlap/support metadata)`.

A **complete atlas** has a primitive direct map for every requested pair.

A **partial atlas** need not.

An indirect map may be reconstructible by composition when a valid path exists.

Frozen distinctions:

- `direct map absent != target perspective absent`;
- `indirect reconstructibility != direct local accessibility`;
- `connected atlas != universal physical frame availability`.

## 9. Path and loop consistency

For two paths from `p` to `q`, path consistency means the induced maps agree on their common declared support/interface.

For a closed loop at `p`, an ideal consistency residual may be:

`H_loop=||M_loop-I_p||`.

`H_loop ~= 0` means the declared atlas is algebraically path-consistent within tolerance.

It is not automatically spacetime flatness.

`H_loop != 0` is not automatically physical curvature.

## 10. Record orientation

A record orientation diagnostic such as:

`A_R=I(record;past)-I(record;future)`

is an information/record asymmetry defined relative to a declared history/event correspondence.

It is distinct from:

- neutral order;
- dynamical irreversibility;
- causal influence;
- modal openness;
- phenomenal passage.

## 11. Accessibility

A structure can exist in the global/formal state while being unavailable to a declared local interface.

Stage 6 therefore distinguishes:

- `exists/formally encoded`;
- `reconstructible with theory + family of views`;
- `accessible to one declared local perspective`.

These are different statuses.

## 12. Potentiality / modal extension

For partial description `D`, write:

`Ext(D)`

for a declared set/family of compatible extensions.

This notation does not determine whether the extensions are:

- epistemic alternatives;
- nomologically possible alternatives;
- ontologically open futures.

The modal semantics must be carried as metadata rather than inferred from set cardinality or sampling.

## 13. Operational correspondence

Operational objectivity in Stage 6 means consistency of corresponding predictions under explicit transport rules, not equality of every local representation.

For the Stage 5 quantum instance:

`rho_q=M rho_p M^dagger`,

`O_q=M O_p M^dagger`,

`Tr(rho_p O_p)=Tr(rho_q O_q)`.

The general Stage 6 concept `Omega` abstracts the correspondence rule, not necessarily the Hilbert-space formula.

## 14. Independence status

An implication `A => B` can receive one of three statuses:

### `refuted`

An executable witness satisfies `A` but not `B` under the frozen definitions.

### `supported_in_declared_family`

All declared witnesses currently satisfying `A` also satisfy `B`.

This is not a universal theorem.

### `not_established`

Current witnesses do not decide the implication.

Frozen guard:

`not_established != refuted`.

## 15. Ablation status

When a layer is removed/neutralized, Stage 6 records the resulting role as one of:

- `preserved`;
- `reconstructible`;
- `inaccessible`;
- `lost`;
- `not_applicable`;
- `not_established`.

The software becoming inconvenient after an ablation is not evidence that the removed layer is metaphysically fundamental.

## 16. Candidate outcome classes for Stage 6G

Stage 6G must choose among at least these outcome types:

### A. Single minimal structure

Several provisional layers are shown executablely to reduce to one smaller structure plus derived quantities.

### B. Layered temporal structure

Multiple independently necessary roles remain, tied by nontrivial compatibility conditions `Xi`.

### C. Complementary family

No single minimal `T` is justified; several structures capture different temporal roles without a demonstrated reduction among them.

### D. Inconclusive

The available toy models/adapters are too heterogeneous to support a reliable minimality conclusion.

Stage 6G may introduce a more precise outcome class if justified, but it may not force A merely for conceptual elegance.

## 17. Current hypothesis, not result

The working hypothesis entering Stage 6A is:

> the Stage 5 perspective atlas is likely an objectivity/perspective layer rather than the whole of temporal structure; Stage 3 records may supply a separate direction layer, Stage 2 may supply an independent modal layer, and neutral order may remain separate from both.

This hypothesis must be pressure-tested by executable independence, compatibility, and ablation witnesses.
